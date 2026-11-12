"""Every test that breaks the founding: single removals, documented groups, and the smallest combinations of people
and bodies whose joint removal drops the chance of a state by 1948 below 35 ('Very unlikely' or worse).
Each result carries its chain of consequences: the key decisions that become unlikely, the force and votes lost
with them, the years of work lost, and the weakest channel. Writes breakers.json."""
import json, itertools, os, time
import viability as V
HERE = os.path.dirname(os.path.abspath(__file__))
CUT = 35.0          # below this the rating is 'Very unlikely' or 'Not possible on this record'
OUTCOME = {'decl_indep', 'provisional', 'israel_gov', 'recognition48'}   # the founding itself: removing it is not a test
POOL = 60           # pairs are searched among the 60 actors whose single removal costs most
POOL3 = 26          # triples among the top 26

def chain(M, R, inp):
    out = {'V': round(R['P'], 1), 'rating': V.rating(R['P']), 'weakest': V.CHANNELS[min(range(V.NC), key=lambda i: R['pc'][i])],
           'channels': [round(x, 3) for x in R['pc']], 'lost_years': round(R.get('lost_years', 0), 1),
           'knocked_out': sorted(set(R.get('removed', set())) - set(inp)),
           'decisions': [{'name': D['name'], 'chance': round(100 * D['chance'])} for D in R.get('decisions', [])],
           'read': V.readings(M, R)}
    return out

def main():
    d = json.load(open(os.path.join(HERE, 'network.json'))); M = V.model(d)
    N = {n['id']: n for n in d['nodes']}; R0 = V.score(M, set()); base = R0['P']
    nm = lambda i: N[i]['name'] if i in N else i
    t0 = time.time()
    single = {}
    for n in d['nodes']:
        if n['id'] in OUTCOME: continue
        R = V.score(M, {n['id']}); single[n['id']] = R['P']
    singles = [dict(ids=[i], names=[nm(i)], **chain(M, V.score(M, {i}), [i])) for i, p in sorted(single.items(), key=lambda x: x[1]) if p < 55]
    groups = []
    G = M['groups']
    for g, ids in G.items():
        R = V.score(M, set(ids), set(M['drop'].get(g, [])))
        groups.append(dict(group=g, n=len(ids), **chain(M, R, ids)))
    gpairs = []
    for a, b in itertools.combinations(G, 2):
        ids = set(G[a]) | set(G[b]); dr = set(M['drop'].get(a, [])) | set(M['drop'].get(b, []))
        R = V.score(M, ids, dr)
        Va = next(x['V'] for x in groups if x['group'] == a); Vb = next(x['V'] for x in groups if x['group'] == b)
        if R['P'] < CUT and Va >= CUT and Vb >= CUT: gpairs.append(dict(groups=[a, b], alone=[Va, Vb], **chain(M, R, ids)))
    pool = [i for i, p in sorted(single.items(), key=lambda x: x[1]) if p < base - 0.05 and N[i]['kind'] != 'document' or i in ('balfour_decl', 'mandate', 'res181')][:POOL]
    pool = [i for i in pool if single[i] >= CUT]
    pairs = []; broken = set()
    for a, b in itertools.combinations(pool, 2):
        R = V.score(M, {a, b})
        if R['P'] < CUT:
            pairs.append(dict(ids=[a, b], names=[nm(a), nm(b)], alone=[round(single[a], 1), round(single[b], 1)], **chain(M, R, [a, b]))); broken.add(frozenset((a, b)))
    triples = []
    for a, b, c in itertools.combinations(pool[:POOL3], 3):
        if any(frozenset(p) in broken for p in ((a, b), (a, c), (b, c))): continue
        R = V.score(M, {a, b, c})
        if R['P'] < CUT:
            triples.append(dict(ids=[a, b, c], names=[nm(a), nm(b), nm(c)], alone=[round(single[x], 1) for x in (a, b, c)], **chain(M, R, [a, b, c])))
    pairs.sort(key=lambda x: x['V']); triples.sort(key=lambda x: x['V']); gpairs.sort(key=lambda x: x['V'])
    out = {'built': time.strftime('%Y-%m-%d'), 'baseline': round(base, 1), 'cut': CUT, 'pool': len(pool), 'pool3': min(POOL3, len(pool)),
           'searched': {'singles': len(single), 'groups': len(G), 'group_pairs': len(G) * (len(G) - 1) // 2,
                        'pairs': len(pool) * (len(pool) - 1) // 2, 'triples': len(list(itertools.combinations(pool[:POOL3], 3)))},
           'singles': singles, 'groups': sorted(groups, key=lambda x: x['V']), 'group_pairs': gpairs, 'pairs': pairs, 'triples': triples,
           'secs': round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(HERE, 'breakers.json'), 'w'), ensure_ascii=False, indent=1)
    return out

if __name__ == '__main__':
    o = main()
    print({k: (len(v) if isinstance(v, list) else v) for k, v in o.items()})
