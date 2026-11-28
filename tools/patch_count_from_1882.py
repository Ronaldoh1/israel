#!/usr/bin/env python3
"""Count lost work from 1882 (27 Nov 2026). The model used to ignore lost work until the movement reached 5% of its 1948
size ("material" threshold), which wiped out 1882-86, when Edmond de Rothschild and Hovevei Zion were nearly the whole
effort. Set to 0 so every year counts. Writes the page and the saved model. Idempotent.

Usage: python3 tools/patch_count_from_1882.py [road-network.html]"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
s = open(P, encoding='utf-8').read(); k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if D['viab'].get('material') != 0:
    D['viab']['material'] = 0; open(P, 'w', encoding='utf-8').write(s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]); print('page: material 0')
S = json.load(open(SNAP, encoding='utf-8'))
if S['viab'].get('material') != 0:
    S['viab']['material'] = 0; json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False); print('saved model: material 0')
