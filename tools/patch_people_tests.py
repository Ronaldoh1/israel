#!/usr/bin/env python3
"""Adds the people-channel tests to the Road to 1948 map. Run after patch_people_channel.py. Idempotent.
Usage: python3 tools/patch_people_tests.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if "id:'people_mandate'" in s:
    print('people tests already applied'); sys.exit(0)
anchor = " {id:'un', q:'What if the UN vote had never happened?'"
assert s.count(anchor) == 1
T = r""" {id:'people_mandate', feat:true, featTag:'Featured test · people channel', q:'What if the Mandate government had issued no immigration certificates?',
  ids:()=>[],
  drop:()=>['mandate_admin>imm_1919_23','mandate_admin>imm_1924_29','mandate_admin>imm_1930_32','mandate_admin>imm_1933_39','mandate_admin>imm_1940_41','mandate_admin>imm_1942_48'],
  what:'Every legal immigration certificate issued under the Mandate from 1919 to 1948, the route by which most of about 480,000 immigrants entered. Article 6 of the Mandate obliged Britain to facilitate Jewish immigration. The Haavara emigrants, the clandestine voyages and the immigrants who came before 1914 stay.',
  read:'About 78% on time, down from about 93. Under the Mandate the British government did not only permit the Jewish national home on paper: its certificates let in most of the people who made up the state\'s population in 1948. The test keeps everything else Britain did, so it isolates this one policy.'},
 {id:'people_ottoman', q:'What if no Jews had immigrated before 1914?',
  ids:()=>['imm_ottoman'],
  what:'The first two waves of immigration, about 60,000 people between 1881 and 1914, who founded the first colonies under Ottoman rule.',
  read:'About 93%, almost unchanged. The early waves were small next to those of the Mandate, and many of their members left again.'},
 {id:'people_fourth', q:'What if the Fourth Aliyah of 1924-1929 had not come?',
  ids:()=>['imm_1924_29'],
  what:'The 72,594 immigrants of 1924 to 1929, many of them from Poland, in the years after the United States closed its doors with the Immigration Act of 1924.',
  read:'About 92%. The record links this wave to the American quotas, but it cannot say how many would have gone to America instead, so the map does not give the Act a share of its own.'},
 {id:'people_fifth', q:'What if the Fifth Aliyah of 1933-1939 had not come?',
  ids:()=>['imm_1933_39'],
  what:'The 235,170 immigrants of 1933 to 1939, many of them fleeing Nazi Germany and the persecution spreading across Central Europe, about 60,000 of them through the Haavara transfer.',
  read:'About 87% on time. This was the largest wave before the state, and the one that made the community large enough to claim a state of its own.'},
 {id:'people_clandestine', q:'What if the clandestine voyages after 1942 had never sailed?',
  ids:()=>[],
  drop:()=>['mossad_aliyah>imm_1942_48'],
  what:'About 70,000 immigrants carried by the Mossad LeAliyah Bet on 66 voyages in defiance of British limits. The organization\'s other work stays.',
  read:'About 93%: in numbers the voyages were small beside the legal waves; the Exodus counts separately, in the legitimacy channel.'},
"""
s = s.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('people tests applied')
