"""The United Nations layer: the founding of the UN, UNSCOP, every vote on Resolution 181 (29 Nov 1947), the reported
pressure campaign, the recognitions of 1948 and admission in 1949. Writes un_layer.json and book/research/road_un_layer.json.
'reported' where the cited page reports the fact as a claim or allegation."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
S = {
 'u_wp_un': ('Wikipedia: United Nations', 'https://en.wikipedia.org/wiki/United_Nations'),
 'u_wp_part': ('Wikipedia: United Nations Partition Plan for Palestine', 'https://en.wikipedia.org/wiki/United_Nations_Partition_Plan_for_Palestine'),
 'u_jvl_181': ('Jewish Virtual Library: UN General Assembly Resolution 181 (vote list)', 'https://jewishvirtuallibrary.org/jsource/History/partition.html'),
 'u_wp_recog': ('Wikipedia: International recognition of Israel', 'https://en.wikipedia.org/wiki/International_recognition_of_Israel'),
 'u_wp_273': ('Wikipedia: United Nations General Assembly Resolution 273', 'https://en.wikipedia.org/wiki/United_Nations_General_Assembly_Resolution_273'),
 'u_wp_decl': ('Wikipedia: Israeli Declaration of Independence', 'https://en.wikipedia.org/wiki/Israeli_Declaration_of_Independence'),
}
# the 57 members on 29 Nov 1947: name -> registry id
YES = {'Australia': 'australia', 'Belgium': 'belgium', 'Bolivia': 'bolivia', 'Brazil': 'brazil', 'Byelorussian SSR': 'byelorussia', 'Canada': 'canada',
       'Costa Rica': 'costa_rica', 'Czechoslovakia': 'czechoslovakia', 'Denmark': 'denmark', 'Dominican Republic': 'dominican', 'Ecuador': 'ecuador',
       'France': 'france_gov', 'Guatemala': 'guatemala', 'Haiti': 'haiti', 'Iceland': 'iceland', 'Liberia': 'liberia', 'Luxembourg': 'luxembourg',
       'Netherlands': 'netherlands', 'New Zealand': 'new_zealand', 'Nicaragua': 'nicaragua', 'Norway': 'norway', 'Panama': 'panama', 'Paraguay': 'paraguay',
       'Peru': 'peru', 'Philippines': 'philippines', 'Poland': 'poland48', 'Sweden': 'sweden', 'Ukrainian SSR': 'ukraine_ssr', 'Union of South Africa': 'south_africa',
       'United States': 'us_gov', 'Soviet Union': 'ussr', 'Uruguay': 'uruguay', 'Venezuela': 'venezuela'}
NO = {'Afghanistan': 'afghanistan', 'Cuba': 'cuba', 'Egypt': 'egypt', 'Greece': 'greece', 'India': 'india', 'Iran': 'iran', 'Iraq': 'iraq', 'Lebanon': 'lebanon',
      'Pakistan': 'pakistan', 'Saudi Arabia': 'saudi', 'Syria': 'syria', 'Turkey': 'turkey', 'Yemen': 'yemen'}
ABST = {'Argentina': 'argentina', 'Chile': 'chile', 'China': 'china', 'Colombia': 'colombia', 'El Salvador': 'el_salvador', 'Ethiopia': 'ethiopia',
        'Honduras': 'honduras', 'Mexico': 'mexico', 'United Kingdom': 'uk', 'Yugoslavia': 'yugoslavia'}
# recognitions of 1948 (date, form) as the cited page gives them
RECOG = [('us_gov', '14 May 1948', 'de facto (de jure 31 Jan 1949)'), ('ussr', '17 May 1948', 'de jure, the first state to grant it'),
         ('czechoslovakia', '18 May 1948', 'de jure'), ('poland48', '18 May 1948', 'de jure'), ('nicaragua', '18 May 1948', 'de facto and de jure'),
         ('guatemala', '19 May 1948', 'de facto'), ('uruguay', '19 May 1948', 'de facto, the first in Latin America'), ('hungary', '24 May 1948', 'de facto'),
         ('finland', '11 June 1948', 'de facto'), ('romania', '12 June 1948', 'de facto'), ('costa_rica', '19 June 1948', ''), ('panama', '19 June 1948', ''),
         ('venezuela', '27 June 1948', ''), ('paraguay', '7 Sept 1948', ''), ('el_salvador', '11 Sept 1948', ''), ('honduras', '11 Sept 1948', 'de facto; formal on 8 Nov 1948'),
         ('bulgaria', '4 Dec 1948', ''), ('dominican', '29 Dec 1948', '')]
V, R = 'verified', 'reported'
E = []
def add(f, t, ty, st, src, lab): E.append((f, t, ty, st, src, lab))
add('un', 'unga', 'branch', V, 'u_wp_un', 'Charter signed at San Francisco on 26 June 1945 by 50 countries; the UN came into existence on 24 Oct 1945. It replaced the League of Nations, which had effectively closed in 1939.')
add('un', 'unscop', 'founding', V, 'u_wp_part', 'May 1947: the UN formed the Special Committee on Palestine (UNSCOP).')
add('unscop', 'res181', 'proposal', V, 'u_wp_part', '3 Sept 1947: UNSCOP\'s majority (Canada, Czechoslovakia, Guatemala, the Netherlands, Peru, Sweden, Uruguay) proposed partition with economic union; India, Iran and Yugoslavia proposed a federal state; Australia abstained.')
for nm, i in [('Canada', 'canada'), ('Czechoslovakia', 'czechoslovakia'), ('Guatemala', 'guatemala'), ('Netherlands', 'netherlands'), ('Peru', 'peru'), ('Sweden', 'sweden'), ('Uruguay', 'uruguay')]:
    add(i, 'unscop', 'membership', V, 'u_wp_part', f'{nm} sat on UNSCOP and backed its majority plan for partition.')
for nm, i in [('India', 'india'), ('Iran', 'iran'), ('Yugoslavia', 'yugoslavia')]:
    add(i, 'unscop', 'membership', V, 'u_wp_part', f'{nm} sat on UNSCOP and backed the minority plan for a federal state.')
add('unga', 'res181', 'official act', V, 'u_wp_part; u_jvl_181', '29 Nov 1947: adopted 33 to 13 with 10 abstentions and 1 absent. It needed two-thirds of the votes cast, abstentions not counted, among the 57 members; held on the original date it would have had a majority but not two-thirds.')
for nm, i in YES.items(): add(i, 'res181', 'vote for', V, 'u_jvl_181', f'{nm} voted for partition, 29 Nov 1947.')
for nm, i in NO.items(): add(i, 'res181', 'vote against', V, 'u_jvl_181', f'{nm} voted against partition, 29 Nov 1947.')
for nm, i in ABST.items(): add(i, 'res181', 'abstention', V, 'u_jvl_181', f'{nm} abstained on partition, 29 Nov 1947.')
add('siam', 'res181', 'association', V, 'u_wp_part', 'Siam was absent: its credentials were cancelled after it voted against partition in committee on 25 Nov 1947.')
# the reported pressure campaign
add('us_gov', 'philippines', 'pressure', R, 'u_wp_part', 'The Philippine delegate had argued against partition; "after a phone call from Washington, the representative was recalled and the Philippines\' vote changed."')
add('us_gov', 'haiti', 'pressure', R, 'u_wp_part', '"The promise of a five million dollar loan may or may not have secured Haiti\'s vote for partition."')
add('firestone', 'liberia', 'pressure', R, 'u_wp_part', 'Harvey S. Firestone Jr., with major holdings in Liberia, pressured the Liberian government; Liberia\'s ambassador complained the US delegation threatened aid cuts.')
add('baruch', 'france_gov', 'pressure', R, 'u_wp_part', 'Bernard Baruch visited France\'s delegate and implied that a French vote against might block planned American aid to France.')
add('us_congress', 'res181', 'pressure', R, 'u_wp_part', 'A telegram signed by 26 senators with influence over foreign-aid bills was sent to wavering countries.')
add('lovett', 'res181', 'testimony', R, 'u_wp_part', 'Under Secretary Robert Lovett reported that "bribes and threats were being used, even of American sanctions against Liberia and Nicaragua."')
add('zemurray', 'res181', 'pressure', R, 'u_wp_part', 'Sam Zemurray reportedly pressured Central American states.')
add('aranha', 'res181', 'coordination', V, 'u_wp_part', 'The vote was postponed by three days after filibustering by the Zionist delegation; supporters used the delay to press states not yet backing the resolution.')
add('india', 'res181', 'testimony', R, 'u_wp_part', 'Nehru said "the Zionists had tried to bribe India with millions"; Ambassador Vijaya Lakshmi Pandit reportedly received threats unless she "voted right".')
add('arab_league', 'res181', 'pressure', R, 'u_wp_part', 'The Arab states warned that endorsing partition might bring an oil embargo or a realignment with the Soviet bloc.')
# from the vote to the state
add('res181', 'decl_indep', 'legal basis', V, 'u_wp_decl', '14 May 1948: the Declaration cited Resolution 181 among its legal bases.')
add('provisional', 'decl_indep', 'signatory', V, 'u_wp_decl', 'All 37 members of the Provisional State Council were to sign; 25 signed at the Tel Aviv Museum on 14 May 1948, with spaces left for the 12 absent.')
for i, dt, form in RECOG: add(i, 'decl_indep', 'recognition', V, 'u_wp_recog', f'{dt}: recognized Israel' + (f', {form}.' if form else '.'))
add('unsc', 'res273', 'proposal', V, 'u_wp_273', '4 Mar 1949: Security Council Resolution 69 recommended admission.')
add('unga', 'res273', 'official act', V, 'u_wp_273', '11 May 1949: Israel admitted to the UN, 37 to 12 with 9 abstentions; the resolution recalls Resolutions 181 (Jerusalem) and 194 (refugees) and notes Israel\'s declarations on implementing them.')

NOTES = {
 '+un': 'Founded 24 Oct 1945 (Charter signed 26 June 1945 by 50 countries), after the League of Nations had effectively closed in 1939. Partition needed two-thirds of the General Assembly votes cast.',
 '+res181': 'Adopted 29 Nov 1947, 33 to 13 with 10 abstentions (Siam absent). Two-thirds of votes cast was needed: 31 of 46. It would have failed with 3 fewer votes for and 3 more against, or with 8 votes for turned into abstentions.',
 'res273': 'UN admission of Israel, 11 May 1949 (37-12-9).',
}
NEW = '''belgium|Belgium (government)|government|international|Belgian government
bolivia|Bolivia (government)|government|international|Bolivian government
byelorussia|Byelorussian SSR|government|soviet bloc|Byelorussian SSR;Byelorussia
costa_rica|Costa Rica (government)|government|international|Costa Rican government
denmark|Denmark (government)|government|international|Danish government
dominican|Dominican Republic (government)|government|international|Dominican Republic
ecuador|Ecuador (government)|government|international|Ecuadorian government
iceland|Iceland (government)|government|international|Icelandic government
luxembourg|Luxembourg (government)|government|international|Luxembourg government
new_zealand|New Zealand (government)|government|international|New Zealand government
norway|Norway (government)|government|international|Norwegian government
paraguay|Paraguay (government)|government|international|Paraguayan government
poland48|Poland (government, 1940s)|government|soviet bloc|Polish government@cw1
ukraine_ssr|Ukrainian SSR|government|soviet bloc|Ukrainian SSR
venezuela|Venezuela (government)|government|international|Venezuelan government
afghanistan|Afghanistan (government)|government|international|Afghan government
lebanon|Lebanon (government)|government|arab states|Lebanese government
pakistan|Pakistan (government)|government|international|Pakistani government
saudi|Saudi Arabia (government)|government|arab states|Saudi government
turkey|Turkey (government)|government|international|Turkish government
yemen|Yemen (government)|government|arab states|Yemeni government
argentina|Argentina (government)|government|international|Argentine government
chile|Chile (government)|government|international|Chilean government
china|China (government)|government|international|Chinese government;Nationalist China
colombia|Colombia (government)|government|international|Colombian government
el_salvador|El Salvador (government)|government|international|Salvadoran government
ethiopia|Ethiopia (government)|government|international|Ethiopian government
honduras|Honduras (government)|government|international|Honduran government
siam|Siam (government)|government|international|Siamese delegation
hungary|Hungary (government)|government|soviet bloc|Hungarian government
finland|Finland (government)|government|international|Finnish government
romania|Romania (government)|government|soviet bloc|Romanian government
bulgaria|Bulgaria (government)|government|soviet bloc|Bulgarian government
baruch|Bernard Baruch|person|finance|Bernard Baruch;Baruch
zemurray|Sam Zemurray|person|finance|Sam Zemurray;Zemurray
res273|UN Resolution 273 (admission of Israel, 1949)|document|international|Resolution 273
'''

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    assert (len(YES), len(NO), len(ABST)) == (33, 13, 10)
    json.dump({'_note': 'UN layer (Nov 2026). Built by un_layer.py; do not edit by hand.', 'node_notes': NOTES,
               'vote181': {'yes': sorted(set(YES.values())), 'no': sorted(set(NO.values())), 'abstain': sorted(set(ABST.values())), 'need': '2/3 of yes+no'},
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'un_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_un_layer', 'stage': 'rd2', 'topic': 'UN layer: the founding of the UN, UNSCOP, all 57 votes on Resolution 181, the reported pressure campaign, the 1948 recognitions and the 1949 admission (Nov 2026)',
             'claims': [lab for *_, lab in E], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_un_layer', 'verified': '2026-11-05', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_un_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__':
    if '--registry' in sys.argv:
        s = open(os.path.join(HERE, 'registry.py')).read()
        if 'UN layer: every vote' not in s:
            i = s.rindex('"""'); s = s[:i] + '# ---------- UN layer: every vote on partition, recognitions (added Nov 2026) ----------\n' + NEW + s[i:]
            open(os.path.join(HERE, 'registry.py'), 'w').write(s); print('registry updated')
    else: main()
