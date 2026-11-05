#!/usr/bin/env python3
"""The Part Twenty-Two scorecard dashboard ("scorecard22") for US System vs Israel System (index.html).

Adds the dashboard in book/src/scorecard22_dashboard.json (built from tools/us22_score.py's output) to
window.DASHBOARDS, so library figures can embed its panels with <figure class="fig-dash" data-ref="scorecard22:Tab:N">.
Idempotent. Run after patch_lineages_map.py. Usage: python3 tools/patch_scorecard22.py [index.html]"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '"scorecard22":' in s.split('window.DASHBOARDS = ', 1)[1][:300]:
    print('scorecard22 dashboard already applied'); sys.exit(0)
D = json.load(open(os.path.join(ROOT, 'book', 'src', 'scorecard22_dashboard.json'), encoding='utf-8'))
D.pop('scenes', None)
old = 'window.DASHBOARDS = {'
assert s.count(old) == 1
s = s.replace(old, old + '"scorecard22": ' + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + ', ')
open(P, 'w', encoding='utf-8').write(s)
print('scorecard22 dashboard applied')
