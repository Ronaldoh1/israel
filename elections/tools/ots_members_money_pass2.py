#!/usr/bin/env python3
"""
OTS: who funds the people in office now, pass 2 (the money the first pass can't see).

Run it AFTER ots_members_money.py has finished, in the same folder (it reads members-data and reuses its downloads):
    FEC_API_KEY=xxxx python3 ots_members_money_pass2.py
Options:
    --state TX                 only some states (repeat for more)
    --skip lobbyists           skip a step (steps: leadership, outside, superpac, earmarks, lobbyists, quality)
    --individuals 2024,2022    ALSO read the FEC's itemized individual-donor files for those cycles. These are very
                               large (several GB per cycle) and take hours; they give every itemized donor by name and
                               every earmark through any conduit.

What it adds, for every current member of Congress and governor:
  1 leadership    their leadership PACs and joint fundraising committees, and every committee that gave to those
                  (corporate, trade, lobbyist, labor, ideological, foreign-policy flagged...)
  2 outside       outside spending for or against them by groups that are not PACs (nonprofits and other spenders
                  that report ads directly), and electioneering communications
  3 superpac      the top donors to every super PAC or outside group that spent at least $25,000 for or against them
  4 earmarks      donations forwarded through ANY flagged foreign-policy PAC, including ones that never gave directly
  5 lobbyists     registered lobbyists' own contributions and payments made to honor them (Senate LD-203 reports)
  6 quality       a re-read of the committee money that separates memo entries and amended duplicates, so totals
                  are not double counted
Every flag is a lead to verify, not a finding. Safe to stop and re-run: finished pieces are reused.
"""
import csv, io, json, os, re, sys, time, urllib.parse, zipfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import ots_members_money as M
except ImportError:
    print('Put this file in the same folder as ots_members_money.py (and run that first).'); raise SystemExit(1)

VERSION = '1.0 (2026-10-13)'
ROOT = M.ROOT
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
log, fetch, money, wcsv, wjson, norm, zip_rows = M.log, M.fetch, M.money, M.wcsv, M.wjson, M.norm, M.zip_rows
OTH = 'CMTE_ID AMNDT_IND RPT_TP TRANSACTION_PGI IMAGE_NUM TRANSACTION_TP ENTITY_TP NAME CITY STATE ZIP_CODE EMPLOYER OCCUPATION TRANSACTION_DT TRANSACTION_AMT OTHER_ID TRAN_ID FILE_NUM MEMO_CD MEMO_TEXT SUB_ID'.split()
CCL = 'CAND_ID CAND_ELECTION_YR FEC_ELECTION_YR CMTE_ID CMTE_TP CMTE_DSGN LINKAGE_ID'.split()
RECEIPT_TP = {'18K': 'Contribution received from a committee', '18J': 'Committee share via joint fundraiser (memo)', '15J': 'Individual share via joint fundraiser (memo)',
              '18G': 'Transfer in from an affiliated committee', '15Z': 'In-kind contribution received', '16C': 'Loan from candidate', '11': 'Contribution from a tribe',
              '12': 'Transfer from a nonfederal account', '15': 'Contribution from an individual', '15E': 'Earmarked contribution from an individual',
              '15C': 'Contribution from the candidate', '18U': 'Contribution from an unregistered committee', '19': 'Electioneering donation'}
LDA_BASES = ['https://lda.senate.gov/api/v1', 'https://lda.gov/api/v1']

# ---------------------------------------------------------------- people from the first pass
class P:
    def __init__(self, folder, d):
        self.folder = folder; self.id = os.path.basename(folder); self.name = d['name']; self.role = d['role']; self.state = d['state']
        self.fec_ids = set(d.get('fec_ids') or [])
        self.pcc = set()
        for s in d.get('principal_committees') or []:
            m = re.match(r'(C\d{8})', s)
            if m: self.pcc.add(m.group(1))
        self.lead = {}; self.jfc = {}
        first, _, last = self.name.rpartition(' ')
        self.f = (norm(first) or [''])[0]; self.l = norm(last) or ['?']
    def matches(self, toks):
        if not all(x in toks for x in self.l): return False
        f = self.f
        return any(t == f or t == f[:1] or (len(t) >= 3 and len(f) >= 3 and (t.startswith(f[:3]) or f.startswith(t))) for t in toks)

