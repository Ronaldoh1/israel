#!/usr/bin/env python3
"""Pass 3 of the coverage plan: media, information and public campaigns, on both sides. Ties in which a
campaign or public opinion reached a decision-maker are weighted in the legitimacy channel; media and
campaigns with no documented route to a decision are recorded without weight; the opposing campaigns are
recorded now and weighed in the counterforces pass. Idempotent; run after the pass 2 patches.
Usage: python3 tools/patch_media_pass3.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if any(n['id'] == 'wwnd' for n in D['nodes']):
    print('pass 3 already applied'); sys.exit(0)
R = {
 'jta56': ("JTA, Truman reveals his fight with State Dept. over creation of Israel (27 Jan 1956; from his memoirs)", "https://www.jta.org/archive/truman-reveals-his-fight-with-state-dept-over-creation-of-israel"),
 'mew': ("MidEastWeb, US support for the creation of Israel (Truman to Pepper, 17 Oct 1947; Wallace; polling)", "https://www.mideastweb.org/us_supportforstate.htm"),
 'ushmm_wwnd': ("USHMM Holocaust Encyclopedia, The 'We Will Never Die' pageant", "https://encyclopedia.ushmm.org/content/en/article/the-we-will-never-die-pageant"),
 'wiki_jta': ("Wikipedia, Jewish Telegraphic Agency", "https://en.wikipedia.org/wiki/Jewish_Telegraphic_Agency"),
 'jvl_agron': ("Jewish Virtual Library, Gershon Agron", "https://www.jewishvirtuallibrary.org/jsource/biography/Agron.html"),
 'ej_balfour': ("Encyclopedia.com, Balfour Declaration (entries citing Renton and Friedman on the propaganda motive)", "https://encyclopedia.com/history/modern-europe/british-and-irish-history/balfour-declaration"),
 'palquest_ao': ("Interactive Encyclopedia of the Palestine Question, The Arab Office", "https://www.palquest.org/en/node/33728"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (media pass).'
new_nodes = [
 ("wwnd", "'We Will Never Die' pageant (1943)", "event", "us lobby", "Ben Hecht's memorial pageant, sponsored by the Bergson group's Committee for a Jewish Army: Madison Square Garden on 9 March 1943, then Washington, Philadelphia, Chicago, Boston and the Hollywood Bowl; seen by at least 100,000 people. Its subject was the murder of Europe's Jews and the call for rescue, not statehood."),
 ("jta_news", "Jewish Telegraphic Agency (1917)", "media", "zionist movement", "News agency founded by Jacob Landau in The Hague on 6 February 1917; in London from 1919 and New York from 1922; more than 400 Jewish and non-Jewish newspapers subscribed by 1925."),
 ("palestine_post", "Palestine Post (1932)", "media", "zionist movement", "English-language daily founded in Jerusalem in 1932 by Gershon Agron, serving the Yishuv's case with the British authorities and the English-speaking world."),
 ("agron", "Gershon Agron", "person", "zionist movement", "Worked in the Zionist Commission's press office (1920-21), edited the JTA (1921-24), founded the Palestine Post (1932) and headed Israel's government information service (1949-51)."),
 ("us_public_1947", "American public opinion on partition (1947)", "event", "us government", "A late-1947 poll found 65% of Americans in favour of partition; the State Department's Loy Henderson judged that the Zionists had the support of Congress, most of the press and most Americans."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
L = 'legitimacy'
E = [  # f, t, label, type, status, refs, channel, weight
 ("azec", "truman", "Truman wrote that he never had as much 'pressure and propaganda aimed at the White House' as over Palestine; in Oct 1947 he told Senator Pepper he had received about 35,000 pieces of mail on it, and in July 1946 he showed Henry Wallace a sheaf of telegrams 'about four inches thick'.", "pressure", "verified", ['jta56', 'mew'], L, 1.0),
 ("us_public_1947", "truman", "Late 1947: 65% of Americans polled favoured partition; Loy Henderson judged that the Zionists had the support of Congress, most of the press and most Americans.", "public opinion", "reported", ['mew'], L, 1.0),
 ("hecht", "wwnd", "Wrote the pageant.", "authorship", "verified", ['ushmm_wwnd'], None, 0),
 ("bergson", "wwnd", "Sponsored by the Committee for a Jewish Army, led by Peter Bergson.", "sponsorship", "verified", ['ushmm_wwnd'], None, 0),
 ("wwnd", "us_congress", "The Washington performance was attended by more than 200 members of Congress, seven Supreme Court justices and Eleanor Roosevelt. It pressed for rescue, not statehood, so it carries no weight toward the founding.", "public campaign", "verified", ['ushmm_wwnd'], None, 0),
 ("agron", "jta_news", "Edited the agency, 1921-1924.", "employment", "verified", ['jvl_agron'], None, 0),
 ("agron", "palestine_post", "Founded the paper in 1932.", "founding", "verified", ['jvl_agron'], None, 0),
 ("uk", "balfour_decl", "Historians James Renton and Isaiah Friedman argue the Declaration's main purpose was propaganda: to win Jewish sympathy for Britain in the United States and Russia. A claim about motive, disputed, recorded without weight.", "motive (disputed)", "reported", ['ej_balfour'], None, 0),
 ("arab_office", "anglo_am", "1946: the Arab Office presented the Arab case to the Anglo-American Committee, with over a thousand pages of documentation, legal and economic argument and a proposal for a self-governing Palestine with full rights for Jewish citizens. An opposing campaign, to be weighed in the counterforces pass.", "opposition", "verified", ['palquest_ao'], None, 0),
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
V['cap0'][C[L]] = round(V['cap0'][C[L]] + added, 4)
D['viability_meta']['per_channel'][L] = sum(1 for e in V['edges'] if e[2] == C[L])
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('pass 3 applied; legitimacy capacity', V['cap0'][C[L]])
