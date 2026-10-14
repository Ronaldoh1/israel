"""Merge the verified 2026 House nominees (research/house/<ST>.json) and the public-records profiles
(records/records.json) into the module data.

- Every House race gets its incumbent, its nominees, a status note and its sources.
- Each nominee becomes a candidate with research 'records' (records-only, not yet scored) unless the
  module already has a fully researched page for them, which is never overwritten.
- data['rec'] holds the full records profile for every candidate in the module (nominees and the
  existing Senate/governor candidates), keyed by the candidate id.
- data['filers'] lists, per race, everyone else who filed with the FEC for it (mostly primary losers
  and withdrawals), with their 2026 receipts, collapsed in the page.
Usage: python3 merge_house.py data.json data_out.json"""
import json, glob, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, 'data.json')
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(H, 'data_states.json')
d = json.load(open(src, encoding='utf-8')); R, C, CITES = d['races'], d['cands'], d['cites']
REC = json.load(open(os.path.join(H, 'records', 'records.json'), encoding='utf-8'))
PMAP = {'D': 'D', 'R': 'R', 'L': 'L', 'G': 'G', 'I': 'I', 'C': 'C', 'DEM': 'D', 'REP': 'R', 'LIB': 'L', 'GRE': 'G', 'IND': 'I', 'DFL': 'D', 'NPA': 'I', 'CON': 'C'}

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def party(p):
    p = (p or '').strip()
    return (PMAP.get(p.upper()) or ('L' if 'libertarian' in p.lower() else 'G' if 'green' in p.lower() else 'C' if 'constitution' in p.lower() else 'O')), p

def slim(p):
    """the record as the page uses it (drop the bulky fields the page never shows)"""
    q = {k: p[k] for k in ('fec', 'cyc', 'pac', 'pac26', 'lob', 'top', 'fp', 'ie', 'ie_hist', 'fara', 'cert', 'fd') if p.get(k)}
    q['st'] = p['st']; return q

used_rec = set(); added = 0; races_done = 0
for f in sorted(glob.glob(os.path.join(H, 'research', 'house', '*.json'))):
    j = json.load(open(f, encoding='utf-8')); st = j['state']
    for k, v in j['cites'].items(): CITES['hn_' + k] = {'t': v['t'], 'u': v['u']}
    for x in j['races']:
        r = R.get(x['race'])
        if r is None: raise SystemExit('unknown race ' + x['race'])
        if r.get('research') == 'complete': continue          # hand-researched races stay as they are
        inc = x.get('incumbent')
        if inc and inc.get('name'):
            r['incumbent'] = {'name': inc['name'], 'party': party(inc.get('party'))[0], 'status': inc.get('status', '')}
        ids = []
        for n in x['nominees']:
            rid = n.get('rec') or ''
            cid = rid if rid else '%s-%s' % (x['race'].lower(), slug(n['name']))
            if cid in C and C[cid].get('research') == 'complete': ids.append(cid); continue
            p, plabel = party(n.get('party'))
            c = {'id': cid, 'name': n['name'], 'party': p, 'race': x['race'], 'incumbent': bool(n.get('incumbent')), 'research': 'records'}
            if p == 'O' and plabel: c['party_note'] = plabel
            if n.get('fec'): c['fec_id'] = n['fec'][0]
            if rid: c['rec'] = rid; used_rec.add(rid)
            C[cid] = c; ids.append(cid); added += 1
        r['candidates'] = ids
        r['note'] = x.get('note', '') or r.get('note', '')
        r['status'] = x.get('status', 'set')
        r['src'] = ['hn_' + k for k in x.get('c', [])]
        r['research'] = 'records'; races_done += 1

# states: every House race now has verified nominees, so a pending state becomes partial
for st in d['states']:
    if st.get('research') != 'complete' and all(R[k].get('candidates') for k in R if R[k].get('state') == st['code'] and R[k].get('chamber') == 'house'):
        st['research'] = 'partial'

# existing Senate/governor/House candidates: their records profile under the same id
for cid, c in C.items():
    if 'rec' not in c and cid in REC: c['rec'] = cid; used_rec.add(cid)
d['rec'] = {rid: slim(REC[rid]) for rid in sorted(used_rec)}

# everyone else who filed for each race
def race_of(p):
    if p['office'] == 'house':
        dd = p['dist'] or '00'
        return '%s-%s' % (p['st'], 'AL' if dd in ('00', '0', '') else '%02d' % int(dd))
    return '%s-%s' % (p['st'], 'SEN' if p['office'] == 'senate' else 'GOV')
fil = {}
for rid, p in REC.items():
    if rid in used_rec: continue
    rc = race_of(p)
    if rc not in R:
        if p['office'] == 'house' and p['st'] + '-AL' in R: rc = p['st'] + '-AL'
        else: continue
    r26 = next((y[1] for y in p.get('cyc', []) if y[0] == 2026), 0)
    fil.setdefault(rc, []).append([p['name'], party(p['party'])[0], r26, 1 if p.get('ico') == 'I' else 0])
for rc in fil: fil[rc].sort(key=lambda x: -x[2])
d['filers'] = fil
d['meta']['records_asof'] = '2026-10-13'
d['meta']['house_nominees_checked'] = '2026-10-14'
json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('races updated', races_done, 'candidates added', added, 'records attached', len(d['rec']), 'filer lists', len(fil), 'filers', sum(len(v) for v in fil.values()))
print('data %.2f MB' % (os.path.getsize(out) / 1e6))
