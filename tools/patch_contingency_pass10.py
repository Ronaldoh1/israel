#!/usr/bin/env python3
"""Pass 10: contingency. Documented ties for events outside the movement's control that opened or closed
the path: the Ottoman entry into the First World War (Nov 1914) and the British war aim that followed;
the Kishinev pogrom (1903); Jamal Pasha's wartime deportations; the Farhud (1941); Bevin's referral of
Palestine to the UN (18 Feb 1947). No weight (their effects run through nodes already weighted), plus one
contingency test. Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if "id:'ottoman_neutral'" in s:
    print('pass 10 already applied'); sys.exit(0)
R = {
 'fop': ("Wikipedia, The Future of Palestine (Samuel memorandum, 1915)", "https://en.wikipedia.org/wiki/The_Future_of_Palestine"),
 'kish': ("Wikipedia (via Wikiwand), Kishinev pogrom", "https://wikiwand.com/en/Kishinev_Pogrom"),
 'jamal': ("Uzay Bulut, JNS, 'How Jews in Palestine were persecuted during the 1915 Armenian genocide' (2021)", "https://www.jns.org/opinion/how-jews-in-palestine-were-persecuted-during-the-1915-armenian-genocide/"),
 'farhud': ("USHMM Holocaust Encyclopedia, The Farhud", "https://encyclopedia.ushmm.org/content/en/article/the-farhud"),
 'hansard': ("Hansard, HC Deb 18 February 1947, Palestine Conference (Government Policy)", "https://api.parliament.uk/historic-hansard/commons/1947/feb/18/palestine-conference-government-policy"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
E = [
 ("ottoman", "asquith", "Britain declared war on the Ottoman Empire in early November 1914; on 9 November Asquith said the Ottoman government had 'rung the death knell of Ottoman dominion', making its lands a war aim. Palestine was discussed in Cabinet the same day.", "war", "verified", ['fop']),
 ("lloydgeorge", "samuel", "Lloyd George told Samuel in November 1914 that he was 'very keen to see a Jewish state established in Palestine'.", "encouragement", "verified", ['fop']),
 ("samuel", "samuel_memo", "Drafted from 21 January 1915 and sent to Asquith and Grey: Palestine to be incorporated into the British Empire; Asquith called it 'an almost lyrical outburst'; Lloyd George its only strong supporter in Cabinet.", "authorship", "verified", ['fop']),
 ("russia_imp", "kishinev", "19-21 April 1903: 47 to 49 Jews killed, 92 gravely injured; a second pogrom in October 1905 killed 19.", "pogrom", "verified", ['kish']),
 ("kishinev", "uganda", "Led Herzl to propose the Uganda scheme as a temporary refuge.", "cause", "verified", ['kish']),
 ("kishinev", "jabotinsky", "Jewish self-defence leagues formed after the pogrom; Jabotinsky led early ones, a root of Revisionist Zionism.", "cause", "verified", ['kish']),
 ("kishinev", "imm_ottoman", "Convinced 'tens of thousands of Russian Jews to leave for the West or Palestine'.", "emigration", "verified", ['kish']),
 ("jamal_pasha", "yishuv", "Wartime persecution: about 7,000 Jewish refugees reached Alexandria by early 1915; in April 1917 about 8,000 Jews were expelled from Jaffa within 48 hours.", "deportation", "reported", ['jamal']),
 ("husseini_amin", "rashid_ali", "In Baghdad from October 1939; supported Rashid Ali's pro-German coup of 2 April 1941.", "support", "verified", ['farhud']),
 ("rashid_ali", "farhud", "The coup's collapse was followed by the Farhud, 1-2 June 1941: 128 Jews killed by the official count (150-180 by another estimate); afterwards many young Iraqi Jews turned to Zionism, and in 1943 Iraqi Jews were included in Zionist immigration plans.", "pogrom", "verified", ['farhud']),
 ("bevin", "un", "18 Feb 1947: Britain would refer Palestine to the UN, the Mandate having 'proved to be unworkable in practice'; Britain had no power under the Mandate 'to award the country' and would recommend no solution.", "referral", "verified", ['hansard']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
anchor = " {id:'fdr_other',"
assert out.count(anchor) == 1
T = r""" {id:'ottoman_neutral', featTag:'Assumption · contingency', q:'What if the Ottoman Empire had stayed out of the First World War?',
  ids:()=>['balfour_decl','sykes_picot','san_remo','mandate','mandate_admin','lto_1920','samuel_memo'].filter(x=>N.get(x)),
  what:'An assumption, marked as such: without an Ottoman war there is no British war aim in Palestine, so the 1915 memorandum, Sykes-Picot, the Balfour Declaration, San Remo, the Mandate, its administration and its land law are removed. Everything that did not depend on British rule stays.',
  read:'About 44% on time and about 49% ever: unlikely, with about 26 years lost. This is the largest single contingency on the map, larger than removing the Balfour Declaration alone (about 56%), because without an Ottoman war Britain has no war aim in Palestine and none of the instruments that followed. The chance does not fall to zero: the money, the immigrants already there, the organizations and later the American and Soviet decisions remain.'},
"""
out = out.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(out)
print('pass 10 applied')
