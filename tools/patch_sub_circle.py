#!/usr/bin/env python3
"""Substitutes from the same circle (27 Nov 2026). When an actor is removed, the model lets the strongest actor already
doing the same kind of work take over the role. It used to pick from anyone on the same side, which gave absurd results:
Edmond de Rothschild standing in for Herzl's fund-raising (Edmond refused Herzl in 1896), Hovevei Zion paying for the
colonies it had to hand to Edmond because it could not, a Manchester editor standing in for President Wilson, the Ottoman
state for the US Treasury. A substitute must now come from the removed actor's own circle (its cluster on the map: the
Zionist movement, the American lobby, the British state, finance, the Rothschilds, and so on). Writes the page (data and
code) and the saved model. Idempotent.

Usage: python3 tools/patch_sub_circle.py [road-network.html]"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
def apply(D):
    N = {n['id']: n for n in D['nodes']}
    D['viab']['circle'] = {a: N.get(a, {}).get('cluster', '') for a in D['viab']['actors']}
s = open(P, encoding='utf-8').read(); k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k); apply(D)
s = s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]
S = json.load(open(SNAP, encoding='utf-8')); apply(S); json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False)
a = "if(b===a||rem.has(b)||A[b][2]!==A[a][2]||A[b][0]>y) continue;"
b = "if(b===a||rem.has(b)||A[b][2]!==A[a][2]||A[b][0]>y||(VB.circle&&VB.circle[b]!==VB.circle[a])) continue;"
if b not in s:
    assert s.count(a) == 1; s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s); print('substitutes from the same circle')
