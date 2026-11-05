"""The decisions layer: the documented ties behind four more key decisions, so the holistic decision standard reaches them
as it reaches Balfour and the American votes: the League's approval of the Mandate (1922), Britain's referral of Palestine
to the UN (Feb 1947), Soviet support for partition (1947-48) and the Czechoslovak arms (1948). Writes decision_layer.json
and book/research/road_decision_layer.json. 'reported' where the page reports or infers rather than documents the act."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
S = {
 'd_spec22': ('The Spectator, 29 July 1922: the Council of the League of Nations on Monday approved the Mandates', 'https://archive.spectator.co.uk/article/29th-july-1922/2/the-council-of-the-league-of-nations-on-monday-app'),
 'd_jvl_league': ('Jewish Virtual Library: The League of Nations', 'https://www.jewishvirtuallibrary.org/the-league-of-nations'),
 'd_oj_league': ('Opinio Juris (27 July 2026): Sleight-of-hand on Palestine at the League of Nations', 'https://opiniojuris.org/2026/07/27/sleight-of-hand-on-palestine-at-the-league-of-nations-how-the-alteration-of-a-verb-tense-legalized-britains-mandate/'),
 'd_frus_736': ('FRUS 1947, vol. V, doc. 736: Gallman (London) to the Secretary of State, 14 Feb 1947', 'https://history.state.gov/historicaldocuments/frus1947v05/d736'),
 'd_cojs_47': ('Center for Online Judaic Studies: British decision to abandon the Mandate, 18 Feb 1947', 'https://cojs.org/british_decision_to_abandon_the_mandate-_feb-_18-_1947/'),
 'd_hansard_47': ('Hansard, HC Deb 25 February 1947, vol 433: Palestine (Government policy)', 'https://api.parliament.uk/historic-hansard/commons/1947/feb/25/palestine-government-policy'),
 'd_frus_765': ('FRUS 1947, vol. V, doc. 765: Statement by the Soviet representative (Gromyko), 14 May 1947', 'https://history.state.gov/historicaldocuments/frus1947v05/d765'),
 'd_jvl_sov': ('Jewish Virtual Library: The Soviet position on partition', 'https://www.jewishvirtuallibrary.org/the-soviet-position-on-partition'),
 'd_mef_prague': ('Middle East Quarterly: The birth of Israel, Prague\'s crucial role', 'https://www.meforum.org/7263/the-birth-of-israel-prague-crucial-role'),
 'd_wp_czarms': ('Wikipedia: Arms shipments from Czechoslovakia to Israel', 'https://en.wikipedia.org/wiki/Arms_shipments_from_Czechoslovakia_to_Israel'),
}
V, R = 'verified', 'reported'
E = []
def add(f, t, ty, st, src, lab): E.append((f, t, ty, st, src, lab))
# --- the League's approval of the Mandate, 24 July 1922 ---
add('balfour', 'league', 'proposal', V, 'd_spec22', 'July 1922, London: at the League Council session that approved the Mandates, Balfour spoke for Britain; he said the Mandates would operate together and appealed to Arabs and Jews to live in peace.')
add('league', 'mandate', 'official act', V, 'd_jvl_league; d_oj_league', '24 Jul 1922: the League Council confirmed the Mandate, which carried the Balfour Declaration. France held up the Palestine mandate until the Syria mandate was settled with Italy; both entered into force on 29 Sept 1923.')
# --- Britain refers Palestine to the UN, February 1947 ---
add('bevin', 'un', 'proposal', V, 'd_frus_736; d_cojs_47', '14 Feb 1947: the Cabinet agreed with Bevin and Creech Jones that, with neither Arabs nor Jews accepting the British plan, the question must go to the UN "without British recommendations"; Bevin announced it to the Commons on 18 Feb, citing an "irreconcilable conflict of principles".')
add('creech', 'bevin', 'collaboration', V, 'd_frus_736', 'Feb 1947: the Colonial Secretary, Arthur Creech Jones, joined Bevin in the proposal the Cabinet accepted.')
add('ahc', 'uk', 'opposition', V, 'd_frus_736; d_cojs_47', 'Feb 1947: the Arab delegates at the London Conference rejected the British plan and any Jewish sovereignty; their refusal and the Jewish Agency\'s were the deadlock Bevin cited.')
add('jewish_agency', 'uk', 'opposition', V, 'd_cojs_47', 'Feb 1947: the Jewish side sought a sovereign Jewish state and rejected the British plan.')
# --- Soviet support for partition ---
add('gromyko', 'ussr', 'membership', V, 'd_frus_765', '14 May 1947: Gromyko, for the USSR, preferred one "dual, democratic" Arab-Jewish state, and called partition justifiable only if relations proved too bad for it.')
add('stalin', 'ussr', 'leadership', R, 'd_mef_prague; d_jvl_sov', 'By spring 1947 Stalin backed a Jewish state; the reasons reported are to get Britain out of Palestine and the hope of a pro-Soviet state.')
# --- the Czechoslovak arms, 1948 ---
add('masaryk', 'czechoslovakia', 'official act', V, 'd_wp_czarms; d_mef_prague', '14 Jan 1948: Foreign Minister Jan Masaryk signed the first sale: rifles, machine guns and ammunition (reported at $750,000), routed on Ethiopian papers because Czech rules allowed sales only to states.')
add('avriel', 'czechoslovakia', 'purchase', V, 'd_mef_prague', '1948: Ehud Avriel, the Haganah\'s man in Prague, arranged the first contract and from April 1948 bought Czech aircraft.')
add('avriel', 'haganah', 'membership', V, 'd_mef_prague', 'Avriel represented the Haganah in Prague.')
NOTES = {
 'masaryk': 'Jan Masaryk (1886-1948), Czechoslovak foreign minister, signed the first arms sale to the Haganah on 14 January 1948; he died in March 1948.',
 'avriel': 'Ehud Avriel (1917-1980), the Haganah\'s purchasing agent in Prague in 1948.',
 '+czechoslovakia': 'Through October 1948: 34,500 rifles, 5,515 MG 34 machine guns, 900 heavy machine guns, 25 Avia S-199 and 61 Spitfire fighters (only 18 Spitfires arrived during the war). Ben-Gurion: "Without these weapons, we would have not survived."',
}
NEW = '''masaryk|Jan Masaryk|person|soviet bloc|Jan Masaryk;Masaryk
avriel|Ehud Avriel|person|militias|Ehud Avriel;Avriel
'''

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    json.dump({'_note': 'Decisions layer (Nov 2026). Built by decision_layer.py; do not edit by hand.', 'node_notes': NOTES,
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'decision_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_decision_layer', 'stage': 'rd3', 'topic': 'Decisions layer: the League approval of the Mandate (1922), Britain\'s referral to the UN (Feb 1947), Soviet support for partition (1947), the Czechoslovak arms (1948) (Nov 2026)',
             'claims': [lab for *_, lab in E], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_decision_layer', 'verified': '2026-11-05', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_decision_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__':
    if '--registry' in sys.argv:
        s = open(os.path.join(HERE, 'registry.py')).read()
        if 'Decisions layer' not in s:
            i = s.rindex('"""'); s = s[:i] + '# ---------- Decisions layer (added Nov 2026) ----------\n' + NEW + s[i:]
            open(os.path.join(HERE, 'registry.py'), 'w').write(s); print('registry updated')
    else: main()
