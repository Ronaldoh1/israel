"""Extract a chapter's research (scenes, entity details, expanded text, deep dives, citation labels) from index.html
into book/src/<chapter>.json, the source the book's writers and auditors work from.
Usage: python3 tools/book_extract.py ch05 ch06 ..."""
import json, os, re, sys
s = open('index.html', encoding='utf-8').read()
g = lambda p: json.loads(re.search(p, s, re.S).group(1))
D = {x['id']: x for x in g(r'<script id="scenedata" type="application/json">(.*?)</script>')}
CH = g(r'window\.CHAPTERS = (\[.*?\]);\n'); EX = g(r'<script id="expanded-en" type="application/json">(.*?)</script>')
DD = g(r'<script id="deepdive-en" type="application/json">(.*?)</script>'); CL = g(r'window\.CITE_LABELS = (\{.*?\});\n')
os.makedirs('book/src', exist_ok=True)
for st in sys.argv[1:]:
    c = next(x for x in CH if x['id'] == st); out = {'stage': st, 'name': c['name'], 'scenes': []}; keys = set()
    for sid in c['scenes']:
        x = D[sid]; sc = {k: x.get(k) for k in ('id', 'yr', 't', 'sub', 'n', 'tld', 'rec')}; sc['entities'] = []
        for e in x['ents']:
            ee = {'id': e['id'], 'name': e.get('nm'), 'role': e.get('rl'), 'detail': e.get('dt')}
            if EX.get(sid, {}).get(e['id']): ee['expanded'] = EX[sid][e['id']].get('dt')
            d = DD.get(sid, {}).get(e['id'])
            if d: ee['deep_dive'] = {'title': d.get('title'), 'subtitle': d.get('subtitle'), 'lead': d.get('lead'), 'sections': [{'heading': q.get('heading'), 'body': q.get('body')} for q in d.get('sections', [])]}
            sc['entities'].append(ee)
        sc['links'] = [{'from': q['f'], 'to': q['t'], 'type': q.get('ty')} for q in x.get('cs', [])]
        out['scenes'].append(sc); keys |= set(re.findall(r'\[cite:([a-zA-Z0-9_]+)\]', json.dumps(sc)))
    out['citation_labels'] = {k: CL.get(k, '') for k in sorted(keys)}
    json.dump(out, open('book/src/%s.json' % st, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(st, len(out['scenes']), 'scenes')
