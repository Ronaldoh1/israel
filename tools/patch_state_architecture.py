#!/usr/bin/env python3
"""Adds the architecture of the state after 1948: the deferred constitution (Harari Resolution, 1950),
the state of emergency (19 May 1948, renewed every year since), the undeclared borders, and the
Nation-State Basic Law (2018), alongside the existing Law of Return and UN admission nodes. All without
weight (after the founding). Idempotent.  Usage: python3 tools/patch_state_architecture.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if any(n['id'] == 'harari_1950' for n in D['nodes']):
    print('state architecture already applied'); sys.exit(0)
R = {
 'dick': ("Michael Dickerman, 'The Israeli Constitutional Decision of 1950', The Reconstructionist (BJPA)", "https://www.bjpa.org/content/upload/bjpa/the_/The%20Israeli%20Constitutional%20Decision%20of%201950.pdf"),
 'emer': ("Wikipedia, Israeli state of emergency", "https://en.wikipedia.org/wiki/Israeli_state_of_emergency"),
 'bord': ("JTA, Ben-Gurion's diary remarks just before independence now public", "https://jta.org/archive/ben-gurions-diary-remarks-just-before-independence-now-public"),
 'nsl': ("Times of Israel (via Americans for Peace Now), final text of the Jewish nation-state law (2018)", "https://peacenow.org/entry.php?id=28560"),
 'unc': ("Wikipedia, Uncodified constitution", "https://en.wikipedia.org/wiki/Uncodified_constitution"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (state architecture).'
new_nodes = [
 ("harari_1950", "Harari Resolution: the constitution deferred (13 June 1950)", "document", "israel state", "The Declaration promised a constitution by 1 October 1948; the assembly elected to write it renamed itself the Knesset on 16 February 1949, and in June 1950 resolved that the constitution would be made up of separate Basic Laws, passed one at a time. No full constitution has been adopted. Israel is one of six states with an uncodified constitution, with the United Kingdom, New Zealand, Canada, Saudi Arabia and San Marino."),
 ("emergency_1948", "State of emergency (19 May 1948 to the present)", "document", "israel state", "Declared under the Law and Administration Ordinance of 19 May 1948 and in continuous effect since; renewed by the Knesset every year, since 1992 under Basic Law: The Government, which allows renewal 'without limit'. Emergency regulations can modify ordinary laws. A civil-rights petition of 1999 was dismissed in 2012."),
 ("borders_undeclared", "Borders left undeclared (May 1948)", "document", "israel state", "When asked about borders before independence, Ben-Gurion answered that a state did not have to determine its borders when it was declared; the Declaration names none, and the state's borders have not been fixed in law. The 1949 armistice lines were not borders."),
 ("nation_state_law", "Basic Law: Israel as the Nation-State of the Jewish People (2018)", "document", "israel state", "Passed by the Knesset in July 2018: national self-determination in Israel is 'unique to the Jewish people'."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
E = [
 ("decl_indep", "harari_1950", "Promised a constitution adopted by an elected constituent assembly 'not later than the 1st October 1948'.", "promise", "verified", ['dick']),
 ("knesset", "harari_1950", "The constituent assembly convened on 14 February 1949 and renamed itself the Knesset two days later; it adopted the Harari compromise on 13 June 1950.", "decision", "verified", ['dick']),
 ("bengurion", "harari_1950", "Opposed a written constitution: it would limit the government, and a fight over religion would deepen divisions while the conflict was unresolved.", "position", "verified", ['dick']),
 ("israel_gov", "emergency_1948", "Declared under section 9 of the Law and Administration Ordinance, 19 May 1948; in continuous effect since.", "declaration", "verified", ['emer']),
 ("knesset", "emergency_1948", "Renews the state of emergency every year; Basic Law: The Government allows renewal without limit.", "renewal", "verified", ['emer']),
 ("bengurion", "borders_undeclared", "'When we declare the State we do not have to determine borders nor do we have to seek international recognition.'", "position", "verified", ['bord']),
 ("decl_indep", "borders_undeclared", "The Declaration of 14 May 1948 names no borders.", "omission", "verified", ['bord']),
 ("knesset", "nation_state_law", "Passed July 2018.", "legislation", "verified", ['nsl']),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
for f, t, lab, ty, st, rk in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(out)
print('state architecture applied')
