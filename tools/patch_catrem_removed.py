#!/usr/bin/env python3
"""Road to 1948 map: when a funder is removed outright, the places he built fall with him (27 Nov 2026).

vCatRem already dropped everything in VB.built_by when every one of a funder's money ties was cut ("what if Edmond
had not bought land and funded colonies"), but not when the funder himself was removed ("Edmond entirely"), so the
list of what was lost was shorter for the larger test. Removing the funder now counts as cutting all his ties.
The chances do not change (the colonies' own ties were already gone with him); the list of what is lost does.
Idempotent. Usage: python3 tools/patch_catrem_removed.py"""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'road-network.html')
s = open(P, encoding='utf-8').read()
a = "if(m.length&&m.every(e=>vDrop.has(e[0]+'>'+e[1]))) list.forEach(x=>out.add(x));"
b = "if(m.length&&(rem0.has(who)||m.every(e=>vDrop.has(e[0]+'>'+e[1])))) list.forEach(x=>out.add(x));"
if b in s: print('already applied')
else:
    assert s.count(a) == 1; s = s.replace(a, b); open(P, 'w', encoding='utf-8').write(s); print('applied')
