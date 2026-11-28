#!/usr/bin/env python3
"""Compounding pass on the Road to 1948 map (27 Nov 2026), after the Edmond de Rothschild questions.

Three rules, each applied the same way to every node, and only where a source documents the link:
1. The First and Second Aliyot become two waves. The First (1882-1903, about 25,000 who stayed) and the Second
   (1904-1914, about 35,000) had different causes, and the Second grew out of the First: its workers sought jobs in the
   First Aliyah's colonies and pressed them to hire Jewish labour. Losing a cause of the First now carries on into the
   Second, and from the Second into Hashomer and the Haganah.
2. People keep themselves. A person's cause links (who trained, funded or brought them) weaken that person in
   proportion, but the person counts as one of their own causes, so no one is erased by losing a single patron.
   (Before this, a person with one cause was removed with it; Pinsker without the 1881 pogroms, for example.)
3. A tie made through someone else falls with them: a tie listed in VB.via exists only while the person who made it
   stands (James de Rothschild was introduced to Weizmann by his father, Edmond).
New documented cause links are added for dead-end nodes around the colonies: Zikhron Ya'akov and Edmond to Aaron
Aaronsohn, Aaronsohn to NILI and the Balfour Declaration, the Second Aliyah to Hashomer, Hashomer, Golomb and the
Jewish Legion to the Haganah, BILU and the May Laws to the First Aliyah.
Writes the page (data and code) and the saved model. Idempotent. Usage: python3 tools/patch_compounding.py"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
W = 'https://en.wikipedia.org/wiki/'
FIRST, SECOND, LABOR = W + 'First_Aliyah', W + 'Second_Aliyah', W + 'Hebrew_labor'
AAR, HASH = W + 'Aaron_Aaronsohn', W + 'Hashomer'
RAMAT = 'https://www.ramat-hanadiv.org.il/en/content/generalpage/james-armand-de-rothschild-1878-1957'

MOVE = {('kishinev', 'imm_ottoman'): 'imm_second', ('wzo', 'imm_ottoman'): 'imm_second'}
CAUSES = [
 ['bilu', 'imm_ottoman', 0, 'BILU\'s students were among the first groups of the First Aliyah.', FIRST],
 ['may_laws', 'imm_ottoman', 0, 'The May Laws of 1882 added to the push behind the First Aliyah.', FIRST],
 ['imm_ottoman', 'imm_second', 0, 'The Second Aliyah\'s workers sought year-round jobs in the First Aliyah\'s colonies and pressed them to hire Jewish labour.', LABOR],
 ['imm_second', 'private_capital_interwar', 0, 'It went into the community the Second Aliyah built, Tel Aviv among it.', SECOND],
 ['imm_second', 'hashomer', 0, 'Hashomer\'s founders and most of its members were pioneers of the Second Aliyah.', HASH],
 ['hashomer', 'haganah', 0, 'Hashomer was the precedent for later Jewish defence bodies, and ceased to exist as a separate body when the Haganah was founded in June 1920.', HASH],
 ['golomb', 'haganah', 0, 'Eliyahu Golomb was a founder of the Haganah and led it for many years.', W + 'Eliyahu_Golomb'],
 ['jewish_legion', 'haganah', 0, 'Some of the Legion\'s dismissed soldiers became instructors and commanders in the newly formed Haganah.', W + 'Jewish_Legion'],
 ['zikhron', 'aaronsohn', 0, 'Aaronsohn\'s parents were among the founders of Zikhron Ya\'akov, where he grew up.', AAR],
 ['edmond_r', 'aaronsohn', 0, 'He studied agronomy in France, sponsored by Edmond de Rothschild.', AAR],
 ['aaronsohn', 'nili', 1, 'Aaronsohn founded and led NILI.', AAR],
 ['aaronsohn', 'balfour_decl', 0, 'His efforts helped lead the British government to look favourably on the Zionist cause.', AAR],
]
VIA = [  # tie from, tie to, made through, why, source
 ['james_armand', 'weizmann', 'edmond_r', 'His father, Edmond, introduced him to Chaim Weizmann.', RAMAT],
]

def apply_viab(V, N):
    E, Y = V['edges'], V['eyear']
    if not any(e[0] == 'imm_second' for e in E):
        for j, e in enumerate(E):
            if e[0] == 'imm_ottoman' and e[1] == 'yishuv':
                E[j] = [e[0], e[1], e[2], e[3], 25]; E.insert(j + 1, ['imm_second', 'yishuv', e[2], e[3], 35]); Y.insert(j + 1, list(Y[j])); break
    C = V['causes']
    for c in C:
        if (c[0], c[1]) in MOVE: c[1] = MOVE[(c[0], c[1])]
    seen = {(c[0], c[1]) for c in C}
    for c in CAUSES:
        if (c[0], c[1]) not in seen: C.append(c)
    V['via'] = VIA
    V['self_cause'] = sorted({c[1] for c in C if N.get(c[1], {}).get('kind') == 'person'})

s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
N = {n['id']: n for n in D['nodes']}
for need in ['imm_ottoman', 'aaronsohn', 'nili', 'hashomer', 'haganah', 'golomb', 'jewish_legion', 'zikhron', 'bilu', 'may_laws', 'james_armand', 'weizmann', 'yishuv']:
    assert need in N, need
if 'imm_second' not in N:
    o = N['imm_ottoman']
    o['name'] = 'Immigration 1882-1903 (First Aliyah)'
    o['note'] = ('About 25,000 to 35,000 Jews went to Palestine in the First Aliyah, 1882-1903, under Ottoman rule and often against '
                 'Ottoman restrictions; many left again. They founded the first colonies, most of which Edmond de Rothschild took over '
                 'from 1883. Split from the Second Aliyah in November 2026 (people channel); figures in thousands of people.')
    n2 = dict(o); n2.update(id='imm_second', name='Immigration 1904-1914 (Second Aliyah)', mentions=0, sections=[],
                            note='About 35,000 Jews, mostly from Russia, some from Yemen, went to Palestine between 1904 and 1914. '
                                 'Its workers sought jobs in the First Aliyah\'s colonies; it founded Hashomer and the first kvutzot, and '
                                 'its pioneers led the labour movement. Added in November 2026 (people channel); figures in thousands of people.')
    D['nodes'].insert(D['nodes'].index(o) + 1, n2); N['imm_second'] = n2
    G = D['edges']
    for j, e in enumerate(G):
        if e['f'] == 'imm_ottoman' and e['t'] == 'yishuv':
            e['label'] = 'About 25,000 immigrants who stayed, 1882-1903.'
            e2 = json.loads(json.dumps(e)); e2['f'] = 'imm_second'; e2['label'] = 'About 35,000 immigrants, 1904-1914.'
            e2['refs'] = [{'t': 'Wikipedia, Second Aliyah', 'u': SECOND}]
            e['refs'] = [{'t': 'Wikipedia, First Aliyah', 'u': FIRST}] + e['refs']
            G.insert(j + 1, e2); break
    for e in G:
        if e['f'] == 'kishinev' and e['t'] == 'imm_ottoman': e['t'] = 'imm_second'
apply_viab(D['viab'], N); D['compounding'] = True
s = s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]
S = json.load(open(SNAP, encoding='utf-8'))
apply_viab(S['viab'], N); S['compounding'] = True; json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False)

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]; s = s.replace(a, b)
# rule 2: a person counts as one of their own causes
if 'VB.self_cause' not in s:
    rep("  const g=x=>rem.has(x)?0:(k.has(x)?k.get(x):1); for(let it=0;it<10;it++) for(const [e,cs] of inc){",
        "  for(const p of VB.self_cause||[]) if(inc.has(p)) inc.get(p).push([null,0]);   /* a person keeps themselves: one standing cause of their own */\n"
        "  const g=x=>x===null?1:rem.has(x)?0:(k.has(x)?k.get(x):1); for(let it=0;it<10;it++) for(const [e,cs] of inc){")
# rule 3: a tie made through someone else falls with them
if '_vd=' not in s:
    rep("const _k=keep, seen=vReach(rem),", "const _vd=new Set(vDrop); for(const [f,t,d] of VB.via||[]) if(rem.has(d)) _vd.add(f+'>'+t); const _k=keep, seen=vReach(rem),")
    rep("if(rem.has(f)||rem.has(t)||vDrop.has(f+'>'+t)) continue; if(seen.has(f)||seen.has(t)){ cap[c]+=",
        "if(rem.has(f)||rem.has(t)||_vd.has(f+'>'+t)) continue; if(seen.has(f)||seen.has(t)){ cap[c]+=")
    rep("const years=(vDrop.size||Object.keys(csc).length||[...rem].some(x=>VB.actors[x]||VB.framework[x]))?vYears(rem,vDrop,csc)",
        "const years=(_vd.size||Object.keys(csc).length||[...rem].some(x=>VB.actors[x]||VB.framework[x]))?vYears(rem,_vd,csc)")
# the tests that remove the early immigration take both waves
s = s.replace("ids:()=>['imm_ottoman'],", "ids:()=>['imm_ottoman','imm_second'],")
s = s.replace("ids:['imm_ottoman','imm_1924_29','imm_1933_39']", "ids:['imm_ottoman','imm_second','imm_1924_29','imm_1933_39']")
open(P, 'w', encoding='utf-8').write(s)
print('compounding pass applied:', len(D['viab']['causes']), 'cause links;', len(D['viab']['self_cause']), 'people keep themselves')
