#!/usr/bin/env python3
"""Pass 11: the Yishuv's own institutions. Adds Ben-Yehuda and the Hebrew revival (Hebrew an official
language under Article 22 of the Mandate), HeHalutz and its training farms, the Elected Assembly and
National Council (1920), the kibbutz movement (Degania, 1909-10), and ties for Hashomer and Mapai. One
weighted tie: the National Council's self-government of the Yishuv (organization channel; cap0 raised so
the baseline holds). Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if any(n['id'] == 'vaad_leumi' for n in D['nodes']):
    print('pass 11 already applied'); sys.exit(0)
R = {
 'mand': ("Mandate for Palestine, 1922, Article 22 (Fordham Modern History Sourcebook)", "https://sourcebooks.web.fordham.edu/mod/1922mandate.asp"),
 'by': ("My Jewish Learning, 'Eliezer Ben-Yehuda and the Making of Modern Hebrew'", "https://www.myjewishlearning.com/article/eliezer-ben-yehuda/"),
 'hh': ("Wikipedia (via Wikiwand), HeHalutz", "https://www.wikiwand.com/en/articles/HeHalutz"),
 'jcm': ("Jewish Virtual Library, The Jewish Community under the Palestine Mandate", "https://jewishvirtuallibrary.org/the-jewish-community-under-the-palestine-mandate"),
 'hs': ("Jewish Virtual Library, Hashomer", "https://www.jewishvirtuallibrary.org/hashomer"),
 'kib': ("Jewish Virtual Library, The Kibbutz and Moshav: History and Overview", "https://www.jewishvirtuallibrary.org/history-and-overview-of-the-kibbutz-movement"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (institutions pass).'
new_nodes = [
 ("ben_yehuda", "Eliezer Ben-Yehuda", "person", "zionist movement", "Arrived in Jerusalem in 1881 and made his the first Modern Hebrew-speaking household; began his dictionary in 1910. He saw Jewish nationalism as both a return to the land and a revival of Hebrew."),
 ("hechalutz", "HeHalutz (pioneer movement)", "institution", "zionist movement", "Founded in 1905 in America and Russia to train young people for agricultural settlement on training farms (hakhsharot). At its peak, 1930-35, it worked in 25 countries; by 1939 about 100,000 members, some 60,000 of whom had already gone to Palestine and 16,000 were in training."),
 ("vaad_leumi", "Elected Assembly and National Council (1920)", "institution", "zionist movement", "Asefat HaNivharim and the Va'ad Leumi, set up in 1920 to run the Jewish community's religious, educational and welfare services: the Yishuv's own government under the Mandate."),
 ("kibbutz_mov", "Kibbutz movement (Degania, 1909-10)", "institution", "settlement", "The first kibbutz, Degania, was founded on Jewish National Fund land about forty years before the state. 82 kibbutzim with 26,550 people by 1940; before statehood the kibbutz took on 'central functions in settlement, immigration, defense and agricultural development'."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [
 ("mandate", "ben_yehuda", "Article 22: 'English, Arabic and Hebrew shall be the official languages of Palestine'; Ben-Yehuda died a month after the recognition.", "official language", "verified", ['mand', 'by'], None, 0),
 ("hechalutz", "yishuv", "About 60,000 members had gone to Palestine by 1939; they are counted in the immigration figures, not again here.", "pioneers", "reported", ['hh'], None, 0),
 ("vaad_leumi", "yishuv", "From 1920 ran the community's religious, educational and welfare services.", "self-government", "reported", ['jcm'], 'organization', 1.0),
 ("hashomer", "haganah", "Founded 1909 (from Bar Giora), never more than 100 members; saw itself as the core of a future army; disbanded when the Haganah was founded in 1920.", "predecessor", "verified", ['hs'], None, 0),
 ("histadrut", "mapai", "Ahdut HaAvoda and HaPoel HaTzair merged into Mapai in 1930; it dominated political life for two generations.", "party", "reported", ['jcm'], None, 0),
 ("jnf", "kibbutz_mov", "Degania was founded on land acquired by the Jewish National Fund.", "land", "verified", ['kib'], None, 0),
 ("kibbutz_mov", "yishuv", "82 kibbutzim, 26,550 people by 1940; central to settlement, immigration and defence before statehood.", "settlement", "verified", ['kib'], None, 0),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
C = {c: i for i, c in enumerate(V['channels'])}
added = 0
for f, t, lab, ty, st, rk, ch, w in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
    if ch and w:
        v = w if st == 'verified' else round(w * 0.6, 4)
        V['edges'].append([f, t, C[ch], 1.0 if st == 'verified' else 0.6, v]); V['eyear'].append([0, 0]); added += v
V['cap0'][C['organization']] = round(V['cap0'][C['organization']] + added, 4)
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
anchor = " {id:'haavara_out',"
assert out.count(anchor) == 1
T = r""" {id:'yishuv_inst', featTag:'Featured test · institutions', q:'What if the Yishuv had built none of its own institutions: no self-government, no Hebrew University or Technion, no Hadassah, no kibbutz movement, no pioneer training?',
  ids:()=>['vaad_leumi','hebrew_univ','technion','hadassah','kibbutz_mov','hechalutz','mapai','hashomer'].filter(x=>N.get(x)),
  what:'The Elected Assembly and National Council, the universities, Hadassah\'s medical work, the kibbutzim, HeHalutz\'s training farms, Mapai and Hashomer. The Histadrut, the Jewish Agency and the Haganah stay.',
  read:'About 88% on time, with about three years of delay. These institutions gave the Yishuv a government, a shared language, universities, medicine and trained settlers before it had a state. On this map they count as organization and money, and the founding still happens because the Jewish Agency, the Histadrut and the Haganah remain. The map measures what decided the founding; what these institutions built was the society the state took over, and that it does not measure.'},
"""
out = out.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(out)
print('pass 11 applied')
