#!/usr/bin/env python3
"""Pass 8: international bodies and expert reports. Gives documented ties to reports and agreements that
were on the map with leads only: Sykes-Picot (1916), the Hussein-McMahon correspondence, the King-Crane
Commission (1919), the Shaw and Hope Simpson inquiries (1930), the Peel (1937) and Woodhead (1938)
commissions, the Évian conference (1938); and adds H. V. Evatt, chairman of the UN committee that took
partition to the vote. All without weight: the decisions they fed (the Mandate, the White Papers, the UN
vote) already carry their own. Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if any(n['id'] == 'evatt' for n in D['nodes']):
    print('pass 8 already applied'); sys.exit(0)
R = {
 'sp': ("Smithsonian Magazine, 'The Sykes-Picot Agreement'", "https://www.smithsonianmag.com/history/sykes-picot-agreement-180957217/"),
 'kc': ("Encyclopaedia Britannica, King-Crane Commission", "https://www.britannica.com/topic/King-Crane-Commission"),
 'hs': ("Encyclopedia.com, Hope-Simpson Commission (1930)", "https://encyclopedia.com/humanities/encyclopedias-almanacs-transcripts-and-maps/hope-simpson-commission-1930"),
 'peel': ("Wikipedia, Peel Commission", "https://en.wikipedia.org/wiki/Peel_Commission"),
 'ev': ("Wikipedia (via Wikiwand), Évian Conference", "https://www.wikiwand.com/en/articles/Evian_Conference"),
 'evatt': ("Middle East Quarterly, review of a study of H. V. Evatt and the establishment of Israel", "https://www.meforum.org/954/hv-evatt-and-the-establishment-of-israel"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
new_nodes = [
 ("evatt", "H. V. Evatt", "person", "international", "Australia's foreign minister; chairman of the UN General Assembly's Ad Hoc Committee on the Palestinian Question in 1947, which took the partition plan to the vote. Added in November 2026 (international bodies pass)."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note, "mentions": 0, "sections": []})
E = [
 ("sykes", "sykes_picot", "Negotiated with François Georges-Picot, Nov 1915 to Mar 1916; terms set out in Grey's letter to Cambon of 16 May 1916.", "negotiation", "verified", ['sp']),
 ("sykes_picot", "mandate", "Palestine (the 'brown area', less Haifa and Acre) to be under international administration; Britain took the whole under the Mandate instead.", "partition plan", "verified", ['sp']),
 ("sykes_picot", "mcmahon_corr", "Set aside the independent Arab state 'contrary to what had previously been promised' to Sharif Hussein; revealed by the Bolsheviks in 1917.", "contradiction", "verified", ['sp']),
 ("mcmahon", "mcmahon_corr", "British promises of Arab independence to Sharif Hussein in return for revolt against the Ottomans, 1915-16.", "correspondence", "verified", ['sp']),
 ("mcmahon_corr", "hussein_sharif", "Addressed to Hussein; the basis of his revolt.", "promise", "verified", ['sp']),
 ("wilson", "king_crane", "Appointed at Wilson's request at the Paris Peace Conference; toured Syria and Palestine, 10 June to 21 July 1919.", "commission", "verified", ['kc']),
 ("king_crane", "balfour_decl", "72 percent of about 1,875 petitions opposed the Zionist programme; the commission advised 'a serious modification of the Zionist immigration program'. Not acted on. A counterforce.", "opposition", "verified", ['kc']),
 ("shaw", "hopesimpson", "The Shaw report on the 1929 disturbances (March 1930) led to the Hope Simpson inquiry.", "inquiry", "verified", ['hs']),
 ("hopesimpson", "wp1930", "Report of 30 Aug 1930: almost 30 percent of Palestinians landless, attributed to Jewish land purchases; its recommendations went into the Passfield White Paper, reversed by the MacDonald letter.", "report", "verified", ['hs']),
 ("peel", "woodhead", "Peel (7 July 1937) first called the Mandate unworkable and proposed partition, a Jewish state on about a fifth of the country and a population exchange of up to 225,000 Arabs and 1,250 Jews; Woodhead (1938) rejected the plan, and Britain dropped partition in November 1938.", "review", "verified", ['peel']),
 ("zionist_congress", "peel", "20 Aug 1937: rejected Peel's borders but accepted partition as a basis for negotiation, 299 to 160.", "response", "verified", ['peel']),
 ("peel", "res181", "The first official partition proposal; the idea returned in UNSCOP's majority plan of 1947.", "precedent", "verified", ['peel']),
 ("uk", "evian", "6-15 July 1938, 32 countries: Britain and the US agreed beforehand to keep Palestine off the agenda; only the Dominican Republic and later Costa Rica offered to take refugees.", "agenda", "verified", ['ev']),
 ("meir", "evian", "Attended for the Jewish community of Palestine as an observer, not allowed to speak.", "attendance", "verified", ['ev']),
 ("evatt", "australia", "Foreign minister.", "office", "verified", ['evatt']),
 ("evatt", "res181", "As chairman of the Ad Hoc Committee he pushed the partition plan to the vote; the Arab delegations 'felt betrayed'.", "chairmanship", "reported", ['evatt']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('pass 8 applied')
