#!/usr/bin/env python3
"""Adds a seventh channel, Legitimacy (public and political support), to the Road to 1948 network map,
plus central-bank nodes found by a breadth-first search of documented ties. Idempotent.

Design rule: the new channel is normalized to its own full-record value, so the baseline (93.2%) and every
existing result stay exactly as they were unless a removal touches one of the new legitimacy ties.

Usage: python3 tools/patch_legitimacy_channel.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if 'legitimacy' in V['channels']:
    print('legitimacy channel already applied'); sys.exit(0)

R = {  # sources, all checked 18-19 Nov 2026
 'ushmm_harrison': ("The Harrison Report, USHMM Holocaust Encyclopedia", "https://encyclopedia.ushmm.org/content/en/article/the-harrison-report"),
 'ushmm_exodus': ("Exodus 1947, USHMM Holocaust Encyclopedia", "https://encyclopedia.ushmm.org/content/en/article/exodus-1947"),
 'unscop37': ("UNSCOP, summary record of the 37th meeting, Jerusalem, 19 July 1947 (UNISPAL)", "https://www.un.org/unispal/document/auto-insert-186653/"),
 'jta_dp': ("JTA, UNSCOP in final stages; sub-committee reports on European DP camps (Aug 1947)", "https://www.jta.org/archive/unscop-in-final-stages-of-palestine-inquiry-sub-committee-reports-on-european-dp-camps"),
 'cz_uk': ("Wikipedia, Christian Zionism in the United Kingdom", "https://en.wikipedia.org/wiki/Christian_Zionism_in_the_United_Kingdom"),
 'blackstone': ("Wikipedia, Blackstone Memorial", "https://en.wikipedia.org/wiki/Blackstone_Memorial"),
 'lodgefish': ("Wikipedia, Lodge-Fish Resolution", "https://en.wikipedia.org/wiki/Lodge%E2%80%93Fish_Resolution"),
 'jvl_lodgefish': ("Jewish Virtual Library, U.S. Congress endorses the Balfour Declaration", "https://www.jewishvirtuallibrary.org/u-s-congress-endores-the-balfour-declaration"),
 'apc': ("Wikipedia, American Palestine Committee", "https://en.wikipedia.org/wiki/American_Palestine_Committee"),
 'jvl_haavara': ("Jewish Virtual Library, Haavara (from Encyclopaedia Judaica)", "https://www.jewishvirtuallibrary.org/haavara"),
 'jta_1934': ("JTA, Reich controls Jewish funds in Holy Land (10 Aug 1934)", "https://jta.org/archive/reich-controls-jewish-funds-in-holy-land"),
 'jta_1936': ("JTA, Reich turns over operation of transfer pact to Haavara, 2 banks (9 Apr 1936)", "https://www.jta.org/archive/reich-turns-over-operation-of-transfer-pact-to-haavara-2-banks"),
 'jvl_mwarburg': ("Jewish Virtual Library, Warburg, Max M. (from Encyclopaedia Judaica)", "https://www.jewishvirtuallibrary.org/warburg-max-m"),
 'alphonse': ("Wikipedia, Alphonse James de Rothschild", "https://en.wikipedia.org/wiki/Alphonse_James_de_Rothschild"),
 'edouard': ("The Rothschild Archive, Edouard Alphonse James de Rothschild (1868-1949)", "https://family.rothschildarchive.org/people/84-edouard-alphonse-james-de-rothschild-1868-1949"),
 'pal_pound': ("Wikipedia, Palestine pound (Palestine Currency Board)", "https://en.wikipedia.org/wiki/Palestine_pound"),
 'frus48': ("FRUS 1948, vol. V part 2, doc. 48: Ness to Humelsine on Palestine's sterling balances (20 Feb 1948)", "https://history.state.gov/historicaldocuments/frus1948v05p2/d48"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added to the map in November 2026; each tie shows its sources.'
new_nodes = [
 ("holocaust", "The Holocaust (1941-1945)", "event", "europe", "The murder of about six million European Jews by Nazi Germany and its collaborators. In this map it enters only through its documented legitimacy ties: the survivors in the displaced-persons camps and the reports and inquiries about them."),
 ("displaced_persons", "Jewish displaced persons (1945-1948)", "event", "europe", "Jewish survivors in the Allied displaced-persons camps of Germany, Austria and Italy, the subject of the Harrison Report and of visits by the UN's Palestine committee."),
 ("harrison_report", "Harrison Report (Aug 1945)", "document", "us government", "Earl G. Harrison's report on the displaced-persons camps, delivered to Truman on 24 August 1945; it cited the Jewish Agency's request for 100,000 immigration certificates to Palestine."),
 ("reichsbank", "Reichsbank (German central bank)", "institution", "finance", "Germany's central bank. Under the Haavara transfer agreement it supplied about £P2.6 million of the £P8.1 million transferred (Encyclopaedia Judaica), and until April 1936 it handled transactions under the agreement."),
 ("max_warburg", "Max Warburg (1867-1946)", "person", "finance", "Hamburg banker (M. M. Warburg & Co.), appointed to the Reichsbank's General Council in 1924; helped emigrants move capital through the Palestine trust company; his bank ran the German end of the transfer from April 1936; emigrated to New York in 1938. Brother of Paul and Felix Warburg."),
 ("banque_france", "Banque de France", "institution", "europe", "France's central bank. Alphonse de Rothschild was one of its regents from 1855 to 1905; Edouard de Rothschild later sat on its board. No documented tie runs from the bank itself to the Zionist movement."),
 ("pcb", "Palestine Currency Board (1926-1948)", "institution", "british state", "Appointed by the Colonial Secretary in 1926 and based in London; issued the Palestine pound at par with sterling; dissolved in May 1948. In August 1948 the Anglo-Palestine Bank issued Israel's first notes."),
 ("sterling_1948", "Palestine's sterling balances blocked (Feb 1948)", "event", "british state", "On 22 February 1948 the British government blocked Palestine's sterling balances, about £100 million, leaving £7 million for current needs, and took Palestine out of the sterling area."),
]
existing = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in existing, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})

# display ties (all), and which carry weight in the legitimacy channel (c=6).
# Shaftesbury 1839 and Blackstone 1891 carry none: the record states no route from them to the founding bodies.
E = [  # f, t, label, type, status, refs, legit_weight
 ("shaftesbury", "palmerston", "1839: Shaftesbury pressed Foreign Secretary Palmerston to sponsor Jewish settlement in Palestine under British protection; Britain had appointed a consul in Jerusalem in 1838.", "pressure", "verified", ['cz_uk'], 0),
 ("blackstone_1891", "bharrison", "March 1891: the Blackstone Memorial, signed by more than 400 prominent Americans, asked President Harrison to support restoring Palestine to the Jews.", "petition", "verified", ['blackstone'], 0),
 ("blackstone", "wilson", "1916: a second Blackstone Memorial was prepared for President Wilson with Brandeis's support.", "petition", "verified", ['blackstone'], 1.0),
 ("lodge_fish", "balfour_decl", "1922: Congress endorsed the Balfour Declaration's 'national home' by joint resolution, signed by Harding on 21 September.", "endorsement", "verified", ['lodgefish', 'jvl_lodgefish'], 1.0),
 ("apc", "concres1945", "The American Palestine Committee, by the 1940s counting two-thirds of the Senate among 15,000 mostly non-Jewish members, worked with AZEC to secure the 1945 congressional resolution.", "pressure", "verified", ['apc'], 1.0),
 ("ccp", "concres1945", "The Christian Council on Palestine, organized for clergy, supported the 1945 resolution.", "pressure", "verified", ['apc'], 1.0),
 ("holocaust", "displaced_persons", "The Jewish displaced persons of 1945-48 were survivors of the Holocaust.", "consequence", "verified", ['ushmm_harrison'], 1.0),
 ("displaced_persons", "harrison_report", "June-Aug 1945: Earl Harrison visited about 30 camps in Germany and Austria and reported on the Jewish displaced persons.", "report", "verified", ['ushmm_harrison'], 1.0),
 ("harrison_report", "truman", "24 Aug 1945: the report reached Truman, who forwarded it to Attlee and asked Britain to admit 100,000 Jewish displaced persons to Palestine.", "report", "verified", ['ushmm_harrison'], 1.0),
 ("truman", "anglo_am", "Britain set up the Anglo-American Committee of Inquiry to ease the tension after Truman's request; its April 1946 report recommended admitting 100,000.", "pressure", "verified", ['ushmm_harrison'], 1.0),
 ("displaced_persons", "exodus", "The Exodus 1947 carried about 4,500 Holocaust survivors from the camps of Europe.", "consequence", "verified", ['ushmm_exodus'], 1.0),
 ("exodus", "unscop", "19 July 1947: UNSCOP's chairman Sandström and the Yugoslav member Simić went to Haifa to see the Exodus arrive.", "witness", "verified", ['unscop37'], 1.0),
 ("displaced_persons", "unscop", "Aug 1947: three UNSCOP members (Fabregat, Hood, García Granados) toured the displaced-persons camps; their report left the committee 'considerably sobered'.", "witness", "verified", ['jta_dp'], 1.0),
 # central-bank search: documented ties, carrying no extra weight (the Haavara money is already counted in full)
 ("reichsbank", "haavara", "The Reichsbank provided about £P2.6 million of the £P8.1 million transferred under Haavara, 'in coordination with Haavara' (Encyclopaedia Judaica). Already counted inside the Haavara total.", "funding", "verified", ['jvl_haavara'], 0),
 ("reichsbank", "haavara", "Aug 1934: under the transfer terms the Reichsbank kept control of capital transferred to Palestine; property not properly certified passed to it. April 1936: it stopped transacting business under the agreement.", "control", "reported", ['jta_1934', 'jta_1936'], 0),
 ("max_warburg", "reichsbank", "1924: appointed to the Reichsbank's General Council.", "membership", "verified", ['jvl_mwarburg'], 0),
 ("max_warburg", "haavara", "He helped emigrants move capital through the Palestine trust company; from April 1936 the Warburg bank of Hamburg ran the German end of the transfer.", "operation", "verified", ['jvl_mwarburg', 'jta_1936'], 0),
 ("alphonse_r", "banque_france", "1855-1905: a regent of the Banque de France.", "membership", "verified", ['alphonse'], 0),
 ("edouard_r", "banque_france", "Described by the Rothschild Archive as a director of the Bank of France.", "membership", "reported", ['edouard'], 0),
 ("uk", "pcb", "1926: the Colonial Secretary appointed the Palestine Currency Board, based in London; it issued the Palestine pound at par with sterling until May 1948.", "founding", "verified", ['pal_pound'], 0),
 ("uk", "sterling_1948", "22 Feb 1948: Britain blocked Palestine's sterling balances (about £100 million) and took it out of the sterling area.", "official act", "verified", ['frus48'], 0),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk, w in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
    if w:
        V['edges'].append([f, t, 6, 1.0 if st == 'verified' else 0.6, w if st == 'verified' else 0.6])
        V['eyear'].append([0, 0])

V['channels'].append('legitimacy')
V['labels']['legitimacy'] = 'Legitimacy'
V['need']['legitimacy'] = 'another source of public and political support on the same scale'
V['exp'].append(1)
V['tbuild'].append(31)
V['tfrom'].append('the Balfour Declaration, 1917')
V['cap0'].append(round(sum(e[4] for e in V['edges'] if e[2] == 6), 4))
V['norm'] = [1, 1, 1, 1, 1, 1, V['cal']]
V['incorp'] += [['displaced_persons', 'holocaust'], ['harrison_report', 'displaced_persons']]
D['viability_meta']['per_channel']['legitimacy'] = sum(1 for e in V['edges'] if e[2] == 6)

out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
# normalize the legitimacy channel to its own full-record value (baseline and other results unchanged)
code = [
 ("const P=pc.reduce((a,b,i)=>a*Math.pow(b,VB.exp[i]),100)*tau",
  "const P=pc.reduce((a,b,i)=>a*Math.pow(b/((VB.norm&&VB.norm[i])||1),VB.exp[i]),100)*tau"),
 ("const Pat=sh=>sh.reduce((p,x,i)=>p*Math.pow(1-Math.exp(-k*x),VB.exp[i]),1);",
  "const Pat=sh=>sh.reduce((p,x,i)=>p*Math.pow((1-Math.exp(-k*x))/((VB.norm&&VB.norm[i])||1),VB.exp[i]),1);"),
]
for a, b in code:
    assert out.count(a) == 1, a[:50]
    out = out.replace(a, b)
open(P, 'w', encoding='utf-8').write(out)
print('legitimacy channel applied:', len(new_nodes), 'nodes,', len(E), 'ties,', V['cap0'][-1], 'legitimacy capacity')
