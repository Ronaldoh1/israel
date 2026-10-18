"""Add many claims from a JSON payload on stdin: {"stage":..,"entry":..,"topic":..,"sources":{key:{url,label}},"claims":[[text,strength,[keys]],...]}"""
import json, sys, os
x = json.load(sys.stdin)
p = os.path.join(os.path.dirname(__file__), x['stage'] + '.work.json')
d = json.load(open(p)) if os.path.exists(p) else {}
e = d.setdefault(x['entry'], {'topic': x['topic'], 'claims': [], 'sources': {}})
e['sources'].update(x['sources'])
for t, s, k in x['claims']:
    assert all(kk in e['sources'] for kk in k), k
    e['claims'].append({'text': t, 'strength': s, 'sources': k})
json.dump(d, open(p, 'w'), indent=1, ensure_ascii=False)
print(x['stage'], x['entry'], len(e['claims']), 'claims;', sum(len(v['claims']) for v in d.values()), 'in stage')
