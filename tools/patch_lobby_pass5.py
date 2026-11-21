#!/usr/bin/env python3
"""Pass 5: lobbying, elections and the money by country. Adds the Keren Hayesod's income by country,
1921-1929; Uruguay's Fabregat and the Latin American bloc at the UN; Guatemala's and Uruguay's places on
UNSCOP; Dewey Stone's and Frank Goldman's call to Eddie Jacobson (March 1948); a second account of
Feinberg's financing of the 1948 train tour. All without weight: the money is already counted in the Keren
Hayesod totals, the votes in the UN vote model, the access in the recognition decision. Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if any(n['id'] == 'kh_1921_29' for n in D['nodes']):
    print('pass 5 already applied'); sys.exit(0)
R = {
 'kh30': ("JTA, 'Keren Hayesod Making Plans to Celebrate 10 Years of Activity This November' (18 July 1930)", "https://www.jta.org/archive/keren-hayesod-making-plans-to-celebrate-10-years-of-activity-this-november"),
 'fab': ("Wikipedia, Enrique Rodríguez Fabregat", "https://en.wikipedia.org/wiki/Enrique_Rodr%C3%ADguez_Fabregat"),
 'unscop': ("Wikipedia, United Nations Special Committee on Palestine", "https://en.wikipedia.org/wiki/United_Nations_Special_Committee_on_Palestine"),
 'jias': ("Journal of Inter-American Studies, 'Latin America and the Palestine Partition Resolution' (Cambridge)", "https://www.cambridge.org/core/journals/journal-of-inter-american-studies/article/latin-america-and-the-palestine-partition-resolution/5C0B5FD52AB7509F638CB9327553C052"),
 'mjl': ("My Jewish Learning, 'A Few Humble Coins and the Making of Israel'", "https://www.myjewishlearning.com/article/a-few-humble-coins-and-the-making-of-israel/"),
 'jps': ("Lawrence Davidson, 'Truman the Politician and the Establishment of Israel', Journal of Palestine Studies", "https://digitalprojects.palestine-studies.org/jps/fulltext/42336"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (lobbying pass).'
new_nodes = [
 ("kh_1921_29", "Keren Hayesod income by country, 1921-1929", "event", "finance", "Worldwide income, 1 April 1921 to 31 December 1929: $20,121,980. United States $10,976,970 (more than half); South Africa $1,505,320; Germany $982,505; Romania $877,645; Great Britain $875,275; Poland $820,550; Canada $737,070; the rest from other countries."),
 ("fabregat", "Enrique Rodríguez Fabregat", "person", "international", "Uruguay's ambassador to the UN (1946-61) and a member of UNSCOP; with García Granados he organized the Latin American states into a voting bloc for partition."),
 ("latam_vote1947", "Latin American votes on partition (29 Nov 1947)", "event", "international", "Of 20 Latin American votes: 13 for; Cuba against; Argentina, Chile, Colombia, El Salvador, Honduras and Mexico abstained. Latin America was a third of the 33 votes for."),
 ("stone_d", "Dewey D. Stone", "person", "us lobby", "Zionist fundraiser who, with Frank Goldman of B'nai B'rith, telephoned Eddie Jacobson in March 1948 to ask him to see Truman."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [
 ("keren_hayesod", "kh_1921_29", "Income by country, 1921-1929: the United States more than half; then South Africa, Germany, Romania, Britain, Poland and Canada.", "income", "verified", ['kh30']),
 ("fabregat", "uruguay", "Uruguay's UN ambassador.", "office", "verified", ['fab']),
 ("fabregat", "unscop", "Member of the committee that recommended partition (seven of eleven members for the majority plan).", "membership", "verified", ['fab', 'unscop']),
 ("granados", "unscop", "Member of the committee; called the Mandate a 'police state'.", "membership", "verified", ['unscop']),
 ("fabregat", "latam_vote1947", "At Abba Eban's request, he and García Granados rallied the Latin American ambassadors into a bloc for partition; the plan 'might not have passed' without it.", "lobbying", "verified", ['fab', 'jias']),
 ("granados", "latam_vote1947", "Credited with Fabregat as leading 'the struggle for a clearly defined partition plan'.", "lobbying", "reported", ['jias']),
 ("eban", "fabregat", "Asked Fabregat to rally the Latin American votes.", "request", "verified", ['fab']),
 ("latam_vote1947", "res181", "13 of the 33 votes for came from Latin America; Cuba voted against and six abstained.", "votes", "verified", ['jias']),
 ("stone_d", "jacobson", "March 1948: with Frank Goldman, telephoned Jacobson to ask him to see Truman on Weizmann's behalf.", "request", "reported", ['mjl']),
 ("feinberg", "truman", "A second account: 'Truman's railroad whistle-stop campaign trip was financed by Jewish businessman Abraham Feinberg', and Truman 'was convinced that in doing so Feinberg made his election possible'.", "money", "reported", ['jps']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('pass 5 applied')
