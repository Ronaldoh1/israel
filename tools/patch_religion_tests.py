#!/usr/bin/env python3
"""Adds the religion-pass tests. Run after patch_religion_pass4.py. Idempotent."""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if "id:'religion_jewish'" in s:
    print('religion tests already applied'); sys.exit(0)
anchor = " {id:'haavara_out',"
assert s.count(anchor) == 1
T = r""" {id:'religion_jewish', featTag:'Featured test · religion', q:'What if religious Jewish support had been absent: no Mizrachi, no Rabbi Mohilever, no Rav Kook or Chief Rabbinate?',
  ids:()=>['mizrachi','mohilever','kook','chief_rabbinate'].filter(x=>N.get(x)),
  what:'The religious Zionist party Mizrachi (1902), Rabbi Samuel Mohilever, whose appeal of 1882 brought Edmond de Rothschild to Rishon LeZion, Rav Kook and the Chief Rabbinate the Mandate recognized in 1921.',
  read:'About 93%, almost no change. Mizrachi kept religious Jews inside the Zionist Organization, and Mohilever\'s appeal brought Edmond de Rothschild in, but the money and the organization they connected to stand without them. Religious Jewish support mattered more to who joined the movement than to the decisions that founded the state.'},
 {id:'religion_all', q:'What if every religious body on the map, Christian and Jewish, for and against, had been absent?',
  ids:()=>['mizrachi','mohilever','kook','chief_rabbinate','hechler','darby','scofield','blackstone','blackstone_1891','apc','ccp','acpc','lsj','jlm_bishopric','vatican','pius10','pius12','agudah','neturei','reform','columbus1937','acj','lazaron','sonnenfeld','dehaan'].filter(x=>N.get(x)),
  what:'Every church, mission, rabbinate, religious party and religious opponent on the map, both sides together. Wise and Silver stay, as political leaders of the American Zionist Emergency Council.',
  read:'About 90% on time. Taking every religious body away, supporters and opponents together, costs about three points, most of it the Christian support counted in legitimacy. On this map the religious opponents carry almost no weight: the Vatican, Agudat Israel and the American Council for Judaism are recorded but not yet weighed against the founding, which the counterforces pass will do.'},
"""
s = s.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('religion tests applied')
