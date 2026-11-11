#!/usr/bin/env python3
"""
OTS 2026 Elections: the deep money record for every federal candidate on the November 3 ballot
(ballot_2026.csv in this folder). It fills every money field the scorecard uses that the earlier
collectors did not: who the individual donors are, where they work, how much came from in-state,
money bundled through interest-group conduits (earmarks), who paid for the outside groups in each
race, groups that spend without disclosing donors ("dark money"), electioneering ads, corporate and
union communication costs, and lobbyists' own contributions.

Run it on your own computer (Python 3.8+, nothing to install), from this folder:
    python3 ots_money_deep.py                       everything, 2026 cycle
    python3 ots_money_deep.py --cycles 2024,2026    more cycles (each adds a large download)
    python3 ots_money_deep.py --state GA            only some states (repeat for more)
    python3 ots_money_deep.py --only outside        only some steps
Steps:
  bulk      downloads the FEC's bulk files for each cycle: committees (cm), candidate-committee links (ccl),
            independent expenditures, electioneering communications, communication costs, other committees'
            receipts (oth, ~0.5-1 GB) and the itemized individual contributions (indiv, several GB). No key needed.
            Files already downloaded by the other collectors (~/Desktop/2026races, extras-data) are reused.
  outside   every independent expenditure FOR or AGAINST each candidate, by spender, with the spender's type;
            spenders that file as "independent expenditors" (FEC type I, usually nonprofits or individuals that
            do not report their donors to the FEC) are marked as not disclosing donors. Also electioneering
            communications and corporate/union communication costs naming the candidate.
  indiv     one pass through the itemized individual contributions: for each candidate's own committees the top
            donors, top employers, in-state share, and earmarks by conduit (money forwarded through a PAC such as
            AIPAC PAC, Club for Growth or J Street; ActBlue and WinRed are counted separately as processors).
            For every super PAC or outside group that spent $25,000+ in a ballot race: its top donors, including
            corporations, unions and nonprofits (organizations that may not disclose their own donors).
  oth       committee-to-committee money into those outside groups (which PACs and party committees funded them).
  lobbyists registered lobbyists' own contributions and honorary payments to each candidate (Senate LD-203
            reports, lda.gov). Optional free key: LDA_API_KEY.
  quarters  money raised per reporting period (needs FEC_API_KEY; one call per committee).
Output: money-deep/<STATE>/<candidate>/money_deep.json (+ csv files), and money-deep/summary.csv.
Every flag is a lead to verify, never a finding. Safe to stop and re-run: finished pieces are reused.
"""
import csv, io, json, os, re, ssl, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request, zipfile
from collections import defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.environ.get('OTS_MONEY_DIR') or os.path.join(HERE, 'money-deep'))
BALLOT = os.path.join(HERE, 'ballot_2026.csv')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
FEC = 'https://www.fec.gov/files/bulk-downloads/{y}/{f}'
API = 'https://api.open.fec.gov/v1'
LDA_BASES = ['https://lda.gov/api/v1', 'https://lda.senate.gov/api/v1']   # the Senate site was retired after 30 June 2026
STEPS = ['bulk', 'outside', 'indiv', 'oth', 'lobbyists', 'quarters']
PROCESSORS = {'C00401224': 'ActBlue', 'C00694323': 'WinRed'}       # payment processors, not interest groups
OUTSIDE_MIN = 25000                                               # outside groups whose donors we list
CM = 'CMTE_ID CMTE_NM TRES_NM CMTE_ST1 CMTE_ST2 CMTE_CITY CMTE_ST CMTE_ZIP CMTE_DSGN CMTE_TP CMTE_PTY_AFFILIATION CMTE_FILING_FREQ ORG_TP CONNECTED_ORG_NM CAND_ID'.split()
CCL = 'CAND_ID CAND_ELECTION_YR FEC_ELECTION_YR CMTE_ID CMTE_TP CMTE_DSGN LINKAGE_ID'.split()
ITEM = 'CMTE_ID AMNDT_IND RPT_TP TRANSACTION_PGI IMAGE_NUM TRANSACTION_TP ENTITY_TP NAME CITY STATE ZIP_CODE EMPLOYER OCCUPATION TRANSACTION_DT TRANSACTION_AMT OTHER_ID TRAN_ID FILE_NUM MEMO_CD MEMO_TEXT SUB_ID'.split()
CMTE_TP = {'Q': 'PAC', 'N': 'PAC (nonqualified)', 'O': 'Super PAC', 'U': 'Single-candidate super PAC', 'V': 'Hybrid PAC', 'W': 'Hybrid PAC (nonqualified)',
           'X': 'Party (nonqualified)', 'Y': 'Party', 'Z': 'National party nonfederal account', 'H': 'House campaign', 'S': 'Senate campaign',
           'P': 'Presidential campaign', 'C': 'Communication cost filer', 'D': 'Delegate committee', 'E': 'Electioneering communication filer',
           'I': 'Independent expenditor (person or group; donors not reported to the FEC)'}
