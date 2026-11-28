#!/usr/bin/env python3
"""Every Rothschild branch, checked (27 Nov 2026): adds to the Road to 1948 network map the documented gifts found
beyond Edmond's (Vienna to the Keren Hayesod, 1926; Robert, Edouard and Edmond to the Paris relief fund, 1929),
Edmond's 1918 hospital gift to Hadassah, and the family's gifts after 1948 (James, 1954; Dorothy, the Supreme Court).
Writes both the page and the saved full model (book/plan/road_map/model_full.json) so a rebuild keeps them.
Weighted money: only the Vienna gifts, which reach the movement's core through the Keren Hayesod. Idempotent.

Usage: python3 tools/patch_rothschild_branches.py [road-network.html]"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
J = lambda u, t: {'t': t, 'u': u}
JTA = 'https://www.jta.org/archive/'
NODES = [
 {'id': 'louis_vr', 'name': 'Louis von Rothschild (Vienna, 1882-1955)', 'kind': 'person', 'cluster': 'rothschild',
  'note': 'Head of the Vienna house, S M von Rothschild. Took up the Keren Hayesod\'s work in 1924; the Vienna house gave $5,000 in August 1926, its second gift to the fund, and Louis £3,000 in November 1926.'},
 {'id': 'robert_r', 'name': 'Robert de Rothschild (Paris, 1880-1946)', 'kind': 'person', 'cluster': 'rothschild',
  'note': 'Of the Paris house. Gave £5,000 to the Palestine relief fund opened in Paris after the riots of August 1929.'},
 {'id': 'relief_1929', 'name': 'Palestine Relief Fund, Paris (1929)', 'kind': 'institution', 'cluster': 'finance',
  'note': 'Opened in Paris after the riots of August 1929; £15,000 subscribed at its opening, £13,000 of it from three Rothschilds.'},
 {'id': 'roth_gift_1954', 'name': 'James de Rothschild\'s gift of 410,000 pounds (1954)', 'kind': 'event', 'cluster': 'after 1948 · the patron', 'era': 'after', 'year': 1954,
  'note': 'Given in April 1954 to mark the reburial of Edmond and Adelheid at Ramat HaNadiv: 100,000 to the agricultural research institute at Rehovot, 100,000 to the Hebrew University, 60,000 to the Technion, 50,000 to the Rothschild Hospital in Haifa, and the rest to religious and smaller institutions and scholarships.'},
 {'id': 'supreme_court_bldg', 'name': 'Supreme Court building, Jerusalem (1992)', 'kind': 'place', 'cluster': 'after 1948 · the patron', 'era': 'after', 'year': 1992,
  'note': 'Given by Dorothy de Rothschild, who chaired Yad Hanadiv, the family\'s charities in Israel.'},
]
EDGES = [
 ('louis_vr', 'keren_hayesod', 'funding', 'Aug 1926: the Vienna house gave $5,000, its second gift to the Keren Hayesod, for an agricultural experiment station at Tel Aviv; Nov 1926: Louis gave £3,000 for the economic crisis in Palestine.', [J(JTA + 'vienna-rothschilds-give-5000-for-keren-hayesod', 'JTA, 24 Aug 1926'), J(JTA + 'louis-rothschild-makes-contribution-to-keren-hayesod', 'JTA, 22 Nov 1926')]),
 ('louis_vr', 'sm_rothschild', 'leadership', 'Head of the Vienna house, S M von Rothschild.', [J('https://family.rothschildarchive.org/people/97-louis-nathaniel-von-rothschild-1882-1955', 'The Rothschild Archive, Louis Nathaniel von Rothschild')]),
 ('robert_r', 'relief_1929', 'funding', 'Sep 1929: £5,000 to the Palestine relief fund opened in Paris after the August riots.', [J(JTA + 'french-palestine-relief-fund-nets-15000-pounds', 'JTA, 6 Sep 1929')]),
 ('edouard_r', 'relief_1929', 'funding', 'Sep 1929: £3,000 to the Palestine relief fund opened in Paris.', [J(JTA + 'french-palestine-relief-fund-nets-15000-pounds', 'JTA, 6 Sep 1929')]),
 ('edmond_r', 'relief_1929', 'funding', 'Sep 1929: £5,000 to the Palestine relief fund opened in Paris.', [J(JTA + 'french-palestine-relief-fund-nets-15000-pounds', 'JTA, 6 Sep 1929')]),
 ('edmond_r', 'hadassah', 'funding', '1918: gave the land and building of the Rothschild hospital in Jerusalem to Hadassah (sold in 1935 for about $200,000).', [J(JTA + 'old-hospital-site-sold-for-200000', 'JTA, 18 Mar 1935')]),
 ('james_armand', 'roth_gift_1954', 'funding', 'Apr 1954: 410,000 pounds to Israeli institutions, marking his parents\' reburial.', [J(JTA + 'baron-rothschild-gives-410000-pounds-to-israel-institutions', 'JTA, 15 Apr 1954')]),
 ('roth_gift_1954', 'hebrew_univ', 'funding', '100,000 pounds of the 1954 gift.', [J(JTA + 'baron-rothschild-gives-410000-pounds-to-israel-institutions', 'JTA, 15 Apr 1954')]),
 ('roth_gift_1954', 'technion', 'funding', '60,000 pounds of the 1954 gift.', [J(JTA + 'baron-rothschild-gives-410000-pounds-to-israel-institutions', 'JTA, 15 Apr 1954')]),
 ('dorothy', 'supreme_court_bldg', 'funding', 'Dorothy de Rothschild gave the building for Israel\'s Supreme Court.', [J('https://en.wikipedia.org/wiki/Dorothy_de_Rothschild', 'Wikipedia, Dorothy de Rothschild')]),
]
# weighted money (1948 dollars, millions): $5,000 and £3,000 x 4.86 in 1926 (CPI 17.7 -> 24.1)
MONEY = [('louis_vr', 'keren_hayesod', round((5000 + 3000 * 4.86) * 24.1 / 17.7 / 1e6, 4), 1926,
          'Vienna Rothschilds: $5,000 (Aug 1926) and £3,000 (Nov 1926) to the Keren Hayesod')]
GROUP_ADD = ['louis_vr', 'robert_r']

def apply(D):
    ids = {n['id'] for n in D['nodes']}
    for n in NODES:
        if n['id'] not in ids: D['nodes'].append(dict(n))
    have = {(e['f'], e['t'], e['type']) for e in D['edges']}
    for f, t, ty, lab, refs in EDGES:
        if (f, t, ty) in have: continue
        e = {'n': 1, 'sec': '', 'f': f, 't': t, 'type': ty, 'status': 'verified', 'src': '', 'label': lab, 'refs': refs}
        if any(x['id'] in (f, t) and x.get('era') == 'after' for x in NODES): e['era'] = 'after'
        D['edges'].append(e)
    V = D['viab']
    for f, t, w, y, desc in MONEY:
        if not any(e[0] == f and e[1] == t and e[2] == 0 for e in V['edges']):
            V['edges'].append([f, t, 0, 1.0, w]); V['eyear'].append([y, y])
            V['amounts'][f + '>' + t] = [w, desc]; V['cap0'][0] = round(V['cap0'][0] + w, 4)
    g = V['groups'].setdefault('Rothschild family and houses', [])
    for x in GROUP_ADD:
        if x not in g: g.append(x)
    # after-1948 nodes join the downstream layer's list
    if 'follow' in D:
        for n in NODES:
            if n.get('era') == 'after' and n['id'] not in D['follow']['after']: D['follow']['after'].append(n['id'])
    D['rothschild_branches'] = True

s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if not D.get('rothschild_branches'):
    apply(D); open(P, 'w', encoding='utf-8').write(s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]); print('page updated')
else: print('page already has the branches')
S = json.load(open(SNAP, encoding='utf-8'))
if not S.get('rothschild_branches'):
    apply(S); json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False); print('saved model updated')
