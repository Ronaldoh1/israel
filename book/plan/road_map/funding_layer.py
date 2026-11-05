"""The funding layer: who paid for the Zionist movement and its institutions before 1948, with the sums the
sources state. Writes funding_layer.json and book/research/road_funding_layer.json. 'reported' where the page
states the fact only indirectly. Sums are carried into the removal model by viability.AMOUNT."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
S = {
 'f_wp_herzl': ('Wikipedia: Theodor Herzl', 'https://en.wikipedia.org/wiki/Theodor_Herzl'),
 'f_je_jct': ('Jewish Encyclopedia (1906): Jewish Colonial Trust', 'https://jewishencyclopedia.com/articles/8632-jewish-colonial-trust-the-judische-colonialbank'),
 'f_ws_org': ('Wikisource: Zionism/Organization (after S. Landman, 1915)', 'https://kiwix.lema.org/wikisource_en_all_nopic_2023-08/A/Zionism/Organization'),
 'f_jta_kh33': ('JTA, 10 Feb 1933: U.S. Jews contributed half of K.H. income in decade', 'https://www.jta.org/archive/u-s-jews-contributed-half-of-k-h-income-in-decade'),
 'f_jta_uja46': ('JTA, 1 Dec 1946: UJA raised $102,000,000 in current drive', 'https://jta.org/archive/uja-estimates-needs-for-1947-at-215000000-raised-102000000-in-current-drive'),
 'f_jta_uja48': ('JTA, 3 Jan 1949: United Jewish Appeal raised total of $150,000,000 in 1948', 'https://www.jta.org/archive/united-jewish-appeal-raised-total-of-150000000-in-1948-national-chairmen-report'),
 'f_jta_upa48': ('JTA, 12 Jul 1948: U.S. Jews contributed most of money used for immigration purposes in Palestine', 'https://www.jta.org/archive/u-s-jews-contributed-most-of-monet-used-for-immigration-purposes-in-palestine'),
 'f_jta_baron': ('JTA, 4 Nov 1934: The Baron', 'https://www.jta.org/archive/the-baron'),
 'f_wp_jnf': ('Wikipedia: Jewish National Fund', 'https://en.wikipedia.org/wiki/Jewish_National_Fund'),
 'f_wp_pec': ('Wikipedia: Palestine Economic Corporation', 'https://en.wikipedia.org/wiki/Palestine_Economic_Corporation'),
 'f_wp_hadassah': ('Wikipedia: Hadassah (organization)', 'https://en.wikipedia.org/wiki/Hadassah_(organization)'),
 'f_jta_straus28': ('JTA, 1 Feb 1928: Nathan Straus $100,000 gift for United Palestine Appeal', 'https://www.jta.org/archive/nathan-straus-100000-gift-for-united-palestine-appeal-announced'),
 'f_wk_kofer': ('Wikiwand (Wikipedia): Community ransom (Kofer HaYishuv)', 'https://www.wikiwand.com/en/articles/Community_ransom'),
 'f_jc_roth': ('The Jewish Chronicle: A family that helped build a new nation', 'https://www.thejc.com/news/features/a-family-that-helped-build-a-new-nation-kkakggbe'),
 'f_jvl_conv': ('Jewish Virtual Library: Convention between the U.S. and Great Britain regarding Palestine (1924)', 'https://www.jewishvirtuallibrary.org/convention-between-the-u-s-and-great-britain-regarding-palestine'),
}
V, R = 'verified', 'reported'
E = []
def add(f, t, ty, st, src, lab): E.append((f, t, ty, st, src, lab))
# --- Herzl and the movement's own money ---
add('herzl', 'die_welt', 'funding', V, 'f_wp_herzl', '1897: Herzl founded the Zionist weekly Die Welt in Vienna "at considerable personal expense".')
add('die_welt', 'wzo', 'association', R, 'f_wp_herzl', 'Die Welt was the Zionist newspaper Herzl founded in the year of the first Congress.')
add('herzl', 'hirsch', 'correspondence', V, 'f_wp_herzl', '1895: Herzl corresponded with Baron Maurice de Hirsch, who had founded the JCA in 1891; it "led nowhere".')
add('shekel', 'wzo', 'funding', V, 'f_ws_org', 'Members joined by paying a nominal "shekel" (a shilling, franc or mark); every 200 shekel-payers elected a delegate to the Congress.')
add('jct', 'apc_bank', 'funding', V, 'f_je_jct', 'The Trust, incorporated in London on 20 Mar 1899 with £2 million of capital in £1 shares (applications from over 100,000 shareholders by the end of May 1899), formed the Anglo-Palestine Company in 1902.')
add('wzo', 'jnf', 'founding', V, 'f_wp_jnf', '1901: the Fifth Zionist Congress established the Jewish National Fund, proposed in 1897 by Hermann Schapira; between the wars about a million blue collection boxes stood in Jewish homes.')
# --- the funds and appeals, 1920-1948 ---
add('keren_hayesod', 'jewish_agency', 'funding', V, 'f_jta_kh33', 'April 1921 to July 1932: Keren Hayesod income £4,714,440, about half of it (£2,395,977) from the United States.')
add('uja', 'upa', 'funding', V, 'f_jta_uja46; f_jta_uja48', 'The United Jewish Appeal (from 1939) split each campaign between the United Palestine Appeal, the Joint Distribution Committee and the United Service for New Americans.')
add('upa', 'jewish_agency', 'funding', V, 'f_jta_uja46; f_jta_uja48; f_jta_upa48', 'UPA share of the UJA: $52 million from the 1946 drive and $74.7 million of the record $150 million of 1948; over $125 million was spent in Palestine in 1946-47, more than 73% of it from American Jews.')
add('edmond_r', 'pica', 'funding', V, 'f_jta_baron', 'Edmond "invested over sixty million dollars in Palestine" (JTA, 1934); his PICA then held about half a million dunams, about twice the JNF\'s holdings.')
add('straus_n', 'upa', 'funding', V, 'f_jta_straus28', 'Feb 1928: $100,000 to the United Palestine Appeal for his 80th birthday, directed to the Hadassah Medical Organization.')
add('straus_n', 'hadassah', 'funding', V, 'f_wp_hadassah', '1924: $10,000 for infant welfare stations; a large Straus family gift built the Nathan and Lina Straus Health Center in Jerusalem (cornerstone 1927, opened 1929).')
add('upa', 'hadassah', 'funding', R, 'f_jta_straus28', 'Straus\'s 1928 gift passed through the UPA to the Hadassah Medical Organization.')
add('hadassah', 'yishuv', 'collaboration', R, 'f_wp_hadassah', '1918: Hadassah\'s American Zionist Medical Unit (45 doctors, nurses, dentists and engineers); 9 May 1939: the Rothschild-Hadassah University Hospital on Mount Scopus opened.')
add('yishuv', 'kofer', 'founding', V, 'f_wk_kofer', 'Imposed by the Jewish National Council (Va\'ad Leumi), formally from 24 June 1938.')
add('kofer', 'haganah', 'funding', V, 'f_wk_kofer', '1938-48: a levy on luxuries, cigarettes and restaurant bills to fund central defense and expand the Haganah.')
add('jdc', 'pec_econ', 'funding', V, 'f_wp_pec', 'Feb 1925: the Palestine Economic Corporation was formed by merging the Palestine Co-operative Company with capital from the Joint Distribution Committee.')
# --- what gave the Balfour Declaration force ---
add('us_gov', 'angloam1924', 'signatory', V, 'f_jvl_conv', '3 Dec 1924: the United States and Britain signed the convention on Palestine; Washington read it narrowly, as protecting American interests.')
add('uk', 'angloam1924', 'signatory', V, 'f_jvl_conv', 'Britain, the Mandatory power, was the other party.')
add('angloam1924', 'mandate', 'legal basis', V, 'f_jvl_conv', 'Jewish opinion saw the convention as a "further international guarantee" for the Mandate, which had written the Balfour Declaration into its text.')
add('weizmann', 'walter_r', 'correspondence', V, 'f_jc_roth', 'After the declaration Weizmann wrote that "the name of the greatest House in Jewry was associated with the granting of the Magna Carta of Jewish liberties."')
add('dorothy', 'weizmann', 'correspondence', V, 'f_jc_roth', '1914-16: Weizmann wrote to Dorothy de Rothschild 33 times; through her and James he reached a wider circle of the British establishment.')
add('james_armand', 'balfour_decl', 'pressure', R, 'f_jc_roth', 'James de Rothschild, with his wife Dorothy, was involved in the diplomacy that led to the declaration.')

NOTES = {
 '+herzl': 'How his work was paid for: he founded Die Welt at his own expense (1897); the movement\'s own money came from shekel dues and the Jewish Colonial Trust\'s share sale to over 100,000 small subscribers (1899). Baron de Hirsch, Albert Rothschild of Vienna and Edmond de Rothschild of Paris did not fund his political plan.',
 '+walter_r': 'Head of the English Rothschilds from 1915, when he inherited the title. The Balfour Declaration was addressed to him at 148 Piccadilly; he had worked on its draft with Weizmann. Weizmann wrote afterwards that "the name of the greatest House in Jewry" was now associated with it.',
 '+jnf': 'Founded 1901. By the eve of statehood it had acquired 936,000 dunams, 54% of the land held by Jews; a further 800,000 dunams were held by other Jewish bodies or individuals (Wikipedia).',
 '+upa': 'The Palestine half of American Jewish fundraising: $52 million in 1946 and $74.7 million in 1948 through the United Jewish Appeal.',
 '+uja': 'The joint American campaign from 1939: $102 million in 1946 and a record $150 million in 1948, divided between the UPA, the JDC and the USNA.',
 'angloam1924': 'The treaty by which the United States accepted the British Mandate for Palestine, whose text carried the Balfour Declaration.',
}

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    json.dump({'_note': 'Funding layer (Nov 2026). Built by funding_layer.py; do not edit by hand.', 'node_notes': NOTES,
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'funding_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_funding_layer', 'stage': 'rd2', 'topic': 'Funding layer: Herzl, the shekel and the Jewish Colonial Trust; Keren Hayesod, the UJA and UPA; Edmond de Rothschild; Nathan Straus and Hadassah; Kofer HaYishuv; the 1924 Anglo-American Convention (Nov 2026)',
             'claims': [lab for *_, lab in E], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_funding_layer', 'verified': '2026-11-05', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_funding_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__': main()