ORG_TP = {'C': 'Corporation', 'L': 'Labor organization', 'M': 'Membership organization', 'T': 'Trade association', 'V': 'Cooperative', 'W': 'Corporation without capital stock'}
ENTITY = {'IND': 'Individual', 'ORG': 'Organization (corporation, union or nonprofit)', 'COM': 'Committee', 'PAC': 'PAC', 'PTY': 'Party', 'CCM': 'Candidate committee', 'CAN': 'Candidate'}
NOT_EMPLOYER = re.compile(r'^(RETIRED|SELF[ -]?EMPLOYED|SELF|NOT EMPLOYED|NONE|N/?A|UNEMPLOYED|HOMEMAKER|INFORMATION REQUESTED.*|REQUESTED|STUDENT|DISABLED|)$')
COUNTRY_WORDS = r'ISRAEL|ZIONIST|NORPAC|AIPAC|UNITED DEMOCRACY PROJECT|J STREET|JACPAC|DEMOCRATIC MAJORITY FOR ISRAEL|PRO-ISRAEL|ARMENIA|ANCA|CUBA|INDIA|HINDU|PAKISTAN|UKRAIN|TAIWAN|KOREA|GREEK|HELLENIC|IRAN|PERSIAN|ARAB|PALESTIN|TURK|CHINA|CHINESE|PHILIPPIN|FILIPINO|VIETNAM|ETHIOPIA|ERITREA|KURD|SOMALI|HAITI|POLISH|POLAND|IRISH|ITALIAN|BALTIC|LITHUAN|LATVIA|ESTONIA'
COUNTRY_RX = re.compile(r'\b(' + COUNTRY_WORDS + r')', re.I)

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
class NetworkDown(Exception): pass

def fetch(url, dest=None, headers=None, tries=8, quiet=False, patience=3600):
    """GET a URL to bytes, or stream it to a file. Big downloads resume where they stopped (HTTP Range), so a dropped
    connection near the end of a multi-GB file does not start it over. Waits out rate limits (429) for up to an hour,
    and waits up to `patience` seconds for a dropped connection to come back before giving up (run again to continue)."""
    if dest and os.path.exists(dest) and os.path.getsize(dest) > 0: return dest
    i = 0; down_since = None; k = 0
    while i < tries:
        h = {'User-Agent': UA, 'Accept': '*/*'}; h.update(headers or {})
        part = (dest + '.part') if dest else None
        have = os.path.getsize(part) if part and os.path.exists(part) else 0
        if have: h['Range'] = f'bytes={have}-'
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), context=CTX, timeout=300) as r:
                if not dest: return r.read()
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                resumed = have and r.status == 206
                if have and not resumed: have = 0
                total = int(r.headers.get('Content-Length') or 0) + have; got = have; last = time.time()
                if resumed: log(f'      resuming at {have / 1e6:,.0f} MB')
                with open(part, 'ab' if resumed else 'wb') as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b: break
                        f.write(b); got += len(b)
                        if total > 20e6 and time.time() - last > 15: log(f'      {got / 1e6:,.0f} of {total / 1e6:,.0f} MB'); last = time.time()
                if total and got < total: raise ConnectionError(f'download cut short at {got / 1e6:,.0f} MB')
            os.replace(part, dest); return dest
        except urllib.error.HTTPError as e:
            down_since = None
            if e.code == 416 and part and os.path.exists(part): os.replace(part, dest); return dest      # already complete
            if e.code == 429:
                i += 1; wait = min(900, 120 * i); log(f'    rate limit reached; waiting {wait // 60} min'); time.sleep(wait); continue
            if e.code >= 500:
                i += 1; wait = 30 * i; log(f'    server busy ({e.code}); waiting {wait}s'); time.sleep(wait); continue
            if not quiet: log(f'    HTTP {e.code}: {url.split("api_key=")[0]}')
            return None
        except (ssl.SSLError, ssl.CertificateError):
            log(CERT_HELP); raise SystemExit(1)
        except Exception as e:
            if isinstance(getattr(e, 'reason', None), ssl.SSLError) or 'CERTIFICATE' in str(e).upper(): log(CERT_HELP); raise SystemExit(1)
            down_since = down_since or time.time()
            if time.time() - down_since > patience: raise NetworkDown(str(getattr(e, 'reason', e)))
            wait = min(60, 5 * 2 ** k); k += 1
            log(f'    connection problem ({getattr(e, "reason", e)}); waiting {wait}s'); time.sleep(wait)
    raise NetworkDown('the server kept answering "busy" for ' + url.split('?')[0])

