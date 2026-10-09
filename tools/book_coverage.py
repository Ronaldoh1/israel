"""Coverage check for a library chapter (LIBRARY-PROTOCOL.md, section 3).
Measures how much of the research in scope (the chapter's own scenes plus every scene its manifest draws on)
made it into the written sections, and lists what is missing.
Usage: python3 tools/book_coverage.py rd2 [--list]
Set-asides: book/part1/<cid>/_coverage.json  {"set_aside": {"<unit id>": "reason"}}"""
import json, os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cid = sys.argv[1]; LIST = '--list' in sys.argv
s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
g = lambda p: json.loads(re.search(p, s, re.S).group(1))
SC = {x['id']: x for x in g(r'<script id="scenedata" type="application/json">(.*?)</script>')}
CH = g(r'window\.CHAPTERS = (\[.*?\]);\n')
EX = g(r'<script id="expanded-en" type="application/json">(.*?)</script>')
DD = g(r'<script id="deepdive-en" type="application/json">(.*?)</script>')
d = os.path.join(ROOT, 'book', 'part1', cid)
mp = os.path.join(d, '_manifest.json')
own = next(c for c in CH if c['id'] == cid)['scenes']
scope = list(own)
if os.path.exists(mp):
    for m in json.load(open(mp, encoding='utf-8'))['sections']:
        for x in [m.get('scene')] + m.get('draws', []):
            if x and x in SC and x not in scope: scope.append(x)
cov = json.load(open(os.path.join(d, '_coverage.json'), encoding='utf-8')) if os.path.exists(os.path.join(d, '_coverage.json')) else {}
aside = cov.get('set_aside', {})
text = ' '.join(open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(d, '*.html')))
plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', text))
strip = lambda t: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'\[cite:[^\]]+\]', '', t or '')))
NUM = re.compile(r'(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])')

def nums(t):
    return {n for n in NUM.findall(strip(t)) if len(n.replace(',', '')) >= 3 or ',' in n}

def present(n):
    return n in plain or n.replace(',', '') in plain.replace(',', '')

units = {'cite': {}, 'number': {}, 'deepdive': {}}
low = plain.lower()
STOP = set('should because between through without within record documented documents shows simulation entity entities scene scenes discipline version dinner table claims claimed actually exactly specific another whether people already itself rather moment others nothing points question'.split())
for sid in scope:
    x = SC[sid]; blob = json.dumps(x, ensure_ascii=False) + json.dumps(EX.get(sid, {}), ensure_ascii=False) + json.dumps(DD.get(sid, {}), ensure_ascii=False)
    for k in re.findall(r'\[cite:([A-Za-z0-9_]+)\]', blob): units['cite'].setdefault(k, sid)
    parts = [x.get('n'), x.get('tld'), x.get('rec')] + [e.get('dt') for e in x.get('ents', [])] + [v.get('dt') for v in EX.get(sid, {}).values() if isinstance(v, dict)]
    for t in parts:
        for n in nums(t): units['number'].setdefault(n, sid)
    for eid, dd in DD.get(sid, {}).items():
        for i, sec in enumerate(dd.get('sections', [])):
            body = sec.get('body') or ''
            ns = nums(body)
            for n in ns: units['number'].setdefault(n, sid)
            ks = set(re.findall(r'\[cite:([A-Za-z0-9_]+)\]', body))
            names = set(re.findall(r'\b[A-Z][a-z]+(?:\s(?:of\s|de\s|al-)?[A-Z][a-z]+)+', strip(body)))
            probes = list(ns) + [w for nm in names for w in nm.split() if len(w) > 3]
            hit1 = sum(1 for p in probes if present(p)) / len(probes) if probes else 0.0
            # content-word overlap catches sections told in paraphrase (no numbers or names to probe)
            words = {w for w in re.findall(r'[a-z]{6,}', strip(body).lower()) if w not in STOP}
            hit2 = sum(1 for w in words if w in low) / len(words) if words else 0.0
            hit = max(hit1, hit2 if len(words) >= 3 else (1.0 if not probes else 0.0))
            units['deepdive']['%s/%s/%d' % (sid, eid, i)] = (hit, sec.get('heading') or '')

def score(kind):
    tot = used = 0; miss = []
    for u, v in units[kind].items():
        uid = '%s:%s' % (kind, u)
        if uid in aside: tot += 1; used += 1; continue
        tot += 1
        ok = ('[cite:%s]' % u) in text if kind == 'cite' else present(u) if kind == 'number' else v[0] >= .6
        used += ok
        if not ok: miss.append((u, v))
    return tot, used, miss

TH = {'cite': 1.0, 'number': .95, 'deepdive': 1.0}
print('Coverage for %s: %d scenes in scope (%d own, %d drawn from other chapters); %d words written' % (cid, len(scope), len(own), len(scope) - len(own), len(plain.split())))
ok_all = True
for kind, label in (('cite', 'citations'), ('number', 'figures and dates'), ('deepdive', 'deep-dive sections')):
    tot, used, miss = score(kind); pct = used / tot if tot else 1
    ok = pct >= TH[kind] - 1e-9; ok_all &= ok
    print('  %-20s %4d / %-4d %5.1f%%  %s' % (label, used, tot, 100 * pct, 'ok' if ok else 'BELOW %d%%' % (100 * TH[kind])))
    if LIST and miss:
        for u, v in miss[:400]: print('      missing %s:%s  (%s)' % (kind, u, v if isinstance(v, str) else '%s, %.0f%% found' % (v[1], 100 * v[0])))
print('PASS' if ok_all else 'NOT DONE: write it in, move it with a reason, or set it aside in _coverage.json with a reason')
