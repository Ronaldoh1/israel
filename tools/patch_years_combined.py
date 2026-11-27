#!/usr/bin/env python3
"""Years of work lost, counted across all channels together (27 Nov 2026). The year model used to take, each year, the
worst-hit single channel, and ignored a channel until it reached 5% of its 1948 size. Both distorted the founding era:
the 5% rule wiped out 1882-86, when Edmond de Rothschild was nearly the whole effort; dropping it let one tiny channel
decide whole years (removing Aaron Aaronsohn's NILI spy ring counted as losing all of 1909-19, because NILI was the only
force on the map then). Now each year's loss is the share of the movement's total work, all channels together, that is
gone: each channel's work counted against its own 1948 size and weighted as in the score (money counts double). Writes
the page. Idempotent.

Usage: python3 tools/patch_years_combined.py [road-network.html]"""
import os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
s = open(P, encoding='utf-8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
if 'VB.ycomb' not in s:
    rep("if(S[k]>0&&S[k]>=material*Sfin[k]){ F[k]=VB.stock===false?0:Math.min(1,D[k]/S[k]); for(const a in Da) if(Da[a][k]>0) who[a].yk[k]=(who[a].yk[k]||0)+Da[a][k]/S[k]; } }",
        "if(!VB.ycomb&&S[k]>0&&S[k]>=material*Sfin[k]){ F[k]=VB.stock===false?0:Math.min(1,D[k]/S[k]); for(const a in Da) if(Da[a][k]>0) who[a].yk[k]=(who[a].yk[k]||0)+Da[a][k]/S[k]; } }\n"
        "    if(VB.ycomb&&VB.stock!==false){ let num=0, den=0; const wk=k=>(VB.exp[k]||1)/(Sfin[k]||1); for(const k of VB.year_ch){ num+=wk(k)*D[k]; den+=wk(k)*S[k]; }\n"
        "      if(den>0){ const fc=Math.min(1,num/den); for(const k of VB.year_ch){ F[k]=0; for(const a in Da) if(Da[a][k]>0) who[a].yk[k]=(who[a].yk[k]||0)+wk(k)*Da[a][k]/den; } F[VB.year_ch[0]]=fc; } }")
    # a removed actor's years: all its channels together
    rep("for(const a in who){ const r=who[a]; if(r.ch!=null) r.years=r.yk[r.ch]||0; }",
        "for(const a in who){ const r=who[a]; if(r.ch!=null) r.years=VB.ycomb&&!r.framework?Object.values(r.yk).reduce((x,y)=>x+y,0):(r.yk[r.ch]||0); }")
import json
k = s.find('const DATA = ') + len('const DATA = '); D, end = json.JSONDecoder().raw_decode(s, k)
D['viab']['ycomb'] = True; s = s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]
open(P, 'w', encoding='utf-8').write(s)
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
S = json.load(open(SNAP, encoding='utf-8')); S['viab']['ycomb'] = True; json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False)
print('combined years on')
