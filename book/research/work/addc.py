"""Append verified claims to a stage working file: python3 addc.py STAGE ENTRY 'topic' KEY URL 'label' STRENGTH 'claim text'"""
import json, sys, os
st, entry, topic, key, url, label, strength, text = sys.argv[1:9]
p = os.path.join(os.path.dirname(__file__), st + '.work.json')
d = json.load(open(p)) if os.path.exists(p) else {}
e = d.setdefault(entry, {'topic': topic, 'claims': [], 'sources': {}})
e['sources'][key] = {'url': url, 'label': label}
e['claims'].append({'text': text, 'strength': strength, 'sources': [key]})
json.dump(d, open(p, 'w'), indent=1, ensure_ascii=False)
print(st, entry, len(e['claims']))