def load_people(states):
    out = []
    if not os.path.isdir(ROOT): log(f'No {ROOT} folder. Run ots_members_money.py first, in this same folder.'); raise SystemExit(1)
    for st in sorted(os.listdir(ROOT)):
        if (states and st not in states) or not os.path.isdir(os.path.join(ROOT, st)) or st.startswith('_'): continue
        for pid in sorted(os.listdir(os.path.join(ROOT, st))):
            f = os.path.join(ROOT, st, pid, 'profile.json')
            if os.path.exists(f): out.append(P(os.path.dirname(f), json.load(open(f, encoding='utf-8'))))
    log(f'  {len(out)} people from the first pass')
    return out

def money_rows(p):
    f = os.path.join(p.folder, 'committee_money.csv')
    return list(csv.DictReader(open(f, encoding='utf-8'))) if os.path.exists(f) else []

# ---------------------------------------------------------------- 1. leadership PACs and joint fundraisers
def find_committees(people, dl, cycles, cm, key):
    log('\n[1/6] Leadership PACs and joint fundraising committees')
    by_cand = {}
    for p in people:
        for i in p.fec_ids: by_cand[i] = p
    # linkage file: committees a candidate has linked to themselves (joint fundraisers, other authorized committees)
    for y in cycles:
        path = M.fec_file(dl, y, f'ccl{str(y)[2:]}.zip')
        if not path: continue
        for r in zip_rows(path, CCL):
            p = by_cand.get(r.get('CAND_ID'))
            if not p or r.get('CMTE_ID') in p.pcc: continue
            if r.get('CMTE_DSGN') == 'J': p.jfc[r['CMTE_ID']] = 'FEC linkage file'
            elif r.get('CMTE_DSGN') == 'D': p.lead[r['CMTE_ID']] = 'FEC linkage file'
    # committee directory: leadership PACs that name the member as sponsor
    for cid, r in cm.items():
        p = by_cand.get(r.get('CAND_ID', ''))
        if p and r.get('CMTE_DSGN') == 'D': p.lead.setdefault(cid, 'FEC committee directory')
    # FEC API: leadership PACs by sponsor (the most complete source)
    if key:
        for i, p in enumerate(people, 1):
            cache = os.path.join(dl, 'fec_api', f'sponsor_{p.id}.json')
            if os.path.exists(cache): res = json.load(open(cache))
            else:
                res = []
                ok = True
                for cand in sorted(p.fec_ids):
                    d = M.api_get('/committees/', key, sponsor_candidate_id=cand, per_page=100)
                    if d is None: ok = False; continue
                    res += [[c.get('committee_id'), c.get('name'), c.get('designation')] for c in d.get('results', [])]
                if ok: os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(res, open(cache, 'w'))
            for cid, nm, ds in res:
                if cid and cid not in p.pcc: (p.jfc if ds == 'J' else p.lead).setdefault(cid, 'FEC API (sponsor)')
            if i % 50 == 0: log(f'  sponsors checked: {i} of {len(people)}')
    log(f'  {sum(1 for p in people if p.lead)} people have a leadership PAC; {sum(1 for p in people if p.jfc)} have joint fundraisers')

