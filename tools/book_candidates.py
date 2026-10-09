"""List scenes elsewhere in the simulation that a pre-1948 chapter should consider drawing on
(cross-library pull, LIBRARY-PROTOCOL.md section 2). Writes book/plan/<cid>_candidates.json."""
import json, os, re, sys
s = open('index.html', encoding='utf-8').read()
g = lambda p: json.loads(re.search(p, s, re.S).group(1))
SC = {x['id']: x for x in g(r'<script id="scenedata" type="application/json">(.*?)</script>')}
CH = g(r'window\.CHAPTERS = (\[.*?\]);\n'); EX = g(r'<script id="expanded-en" type="application/json">(.*?)</script>'); DD = g(r'<script id="deepdive-en" type="application/json">(.*?)</script>')
cof = {sid: c['id'] for c in CH for sid in c['scenes']}
PRE = ['ch01'] + ['rd%d' % i for i in range(7)]
SPAN = {'rd0': (1694, 1896), 'rd1': (1896, 1917), 'rd2': (1917, 1922), 'rd3': (1922, 1936), 'rd4': (1936, 1945), 'rd5': (1945, 1948), 'rd6': (1948, 1958), 'ch01': None}
claimed = {}
for c in PRE:
    mp = 'book/part1/%s/_manifest.json' % c
    if os.path.exists(mp):
        m = json.load(open(mp))
        for sec in m.get('sections', []) + [x for ch in m.get('chapters', []) for x in ch['sections']]:
            for d in sec.get('draws', []): claimed[d] = c
def blob(sid): return json.dumps(SC[sid], ensure_ascii=False) + json.dumps(EX.get(sid, {}), ensure_ascii=False) + json.dumps(DD.get(sid, {}), ensure_ascii=False)
def names(sid):
    t = re.sub(r'<[^>]+>', ' ', blob(sid))
    return {n for n in re.findall(r'\b[A-Z][a-z]+(?:[ -][A-Z][a-z]+)+', t) if len(n) > 8}
def years(sid):
    ys = [int(y) for y in re.findall(r'\b(1[5-9]\d\d|20[0-2]\d)\b', str(SC[sid].get('yr', '')))]
    return (min(ys), max(ys)) if ys else None
for cid in sys.argv[1:]:
    own = next(c for c in CH if c['id'] == cid)['scenes']
    N = set().union(*[names(x) for x in own])
    out = []
    for sid, x in SC.items():
        h = cof.get(sid)
        if h in PRE or sid in claimed: continue
        y = years(sid); sp = SPAN[cid]; score = 0; why = []
        if sp and y and y[0] <= sp[1] and y[1] >= sp[0] and (y[1] - y[0]) <= 90:
            score += 10; why.append('dates overlap')
        shared = names(sid) & N
        if len(shared) >= 3: score += len(shared); why.append('shares: ' + ', '.join(sorted(shared)[:8]))
        if score >= 10 or (not sp and len(shared) >= 6):
            out.append({'id': sid, 'home': h, 'yr': x.get('yr'), 'title': x['t'], 'score': score, 'why': why})
    out.sort(key=lambda r: -r['score'])
    json.dump({'chapter': cid, 'already_claimed_by_other_chapters': claimed, 'candidates': out[:60]}, open('book/plan/%s_candidates.json' % cid, 'w'), ensure_ascii=False, indent=1)
    print(cid, len(out), 'candidates;', [r['id'] for r in out[:12]])
