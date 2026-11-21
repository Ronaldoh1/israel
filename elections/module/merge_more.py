"""Second-stage merge, run after merge_house.py:
  1. full candidate dossiers in research/<id>.json for candidates not yet complete (same rules as merge_research_v2)
  2. completion patches in research/completion/<id>.json (checklist, checks, legal, democracy, finances)
  3. governor nominees in research/gov/<RACE>.json
  4. record aliases where the records id differs from the module id
Usage: python3 merge_more.py data_states.json data_states.json"""
import json, glob, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, 'data_states.json')
out = sys.argv[2] if len(sys.argv) > 2 else src
d = json.load(open(src, encoding='utf-8')); C, R, CI = d['cands'], d['races'], d['cites']
REC = json.load(open(os.path.join(H, 'records', 'records.json'), encoding='utf-8'))

def recite(obj, pre):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == 'c' and isinstance(v, list): obj[k] = [pre + x for x in v]
            else: recite(v, pre)
    elif isinstance(obj, list):
        for x in obj: recite(x, pre)
def add_cites(cites, pre):
    for k, v in (cites or {}).items():
        if isinstance(v, dict) and v.get('u'): CI[pre + k] = {'t': v.get('t', ''), 'u': v['u']}
def slim(p):
    q = {k: p[k] for k in ('fec', 'cyc', 'pac', 'pac26', 'lob', 'top', 'fp', 'ie', 'ie_hist', 'fara', 'cert', 'fd') if p.get(k)}
    q['st'] = p['st']; return q
PMAP = {'D': 'D', 'R': 'R', 'L': 'L', 'G': 'G', 'I': 'I', 'C': 'C'}
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

# 4. aliases (module id -> records id)
ALIAS = {'az-08-abe-hamadeh': 'az-08-abraham-hamadeh'}
for cid, rid in ALIAS.items():
    if cid in C and rid in REC: C[cid]['rec'] = rid

# refresh every attached record from the corrected records build
for cid, c in C.items():
    rid = c.get('rec')
    if rid and rid in REC: d['rec'][rid] = slim(REC[rid])
    elif rid and rid not in REC: c.pop('rec', None)

# 1. full dossiers
done = []
for path in sorted(glob.glob(os.path.join(H, 'research', '*.json'))):
    cid = os.path.basename(path)[:-5]
    if cid not in C or C[cid].get('research') == 'complete' or cid.endswith('-votes') or cid.endswith('-races') or cid.endswith('-house'): continue
    D0 = json.load(open(path, encoding='utf-8'))
    if not isinstance(D0, dict) or 'profile' not in D0: continue
    pre = 'k' + re.sub(r'[^a-z0-9]', '', cid)[-14:] + '_'
    add_cites(D0.pop('cites', {}), pre); D0.pop('research_notes', None); D0.pop('id', None); recite(D0, pre)
    c = C[cid]
    for k, v in D0.items():
        if k in ('id', 'name', 'party', 'race', 'incumbent', 'research'): continue
        if v in (None, {}, []) and k not in ('legal', 'foreign', 'democracy', 'money_flags'): continue
        c[k] = v
    if c.get('money_flags_note'): c.setdefault('checklist', {})['money_history'] = 'news'
    c['research'] = 'complete'; done.append(cid)

# 2. completion patches
patched = []
for path in sorted(glob.glob(os.path.join(H, 'research', 'completion', '*.json'))):
    P = json.load(open(path, encoding='utf-8')); cid = P.get('id') or os.path.basename(path)[:-5]
    if cid not in C:
        cid = {v: k for k, v in ALIAS.items()}.get(cid, cid)
        if cid not in C: continue
    pre = 'q' + re.sub(r'[^a-z0-9]', '', cid)[-14:] + '_'
    add_cites(P.pop('cites', {}), pre); P.pop('research_notes', None); P.pop('id', None); recite(P, pre)
    c = C[cid]
    if P.get('checklist'): c.setdefault('checklist', {}).update(P['checklist'])
    if P.get('checks'): c.setdefault('checks', {}).update(P['checks'])
    for k in ('legal', 'democracy', 'finances', 'foreign', 'recordx', 'money_flags'):
        if k in P: c[k] = P[k]
    c.pop('_sc', None); patched.append(cid)

# 3. governor nominees
gov = 0
for path in sorted(glob.glob(os.path.join(H, 'research', 'gov', '*.json'))):
    j = json.load(open(path, encoding='utf-8'))
    for k, v in j.get('cites', {}).items(): CI['gv_' + k] = {'t': v['t'], 'u': v['u']}
    for x in j['races']:
        r = R[x['race']]
        if r.get('candidates'): continue
        inc = x.get('incumbent') or {}
        if inc.get('name'): r['incumbent'] = {'name': inc['name'], 'party': PMAP.get((inc.get('party') or '')[:1].upper(), 'O'), 'status': inc.get('status', '')}
        ids = []
        for n in x['nominees']:
            cid = n.get('rec') or '%s-%s' % (x['race'].lower(), slug(n['name']))
            p = (n.get('party') or '').strip()
            c = {'id': cid, 'name': n['name'], 'party': PMAP.get(p[:1].upper(), 'O') if len(p) <= 3 else ('L' if 'libert' in p.lower() else 'G' if 'green' in p.lower() else 'O'),
                 'race': x['race'], 'incumbent': bool(n.get('incumbent')), 'research': 'records'}
            if c['party'] == 'O' and p: c['party_note'] = p
            if n.get('rec') and n['rec'] in REC: c['rec'] = n['rec']; d['rec'][n['rec']] = slim(REC[n['rec']])
            C[cid] = c; ids.append(cid); gov += 1
        r['candidates'] = ids; r['note'] = x.get('note', ''); r['status'] = x.get('status', 'set')
        r['src'] = ['gv_' + k for k in x.get('c', [])]; r['research'] = 'records'

# races: complete when every candidate is complete; in progress otherwise
for r in R.values():
    ids = r.get('candidates') or []
    if ids and all(C[i].get('research') == 'complete' for i in ids): r['research'] = 'complete'
    elif any(C[i].get('research') == 'complete' for i in ids) and r.get('research') != 'complete': r['research'] = 'partial'
json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('dossiers merged', len(done), done)
print('completion patches', len(patched), 'governor nominees added', gov)