def leadership_money(people, dl, cycles, info):
    owner = {}
    for p in people:
        for c in list(p.lead) + list(p.jfc): owner[c] = p
    rows = {p.id: [] for p in people}
    for y in cycles:
        path = M.fec_file(dl, y, f'oth{str(y)[2:]}.zip')
        if not path: continue
        log(f'  reading committee-to-committee money {y}')
        for v in zip_rows(path, None):
            if len(v) < 21: continue
            p = owner.get(v[0])
            if not p: continue
            donor = info.get(v[15], {})
            rows[p.id].append([y, v[13], money(v[14]), v[0], 'leadership PAC' if v[0] in p.lead else 'joint fundraiser', RECEIPT_TP.get(v[5], v[5]),
                               v[15], donor.get('name') or v[7], donor.get('kind', 'Individual or unregistered' if not v[15] else ''), donor.get('connected_org', ''),
                               donor.get('foreign_policy', ''), donor.get('fara_registrant', ''), v[18], v[1], v[20],
                               f'https://docquery.fec.gov/cgi-bin/fecimg/?{v[4]}' if v[4] else ''])
    out = {}
    for p in people:
        if not (p.lead or p.jfc): continue
        wjson(os.path.join(p.folder, 'leadership_and_joint_committees.json'), {'leadership_pacs': p.lead, 'joint_fundraisers': p.jfc})
        R = rows[p.id]
        wcsv(os.path.join(p.folder, 'money_into_leadership_pac_and_jfc.csv'), ['cycle', 'date', 'amount', 'into_committee', 'committee_role', 'what',
             'from_committee_id', 'from', 'from_kind', 'connected_org', 'foreign_policy_country', 'fara_registrant', 'memo', 'amended', 'sub_id', 'filing'], R)
        # only gifts the member's committees reported RECEIVING; the same oth file also lists what those committees gave
        # to others (24K, 24Z...) and transfers between them, which are not money coming in
        IN = ('Contribution received from a committee', 'In-kind contribution received', 'Contribution from an unregistered committee')
        real = [r for r in R if r[12] != 'X' and r[4] == 'leadership PAC' and r[5] in IN]
        k = lambda kind: round(sum(r[2] for r in real if r[8] == kind), 2)
        out[p.id] = {'leadership_pacs': ' '.join(sorted(p.lead)), 'joint_fundraisers': ' '.join(sorted(p.jfc)),
                     'into_leadership_pac_from_committees': round(sum(r[2] for r in real if r[6]), 2), 'into_leadership_pac_corporate': k('Corporate PAC'),
                     'into_leadership_pac_trade': k('Trade association PAC'), 'into_leadership_pac_lobbyist_pacs': k('Lobbyist/registrant PAC'),
                     'into_leadership_pac_labor': k('Labor PAC'), 'into_leadership_pac_flagged_foreign_policy': round(sum(r[2] for r in real if r[10]), 2),
                     'into_joint_fundraisers_from_committees': round(sum(r[2] for r in R if r[12] != 'X' and r[4] == 'joint fundraiser' and r[6] and r[5] in IN), 2)}
    return out

# ---------------------------------------------------------------- 2. outside spending by non-PAC groups
def outside(people, dl, cycles, cm):
    log('\n[2/6] Outside spending by groups that are not PACs, and electioneering communications')
    ids = {i: p for p in people for i in p.fec_ids}
    rows = {p.id: [] for p in people}; got = 0
    for y in cycles:
        if y < 2004: continue
        for fname, kind in ((f'independent_expenditure_{y}.csv', 'independent expenditure'), (f'ElectioneeringComm_{y}.csv', 'electioneering communication')):
            path = fetch(M.FEC.format(y=y, f=fname), os.path.join(dl, 'fec', str(y), fname), quiet=True)
            if not path: continue
            got += 1
            with open(path, encoding='latin-1', newline='') as f:
                rd = csv.DictReader(f)
                for r in rd:
                    r = {k.strip().lower(): (v or '').strip() for k, v in r.items() if k}
                    cid = r.get('cand_id') or r.get('candidate_id') or ''
                    p = ids.get(cid)
                    if not p: continue
                    spender = r.get('spe_id') or r.get('committee_id') or r.get('filer_id') or ''
                    rows[p.id].append([y, kind, r.get('exp_date') or r.get('disbursement_date') or r.get('pub_dist_date') or '', money(r.get('exp_amo') or r.get('calculated_cand_share') or r.get('disbursement_amount')),
                                       {'S': 'FOR', 'O': 'AGAINST'}.get(r.get('sup_opp', ''), r.get('sup_opp', '')), spender, r.get('spe_nam') or r.get('committee_name') or r.get('filer_name') or '',
                                       'registered committee' if spender in cm else 'not a registered committee (e.g. nonprofit or person)',
                                       r.get('pur') or r.get('purpose') or '', r.get('pay') or r.get('payee_name') or '', r.get('tran_id', ''), r.get('image_num') or r.get('file_num') or ''])
    log(f'  read {got} files')
    out = {}
    for p in people:
        R = rows[p.id]
        if not R: continue
        wcsv(os.path.join(p.folder, 'outside_spending_all_spenders.csv'), ['cycle', 'kind', 'date', 'amount', 'for_or_against', 'spender_id', 'spender',
             'spender_type', 'purpose', 'payee', 'tran_id', 'image_or_file'], R)
        nc = [r for r in R if r[7].startswith('not')]
        out[p.id] = {'noncommittee_outside_for': round(sum(r[3] for r in nc if r[4] == 'FOR'), 2),
                     'noncommittee_outside_against': round(sum(r[3] for r in nc if r[4] == 'AGAINST'), 2),
                     'electioneering_communications': round(sum(r[3] for r in R if r[1] == 'electioneering communication'), 2)}
    return out, rows

