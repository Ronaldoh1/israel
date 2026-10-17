#!/usr/bin/env python3
"""Maps in dashboards and library figures, and the "Jewish Lineages" map dashboard (index.html).

- Injects the shared basemap (tools/geo_base.json), the map renderer (tools/geo.js) and its styles (tools/geo.css).
- Adds a "geomap" panel type to the simulation's dashboard renderer (the library's tools/charts.js has its own hook).
- Adds the dashboard in book/src/lineages_dashboard.json and links it from the scenes it lists.
Idempotent. Run after patch_four_words.py. Usage: python3 tools/patch_lineages_map.py [index.html]"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '<!--GEO-START-->' in s:
    print('lineages map already applied'); sys.exit(0)
def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('found %d time(s), expected %d: ' % (s.count(old), count)) + old[:110]
    s = s.replace(old, new)
rd = lambda n: open(os.path.join(ROOT, 'tools', n), encoding='utf-8').read()
base = json.load(open(os.path.join(ROOT, 'tools', 'geo_base.json')))
block = ('<!--GEO-START--><style>' + rd('geo.css') + '</style><script>window.OTS_GEO=' + json.dumps(base, separators=(',', ':')) + ';</script><script>' + rd('geo.js') + '</script><!--GEO-END-->\n')
i = s.rfind('</body>'); s = s[:i] + block + s[i:]
swap("pair:pair,venn:venn};", "pair:pair,venn:venn,geomap:function(s){ return window.OTSGeo?window.OTSGeo.render(s):''; }};")
D = json.load(open(os.path.join(ROOT, 'book', 'src', 'lineages_dashboard.json'), encoding='utf-8'))
scenes = D.pop('scenes', [])
swap('window.DASHBOARDS = {', 'window.DASHBOARDS = {"jewish_lineages": ' + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + ', ')
for sid in scenes: assert ('"id":"%s"' % sid) in s, 'unknown scene ' + sid
swap('window.DASH_SCENES = {', 'window.DASH_SCENES = {' + ''.join('"%s": "jewish_lineages", ' % x for x in scenes))
open(P, 'w', encoding='utf-8').write(s)
print('lineages map applied (linked from %d scenes)' % len(scenes))
