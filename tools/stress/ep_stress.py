#!/usr/bin/env python3
"""Stress test of the Epstein what-if model (book/plan/epstein_map/ep_viability.py), mirroring the 1948 map's.
Runs the 17 published tests under alternative assumptions, leaves each of the most-used sources out in turn,
and runs two 'seat' tests (who else could have held Epstein's place). Writes tools/stress/ep_stress_<date>.json.
Usage: python3 tools/stress/ep_stress.py"""
import json, math, sys, os, copy, datetime, collections
HERE = os.path.dirname(os.path.abspath(__file__))
EM = os.path.join(HERE, '..', '..', 'book', 'plan', 'epstein_map')
sys.path.insert(0, EM)
import ep_viability as V

D0 = json.load(open(os.path.join(EM, 'network.json')))
G = V.GROUPS
TESTS = [('epstein', ['epstein']), ('gmax', ['gmax']), ('both', ['epstein', 'gmax']), ('wexner', ['wexner']),
         ('black', ['black', 'bv70']), ('payers', G['The big payers (Wexner and Black)']), ('jpm', ['jpm']),
         ('banks', G['The banks']), ('npa', ['npa']), ('acosta', ['acosta']), ('defence', G['The defence lawyers (2005-08)']),
         ('herald', G['The Miami Herald and its series']), ('giuffre', ['giuffre', 'boies']), ('usvi', ['usvi_edc', 'usvi']),
         ('properties', G['The properties']), ('aircraft', G['The aircraft and pilots']), ('reputation', G['The reputation managers'])]

EXP = [1.0] * len(V.CHANNELS); FLOOR = 0.5
_base = V.base
def base(M, removed, after=None):
    R = _base(M, removed, after)
    eff = [(FLOOR + (1 - FLOOR) * p if i in M['cover'] else p) ** EXP[i] for i, p in enumerate(R['pc'])]
    R['P'] = 100 * math.prod(eff); return R
V.base = base

def build(d=None):
    d = copy.deepcopy(d or D0)
    return d, V.model(d)

def run_tests(M):
    out = {'base': V.score(M, set())['P']}
    for k, ids in TESTS: out[k] = V.score(M, set(i for i in ids)) ['P']
    return out

def variant(**kw):
    global EXP, FLOOR
    saved = {k: getattr(V, k) for k in ('SW', 'DEFAULT_M', 'DEFAULT_BANK_YEARS', 'CAL')}
    e0, f0 = EXP[:], FLOOR
    try:
        for k, v in kw.items():
            if k == 'exp': EXP = v
            elif k == 'floor': FLOOR = v
            elif k == 'reported': V.SW = dict(V.SW, reported=v, probable=v, planned=v, scheduled=v)
            else: setattr(V, k, v)
        d, M = build()
        if 'herald_w' in kw: pass
        return run_tests(M)
    finally:
        for k, v in saved.items(): setattr(V, k, v)
        EXP, FLOOR = e0, f0

res = {'published': variant()}
for i, c in enumerate(V.CHANNELS):
    for m in (0.5, 2.0):
        e = [1.0] * len(V.CHANNELS); e[i] = m; res[f'exp_{c}_x{m}'] = variant(exp=e)
for v in (0.3, 1.0): res[f'reported_{v}'] = variant(reported=v)
for v in (0.25, 4.0): res[f'default_m_{v}'] = variant(DEFAULT_M=v)
for v in (1, 10): res[f'bank_years_{v}'] = variant(DEFAULT_BANK_YEARS=v)
for v in (0.25, 0.75): res[f'cover_floor_{v}'] = variant(floor=v)
for v in (0.95, 0.999): res[f'cal_{v}'] = variant(CAL=v)
# decision weights: the Herald counted once instead of twice; an unknown successor at half and double weight
for name, fn in (('herald_once', lambda: V.DECISIONS[1]['weights'].update({'herald_series': 1})),
                 ('unknown_succ_0.5', lambda: setattr(V, 'UNKNOWN_SUCCESSOR', 0.5)),
                 ('unknown_succ_2', lambda: setattr(V, 'UNKNOWN_SUCCESSOR', 2))):
    keep = (copy.deepcopy(V.DECISIONS), V.UNKNOWN_SUCCESSOR); fn(); res[name] = variant(); V.DECISIONS[:] = keep[0]; V.UNKNOWN_SUCCESSOR = keep[1]

# leave one source out: the sources behind the most weighted ties
d, M = build()
wt = {(f, t) for f, t, c, w, y in M['edges']}
cnt = collections.Counter()
for e in D0['edges']:
    if (e['f'], e['t']) in wt:
        for s in [r['u'] for r in e.get('refs', [])] or [e.get('src', '')]:
            if s: cnt[s] += 1
loso = {}
pub = res['published']
for s, n in cnt.most_common(40):
    d = copy.deepcopy(D0)
    keep = []
    for e in d['edges']:
        srcs = [r['u'] for r in e.get('refs', [])] or [e.get('src', '')]
        if s in srcs and len(set(srcs)) == 1: continue   # the tie rests on this source alone
        keep.append(e)
    d['edges'] = keep
    _, M2 = build(d); r = run_tests(M2)
    k = max(r, key=lambda x: abs(r[x] - pub[x]))
    loso[s] = {'n': n, 'test': k, 'shift': round(r[k] - pub[k], 1)}

# seat tests: someone else in Epstein's place
def seat(rule):
    d, M = build(); N = {n['id']: n for n in D0['nodes']}
    own = collections.defaultdict(set)   # Maxwell's own documented ties (not through Epstein)
    for e in D0['edges']:
        if e['status'] in ('verified', 'reported') and e['type'] not in V.PROBE:
            if e['f'] == 'gmax' and e['t'] != 'epstein': own['gmax'].add(e['t'])
            if e['t'] == 'gmax' and e['f'] != 'epstein': own['gmax'].add(e['f'])
    def keep(x):
        if rule == 'maxwell': return x in own['gmax'] or x in M['ent']
        if rule == 'institutions': return N.get(x, {}).get('kind') in ('institution', 'company', 'government', 'place', 'trust', 'project') or x in M['ent']
    rows = []
    for f, t, c, w, y in M['edges']:
        if 'epstein' in (f, t):
            x = t if f == 'epstein' else f
            if not keep(x): rows.append(['x_lost', x, c, w, y]); continue   # lost tie: kept in the full record, cut here
        rows.append([f, t, c, w, y])
    M2 = dict(M, edges=rows)
    R = V.score(M2, {'x_lost'})
    return R['P'], sum(1 for r in rows if r[0] == 'x_lost'), [round(x, 3) for x in R['pc']]
seats = {r: dict(zip(('P', 'ties_lost', 'pc'), seat(r))) for r in ('maxwell', 'institutions')}

lo = {k: min(v[k] for n, v in res.items() if n != 'published') for k in pub}
hi = {k: max(v[k] for n, v in res.items() if n != 'published') for k in pub}
out = {'built': str(datetime.date.today()), 'published': pub, 'variants': res, 'range': {k: [round(pub[k], 1), round(lo[k], 1), round(hi[k], 1)] for k in pub},
       'loso': loso, 'seats': seats}
P = os.path.join(HERE, f'ep_stress_{datetime.date.today()}.json')
json.dump(out, open(P, 'w'), indent=1)
for k in pub: print(f'{k:12} {pub[k]:6.1f}  range {lo[k]:6.1f} – {hi[k]:6.1f}')
print('largest single-source shifts:', sorted(loso.items(), key=lambda kv: -abs(kv[1]['shift']))[:5])
print('seats', seats)
