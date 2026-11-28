#!/usr/bin/env python3
"""Refresh the figures in the Tests table (book/part1/rd7/rd7_tests.html) from a live run of the map
(tools/stress/tests_live.json, written by tools/stress/tests_live.js), re-sort the rows by the on-time
figure and update the count in the opening paragraph. Rows are matched to tests by their question text
('What if ...?'). Rows that match nothing are kept as they are and reported.
Usage: python3 tools/refresh_tests_table.py tools/stress/tests_live.json"""
import json, re, sys, html
J = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'tools/stress/tests_live.json'))
P = 'book/part1/rd7/rd7_tests.html'
s = open(P, encoding='utf-8').read()
def key(q):
    q = re.sub(r'<small>.*?</small>', '', q)
    q = html.unescape(re.sub(r'<[^>]+>', '', q)).strip()
    q = re.sub(r'^What if\s+', '', q).rstrip('?').strip()
    return re.sub(r'[^a-z0-9]+', ' ', q.lower()).strip()
live, byid = {}, {}
for r in J['rows'] + J['disp']:
    live[key(r['q'])] = r; byid.setdefault(r['id'], r)
# table rows whose wording differs from the map's question
ALIAS = [('The Rothschilds had gone, and everyone with a documented tie', 'roth_web'),
 ('The Rothschilds had gone, with every institution tied to them', 'roth_web_inst'),
 ('The Rothschilds had gone, and the Balfour Declaration could not', 'roth_decl'),
 ('The Rothschilds, Herzl and the whole network before 1897', 'roth_herzl_pre'),
 ('The Rothschilds and the whole network before 1897', 'roth_pre'),
 ('The Rothschilds had gone, and everything cut off', 'roth_cascade'),
 ('The whole network before 1897 had been absent', 'pre_all'),
 ("The Holocaust survivors' case had never been made", 'legit_holocaust'),
 ('The Yishuv had built none of its own institutions', 'yishuv_inst'),
 ('American public and Christian support had been absent', 'legit_christian_us'),
 ('There had been no pogroms of 1881', 'pre_trigger'),
 ('The Passfield limits had stood', 'policy_macdonald'),
 ('The Transfer Agreement of 1933 had never been made', 'haavara_out'),
 ('The eight nodes added to the map from outside sources', 'pre_new_all')]
row_re = re.compile(r'<tr><th>(.*?)</th><td>(\d+)%</td><td>(\d+)%</td><td>(\d+)</td><td>(.*?)</td></tr>')
tb0 = s.index('<tbody>'); tb1 = s.index('</tbody>', tb0)
body = s[tb0 + 7:tb1]
rows = row_re.findall(body)
out, miss, changed = [], [], []
for th, on, ev, yl, verdict in rows:
    r = live.get(key(th))
    if r is None:
        for a, i in ALIAS:
            if html.unescape(th).startswith(a): r = byid[i]; break
    if r is None:
        miss.append(th); out.append((int(on), (th, on, ev, yl, verdict))); continue
    n_on, n_ev, n_yl = round(r['on']), round(r['ever']), round(r['lost'] or 0)
    n_v = r['verdict']
    if (str(n_on), str(n_ev), str(n_yl), n_v) != (on, ev, yl, verdict):
        changed.append(f'{th[:70]}: {on}/{ev}/{yl} -> {n_on}/{n_ev}/{n_yl}')
    out.append((r['on'], (th, str(n_on), str(n_ev), str(n_yl), n_v)))
out.sort(key=lambda x: x[0])
nb = '\n' + '\n'.join(f'<tr><th>{a}</th><td>{b}%</td><td>{c}%</td><td>{d}</td><td>{e}</td></tr>' for _, (a, b, c, d, e) in out) + '\n'
s = s[:tb0 + 7] + nb + s[tb1:]
nt, nd = len(J['rows']), len(J['disp'])
NUM = {7:'seven',8:'eight',9:'nine',10:'ten',11:'eleven',12:'twelve'}
s = re.sub(r'There are now \d+ of them, together with [a-z0-9]+ that take', f'There are now {nt} of them, together with {NUM.get(nd, nd)} that take', s, count=1)
open(P, 'w', encoding='utf-8').write(s)
print('rows', len(rows), 'changed', len(changed), 'unmatched', len(miss))
for c in changed: print('  ', c)
for m in miss: print('  UNMATCHED', m[:90])
