"""The historical layer: the Rothschild family tree and houses, the British government around the Balfour Declaration
and the Mandate, San Remo, and the Vatican's documented positions. Writes history_layer.json and
book/research/road_history_layer.json. 'reported' where the cited page states the fact only indirectly."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
S = {
 'h_wp_rfamily': ('Wikipedia: Rothschild family', 'https://en.wikipedia.org/wiki/Rothschild_family'),
 'h_wp_lionel': ('Wikipedia: Lionel de Rothschild', 'https://en.wikipedia.org/wiki/Lionel_de_Rothschild'),
 'h_wp_natty': ('Wikipedia: Nathan Rothschild, 1st Baron Rothschild', 'https://en.wikipedia.org/wiki/Nathan_Rothschild,_1st_Baron_Rothschild'),
 'h_ra_natty': ('The Rothschild Archive family pages: Nathaniel Mayer (Natty) de Rothschild (1840-1915)', 'https://family.rothschildarchive.org/people/61-nathaniel-mayer-natty-de-rothschild-1840-1915'),
 'h_wp_balfour': ('Wikipedia: Balfour Declaration (drafting and approval)', 'https://en.wikipedia.org/wiki/Balfour_Declaration'),
 'h_wp_montagu': ('Wikipedia: Edwin Montagu', 'https://en.wikipedia.org/wiki/Edwin_Montagu'),
 'h_wp_lbj': ('Wikipedia: League of British Jews', 'https://en.wikipedia.org/wiki/League_of_British_Jews'),
 'h_wp_uganda': ('Wikipedia: British Uganda Programme', 'https://en.wikipedia.org/wiki/British_Uganda_Programme'),
 'h_wp_hc': ('Wikipedia: List of high commissioners for Palestine and Transjordan', 'https://en.wikipedia.org/wiki/List_of_high_commissioners_for_Palestine_and_Transjordan'),
 'h_wp_sanremo': ('Wikipedia: San Remo conference (1920)', 'https://en.wikipedia.org/wiki/San_Remo_conference'),
 'h_jvl_vatican': ('Jewish Virtual Library (Encyclopaedia Judaica): Vatican', 'https://www.jewishvirtuallibrary.org/vatican'),
}
V, R = 'verified', 'reported'
E = []
def add(f, t, ty, st, src, lab): E.append((f, t, ty, st, src, lab))
# --- the Rothschild family and houses ---
for son, city, house in [('amschel_m', 'Frankfurt', 'ma_rothschild'), ('salomon_r', 'Vienna', 'sm_rothschild'), ('nathan_r', 'London', 'nm_rothschild'), ('carl_r', 'Naples', 'cm_rothschild'), ('james_mayer', 'Paris', 'rothschild_freres')]:
    add('mayer_amschel', son, 'kinship', V, 'h_wp_rfamily', f'Son of Mayer Amschel Rothschild (1744-1812), court factor to Hesse-Kassel; ran the {city} house.')
    add(son, house, 'leadership', V, 'h_wp_rfamily', f'Head of the {city} house.')
add('cm_rothschild', 'carl_r', 'association', V, 'h_wp_rfamily', 'The Naples house closed in 1863.')
add('nathan_r', 'lionel_r', 'kinship', V, 'h_wp_rfamily', 'Lionel (1808-79), Nathan\'s eldest son, succeeded him in London.')
add('lionel_r', 'nm_rothschild', 'leadership', V, 'h_wp_rfamily', 'Lionel led N M Rothschild & Sons after his father.')
add('nathan_r', 'nathaniel_paris', 'kinship', V, 'h_wp_rfamily', 'Nathaniel (1812-70), Nathan\'s fourth child, moved to Paris.')
add('nathan_r', 'anthony_r', 'kinship', R, 'h_wp_rfamily', 'Anthony (1810-76), 1st Baronet, of Nathan\'s line.')
for c in ['natty', 'alfred_r', 'leopold_r']:
    add('lionel_r', c, 'kinship', V, 'h_wp_lionel', 'Child of Lionel de Rothschild (children: Leonora, Evelina, Nathan Mayer, Alfred Charles, Leopold).')
add('lionel_r', 'parliament', 'membership', V, 'h_wp_lionel', 'Elected for the City of London in 1847; seated 26 July 1858 as the first practising Jew in the Commons, after the Jews Relief Act.')
add('lionel_r', 'uk', 'funding', V, 'h_wp_lionel; h_wp_rfamily', 'The bank under Lionel financed the British government\'s £4M purchase of Egypt\'s Suez Canal shares (1875).')
for c in ['walter_r', 'charles_r']:
    add('natty', c, 'kinship', V, 'h_wp_natty', 'Child of Natty, 1st Baron Rothschild (children: Walter 1868-1937, Evelina, Charles 1877-1923).')
add('natty', 'parliament', 'membership', V, 'h_wp_natty; h_ra_natty', '1885: created Baron Rothschild; the first Jewish member of the Lords who had not converted.')
add('natty', 'nm_rothschild', 'leadership', V, 'h_ra_natty', 'Senior partner of the London house.')
add('charles_r', 'victor_r', 'kinship', R, 'h_wp_rfamily', 'Victor (1910-90), 3rd Baron, of Charles\'s line.')
add('charles_r', 'miriam_r', 'kinship', R, 'h_wp_rfamily', 'Miriam (1908-2005), of Charles\'s line.')
for c in ['alphonse_r', 'gustave_r', 'edmond_r']:
    add('james_mayer', c, 'kinship', V, 'h_wp_rfamily', 'Son of James Mayer de Rothschild of Paris (Alphonse eldest; Edmond youngest).')
add('alphonse_r', 'rothschild_freres', 'leadership', V, 'h_wp_rfamily', 'Alphonse, eldest son, succeeded to the Paris house.')
add('edmond_r', 'james_armand', 'kinship', V, 'h_wp_rfamily', 'James Armand (1878-1957), son of Edmond.')
add('edmond_r', 'maurice_r', 'kinship', R, 'h_wp_rfamily', 'Maurice (1881-1957), of Edmond\'s line.')
add('alphonse_r', 'edouard_r', 'kinship', R, 'h_wp_rfamily', 'Édouard (1868-1949), of Alphonse\'s line.')
add('edouard_r', 'guy_r', 'kinship', R, 'h_wp_rfamily', 'Guy (1909-2007), of Édouard\'s line.')
add('edouard_r', 'rothschild_freres', 'leadership', R, 'h_wp_rfamily', 'Paris house, next generation.')
add('lionel_1882', 'nm_rothschild', 'leadership', V, 'h_wp_rfamily', 'Lionel Nathan (1882-1942) and Anthony Gustav (1887-1961) ran the London bank.')
add('anthony_g', 'nm_rothschild', 'leadership', V, 'h_wp_rfamily', 'Anthony Gustav ran the London bank with Lionel Nathan.')
add('lionel_1882', 'league_bj', 'founding', V, 'h_wp_lbj', 'Nov 1917: co-founder and first president of the League of British Jews.')
add('magnus_p', 'league_bj', 'founding', V, 'h_wp_lbj', 'Sir Philip Magnus, vice-president.')
add('swaythling', 'league_bj', 'founding', V, 'h_wp_lbj', 'Louis Montagu, 2nd Baron Swaythling, vice-president.')
add('league_bj', 'balfour_decl', 'opposition', V, 'h_wp_lbj', 'Anti-Zionist: opposed the declaration and the claim that Jews are a separate nationality.')
add('walter_r', 'balfour', 'correspondence', V, 'h_wp_balfour', '18 July 1917: Walter sent Balfour the 46-word draft formula.')
add('chamberlain_j', 'herzl', 'proposal', V, 'h_wp_uganda', '1902-03: Colonial Secretary Chamberlain, who knew Herzl through the Rothschilds, discussed Cyprus, Sinai and El Arish, then proposed East Africa.')
add('chamberlain_j', 'uganda', 'proposal', V, 'h_wp_uganda', 'The British offer of East African land for Jewish settlement (1903).')
add('lansdowne', 'uganda', 'association', V, 'h_wp_uganda', 'Chamberlain agreed to discuss El Arish with Foreign Secretary Lansdowne.')
add('greenberg_l', 'uganda', 'coordination', V, 'h_wp_uganda', 'Leopold Greenberg, Herzl\'s main negotiator, obtained the Foreign Office letter offering a colony with autonomy.')
add('uganda', 'zionist_congress', 'association', V, 'h_wp_uganda', '1903, Sixth Congress: 295-178 to send a commission to East Africa; Britain withdrew the offer in 1905.')
# --- Whitehall and the Balfour Declaration ---
add('balfour', 'weizmann', 'correspondence', V, 'h_wp_balfour', '19 June 1917: Balfour asked Rothschild and Weizmann for a draft; Weizmann had met him on 22 March.')
add('lloydgeorge', 'war_cabinet', 'leadership', V, 'h_wp_balfour', 'Prime Minister from December 1916; the War Cabinet approved the declaration on 31 Oct 1917.')
add('war_cabinet', 'balfour_decl', 'official act', V, 'h_wp_balfour', '31 Oct 1917: the War Cabinet decision.')
add('milner', 'war_cabinet', 'membership', V, 'h_wp_balfour', 'Lord Milner, War Cabinet minister without portfolio.')
add('milner', 'balfour_decl', 'drafting', V, 'h_wp_balfour', 'His late-August 1917 draft changed the scope to "in Palestine"; co-author of the 4 Oct Milner-Amery draft.')
add('amery', 'balfour_decl', 'drafting', V, 'h_wp_balfour', 'Leo Amery co-drafted the safeguard clauses with Milner (Oct 1917).')
add('ormsby_gore', 'balfour_decl', 'drafting', R, 'h_wp_balfour', 'Claimed co-authorship of the final draft with Amery.')
add('curzon', 'balfour_decl', 'opposition', V, 'h_wp_balfour', '26 Oct 1917: Curzon\'s memorandum questioned what "National Home" would mean.')
add('cecil_r', 'balfour_decl', 'pressure', V, 'h_wp_balfour', 'Under-Secretary Robert Cecil backed the policy by June 1917; 2 Dec 1917: "Judea [is] for the Jews."')
add('graham_r', 'balfour_decl', 'pressure', V, 'h_wp_balfour', 'Ronald Graham of the Foreign Office recorded on 13 June 1917 that the PM, Foreign Secretary and Cecil favoured the policy.')
add('sykes', 'war_cabinet', 'correspondence', V, 'h_wp_balfour', 'Sept 1917: Sykes reported to the War Cabinet after talks with Zionist leaders from Feb 1917.')
add('samuel', 'samuel_memo', 'authorship', V, 'h_wp_balfour', 'Jan 1915: Samuel circulated "The Future of Palestine" to the Cabinet.')
add('asquith', 'uk', 'leadership', V, 'h_wp_balfour', 'Prime Minister until Dec 1916; favoured reform of the Ottoman Empire over partition.')
add('grey_e', 'uk', 'membership', V, 'h_wp_balfour', 'Foreign Secretary under Asquith.')
add('montagu', 'montagu_memo', 'authorship', V, 'h_wp_montagu', '23 Aug 1917: called Zionism "a mischievous political creed" and the declaration antisemitic.')
add('montagu_memo', 'balfour_decl', 'opposition', V, 'h_wp_montagu', 'Montagu\'s opposition modified the declaration\'s terms.')
add('samuel', 'montagu', 'opposition', V, 'h_wp_montagu', 'Cousins on opposite sides: Samuel the moderate Zionist, Montagu the opponent.')
add('montagu', 'swaythling', 'kinship', R, 'h_wp_montagu; h_wp_lbj', 'Edwin was a son of the 1st Baron Swaythling; Louis was the 2nd Baron.')
add('sokolow', 'benedict15', 'meeting', V, 'h_wp_balfour; h_jvl_vatican', '6 May 1917: Benedict XV received Sokolow; per Sokolow\'s notes he expressed general sympathy, stressing the holy places.')
# --- San Remo ---
for p, role in [('lloydgeorge', 'British Prime Minister'), ('curzon', 'Foreign Secretary'), ('hankey', 'secretary to the British delegation'), ('millerand', 'French premier'), ('berthelot', 'French foreign ministry'), ('matsui', 'Japanese ambassador')]:
    add(p, 'san_remo', 'meeting', V, 'h_wp_sanremo', f'19-26 April 1920: {role} at San Remo.')
add('nitti', 'san_remo', 'leadership', V, 'h_wp_sanremo', 'Italian Prime Minister Nitti presided.')
add('millerand', 'france_gov', 'leadership', V, 'h_wp_sanremo', 'President of the French Council of Ministers (1920).')
add('nitti', 'italy_gov', 'leadership', V, 'h_wp_sanremo', 'Prime Minister of Italy (1920).')
add('matsui', 'japan_gov', 'membership', V, 'h_wp_sanremo', 'Japan\'s ambassador.')
add('san_remo', 'mandate', 'official act', V, 'h_wp_sanremo', '25 April 1920: Britain named Mandatory for Palestine, to implement the Balfour Declaration while protecting non-Jewish communities\' civil and religious rights.')
# --- the High Commissioners ---
for p, dates in [('samuel', '1 July 1920 - 30 June 1925'), ('plumer', '25 Aug 1925 - 31 July 1928'), ('luke_h', '(acting) 31 July - 6 Dec 1928'), ('chancellor_j', '6 Dec 1928 - 3 Sept 1931'), ('wauchope', '20 Nov 1931 - 1 Mar 1938'), ('macmichael', '3 Mar 1938 - 30 Aug 1944'), ('gort', '31 Oct 1944 - 5 Nov 1945'), ('cunningham_a', '21 Nov 1945 - 14 May 1948')]:
    add(p, 'mandate_admin', 'leadership', V, 'h_wp_hc', f'High Commissioner for Palestine, {dates}.')
# --- the Vatican ---
add('agliardi', 'herzl', 'meeting', V, 'h_jvl_vatican', '19 May 1896: Herzl proposed extraterritorial status for the holy places to the nuncio in Vienna.')
add('merry_del_val', 'herzl', 'meeting', V, 'h_jvl_vatican', '22 Jan 1904: the Secretary of State told Herzl the holy places could not be separated from the Holy Land.')
add('pius10', 'herzl', 'opposition', V, 'h_jvl_vatican', '25 Jan 1904: "We cannot prevent the Jews from going to Jerusalem but we could never sanction it."')
add('merry_del_val', 'vatican', 'leadership', V, 'h_jvl_vatican', 'Cardinal Secretary of State.')
add('sokolow', 'gasparri', 'meeting', V, 'h_jvl_vatican', 'Apr-May 1917: Gasparri sought a "reserved zone" (Jerusalem, Bethlehem, Nazareth, Tiberias, Jericho).')
add('sokolow', 'pius12', 'meeting', V, 'h_jvl_vatican', '1917: Sokolow met Msgr. Eugenio Pacelli, the future Pius XII.')
add('gasparri', 'vatican', 'leadership', V, 'h_jvl_vatican', 'Cardinal Secretary of State.')
add('gasparri', 'mandate', 'opposition', V, 'h_jvl_vatican', '15 May 1922: note to the League opposing a "privileged and preponderant position" for Jews; 18 Dec 1917 he had opposed a Jewish state.')
add('tardini', 'vatican', 'membership', V, 'h_jvl_vatican', 'Mar 1943: the Holy See "has never approved" making Palestine a Jewish home.')
add('maglione', 'vatican', 'leadership', V, 'h_jvl_vatican', 'May 1943: Cardinal Maglione suggested other territories for a Jewish homeland.')
add('pius12', 'sharett', 'meeting', V, 'h_jvl_vatican', '10 Apr 1945: Pius XII received Shertok but gave no support.')
add('pius12', 'un', 'pressure', V, 'h_jvl_vatican', '1948-49: three encyclicals calling for an internationally guaranteed Jerusalem, a campaign run with France.')
add('vatican', 'res181', 'association', V, 'h_jvl_vatican', '1947: the Holy See avoided interfering, likely to protect the corpus separatum for Jerusalem.')
add('paul6', 'israel_gov', 'meeting', V, 'h_jvl_vatican', '5 Jan 1964: the first papal visit to Israel (no diplomatic relations until 1993-94).')

NOTES = {
 'nm_rothschild': 'London house of the Rothschild bank (Nathan Mayer, then Lionel, Natty, and from the 1910s Lionel Nathan and Anthony Gustav). Documented acts in this map: the Suez Canal shares loan (1875), the London gold fixing at its offices from 1919, and the 1917 address of the Balfour letter to Walter, a family member who was not a partner. Family members were on both sides of Zionism: Walter and Edmond for, Lionel Nathan\'s League of British Jews against.',
}

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    json.dump({'_note': 'Historical layer (Nov 2026). Built by history_layer.py; do not edit by hand.', 'node_notes': NOTES,
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'history_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_history_layer', 'stage': 'rd2', 'topic': 'Historical layer: Rothschild family and houses, Whitehall and the Balfour Declaration, San Remo, High Commissioners, the Vatican (Nov 2026)',
             'claims': [lab for *_, lab in E], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_history_layer', 'verified': '2026-11-04', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_history_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__': main()
