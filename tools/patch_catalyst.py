#!/usr/bin/env python3
"""The catalyst reading (27 Nov 2026). The map's usual rule treats money and work as interchangeable: when an early builder is
removed, later builders can outgrow the loss. The catalyst reading adds one rule, applied the same way to every builder:
farm money stands on the land it was planted on, so when a landowner is removed, the share of later farm money that stood on
its land goes too. Shares come from the record:
  private capital 1919-39 -> PICA 0.20: about half of immigrant capital went into citrus groves and farms (63% in the
      Jewish Agency's survey of 1926-32 immigrants, ILO 1934); PICA held 31% of Jewish land in 1929 against 46% held
      privately (Karlinsky, California Dreaming), i.e. about 40% of the land outside the JNF where private farms stood:
      0.5 x 0.4 = 0.20
  Keren Hayesod -> JNF 0.31: 31% of its first 20 years' spending went to colonisation (P£2,924,000 of P£9,340,000,
      JTA 1940), on the JNF's land
  wartime fund drives -> JNF 0.56: $35.5M of the $63.3M the UPA's agencies spent from 1939 to March 1945 went to new
      settlements and land (JTA 1945), on the JNF's land
PICA itself was founded by Edmond de Rothschild in 1924 and paid for by him, so it now goes with him in both readings.
A test removing Edmond's money removes, in the catalyst reading, what the money built: his colonies and PICA.
Writes the page (data and code) and the saved model. Idempotent.

Usage: python3 tools/patch_catalyst.py [road-network.html]"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
BUILDS = [
 ['private_capital_interwar', 'pica', 0.20, 'About half of immigrant capital went into groves and farms; PICA held about 40% of the Jewish land outside the JNF where private farms stood (31% of all Jewish land in 1929).'],
 ['keren_hayesod', 'jnf', 0.31, '31% of the Keren Hayesod\'s spending in its first 20 years went to colonisation on JNF land.'],
 ['wartime_appeals', 'jnf', 0.56, '$35.5 million of the $63.3 million spent from 1939 to March 1945 went to new settlements and land, on JNF land.'],
]
BUILT = {'edmond_r': ['rishon', 'zikhron', 'rosh_pinna', 'mazkeret', 'ekron', 'metulla', 'carmel_wine', 'pica']}

def apply(V):
    if ['pica', 'edmond_r'] not in V['incorp']: V['incorp'].append(['pica', 'edmond_r'])
    V['builds'] = BUILDS; V['built_by'] = BUILT

s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if not D.get('catalyst'):
    apply(D['viab']); D['catalyst'] = True
    s = s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]
S = json.load(open(SNAP, encoding='utf-8'))
if not S.get('catalyst'):
    apply(S['viab']); S['catalyst'] = True; json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False)

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
if 'let vCat=' not in s:
    # the factor each dependent's work keeps: 1 minus the share that stood on removed land
    rep('function vKnockSet(rem){',
        "let vCat=false;\n"
        "function vCatScale(rem){ const sc={}; if(!vCat||!VB.builds) return sc; for(const [dep,base,sh] of VB.builds) if(rem.has(base)&&!rem.has(dep)) sc[dep]=(sc[dep]??1)*(1-sh); return sc; }\n"
        "function vCatRem(rem0){ if(!vCat||!VB.built_by) return rem0; const out=new Set(rem0); for(const [who,list] of Object.entries(VB.built_by)){ const m=VB.edges.filter(e=>e[2]===0&&e[0]===who&&e[4]>0); if(m.length&&m.every(e=>vDrop.has(e[0]+'>'+e[1]))) list.forEach(x=>out.add(x)); } return out; }\n"
        "function vKnockSet(rem){")
    rep('function vScoreBase(rem0){ const rem1=vLost(rem0), rem=vKnockSet(rem1), keep={};',
        'function vScoreBase(rem0){ const rem1=vLost(vCatRem(rem0)), rem=vKnockSet(rem1), keep={}, csc=vCatScale(rem);')
    rep('if(seen.has(f)||seen.has(t)){ cap[c]+=v*(c===5?(_k[f]??1):1);',
        'if(seen.has(f)||seen.has(t)){ cap[c]+=v*(c===5?(_k[f]??1):1)*(csc[f]??1);')
    rep('const years=(vDrop.size||[...rem].some(x=>VB.actors[x]||VB.framework[x]))?vYears(rem,vDrop)',
        'const years=(vDrop.size||Object.keys(csc).length||[...rem].some(x=>VB.actors[x]||VB.framework[x]))?vYears(rem,vDrop,csc)')
    rep('function vYears(rem, drop){', 'function vYears(rem, drop, csc){ csc=csc||{};')
    rep("for(let y=lo;y<=hi;y++){ cap[x][c][y-y0]+=rate; if(!(rem.has(x)||dropped)) live[x][c][y-y0]+=rate; if(!(rem.has(f)||rem.has(t)||dropped)) avail[x][c][y-y0]+=rate; } } });",
        "const ks=csc[f]??1; for(let y=lo;y<=hi;y++){ cap[x][c][y-y0]+=rate; if(!(rem.has(x)||dropped)) live[x][c][y-y0]+=rate*ks; if(!(rem.has(f)||rem.has(t)||dropped)) avail[x][c][y-y0]+=rate*ks; } } });")
    rep('function vRunScenario(t, fn){ const r0=new Set(removed), d0=new Set(vDrop), m0=vMode;',
        'function vRunScenario(t, fn){ const r0=new Set(removed), d0=new Set(vDrop), m0=vMode, c0=vCat; if(t.cat!=null) vCat=t.cat;')
    rep('fl0.forEach(x=>vFlip.add(x)); return out; }\nfunction vTestResults(){', 'fl0.forEach(x=>vFlip.add(x)); vCat=c0; return out; }\nfunction vTestResults(){')
open(P, 'w', encoding='utf-8').write(s)
print('catalyst reading applied')
