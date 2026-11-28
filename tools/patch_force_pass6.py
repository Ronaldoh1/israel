#!/usr/bin/env python3
"""Pass 6: outside military training and intelligence. The British-raised Jewish police (from June 1936)
and Wingate's Special Night Squads (1938) trained men who became the Haganah's nucleus and its later
commanders: weighted in the force channel (cap0 raised to match, so the baseline holds; the British state
now carries this share). Recorded without weight: the Haganah's village files, Polish training and rifles
for the Irgun (single source for the totals), the Pan York and Pan Crescent (Dec 1947). Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if any(n['id'] == 'sns' for n in D['nodes']):
    print('pass 6 already applied'); sys.exit(0)
R = {
 'jvl_w': ("Jewish Virtual Library, Charles Orde Wingate", "https://www.jewishvirtuallibrary.org/charles-orde-wingate"),
 'jsp': ("Wikipedia (via Wikiwand), Jewish Supernumerary Police", "https://wikiwand.com/en/Jewish_Supernumerary_Police"),
 'vf': ("Rona Sela, Haaretz, 13 May 2011 (republished by Zochrot): the Haganah's village files", "https://www.zochrot.org/publication_articles/view/56408/en"),
 'wi': ("Warsaw Institute, special report on Polish support for the Irgun, 1938-39", "https://warsawinstitute.org/?p=12678"),
 'pans': ("Jewish Virtual Library, 'Pan Crescent' and 'Pan York' illegal immigration ships", "https://www.jewishvirtuallibrary.org/quot-pan-crescent-quot-and-quot-pan-york-quot-illegal-immigration-ships"),
 'palmach': ("Jewish Virtual Library, The Palmach", "https://www.jewishvirtuallibrary.org/the-palmach"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (military training pass).'
new_nodes = [
 ("sns", "Special Night Squads (1938)", "militia", "militias", "Formed by Captain Orde Wingate of the British Army, 'comprised primarily of Haganah fighters'; tactics of surprise, mobility and night attack. Many of those he trained became heads of the Palmach and later of the Israel Defense Forces."),
 ("notrim", "Jewish Supernumerary Police (from June 1936)", "militia", "militias", "Set up by the British in June 1936 during the Arab revolt and expanded from 6,000 to 14,000 and ultimately 22,000; its mobile branch, the Jewish Settlement Police, from 1938. 'Those trained became the nucleus of the Haganah.'"),
 ("village_files", "Haganah village files (from the early 1940s)", "document", "intelligence", "Files on Arab villages compiled from the beginning of the 1940s by Haganah scouts and later the Shai intelligence service: roads, houses, wells, demography, and military details, with maps and aerial photographs taken despite British bans, catalogued by the Haganah general staff's planning bureau 'in preparation for a future conflict'."),
 ("pans_1947", "Pan York and Pan Crescent (Dec 1947)", "event", "settlement", "Two ships bought in the United States in spring 1947 carried about 15,000 immigrants from Burgas, Bulgaria, on 27 December 1947, after Romania withdrew permission to sail from Constanța; Britain had them interned in Cyprus."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
FC = 'force'
E = [
 ("wingate", "sns", "Created and trained the squads as a British Army officer.", "command", "verified", ['jvl_w'], None, 0),
 ("sns", "haganah", "Trained Haganah fighters in night tactics; many became heads of the Palmach and the Israel Defense Forces.", "training", "verified", ['jvl_w'], FC, 1.0),
 ("mandate_admin", "notrim", "Set up by the Mandate government in June 1936; grew to 22,000.", "founding", "verified", ['jsp'], None, 0),
 ("notrim", "haganah", "'Those trained became the nucleus of the Haganah.'", "training", "verified", ['jsp'], FC, 1.0),
 ("haganah", "village_files", "Compiled by Haganah scouts and the Shai from the early 1940s.", "intelligence", "reported", ['vf'], None, 0),
 ("poland_gov", "irgun", "1938-39: Polish army instructors trained Irgun members (40 in 1938, 25 at Andrychów in 1939, supervised by Avraham Stern); one Polish account puts the rifles sent at about 20,000, part never delivered because of the war. Single source for the totals; not weighted.", "training", "reported", ['wi'], None, 0),
 ("mossad_aliyah", "pans_1947", "Bought in the United States in 1947; about 15,000 passengers.", "operation", "verified", ['pans'], None, 0),
 ("bulgaria", "pans_1947", "Allowed the ships to sail from Burgas, 27 Dec 1947, after Britain agreed they would go to Cyprus.", "permission", "verified", ['pans'], None, 0),
 ("us_gov", "pans_1947", "The United States threatened not to support partition if the Jewish Agency let the ships sail.", "pressure", "verified", ['pans'], None, 0),
 ("pans_1947", "cyprus_camps", "Arrived 31 Dec 1947; passengers interned in Cyprus.", "internment", "verified", ['pans'], None, 0),
 ("palmach", "haganah", "Founded 15-19 May 1941 within the Haganah for fear of a German invasion; more than 2,000 at first; about 7,000 served in the 1948 war; three of the Haganah's twelve brigades.", "force", "verified", ['palmach'], None, 0),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
C = {c: i for i, c in enumerate(V['channels'])}
added = 0
for f, t, lab, ty, st, rk, ch, w in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
    if ch and w:
        V['edges'].append([f, t, C[ch], 1.0, w]); V['eyear'].append([0, 0]); added += w
V['cap0'][C[FC]] = round(V['cap0'][C[FC]] + added, 4)
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('pass 6 applied; force capacity', V['cap0'][C[FC]])