def money(x):
    try: return round(float(x or 0), 2)
    except ValueError: return 0.0
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().upper()
    return re.sub(r'\s+', ' ', re.sub(r'[^A-Z0-9 &]+', ' ', s)).strip()
def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + '.tmp', 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(path + '.tmp', path)
def wcsv(path, head, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f: w = csv.writer(f); w.writerow(head); w.writerows(rows)
def zip_rows(path):
    try: z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        log(f'    {os.path.basename(path)} is damaged; removing it so the next run downloads it again')
        try: os.remove(path)
        except OSError: pass
        raise NetworkDown('damaged download removed: ' + os.path.basename(path))
    names = [n for n in z.namelist() if n.lower().endswith(('.txt', '.csv'))]
    for n in names:
        with z.open(n) as f:
            for line in io.TextIOWrapper(f, encoding='latin-1', newline=''):
                yield line.rstrip('\r\n').split('|')
def csv_rows(path):
    with open(path, encoding='latin-1', newline='') as f:
        for r in csv.DictReader(f): yield {(k or '').strip().lower(): (v or '').strip() for k, v in r.items()}

def shared_dirs():
    """bulk files the other collectors may already have downloaded"""
    home = os.path.expanduser('~')
    cands = [os.path.join(ROOT, '_downloads'), os.path.join(home, 'Desktop', '2026races', '_downloads'),
             os.path.join(os.path.dirname(HERE), 'extras-data', 'members-data', '_downloads'),
             os.path.join(os.path.dirname(HERE), 'extras-data', 'aipac-data', '_downloads')]
    return [d for d in cands if os.path.isdir(d)]
def bulk(y, f, required=True):
    for d in shared_dirs():
        p = os.path.join(d, 'fec', str(y), f)
        if os.path.exists(p) and os.path.getsize(p) > 0: return p
    dest = os.path.join(ROOT, '_downloads', 'fec', str(y), f)
    log(f'  downloading {f} ({y})')
    p = fetch(FEC.format(y=y, f=f), dest, quiet=not required)
    if not p and required: log(f'    {f} is not on the FEC site for {y}; that part is skipped for {y}.')
    return p

# ---------------------------------------------------------------- the ballot
class Cand:
    def __init__(self, r):
        self.r = r; self.st = r['state']; self.office = r['office']; self.name = r['name']
        self.id = r['data_id'] or ('%s-%s' % (r['race'].lower(), re.sub(r'[^a-z0-9]+', '-', r['name'].lower()).strip('-')))
        self.fec = [x.strip() for x in re.split(r'[ ;,|]+', r.get('fec_ids') or '') if x.strip()]
        self.cmtes = defaultdict(set)          # cycle -> own committee ids
    def folder(self): return os.path.join(ROOT, self.st, self.id)
def load_ballot(states):
    out = []
    for r in csv.DictReader(open(BALLOT, encoding='utf-8')):
        if states and r['state'] not in states: continue
        out.append(Cand(r))
    return out

def load_committees(cycles):
    info = {}
    for y in cycles:
        p = bulk(y, f'cm{str(y)[2:]}.zip')
        if not p: continue
        for v in zip_rows(p):
            if len(v) < 15: continue
            d = dict(zip(CM, v)); info[d['CMTE_ID']] = d
    return info
def link_committees(cands, cycles):
    by_cand = defaultdict(list)
    for c in cands:
        for i in c.fec: by_cand[i].append(c)
    for y in cycles:
        p = bulk(y, f'ccl{str(y)[2:]}.zip')
        if not p: continue
        for v in zip_rows(p):
            if len(v) < 7: continue
            d = dict(zip(CCL, v))
            for c in by_cand.get(d['CAND_ID'], []):
                if d['CMTE_DSGN'] in ('P', 'A'): c.cmtes[y].add(d['CMTE_ID'])
    return sum(1 for c in cands if any(c.cmtes.values()))

def cm_label(info, cid):
    d = info.get(cid) or {}
    t = CMTE_TP.get(d.get('CMTE_TP', ''), d.get('CMTE_TP', '') or 'unknown')
    org = ORG_TP.get(d.get('ORG_TP', ''), '')
    return {'id': cid, 'name': d.get('CMTE_NM', cid), 'type': t, 'connected_org': d.get('CONNECTED_ORG_NM', ''), 'org_type': org,
            'discloses_donors_to_fec': d.get('CMTE_TP') != 'I',
            'foreign_policy_flag': bool(COUNTRY_RX.search((d.get('CMTE_NM', '') + ' ' + d.get('CONNECTED_ORG_NM', '')))),
            'corporate_or_trade': d.get('ORG_TP') in ('C', 'T', 'W')}

# ---------------------------------------------------------------- outside money
def step_outside(cands, cycles, info, state):
    log('\n[outside] Independent expenditures, electioneering communications and communication costs')
    byfec = defaultdict(list)
    for c in cands:
        for i in c.fec: byfec[i].append(c)
    big_spenders = defaultdict(float)
    for y in cycles:
        res = {c.id: {'support': defaultdict(float), 'oppose': defaultdict(float), 'rows': []} for c in cands}
        p = bulk(y, f'independent_expenditure_{y}.csv')
        seen = {}
        if p:
            for d in csv_rows(p):
                if d.get('cand_id') not in byfec: continue
                key = (d.get('spe_id'), d.get('tran_id') or d.get('image_num'))
                seen[key] = d                               # the latest amendment of each expenditure wins
            for d in seen.values():
                for c in byfec[d['cand_id']]:
                    side = 'support' if d.get('sup_opp') == 'S' else 'oppose' if d.get('sup_opp') == 'O' else None
                    if not side: continue
                    amt = money(d.get('exp_amo')); res[c.id][side][d['spe_id']] += amt
                    res[c.id]['rows'].append([y, d.get('exp_date') or d.get('dissem_dt'), d['spe_id'], d.get('spe_nam'), side, amt, d.get('pur'), d.get('pay'), d.get('image_num')])
        ec = defaultdict(list)
        p2 = bulk(y, f'ElectioneeringComm_{y}.csv', required=False)
        if p2:
            for d in csv_rows(p2):
                cid = d.get('cand_id') or d.get('candidate_id')
                if cid in byfec:
                    for c in byfec[cid]: ec[c.id].append([y, d.get('disb_dt') or d.get('communication_date') or d.get('pub_distrib_dt'), d.get('cmte_id') or d.get('committee_id'),
                                                          d.get('cmte_nm') or d.get('committee_name'), money(d.get('calculated_cand_share') or d.get('reported_disb_amt') or d.get('disb_amt')), d.get('disb_desc') or d.get('purpose', '')])
        cc = defaultdict(list)
        p3 = bulk(y, f'CommunicationCosts_{y}.csv', required=False)
        if p3:
            for d in csv_rows(p3):
                cid = d.get('s_o_cand_id') or d.get('cand_id') or d.get('candidate_id')
                if cid in byfec:
                    for c in byfec[cid]: cc[c.id].append([y, d.get('communication_dt') or d.get('transaction_dt'), d.get('cmte_id') or d.get('committee_id'),
                                                          d.get('cmte_nm') or d.get('committee_name'), d.get('s_o_ind') or d.get('support_oppose_indicator'), money(d.get('communication_cost') or d.get('transaction_amt'))])
        for c in cands:
            R = res[c.id]
            if not (R['rows'] or ec.get(c.id) or cc.get(c.id)): continue
            def side(s):
                L = []
                for sid, amt in sorted(R[s].items(), key=lambda kv: -kv[1]):
                    lab = cm_label(info, sid); lab['amount'] = round(amt, 2); L.append(lab)
                    if amt >= OUTSIDE_MIN: big_spenders[sid] += amt
                return L
            out = {'cycle': y, 'support': side('support'), 'oppose': side('oppose'),
                   'non_disclosing_spending': round(sum(a for s in ('support', 'oppose') for k, a in R[s].items() if not cm_label(info, k)['discloses_donors_to_fec']), 2),
                   'electioneering_communications': ec.get(c.id, []), 'communication_costs': cc.get(c.id, [])}
            state.setdefault(c.id, {}).setdefault('cycles', {}).setdefault(str(y), {})['outside'] = out
            if R['rows']: wcsv(os.path.join(c.folder(), f'outside_expenditures_{y}.csv'), ['cycle', 'date', 'spender_id', 'spender', 'side', 'amount', 'purpose', 'payee', 'fec_image'], R['rows'])
    log(f'  {len(big_spenders)} outside groups spent ${OUTSIDE_MIN:,}+ in a ballot race')
    return big_spenders

# ---------------------------------------------------------------- itemized individual contributions
def top(d, n): return sorted(d.items(), key=lambda kv: -kv[1])[:n]
def step_indiv(cands, cycles, info, spenders, state):
    log('\n[indiv] Itemized individual contributions (one pass per cycle through a large file; allow 20-60 minutes)')
    for y in cycles:
        own = {}
        for c in cands:
            for cm in c.cmtes.get(y, ()): own[cm] = c
        targets = set(own) | set(spenders)
        done_flag = os.path.join(ROOT, '_downloads', f'indiv_{y}.done')
        if os.path.exists(done_flag) and all(str(y) in (state.get(c.id, {}).get('cycles', {})) and 'donors' in state[c.id]['cycles'][str(y)] for c in cands if c.cmtes.get(y)):
            log(f'  {y}: already done'); continue
        p = bulk(y, f'indiv{str(y)[2:]}.zip')
        if not p: continue
        donors = defaultdict(lambda: defaultdict(float)); emp = defaultdict(lambda: defaultdict(float)); occ = defaultdict(lambda: defaultdict(float))
        instate = defaultdict(float); total = defaultdict(float); ear = defaultdict(lambda: defaultdict(float)); proc = defaultdict(lambda: defaultdict(float))
        sdon = defaultdict(lambda: defaultdict(float)); sorg = defaultdict(lambda: defaultdict(float))
        n = 0; t0 = time.time()
        for v in zip_rows(p):
            n += 1
            if n % 5_000_000 == 0: log(f'    {n / 1e6:.0f} million rows read ({(time.time() - t0) / 60:.0f} min)')
            if len(v) < 21 or v[0] not in targets or v[18] == 'X': continue
            cm, amt = v[0], money(v[14])
            if amt == 0: continue
            if cm in own:
                c = own[cm]
                total[c.id] += amt
                if v[9] == c.st: instate[c.id] += amt
                donors[c.id][(norm(v[7]), (v[10] or '')[:5], norm(v[11]), norm(v[12]))] += amt
                e = norm(v[11])
                if not NOT_EMPLOYER.match(e): emp[c.id][e] += amt
                occ[c.id][norm(v[12]) or 'NOT GIVEN'] += amt
                conduit = v[15] if v[15].startswith('C') else ''
                if v[5] == '15E' or 'EARMARK' in v[19].upper():
                    if not conduit:
                        m = re.search(r'EARMARK\w*\s+(?:THROUGH|THRU|VIA|FROM)\s+(.+)', v[19].upper()); conduit = ('name:' + norm(m.group(1))) if m else 'unknown'
                    (proc if conduit in PROCESSORS else ear)[c.id][conduit] += amt
            if cm in spenders:
                key = (norm(v[7]), v[6] or 'IND', norm(v[11]))
                (sorg if v[6] == 'ORG' else sdon)[cm][key] += amt
        log(f'  {y}: read {n / 1e6:.1f} million rows')
        for c in cands:
            if not c.cmtes.get(y): continue
            S = state.setdefault(c.id, {}).setdefault('cycles', {}).setdefault(str(y), {})
            T = total.get(c.id, 0.0)
            S['donors'] = {'committees': sorted(c.cmtes[y]), 'itemized_individual_total': round(T, 2),
                           'instate_share': round(instate[c.id] / T, 4) if T else None,
                           'top_donors': [[k[0], round(a, 2), ', '.join(x for x in (k[3], k[2]) if x), k[1]] for k, a in top(donors[c.id], 50)],
                           'top_employers': [[k, round(a, 2)] for k, a in top(emp[c.id], 50)],
                           'top_occupations': [[k, round(a, 2)] for k, a in top(occ[c.id], 25)],
                           'earmarks_by_conduit': [dict(cm_label(info, k) if k.startswith('C') else {'id': '', 'name': k.replace('name:', ''), 'type': 'conduit (name only)', 'foreign_policy_flag': bool(COUNTRY_RX.search(k))}, amount=round(a, 2)) for k, a in top(ear[c.id], 100)],
                           'via_payment_processors': {PROCESSORS[k]: round(a, 2) for k, a in proc[c.id].items()},
                           'note': 'From the FEC itemized-contribution file (contributions over $200). Memo entries excluded. Totals can differ slightly from the FEC summary totals in fec_totals.json, which are authoritative.'}
        SP = {}
        for sid in spenders:
            SP[sid] = dict(cm_label(info, sid), donors_individual=[[k[0], round(a, 2), k[2]] for k, a in top(sdon[sid], 25)],
                           donors_organizations=[[k[0], round(a, 2), ENTITY['ORG']] for k, a in top(sorg[sid], 25)])
        wjson(os.path.join(ROOT, '_outside_groups', f'donors_{y}.json'), SP)
        os.makedirs(os.path.dirname(done_flag), exist_ok=True); open(done_flag, 'w').write(NOW)

def step_oth(cands, cycles, info, spenders):
    log('\n[oth] Committees that funded the outside groups')
    for y in cycles:
        p = bulk(y, f'oth{str(y)[2:]}.zip')
        if not p: continue
        got = defaultdict(lambda: defaultdict(float))
        for v in zip_rows(p):
            if len(v) < 21 or v[0] not in spenders or v[18] == 'X': continue
            if v[5].startswith('1') or v[5] in ('18G', '18J', '18K', '11'):          # receipts from other committees
                got[v[0]][(v[15] or norm(v[7]))] += money(v[14])
        path = os.path.join(ROOT, '_outside_groups', f'donors_{y}.json')
        SP = json.load(open(path)) if os.path.exists(path) else {}
        for sid, d in got.items():
            SP.setdefault(sid, cm_label(info, sid))['donors_committees'] = [dict(cm_label(info, k) if k.startswith('C') else {'name': k}, amount=round(a, 2)) for k, a in top(d, 25)]
        wjson(path, SP)

# ---------------------------------------------------------------- lobbyists (LD-203)
def step_lobbyists(cands, state):
    log('\n[lobbyists] Registered lobbyists\' contributions and honorary payments (LD-203)')
    key = os.environ.get('LDA_API_KEY'); H = {'Accept': 'application/json'}
    if key: H['Authorization'] = f'Token {key}'
    base = None
    for b in LDA_BASES:   # LDA.gov first, then the Senate's old address; a busy or retired address must not stop the run
        try:
            # probe with a small filtered query: the unfiltered list counts every filing and can time out (503)
            if fetch(f'{b}/contributions/?' + urllib.parse.urlencode({'contribution_honoree': 'Smith', 'filing_year': 2025, 'page_size': 1}), headers=H, tries=3, quiet=True): base = b; break
        except NetworkDown: log(f'  {b} is not answering; trying the next address')
    if not base: log('  the LD-203 database did not answer; skipped. Run again later with --only lobbyists.'); return
    log(f'  using {base}')
    pause = 1.0 if key else 4.5
    for i, c in enumerate(cands, 1):
        cache = os.path.join(ROOT, '_downloads', 'lda', f'{c.id}.json')
        if os.path.exists(cache): items = json.load(open(cache))
        else:
            last = norm(c.name).split()[-1]; first = norm(c.name).split()[0]
            items, url, pages, ok = [], f'{base}/contributions/?' + urllib.parse.urlencode({'contribution_honoree': last, 'page_size': 25}), 0, True
            while url and pages < 200:
                try: b = fetch(url, headers=H, quiet=True, tries=5)
                except NetworkDown:
                    log(f'  the LD-203 database stopped answering at candidate {i} of {len(cands)}; the rest are skipped this run (finished ones are kept). Run again later with --only lobbyists.')
                    return
                time.sleep(pause); pages += 1
                if not b: ok = False; break
                try: d = json.loads(b)
                except ValueError: ok = False; break
                for rep in d.get('results', []):
                    for it in rep.get('contribution_items') or []:
                        hon = norm(it.get('honoree_name') or '')
                        if last not in hon.split() or not any(t[:3] == first[:3] for t in hon.split()): continue
                        reg = rep.get('registrant') if isinstance(rep.get('registrant'), dict) else {}
                        items.append([str(rep.get('filing_year', '')), it.get('date', ''), money(it.get('amount')), it.get('contribution_type_display') or it.get('contribution_type') or '',
                                      it.get('contributor_name') or '', reg.get('name', ''), it.get('payee_name') or '', it.get('honoree_name') or '', rep.get('filing_document_url') or rep.get('url') or ''])
                url = d.get('next')
            if ok: os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(items, open(cache, 'w'))
        if items:
            wcsv(os.path.join(c.folder(), 'lobbyist_contributions_ld203.csv'), ['filing_year', 'date', 'amount', 'type', 'contributor', 'registrant_firm', 'payee', 'honoree', 'filing'], items)
        state.setdefault(c.id, {})['lobbyists'] = {'reports_found': len(items), 'total': round(sum(r[2] for r in items), 2)}
        if i % 50 == 0: log(f'  {i} of {len(cands)}')

# ---------------------------------------------------------------- quarters (API)
def step_quarters(cands, cycles, state):
    log('\n[quarters] Money raised in each reporting period (FEC API)')
    key = os.environ.get('FEC_API_KEY')
    if not key: log('  skipped: needs FEC_API_KEY'); return
    for i, c in enumerate(cands, 1):
        for y in cycles:
            for cm in sorted(c.cmtes.get(y, ())):
                cache = os.path.join(ROOT, '_downloads', 'reports', f'{cm}_{y}.json')
                if not os.path.exists(cache):
                    b = fetch(f'{API}/committee/{cm}/reports/?' + urllib.parse.urlencode({'api_key': key, 'cycle': y, 'per_page': 100, 'is_amended': 'false'}), headers={'Accept': 'application/json'}, quiet=True)
                    if not b: continue
                    os.makedirs(os.path.dirname(cache), exist_ok=True); open(cache, 'wb').write(b); time.sleep(3.7)
                try: res = json.load(open(cache)).get('results', [])
                except ValueError: continue
                rows = sorted([[r.get('report_type_full') or r.get('report_type'), (r.get('coverage_start_date') or '')[:10], (r.get('coverage_end_date') or '')[:10],
                                money(r.get('total_receipts_period')), money(r.get('total_individual_contributions_period')), money(r.get('individual_unitemized_contributions_period')),
                                money(r.get('other_political_committee_contributions_period')), money(r.get('cash_on_hand_end_period'))] for r in res], key=lambda r: r[2])
                S = state.setdefault(c.id, {}).setdefault('cycles', {}).setdefault(str(y), {})
                S.setdefault('quarters', {})[cm] = rows
        if i % 50 == 0: log(f'  {i} of {len(cands)}')

# ---------------------------------------------------------------- flags and output
def write_all(cands, state, cycles):
    rows = []
    groups = {}
    for y in cycles:
        gp = os.path.join(ROOT, '_outside_groups', f'donors_{y}.json')
        if os.path.exists(gp): groups[str(y)] = json.load(open(gp))
    for c in cands:
        S = state.setdefault(c.id, {})
        corp, lobby, dark = [], [], 0.0
        for y, C in S.get('cycles', {}).items():
            o = C.get('outside') or {}
            G = groups.get(y, {})
            for s in ('support', 'oppose'):
                for g in o.get(s, []):
                    D = G.get(g['id'])
                    if D and g['amount'] >= OUTSIDE_MIN:
                        g['funders'] = {k: D.get(k, []) for k in ('donors_individual', 'donors_organizations', 'donors_committees')}
                        orgs = D.get('donors_organizations') or []
                        if orgs: corp.append(f"{g['name']} spent ${g['amount']:,.0f} {'for' if s == 'support' else 'against'} ({y}); its organization donors include {orgs[0][0]} (${orgs[0][1]:,.0f})")
                        for f in D.get('donors_committees') or []:
                            if f.get('foreign_policy_flag'): lobby.append(f"{g['name']} spent ${g['amount']:,.0f} {'for' if s == 'support' else 'against'} ({y}) and was funded in part by {f['name']} (${f['amount']:,.0f})")
                            if f.get('corporate_or_trade'): corp.append(f"{g['name']} was funded in part by {f['name']} (${f['amount']:,.0f}, {y})")
                    if g.get('foreign_policy_flag'): lobby.append(f"{g['name']} spent ${g['amount']:,.0f} {'for' if s == 'support' else 'against'} ({y})")
                    if g.get('corporate_or_trade'): corp.append(f"{g['name']} ({g.get('org_type')}) spent ${g['amount']:,.0f} {'for' if s == 'support' else 'against'} ({y})")
            dark += o.get('non_disclosing_spending', 0)
            for e in (C.get('donors') or {}).get('earmarks_by_conduit', []):
                if e.get('foreign_policy_flag'): lobby.append(f"${e['amount']:,.0f} earmarked through {e['name']} ({y})")
        S['flags'] = {'lobby_leads': lobby, 'corp_leads': corp, 'non_disclosing_outside_spending': round(dark, 2),
                      'note': 'Leads from committee names and FEC types, to verify. Direct PAC contributions are in fec_committee_contributions.csv from the 2026 collector.'}
        S.update({'id': c.id, 'name': c.name, 'state': c.st, 'office': c.office, 'fec_ids': c.fec, 'collected': NOW, 'cycles_searched': cycles})
        wjson(os.path.join(c.folder(), 'money_deep.json'), S)
        d26 = S.get('cycles', {}).get(str(max(cycles)), {})
        rows.append([c.st, c.id, c.name, c.office, (d26.get('donors') or {}).get('itemized_individual_total', ''), (d26.get('donors') or {}).get('instate_share', ''),
                     round(sum(e['amount'] for e in (d26.get('donors') or {}).get('earmarks_by_conduit', [])), 2),
                     round(sum(g['amount'] for g in (d26.get('outside') or {}).get('support', [])), 2), round(sum(g['amount'] for g in (d26.get('outside') or {}).get('oppose', [])), 2),
                     S['flags']['non_disclosing_outside_spending'], len(S['flags']['lobby_leads']), len(S['flags']['corp_leads']), (S.get('lobbyists') or {}).get('total', '')])
    wcsv(os.path.join(ROOT, 'summary.csv'), ['state', 'id', 'name', 'office', 'itemized_individual', 'instate_share', 'earmarked_via_conduits', 'outside_for', 'outside_against',
         'non_disclosing_outside', 'lobby_leads', 'corp_leads', 'lobbyist_ld203_total'], rows)

def main():
    a = sys.argv[1:]
    states = [a[i + 1].upper() for i, x in enumerate(a) if x == '--state' and i + 1 < len(a)]
    only = a[a.index('--only') + 1].split(',') if '--only' in a else STEPS
    cycles = sorted(int(x) for x in (a[a.index('--cycles') + 1].split(',') if '--cycles' in a else ['2026']))
    log(f'OTS money-deep, {NOW}. Cycles: {cycles}. Output: {ROOT}')
    cands = load_ballot(states)
    fed = [c for c in cands if c.office != 'governor' and c.fec]
    log(f'{len(cands)} ballot candidates in scope; {len(fed)} with FEC ids (governors file with their states, not the FEC)')
    state_path = os.path.join(ROOT, '_state.json')
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    def save(): wjson(state_path, state)
    try:
        info = load_committees(cycles)
        n = link_committees(fed, cycles); log(f'  {n} candidates matched to their campaign committees')
        spenders = {}
        if 'outside' in only or 'indiv' in only or 'oth' in only:
            spenders = step_outside(fed, cycles, info, state); save()
        if 'indiv' in only: step_indiv(fed, cycles, info, spenders, state); save()
        if 'oth' in only: step_oth(fed, cycles, info, spenders)
        if 'lobbyists' in only: step_lobbyists(fed, state); save()
        if 'quarters' in only: step_quarters(fed, cycles, state); save()
    except NetworkDown as e:
        save(); log(f'\nThe connection stayed down ({e}). Finished parts are saved; run the same command again to continue.'); raise SystemExit(2)
    write_all(fed, state, cycles); save()
    log(f'\nDone. Per-candidate files in {ROOT}/<STATE>/<candidate>/money_deep.json; overview in summary.csv')

if __name__ == '__main__':
    main()