# ---------------------------------------------------------------- 3. who funds the outside spenders
def superpac_donors(people, dl, key, info, ie_rows, threshold):
    log('\n[3/6] Top donors to super PACs and outside groups that spent on them')
    if not key: log('  skipped: needs FEC_API_KEY'); return {}
    spent = {}   # (spender, cycle) -> total spent on current officials
    for p in people:
        for r in money_rows(p):
            if 'Independent expenditure' in r['what'] or 'Communication cost' in r['what']:
                k = (r['committee_id'], int(r['cycle'])); spent[k] = spent.get(k, 0) + money(r['amount'])
        for r in ie_rows.get(p.id, []):
            if r[5].startswith('C'): k = (r[5], r[0]); spent[k] = spent.get(k, 0) + r[3]
    todo = sorted((k for k, v in spent.items() if v >= threshold), key=lambda k: -spent[k])
    log(f'  {len(todo)} spender-cycles spent at least ${threshold:,} on current officials')
    out = []
    for n, (cid, y) in enumerate(todo, 1):
        cache = os.path.join(dl, 'fec_api', f'donors_{cid}_{y}.json')
        if os.path.exists(cache): res = json.load(open(cache))
        else:
            d = M.api_get('/schedules/schedule_a/', key, committee_id=cid, two_year_transaction_period=y, sort='-contribution_receipt_amount', per_page=100)
            if d is None: continue
            res = [[r.get('contributor_name'), r.get('contributor_employer'), r.get('contributor_occupation'), r.get('entity_type_desc') or r.get('entity_type'),
                    r.get('contributor_id') or '', money(r.get('contribution_receipt_amount')), (r.get('contribution_receipt_date') or '')[:10], r.get('pdf_url') or '']
                   for r in (d or {}).get('results', [])]
            os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(res, open(cache, 'w'))
        c = info.get(cid, {})
        for r in res: out.append([cid, c.get('name', ''), c.get('foreign_policy', ''), y, round(spent[(cid, y)], 2)] + r)
        if n % 25 == 0: log(f'  {n} of {len(todo)}')
    wcsv(os.path.join(ROOT, 'outside_spender_top_donors.csv'), ['spender_id', 'spender', 'spender_flagged_country', 'cycle', 'spent_on_current_officials',
         'donor', 'donor_employer', 'donor_occupation', 'donor_type', 'donor_committee_id', 'amount', 'date', 'filing'], out)
    log(f'  wrote outside_spender_top_donors.csv ({len(out)} rows)')
    return {}

# ---------------------------------------------------------------- 4. earmarks through every flagged foreign-policy PAC
def earmarks(people, dl, key, info, start):
    log('\n[4/6] Donations forwarded through every flagged foreign-policy PAC')
    if not key: log('  skipped: needs FEC_API_KEY'); return {}
    owner = {}
    for p in people:
        for c in list(p.pcc) + list(p.lead) + list(p.jfc): owner[c] = p
    flagged = sorted(cid for cid, c in info.items() if c['foreign_policy'] and c['type'] in ('PAC', 'PAC (nonqualified)'))
    log(f'  {len(flagged)} flagged PACs to check (results already fetched by the first pass are reused)')
    rows = {p.id: [] for p in people}; allrows = []
    for n, cid in enumerate(flagged, 1):
        cache = os.path.join(dl, 'fec_api', f'conduit2_{cid}_{start}.json')
        if os.path.exists(cache): res = json.load(open(cache))
        else:
            res, last = [], {}
            ok = True
            while True:
                d = M.api_get('/schedules/schedule_b/', key, committee_id=cid, min_date=f'{start}-01-01', per_page=100, sort='-disbursement_date', **last)
                if d is None: ok = False; break
                if not d.get('results'): break
                for r in d['results']:
                    res.append([r.get('disbursement_date', '')[:10], money(r.get('disbursement_amount')), r.get('recipient_committee_id') or '',
                                r.get('recipient_name') or '', r.get('disbursement_description') or r.get('memo_text') or '', r.get('memo_code') or '', r.get('pdf_url') or ''])
                li = (d.get('pagination') or {}).get('last_indexes')
                if not li: break
                last = li
            if ok: os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(res, open(cache, 'w'))
            else: log(f'  {info[cid]["name"]}: incomplete, not saved (retried next run)')
        for r in res:
            p = owner.get(r[2])
            row = [r[0], r[1], cid, info[cid]['name'], info[cid]['foreign_policy'], info[cid]['foreign_policy_reason'], r[2], r[3], p.id if p else '', r[4], r[5], r[6]]
            allrows.append(row)
            if p: rows[p.id].append(row)
        if n % 25 == 0: log(f'  {n} of {len(flagged)}')
    head = ['date', 'amount', 'pac_id', 'pac', 'country', 'why_flagged', 'recipient_committee', 'recipient', 'official', 'description', 'memo_code', 'filing']
    wcsv(os.path.join(ROOT, 'foreign_policy_pac_disbursements_all.csv'), head, allrows)
    out = {}
    for p in people:
        if not rows[p.id]: continue
        wcsv(os.path.join(p.folder, 'foreign_policy_pac_disbursements.csv'), head, rows[p.id])
        ear = [r for r in rows[p.id] if 'EARMARK' in (r[9] or '').upper() or r[10] == 'X']
        by = {}
        for r in rows[p.id]: by[r[4]] = by.get(r[4], 0) + r[1]
        out[p.id] = {'flagged_fp_pacs_paid_to_their_committees': round(sum(r[1] for r in rows[p.id]), 2), 'flagged_fp_earmarked_or_memo': round(sum(r[1] for r in ear), 2),
                     'flagged_fp_paid_by_country': '; '.join(f'{k} ${v:,.0f}' for k, v in sorted(by.items(), key=lambda kv: -kv[1]))}
    return out

