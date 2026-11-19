#!/usr/bin/env python3
"""Counterforces pass, step 1: opposition ties no longer count as the movement's capacity. Each listed
weighted tie records an opponent acting against the founding (or a vote against); its weight is set to
zero and the channel's full-record total is reduced by the same amount, so the baseline does not move.
Opposition is weighed instead in the decision model (push against resistance). Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
OPP = [('henderson','marshall_g'),('kennan','state_dept'),('marshall_g','may12'),('partition_notes','cuba'),
       ('partition_notes','greece'),('siam','res181'),('india','res181'),('tardini','vatican'),('pius12','sharett'),
       ('merry_del_val','vatican'),('gasparri','vatican'),('maglione','vatican'),('pius12','un'),('vatican','res181')]
if V.get('opp_zeroed'):
    print('sign fix already applied'); sys.exit(0)
done = []
for e in V['edges']:
    if (e[0], e[1]) in OPP and e[4] > 0:
        V['cap0'][e[2]] = round(V['cap0'][e[2]] - e[4], 4); done.append((e[0], e[1], V['channels'][e[2]], round(e[4], 2))); e[4] = 0.0
V['opp_zeroed'] = [list(x[:2]) for x in done]
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
for x in done: print('zeroed', x)
print(len(done), 'opposition ties zeroed')
