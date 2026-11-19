#!/usr/bin/env python3
"""Adds the 1944 vice-presidential swap in detail: the White House meeting of 11 July 1944, Wallace's
trip to China and the Soviet Union (May-July 1944), the adjournment of 20 July, and Wallace's Madison
Square Garden speech of September 1946 and his dismissal. All recorded without weight (they are about
who held the presidency, which the decision model already handles through the successor). Idempotent.
Usage: python3 tools/patch_conv1944.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if any(n['id'] == 'wh_meeting_1944' for n in D['nodes']):
    print('1944 detail already applied'); sys.exit(0)
R = {
 'vpsel': ("Wikipedia, 1944 Democratic Party vice presidential candidate selection", "https://en.wikipedia.org/wiki/1944_Democratic_Party_vice_presidential_candidate_selection"),
 'time44': ("Time, 'U.S. at War: How the Bosses Did It' (31 July 1944)", "https://time.com/archive/6897922/u-s-at-war-how-the-bosses-did-it"),
 'gwu': ("Eleanor Roosevelt Papers Project (George Washington University), Henry Wallace", "https://www2.gwu.edu/~erpapers/teachinger/glossary/wallace-henry.cfm"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026.'
new_nodes = [
 ("wh_meeting_1944", "White House meeting on the running mate (11 July 1944)", "event", "us government", "Party leaders met Roosevelt at the White House and recommended Truman; by one account Roosevelt said 'Bob, I think you and everyone else here want Truman'. A note naming Truman and Douglas followed. No Zionist or Jewish organization is recorded among those present or consulted."),
 ("wallace_trip_1944", "Wallace's mission to China and the Soviet Union (May-July 1944)", "event", "us government", "Roosevelt sent Wallace on a mission to China and Soviet Asia in May 1944; accounts suggest it kept him away while the running mate was being decided. Wallace wrote that Roosevelt 'wanted to ditch me as noiselessly as possible'."),
 ("adjourn_1944", "The adjournment of 20 July 1944", "event", "us government", "With the galleries chanting for Wallace, the chairman, Senator Samuel Jackson, recognized Pittsburgh's mayor, David Lawrence, who moved to adjourn; Jackson ruled 'the ayes have it' over shouts of 'No'. Overnight the leaders lobbied delegates, and Truman was nominated on 21 July on the second ballot. Jackson later wanted his tombstone to say he stopped Wallace becoming president."),
 ("msg_1946", "Wallace's Madison Square Garden speech (Sept 1946)", "event", "us government", "As Secretary of Commerce, Wallace criticized Truman's policy toward the Soviet Union in a speech at Madison Square Garden, New York; he was forced to resign that September. The speech was about the Soviet Union, not Palestine."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [
 ("hannegan", "wh_meeting_1944", "Led the party leaders who met Roosevelt on 11 July 1944 and recommended Truman.", "meeting", "verified", ['vpsel']),
 ("fdr", "wh_meeting_1944", "Agreed to Truman (or Douglas) in a note after the meeting; on 19 July told Hannegan's suite that refusing would 'break up the Democratic Party in the middle of a war'.", "decision", "verified", ['vpsel']),
 ("wh_meeting_1944", "conv1944", "The meeting's choice was carried into the convention.", "decision", "verified", ['vpsel']),
 ("fdr", "wallace_trip_1944", "Sent Wallace to China and the Soviet Union in May 1944.", "assignment", "verified", ['vpsel']),
 ("adjourn_1944", "conv1944", "Session adjourned on 20 July during the Wallace demonstration; Truman nominated the next day, 1,031 votes on the second ballot.", "procedure", "verified", ['vpsel', 'time44']),
 ("wallace", "msg_1946", "Criticized Truman's Soviet policy at Madison Square Garden; forced to resign as Secretary of Commerce that month.", "speech", "verified", ['gwu']),
 ("msg_1946", "truman", "Led to Wallace's dismissal from the cabinet; the break that ended in his 1948 run against Truman.", "dismissal", "verified", ['gwu']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
# tests
anchor = " {id:'fdr_other',"
assert out.count(anchor) == 1
T = r""" {id:'conv_1944', featTag:'Featured test · contingency', q:'What if the convention had not been adjourned on 20 July 1944, and Wallace had been renominated?',
  ids:()=>['truman'],
  what:'The chairman adjourns the session in the middle of the Wallace demonstration, the party leaders work the delegates overnight, and Truman wins the next day. Here the vote goes ahead, Wallace is renominated, and he becomes president when Roosevelt dies in April 1945, taking both American decisions of 1947-48. The same removal as the test without Truman, read from the other end.',
  read:'About 89% on time. On the record Wallace was a supporter: Zionist by his own account since the 1930s, in Palestine with Ben-Gurion and Begin in 1947, and in 1948 attacking Truman for not arming the new state. What changes is who pushed: the personal ties aimed at Truman (Jacobson, Clifford, Niles) fall away, and the State Department\'s resistance stays.'},
 {id:'wallace_doubt', featTag:'Assumption', q:'What if President Wallace had been no supporter, his 1947-48 statements read as campaign positions?',
  ids:()=>['truman'], decider:{us_partition:'other_dem', us_recognition:'other_dem'},
  what:'An assumption, marked as such: Wallace is in office, but his documented support is set aside and he is treated as a president with no recorded position, facing the same State Department resistance and none of Truman\'s personal ties.',
  read:'About 85% on time and about 88% ever, the same as an unknown Democrat. Even read this way the founding is likely: Congress, the Zionist organizations, the UN committee and the money do not depend on who sits in the White House. Only a president bound the other way, as Roosevelt was by his April 1945 pledge to Ibn Saud, lowers it further.'},
"""
out = out.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(out)
print('1944 detail applied')
