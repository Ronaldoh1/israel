"""Build the deep-rebuild source for one chapter: every scene its manifest uses (own + drawn from other chapters),
with entity details, expanded text, deep dives and links, plus the chapter's research addenda and citation labels.
Usage: python3 tools/book_extract_deep.py rd2   -> book/src/rd2_deep.json"""
import json, os, re, sys
cid = sys.argv[1]
s = open('index.html', encoding='utf-8').read()
g = lambda p: json.loads(re.search(p, s, re.S).group(1))
D = {x['id']: x for x in g(r'<script id="scenedata" type="application/json">(.*?)</script>')}
CH = g(r'window\.CHAPTERS = (\[.*?\]);\n'); EX = g(r'<script id="expanded-en" type="application/json">(.*?)</script>')
DD = g(r'<script id="deepdive-en" type="application/json">(.*?)</script>'); CL = g(r'window\.CITE_LABELS = (\{.*?\});\n')
man = json.load(open('book/part1/%s/_manifest.json' % cid, encoding='utf-8'))
own = next(c for c in CH if c['id'] == cid)['scenes']
ids = []
for m in man['sections']:
    for x in [m.get('scene')] + m.get('draws', []):
        if x and x not in ids: ids.append(x)
missing = [x for x in own if x not in ids]
assert not missing, 'own scenes not placed in the manifest: %s' % missing
RS = {}
for fn in os.listdir('book/research'):
    if fn.endswith('.json'):
        for e in json.load(open('book/research/' + fn, encoding='utf-8'))['entries']: RS[e['id']] = e
out = {'chapter': cid, 'title': man.get('title'), 'sections': man['sections'], 'scenes': [], 'research': [], 'citation_labels': {}}
keys = set()
for sid in ids:
    x = D[sid]; sc = {k: x.get(k) for k in ('id', 'yr', 't', 'sub', 'n', 'tld', 'rec')}; sc['home_chapter'] = next((c['id'] for c in CH if sid in c['scenes']), None); sc['entities'] = []
    for e in x['ents']:
        ee = {'id': e['id'], 'name': e.get('nm'), 'role': e.get('rl'), 'detail': e.get('dt')}
        if EX.get(sid, {}).get(e['id']): ee['expanded'] = EX[sid][e['id']].get('dt')
        d = DD.get(sid, {}).get(e['id'])
        if d: ee['deep_dive'] = {'title': d.get('title'), 'subtitle': d.get('subtitle'), 'lead': d.get('lead'), 'sections': [{'heading': q.get('heading'), 'body': q.get('body')} for q in d.get('sections', [])]}
        sc['entities'].append(ee)
    sc['links'] = [{'from': q['f'], 'to': q['t'], 'type': q.get('ty')} for q in x.get('cs', [])]
    out['scenes'].append(sc); keys |= set(re.findall(r'\[cite:([a-zA-Z0-9_]+)\]', json.dumps(sc)))
for m in man['sections']:
    for r in m.get('research', []):
        if r in RS and RS[r] not in out['research']: out['research'].append(RS[r])
out['citation_labels'] = {k: CL.get(k, '') for k in sorted(keys)}
for r in out['research']:
    for c in r['sources']: out['citation_labels'][c['key']] = c['label']
json.dump(out, open('book/src/%s_deep.json' % cid, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('%s: %d sections, %d scenes (%d own, %d drawn), %d research entries, %d citation keys' % (cid, len(man['sections']), len(ids), len(own), len(ids) - len(own), len(out['research']), len(out['citation_labels'])))
