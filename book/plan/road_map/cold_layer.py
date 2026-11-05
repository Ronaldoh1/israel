"""The Cold War layer of the network, 1949-1967: money, the lobby and FARA, intelligence, Dimona and NUMEC,
German arms, oil, and pre-1948 advocacy. Ties cite the book's own source keys (Cold War volume and Volume II),
plus new keys (c_*). Writes cold_layer.json and book/research/road_cold_layer.json."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
S = {
 'c_wp_boi': ('Wikipedia: Bank of Israel', 'https://en.wikipedia.org/wiki/Bank_of_Israel'),
 'c_wp_knesset_bldg': ('Wikipedia: Knesset building', 'https://en.wikipedia.org/wiki/Knesset_building'),
 'c_wp_kirchwey': ('Wikipedia: Freda Kirchwey', 'https://en.wikipedia.org/wiki/Freda_Kirchwey'),
 'c_djn_19470523': ('Detroit Jewish News, 23 May 1947: Nation Associates document on the Arab Higher Committee given to UN delegates', 'https://digital.bentley.umich.edu/djnews/djn.1947.05.23.001/5'),
 'c_hathi_farouk': ('Nation Associates, The record of collaboration of King Farouk of Egypt with the Nazis and their ally, the Mufti (memorandum to the UN, June 1948), HathiTrust record', 'https://catalog.hathitrust.org/Record/000487097/Cite'),
 'c_gendzier_salon': ('Irene Gendzier, Dying to Forget: Oil, Power, Palestine (Columbia UP, 2015), excerpt in Salon, 4 Jan 2016', 'https://www.salon.com/2016/01/04/oil_drives_our_israel_policy_new_government_documents_reveal_a_very_different_history_of_america_and_the_middle_east'),
}
V, R = 'verified', 'reported'
E = [
 # --- who paid for the new state ---
 ('us_gov', 'israel_gov', 'funding', V, 'rs_rd6_jvl_usaid_table; merip_us_aid_israel_1990', 'US aid 1949-59 totalled $652.9M (CRS table), economic aid and loans only; Washington withheld arms so as not to alienate Arab oil states. First military loan: $0.4M in 1959 (CRS) or 1962 (another study).'),
 ('bengurion', 'bonds', 'founding', V, 'rs_rd6_jvl_bonds', 'Sept 1950: Ben-Gurion convened American Jewish leaders at the King David Hotel; sales launched in the US in spring 1951 at Madison Square Garden.'),
 ('bonds', 'israel_gov', 'funding', V, 'rs_rd6_jvl_bonds', '1951 Independence Issue at 3.5%; first-year sales over $52M; within six years 35% of the development budget (Water Carrier, Dead Sea Works, power, ports).'),
 ('knesset', 'lux_agreement', 'official act', V, 'rs_rd6_jvl_reparations', '9 Jan 1952: the Knesset voted 61-50 to negotiate directly with West Germany, amid demonstrations.'),
 ('begin', 'lux_agreement', 'opposition', V, 'rs_rd6_nli_reparations', 'Begin led the opposition at mass demonstrations: "blood money" from the "land of the murderers".'),
 ('sharett', 'lux_agreement', 'signatory', V, 'rs_rd6_nli_reparations; rs_rd6_jvl_reparations', 'Signed in Luxembourg, 10 Sept 1952, by Sharett, Goldmann and Adenauer; in force 21 Mar 1953.'),
 ('goldmann', 'lux_agreement', 'signatory', V, 'rs_rd6_nli_reparations', 'Nahum Goldmann signed for the Claims Conference side.'),
 ('adenauer', 'lux_agreement', 'signatory', V, 'rs_rd6_nli_reparations', 'Chancellor Adenauer signed for West Germany.'),
 ('west_germany', 'lux_agreement', 'signatory', V, 'rs_rd6_nli_reparations', 'West Germany paid in kind, 1953-66.'),
 ('lux_agreement', 'israel_gov', 'funding', V, 'rs_rd6_jvl_reparations; rs_rd6_nli_reparations', '$845M (JVL) or 3.5bn + 0.45bn marks (NLI); 30% as crude oil bought in Britain, 70% German goods; 12-14% of Israel\'s imports for a decade.'),
 ('lux_agreement', 'claims_conf', 'funding', V, 'rs_rd6_jvl_reparations', '$100M of the total went to the Claims Conference (one source\'s figure).'),
 ('eban', 'acheson', 'meeting', V, 'rs_cw1_frus1951_eban_request', 'Mar 1951: Eban and David Horowitz handed Acheson a request for a $150M grant-in-aid (immigrants, defence, UNRWA reintegration).'),
 ('horowitz_d', 'acheson', 'meeting', V, 'rs_cw1_frus1951_eban_request', 'Horowitz of the Finance Ministry joined Eban in the grant request.'),
 ('douglas_p', 'msa1951', 'drafting', V, 'rs_cw1_jta_douglas_taft_1951', 'About 3 Apr 1951: Senators Douglas and Taft introduced a $150M aid bill, calling Israel "a bulwark" against Communism, "particularly in Iran".'),
 ('taft', 'msa1951', 'drafting', V, 'rs_cw1_jta_douglas_taft_1951; rs_cw1_kenen_silver_letter', 'Taft co-sponsored the bill and backed the Douglas amendment of Aug 1951.'),
 ('mccormack', 'msa1951', 'drafting', V, 'rs_cw1_jta_douglas_taft_1951', 'House Majority Leader McCormack introduced the companion bill ("a dependable ally").'),
 ('truman', 'msa1951', 'official act', V, 'rs_cw1_truman_unrpr_letter', '10 Oct 1951: Truman signed the Mutual Security Act of 1951 ($50M for the UN refugee programme).'),
 ('msa1951', 'israel_gov', 'funding', V, 'rs_cw1_jta_kenen_obit; rs_cw1_kenen_silver_letter', 'First US grant to Israel: $65M (JTA) or about $68.8M authorized (Kenen); FY1953 a further $73M (June 1952).'),
 ('state_dept', 'msa1951', 'opposition', V, 'rs_cw1_frus1951_feinberg_memo', 'The Administration proposed $23.5M for Israel, $23.5M for the Arab states and $50M for refugees (24 May 1951).'),
 ('mcghee', 'blaustein', 'opposition', V, 'rs_cw1_frus1951_feinberg_memo', 'McGhee declined Jacob Blaustein\'s request for $75M each.'),
 ('feinberg', 'mcghee', 'pressure', V, 'rs_cw1_frus1951_feinberg_memo', 'July 1951: Feinberg visited McGhee "at the Suggestion of the President".'),
 ('truman', 'feinberg', 'instruction', V, 'rs_cw1_frus1951_feinberg_memo', 'The memo records Feinberg came at the President\'s suggestion.'),
 ('kenen', 'msa1951', 'pressure', V, 'rs_cw1_kenen_silver_letter', 'Aug 1951: Kenen worked the Senate floor; Israel\'s share rose from about 1% to 5.2% of the bill.'),
 ('kenen', 'silver', 'correspondence', V, 'rs_cw1_kenen_silver_letter', 'Kenen reported to Silver: "all this is still an authorization."'),
 ('eban', 'kenen', 'instruction', R, 'rs_cw1_israelhayom_barda', 'Eban suggested Kenen move to Washington (Barda, via Israel Hayom).'),
 ('kenen', 'israel_gov', 'membership', V, 'rs_cw1_jta_kenen_obit', '1949: member of Israel\'s first UN delegation; 1947-48 the Jewish Agency\'s information director at the UN.'),
 ('kenen', 'azcpa', 'founding', V, 'rs_cw1_jta_kenen_obit; rs_cw1_jvl_aipac; rs_cw5_kenen_uja_1963', 'Founded the American Zionist Committee for Public Affairs (1951, 1953 or 1954 by different accounts), renamed AIPAC.'),
 ('knesset', 'bank_israel', 'founding', V, 'c_wp_boi', '24 Aug 1954: the Knesset passed the Bank of Israel Law; the central bank is state-owned (Ministry of Finance).'),
 ('horowitz_d', 'bank_israel', 'leadership', V, 'c_wp_boi', 'David Horowitz was the first governor, for 17 years.'),
 ('apc_bank', 'bank_israel', 'succession', V, 'c_wp_boi', 'Before 1954 the currency was issued by the Anglo-Palestine Bank (Bank Leumi from 1950).'),
 ('james_armand', 'knesset_bldg', 'funding', V, 'c_wp_knesset_bldg', 'James de Rothschild left £1.25M in his will for the Knesset building (announced July 1957); inaugurated 30 Aug 1966.'),
 ('knesset_bldg', 'knesset', 'association', V, 'c_wp_knesset_bldg', 'Home of the Knesset from 1966.'),
 # --- the lobby, FARA and the Senate inquiry ---
 ('rfk', 'doj', 'leadership', V, 'israellobby_org_fara_doj_order', 'Robert F. Kennedy was Attorney General 1961-63; the Internal Security Section acted under his authority.'),
 ('doj', 'azc', 'official act', V, 'israellobby_org_fara_doj_order; acjna_fara', '21 Nov 1962: ordered the American Zionist Council to register as agent of a foreign principal. Never enforced to completion; the Council never registered (one 2016 Wikipedia version says otherwise).'),
 ('jewish_agency', 'azc', 'funding', V, 'azc_fara_doj; jta_fulbright_jewish_agency_hearing', 'Senate record: $5,100,001.02 from the Jewish Agency to the Council, 1955-62 (Barda gives $1.5M; unreconciled).'),
 ('fulbright', 'sfrc', 'leadership', V, 'rs_cw5_djn_19630628', 'Fulbright chaired the Senate Foreign Relations Committee inquiry (S. Res. 362 and 26, 1963).'),
 ('sfrc', 'ja_american', 'surveillance', V, 'rs_cw5_ol_hearings; rs_cw5_djn_19630628', 'Part 9 of the 13-part inquiry into agents of foreign principals concerned the Jewish Agency; closed sessions, June-Aug 1963.'),
 ('hammer_g', 'sfrc', 'testimony', V, 'rs_cw5_djn_19630628', 'Gottlieb Hammer testified in closed session, 28 June 1963.'),
 ('boukstein', 'sfrc', 'testimony', V, 'jta_fulbright_jewish_agency_hearing', 'Agency attorney Boukstein rejected Fulbright\'s premise: the Agency was "a completely independent body".'),
 ('ja_american', 'jewish_agency', 'branch', V, 'rs_cw5_djn_19630628', 'The American Section of the Jewish Agency.'),
 ('ja_american', 'fara', 'legal basis', V, 'rs_cw5_djn_19630628; rs_cw5_doj_fara_1964', 'The American Section was already a FARA registrant in 1963, as agent of the WZO and the Jewish Agency in Jerusalem.'),
 ('neumann', 'ja_american', 'leadership', V, 'rs_cw5_djn_19630816', 'Aug 1963: Neumann, chairman of the American Section, called the result a vindication.'),
 ('azc', 'near_east_report', 'funding', V, 'rs_cw5_barda_2026', '25 Jan 1955: the Council\'s board decided to launch the newsletter and bought 5,500 copies at 15 cents (Barda, from Council records).'),
 ('kenen', 'near_east_report', 'leadership', V, 'rs_cw5_barda_2026', 'Kenen ran the Near East Report; his affidavit said Council purchases never exceeded 23% and ended in 1962.'),
 ('fbi', 'azc', 'association', R, 'rs_cw5_smith_podcast', 'Oct 1963: the FBI offered to help enforce the order (Grant F. Smith, IRmep).'),
 # --- intelligence ---
 ('bengurion', 'mossad', 'founding', V, 'rs_cw1_jvl_mossad_directive', '13 Dec 1949: secret directive establishing "an institute ... to co-ordinate state intelligence agencies", Shiloah to head it, about IL20,000 for 1950-51.'),
 ('harel', 'shin_bet', 'leadership', V, 'rs_cw1_jvl_isa', 'Isser Harel headed the internal security service (Shin Bet), created 1948.'),
 ('aman', 'idf', 'branch', V, 'rs_cw1_jvl_isa', 'Military intelligence (Aman) went to the army when the Haganah intelligence service dissolved, 30 June 1948.'),
 ('angleton', 'mossad', 'collaboration', V, 'rs_cw2_robarge', 'From 1954 Angleton ran the CIA\'s Counterintelligence Staff and controlled the Israel account, "an administrative anomaly" (CIA chief historian); he "saw Israel as a bastion against the Soviet Union".'),
 ('aman', 'susannah', 'operation', V, 'wiki_lavon_affair; rs_cw2_mod_lavon', 'July 1954: Aman activated Unit 131, Egyptian Jews trained for sabotage, to damage Egypt\'s relations with the West during the Suez base talks.'),
 ('susannah', 'us_gov', 'violence', V, 'wiki_lavon_affair; rs_cw2_mod_lavon', 'Targets included the American information libraries in Cairo and Alexandria (14 July 1954) and British cinemas, with blame meant to fall on Egyptians.'),
 ('susannah', 'egypt', 'violence', V, 'wiki_lavon_affair', 'Incendiary devices in Cairo and Alexandria; the cell was caught.'),
 # --- the nuclear thread ---
 ('peres', 'dimona', 'leadership', V, 'rs_cw4_ebb510', '1955: Ben-Gurion launched a secret feasibility initiative and delegated it to Peres.'),
 ('france_gov', 'dimona', 'supply', V, 'rs_cw4_fas_israel; rs_cw4_jvl_nuclear; rs_cw4_goldschmidt', 'Autumn 1956: France agreed to supply a reactor; a reprocessing (plutonium separation) plant followed after internal resistance at the CEA.'),
 ('jfk', 'bengurion', 'correspondence', V, 'rs_cw5_nsa_letters', 'The battle of the letters, 27 Mar-15 June 1963: Kennedy pressed for regular inspections of Dimona.'),
 ('jfk', 'eshkol', 'correspondence', V, 'rs_cw5_nsa_letters', '19 Aug 1963: Eshkol accepted regular visits in principle, not the twice-yearly interval; Kennedy\'s 26 Aug reply assumed "basic agreement".'),
 ('jfk', 'dimona', 'pressure', V, 'rs_cw5_nsa_letters', 'Kennedy demanded inspections; the first visit under the 1963 arrangement came on 18 Jan 1964.'),
 ('lbj', 'dimona', 'pressure', V, 'rs_cw5_cns_duplicity; rs_cw5_frus6468_summary', 'Johnson kept insisting on the visits; inspectors found no weapons programme while suspicions continued.'),
 ('shapiro_z', 'numec', 'leadership', V, 'rs_cw6_nsa_numec', 'NUMEC founded 1957 at Apollo, Pennsylvania; Zalman Shapiro a founder and later president.'),
 ('numec', 'israel_gov', 'association', R, 'rs_cw6_nsa_numec', '1965-66: 93.8 kg of government-owned U-235 unexplained. The archive editors call evidence of diversion to Israel "strong but not incontrovertible"; the AEC found no evidence of theft and did not look; CIA records remain redacted.'),
 # --- German arms ---
 ('strauss_fj', 'peres', 'meeting', V, 'rs_cw6_serr_bpb', 'Winter 1957: Peres and Strauss met secretly; the channel ran without a German embassy in Israel.'),
 ('adenauer', 'israel_gov', 'supply', V, 'rs_cw6_serr_bpb', 'Aug 1962: Adenauer approved a secret Israeli wish list of 240M DM, including tanks.'),
 ('west_germany', 'israel_gov', 'supply', V, 'rs_cw6_frus18_d99', '1964: 150 M48 tanks from West Germany "as is", with an option on 82 more.'),
 ('us_gov', 'west_germany', 'coordination', V, 'rs_cw6_frus18_d99', 'The US sold $24M of modernization kits on credit and sped replacement tanks to Germany; the deal could be cancelled if it became public.'),
 ('rusk', 'lbj', 'correspondence', V, 'rs_cw6_frus18_d99', 'Oct 1964: Rusk\'s memo "FY-1965 Help to Israel" to Johnson.'),
 ('hawk', 'israel_gov', 'supply', V, 'merip_us_aid_israel_1990', '1962: the first American military aid, as loans (the Hawk decision).'),
 ('west_germany', 'dimona', 'funding', R, 'rs_cw4_barjoseph', 'Contested: the historian Uri Bar-Joseph argues West Germany was the "major funder" of Dimona through the Negev loan; Peres denied it and Germany has been silent.'),
 ('numec', 'dimona', 'association', R, 'nsarchive_numec', 'The National Security Archive reports a CIA conclusion that 1968 sampling near Dimona found uranium of the same unusual enrichment as NUMEC\'s missing material; Helms raised it with Johnson (still classified). A 1978 GAO study said a concerted effort could have resolved the question "if they desired to do so".'),
 # --- oil and advocacy around 1948 ---
 ('max_ball', 'epstein_e', 'meeting', V, 'c_gendzier_salon', '1948: Max Ball, head of the Interior Department\'s oil and gas division, met Eliahu Epstein of the Jewish Agency; Gendzier calls it the basis of the "oil connection" (from Ball\'s papers).'),
 ('epstein_e', 'jewish_agency', 'membership', V, 'c_gendzier_salon', 'Eliahu Epstein, the Jewish Agency\'s representative in Washington.'),
 ('kirchwey', 'nation_assoc', 'founding', V, 'c_wp_kirchwey', '1943: Freda Kirchwey created the Nation Associates, a sponsor-funded nonprofit, when she sold her ownership of The Nation.'),
 ('kirchwey', 'truman', 'correspondence', V, 'c_wp_kirchwey', 'Letters to Truman of 10 May and 19 June 1948.'),
 ('nation_assoc', 'ahc', 'opposition', V, 'c_djn_19470523', 'May 1947: Kirchwey gave UN delegates a 75-page dossier from the Mufti\'s files arguing the Arab Higher Committee was in "active partnership with Rome and Tokyo".'),
 ('nation_assoc', 'un', 'testimony', V, 'c_djn_19470523; c_hathi_farouk', 'Submissions to the UN in May 1947 and June 1948 (the second on King Farouk\'s and the Mufti\'s Nazi ties).'),
 ('nation_assoc', 'egypt', 'opposition', V, 'c_hathi_farouk', 'June 1948 memorandum: "The record of collaboration of King Farouk of Egypt with the Nazis and their ally, the Mufti".'),
]
NOTES = {
 'jfk': 'Documented: the Dimona letters (1963), the FARA order to the American Zionist Council under his brother\'s Justice Department (Nov 1962), and the Fulbright inquiry. On the assassination: the Warren Commission and the House Select Committee did not identify Dimona, the lobby or Israel as a factor, and the standard historians of the nuclear dispute (Avner Cohen, Seymour Hersh) draw no connection. The map records 22 November 1963 as a date, not a tie. See the book, section s11c.',
 'max_ball': 'Irene Gendzier, from Ball\'s papers, FRUS and Israeli records: the choice in Washington was "not oil versus Israel but rather oil and Israel".',
 'nation_assoc': 'An advocacy group that put the Arab leadership\'s wartime Axis ties before the UN and the President in 1947-48. The Mufti\'s collaboration is itself documented (Volume II). No funding link between the Nation Associates and Zionist bodies was found in the sources checked.',
 'james_armand': 'After 1948 the documented Rothschild money in Israel ran through visible institutions: PICA\'s land passed to the JNF (1957-58); Yad Hanadiv; the Knesset building (£1.25M bequest, 1966). No document found shows Rothschild ownership or control of the Bank of Israel, which is state-owned and created by Knesset law in 1954.',
}

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    json.dump({'_note': 'Cold War layer (Nov 2026). Built by cold_layer.py; do not edit by hand.', 'node_notes': NOTES,
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'cold_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_cold_layer', 'stage': 'cw1', 'topic': 'Cold War layer of the network: the Bank of Israel, the Knesset building, the Nation Associates and the oil connection (Nov 2026)',
             'claims': [lab for f, t, ty, st, src, lab in E if 'c_' in src], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_cold_layer', 'verified': '2026-11-04', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_cold_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__': main()
