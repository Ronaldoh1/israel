#!/usr/bin/env python3
"""The year-by-year tally of US aid to Israel ("aid_tally" dashboard) in index.html.

Puts book/src/aid_tally_dashboard.json (written by book/plan/aid_tally/tally.py) into window.DASHBOARDS, so
the Aid and Arms volume can embed its panels with <figure class="fig-dash" data-ref="aid_tally:Tab:N">.
Replaces an earlier copy, so a re-run after the tally changes updates it. Usage: python3 tools/patch_aid_tally.py [index.html]"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')
s = open(P, encoding='utf-8').read()
D = json.load(open(os.path.join(ROOT, 'book', 'src', 'aid_tally_dashboard.json'), encoding='utf-8'))
head = 'window.DASHBOARDS = '
i = s.index(head) + len(head)
obj, end = json.JSONDecoder().raw_decode(s, i)
new = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
key = '"aid_tally": '
k = s.find(key, i, end)
if k >= 0:                                   # replace the earlier copy in place
    _, vend = json.JSONDecoder().raw_decode(s, k + len(key))
    s = s[:k + len(key)] + new + s[vend:]
else:                                        # first run: insert at the start of the object
    s = s[:i + 1] + key + new + ', ' + s[i + 1:]
json.JSONDecoder().raw_decode(s, i)          # the object still parses
open(P, 'w', encoding='utf-8').write(s)
print('aid_tally dashboard', 'updated' if k >= 0 else 'added')
