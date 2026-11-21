#!/usr/bin/env python3
"""Coverage audit: the one weighted tie still marked to-verify (Kofer HaYishuv -> Haganah) gets a second
source and is marked reported; its weight is unchanged. Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
n = 0
for e in D['edges']:
    if e['f'] == 'kofer' and e['t'] == 'haganah' and e['status'] == 'to-verify':
        e['status'] = 'reported'
        e['refs'] = (e.get('refs') or []) + [{"t": "Canadian Jewish News, David Matlow on Kofer HaYishuv (established by the Va'ad Leumi in 1938; the money 'was used to train soldiers, establish defence units, build fences')", "u": "https://thecjn.ca/arts/treasure-trove-david-matlow-looks-at-a-fund-that-helped-jewish-settlements-protect-themselves/"}]
        n += 1
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('kofer tie verified:', n)
