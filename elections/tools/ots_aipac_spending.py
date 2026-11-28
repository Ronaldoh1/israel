#!/usr/bin/env python3
"""
OTS: the AIPAC network's election and influence spending, 2016-2026.

Run it on your own computer (Python 3.8+, nothing to install), in the folder you want the data in:
    FEC_API_KEY=yourkey python3 ots_aipac_spending.py
Options:
    --only fec,lobbying,990     run only some steps
    --cycles 2022,2024          only some election cycles (default 2016-2026)
    --min-donation 200          how small a donation to UDP / AIPAC PAC to list (default $1,000)

What it collects, all from public filings:
  FEC (AIPAC PAC and United Democracy Project, its super PAC), cycle by cycle:
     totals; every disbursement (contributions to candidates, earmarked donations forwarded,
     ad buys, consultants, events, travel...) with the recipient's party, office and state;
     every independent expenditure FOR or AGAINST a candidate, with party, race, purpose and vendor;
     donors of $1,000+.
  Lobbying (Senate LD-2 reports): AIPAC's reported lobbying spending each quarter, issues and bills lobbied.
  IRS Form 990s (via ProPublica Nonprofit Explorer): AIPAC and the American Israel Education Foundation
     (the AIPAC affiliate that pays for congressional trips to Israel): revenue, spending, pay, with links to the full filings.

Before AIPAC PAC (Dec 2021) and UDP (Jan 2022) existed, AIPAC itself did not give to campaigns; those
cycles show lobbying and nonprofit spending only. Safe to stop and re-run: finished pieces are reused.
Big shared downloads come from ~/Desktop/2026races if that folder exists.
"""
import csv, io, json, os, re, ssl, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request, zipfile
from datetime import datetime, timezone

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

# ---------------------------------------------------------------- helpers
def log(*a): print(*a, flush=True)
def _ctx():
    try:
        import certifi; return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()
CTX = _ctx()
CERT_HELP = ('\n  SSL certificate problem. On a Mac, open Applications > Python 3.x and double-click "Install Certificates.command"'
             '\n  (or run: pip3 install certifi), then run this again.\n')

class NetworkDown(Exception):
    """the connection stayed down; nothing partial gets saved, and running the same command again continues"""

def fetch(url, dest=None, headers=None, tries=4, quiet=False, patience=1800):
    """GET a URL to bytes, or stream it to a file (re-uses a finished file). Returns None only for a definite answer
    such as 'not found'. If the connection drops it waits up to `patience` seconds for it to come back, then raises NetworkDown."""
    if dest and os.path.exists(dest) and os.path.getsize(dest) > 0: return dest
    h = {'User-Agent': UA, 'Accept': '*/*'}; h.update(headers or {})
    i = 0; down_since = None; k = 0
    while i < tries:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), context=CTX, timeout=180) as r:
                if not dest: return r.read()
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                total = int(r.headers.get('Content-Length') or 0); got = 0; last = time.time()
                with open(dest + '.part', 'wb') as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b: break
                        f.write(b); got += len(b)
                        if total > 20e6 and time.time() - last > 5: log(f'      {got / 1e6:.0f} of {total / 1e6:.0f} MB'); last = time.time()
            os.replace(dest + '.part', dest); return dest
        except urllib.error.HTTPError as e:
            down_since = None
            if e.code == 429 or e.code >= 500:
                i += 1; wait = 30 * i; log(f'    busy ({e.code}); waiting {wait}s'); time.sleep(wait); continue
            if not quiet: log(f'    HTTP {e.code}: {url.split("api_key=")[0]}')
            return None
        except (ssl.SSLError, ssl.CertificateError):
            log(CERT_HELP); raise SystemExit(1)
        except Exception as e:
            if isinstance(getattr(e, 'reason', None), ssl.SSLError) or 'CERTIFICATE' in str(e).upper(): log(CERT_HELP); raise SystemExit(1)
            down_since = down_since or time.time()
            if time.time() - down_since > patience: raise NetworkDown(str(getattr(e, 'reason', e)))
            wait = min(60, 5 * 2 ** k); k += 1
            log(f'    connection problem ({getattr(e, "reason", e)}); waiting {wait}s for it to come back'); time.sleep(wait)
    raise NetworkDown(f'the server kept answering "busy" for {url.split("?")[0]}')

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z ]+', ' ', s.replace('-', ' ')).split()
def slug(s): return '-'.join(norm(s)) or 'x'
def money(x):
    try: return round(float(x or 0), 2)
    except ValueError: return 0.0
