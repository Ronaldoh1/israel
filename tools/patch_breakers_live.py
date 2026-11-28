#!/usr/bin/env python3
"""Replace the map's precomputed 'Every removal that breaks it' list (DATA.viab.breakers) with a search run
against the live in-page model (tools/stress/breakers_live.js writes the JSON). The earlier list was built on
12 Nov 2026 by the Python model, which no longer carries the channels, opposition and decision rules added since.
Idempotent: re-running with the same JSON leaves the file unchanged.
Usage: python3 tools/patch_breakers_live.py tools/stress/breakers_live.json [road-network.html]"""
import json, sys
J = sys.argv[1] if len(sys.argv) > 1 else 'tools/stress/breakers_live.json'
P = sys.argv[2] if len(sys.argv) > 2 else 'road-network.html'
B = json.load(open(J, encoding='utf-8'))
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if D['viab'].get('breakers') == B:
    print('breakers already current'); sys.exit(0)
D['viab']['breakers'] = B
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('breakers replaced:', len(B['items']), 'items, built', B['built'])
