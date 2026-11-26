#!/usr/bin/env python3
"""Restores the full nine-channel model of the Road to 1948 network map onto a page rebuilt by
book/plan/road_map/build_road.py. That build regenerates DATA from the road_map JSON, which does not hold the
channels and passes added on 19 Nov 2026 by the tools/patch_*.py scripts (legitimacy, people, land held,
passes 3-12, holdings fix, live breakers), so a rebuild silently drops them (it happened on 23 Nov 2026).

The model as patched is kept in book/plan/road_map/model_full.json (snapshot of 20 Nov 2026). This script
takes the rebuilt page and: keeps the snapshot's model (viab), adding any weighted tie the rebuild has that the
snapshot lacks; keeps the rebuild's ties for display, adding the snapshot's ties for pairs the rebuild lost;
keeps the rebuild's node text, adding the snapshot's nodes the rebuild lost. Idempotent.

Usage: python3 tools/restore_model.py [road-network.html]"""
import json, sys, os, collections
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
SNAP = os.path.join(os.path.dirname(__file__), '..', 'book', 'plan', 'road_map', 'model_full.json')
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
B, end = json.JSONDecoder().raw_decode(s, k)
A = json.load(open(SNAP, encoding='utf-8'))
if len(B['viab']['channels']) == len(A['viab']['channels']) and B['viab'].get('restored'):
    print('model already restored'); sys.exit(0)
V = json.loads(json.dumps(A['viab']))
key = lambda e: (e[0], e[1], e[2])
av = {key(e): i for i, e in enumerate(V['edges'])}
added = changed = 0
for i, e in enumerate(B['viab']['edges']):
    kk = key(e)
    if kk not in av:
        V['edges'].append(e); V['eyear'].append(B['viab']['eyear'][i]); av[kk] = len(V['edges']) - 1; added += 1
# weights the patterns pass (24 Nov) re-derived on the rebuild: take the rebuild's value where the snapshot
# still holds the value the rebuild had before that pass
for kk, w in A.get('_pre_patterns', {}).items():
    f, t, c = kk.split('|'); c = int(c)
    j = av.get((f, t, c)); bi = next((x for x in B['viab']['edges'] if key(x) == (f, t, c)), None)
    if j is not None and bi is not None and abs(bi[4] - w) > 1e-6:
        V['edges'][j] = bi; changed += 1
for a, v in B['viab']['actors'].items():
    if a not in V['actors']: V['actors'][a] = v
for a, v in A.get('_actor_fixes', {}).items(): V['actors'][a] = v
cap = collections.defaultdict(float)
for e in V['edges']: cap[e[2]] += e[4]
V['cap0'] = [round(cap[i], 4) for i in range(len(V['channels']))]
V['restored'] = True
# display ties: the rebuild's, plus the snapshot's for pairs the rebuild has no tie for
pairs = {(e['f'], e['t']) for e in B['edges']} | {(e['t'], e['f']) for e in B['edges']}
nodes_b = {n['id'] for n in B['nodes']}
lost_n = [n for n in A['nodes'] if n['id'] not in nodes_b]
B['nodes'] += lost_n
extra = [e for e in A['edges'] if (e['f'], e['t']) not in pairs]
B['edges'] += extra
B['viab'] = V
B['viability_meta'] = A['viability_meta']
out = s[:k] + json.dumps(B, ensure_ascii=False) + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print(f'model restored: {len(V["channels"])} channels, +{added} weighted ties from the rebuild, {changed} re-derived weights, +{len(lost_n)} nodes, +{len(extra)} display ties')
