"""The global layer after 1948: how Israel and pro-Israel networks have worked to hold allies and votes abroad, and what has
protected Israel's standing at the UN. Writes global_layer.json and book/research/road_global_layer.json. Every node here is
post-1948 and is kept out of the 1948 removal model (viability.POST_EXTRA)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
S = {
 'g_jvl_africa': ('Jewish Virtual Library: The Evolution of Israel\'s Africa Policy', 'https://www.jewishvirtuallibrary.org/the-evolution-of-israel-rsquo-s-africa-policy'),
 'g_wp_elnet': ('Wikipedia: ELNET', 'https://en.wikipedia.org/wiki/ELNET'),
 'g_shomrim': ('Shomrim, 31 Oct 2024: "A Failure by Every Conceivable Parameter"', 'https://www.shomrim.news/eng/advocacy-failure'),
 'g_iaf_africa': ('Yahoo News: Israel Allies Foundation launches six new caucuses in Africa', 'https://www.yahoo.com/news/israel-allies-foundation-launches-six-130225706.html'),
 'g_aj_veto': ('Al Jazeera, 26 Oct 2023: How the US has used its veto power at the UN in support of Israel', 'https://www.aljazeera.com/news/2023/10/26/how-the-us-has-used-its-veto-power-at-the-un-in-support-of-israel'),
 'g_jta82': ('JTA via COJS, 5 Feb 1982: U.S. threatens to withdraw from UN if Israel is suspended or expelled', 'https://cojs.org/U.S-_Threatens_to_Withdraw_from_UN_if_Israel_Is_Suspended_or_Expelled-_JTA-_Feb-_5-_1982/'),
 'g_csm82': ('Christian Science Monitor, 26 Apr 1982: Syria tries to oust Israel from UN', 'https://csmonitor.com/1982/0426/042615.html'),
 'g_wp_3379': ('Wikipedia: UN General Assembly Resolution 3379', 'https://en.wikipedia.org/wiki/United_Nations_General_Assembly_Resolution_3379'),
}
# 1975 votes on Resolution 3379 by the countries already in the map (voting against it was the pro-Israel position)
FOR75 = ['afghanistan', 'brazil', 'bulgaria', 'byelorussia', 'china', 'cuba', 'czechoslovakia', 'egypt', 'hungary', 'india', 'iran', 'iraq', 'lebanon',
         'mexico', 'pakistan', 'poland48', 'saudi', 'syria', 'turkey', 'ukraine_ssr', 'ussr', 'yemen', 'yugoslavia']
AGAINST75 = ['australia', 'belgium', 'canada', 'costa_rica', 'denmark', 'dominican', 'el_salvador', 'finland', 'france_gov', 'haiti', 'honduras', 'iceland',
             'liberia', 'luxembourg', 'netherlands', 'new_zealand', 'nicaragua', 'norway', 'panama', 'sweden', 'uk', 'us_gov', 'uruguay']
ABST75 = ['argentina', 'bolivia', 'chile', 'colombia', 'ecuador', 'ethiopia', 'greece', 'guatemala', 'paraguay', 'peru', 'philippines', 'venezuela']
V, R = 'verified', 'reported'
E = []
def add(f, t, ty, st, src, lab): E.append((f, t, ty, st, src, lab))
add('israel_gov', 'africa_aid', 'funding', V, 'g_jvl_africa', 'From the late 1950s Israel sent aid to newly independent African states. Ben-Gurion: "Our aid to the new countries... is not a matter of philanthropy."')
add('africa_aid', 'unga', 'influence', V, 'g_jvl_africa', 'Israel had one UN vote against 18 Arab members, so "it was important for Israel to try to win as many African votes as possible."')
add('africa_aid', 'africa_break73', 'association', V, 'g_jvl_africa', 'After the October 1973 war "all of Israel\'s friends on the continent" cut ties; Ethiopia did so formally on 23 Oct 1973.')
add('ethiopia', 'africa_break73', 'association', V, 'g_jvl_africa', '23 Oct 1973: Ethiopia formally broke relations with Israel.')
add('elnet', 'israel_gov', 'association', V, 'g_wp_elnet', 'Registered 22 Oct 2007; in Belgium, France, Germany, Poland, the UK, Italy and Israel; describes itself as "the most influential pro-Israel advocacy organisation in Europe"; takes European lawmakers and officials to Israel.')
add('elnet', 'parliament', 'influence', R, 'g_wp_elnet', 'Declassified UK (2024): pro-Israel lobbyists including ELNET donated to 13 of the 25 members of Labour\'s cabinet; The Intercept (2025): US donors fund its American arm, FELNET.')
add('iaf', 'israel_gov', 'association', R, 'g_iaf_africa', 'Builds pro-Israel caucuses of lawmakers in parliaments abroad; it launched six new caucuses in Africa.')
add('israel_gov', 'concert', 'funding', V, 'g_shomrim', '2018: 128 million shekels approved for Kela Shlomo (it raised about a fifth of the matching funds); 2022: 25 million shekels a year as "Concert"; later "Voices of Israel", whose contract the Diaspora Ministry ended in 2024. Its director general: "this activity has failed by every conceivable parameter."')
add('us_gov', 'us_vetoes', 'official act', V, 'g_aj_veto', 'By 2023 the US had vetoed Israel-related Security Council resolutions 46 times, and cast 34 of the 36 vetoes on Israel-Palestine drafts since 1945 (Al Jazeera count).')
add('us_vetoes', 'unsc', 'association', V, 'g_aj_veto', 'Expelling or suspending a UN member needs a Security Council recommendation, where the US holds a veto.')
add('syria', 'syria82', 'proposal', V, 'g_csm82', 'April 1982: Syria moved that the General Assembly "review Israel\'s status in the United Nations", opening a later vote on suspension or expulsion; diplomats saw no majority for expulsion.')
add('us_gov', 'syria82', 'opposition', V, 'g_jta82', 'Feb 1982: the State Department warned that suspending or expelling Israel "would have serious consequences for continued U.S. participation in and support for the United Nations."')
add('unga', 'res3379', 'official act', V, 'g_wp_3379', '10 Nov 1975: "Zionism is a form of racism" adopted 72 to 35 with 32 abstaining.')
add('unga', 'res4686', 'official act', V, 'g_wp_3379', '16 Dec 1991: Resolution 46/86 revoked 3379, 111 to 25 with 13 abstaining.')
add('res4686', 'res3379', 'opposition', V, 'g_wp_3379', 'Revoked Resolution 3379 in 1991.')
for i in FOR75: add(i, 'res3379', 'vote for', V, 'g_wp_3379', 'Voted for Resolution 3379, 10 Nov 1975.')
for i in AGAINST75: add(i, 'res3379', 'vote against', V, 'g_wp_3379', 'Voted against Resolution 3379, 10 Nov 1975.')
for i in ABST75: add(i, 'res3379', 'abstention', V, 'g_wp_3379', 'Abstained on Resolution 3379, 10 Nov 1975.')
NOTES = {
 'us_vetoes': 'The US veto in the Security Council: 46 vetoes of Israel-related resolutions by 2023. Because expulsion or suspension needs a Council recommendation, the veto is what protects Israel\'s UN membership.',
 'res3379': 'Of the 33 states that voted for partition in 1947, 19 voted against this resolution in 1975 (sided with Israel), 7 abstained and 6 voted for it (the Soviet bloc and Brazil).',
}
NEW = '''africa_aid|Israeli aid to Africa (from the late 1950s)|event|israel state|aid to Africa;African aid program
africa_break73|African states break with Israel (1973)|event|international|broke relations with Israel
elnet|ELNET (European Leadership Network)|institution|europe|ELNET;European Leadership Network
iaf|Israel Allies Foundation|institution|christian zionism|Israel Allies Foundation;Israel Allies Caucus
concert|Kela Shlomo / Concert / Voices of Israel|institution|israel state|Kela Shlomo;Voices of Israel;Concert - Together for Israel
us_vetoes|US vetoes in the Security Council on Israel|event|us government|vetoed
syria82|Move to review Israel's UN status (1982)|event|international|review Israel's status
res3379|UN Resolution 3379 (1975)|document|international|Resolution 3379;Zionism is a form of racism
res4686|UN Resolution 46/86 (1991)|document|international|Resolution 46/86
'''
POST = ['africa_aid', 'africa_break73', 'elnet', 'iaf', 'concert', 'us_vetoes', 'syria82', 'res3379', 'res4686']

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    json.dump({'_note': 'Global layer after 1948 (Nov 2026). Built by global_layer.py; do not edit by hand.', 'node_notes': NOTES, 'post': POST,
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'global_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_global_layer', 'stage': 'cw6', 'topic': 'Global layer after 1948: aid to Africa for UN votes, ELNET, the Israel Allies Foundation, the state campaigns (Kela Shlomo, Concert, Voices of Israel), US vetoes, the 1982 move against Israel\'s UN status, Resolution 3379 and its 1975 votes (Nov 2026)',
             'claims': [lab for *_, lab in E], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_global_layer', 'verified': '2026-11-05', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_global_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__':
    if '--registry' in sys.argv:
        s = open(os.path.join(HERE, 'registry.py')).read()
        if 'Global layer after 1948' not in s:
            i = s.rindex('"""'); s = s[:i] + '# ---------- Global layer after 1948 (added Nov 2026) ----------\n' + NEW + s[i:]
            open(os.path.join(HERE, 'registry.py'), 'w').write(s); print('registry updated')
    else: main()