# ---------------------------------------------------------------- 5. lobbyists' contributions (LD-203)
def lobbyists(people, dl):
    log('\n[5/6] Registered lobbyists\' contributions and honorary payments (Senate LD-203 reports)')
    key = os.environ.get('LDA_API_KEY')
    H = {'Accept': 'application/json'}
    if key: H['Authorization'] = f'Token {key}'
    base = None
    for b in LDA_BASES:
        if fetch(f'{b}/contributions/?page_size=1', headers=H, tries=2, quiet=True): base = b; break
    if not base:
        log('  the LD-203 database did not answer (lda.senate.gov / lda.gov); skipped. Re-run later with --only lobbyists.'); return {}
    pause = 1.0 if key else 4.5
    out = {}
    for i, p in enumerate(people, 1):
        cache = os.path.join(dl, 'lda', f'{p.id}.json')
        if os.path.exists(cache): items = json.load(open(cache))
        else:
            items, url = [], f'{base}/contributions/?' + urllib.parse.urlencode({'contribution_honoree': ' '.join(p.l), 'page_size': 25})
            pages = 0; complete = True
            while url and pages < 400:
                b = fetch(url, headers=H, quiet=True); time.sleep(pause); pages += 1
                if not b: complete = False; break
                try: d = json.loads(b)
                except ValueError: complete = False; break
                if pages == 4 and not items and (d.get('count') or 0) > 5000:
                    log(f'  the LD-203 search returned {d.get("count"):,} unrelated reports for {p.name}: its name filter did not apply.'
                        '\n  Stopping this step so it does not run for days; tell Claude and it will adjust the query.'); return out
                for rep in d.get('results', []):
                    for it in rep.get('contribution_items') or []:
                        hon = it.get('honoree_name') or ''
                        if not p.matches(set(norm(hon))): continue
                        items.append([str(rep.get('filing_year', '')), it.get('date', ''), money(it.get('amount')), it.get('contribution_type_display') or it.get('contribution_type') or '',
                                      it.get('contributor_name') or '', (rep.get('registrant') or {}).get('name', '') if isinstance(rep.get('registrant'), dict) else '',
                                      (rep.get('lobbyist') or {}).get('first_name', '') + ' ' + (rep.get('lobbyist') or {}).get('last_name', '') if isinstance(rep.get('lobbyist'), dict) else '',
                                      it.get('payee_name') or '', hon, rep.get('filing_document_url') or rep.get('url') or ''])
                url = d.get('next')
            if complete: os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(items, open(cache, 'w'))
        if items:
            wcsv(os.path.join(p.folder, 'lobbyist_contributions_ld203.csv'), ['filing_year', 'date', 'amount', 'type', 'contributor', 'registrant_firm', 'lobbyist',
                 'payee', 'honoree', 'filing'], items)
            # the same contribution is repeated in each amended report, and the honoree search also matches namesakes:
            # count each (date, amount, contributor, payee, type) once, and only payments whose payee names the person
            sur = (p.l[-1] if p.l else '').upper()
            seen = {}
            for r in items:
                if r[3].lower().startswith('feca') and sur and sur not in (r[7] or '').upper(): continue
                seen[(r[1], r[2], r[4], r[7], r[3])] = r
            items_c = list(seen.values())
            t = lambda w: round(sum(r[2] for r in items_c if w in r[3].lower()), 2)
            out[p.id] = {'lobbyist_feca_contributions': t('feca'), 'lobbyist_honorary_payments': t('honorary'), 'lobbyist_meeting_expenses': t('meeting'),
                         'lobbyist_all_reported_payments': round(sum(r[2] for r in items_c), 2)}
        if i % 25 == 0: log(f'  {i} of {len(people)}')
    return out

