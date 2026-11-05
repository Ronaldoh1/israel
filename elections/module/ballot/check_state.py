#!/usr/bin/env python3
"""Check one state's downloads against what the scoring rubric needs, and keep the progress list.

    python3 check_state.py GA              check GA, write its coverage file, update progress.csv
    python3 check_state.py GA --uploaded   also record that GA's zip was uploaded
    python3 check_state.py --status        show every state's progress

Exit code 3 means some downloads are missing that a re-run can fill (run_states.sh re-runs once by itself)."""
import csv, json, os, sys
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__)); TOP = os.path.dirname(HERE)
REC = os.environ.get('OTS_RECORDS_DIR') or os.path.join(TOP, 'data', 'ballot-records')
RES = os.environ.get('OTS_RESEARCH_DIR') or os.path.join(TOP, 'data', 'research-pack')
PROG = os.path.join(TOP, 'progress.csv')
BALLOT = os.path.join(HERE, 'ballot_2026.csv')
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
ORDER = 'GA MI NC ME NH TX OH IA AK AZ NE MN NV PA WI VA NM CO FL NY CA NJ IL KS MO MT SC KY LA MS AL AR CT DE HI ID IN MA MD ND OK OR RI SD TN UT VT WA WV WY'.split()
FIELDS = ['state', 'candidates', 'checked', 'ready', 'retry_needed', 'gaps', 'uploaded']
import re
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def load_prog():
    if not os.path.exists(PROG): return {}
    return {r['state']: r for r in csv.DictReader(open(PROG, encoding='utf-8'))}
def save_prog(P):
    with open(PROG, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
        for st in ORDER:
            if st in P: w.writerow({k: P[st].get(k, '') for k in FIELDS})

def status():
    P = load_prog(); done = [s for s in ORDER if P.get(s, {}).get('uploaded')]
    print(f'{len(done)} of {len(ORDER)} states uploaded.\n')
    print(f'{"state":6}{"cands":>6}  {"checked":17}{"ready":>6}{"retry":>6}  uploaded')
    for st in ORDER:
        r = P.get(st)
        if r: print(f'{st:6}{r["candidates"]:>6}  {r["checked"]:17}{r["ready"]:>6}{r["retry_needed"]:>6}  {r["uploaded"] or "-"}')
    left = [s for s in ORDER if not P.get(s, {}).get('uploaded')]
    print('\nStill to do:', ' '.join(left) if left else 'nothing')

def check(st, uploaded=False):
    rows = [r for r in csv.DictReader(open(BALLOT, encoding='utf-8')) if r['state'] == st]
    if not rows: print('No ballot candidates for', st); return 1
    out, retry, ready, gaps = [], 0, 0, set()
    for r in rows:
        cid = r['data_id'] or '%s-%s' % (r['race'].lower(), slug(r['name']))
        rp = lambda f: os.path.join(RES, st, cid, f); bp = lambda f: os.path.join(REC, st, cid, f)
        J = lambda p: json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
        gov = r['office'] == 'governor'; sen = r['office'] == 'senate'
        member = os.path.exists(rp('ids.json'))
        miss = [f for f in ('wikipedia.json', 'ballotpedia.json', 'factchecks.json', 'ethics.json') if not os.path.exists(rp(f))]
        if not os.path.exists(bp('courts_courtlistener.json')): miss.append('courts')
        if sen and not os.path.exists(bp('senate_disclosures.json')): miss.append('senate_disclosures')
        if member and not os.path.exists(rp('votes_all.csv')): miss.append('votes')
        if member and not os.path.exists(rp('bills.json')): miss.append('bills')
        if r['fec_ids'] and not os.path.exists(rp('fec_filing_record.json')): miss.append('fec_filing_record')
        if os.path.exists(rp('ballotpedia.json')) and not os.path.exists(rp('campaign_site.json')): miss.append('campaign_site')
        cs = J(rp('campaign_site.json')) or {}; bpj = J(rp('ballotpedia.json')) or {}; fc = J(rp('factchecks.json')) or {}; wk = J(rp('wikipedia.json')) or {}
        cov = {
            'money_history': 'state filings not collected' if gov else ('FEC (2026 collector)' if r['data_id'] else 'never filed with the FEC'),
            'courts': 'federal (CourtListener); state trial courts by news' if os.path.exists(bp('courts_courtlistener.json')) else 'MISSING',
            'ethics': ('House/Senate Ethics' if member else 'federal ethics n/a; state boards by news') if os.path.exists(rp('ethics.json')) else 'MISSING',
            'disclosures': 'state disclosure not collected' if gov else ('Senate eFD' if sen and os.path.exists(bp('senate_disclosures.json')) else
                           'MISSING' if sen else 'House Clerk (2026 collector)' if r['data_id'] else 'none on file'),
            'fara': 'FARA (2026 collector)' if r['data_id'] else 'to check by name',
            'claims': 'sources: ' + ', '.join(x for x, ok in (('campaign site', cs.get('pages')), ('Ballotpedia', bpj.get('url')), ('PolitiFact', fc.get('rulings'))) if ok) if (cs.get('pages') or bpj.get('url') or fc.get('rulings')) else 'THIN',
            'votes': ('Voteview' if os.path.exists(rp('votes_all.csv')) else 'MISSING') if member else 'n/a (never served in Congress)',
            'democracy': 'certification roll calls + statements' if member else 'statements only',
            'prep': 'Wikipedia/Ballotpedia' if (wk.get('title') or bpj.get('url')) else 'THIN',
        }
        if gov: gaps.update(['governor money/disclosures are state records'])
        if not miss: ready += 1
        else: retry += 1
        out.append([r['race'], r['name'], cid] + [cov[k] for k in cov] + [' '.join(miss)])
    os.makedirs(os.path.join(RES, st), exist_ok=True)
    with open(os.path.join(RES, st, '_coverage.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['race', 'name', 'id', 'money_history', 'courts', 'ethics', 'disclosures', 'fara', 'claims', 'votes', 'democracy', 'prep', 'missing_downloads']); w.writerows(out)
    P = load_prog(); prev = P.get(st, {})
    P[st] = {'state': st, 'candidates': len(rows), 'checked': NOW, 'ready': ready, 'retry_needed': retry, 'gaps': '; '.join(sorted(gaps)),
             'uploaded': NOW if uploaded else prev.get('uploaded', '')}
    save_prog(P)
    print(f'{st}: {len(rows)} ballot candidates, {ready} with every download, {retry} missing something a re-run can fill.')
    for x in out:
        if x[-1]: print(f'   {x[1]} ({x[0]}): missing {x[-1]}')
    return 3 if retry else 0

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == '--status': status(); sys.exit(0)
    sys.exit(check(a[0].upper(), '--uploaded' in a))
