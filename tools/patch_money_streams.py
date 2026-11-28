#!/usr/bin/env python3
"""The money streams the map was missing (27 Nov 2026): private and immigrant capital, the Keren Hayesod after 1932,
the Jewish National Fund's own collections, the Jewish Agency's wartime budget and Hadassah's spending. Labels every money
tie on the map by kind (donation, fund drive, investment, capital transfer, credit, political gift, bequest, dues).
Writes both the page and the saved full model (book/plan/road_map/model_full.json) so a rebuild keeps them. Idempotent.

Sums are converted to 1948 dollars from the years they were given (CPI 1948 = 24.1), the map's unit.
  private capital 1919-39: about P£110M of Jewish capital came in between the wars (Cliff 1946); 75% of it was private
      (Metzer 1998, p. 106) = P£82.5M; less the Haavara transfer already on the map (105M RM, about $35M = P£7.1M)
      = P£75.4M x $4.90 = $369.5M; about 60% came in 1932-39 (CPI 13.7) and 40% in 1919-31 (CPI 17.5)
      -> x 24.1 x (0.6/13.7 + 0.4/17.5) = $594M
  private capital 1940-44: P£38M of Jewish capital came in (Survey of Palestine II, p. 556); about half private
      (Metzer p. 106) = P£19M x $4.03, CPI 16.0 -> $115M
  Jewish Agency, wartime: P£17,827,146 spent 1939-45 (JTA 1951) x $4.03, CPI 16.0 -> $108M (funded by the Keren
      Hayesod and the United Palestine Appeal in those years, which are therefore not counted again)
  Keren Hayesod: P£9,604,000 net income in its first 20 years (JTA 1940), less the P£4,714,440 of 1921-32 already on
      the map and the last year, P£623,000 (inside the Agency's wartime figure) = P£4,267,000 for 1933-39 x $4.90,
      CPI 13.6 -> $37.1M, added to the 1921-32 tie
  JNF: American Jews gave P£7,863,200 to September 1946, 51.8% of the fund's net direct income (Lehn 1974, citing the
      JNF Report 1946) -> P£15.18M; of it $20M to 1935 (JTA 1936; CPI 15.5 -> $31.1M) and P£11.07M after x $4.10,
      CPI 16.0 -> $68.4M; $99.5M. The Blue Box and JNF-to-Hankin placeholders fall inside it and go to zero.
  Hadassah: over $13M spent on health work, June 1918 to October 1942 (JTA 1942), CPI 16.2 -> $19.3M

Usage: python3 tools/patch_money_streams.py [road-network.html]"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
J = lambda u, t: {'t': t, 'u': u}
JTA = 'https://www.jta.org/archive/'
R_CLIFF = J('https://www.marxists.org/archive/cliff/works/1946/probme/chap10.html', 'Tony Cliff, The Problem of the Middle East (1946), ch. 10')
R_METZER = J('https://israeled.org/wp-content/uploads/2022/10/Metzer-Jacob-The-Divided-Economy-of-Mandatory-Palestine-1998-essential.pdf', 'Jacob Metzer, The Divided Economy of Mandatory Palestine (Cambridge, 1998), p. 106')
R_SURVEY = J('https://www.bjpa.org/content/upload/bjpa/a_su/A%20SURVEY%20OF%20PALESTINE%20DEC%201945-JAN%201946%20VOL%20II.pdf', 'A Survey of Palestine (1946), vol. II, p. 556')
R_MERIP = J('https://www.merip.org/1986/09/private-capital-in-israel/', 'MERIP, Private Capital in Israel (1986)')
R_ZE = J(JTA + '49000000-invested-by-jews-in-palestine-in-last-eight-years-zionist-executive-states-in-memorandum', 'JTA, 8 Jun 1926')
R_JA = J(JTA + 'striking-increase-in-jewish-agency-activities-reviewed-in-report-to-zionist-congress', 'JTA, 6 Aug 1951')
R_UPA45 = J(JTA + 'united-palestine-appeal-agencies-spent-63297000-during-war-years-report-says', 'JTA, 14 May 1945')
R_KH40 = J(JTA + 'keren-hayesods-income-50000000-in-20-years', 'JTA, 6 Sep 1940')
R_KH37 = J(JTA + '17-year-income-of-keren-hayesod-put-at-30000000', 'JTA, 19 May 1937')
R_KH39 = J(JTA + 'keren-hayesod-collected-l623000-in-past-year', 'JTA, Keren Hayesod collected £623,000 in past year')
R_LEHN = J('https://www.palquest.org/sites/default/files/The_Jewish_National_Fund-Walter_Lahen.pdf', 'Walter Lehn, The Jewish National Fund, Journal of Palestine Studies (1974), p. 87')
R_JNF36 = J('https://jta.org/archive/47000000-spent-in-palestine', 'JTA, 16 Feb 1936')
R_JNF41 = J(JTA + 'jnf-received-2500000-during-1941-for-land-purchases-in-palestine', 'JTA, 29 Dec 1941')
R_HAD = J(JTA + '13000000-spent-by-hadassah-for-health-work-in-palestine-between-two-wars', 'JTA, 25 Sep 1942')

NODES = [
 {'id': 'jewish_economy', 'name': 'Jewish economy of Mandate Palestine', 'kind': 'institution', 'cluster': 'finance',
  'note': 'The farms, groves, factories, homes and businesses of the Jewish community under the Mandate. Its growth, about 13% a year from 1922 to 1947, was carried by immigration and imported capital.'},
 {'id': 'private_capital_interwar', 'name': 'Private and immigrant capital (1919-1939)', 'kind': 'institution', 'cluster': 'finance',
  'note': 'The money Jewish immigrants brought with them and private investors sent: citrus groves, building, industry and trade. About three-quarters of all Jewish capital that came in between the wars, the largest single stream of money into the Jewish community. Most of it arrived in 1932-36, with the immigration from Poland and Germany.'},
 {'id': 'private_capital_war', 'name': 'Private capital (1940-1944)', 'kind': 'institution', 'cluster': 'finance',
  'note': 'Private money that kept coming in during the Second World War, about half of the P£38 million of Jewish capital the Mandate government counted for 1940-44.'},
 {'id': 'jnf_collections', 'name': 'JNF collections worldwide (1901-1946)', 'kind': 'institution', 'cluster': 'finance',
  'note': 'The Jewish National Fund\'s own income from donations, the Blue Box tins, Golden Book entries and tree certificates, which bought the land it held: 936,000 dunams by May 1948. About P£15 million to September 1946, half of it from American Jews.'},
 {'id': 'wartime_appeals', 'name': 'Wartime fund drives for the Jewish Agency (1939-1945)', 'kind': 'institution', 'cluster': 'finance',
  'note': 'The Keren Hayesod and the United Palestine Appeal\'s money in the war years, spent by the Jewish Agency on settlement, land, immigration, enlistment and security: P£17.8 million from 1939 to 1945.'},
 {'id': 'hadassah_members', 'name': 'Hadassah members and chapters (United States)', 'kind': 'institution', 'cluster': 'finance',
  'note': 'The women\'s Zionist organisation of America, whose dues and campaigns paid for the hospitals, clinics and nursing in Palestine run by the Hadassah Medical Organization.'},
]
ACTORS = {'jewish_economy': [1919, 1948, 'm'], 'private_capital_interwar': [1919, 1939, 'm'], 'private_capital_war': [1940, 1944, 'm'],
          'jnf_collections': [1901, 1946, 'm'], 'wartime_appeals': [1939, 1945, 'm'], 'hadassah_members': [1918, 1942, 'm']}
EDGES = [  # display ties: f, t, type, label, refs
 ('private_capital_interwar', 'jewish_economy', 'funding', 'About P£110 million of Jewish capital came in between the wars, three-quarters of it private; the map counts about P£75 million of private and immigrant capital (leaving out the Haavara transfer, counted on its own). An estimate from stated totals.', [R_CLIFF, R_METZER, R_MERIP, R_ZE]),
 ('private_capital_war', 'jewish_economy', 'funding', '1940-44: P£38 million of Jewish capital came in, about half of it private: about P£19 million. An estimate from stated totals.', [R_SURVEY, R_METZER]),
 ('jewish_economy', 'yishuv', 'membership', 'The economy the Yishuv\'s institutions governed and taxed.', [R_METZER]),
 ('jewish_economy', 'apc_bank', 'funding', 'Imported capital raised the deposits of the Jewish banks, chief among them the Anglo-Palestine Bank.', [R_SURVEY]),
 ('jnf_collections', 'jnf', 'funding', 'About P£15.2 million of net direct income to September 1946 (American Jews gave P£7,863,200 of it, 51.8%); $20 million raised from 1901 to 1935; P£620,000 in 1941 alone.', [R_LEHN, R_JNF36, R_JNF41]),
 ('wartime_appeals', 'jewish_agency', 'funding', 'P£17,827,146 spent by the Jewish Agency in the war years; the UPA\'s agencies reported $63.3 million spent from the outbreak of war to March 1945.', [R_JA, R_UPA45]),
 ('hadassah_members', 'hadassah', 'funding', 'Over $13 million spent on health work in Palestine, June 1918 to October 1942.', [R_HAD]),
]
MONEY = [  # f, t, weight (1948 $M), years, description, conf
 ('private_capital_interwar', 'jewish_economy', 594.0, [1919, 1939], 'Private and immigrant capital, 1919-39: about P£75 million (an estimate: three-quarters of about P£110 million of Jewish capital, less the Haavara transfer)', 0.6),
 ('private_capital_war', 'jewish_economy', 115.3, [1940, 1944], 'Private capital, 1940-44: about P£19 million (an estimate: about half of P£38 million of Jewish capital)', 0.6),
 ('jewish_economy', 'yishuv', 0.0, [1919, 1948], '', 0.6),
 ('jewish_economy', 'apc_bank', 0.0, [1919, 1948], '', 0.6),
 ('jnf_collections', 'jnf', 99.5, [1901, 1946], 'Jewish National Fund: about P£15.2 million of net direct income, 1901 to September 1946', 1.0),
 ('wartime_appeals', 'jewish_agency', 108.2, [1939, 1945], 'Jewish Agency wartime spending, 1939-45: P£17,827,146, from the Keren Hayesod and the United Palestine Appeal', 1.0),
 ('hadassah_members', 'hadassah', 19.3, [1918, 1942], 'Hadassah: over $13 million spent on health work in Palestine, June 1918 to October 1942', 1.0),
]
KH_NEW = (68.25, [1921, 1939], 'Keren Hayesod: £4,714,440 income 1921-32 (half from the United States) and about £4,267,000 more to 1939; P£9,604,000 in its first 20 years')
ZEROED = {'blue_box>jnf': 'Blue Box collections: inside the Jewish National Fund\'s income, counted there',
          'jnf>hankin': 'The JNF\'s land purchases through Hankin: paid from the fund\'s income, counted there'}
KIND = {  # every money tie on the map, by kind
 'edmond_r': 'donation and investment', 'james_armand': 'donation and investment', 'upa': 'fund drive', 'uja': 'fund drive', 'meir': 'fund drive',
 'haavara': 'capital transfer', 'keren_hayesod': 'fund drive', 'nicaragua': 'credit', 'jnf': 'fund drive', 'jewish_agency': 'investment',
 'sonneborn_inst': 'fund drive', 'zoa': 'fund drive', 'ajrc': 'fund drive', 'schiff': 'donation', 'herzl': 'investment', 'shekel': 'dues',
 'kofer': 'levy', 'jdc': 'donation', 'sieff': 'donation', 'marks_s': 'donation', 'state_dept': 'government aid', 'warburg_f': 'investment',
 'mond': 'investment', 'jct': 'investment', 'americans_haganah': 'fund drive', 'sacher': 'donation', 'elias_sursock': 'land sale',
 'nagib_albert_s': 'land sale', 'blue_box': 'donation', 'hecht': 'fund drive', 'uk_arms_appeal': 'fund drive', 'straus_n': 'donation',
 'wissotzky': 'bequest', 'kaufmann_e': 'political gift', 'feinberg': 'political gift', 'mickey_cohen': 'fund drive', 'siegel': 'donation',
 'louis_vr': 'donation', 'private_capital_interwar': 'private investment', 'private_capital_war': 'private investment',
 'jnf_collections': 'fund drive', 'wartime_appeals': 'fund drive', 'hadassah_members': 'fund drive', 'jewish_economy': 'private investment'}
KIND_EDGE = {'mond>jabotinsky': 'donation', 'jdc>pec_econ': 'investment', 'jct>pec': 'investment'}

def apply(D):
    ids = {n['id'] for n in D['nodes']}
    for n in NODES:
        if n['id'] not in ids: D['nodes'].append(dict(n))
    have = {(e['f'], e['t'], e['type']) for e in D['edges']}
    for f, t, ty, lab, refs in EDGES:
        if (f, t, ty) not in have:
            D['edges'].append({'n': 1, 'sec': '', 'f': f, 't': t, 'type': ty, 'status': 'verified', 'src': '', 'label': lab, 'refs': refs})
    V = D['viab']
    for k, a in ACTORS.items(): V['actors'].setdefault(k, a)
    for f, t, w, y, desc, conf in MONEY:
        if not any(e[0] == f and e[1] == t and e[2] == 0 for e in V['edges']):
            V['edges'].append([f, t, 0, conf, w]); V['eyear'].append(list(y))
            if desc: V['amounts'][f + '>' + t] = [w, desc]
    for e, y in zip(V['edges'], V['eyear']):
        k = e[0] + '>' + e[1]
        if e[2] != 0: continue
        if k == 'keren_hayesod>jewish_agency':
            e[4] = KH_NEW[0]; y[:] = KH_NEW[1]; V['amounts'][k] = [KH_NEW[0], KH_NEW[2]]
        if k in ZEROED:
            e[4] = 0.0; V['amounts'][k] = [0.0, ZEROED[k]]
    V['cap0'][0] = round(sum(e[4] for e in V['edges'] if e[2] == 0), 4)
    V['mkind'] = {e[0] + '>' + e[1]: KIND_EDGE.get(e[0] + '>' + e[1], KIND.get(e[0], 'donation')) for e in V['edges'] if e[2] == 0}
    D['money_streams'] = True

s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if not D.get('money_streams'):
    apply(D); open(P, 'w', encoding='utf-8').write(s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]); print('page updated; money', D['viab']['cap0'][0])
else: print('page already has the money streams')
S = json.load(open(SNAP, encoding='utf-8'))
if not S.get('money_streams'):
    apply(S); json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False); print('saved model updated')