# ---------------------------------------------------------------- 6. data quality: memo entries and amendments
def quality(people, dl, cycles):
    log('\n[6/6] Checking the committee money for memo entries and amended duplicates')
    ids = {i: p for p in people for i in p.fec_ids}
    seen = {p.id: {} for p in people}
    for y in cycles:
        path = M.fec_file(dl, y, f'pas2{str(y)[2:]}.zip')
        if not path: continue
        for v in zip_rows(path, None):
            if len(v) < 22: continue
            p = ids.get(v[16])
            if not p: continue
            key = (v[0], v[17] or v[21])            # filer + transaction id (falls back to the FEC row id)
            seen[p.id].setdefault(key, []).append((y, v[1], v[19], money(v[14]), v[5], v[21]))
    out = {}
    for p in people:
        S = seen[p.id]
        if not S: continue
        dup = sum(len(v) - 1 for v in S.values() if len(v) > 1)
        memo = [r for v in S.values() for r in v if r[2] == 'X']
        clean = []
        for v in S.values():
            v = [r for r in v if r[2] != 'X']
            if v: clean.append(sorted(v, key=lambda r: (r[1] == 'A', r[5]))[-1])   # keep the latest amendment
        contrib = lambda rows: round(sum(r[3] for r in rows if r[4] in ('24K', '24Z', '24U')), 2)
        raw = contrib([r for v in S.values() for r in v])
        out[p.id] = {'committee_contributions_raw': raw, 'committee_contributions_deduplicated': contrib(clean), 'memo_rows': len(memo),
                     'memo_amount': round(sum(r[3] for r in memo), 2), 'amended_duplicate_rows': dup}
    return out

# ---------------------------------------------------------------- optional: itemized individual donors
def individuals(people, dl, years, info):
    log(f'\n[optional] Itemized individual donors for {", ".join(map(str, years))} (very large files)')
    owner = {}
    for p in people:
        for c in list(p.pcc) + list(p.lead) + list(p.jfc): owner[c] = p
    conduit_rx = re.compile(r'EARMARKED (?:THROUGH|VIA|FROM)\s+(.+)', re.I)
    out = {}
    for y in years:
        path = M.fec_file(dl, y, f'indiv{str(y)[2:]}.zip')
        if not path: log(f'  could not download indiv{str(y)[2:]}.zip'); continue
        files, ear = {}, {}
        n = 0
        for v in zip_rows(path, None):
            n += 1
            if n % 5000000 == 0: log(f'    {n / 1e6:.0f} million rows read')
            if len(v) < 21: continue
            p = owner.get(v[0])
            if not p: continue
            if p.id not in files:
                fh = open(os.path.join(p.folder, f'itemized_individuals_{y}.csv'), 'w', newline='', encoding='utf-8')
                w = csv.writer(fh); w.writerow(['committee', 'date', 'amount', 'name', 'city', 'state', 'employer', 'occupation', 'type', 'memo', 'memo_text', 'sub_id'])
                files[p.id] = (fh, w)
            files[p.id][1].writerow([v[0], v[13], v[14], v[7], v[8], v[9], v[11], v[12], v[5], v[18], v[19], v[20]])
            m = conduit_rx.search(v[19] or '')
            if m:
                k = (p.id, m.group(1).strip().upper()[:80]); ear[k] = ear.get(k, 0) + money(v[14])
        for fh, _ in files.values(): fh.close()
        for (pid, conduit), amt in ear.items():
            out.setdefault(pid, {}); out[pid][conduit] = out[pid].get(conduit, 0) + amt
        log(f'  {y}: {len(files)} people')
    rows = []
    for pid, d in out.items():
        for conduit, amt in d.items():
            fp = ''
            for rx, country in M.NAMED.items():
                if re.search(rx, conduit, re.I): fp = country
            if not fp:
                m = M.COUNTRY_RX.search(conduit); fp = m.group(1).title() if m else ''
            rows.append([pid, conduit, round(amt, 2), fp])
    wcsv(os.path.join(ROOT, 'earmarks_by_conduit_from_individual_files.csv'), ['official', 'conduit', 'amount', 'flagged_country'], sorted(rows, key=lambda r: (r[0], -r[2])))

