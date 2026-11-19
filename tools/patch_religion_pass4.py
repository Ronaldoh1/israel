#!/usr/bin/env python3
"""Pass 4 of the coverage plan: religious institutions, both sides. Adds the London Jews Society and the
Jerusalem bishopric, the Chief Rabbinate (1921), Reform's Columbus Platform (1937), the status quo letter
(1947), Rabbi Sonnenfeld and the killing of Jacob de Haan (1924). All recorded without weight: none is
documented acting on one of the founding decisions; the opposition is weighed in the counterforces pass.
Idempotent; run after patch_conv1944.py.  Usage: python3 tools/patch_religion_pass4.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if any(n['id'] == 'status_quo_1947' for n in D['nodes']):
    print('pass 4 already applied'); sys.exit(0)
R = {
 'cmj': ("Wikipedia, Church's Ministry Among Jewish People (London Society for Promoting Christianity Amongst the Jews)", "https://en.wikipedia.org/wiki/Church%27s_Ministry_Among_Jewish_People"),
 'bish': ("Wikipedia, Anglo-Prussian bishopric in Jerusalem", "https://en.wikipedia.org/wiki/Anglo-Prussian_bishopric_in_Jerusalem"),
 'kook': ("Wikipedia, Abraham Isaac Kook (Palestine Gazette notice, 1 April 1921)", "https://en.wikipedia.org/wiki/Abraham_Isaac_Kook"),
 'reform': ("Wikipedia, Reform anti-Zionism (Pittsburgh 1885, Columbus 1937, American Council for Judaism 1942)", "https://en.wikipedia.org/wiki/Reform_anti-Zionism"),
 'sq': ("Wikipedia, Status quo (Israel): Ben-Gurion's letter of 19 June 1947", "https://en.wikipedia.org/wiki/Status_quo_(Israel)"),
 'dehaan': ("Wikipedia, Jacob Israël de Haan", "https://en.wikipedia.org/wiki/Jacob_Isra%C3%ABl_de_Haan"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (religion pass).'
new_nodes = [
 ("lsj", "London Society for Promoting Christianity Amongst the Jews (1809)", "organization", "christian zionism", "Founded in 1809 by evangelical Anglicans including William Wilberforce and Charles Simeon; its original agenda included encouraging the physical restoration of the Jewish people to the land. It opened a clinic in Jerusalem in 1836 and built Christ Church, completed in 1849."),
 ("jlm_bishopric", "Anglo-Prussian bishopric in Jerusalem (1841)", "institution", "christian zionism", "A joint see of the Church of England and the Prussian Evangelical Church, proposed by Frederick William IV of Prussia; its first bishop, Michael Solomon Alexander, a former rabbi and a worker of the London Jews Society, was consecrated on 7 November 1841."),
 ("chief_rabbinate", "Chief Rabbinate of Palestine (1921)", "institution", "religion", "Elected by a rabbinical assembly in Jerusalem on 24 February 1921 (Rav Kook and Rabbi Jacob Meir); the Mandate government recognized its council as the sole authority in matters of Jewish law."),
 ("columbus1937", "Columbus Platform of Reform Judaism (1937)", "document", "religion", "Reversed the Pittsburgh Platform of 1885 ('no longer a nation, but a religious community'): it affirmed 'the obligation of all Jewry to aid in its upbuilding as a Jewish homeland'."),
 ("status_quo_1947", "Status quo letter (19 June 1947)", "document", "zionist movement", "Ben-Gurion, for the Jewish Agency Executive, wrote to Agudat Israel four days after the UN committee began its tour, to present a united position: a Jewish day of rest, kosher state kitchens, religious courts for marriage and divorce, and autonomy for religious schools."),
 ("sonnenfeld", "Rabbi Yosef Chaim Sonnenfeld", "person", "religion", "Leader of the Orthodox community of Jerusalem that opposed political Zionism; chose Jacob de Haan to represent its case abroad."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [
 ("lsj", "jlm_bishopric", "Supported the bishopric's creation; its first bishop was one of the Society's workers.", "support", "verified", ['cmj', 'bish']),
 ("mandate_admin", "chief_rabbinate", "1 April 1921 Palestine Gazette: the government recognizes the Council and its courts as 'the sole authorities in matters of Jewish Law'.", "recognition", "verified", ['kook']),
 ("kook", "chief_rabbinate", "Elected the first Ashkenazi Chief Rabbi of Palestine, 24 February 1921; he 'enthusiastically supported the settlement of the land'.", "office", "verified", ['kook']),
 ("reform", "columbus1937", "1937: Reform's rabbis reversed the 1885 position and endorsed aid to a Jewish homeland; Reform rabbis (Wise, Silver) later led the American Zionist Emergency Council.", "reversal", "verified", ['reform']),
 ("columbus1937", "acj", "The American Council for Judaism was founded in 1942 by Reform opponents after the rabbis' conference repudiated its 1935 neutrality on Zionism.", "split", "verified", ['reform']),
 ("bengurion", "status_quo_1947", "Signed the letter as chairman of the Jewish Agency Executive.", "authorship", "verified", ['sq']),
 ("status_quo_1947", "agudah", "Addressed to Agudat Israel, to win a united position before the UN committee; it promised the Sabbath, kosher state kitchens, religious marriage law and school autonomy. A counterforce answered, weighed in the counterforces pass.", "accommodation", "verified", ['sq']),
 ("sonnenfeld", "dehaan", "Chose de Haan as the Orthodox community's representative abroad.", "appointment", "verified", ['dehaan']),
 ("dehaan", "uk", "Lobbied the British authorities against the Zionist leadership; put the Orthodox case to Lord Northcliffe in 1922; planned a July 1924 trip to London with an anti-Zionist delegation.", "opposition", "verified", ['dehaan']),
 ("haganah", "dehaan", "30 June 1924: shot in Jerusalem by Avraham Tehomi, a Haganah member; the Haganah's first commander, Yosef Hecht, testified in 1952 that he and the Jerusalem commander decided on the killing to stop the London plans.", "assassination", "verified", ['dehaan']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('pass 4 applied')
