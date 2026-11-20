#!/usr/bin/env python3
"""Pass 12: transfer thinking and displacement before 14 May 1948. Documented ties, all without weight,
because the central questions (whether there was a design, whether a committee existed) are disputed by
named historians; both readings are recorded. Adds the British Labour Party's 1944 resolution and the 1948
'Transfer Committee' (existence disputed). Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if any(n['id'] == 'labour_1944' for n in D['nodes']):
    print('pass 12 already applied'); sys.exit(0)
R = {
 'weitz': ("Wikipedia (via Wikiwand), Yosef Weitz (citing his diary, Masalha, Morris and Karsh)", "https://www.wikiwand.com/en/articles/Yosef_Weitz"),
 'kimche': ("Jon Kimche, 'British Labor's Turnabout on Zionism', Commentary", "https://www.commentary.org/articles/jon-kimche/british-labors-turnabout-on-zionismthe-events-leading-up-to-withdrawal/"),
 'arieli': ("Shaul Arieli, 'A Chronicle of 100 Years of Support for Transfer' (2025)", "https://shaularieli.com/wp-content/uploads/2025/02/A-Chronicle-of-100-Years-of-Support-for-Transfer.pdf"),
 'bg37': ("Wikipedia, 1937 Ben-Gurion letter (citing the JPS translation, Morris, Karsh, Teveth)", "https://en.wikipedia.org/wiki/1937_Ben-Gurion_letter"),
 'khalidi': ("Walid Khalidi, 'Plan Dalet: Master Plan for the Conquest of Palestine', Journal of Palestine Studies (1988)", "https://www.palestine-studies.org/sites/default/files/attachments/jps-articles/Plan%20dalet.pdf"),
 'lockman': ("Zachary Lockman, 'Original Sin', Middle East Report 152 (1988), reviewing Morris", "https://merip.org/1988/05/original-sin"),
 'shlaim': ("Avi Shlaim, 'Israel's \"new history\" and the Palestinians', History News Network", "https://historynewsnetwork.org/article/119484"),
 'dy': ("Wikipedia, Deir Yassin massacre", "https://en.wikipedia.org/wiki/Deir_Yassin_massacre"),
 's745': ("UN document S/745: Arab League cablegram to the UN Secretary-General, 15 May 1948", "https://www.un.org/unispal/?p=214183"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (transfer pass).'
new_nodes = [
 ("labour_1944", "British Labour Party resolution on Palestine (Dec 1944)", "document", "british state", "'Let the Arabs be encouraged to move out of Palestine, as the Jews move in', with handsome compensation, and a re-examination of 'extending the present Palestinian boundaries'. In office from 1945, Labour kept the White Paper limits instead."),
 ("transfer_comm_1948", "'Transfer Committee' (1948)", "event", "zionist movement", "Historians Nur Masalha and Benny Morris describe an unofficial committee of Yosef Weitz, Ezra Danin and Eliyahu Sasson from May 1948; Efraim Karsh writes that Ben-Gurion rejected the idea and that no such committee was ever established. Its existence is disputed."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [
 ("jnf", "weitz", "Weitz joined the JNF in 1932 and directed its land department, overseeing purchases from absentee landlords and the removal of tenant farmers.", "employment", "verified", ['weitz']),
 ("weitz", "transfer_comm_1948", "Diary, 20 Dec 1940: 'There is no room in Palestine for these two peoples... not one village, not one tribe should be left.' In 1948 he spoke of a transfer committee; Masalha and Morris say it met, Karsh that it was never established.", "advocacy (disputed committee)", "reported", ['weitz']),
 ("bengurion", "peel", "His 1937 letter to his son on the Peel plan is read by Morris and others as accepting transfer, and by Karsh and Teveth as mistranslated on that point. Disputed.", "letter (disputed reading)", "reported", ['bg37']),
 ("labour_1944", "bevin", "Labour's 1944 resolution called for Arabs to be 'encouraged to move out'; in office from October 1945 Bevin's government kept the White Paper limits instead.", "reversal", "verified", ['kimche']),
 ("labour_1944", "uk", "A governing party's platform endorsing transfer, one of many such proposals in British and Zionist circles traced by Arieli across a century.", "platform", "verified", ['kimche', 'arieli']),
 ("plan_dalet", "nakba", "Plan D (10 March 1948) provided for the destruction of villages that resisted and the expulsion of their inhabitants; Walid Khalidi reads it as a master plan for conquest and expulsion, Morris as a military plan without a general policy of expulsion. Disputed.", "plan (disputed intent)", "reported", ['khalidi', 'lockman']),
 ("deir_yassin", "nakba", "9 April 1948: Irgun and Lehi forces, with Haganah and Palmach support, attacked Deir Yassin west of Jerusalem and killed villagers; news of it spread and is counted among the causes of flight.", "flight", "reported", ['dy']),
 ("arab_league", "nakba", "Cable to the UN, 15 May 1948: 'approximately over a quarter of a million of the Arab population have been compelled to leave their homes' before the state's declaration.", "count", "verified", ['s745']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('pass 12 applied')
