"""Which talking points does the Israel module already answer, and where?
Reads the simulation scenes (index.html) and the library sections (book/part1/*/*.html) of the israel repo,
looks for each talking point's phrasings, and writes config/coverage.json.
Usage: python3 build_coverage.py /path/to/israel-repo   (the kit ships with this already run)"""
import json, os, re, sys, glob, html
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..')
TP = json.load(open(os.path.join(HERE, 'config', 'talking_points.json'), encoding='utf-8'))
def plain(s): return html.unescape(re.sub(r'<[^>]+>', ' ', s))
docs = []   # (kind, id, title, text)
s = open(os.path.join(REPO, 'index.html'), encoding='utf-8').read()
g = lambda name: json.loads(re.search(r'<script id="%s" type="application/json">(.*?)</script>' % name, s, re.S).group(1))
EX, DD = g('expanded-en'), g('deepdive-en')
for sc in g('scenedata'):
    parts = [sc.get('t', ''), sc.get('sub', ''), sc.get('n', ''), sc.get('tld', ''), sc.get('rec', '')]
    for e in sc.get('ents', []): parts += [e.get('nm', ''), e.get('rl', ''), e.get('dt', '')]
    parts.append(json.dumps(EX.get(sc['id'], ''))); parts.append(json.dumps(DD.get(sc['id'], '')))
    docs.append(('scene', sc['id'], sc.get('t', ''), plain(' '.join(map(str, parts)))))
for f in sorted(glob.glob(os.path.join(REPO, 'book', 'part1', '*', '*.html'))):
    b = os.path.basename(f)
    if b.startswith('_'): continue
    t = open(f, encoding='utf-8').read(); m = re.search(r'<h2[^>]*>(.*?)</h2>', t, re.S)
    docs.append(('book', os.path.basename(os.path.dirname(f)) + '/' + b[:-5], plain(m.group(1)).strip() if m else b, plain(t)))
out = {}
for p in TP['points']:
    say = [re.compile(x, re.I) for x in p['say']]; cov = [re.compile(x, re.I) for x in p.get('cov', [])]
    hits = []
    for kind, i, title, text in docs:
        n_say = sum(len(r.findall(text)) for r in say); n_cov = sum(len(r.findall(text)) for r in cov)
        if n_say or n_cov: hits.append({'kind': kind, 'id': i, 'title': title, 'say': n_say, 'cov': n_cov})
    hits.sort(key=lambda h: -(h['say'] * 3 + h['cov']))
    named = sum(1 for h in hits if h['say']); topical = len(hits)
    level = 'answered' if named >= 2 or (named and topical >= 4) else 'touched' if topical else 'missing'
    out[p['id']] = {'level': level, 'places_naming_it': named, 'places_on_topic': topical, 'top': hits[:6]}
json.dump({'built_from': os.path.abspath(REPO), 'points': out}, open(os.path.join(HERE, 'config', 'coverage.json'), 'w'), indent=1, ensure_ascii=False)
for k, v in out.items(): print('%-28s %-9s naming=%-3d topic=%-3d %s' % (k, v['level'], v['places_naming_it'], v['places_on_topic'], '; '.join(h['id'] for h in v['top'][:3])))
