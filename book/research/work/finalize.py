"""Turn a stage's working file into book/research/<stage>.json (the library's research format)."""
import json, sys, os, datetime
st = sys.argv[1]; vol = sys.argv[2] if len(sys.argv) > 2 else 'divine'
W = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(W, st + '.work.json')))
out = {'volume': vol, 'verified': datetime.date.today().isoformat(), 'entries': []}
for eid, e in d.items():
    out['entries'].append({'id': eid, 'stage': st, 'topic': e['topic'], 'claims': e['claims'],
                           'sources': [{'key': k, 'url': v['url'], 'label': v['label']} for k, v in e['sources'].items()]})
json.dump(out, open(os.path.join(W, '..', st + '.json'), 'w'), indent=1, ensure_ascii=False)
print(st, len(out['entries']), 'entries', sum(len(e['claims']) for e in out['entries']), 'claims')
