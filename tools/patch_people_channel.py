#!/usr/bin/env python3
"""Pass 1 of the coverage plan: adds an eighth channel, People (immigration and population), to the
Road to 1948 network map. Idempotent; run after patch_legitimacy_channel.py and patch_legitimacy_tests.py.

Values are thousands of people. Each period of immigration is a node; the actors that let people in carry
the share the record documents (the Mandate government issued the legal certificates; the Haavara transfer
helped about 60,000 German Jews; the clandestine voyages carried about 70,000 after 1942). The channel is
normalized to its own full record, so the baseline and unrelated tests do not move.

Usage: python3 tools/patch_people_channel.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if 'people' in V['channels']:
    print('people channel already applied'); sys.exit(0)
assert 'legitimacy' in V['channels'], 'run the legitimacy patch first'

R = {
 'jvl_table': ("Jewish Virtual Library, Jewish immigration to Palestine, 1919-1941 (from Y. Porath)", "https://www.jewishvirtuallibrary.org/jewish-immigrantion-to-palestine-1919-1941"),
 'jvl_bet': ("Jewish Virtual Library, Aliyah Bet, 1939-1948", "https://www.jewishvirtuallibrary.org/aliyah-bet-1939-1948"),
 'wiki_aliyah': ("Wikipedia, Aliyah (waves before 1948; population 1880 and 1948)", "https://en.wikipedia.org/wiki/Aliyah"),
 'posen': ("Posen Library, The Mass Migration of Jews", "https://www.posenlibrary.com/node/12125"),
 'mandate_text': ("Mandate for Palestine, 1922, Articles 2, 4 and 6 (Fordham Modern History Sourcebook)", "https://sourcebooks.web.fordham.edu/mod/1922mandate.asp"),
 'cojs_limits': ("Center for Online Judaic Studies, British limits on immigration", "https://cojs.org/?p=5028"),
 'jvl_haavara': ("Jewish Virtual Library, Haavara (from Encyclopaedia Judaica)", "https://www.jewishvirtuallibrary.org/haavara"),
 'israeled_1924': ("Center for Israel Education, Restrictive U.S. 1924 Immigration Act boosts Jewish immigration to Palestine", "https://israeled.org/?p=5023"),
 'meyerson_1924': ("Harold Meyerson, The American Prospect, 6 May 2024 (argument that the 1924 Act redirected Jewish emigration)", "https://prospect.org/world/2024-05-06-who-created-israel-palestine-conflict/"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added to the map in November 2026 (people channel); figures in thousands of people.'
nodes = [
 ("old_yishuv", "Jewish community of Palestine before 1882", "population", "yishuv", "About 20,000 to 25,000 Jews lived in Palestine in 1880, mostly in Jerusalem, Safed, Tiberias and Hebron."),
 ("imm_ottoman", "Immigration 1882-1914 (First and Second Aliyot)", "population", "yishuv", "About 60,000 Jews went to Palestine between 1881 and 1914 (Posen Library), under Ottoman rule and often against Ottoman restrictions."),
 ("imm_1919_23", "Immigration 1919-1923 (Third Aliyah)", "population", "yishuv", "35,183 Jewish immigrants under the early Mandate."),
 ("imm_1924_29", "Immigration 1924-1929 (Fourth Aliyah)", "population", "yishuv", "72,594 Jewish immigrants, many from Poland, in the years the United States closed its doors."),
 ("imm_1930_32", "Immigration 1930-1932", "population", "yishuv", "21,552 Jewish immigrants."),
 ("imm_1933_39", "Immigration 1933-1939 (Fifth Aliyah)", "population", "yishuv", "235,170 Jewish immigrants, many from Germany, Austria, Poland and Czechoslovakia; about 60,000 German Jews came with the help of the Haavara transfer."),
 ("imm_1940_41", "Immigration 1940-1941", "population", "yishuv", "15,235 Jewish immigrants under the 1939 White Paper's quota."),
 ("imm_1942_48", "Immigration 1942-1948 (quota and clandestine)", "population", "yishuv", "About 100,000 more, bringing the Mandate total to about 480,000; about 70,000 of the clandestine arrivals came on 66 voyages, most of the rest through the monthly quota."),
 ("us_1924_act", "US Immigration Act of 1924 (Johnson-Reed)", "document", "us government", "Limited immigration from each country to 2% of its US residents in the 1890 census, sharply cutting entry from Eastern and Southern Europe."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in nodes:
    if i in have: continue
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [  # f, t, label, type, status, refs, people (thousands, weighted) or 0 for display only
 ("old_yishuv", "yishuv", "The community before 1882: about 20,000-25,000 people in 1880.", "population", "verified", ['wiki_aliyah'], 24),
 ("imm_ottoman", "yishuv", "About 60,000 immigrants, 1881-1914.", "population", "verified", ['posen', 'wiki_aliyah'], 60),
 ("mandate", "mandate_admin", "Article 6: the Administration 'shall facilitate Jewish immigration under suitable conditions' and encourage close settlement on the land.", "obligation", "verified", ['mandate_text'], 0),
 ("mandate_admin", "imm_1919_23", "Immigration certificates issued under the Mandate, 1919-1923: 35,183 immigrants.", "certificates", "verified", ['jvl_table', 'cojs_limits'], 35.2),
 ("mandate_admin", "imm_1924_29", "Certificates 1924-1929: 72,594 immigrants.", "certificates", "verified", ['jvl_table'], 72.6),
 ("mandate_admin", "imm_1930_32", "Certificates 1930-1932: 21,552 immigrants.", "certificates", "verified", ['jvl_table'], 21.6),
 ("mandate_admin", "imm_1933_39", "Certificates 1933-1939, apart from the Haavara emigrants: about 175,000 immigrants.", "certificates", "verified", ['jvl_table'], 175.2),
 ("haavara", "imm_1933_39", "About 60,000 German Jews reached Palestine with the help of the transfer, 1933-1939.", "emigration", "verified", ['jvl_haavara'], 60),
 ("mandate_admin", "imm_1940_41", "Certificates 1940-1941 under the White Paper quota: 15,235 immigrants.", "certificates", "verified", ['jvl_table'], 15.2),
 ("wp1939", "imm_1940_41", "The 1939 White Paper limited immigration to about 75,000 over five years.", "restriction", "verified", ['cojs_limits'], 0),
 ("mandate_admin", "imm_1942_48", "The monthly quota, 1942-1948: about 30,000 of the period's immigrants.", "certificates", "reported", ['jvl_bet', 'cojs_limits'], 30),
 ("mossad_aliyah", "imm_1942_48", "Clandestine voyages: about 70,000 immigrants on 66 sailings.", "clandestine", "verified", ['jvl_bet'], 70),
 ("us_1924_act", "imm_1924_29", "The 1924 Act's quotas 'kept Jews out' of the US; many Eastern European Jews turned to Palestine instead. One writer argues the share of Jewish emigrants going to Palestine rose from about 3% to 46% by the 1930s.", "redirection", "reported", ['israeled_1924', 'meyerson_1924'], 0),
]
for blk in ["imm_1919_23", "imm_1924_29", "imm_1930_32", "imm_1933_39", "imm_1940_41", "imm_1942_48"]:
    E.append((blk, "yishuv", "The immigrants join the Jewish community of Palestine.", "population", "verified", ['jvl_table'], 0.0001))
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
C = len(V['channels'])
for f, t, lab, ty, st, rk, w in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
    if w:
        V['edges'].append([f, t, C, 1.0 if st == 'verified' else 0.6, w if st == 'verified' else round(w * 0.6, 4)])
        V['eyear'].append([0, 0])
V['channels'].append('people')
V['labels']['people'] = 'People'
V['need']['people'] = 'another source of immigrants on the same scale'
V['exp'].append(1)
V['tbuild'].append(66)
V['tfrom'].append('the first wave of immigration, 1882')
V['cap0'].append(round(sum(e[4] for e in V['edges'] if e[2] == C), 4))
V['norm'].append(V['cal'])
D['viability_meta']['per_channel']['people'] = sum(1 for e in V['edges'] if e[2] == C)
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
for a, b in [("<h4>The seven channels</h4>", "<h4>The eight channels</h4>"),
             ("<h3 class=\"vsec\">The seven channels</h3>", "<h3 class=\"vsec\">The eight channels</h3>")]:
    assert a in out, a
    out = out.replace(a, b)
# central-bank nodes join the map's finance group
gi=out.find('"Finance and banks": [')
assert gi>0
out=out[:gi]+'"Finance and banks": ["reichsbank", "max_warburg", "banque_france", "pcb", '+out[gi+len('"Finance and banks": ['):]
open(P, 'w', encoding='utf-8').write(out)
print('people channel applied; capacity', V['cap0'][-1], 'thousand')
