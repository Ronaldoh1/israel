#!/usr/bin/env python3
"""Adds extra-opposition tests: a test's decider object may carry 'xopp:<decision id>' = n, which adds n to
that decision's documented resistance (the baseline is computed without it). Used for weight-sensitivity
tests of the opposition. Idempotent."""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if 'function vDecisionChance(D, rem, dec0, xo)' in s:
    print('xopp already applied'); sys.exit(0)
R = [("function vDecisionChance(D, rem, dec0){", "function vDecisionChance(D, rem, dec0, xo){"),
     ("  for(const o of D.oppose) if(!rem.has(o)) O++;\n", "  for(const o of D.oppose) if(!rem.has(o)) O++;\n  O+=(+xo||0);\n"),
     ("vDecisionChance(D,rem0,vDecider[D.id])", "vDecisionChance(D,rem0,vDecider[D.id],vDecider['xopp:'+D.id])")]
for a, b in R:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
anchor = " {id:'fdr_other',"
assert s.count(anchor) == 1
T = r""" {id:'opp_double', featTag:'Assumption · opposition', q:'What if the opposition inside the American government had carried twice its weight?',
  ids:()=>[], decider:{'xopp:us_partition':5,'xopp:us_recognition':5},
  what:'An assumption, marked as such: the documented opponents of the two American decisions (the Secretary of State, the State Department and its planners, Loy Henderson, the Defense Secretary and the Joint Chiefs) count twice. Nothing is removed.',
  read:'About 88% on time. Counting the opposition twice lowers the chance that the two American decisions are taken, but the founding still happens on time: the UN vote, the Soviet bloc\'s support and the movement\'s own forces do not rest on Washington alone.'},
 {id:'opp_triple', featTag:'Assumption · opposition', q:'What if it had carried three times its weight?',
  ids:()=>[], decider:{'xopp:us_partition':10,'xopp:us_recognition':10},
  what:'The same, with the opponents counted three times.',
  read:'About 84%, and the founding is delayed. Even at three times its weight, the opposition inside the American government could delay the state by making the American decisions uncertain; it could not stop it, because it could reach only those decisions.'},
"""
s = s.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('xopp applied')
