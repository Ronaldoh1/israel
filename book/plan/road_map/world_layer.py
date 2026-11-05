"""The world layer of the 1948 network: Congress, the arms network, Aliyah Bet, the UN vote and foreign governments.
Ties cite the book's own source keys where the book documents them, and new keys (w_*) where it does not.
Writes world_layer.json and book/research/road_world_layer.json."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)

S = {
 'w_wp_cambon': ('Wikipedia: Cambon letter (June 1917)', 'https://en.wikipedia.org/wiki/Cambon_letter'),
 'w_etzel_poland': ('Irgun (Etzel) history site, daat.ac.il: Activities in Europe before World War Two (the Irgun\'s own account)', 'https://daat.ac.il/etzel/english/ac16.htm'),
 'w_wp_altalena': ('Wikipedia: Altalena Affair', 'https://en.wikipedia.org/wiki/Altalena_Affair'),
 'w_wp_granados': ('Wikipedia: Jorge García Granados', 'https://en.wikipedia.org/wiki/Jorge_Garc%C3%ADa_Granados'),
 'w_ecom_smuts': ('Encyclopaedia Judaica via Encyclopedia.com: Smuts, Jan Christiaan', 'https://encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/smuts-jan-christiaandeg'),
 'w_jrb_1944': ('Jewish Review of Books: Zion and Party Politics, 1944', 'https://jewishreviewofbooks.com/articles/2287/zion-and-party-politics-1944/'),
}
V, R = 'verified', 'reported'
E = [
 # --- Congress, 1922 ---
 ('glazer', 'lodge_fish', 'pressure', V, 'jvl_lodge_fish', 'American Zionist leaders asked Lodge and Fish to introduce the resolution; the JVL credits the lobbying work of Rabbi Simon Glazer.'),
 ('lodge', 'lodge_fish', 'drafting', V, 'jvl_lodge_fish; wiki_lodge_fish', 'Senator Henry Cabot Lodge (R-Mass.) introduced the resolution endorsing the Balfour Declaration.'),
 ('fish', 'lodge_fish', 'drafting', V, 'jvl_lodge_fish; wiki_lodge_fish', 'Representative Hamilton Fish III (R-N.Y.) introduced it in the House.'),
 ('state_dept', 'lodge_fish', 'opposition', V, 'jvl_lodge_fish; wjc_lodge_fish', 'The State Department (and the New York Times) opposed the resolution.'),
 ('us_congress', 'lodge_fish', 'official act', V, 'jvl_lodge_fish; wjc_lodge_fish', 'House passed it 30 June 1922; the Senate by unanimous consent 13 July 1922.'),
 ('harding', 'lodge_fish', 'official act', V, 'wiki_lodge_fish; jvl_lodge_fish', '21 Sep 1922: Harding signed Public Resolution 67-73, favouring a national home and protecting the rights of "Christian and all other non-Jewish communities".'),
 ('sokolow', 'harding', 'meeting', V, 'israeled_sokolow_harding', '13 Jan 1922: Sokolow met Harding for nearly an hour during the Keren Hayesod tour (whether it touched the resolution is not recorded).'),
 ('lodge_fish', 'balfour_decl', 'association', V, 'wiki_lodge_fish; balfour_letter', 'The resolution repeated the Balfour Declaration\'s phrase "a national home for the Jewish people".'),
 # --- Congress, 1944-45 ---
 ('wright_j', 'wright_compton', 'drafting', V, 'djn_1944_hearings; aja_azec_dec1944', 'Jan 1944: Rep. James Wright (D-Pa.) co-sponsored the House resolution for a "free and democratic Jewish commonwealth".'),
 ('compton_r', 'wright_compton', 'drafting', V, 'djn_1944_hearings; aja_azec_dec1944', 'Rep. Ranulf Compton (R-Conn.) co-sponsored it.'),
 ('wagner', 'wright_compton', 'drafting', V, 'djn_1944_hearings; aja_azec_dec1944', 'Sen. Robert Wagner (D-N.Y.) sponsored the Senate version.'),
 ('taft', 'wright_compton', 'drafting', V, 'djn_1944_hearings; aja_azec_dec1944', 'Sen. Robert Taft (R-Ohio) co-sponsored the Senate version.'),
 ('azec', 'wright_compton', 'pressure', V, 'aja_azec_local_1944', 'Jan 1944: the Emergency Council\'s local committees began their first nationwide letter campaign for the resolutions.'),
 ('lazaron', 'wright_compton', 'opposition', V, 'djn_1944_hearings', 'Rabbi Morris Lazaron testified against: Zionism was an internal Jewish matter, not one for Congress.'),
 ('marshall_g', 'wright_compton', 'opposition', V, 'djn_1944_marshall', 'Mar 1944: Army Chief of Staff Marshall asked Congress to postpone action for military reasons.'),
 ('stimson', 'wright_compton', 'opposition', V, 'djn_1944_marshall; aja_azec_dec1944', 'Mar 1944: Secretary of War Stimson opposed it on military grounds; it was put aside.'),
 ('stimson', 'taft', 'correspondence', V, 'aja_silver_1944', 'Oct 1944: Stimson wrote to Taft that political considerations now outweighed military ones; the objection was withdrawn days before the election.'),
 ('state_dept', 'wright_compton', 'opposition', V, 'aja_azec_dec1944; aja_silver_1944', 'Dec 1944: after House committee approval (30 Nov), action deferred again at the State Department\'s insistence.'),
 ('azec', 'platforms1944', 'pressure', V, 'aja_azec_appraisal_1944', 'Summer 1944: both parties adopted Palestine planks, "the first time in American history", by the council\'s own appraisal.'),
 ('taft', 'platforms1944', 'leadership', V, 'w_jrb_1944', 'Taft chaired the Republican Resolutions Committee and invited Silver to give the convention benediction; the GOP plank called for "unrestricted immigration and land ownership".'),
 ('silver', 'taft', 'collaboration', V, 'w_jrb_1944', 'Silver had a close relationship with Taft and lobbied Republican leaders on the plank.'),
 ('celler', 'platforms1944', 'pressure', V, 'w_jrb_1944', 'Celler sat on the Democratic Resolutions Committee and backed Wise\'s push for a stronger plank; he warned the White House of Jewish voters\' anger over the White Paper.'),
 ('wise', 'platforms1944', 'pressure', V, 'w_jrb_1944', 'Wise lobbied Democratic delegates in Chicago for a plank to match the Republicans\'.'),
 ('wise', 'fdr', 'meeting', V, 'w_jrb_1944', 'Wise secured a meeting with Roosevelt, who weakened the Palestine statement Wise had drafted.'),
 ('us_congress', 'concres1945', 'official act', V, 'frus1945_concres', '17 and 19 Dec 1945: both houses adopted a concurrent resolution, now calling for a "democratic commonwealth" with equal rights "regardless of race or creed".'),
 ('apc', 'concres1945', 'pressure', V, 'wiki_american_palestine_committee', 'The 1945 resolution had the American Palestine Committee\'s support.'),
 ('ccp', 'concres1945', 'pressure', V, 'wiki_american_palestine_committee', 'And the Christian Council on Palestine\'s.'),
 ('celler', 'us_congress', 'membership', V, 'w_celler', 'Rep. Emanuel Celler of Brooklyn, a leading House supporter.'),
 ('bloom', 'us_congress', 'leadership', V, 'w_sol_bloom', 'Sol Bloom chaired the House Foreign Affairs Committee and was a leading supporter.'),
 ('azec', 'bloom', 'pressure', V, 'aja_azec_local_1944', 'Bloom was a target of the council\'s telegram campaigns: it pressed allies as well as opponents.'),
 # --- FARA, the Bergson group, OSS ---
 ('hcnl', 'fara', 'legal basis', V, 'djn_bergson_fara_1944; ushmm_peter_bergson', 'June 1944: the Hebrew Committee of National Liberation registered as a foreign agent, naming the "Hebrew nation" as principal.'),
 ('bergson', 'hcnl', 'leadership', V, 'djn_bergson_fara_1944', 'Hillel Kook ("Peter Bergson") led it and opened a "Hebrew Embassy" in Washington.'),
 ('state_dept', 'fbi', 'instruction', V, 'jta_bergson_fbi', 'FBI files (FOIA, Wyman Institute): the Bergson investigation began at the State Department\'s instigation; informants, mail opening, trash searches.'),
 ('bergson', 'hull', 'opposition', V, 'jta_bergson_fbi', 'An FBI memo: Bergson had "been in the hair of" Secretary of State Cordell Hull.'),
 ('waldman', 'bergson', 'opposition', V, 'jta_bergson_fbi; jewishpress_bergson_part2', 'Morris Waldman of the American Jewish Committee urged officials to deport or draft Kook.'),
 ('goldmann', 'bergson', 'opposition', V, 'jta_bergson_fbi; jewishpress_bergson_part2', 'Nahum Goldmann also urged deportation or the draft.'),
 ('waldman', 'ajc', 'membership', V, 'jta_bergson_fbi', 'Waldman of the American Jewish Committee.'),
 ('oss', 'jewish_agency', 'surveillance', V, 'forward_oss_palestine_desk', 'The OSS Foreign Nationalities Branch ran a Palestine desk tracking Zionist activity, largely from volunteered information.'),
 ('oss', 'sharett', 'surveillance', V, 'forward_oss_palestine_desk', 'Its list reportedly included Moshe Shertok (Sharett).'),
 ('haganah', 'shai', 'branch', V, 'shai_wiki', '1940: the Haganah founded the Shai, its intelligence and counter-espionage service.'),
 ('shai', 'fbi', 'association', R, 'medium_zionist; ips_espionage', 'One account: the Shai had unregistered American branches in New York and Detroit, the FBI knew, and the Justice Department declined to act (contested).'),
 ('fbi', 'bernstein', 'surveillance', R, 'ips_espionage', 'According to the FBI, attorney Bernstein trained Mossad agents, incorporated arms-smuggling companies and watched Arab UN delegates.'),
 # --- the arms network ---
 ('sonneborn_inst', 'czechoslovakia', 'operation', V, 'mexico_arms', 'Purchases were routed through neutral countries: Czechoslovakia, Panama, Mexico, Canada and France.'),
 ('sonneborn_inst', 'panama', 'operation', V, 'mexico_arms', 'Panama was a documented transit country.'),
 ('sonneborn_inst', 'mexico', 'operation', V, 'mexico_arms', 'Mexico was a named, documented transit point.'),
 ('sonneborn_inst', 'canada', 'operation', V, 'mexico_arms', 'Canada was a documented transit country.'),
 ('sonneborn_inst', 'france_gov', 'operation', V, 'mexico_arms', 'France was a documented transit country.'),
 ('sonneborn_inst', 'haganah', 'supply', V, 'mexico_arms_1948', 'Some 800 disguised shipments, about 2,400 tons; most arrived.'),
 ('schwimmer', 'lap', 'operation', V, 'schwimmer_wiki', 'One account: a fictitious Panamanian airline, Lineas Aereas de Panama, carried the aircraft.'),
 ('schwimmer', 'service_airways', 'operation', V, 'sdjw_schwimmer', 'Other account: the charter firm Service Airways Inc. was the cover.'),
 ('schwimmer', 'brazil', 'operation', V, 'schwimmer_wiki', 'About 30 surplus warplanes went via Panama, Brazil and Casablanca.'),
 ('winters', 'haganah', 'supply', V, 'schwimmer_wiki; sdjw_winters', 'Charles Winters exported B-17 bombers (two or three by different accounts).'),
 ('doj', 'winters', 'litigation', V, 'nbc_bush_pardons_winters; sdjw_winters', 'Convicted under the Neutrality Act (1949); served 18 months; pardoned posthumously (2008, Bush; another account says 2001, Clinton).'),
 ('doj', 'greenspun', 'litigation', V, 'nbc_bush_pardons_winters', 'Hank Greenspun convicted under the Neutrality Act, no prison; pardoned by Kennedy in 1961.'),
 ('greenspun', 'haganah', 'supply', V, 'nbc_bush_pardons_winters', 'Greenspun was part of the arms operation tried after the war.'),
 ('meir', 'czechoslovakia', 'funding', V, 'reformjudaism_golda; jwa_golda_50m', 'The reported $50 million from Golda Meyerson\'s 1948 American tour financed arms purchases, including Czechoslovakia\'s.'),
 ('czechoslovakia', 'balak', 'operation', V, 'wiki_operation_balak', 'May-Aug 1948: the airlift from Žatec ("Zebra") to Ekron carried arms and about 25 Avia S-199 fighters (101 Squadron).'),
 ('balak', 'zatec', 'operation', V, 'wiki_operation_balak', 'Base: Žatec airfield, code-named "Zebra".'),
 ('avia', 'balak', 'supply', V, 'machal_avia_s199', 'Avia S-199, a Czech-built Messerschmitt Bf 109 derivative, flown in crated.'),
 ('balak', 'yugoslavia', 'operation', V, 'wiki_operation_balak', 'After a defector exposed Zebra, operations moved to Nikšić in Yugoslavia.'),
 ('us_gov', 'balak', 'opposition', V, 'wiki_operation_balak', 'The United States pressed the UN to close the Zebra base.'),
 ('siroky', 'czechoslovakia', 'membership', V, 'jpost_czech_arms_saved_israel; wiki_czech_arms_israel', '1952: Foreign Minister Široký reported receipts of almost $14.5 million from the sales.'),
 ('stalin', 'czechoslovakia', 'instruction', V, 'jpost_czech_arms_saved_israel', 'The sales went ahead with Stalin\'s consent.'),
 ('uk', 'arab_league', 'supply', V, 'jpost_czech_arms_saved_israel; wiki_czech_arms_israel', 'Britain supplied aircraft and training to the Arab air forces.'),
 ('nicaragua', 'jewish_agency', 'funding', V, 'israelaffairs_italy', 'Somoza\'s Nicaragua extended $3 million in letters of credit for arms buying.'),
 ('france_gov', 'irgun', 'supply', V, 'w_wp_altalena', 'Secret agreement approved by Foreign Minister Bidault: weapons worth 153 million francs for the Altalena, sailed from Port-de-Bouc 11 June 1948 (text of the agreement not found; motives unclear).'),
 ('bidault', 'france_gov', 'leadership', V, 'w_wp_altalena', 'Georges Bidault, French Foreign Minister.'),
 ('altalena', 'irgun', 'operation', V, 'w_wp_altalena', 'The Irgun\'s arms ship (about 940 volunteers).'),
 # --- Aliyah Bet ---
 ('mossad_aliyah', 'haganah', 'branch', V, 'ushmm_aliyah_bet', '1938: the Mossad LeAliyah Bet was created as a branch of the Haganah to organize clandestine immigration.'),
 ('brihah', 'mossad_aliyah', 'coordination', V, 'hsb_aliyah_bet_exodus', 'Brihah, run with Mossad emissaries, partisans and youth movements, moved nearly 200,000 survivors from DP camps to ports in Italy, France, Yugoslavia and Greece.'),
 ('brihah', 'yugoslavia', 'operation', V, 'hsb_aliyah_bet_exodus', 'Yugoslav ports were among the exits.'),
 ('brihah', 'greece', 'operation', V, 'hsb_aliyah_bet_exodus', 'Greek ports were among the exits.'),
 ('brihah', 'france_gov', 'operation', V, 'hsb_aliyah_bet_exodus', 'French ports were among the exits.'),
 ('mossad_aliyah', 'exodus', 'operation', V, 'rs_rd5_ushmm_exodus; ushmm_aliyah_bet', 'July 1947: the Exodus 1947 sailed from Sète, France, with more than 4,500 passengers.'),
 ('uk', 'exodus', 'violence', V, 'ushmm_cyprus_camps', 'Boarded in international waters; passengers returned to camps in Germany.'),
 ('uk', 'cyprus_camps', 'official act', V, 'ushmm_cyprus_camps', 'From Aug 1946 Britain interned intercepted immigrants on Cyprus: about 52,000 by 1948; last camp closed Feb 1949.'),
 # --- the UN vote and recognitions ---
 ('gromyko', 'unga', 'proposal', V, 'israeled_gromyko_speech', '14 May 1947: Gromyko said a single state was preferred but partition was a justifiable alternative, reversing decades of Soviet anti-Zionism.'),
 ('ussr', 'res181', 'official act', V, 'washinst_who_saved_israel', 'Nov 1947: the USSR and its satellites voted for partition; in March 1948 Moscow held to it at the Security Council while Washington turned to trusteeship.'),
 ('ussr', 'israel_gov', 'official act', V, 'wiki_soviet_arab_israeli', '17 May 1948: the first de jure recognition of Israel.'),
 ('aranha', 'res181', 'official act', V, 'un_181_records', 'Assembly president Oswaldo Aranha arranged the three-day postponement before the decisive vote.'),
 ('us_gov', 'haiti', 'pressure', V, 'militaryhistory_partition_plan', 'Haiti moved to yes after direct communication from the American executive.'),
 ('us_gov', 'liberia', 'pressure', V, 'militaryhistory_partition_plan', 'Liberia\'s ambassador complained the US delegation threatened aid cuts.'),
 ('us_gov', 'philippines', 'pressure', V, 'militaryhistory_partition_plan', 'The Philippines came under pressure through economic ties and switched to yes.'),
 ('firestone', 'liberia', 'influence', R, 'militaryhistory_partition_plan', 'Firestone held a rubber concession of about 1.1 million acres, Liberia\'s dominant employer; Michael Cohen ties it to Liberia\'s switch (historian\'s reading).'),
 ('romulo', 'philippines', 'membership', V, 'sagepub_price_resisting_partition', 'Gen. Carlos Romulo wrote of being recalled and overruled by his own president.'),
 ('cuba', 'res181', 'opposition', V, 'sagepub_price_resisting_partition', 'Cuba voted no "in spite of the pressure that has been brought to bear upon us."'),
 ('sandstrom', 'unscop', 'leadership', V, 'rs_rd5_unscop_report', '2 June 1947: Justice Emil Sandström of Sweden elected chairman.'),
] + [(c, 'unscop', 'membership', V, 'rs_rd5_unscop_report', f'UNSCOP member; one of the majority of seven that recommended partition with economic union.') for c in ['canada', 'czechoslovakia', 'guatemala', 'netherlands', 'peru', 'sweden', 'uruguay']] + [
 (c, 'unscop', 'membership', V, 'rs_rd5_unscop_report', 'UNSCOP member; one of the minority of three that recommended a single federal state.') for c in ['india', 'iran', 'yugoslavia']] + [
 ('australia', 'unscop', 'membership', V, 'rs_rd5_unscop_report', 'UNSCOP member (abstained on the report).'),
 ('granados', 'guatemala', 'membership', V, 'w_wp_granados', 'Guatemala\'s UN ambassador and UNSCOP member.'),
 ('granados', 'res181', 'pressure', V, 'w_wp_granados', 'Organized a lobby of Central and South American states for partition.'),
 ('guatemala', 'israel_gov', 'official act', V, 'w_wp_granados', 'First Latin American state to recognize Israel.'),
 ('uk', 'israel_gov', 'official act', V, 'rs_rd5_langham_exit', 'Britain recognized Israel in January 1949; Bevin\'s acceptance was "grudging".'),
 # --- governments that backed the movement before 1948 ---
 ('cambon', 'cambon_letter', 'authorship', V, 'w_wp_cambon', 'June 1917: the French diplomat Jules Cambon wrote of "the renaissance of the Jewish nationality in that Land", months before Balfour.'),
 ('cambon_letter', 'sokolow', 'addressee', V, 'w_wp_cambon', 'Addressed to Nahum Sokolow.'),
 ('france_gov', 'cambon_letter', 'official act', V, 'w_wp_cambon', 'A statement of French government sympathy (unpublished at the time).'),
 ('cambon_letter', 'balfour_decl', 'influence', R, 'w_wp_cambon', 'Martin Kramer argues French assent, with the Vatican\'s, was a precondition for Balfour.'),
 ('beck', 'jabotinsky', 'meeting', R, 'w_etzel_poland', '1936: Jabotinsky met Polish Foreign Minister Józef Beck and laid a basis for cooperation (Irgun\'s own history).'),
 ('beck', 'poland_gov', 'leadership', R, 'w_etzel_poland', 'Józef Beck, Polish Foreign Minister.'),
 ('stern_a', 'poland_gov', 'meeting', R, 'w_etzel_poland', 'Nov 1937: Avraham Stern met senior officials in Warsaw to arrange army-Irgun cooperation.'),
 ('poland_gov', 'irgun', 'supply', R, 'w_etzel_poland', '1937-39: weapons from Polish army depots were shipped to Palestine; Polish officers in civilian clothes trained Irgun commanders (Carpathians, 25 Mar 1939). Warsaw hoped a Jewish state would draw Jewish emigration from Poland.'),
 ('stern_a', 'irgun', 'membership', R, 'w_etzel_poland', 'Stern, then of the Irgun (later founder of Lehi).'),
 ('smuts', 'balfour_decl', 'drafting', V, 'w_ecom_smuts', 'Member of Britain\'s Imperial War Cabinet; helped formulate the Balfour Declaration and the Mandate.'),
 ('smuts', 'weizmann', 'association', V, 'w_ecom_smuts', 'A personal friend of Weizmann and long-standing supporter.'),
 ('smuts', 'south_africa', 'leadership', V, 'w_ecom_smuts', 'Prime Minister of South Africa.'),
 ('south_africa', 'israel_gov', 'official act', V, 'w_ecom_smuts', '1948: Smuts\'s government quickly granted de facto recognition, shortly before losing the election.'),
]
NOTES = {
 'us_congress': 'Congress passed resolutions of support (1922 Lodge-Fish, the 1945 concurrent resolution) but never voted to create or recognize a state; those were executive acts. Named champions: Lodge, Fish, Wagner, Taft, Wright, Compton, Celler, Bloom; two-thirds of the Senate joined the American Palestine Committee. No documented campaign money from Zionist organizations to members of Congress before 1948 was found in the sources checked; the documented levers were letters, telegrams, platform planks and votes. The one documented campaign money in this map is Feinberg and Kaufmann\'s $100,000 for Truman in 1948.',
}

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    json.dump({'_note': 'World layer (Nov 2026). Built by world_layer.py; do not edit by hand.', 'node_notes': NOTES,
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'world_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_world_layer', 'stage': 'rd5', 'topic': 'World layer of the 1948 network: foreign governments before 1948 (France 1917, Poland 1937-39, Smuts), the 1944 platforms, UNSCOP, the French arms for the Altalena (Nov 2026)',
             'claims': [lab for f, t, ty, st, src, lab in E if 'w_' in src], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_world_layer', 'verified': '2026-11-04', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_world_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__': main()
