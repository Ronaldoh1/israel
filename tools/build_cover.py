#!/usr/bin/env python3
"""Build road-1948.html, the cover page of the Road to 1948 network map.
Reads tools/cover/road-1948.template.html and the live test figures in tools/stress/cover_data.json
(written by tools/stress/cover_data.js from a live run of road-network.html), and the tie counts from
road-network.html itself, so the page never states a figure the map does not produce.
Usage: python3 tools/build_cover.py"""
import json, math, re
ROOT = __file__.rsplit('/tools/', 1)[0]
T = open(ROOT + '/tools/cover/road-1948.template.html', encoding='utf-8').read()
C = json.load(open(ROOT + '/tools/stress/cover_data.json'))
s = open(ROOT + '/road-network.html', encoding='utf-8').read()
d = json.JSONDecoder().raw_decode(s[re.search(r'const DATA\s*=\s*', s).end():])[0]
VB = d['viab']
st = {}
for e in d['edges']: st[e['status']] = st.get(e['status'], 0) + 1
srcs = {e.get('src') for e in d['edges'] if e['status'] in ('verified', 'reported') and e.get('src')}
k = -math.log(1 - VB['cal'])
NORM = VB.get('norm') or [1] * 9
EXP = VB['exp']
ORDER = [('none', 'Nothing: the full record'), ('roth', 'The Rothschild family'), ('us', 'The United States'),
         ('britain', "Britain's backing"), ('balfour', 'The Balfour Declaration'), ('un', 'The UN vote'),
         ('soviet', "The Soviet bloc's arms and votes"), ('czech', 'The Czechoslovak arms'),
         ('people_mandate', "The Mandate's immigration certificates"),
         ('legit_holocaust', "The Holocaust survivors' case"), ('herzl', 'Theodor Herzl'),
         ('truman', 'Truman'), ('movement', 'Zionism as an organized movement')]
span = VB['y1'] - VB['y0']
base = C['base']['on']
tests = []
for tid, label in ORDER:
    if tid == 'none':
        r = {'q': 'What if nothing were removed?', 'pc': C['base']['pc'], 'on': base, 'ever': base, 'lost': 0,
             'verdict': 'Happens on time, in 1948', 'by1958': base, 'by1978': base, 'retry': None}
    else:
        r = C[tid]
    pc = r['pc']
    share = [min(1, -math.log(max(1e-9, 1 - p)) / k) if p < VB['cal'] else 1 for p in pc]
    needs = 1.0
    for i, p in enumerate(pc): needs *= (p / NORM[i]) ** EXP[i]
    needs /= VB['cal'] ** 7
    kept = max(0.0, 1 - (r['lost'] or 0) / span)
    tests.append({'id': tid, 'label': label, 'q': r['q'], 'on': round(r['on'], 2), 'ever': round(r['ever'], 2),
                  'b58': round(r['by1958'], 2), 'b78': round(r['by1978'], 2), 'lost': round(r['lost'] or 0, 1),
                  'verdict': r['verdict'], 'retry': r['retry'], 'needs': round(100 * needs, 1),
                  'kept': round(100 * kept, 1), 'share': [round(100 * x) for x in share]})
import glob
R = json.load(open(sorted(glob.glob(ROOT + '/tools/stress/stress_ranges_2*.json'))[-1]))
RANGE = [('base', 'Full record'), ('herzl', 'Without Herzl'), ('un', 'Without the UN vote'),
         ('balfour', 'Without the Balfour Declaration'), ('britain', "Without Britain's backing"),
         ('roth', 'Without the Rothschild family'), ('us', 'Without the United States'),
         ('d_all', 'Every often-denied part at once')]
ranges = [{'label': l, 'v': min(100, R[i][0]), 'lo': min(100, R[i][1]), 'hi': min(100, R[i][2])} for i, l in RANGE]
LOSO = json.load(open(sorted(glob.glob(ROOT + '/tools/stress/loso_2*.json'))[-1]))
fmt = lambda n: f'{n:,}'
sub = {
    '%%VERRAW%%': str(st.get('verified', 0)), '%%REPRAW%%': str(st.get('reported', 0)), '%%COMRAW%%': str(st.get('co-mention', 0)),
    '%%NODES%%': fmt(len(d['nodes'])), '%%VER%%': fmt(st.get('verified', 0)), '%%REP%%': fmt(st.get('reported', 0)),
    '%%COM%%': fmt(st.get('co-mention', 0)), '%%TOV%%': fmt(st.get('to-verify', 0)),
    '%%TIES%%': fmt(st.get('verified', 0) + st.get('reported', 0)), '%%SRC%%': fmt(len(srcs)),
    '%%BASE%%': f'{base:.1f}', '%%NSRC%%': str(LOSO['nsrc']), '%%BUILT%%': __import__('datetime').date.today().strftime('%-d %B %Y'),
    '%%TESTS%%': json.dumps(tests, ensure_ascii=False), '%%RANGES%%': json.dumps(ranges, ensure_ascii=False),
}
for a, b in sub.items(): T = T.replace(a, b)
assert '%%' not in T, re.findall(r'%%\w+%%', T)
open(ROOT + '/road-1948.html', 'w', encoding='utf-8').write(T)
print('road-1948.html written:', len(T), 'bytes;', len(tests), 'tests;', sub['%%TIES%%'], 'weighted-eligible ties')
