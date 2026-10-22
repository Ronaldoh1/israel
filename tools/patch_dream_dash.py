#!/usr/bin/env python3
"""The American Dream Architecture data dashboard ("dream") (index.html).

Adds the dashboard in book/src/dream_dashboard.json (built from the ad_series files) to
window.DASHBOARDS, so library figures can embed its panels with <figure class="fig-dash" data-ref="dream:Tab:N">.
Idempotent. Run after patch_scorecard22.py. Usage: python3 tools/patch_dream_dash.py [index.html]"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '"dream":' in s.split('window.DASHBOARDS = ', 1)[1][:300]:
    print('dream dashboard already applied'); sys.exit(0)
D = json.load(open(os.path.join(ROOT, 'book', 'src', 'dream_dashboard.json'), encoding='utf-8'))
D.pop('scenes', None)
old = 'window.DASHBOARDS = {'
assert s.count(old) == 1
s = s.replace(old, old + '"dream": ' + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + ', ')
open(P, 'w', encoding='utf-8').write(s)
print('dream dashboard applied')