# ---------------------------------------------------------------- main
def main():
    a = sys.argv[1:]
    states = {a[i + 1].upper() for i, x in enumerate(a) if x == '--state'}
    skip = {s for i, x in enumerate(a) if x == '--skip' for s in a[i + 1].split(',')}
    only = set(a[a.index('--only') + 1].split(',')) if '--only' in a else None
    run = lambda step: (only is None or step in only) and step not in skip
    since = int(a[a.index('--since') + 1]) if '--since' in a else 1980
    cycles = list(range(since - since % 2, 2028, 2)); start = max(since, 2008)
    indiv = [int(x) for x in a[a.index('--individuals') + 1].split(',')] if '--individuals' in a else []
    key = os.environ.get('FEC_API_KEY') or (a[a.index('--fec-key') + 1] if '--fec-key' in a else None)
    dl = next((d for d in M.SIBLING_DL if os.path.isdir(d)), os.path.join(ROOT, '_downloads'))
    log(f'OTS members money, pass 2 {VERSION}\n  data: {ROOT}\n  downloads: {dl}')
    if not key: log('  (no FEC_API_KEY: leadership-PAC sponsors, super PAC donors and earmarks will be limited or skipped)')
    people = load_people(states)
    log('  committee directory and foreign-agent registrations')
    cmraw = M.committees(dl, cycles); info = M.classify(cmraw, M.fara_firms(dl))
    cols = {p.id: {} for p in people}
    def merge(d):
        for k, v in (d or {}).items(): cols.setdefault(k, {}).update(v)
    ie_rows = {}
    if run('leadership'):
        find_committees(people, dl, cycles, cmraw, key); merge(leadership_money(people, dl, cycles, info))
    if run('outside'):
        o, ie_rows = outside(people, dl, cycles, cmraw); merge(o)
    if run('superpac'): superpac_donors(people, dl, key, info, ie_rows, 25000)
    if run('earmarks'): merge(earmarks(people, dl, key, info, start))
    if run('lobbyists'): merge(lobbyists(people, dl))
    if run('quality'): merge(quality(people, dl, cycles))
    if indiv: individuals(people, dl, indiv, info)
    # one row per person; reruns keep earlier columns
    path = os.path.join(ROOT, 'summary_pass2.csv')
    old = {r['id']: r for r in csv.DictReader(open(path, encoding='utf-8'))} if os.path.exists(path) else {}
    keys = []
    for d in list(old.values()) + list(cols.values()):
        for k in d:
            if k not in keys and k not in ('id', 'name', 'role', 'state'): keys.append(k)
    rows = []
    for p in people:
        d = dict(old.get(p.id, {})); d.update(cols.get(p.id, {}))
        rows.append([p.id, p.name, p.role, p.state] + [d.get(k, '') for k in keys])
    wcsv(path, ['id', 'name', 'role', 'state'] + keys, rows)
    wjson(os.path.join(ROOT, 'manifest_pass2.json'), {'script': 'ots_members_money_pass2.py ' + VERSION, 'run_at': NOW, 'steps': sorted(s for s in
          ['leadership', 'outside', 'superpac', 'earmarks', 'lobbyists', 'quality'] if run(s)), 'individual_files': indiv})
    log(f'\nFinished. New per-person files are next to the first-pass files; overview: {path}'
        f'\nPush members-data to GitHub the same way as before when you are ready.')

if __name__ == '__main__':
    try:
        main()
    except M.NetworkDown as e:
        log(f'\nThe internet connection was down for 30 minutes ({e}).\nEverything finished so far is saved. When you are back online,'
            ' run the same command again in the same folder: it skips what is already done and continues.')
        raise SystemExit(2)
