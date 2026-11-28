#!/usr/bin/env python3
"""Road to 1948 map: a stand-in cannot be someone whose role came from the person removed (27 Nov 2026).

When a removed actor's money or work is lost, the model lets another actor of the same circle, already active, cover
part of the gap. It allowed heirs and appointees to do so: with Edmond de Rothschild removed, his son James Armand,
his daughter-in-law Dorothy and his administrator Elie Scheid could stand in for him, though each held the role
because of him. The rule now bars, for every actor, any later actor of the same circle tied to him by kinship,
appointment or employment, directly or through one person. Applies to every node, not only Edmond.
Idempotent. Usage: python3 tools/patch_heirs_rule.py"""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'road-network.html')
s = open(P, encoding='utf-8').read(); s0 = s
H = """const VB = DATA.viab;
/* 27 Nov 2026: who held a role because of whom: a later actor in the same circle tied to an earlier one by kinship, appointment
   or employment, directly or through one person. Such an heir or appointee cannot stand in for the person removed (see vYears). */
VB.heirs=(()=>{ const A=VB.actors||{}, C=VB.circle||{}, T=new Set(['kinship','appointment','employment']), adj=new Map(), out={};
  DATA.edges.forEach(e=>{ if(!T.has(e.type)||!(e.status==='verified'||e.status==='reported')) return; [[e.f,e.t],[e.t,e.f]].forEach(([u,v])=>{ if(!adj.has(u)) adj.set(u,new Set()); adj.get(u).add(v); }); });
  for(const a of Object.keys(A)){ const seen=new Set([a]); let fr=[a]; for(let d=0;d<2;d++){ const nx=[]; for(const u of fr) for(const v of adj.get(u)||[]) if(!seen.has(v)){ seen.add(v); nx.push(v); } fr=nx; }
    const h=[...seen].filter(b=>b!==a&&A[b]&&C[b]&&C[b]===C[a]&&A[b][0]>=A[a][0]); if(h.length) out[a]=h; }
  return out; })();"""
if 'VB.heirs=' not in s:
    assert s.count('const VB = DATA.viab;') == 1
    s = s.replace('const VB = DATA.viab;', H, 1)
a = "A[b][2]!==A[a][2]||A[b][0]>y||(VB.circle&&VB.circle[b]!==VB.circle[a]))"
b = "A[b][2]!==A[a][2]||A[b][0]>y||(VB.circle&&VB.circle[b]!==VB.circle[a])||(VB.heirs&&VB.heirs[a]&&VB.heirs[a].includes(b)))"
if b not in s:
    assert s.count(a) == 1; s = s.replace(a, b, 1)
if s != s0: open(P, 'w', encoding='utf-8').write(s); print('applied')
else: print('already applied')
