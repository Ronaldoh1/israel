#!/usr/bin/env python3
"""Coverage-audit fix (19 Nov 2026). Land bought by private buyers and companies ('other_holdings' via
'private_land') reached the core of the map only through PICA, so removing PICA also erased the 564,000
dunams that private buyers held: an artifact of the wiring, not of the record. The WZO's land company bought
land with JNF and private money (Encyclopedia.com), which is the documented route by which private buying
reached the organized movement. Added as a reported tie, weighted in the land channel, with the land
capacity raised by the same amount so the full-record figure holds. Idempotent.
Usage: python3 tools/patch_holdings_reach.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if any(e[0] == 'pldc' and e[1] == 'private_land' for e in V['edges']):
    print('holdings reach already fixed'); sys.exit(0)
C = {c: i for i, c in enumerate(V['channels'])}
ref = {"t": "Encyclopedia.com, Palestine Land Development Company (established 1908 by Arthur Ruppin as part of the World Zionist Organization; bought land with JNF and private money)",
       "u": "https://www.encyclopedia.com/humanities/encyclopedias-almanacs-transcripts-and-maps/palestine-land-development-company"}
D['edges'].append({"f": "pldc", "t": "private_land", "label": "The World Zionist Organization's land company, founded in 1908, bought land with Jewish National Fund money and with private money.",
                   "type": "land purchase", "status": "reported", "src": "", "n": 1, "sec": "", "refs": [ref], "ext": True})
v = 0.6
V['edges'].append(['pldc', 'private_land', C['land'], 0.6, v]); V['eyear'].append([0, 0])
V['cap0'][C['land']] = round(V['cap0'][C['land']] + v, 4)
D['viability_meta']['per_channel']['land'] = sum(1 for e in V['edges'] if e[2] == C['land'])
V['holdings_reach_fix'] = '2026-11-19'
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('holdings reach fixed; land capacity', V['cap0'][C['land']])
