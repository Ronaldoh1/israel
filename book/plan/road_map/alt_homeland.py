"""Other homelands: the documented alternatives to Palestine (Argentina, 1890s; British East Africa, 1903) measured on the
same six things the state needed. Each channel gets a share of what the Palestine record had, with the reason and the source;
the chance is computed with the same formula as the removal model (viability.CAL, viability.EXP). The shares are judgments
read from the record and are disclosed as such. Writes alt_layer.json and book/research/road_alt_layer.json."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
import viability as V

S = {
 'a_wp_judenstaat': ('Wikipedia: Der Judenstaat', 'https://en.wikipedia.org/wiki/Der_Judenstaat'),
 'a_wp_hirsch_arg': ('Wikipedia: Baron Maurice de Hirsch\'s agricultural settlements in Argentina', 'https://en.wikipedia.org/wiki/Baron_Maurice_de_Hirsch%27s_Agricultural_Settlements_in_Argentina'),
 'a_jvl_ica': ('Jewish Virtual Library: Jewish Colonization Association (ICA)', 'https://www.jewishvirtuallibrary.org/jewish-colonization-association-ica'),
 'a_jta_ica24': ('JTA, 1 Jan 1924: The extent of Jewish colonization in the Argentine: 30,725 persons settled on 590,000 hectares of ICA', 'https://www.jta.org/archive/the-extent-of-jewish-colonization-in-the-argentine-30725-persons-settled-on-590000-hectares-of-ica'),
 'a_jc_tragic': ('Jewish Currents: Argentina\'s Tragic Week', 'https://jewishcurrents.org/argentinas-tragic-week'),
 'a_jvl_uganda': ('Jewish Virtual Library: The Uganda Proposal (1903)', 'https://www.jewishvirtuallibrary.org/the-uganda-proposal-1903'),
 'a_ea_kenya': ('The EastAfrican: Before Israel, Jews considered settling in western Kenya', 'https://theeastafrican.co.ke/tea/magazine/before-israel-jews-considered-settling-in-western-kenya--1340104'),
 'a_unpo_maasai': ('UNPO: Maasai, the background to the land question', 'https://unpo.org/article/7635'),
 'a_wp_ito': ('Wikipedia: Jewish Territorial Organization', 'https://en.wikipedia.org/wiki/Jewish_Territorial_Organization'),
 'a_wp_mandpal': ('Wikipedia: Mandatory Palestine', 'https://en.wikipedia.org/wiki/Mandatory_Palestine'),
 'a_wp_jnf': ('Wikipedia: Jewish National Fund', 'https://en.wikipedia.org/wiki/Jewish_National_Fund'),
 'a_jvl_elarish': ('Jewish Virtual Library: El-Arish, Egypt', 'https://www.jewishvirtuallibrary.org/jsource/vjw/elarish.html'),
 'a_wp_kessler': ('Wikipedia: Leopold Kessler (Zionist), the El Arish expedition of 1903', 'https://en.wikipedia.org/wiki/Leopold_Kessler_(Zionist)'),
 'a_wp_jao': ('Wikipedia: Jewish Autonomous Oblast', 'https://en.wikipedia.org/wiki/Jewish_Autonomous_Oblast'),
 'a_wp_jao_hist': ('Wikipedia: History of the Jews in the Jewish Autonomous Oblast', 'https://en.wikipedia.org/wiki/History_of_the_Jews_in_the_Jewish_Autonomous_Oblast'),
 'a_wp_madagascar': ('Wikipedia: Madagascar Plan', 'https://en.wikipedia.org/wiki/Madagascar_Plan'),
 'a_wp_slattery': ('Wikipedia: Slattery Report', 'https://en.wikipedia.org/wiki/Slattery_Report'),
 'a_jvl_dr': ('Jewish Virtual Library: The Dominican Republic as a haven for Jewish refugees', 'https://www.jewishvirtuallibrary.org/dominican-republic-as-haven-for-jewish-refugees'),
 'a_jvl_sosua': ('Jewish Virtual Library: Sosua', 'https://www.jewishvirtuallibrary.org/jsource/Holocaust/sosua.html'),
 'a_jta_sur47': ('JTA, 31 Jul 1947: Government of Holland approves plan to settle 30,000 homeless Jews in Surinam', 'https://www.jta.org/archive/government-of-holland-approves-plan-to-settle-30000-homeless-jews-in-surinam'),
 'a_jta_sur48a': ('JTA, 18 Apr 1948: Zionist reports Dutch government did not offer haven to 30,000 Jews in Surinam', 'https://www.jta.org/archive/zionist-reports-dutch-government-did-not-offer-haven-to-30000-jews-in-surinam'),
 'a_jta_sur48b': ('JTA, 10 Sep 1948: Governor of Surinam suspends negotiations on admission of Jews', 'https://jta.org/archive/governor-of-surinam-suspends-negotiations-in-admission-of-jews-into-his-territory'),
 'a_wp_scramble': ('Wikipedia: Scramble for Africa', 'https://en.wikipedia.org/wiki/Scramble_for_Africa'),
 'a_cojs_47': ('Center for Online Judaic Studies: British decision to abandon the Mandate, 18 Feb 1947', 'https://cojs.org/british_decision_to_abandon_the_mandate-_feb-_18-_1947/'),
}

ALTS = [
 {'id': 'argentina', 'name': 'Argentina (the Hirsch colonies, from 1891)',
  'facts': [
   ('In Der Judenstaat (14 Feb 1896) Herzl named two possible lands, Argentina and Palestine. Both, he wrote, would fail by slow "infiltration": immigration was pointless without a sovereign right to keep it going.', 'a_wp_judenstaat'),
   ('Baron Maurice de Hirsch founded the Jewish Colonization Association in 1891 to move Jews out of the Russian Empire and settle them as farmers in Argentina; he spent nearly his whole fortune on it. At his death in 1896 there were 6,757 colonists.', 'a_wp_hirsch_arg'),
   ('By 1923 the Association had settled 30,725 people (5,360 families) on 590,000 hectares, more than three times all the land Jews held in Palestine on the eve of statehood (about 173,000 hectares, of which the JNF held 936,000 dunams).', 'a_jta_ica24; a_wp_jnf'),
   ('The colonies peaked at over 20,000 colonists in 1930. Progress was "hampered by insufficient land for extensive cultivation and the unfavorable location of many of the colonies"; by 1966 only 8,000 Jews remained in them.', 'a_jvl_ica'),
   ('Argentina was an independent republic that welcomed European immigrants as citizens. No Argentine government offered self-rule to the colonies, and none was sought.', 'a_wp_judenstaat; a_wp_hirsch_arg'),
   ('January 1919, the Tragic Week in Buenos Aires: during the suppression of a general strike the Argentine Patriotic League singled out the Jewish neighborhood of Once, in what has been called the first pogrom in the Americas.', 'a_jc_tragic'),
  ],
  'share': {
   'money': (0.15, 'Hirsch\'s fortune went to Argentina; nothing documented of the movement\'s later money (Edmond, the Keren Hayesod, the American appeals) would have.'),
   'land': (1.0, 'More land was bought than in all of Palestine; land was not the limit.'),
   'force': (0.05, 'No armed body: the colonists were citizens under Argentine law.'),
   'diplomacy': (0.02, 'No sovereign willing to grant self-rule; Herzl\'s own condition, a sovereign right, never met.'),
   'organization': (0.3, 'The Association organized settlement, but the Zionist Organization never adopted Argentina.'),
   'recognition': (0.0, 'No international process toward a state.'),
  },
  'path': 'A large community of citizens, not a state. That is what happened: farm colonies of up to 20,000 people, most of whose children moved to the cities, inside a Jewish community that became one of the largest in the Americas.',
  'cost': 'No war over sovereignty, because sovereignty never changed hands. There was violence against Jews all the same (the 1919 Tragic Week).'},
 {'id': 'east_africa', 'name': 'British East Africa, the "Uganda" offer (1903)',
  'facts': [
   ('After the Kishinev pogrom, Colonial Secretary Joseph Chamberlain offered land for Jewish settlement in British East Africa: about 16,300 square kilometres of the Uasin Gishu plateau, in what is now Kenya, between Lake Nakuru, Kisumu and Mount Elgon. That is smaller than Mandatory Palestine (about 26,000 square kilometres).', 'a_ea_kenya; a_wp_mandpal'),
   ('26 Aug 1903: the Sixth Zionist Congress voted 295 to 178 only to send a commission to look at it. Herzl presented it as a temporary refuge for Jews in danger in Russia, not a replacement for the Land of Israel.', 'a_jvl_uganda; a_ea_kenya'),
   ('The three-man commission split two to one against it.', 'a_ea_kenya'),
   ('British settlers opposed the plan; the East African Standard denounced "pauper alien Jews" turning the highlands into "Jewganda".', 'a_ea_kenya'),
   ('The plateau was Maasai grazing land. Under agreements of 1904 and 1911 the British moved the Maasai off much of the Rift Valley and the Uasin Gishu to make room for European settlers; over a million acres had been leased or sold by the end of 1905.', 'a_unpo_maasai; a_ea_kenya'),
   ('The Seventh Zionist Congress rejected the offer in 1905. Israel Zangwill led the minority out and founded the Jewish Territorial Organization, which searched for a territory elsewhere (Angola, Galveston and others), found none, and dissolved in 1925; in 1944 Australia vetoed the last such plan, in the Kimberley.', 'a_wp_ito'),
  ],
  'share': {
   'money': (0.1, 'The large sums of the record were raised for Palestine; nothing documented would have followed to East Africa.'),
   'land': (0.3, 'Land offered by the ruling power without purchase, but smaller than Palestine and judged unsuitable by the commission.'),
   'force': (0.2, 'British protection, but no Jewish force and settler hostility.'),
   'diplomacy': (0.6, 'The ruling power made the offer itself; the settlers and the Protectorate\'s officials opposed it.'),
   'organization': (0.3, 'The movement approved only a survey, split over it, and rejected it in 1905.'),
   'recognition': (0.1, 'At most a self-governing settlement under the British crown; no route to statehood on the record.'),
  },
  'path': 'At most a small self-governing settlement under British rule, opposed by the British settlers, on land taken from the Maasai. On the record the movement itself refused it, and those who did go looking for a territory found no ruler willing to give one.',
  'cost': 'Not a peaceful alternative: the land was already the Maasai\'s, and its settlers fought for it.'},
]
ALTS += [
 {'id': 'el_arish', 'name': 'El Arish, northern Sinai (1902-03)',
  'facts': [
   ('In 1902 Herzl met Joseph Chamberlain, and northern Sinai, including the Pelusian Plain, was designated for an autonomous Jewish settlement sponsored by the British government. The idea had been proposed by Davis Trietsch.', 'a_jvl_elarish'),
   ('From 11 February to 25 March 1903 an expedition led by Leopold Kessler, with an agronomist, an architect, the physician of the Palestine colonies, a water engineer and a representative of the Egyptian government, toured the area. Its joint report found that everything depended on water, and recommended diverting some of the Nile.', 'a_wp_kessler'),
   ('Egypt refused, calculating that the plan needed five times the water the engineer had estimated. Lord Cromer, Britain\'s consul-general in Egypt, upheld the refusal even after Herzl narrowed the scheme to the El Arish area and gave up any claim to Nile water.', 'a_wp_kessler; a_jvl_elarish'),
  ],
  'share': {
   'money': (0.1, 'The movement\'s early funds only; none of the later sums.'),
   'land': (0.15, 'Desert land whose settlement depended on water the ruling government would not give.'),
   'force': (0.2, 'British protection, no Jewish force.'),
   'diplomacy': (0.5, 'Britain sponsored it; Egypt, which held the water, refused.'),
   'organization': (0.4, 'Herzl himself pursued it, and the movement\'s experts surveyed it.'),
   'recognition': (0.1, 'An autonomous settlement under British and Egyptian authority, not a state.'),
  },
  'path': 'Refused before it began. Had Egypt agreed, a small autonomous settlement on irrigated land at the edge of Egypt, dependent on Cairo for its water.',
  'cost': 'No settlement, so no conflict on the record; its whole future depended on a neighbour controlling its water.'},
 {'id': 'birobidzhan', 'name': 'Birobidzhan, the Soviet Far East (1928-34)',
  'facts': [
   ('A Soviet decree of 28 March 1928 set aside the territory; on 7 May 1934 it became the Jewish Autonomous Region, with Yiddish as its official language. It covers about 36,271 square kilometres, more than Mandatory Palestine.', 'a_wp_jao; a_wp_jao_hist'),
   ('It was created to show that Soviet Jews, like other Soviet nationalities, could have a territory for cultural autonomy within the socialist state.', 'a_wp_jao_hist'),
   ('Settlement went badly from the start: by October 1928, 49.7 percent of the first settlers had left because of floods, anthrax and harsh conditions. Jews numbered about 20,000 in 1937, 17,695 in 1939 (16 percent of the population), and peaked at about 46,000 to 50,000 in the late 1940s, about a quarter.', 'a_wp_jao'),
   ('By 1959 the Jewish population had fallen to 14,269; the 2021 census counted 837.', 'a_wp_jao'),
  ],
  'share': {
   'money': (0.1, 'Soviet state investment; none of the movement\'s money.'),
   'land': (0.6, 'A territory larger than Palestine, granted by the state that ruled it.'),
   'force': (0.0, 'No Jewish force; Soviet rule.'),
   'diplomacy': (0.3, 'The sovereign granted autonomy, inside the Soviet Union and never toward independence.'),
   'organization': (0.15, 'Soviet institutions only; the Zionist movement had no part in it.'),
   'recognition': (0.0, 'A region of the Soviet Union, never a candidate for statehood.'),
  },
  'path': 'What happened: a Jewish region inside the Soviet Union that never held more than about a quarter Jews and emptied after 1959. The only place where a government actually granted a Jewish territory, and few chose to live there.',
  'cost': 'No war over it; the cost was borne by the settlers in a hard climate under Soviet rule.'},
 {'id': 'madagascar', 'name': 'Madagascar (1937, 1940)',
  'facts': [
   ('The idea of sending Europe\'s Jews to Madagascar came from antisemites, first Paul de Lagarde in 1878. No Jewish organization is documented as seeking it.', 'a_wp_madagascar'),
   ('In 1937 Poland, working with France, sent a commission to the French colony. Its head, Mieczysław Lepecki, estimated 5,000 to 7,000 families could settle there; its Jewish members estimated about 500 families or fewer, because of the climate and the lack of infrastructure.', 'a_wp_madagascar'),
   ('In 1940 Nazi Germany planned to deport about a million Jews a year for four years to the island, to be run by the SS as a police state, expecting many to die. Ian Kershaw calls it genocide by another method. It was shelved after the Battle of Britain left the sea lanes in British hands, and formally in February 1942.', 'a_wp_madagascar'),
  ],
  'share': {
   'money': (0.0, 'None.'),
   'land': (0.05, 'A French colony with its own population; the Jewish members of the 1937 commission judged it able to take about 500 families.'),
   'force': (0.0, 'None.'),
   'diplomacy': (0.0, 'No ruler offered it as a home; France studied it as a place to send Jews, Germany as a place to deport them.'),
   'organization': (0.0, 'No Jewish organization sought it.'),
   'recognition': (0.0, 'None.'),
  },
  'path': 'Not an alternative homeland: a plan by others to remove Jews from Europe. In its 1940 form it was a plan for mass death.',
  'cost': 'Had the Nazi plan been carried out, the record\'s own estimate is that many of the deportees would have died.'},
 {'id': 'alaska', 'name': 'Alaska (1938-40)',
  'facts': [
   ('In November 1938 Interior Secretary Harold Ickes proposed settling European refugees, especially Jews from Germany and Austria, in Alaska; his department\'s report of 1939-40 named four sites, including Baranof Island and the Matanuska-Susitna Valley. Because Alaska was a territory, settlers could have entered outside the normal immigration quotas.', 'a_wp_slattery'),
   ('Senator William King and Representative Franck Havenner introduced a bill. Skagway, Petersburg and Seward endorsed the plan; some opponents called the refugees "Trojan horses".', 'a_wp_slattery'),
   ('Most American Jewish leaders opposed it; Rabbi Stephen Wise said it would give a "wrong and hurtful impression". Roosevelt would accept only 10,000 settlers a year for five years, no more than 10 percent of them Jews, never spoke of it in public, and it died.', 'a_wp_slattery'),
  ],
  'share': {
   'money': (0.1, 'No funding beyond a proposed development corporation.'),
   'land': (0.3, 'Open land in an American territory, at four named sites.'),
   'force': (0.0, 'None; American rule.'),
   'diplomacy': (0.05, 'The President capped Jews at 10 percent of a small quota.'),
   'organization': (0.05, 'Most American Jewish leaders opposed it.'),
   'recognition': (0.0, 'Part of the United States; no route to statehood of its own.'),
  },
  'path': 'At most a few thousand refugees settled as Americans in a territory that became a state of the Union in 1959. A refuge, never a homeland.',
  'cost': 'None in violence; its cost was the refugees it did not save.'},
 {'id': 'dominican', 'name': 'Sosúa, Dominican Republic (1938-44)',
  'facts': [
   ('At the Evian conference of July 1938 the Dominican Republic was the only state to offer to take a large number of refugees, 50,000 to 100,000 Jews. The reported motives of its dictator, Rafael Trujillo, were to repair his image after his army\'s massacre of about 25,000 Haitians in 1937, and to "whiten" the population.', 'a_jvl_dr'),
   ('The Dominican Republic Settlement Association, backed by the Joint Distribution Committee, signed its contract on 30 January 1940; it bought about 26,000 acres at Sosúa, and each settler received 80 acres. The contract guaranteed "full freedom of religion" and protection from persecution.', 'a_jvl_sosua'),
   ('About 50 refugees arrived in the first year and the community peaked at about 500 before the Nazis stopped Jewish emigration in October 1941. Most later left for the United States or Israel; about 25 families remain.', 'a_jvl_sosua; a_jvl_dr'),
  ],
  'share': {
   'money': (0.1, 'The Joint Distribution Committee\'s settlement association.'),
   'land': (0.1, 'About 26,000 acres bought, room for far more than came.'),
   'force': (0.0, 'None; a dictatorship\'s protection.'),
   'diplomacy': (0.2, 'A ruler offered refuge for his own reasons; no self-rule.'),
   'organization': (0.1, 'A relief association, not a national movement.'),
   'recognition': (0.0, 'None.'),
  },
  'path': 'What happened: a refuge of about 500 people that saved lives and ended as a dairy town. A haven under a dictator, not a homeland.',
  'cost': 'No conflict over the land; the offer itself came from a regime that had just massacred its neighbours.'},
 {'id': 'suriname', 'name': 'Suriname (1947-48)',
  'facts': [
   ('In April 1947 the Freeland League, the successor to the territorialists, reached a preliminary agreement in Paramaribo; on 27 June 1947 Suriname\'s Legislative Council voted to accept a plan to settle 30,000 homeless European Jews in an undeveloped area, and the Netherlands government approved it on 3 July.', 'a_jta_sur47'),
   ('The terms were disputed: an American Zionist reported in April 1948 that only about 200 skilled workers had been agreed as a first group, on 75-year leases rather than ownership; the League called this "an absolute distortion", citing the Dutch delegate at the UN and the governor\'s own letter.', 'a_jta_sur48a'),
   ('On 14 August 1948, three months after Israel\'s founding, the governor suspended the talks "in the light of the present international situation".', 'a_jta_sur48b'),
  ],
  'share': {
   'money': (0.1, 'The Freeland League\'s own resources.'),
   'land': (0.3, 'An undeveloped area offered by the governing power, on lease.'),
   'force': (0.0, 'None; Dutch rule.'),
   'diplomacy': (0.3, 'The colony and the Netherlands approved it, then suspended it.'),
   'organization': (0.15, 'The Freeland League, opposed to a Jewish state; the Zionist movement disputed the offer.'),
   'recognition': (0.0, 'A settlement inside a Dutch colony, not a state.'),
  },
  'path': 'At most 30,000 settlers in an autonomous community under Dutch rule, on leased land. Approved by a government, then withdrawn once Israel existed.',
  'cost': 'Peaceful on the record; who lived in the area it targeted is not documented here and would have had to be established.'},
]
PEAK = {'argentina': 'over 20,000 colonists (1930)', 'east_africa': 'none', 'el_arish': 'none', 'birobidzhan': 'about 46,000 to 50,000 Jews (late 1940s)',
        'madagascar': 'none', 'alaska': 'none', 'dominican': 'about 500 (1941)', 'suriname': 'none'}
for _A in ALTS: _A['peak'] = PEAK[_A['id']]
PALESTINE = {'name': 'Palestine (the record)', 'facts': [
  ('About 25,600 to 26,600 square kilometres; in 1945 about 1,061,000 Muslims, 136,000 Christians and 554,000 Jews.', 'a_wp_mandpal'),
  ('The two sides\' positions were an "irreconcilable conflict of principles", Bevin told the Commons on 18 February 1947: the Jews sought a sovereign state, and the Arabs opposed Jewish sovereignty anywhere in Palestine.', 'a_cojs_47')],
  'peak': 'about 630,000 Jews (1947)', 'path': 'The state, founded in 1948, through war.', 'cost': 'A war in 1947-49 and a conflict that has continued since.'}


def chance(share, chans=None):
    k = -math.log(1 - V.CAL); p = 1.0
    for c in (chans or V.CHANNELS): p *= (1 - math.exp(-k * share[c][0])) ** V.EXP[c]
    return round(100 * p, 2)


def main():
    out = []
    ORDER = ['argentina', 'el_arish', 'east_africa', 'birobidzhan', 'madagascar', 'alaska', 'dominican', 'suriname']   # in the order they were raised
    for A in sorted(ALTS, key=lambda a: ORDER.index(a['id'])):
        A = dict(A); A['chance'] = chance(A['share'])
        A['weakest'] = min(V.CHANNELS, key=lambda c: A['share'][c][0])
        A['verdict'] = next(t for cut, key, t in V.VERDICT if A['chance'] >= cut)
        A['share'] = {c: list(v) for c, v in A['share'].items()}
        out.append(A)
    json.dump({'_note': 'Other homelands (Nov 2026). Built by alt_homeland.py; do not edit by hand.', 'alts': out, 'palestine': PALESTINE,
               'sources': {k: list(v) for k, v in S.items()}}, open(os.path.join(HERE, 'alt_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_alt_layer', 'stage': 'rd3', 'topic': 'Other homelands: Argentina (Hirsch colonies) and British East Africa (1903 offer) measured on the same six channels (Nov 2026)',
             'claims': [f for A in ALTS + [PALESTINE] for f, _ in A['facts']], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_alt_layer', 'verified': '2026-11-05', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_alt_layer.json'), 'w'), ensure_ascii=False, indent=1)
    for A in out: print(A['id'], A['chance'], A['verdict'], A['peak'])

if __name__ == '__main__': main()
