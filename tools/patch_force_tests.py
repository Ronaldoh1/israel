#!/usr/bin/env python3
"""Adds the military-training tests. Run after patch_force_pass6.py. Idempotent."""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if "id:'force_british_training'" in s:
    print('force tests already applied'); sys.exit(0)
anchor = " {id:'haavara_out',"
assert s.count(anchor) == 1
T = r""" {id:'force_british_training', featTag:'Featured test · military training', q:'What if Britain had never trained or armed Jewish forces: no Jewish police of 1936, no Night Squads, no Jewish Brigade?',
  ids:()=>['notrim','sns','jewish_brigade'].filter(x=>N.get(x)),
  what:'The British-raised Jewish police of 1936, up to 22,000 men; Wingate\'s Special Night Squads of 1938; and the Jewish Brigade Group of 1944. The Jewish Legion of the First World War stays.',
  read:'About 93%, almost no change, and this is a limit of the map rather than a finding. The arms channel counts weapons and supply ties; the training these units gave counts as two ties beside the Czechoslovak rifles and machine guns that dominate it. The record says those trained became the nucleus of the Haganah, and that many of Wingate\'s men led the Palmach and the army; the map has no measure of how much better trained men fought, so the figure understates it.'},
"""
s = s.replace(anchor, T + anchor)
# the arms-from-abroad tests already remove British training (Wingate, the Brigade, the Mandate's arming of the Haganah): include the two new units
for a, b in [("ids:()=>['wingate','jewish_brigade','sonneborn_inst'", "ids:()=>['wingate','sns','notrim','jewish_brigade','sonneborn_inst'"),
             ("'irgun','lehi','wingate','jewish_brigade',", "'irgun','lehi','wingate','sns','notrim','jewish_brigade',")]:
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s)
print('force tests applied')
