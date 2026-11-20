#!/usr/bin/env python3
"""Maps node kinds added in the November 2026 passes onto the map's seven drawn kinds (person, institution,
company, government, document, event, place). Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
MAP = {'organization': 'institution', 'militia': 'institution', 'media': 'company', 'infrastructure': 'place', 'population': 'event'}
n = 0
for x in D['nodes']:
    if x['kind'] in MAP:
        x['kind'] = MAP[x['kind']]; n += 1
for x in D['nodes']:
    if x['id'] == 'palestine_post': x['kind'] = 'company'
    if x['id'] == 'jta_news': x['kind'] = 'institution'
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('kinds normalized:', n)
