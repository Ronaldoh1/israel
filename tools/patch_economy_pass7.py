#!/usr/bin/env python3
"""Pass 7: economy and infrastructure. Adds the Kirkuk-Haifa pipeline (1934-35) and the Haifa refinery
(1939), the Dead Sea concession (1927-30), the Histadrut's economic arm Hevrat ha-Ovdim (1923), the
Second World War economy, and the acetone claim (disputed). All without weight: they explain why Britain
held Palestine and how the Yishuv's economy grew, but none is a documented act on a founding decision, and
the capital they brought is already counted in the money channel. Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if any(n['id'] == 'kirkuk_haifa' for n in D['nodes']):
    print('pass 7 already applied'); sys.exit(0)
R = {
 'pipe': ("Wikipedia, Kirkuk-Haifa oil pipeline", "https://en.wikipedia.org/wiki/Kirkuk%E2%80%93Haifa_oil_pipeline"),
 'ds': ("JTA, 'Novomejski-Tulloch Will Get Dead Sea Concession, British Government Says' (2 Dec 1927)", "https://www.jta.org/archive/novomejski-tulloch-will-get-dead-sea-concession-british-government-says"),
 'hev': ("Encyclopedia.com, Hevrat ha-Ovedim", "https://encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/hevrat-ha-ovedim"),
 'ww2': ("Jewish Agency archive, the Yishuv in the Second World War", "https://archive.jewishagency.org/israel/content/23390"),
 'acet': ("Jewish Virtual Library, History of the Balfour Declaration (explanations 'subject to debate')", "https://www.jewishvirtuallibrary.org/commentary-on-the-balfour-declaration"),
 'acet2': ("Wikipedia, Arthur and the Acetone (the claim as told in Lloyd George's memoirs, 1933)", "https://en.wikipedia.org/wiki/Arthur_and_the_Acetone"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (economy pass).'
new_nodes = [
 ("kirkuk_haifa", "Kirkuk-Haifa oil pipeline (1934-35)", "infrastructure", "british state", "Built 1932-34 by the Iraq Petroleum Company (Anglo-Iranian and Shell each held 23.75%); oil reached Haifa on 14 October 1934; about 27 million barrels in 1935. Considered strategically important by the British government; it fuelled British and American forces in the Mediterranean in the Second World War."),
 ("haifa_refinery", "Haifa refinery (1939)", "infrastructure", "british state", "Production from 29 November 1939; shut on 12 April 1948 after a strike by Arab workers, following the refinery massacre of 30 December 1947."),
 ("dead_sea_conc", "Dead Sea concession (1927-30)", "document", "british state", "Granted in principle in December 1927 to Moshe Novomeysky, a Jewish engineer, and Major Tulloch, a British engineer; leasehold, with the Palestine and Transjordan governments sharing profits; British peers argued for a British company instead."),
 ("hevrat_ovdim", "Hevrat ha-Ovdim (1923)", "organization", "zionist movement", "The Histadrut's economic arm, founded at its second conference in 1923; its holdings included the construction firm Solel Boneh and the workers' bank."),
 ("ww2_economy", "The Yishuv's wartime economy (1939-45)", "event", "economy", "From 10% Jewish unemployment at the start of the war to a long boom from 1942, as industry grew 'at an astonishing rate' to supply the British army; about 30,000 Jews of Palestine enlisted, 4,000 of them women."),
 ("acetone", "Weizmann's acetone work and the 'reward' claim", "event", "zionist movement", "Weizmann's process for producing acetone for British munitions in the First World War. Lloyd George's memoirs (1933) presented the Balfour Declaration as Britain's reward; historians list it as one explanation among several, all 'subject to debate'."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [
 ("uk", "kirkuk_haifa", "Britain's strategic interest: the pipeline's Mediterranean terminal at Haifa, under the Mandate, was 'considered strategically important by the British Government'.", "strategic interest", "verified", ['pipe']),
 ("kirkuk_haifa", "haifa_refinery", "The refinery processed the Kirkuk crude from 1939; by 1944 it could take all the oil the lines delivered.", "supply", "verified", ['pipe']),
 ("uk", "dead_sea_conc", "Granted in principle by the Colonial Office, December 1927.", "concession", "verified", ['ds']),
 ("histadrut", "hevrat_ovdim", "Founded as the Histadrut's economic arm in 1923.", "founding", "reported", ['hev']),
 ("hevrat_ovdim", "solel_boneh", "Solel Boneh was among its holdings.", "ownership", "reported", ['hev']),
 ("uk", "ww2_economy", "British army demand drove the wartime boom; Palestine became a logistic centre for British forces.", "spending", "reported", ['ww2']),
 ("ww2_economy", "yishuv", "Unemployment of 10% disappeared; about 30,000 men and women enlisted in the British army.", "growth", "reported", ['ww2']),
 ("weizmann", "acetone", "His acetone process supplied British munitions in the First World War.", "work", "reported", ['acet']),
 ("acetone", "balfour_decl", "Lloyd George's memoirs presented the Declaration as a reward for the acetone work; historians count it as one explanation among several, all disputed. Recorded without weight.", "motive (disputed)", "reported", ['acet', 'acet2']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('pass 7 applied')
