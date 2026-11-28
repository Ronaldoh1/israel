"""Build language-atlas.html (repo root) from atlas_template.html + atlas_data.py + the shared basemap.
Usage: python3 build_atlas.py [OUT]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
import atlas_data as A

geo = json.load(open(os.path.join(REPO, 'tools/geo_base.json')))
# other Jewish lineages, from the library's lineages dashboard (numbered points only, Ashkenazim excluded)
lin = []
ld = json.load(open(os.path.join(REPO, 'book/src/lineages_dashboard.json')))
for t in ld['tabs']:
    for s in t['sections']:
        if s.get('type') != 'geomap': continue
        fam = s.get('families', {})
        for p in s['points']:
            if p.get('n') and p.get('lang') and p['id'] != 'ashkenazi' and p['id'] not in [x['id'] for x in lin]:
                lin.append({'id': p['id'], 'name': p['name'], 'place': p.get('place', ''), 'lang': p['lang'], 'c': fam.get(p.get('family'), ['', '#888'])[1]})

for l in A.LANGS:
    for k in l['src']: assert k in A.SRC, k
for a in A.ASHK:
    for k in a['src']: assert k in A.SRC, k
for c in A.ASHK_ANCESTRY:
    for k in c[2]: assert k in A.SRC, k

D = {'src': A.SRC, 'branch': A.BRANCH, 'tree': A.TREE, 'siblings': A.TREE_SIBLINGS, 'langs': A.LANGS,
     'routes': A.ROUTES, 'origin': A.ORIGIN, 'ashk': A.ASHK, 'ancestry': A.ASHK_ANCESTRY, 'lineages': lin,
     'geo': {k: geo[k] for k in ['W', 'H', 'lon0', 'lat1', 'k', 'land', 'borders']}}
t = open(os.path.join(HERE, 'atlas_template.html'), encoding='utf-8').read()
t = t.replace('__DATA__', json.dumps(D, ensure_ascii=False).replace('</', '<\\/'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'language-atlas.html')
open(out, 'w', encoding='utf-8').write(t)
print('built', out, len(A.LANGS), 'languages', len(A.ASHK), 'stages', len(lin), 'other lineages', len(t) // 1024, 'KB')
