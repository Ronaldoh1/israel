#!/usr/bin/env python3
"""Adds the lobbying-pass tests. Run after patch_lobby_pass5.py. Idempotent."""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if "id:'latam_bloc'" in s:
    print('lobby tests already applied'); sys.exit(0)
anchor = " {id:'votes', q:'What if the three pressured votes had gone the other way?'"
assert s.count(anchor) == 1
T = r""" {id:'latam_bloc', featTag:'Assumption · upper bound', q:'What if García Granados and Fabregat had not organized the Latin American bloc?',
  ids:()=>['bolivia','brazil','costa_rica','dominican','ecuador','haiti','nicaragua','panama','paraguay','peru','venezuela'].filter(x=>N.get(x)),
  what:'An assumption and an upper bound: the eleven Latin American states that voted for partition, other than Guatemala and Uruguay, abstain instead. Some would have voted for it anyway; the source says only that the plan might not have passed without the bloc.',
  read:'About 78% on time and about 86% ever, with the founding delayed. With the eleven abstaining the vote is 22 to 13, short of two-thirds, and Resolution 181 fails. The state could still come, later, through recognition by the great powers, which is why the figure stays high. This is an upper bound: the documents say the bloc was organized, not how many of its members would have voted no without it.'},
"""
s = s.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('lobby tests applied')