def wcsv(path, head, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f: w = csv.writer(f); w.writerow(head); w.writerows(rows)
def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- what to collect
VERSION = '1.0 (2026-10-13)'
ROOT = os.path.abspath('aipac-data')
SIBLING_DL = [os.path.expanduser('~/Desktop/2026races/2026elections-data/_downloads'), os.path.abspath('2026elections-data/_downloads')]
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
CYCLES = [2016, 2018, 2020, 2022, 2024, 2026]
API = 'https://api.open.fec.gov/v1'
FEC = 'https://www.fec.gov/files/bulk-downloads/{y}/{f}'
PROPUBLICA = 'https://projects.propublica.org/nonprofits/api/v2'
LDA_BASES = ['https://lda.senate.gov/api/v1', 'https://lda.gov/api/v1']

# The AIPAC network's federal election committees (ids checked against the FEC at run time; found by name if they differ)
FEC_COMMITTEES = [
    {'key': 'aipac_pac', 'id': 'C00797670', 'expect': 'AMERICAN ISRAEL PUBLIC AFFAIRS', 'label': 'AIPAC PAC', 'role': 'PAC: direct contributions and earmarked (bundled) donations'},
    {'key': 'udp', 'id': 'C00799031', 'expect': 'UNITED DEMOCRACY PROJECT', 'label': 'United Democracy Project', 'role': "AIPAC's super PAC: ads and other spending for or against candidates"},
]
# Nonprofits whose IRS filings show the rest of the spending (lobbying, conferences, sponsored travel)
NONPROFITS = [
    {'key': 'aipac', 'search': 'American Israel Public Affairs Committee', 'label': 'AIPAC (501(c)(4) lobbying organization)'},
    {'key': 'aief', 'search': 'American Israel Education Foundation', 'label': 'American Israel Education Foundation (501(c)(3) that funds congressional trips)'},
]
LDA_CLIENTS = ['American Israel Public Affairs Committee']

CN = 'CAND_ID CAND_NAME CAND_PTY_AFFILIATION CAND_ELECTION_YR CAND_OFFICE_ST CAND_OFFICE CAND_OFFICE_DISTRICT CAND_ICI CAND_STATUS CAND_PCC CAND_ST1 CAND_ST2 CAND_CITY CAND_ST CAND_ZIP'.split()
CM = 'CMTE_ID CMTE_NM TRES_NM CMTE_ST1 CMTE_ST2 CMTE_CITY CMTE_ST CMTE_ZIP CMTE_DSGN CMTE_TP CMTE_PTY_AFFILIATION CMTE_FILING_FREQ ORG_TP CONNECTED_ORG_NM CAND_ID'.split()
PARTY = {'DEM': 'Democrat', 'REP': 'Republican', 'IND': 'Independent', 'LIB': 'Libertarian', 'GRE': 'Green', 'DFL': 'Democrat', 'NPA': 'No party', 'OTH': 'Other', 'UNK': 'Unknown'}

# ---------------------------------------------------------------- FEC API with complete-only caching
def api(path, key, **q):
    q['api_key'] = key
    b = fetch(f'{API}{path}?{urllib.parse.urlencode(q, doseq=True)}', headers={'Accept': 'application/json'})
    time.sleep(3.7)
    return json.loads(b) if b else None

def api_all(path, key, cache, **q):
    """every page of a FEC API list; saved only when complete"""
    if os.path.exists(cache): return json.load(open(cache))
    rows, last, pages = [], {}, 0
    while True:
        d = api(path, key, per_page=100, **q, **last)
        if d is None: log(f'    incomplete (not saved; retried next run): {path} {q}'); return None
        res = d.get('results') or []
        rows += res; pages += 1
        if pages % 20 == 0: log(f'      {len(rows)} rows so far')
        li = (d.get('pagination') or {}).get('last_indexes')
        pg = d.get('pagination') or {}
        if not res or (not li and pg.get('page', 1) >= pg.get('pages', 1)): break
        if li: last = li
        else: q['page'] = pg.get('page', 1) + 1
    os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(rows, open(cache, 'w'))
    return rows

def resolve(cmte, key, dl):
    d = api(f'/committee/{cmte["id"]}/', key)
    r = (d or {}).get('results') or []
    if r and cmte['expect'] in (r[0].get('name') or '').upper():
        return cmte['id'], r[0].get('name'), r[0].get('first_file_date')
    d = api('/committees/', key, q=cmte['expect'], per_page=20)
    for c in (d or {}).get('results') or []:
        if cmte['expect'] in (c.get('name') or '').upper(): return c['committee_id'], c.get('name'), c.get('first_file_date')
    return None, None, None

# ---------------------------------------------------------------- who is a recipient (candidate, party, office)
class Directory:
    def __init__(self, dl, key):
        self.dl, self.key = dl, key; self.cand = {}; self.cmte = {}; self.cache = {}
        n = 0
        for y in CYCLES:
            for f, cols, store, idk in ((f'cn{str(y)[2:]}.zip', CN, self.cand, 'CAND_ID'), (f'cm{str(y)[2:]}.zip', CM, self.cmte, 'CMTE_ID')):
                p = os.path.join(dl, 'fec', str(y), f)
                if not os.path.exists(p): p = fetch(FEC.format(y=y, f=f), p, quiet=True)
                if not p: continue
                try: z = zipfile.ZipFile(p)
                except zipfile.BadZipFile: continue
                m = [x for x in z.namelist() if x.lower().endswith('.txt')]
                if not m: continue
                for line in io.TextIOWrapper(z.open(m[0]), encoding='latin-1', newline=''):
                    r = dict(zip(cols, line.rstrip('\r\n').split('|'))); store[r.get(idk, '')] = r; n += 1
        log(f'  candidate and committee directory: {len(self.cand)} candidates, {len(self.cmte)} committees')
    def candidate(self, cand_id):
        c = self.cand.get(cand_id or '')
        if not c: return {}
        off = {'H': 'House', 'S': 'Senate', 'P': 'President'}.get(c.get('CAND_OFFICE'), c.get('CAND_OFFICE', ''))
        return {'candidate_id': cand_id, 'candidate': c.get('CAND_NAME', ''), 'party': PARTY.get(c.get('CAND_PTY_AFFILIATION', ''), c.get('CAND_PTY_AFFILIATION', '')),
                'office': off, 'state': c.get('CAND_OFFICE_ST', ''), 'district': c.get('CAND_OFFICE_DISTRICT', '') if off == 'House' else ''}
    def by_committee(self, cmte_id):
        m = self.cmte.get(cmte_id or '')
        if not m: return {}
        if m.get('CAND_ID'): return self.candidate(m['CAND_ID'])
        return {'party': PARTY.get(m.get('CMTE_PTY_AFFILIATION', ''), m.get('CMTE_PTY_AFFILIATION', '')), 'committee_name': m.get('CMTE_NM', '')}

# ---------------------------------------------------------------- 1. FEC committees
def run_fec(key, dl, D, cycles, min_donation):
    log('\n[1/3] FEC: AIPAC PAC and United Democracy Project')
    found = []
    for c in FEC_COMMITTEES:
        cid, name, first = resolve(c, key, dl)
        if not cid: log(f'  could not find {c["label"]} at the FEC; skipped'); continue
        log(f'  {c["label"]}: {cid} {name} (first filed {first})'); found.append(dict(c, id=cid, fec_name=name, first_filed=first))
        tot, dis, ies, don = [], [], [], []
        for y in cycles:
            if first and int(first[:4]) > y: continue      # did not exist yet
            base = os.path.join(dl, 'aipac_api', cid, str(y))
            t = api_all(f'/committee/{cid}/totals/', key, base + '_totals.json', cycle=y)
            for r in t or []: tot.append({'committee': c['label'], 'cycle': y, **{k: r.get(k) for k in ('receipts', 'disbursements', 'contributions', 'individual_contributions',
                         'other_political_committee_contributions', 'transfers_from_affiliated_committee', 'independent_expenditures', 'contributions_to_other_committees',
                         'operating_expenditures', 'cash_on_hand_end_period', 'coverage_start_date', 'coverage_end_date') if k in r}})
            log(f'  {c["label"]} {y}: spending')
            b = api_all('/schedules/schedule_b/', key, base + '_b.json', committee_id=cid, two_year_transaction_period=y)
            for r in b or []:
                who = D.by_committee(r.get('recipient_committee_id')) if r.get('recipient_committee_id') else {}
                desc = (r.get('disbursement_description') or r.get('memo_text') or '').upper()
                kind = ('Earmarked donations forwarded' if 'EARMARK' in desc or (r.get('memo_code') == 'X' and r.get('recipient_committee_id'))
                        else 'Contribution to a candidate or committee' if r.get('recipient_committee_id') else (r.get('disbursement_purpose_category') or 'OTHER').title())
                dis.append({'committee': c['label'], 'cycle': y, 'date': (r.get('disbursement_date') or '')[:10], 'amount': money(r.get('disbursement_amount')), 'kind': kind,
                            'purpose_category': r.get('disbursement_purpose_category') or '', 'description': r.get('disbursement_description') or '', 'memo': r.get('memo_code') or '',
                            'recipient': r.get('recipient_name') or '', 'recipient_committee_id': r.get('recipient_committee_id') or '',
                            'candidate': who.get('candidate', ''), 'candidate_id': who.get('candidate_id', ''), 'party': who.get('party', ''), 'office': who.get('office', ''),
                            'state': who.get('state', '') or r.get('recipient_state') or '', 'district': who.get('district', ''), 'filing': r.get('pdf_url') or ''})
            log(f'  {c["label"]} {y}: independent expenditures')
            e = api_all('/schedules/schedule_e/', key, base + '_e.json', committee_id=cid, cycle=y)
            for r in e or []:
                who = D.candidate(r.get('candidate_id')) or {}
                ies.append({'committee': c['label'], 'cycle': y, 'date': (r.get('expenditure_date') or r.get('dissemination_date') or '')[:10], 'amount': money(r.get('expenditure_amount')),
                            'for_or_against': {'S': 'FOR', 'O': 'AGAINST'}.get(r.get('support_oppose_indicator'), r.get('support_oppose_indicator') or ''),
                            'candidate': r.get('candidate_name') or who.get('candidate', ''), 'candidate_id': r.get('candidate_id') or '',
                            'party': PARTY.get(r.get('candidate_party') or '', r.get('candidate_party') or '') or who.get('party', ''),
                            'office': {'H': 'House', 'S': 'Senate', 'P': 'President'}.get(r.get('candidate_office') or '', r.get('candidate_office') or '') or who.get('office', ''),
                            'state': r.get('candidate_office_state') or who.get('state', ''), 'district': r.get('candidate_office_district') or who.get('district', ''),
                            'election': r.get('election_type') or r.get('election_type_full') or '', 'purpose': r.get('expenditure_description') or '',
                            'payee': r.get('payee_name') or '', 'memo': r.get('memo_code') or '', 'amendment': r.get('amendment_indicator') or '', 'filing': r.get('pdf_url') or ''})
            log(f'  {c["label"]} {y}: donors of ${min_donation:,}+')
            a = api_all('/schedules/schedule_a/', key, base + f'_a{min_donation}.json', committee_id=cid, two_year_transaction_period=y, min_amount=min_donation)
            for r in a or []:
                don.append({'committee': c['label'], 'cycle': y, 'date': (r.get('contribution_receipt_date') or '')[:10], 'amount': money(r.get('contribution_receipt_amount')),
                            'donor': r.get('contributor_name') or '', 'donor_type': r.get('entity_type_desc') or r.get('entity_type') or '', 'employer': r.get('contributor_employer') or '',
                            'occupation': r.get('contributor_occupation') or '', 'city': r.get('contributor_city') or '', 'state': r.get('contributor_state') or '',
                            'donor_committee_id': r.get('contributor_id') or '', 'memo': r.get('memo_code') or '', 'memo_text': r.get('memo_text') or '', 'filing': r.get('pdf_url') or ''})
        for name, rows in (('totals', tot), ('spending', dis), ('independent_expenditures', ies), ('donors', don)):
            if rows: wcsv(os.path.join(ROOT, f'fec_{c["key"]}_{name}.csv'), list(rows[0].keys()), [list(r.values()) for r in rows])
        log(f'  {c["label"]}: {len(dis)} spending rows, {len(ies)} independent expenditures, {len(don)} donor rows')
    wjson(os.path.join(ROOT, 'committees.json'), found)

# ---------------------------------------------------------------- 2. lobbying (LD-2 reports)
def run_lobbying(dl, cycles):
    log('\n[2/3] Lobbying reports (Senate LDA)')
    key = os.environ.get('LDA_API_KEY'); H = {'Accept': 'application/json'}
    if key: H['Authorization'] = f'Token {key}'
    base = next((b for b in LDA_BASES if fetch(f'{b}/filings/?page_size=1', headers=H, tries=2, quiet=True)), None)
    if not base: log('  the lobbying database did not answer; skipped (re-run later with --only lobbying)'); return
    rows, issues = [], []
    years = range(min(cycles) - 1, datetime.now().year + 1)
    for client in LDA_CLIENTS:
        for y in years:
            cache = os.path.join(dl, 'aipac_lda', f'{slug(client)}_{y}.json')
            if os.path.exists(cache): res = json.load(open(cache))
            else:
                res, url, ok = [], f'{base}/filings/?' + urllib.parse.urlencode({'client_name': client, 'filing_year': y, 'page_size': 25}), True
                while url:
                    b = fetch(url, headers=H, quiet=True); time.sleep(1 if key else 4.5)
                    if not b: ok = False; break
                    try: d = json.loads(b)
                    except ValueError: ok = False; break
                    res += d.get('results') or []; url = d.get('next')
                if not ok: log(f'    {y}: incomplete, not saved'); continue
                os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(res, open(cache, 'w'))
            for f in res:
                cl = (f.get('client') or {}).get('name', '') if isinstance(f.get('client'), dict) else ''
                if client.lower() not in cl.lower(): continue
                rows.append({'year': f.get('filing_year'), 'period': f.get('filing_period_display') or f.get('filing_period'), 'type': f.get('filing_type_display') or f.get('filing_type'),
                             'registrant': (f.get('registrant') or {}).get('name', '') if isinstance(f.get('registrant'), dict) else '', 'client': cl,
                             'income': money(f.get('income')), 'expenses': money(f.get('expenses')), 'posted': f.get('dt_posted') or '',
                             'filing': f.get('filing_document_url') or f.get('url') or ''})
                for act in f.get('lobbying_activities') or []:
                    issues.append({'year': f.get('filing_year'), 'period': f.get('filing_period_display') or f.get('filing_period'), 'issue': act.get('general_issue_code_display') or act.get('general_issue_code'),
                                   'description': (act.get('description') or '')[:1500], 'lobbied': '; '.join(e.get('name', '') for e in act.get('government_entities') or [] if isinstance(e, dict)),
                                   'lobbyists': '; '.join(' '.join(filter(None, [(l.get('lobbyist') or {}).get('first_name'), (l.get('lobbyist') or {}).get('last_name')])) for l in act.get('lobbyists') or [] if isinstance(l, dict))})
            log(f'  {client} {y}: {sum(1 for r in rows if r["year"] == y)} reports')
    if rows: wcsv(os.path.join(ROOT, 'lobbying_reports.csv'), list(rows[0].keys()), [list(r.values()) for r in rows])
    if issues: wcsv(os.path.join(ROOT, 'lobbying_issues.csv'), list(issues[0].keys()), [list(r.values()) for r in issues])

# ---------------------------------------------------------------- 3. IRS Form 990s (ProPublica Nonprofit Explorer)
def run_990(dl):
    log('\n[3/3] IRS Form 990 filings (via ProPublica Nonprofit Explorer)')
    summary = []
    for org in NONPROFITS:
        cache = os.path.join(dl, 'aipac_990', f'{org["key"]}.json')
        if os.path.exists(cache): data = json.load(open(cache))
        else:
            b = fetch(f'{PROPUBLICA}/search.json?' + urllib.parse.urlencode({'q': org['search']}))
            hits = (json.loads(b) if b else {}).get('organizations') or []
            hit = next((h for h in hits if org['search'].lower() == (h.get('name') or '').lower()), None) or next((h for h in hits if org['search'].lower() in (h.get('name') or '').lower()), None)
            if not hit: log(f'  {org["label"]}: not found'); continue
            b = fetch(f'{PROPUBLICA}/organizations/{hit["ein"]}.json')
            if not b: log(f'  {org["label"]}: could not download; retried next run'); continue
            data = json.loads(b); os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(data, open(cache, 'w'))
        o = data.get('organization') or {}
        wjson(os.path.join(ROOT, f'irs990_{org["key"]}.json'), data)
        for f in data.get('filings_with_data') or []:
            summary.append({'org': org['label'], 'ein': o.get('ein'), 'tax_year': f.get('tax_prd_yr'), 'period_end': f.get('tax_prd'), 'form': f.get('formtype'),
                            'revenue': f.get('totrevenue'), 'expenses': f.get('totfuncexpns'), 'contributions_received': f.get('totcntrbgfts'),
                            'officer_pay': f.get('compnsatncurrofcr'), 'other_salaries': f.get('othrsalwages'), 'assets_end': f.get('totassetsend'), 'pdf': f.get('pdf_url') or ''})
        log(f'  {org["label"]} (EIN {o.get("ein")}): {len(data.get("filings_with_data") or [])} filings with data, {len(data.get("filings_without_data") or [])} more as PDFs only')
    if summary: wcsv(os.path.join(ROOT, 'irs990_summary.csv'), list(summary[0].keys()), [list(r.values()) for r in summary])

def main():
    a = sys.argv[1:]
    key = os.environ.get('FEC_API_KEY') or (a[a.index('--fec-key') + 1] if '--fec-key' in a else None)
    only = set(a[a.index('--only') + 1].split(',')) if '--only' in a else {'fec', 'lobbying', '990'}
    min_donation = int(a[a.index('--min-donation') + 1]) if '--min-donation' in a else 1000
    cycles = [int(x) for x in a[a.index('--cycles') + 1].split(',')] if '--cycles' in a else CYCLES
    dl = next((d for d in SIBLING_DL if os.path.isdir(d)), os.path.join(ROOT, '_downloads'))
    os.makedirs(ROOT, exist_ok=True)
    log(f'OTS AIPAC spending collector {VERSION}: cycles {", ".join(map(str, cycles))}\n  saving to {ROOT}\n  downloads: {dl}')
    if 'fec' in only:
        if not key: log('\nFEC step needs your key:  FEC_API_KEY=yourkey python3 ots_aipac_spending.py'); return
        run_fec(key, dl, Directory(dl, key), cycles, min_donation)
    if 'lobbying' in only: run_lobbying(dl, cycles)
    if '990' in only: run_990(dl)
    with open(os.path.join(ROOT, '.gitignore'), 'w') as f: f.write('_downloads/\n*.part\n.DS_Store\n')
    wjson(os.path.join(ROOT, 'manifest.json'), {'script': 'ots_aipac_spending.py ' + VERSION, 'run_at': NOW, 'cycles': cycles, 'min_donation': min_donation,
          'sources': {'fec_api': API, 'fec_bulk': FEC, 'lobbying': LDA_BASES, 'irs990': PROPUBLICA}})
    log(f'\nFinished: {ROOT}\nPush that folder to GitHub (a new repo is fine) and send Claude the link to build the dashboard.')

if __name__ == '__main__':
    try:
        main()
    except NetworkDown as e:
        log(f'\nThe internet connection was down for 30 minutes ({e}).\nEverything finished so far is saved. Run the same command again to continue.')
        raise SystemExit(2)
