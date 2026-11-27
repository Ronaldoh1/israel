#!/usr/bin/env python3
"""The cause-and-effect reading before 1948 (27 Nov 2026), extending the catalyst reading of tools/patch_catalyst.py.
Each money stream and immigration wave carries its documented causes, the same way the red layer after 1948 does. In this
reading, removing a cause weakens what grew from it: a stream keeps the share of its causes still standing, counted equally;
it is lost when it loses every cause, or a cause it could not exist without. Losses run on down the chain (no Zionist
Organization, no Keren Hayesod; no Keren Hayesod, a weaker United Palestine Appeal). Applied the same way to every cause.
Writes the page (data and code) and the saved model. Idempotent.

Usage: python3 tools/patch_causes.py [road-network.html]"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
W = 'https://en.wikipedia.org/wiki/'
FIRST, SECOND, FOURTH, FIFTH = W + 'First_Aliyah', W + 'Second_Aliyah', W + 'Fourth_Aliyah', W + 'Fifth_Aliyah'
KH = 'https://israeled.org/keren-hayesod-is-founded'
UPA = 'https://www.jta.org/archive/palestine-funds-make-large-gains-in-income-by-consolidation'
CAUSES = [  # cause, effect, could not exist without it (1/0), why, source
 # the first base: the First and Second Aliyot
 ['pogroms_1881', 'imm_ottoman', 0, 'The pogroms after 1881 and the May Laws drove the First Aliyah.', FIRST],
 ['hovevei', 'imm_ottoman', 0, 'Hovevei Zion organised the first groups and their settlement in the colonies.', FIRST],
 ['edmond_r', 'imm_ottoman', 0, 'Edmond took over the failing colonies from 1883 and kept the settlers on the land.', FIRST],
 ['kishinev', 'imm_ottoman', 0, 'The Kishinev pogrom of 1903 began the Second Aliyah.', SECOND],
 ['wzo', 'imm_ottoman', 0, 'The Zionist Organization\'s Palestine Office (1908) settled the Second Aliyah\'s workers.', SECOND],
 # the movement and its funds
 ['herzl', 'wzo', 1, 'Herzl founded the Zionist Organization at the First Congress in 1897.', W + 'Theodor_Herzl'],
 ['dreyfus', 'wzo', 0, 'Herzl traced his turn to a Jewish state to the Dreyfus affair.', W + 'Theodor_Herzl'],
 ['pogroms_1881', 'wzo', 0, 'The Russian pogroms had made the question urgent and built the movement Herzl drew on.', FIRST],
 ['hovevei', 'wzo', 0, 'Hovevei Zion\'s societies were the movement Herzl drew into the Congress.', FIRST],
 ['wzo', 'jnf', 1, 'The Jewish National Fund was founded by the Fifth Zionist Congress in 1901.', W + 'Jewish_National_Fund'],
 ['wzo', 'jnf_collections', 1, 'The fund\'s collections were the Zionist Organization\'s.', W + 'Jewish_National_Fund'],
 ['wzo', 'jct', 1, 'The Jewish Colonial Trust was the Zionist Organization\'s bank (1899).', W + 'Jewish_Colonial_Trust'],
 ['wzo', 'keren_hayesod', 1, 'The Keren Hayesod was launched by the Zionist movement in London in December 1920.', KH],
 ['balfour_decl', 'keren_hayesod', 0, 'It was founded to fulfil the Balfour Declaration\'s promise of a national home.', KH],
 ['wzo', 'jewish_agency', 1, 'The Zionist Organization was the Jewish Agency until 1929 and half of it after.', W + 'Jewish_Agency_for_Israel'],
 ['mandate', 'jewish_agency', 1, 'Article 4 of the Mandate created the Jewish Agency.', W + 'Jewish_Agency_for_Israel'],
 ['keren_hayesod', 'upa', 0, 'The United Palestine Appeal (1925) raised money for the Keren Hayesod and the JNF.', UPA],
 ['jnf', 'upa', 0, 'The United Palestine Appeal raised money for the JNF too.', UPA],
 ['zoa', 'upa', 1, 'It was the American Zionists\' campaign.', UPA],
 ['holocaust', 'upa', 0, 'The appeals of 1946 and 1948 raised record sums after the Holocaust, for its survivors.', W + 'United_Jewish_Appeal'],
 ['upa', 'wartime_appeals', 0, 'The United Palestine Appeal paid for much of the Agency\'s wartime work.', W + 'United_Jewish_Appeal'],
 ['keren_hayesod', 'wartime_appeals', 0, 'So did the Keren Hayesod.', KH],
 ['jewish_agency', 'wartime_appeals', 1, 'The money was the Jewish Agency\'s budget.', W + 'Jewish_Agency_for_Israel'],
 # the immigration waves and the capital they brought
 ['balfour_decl', 'imm_1919_23', 0, 'The Third Aliyah came after the Balfour Declaration opened the way.', W + 'Third_Aliyah'],
 ['mandate', 'imm_1919_23', 0, 'The Mandate administration admitted it.', W + 'Third_Aliyah'],
 ['us_1924_act', 'imm_1924_29', 0, 'The American quotas of 1921 and 1924 turned many Jews leaving Europe towards Palestine.', FOURTH],
 ['mandate', 'imm_1924_29', 0, 'The Mandate administration admitted them.', FOURTH],
 ['nazi_germany', 'imm_1933_39', 0, 'Nazi persecution made the 1930s wave a mass migration.', FIFTH],
 ['mandate', 'imm_1933_39', 0, 'The Mandate administration admitted it.', FIFTH],
 ['mandate', 'private_capital_interwar', 0, 'The capital came with immigrants the Mandate admitted, under a currency and law it set.', FOURTH],
 ['us_1924_act', 'private_capital_interwar', 0, 'The middle-class immigrants of the 1920s, many turned away by the American quotas, brought much of it.', FOURTH],
 ['nazi_germany', 'private_capital_interwar', 0, 'The refugees from Germany brought much of the rest.', FIFTH],
 ['imm_ottoman', 'private_capital_interwar', 0, 'It went into a Jewish community already there: the colonies, their groves and Tel Aviv.', FIRST],
 ['mandate', 'private_capital_war', 0, 'Wartime capital came into the Mandate\'s economy.', W + 'Mandatory_Palestine'],
 ['nazi_germany', 'private_capital_war', 0, 'Much of it was refugee capital.', FIFTH],
 ['pogroms_1881', 'hovevei', 0, 'Hovevei Zion\'s societies spread in response to the pogroms of 1881-82.', W + 'Hovevei_Zion'],
 ['may_laws', 'hovevei', 0, 'The May Laws of 1882 confined Russia\'s Jews further and added to the push.', FIRST],
 ['pogroms_1881', 'bilu', 0, 'BILU was formed by students in Kharkov in 1882 after the pogroms.', FIRST],
 ['may_laws', 'bilu', 0, 'The May Laws added to the push.', FIRST],
 ['pogroms_1881', 'pinsker', 0, 'Pinsker, an assimilationist before 1881, wrote Auto-Emancipation (1882) in response to the pogroms.', W + 'Leon_Pinsker'],
 ['nazi_germany', 'haavara', 1, 'The Haavara was an agreement with the Nazi government.', W + 'Haavara_Agreement'],
 ['wzo', 'haavara', 0, 'Zionist bodies made it, through the Anglo-Palestine Bank.', W + 'Haavara_Agreement'],
]

def apply(V):
    C = V.setdefault('causes', []); seen = {(c[0], c[1]) for c in C}
    for c in CAUSES:
        if (c[0], c[1]) not in seen: C.append(c)

s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
apply(D['viab']); D['causes_pre'] = True
s = s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]
S = json.load(open(SNAP, encoding='utf-8'))
apply(S['viab']); S['causes_pre'] = True; json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False)

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
if 'function vCauseK(' not in s:
    rep('function vKnockSet(rem){',
        "function vCauseK(rem){ const inc=new Map(), k=new Map(); for(const [c,e,nd] of VB.causes||[]){ if(!inc.has(e)) inc.set(e,[]); inc.get(e).push([c,nd]); }\n"
        "  const g=x=>rem.has(x)?0:(k.has(x)?k.get(x):1); for(let it=0;it<10;it++) for(const [e,cs] of inc){ if(rem.has(e)){ k.set(e,0); continue; } let s=0, nd1=1; for(const [c,nd] of cs){ const v=g(c); s+=v; if(nd) nd1=Math.min(nd1,v); } k.set(e,Math.min(nd1,s/cs.length)); }\n"
        "  return k; }\n"
        "function vKnockSet(rem){")
    rep('const rem1=vLost(vCatRem(rem0)), rem=vKnockSet(rem1), keep={}, csc=vCatScale(rem);',
        'const rem1=vLost(vCatRem(rem0)), keep={}; let rem=vKnockSet(rem1); const csc=vCatScale(rem); if(vCat&&VB.causes){ for(const [x,v] of vCauseK(rem)){ if(v<=1e-6) rem.add(x); else if(v<0.9999) csc[x]=(csc[x]??1)*v; } rem=vKnockSet(vLost(rem)); }')
    rep('*(csc[f]??1); ties[c]++;', '*Math.min(csc[f]??1,csc[t]??1); ties[c]++;')
    rep('const ks=csc[f]??1;', 'const ks=Math.min(csc[f]??1,csc[t]??1);')
open(P, 'w', encoding='utf-8').write(s)
print('cause-and-effect reading applied')
