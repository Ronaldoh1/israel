#!/usr/bin/env python3
"""Counterforces pass, step 2: the opposition's documented acts and the costs of its defeat. Adds the
Arab Higher Committee's boycott of UNSCOP, its outlawing and the deportations of 1937, the revolt's toll
and its outcome in the 1939 White Paper, the Lebanese testimony to UNSCOP, Faisal's reservation, and the
Defense Secretary's and Joint Chiefs' opposition, which joins the resistance in the US partition decision.
Run after patch_counter_sign.py. Idempotent."""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if V.get('counter9'):
    print('counterforces step 2 already applied'); sys.exit(0)
R = {
 'unscop': ("Wikipedia, United Nations Special Committee on Palestine", "https://en.wikipedia.org/wiki/United_Nations_Special_Committee_on_Palestine"),
 'ahc': ("Wikipedia, Arab Higher Committee", "https://en.wikipedia.org/wiki/Arab_Higher_Committee"),
 'osu': ("Origins (Ohio State University), 'The 1936-1939 Arab Revolt in Palestine'", "https://origins.osu.edu/read/1936-1939-arab-revolt-palestine"),
 'fw': ("UNISPAL, Text of the Faisal-Weizmann Agreement (3 Jan 1919)", "https://www.un.org/unispal/document/auto-insert-207006"),
 'jvl': ("Jewish Virtual Library, Truman and the Trusteeship Proposal", "https://www.jewishvirtuallibrary.org/truman-and-the-trusteeship-proposal"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
E = [
 ("ahc", "unscop", "Boycotted the committee (letter of 10 July 1947): the Palestinian Arabs' rights were 'self-evident and could not continue to be subject to investigation'. Some figures, among them Husayn al-Khalidi, met members privately.", "boycott", "verified", ['unscop', 'ahc']),
 ("riad_solh", "unscop", "23 July 1947, at Sofar in Lebanon: the Arab states' case to the committee, an end to Jewish immigration and an Arab government in Palestine.", "testimony", "verified", ['unscop']),
 ("mandate_admin", "ahc", "Outlawed the committee after the assassination of Lewis Andrews (26 Sept 1937); three members deported to the Seychelles; Hajj Amin al-Husseini escaped into exile.", "suppression", "verified", ['ahc']),
 ("revolt36", "wp1939", "The revolt's outcome: Britain issued the 1939 White Paper limiting Jewish immigration to 75,000 over five years and restricting land purchase.", "outcome", "verified", ['osu']),
 ("mandate_admin", "revolt36", "About 5,000 Arabs, 415 Jews and 100 British killed by summer 1939; 20,000 British troops; house demolitions and executions; Arab leaders arrested and expelled and Palestinians disarmed. Historians cite the revolt's defeat as an important reason for the Palestinian defeat in 1948.", "suppression", "verified", ['osu']),
 ("faisal", "weizmann", "3 Jan 1919: Faisal signed the agreement encouraging large-scale Jewish immigration, on condition that the Arabs obtained their independence; otherwise he would 'not be bound by a single word' of it. The condition was not met.", "conditional agreement", "verified", ['fw']),
 ("forrestal", "truman", "Defense Secretary Forrestal was the most outspoken opponent of partition: he complained of party-fund contributions shaping policy and warned in January 1948 of the loss of Middle Eastern oil.", "opposition", "verified", ['jvl']),
 ("jcs", "truman", "The Joint Chiefs feared Soviet participation in any enforcement force and an Arab alignment with Moscow; in February 1948 the President was told enforcement could need 80,000 to 160,000 troops.", "opposition", "verified", ['jvl']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
for d in V['decisions']:
    if d['id'] == 'us_partition':
        for x in ('forrestal', 'jcs'):
            if x not in d['oppose']: d['oppose'].append(x)
V['counter9'] = True
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('counterforces step 2 applied')
