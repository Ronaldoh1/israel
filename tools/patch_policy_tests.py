#!/usr/bin/env python3
"""Adds the policy-pass tests to the Road to 1948 map. Run after patch_policy_pass2.py. Idempotent.
Usage: python3 tools/patch_policy_tests.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if "id:'policy_lto'" in s:
    print('policy tests already applied'); sys.exit(0)
anchor = " {id:'un', q:'What if the UN vote had never happened?'"
assert s.count(anchor) == 1
T = r""" {id:'policy_lto', feat:true, featTag:'Featured test · policy', q:'What if the Mandate\'s land-transfer law had not opened the land market?',
  ids:()=>['lto_1920'],
  what:'The Land Transfer Ordinance of 1920, the legal route for every purchase the Jewish National Fund made under the Mandate: about 914,000 of the 936,000 dunams it held in May 1948. Land bought before 1920, and land held by PICA and private buyers, stays.',
  read:'About 86% on time, down from about 93.'},
 {id:'policy_jnf', q:'What if the Jewish National Fund had never existed?',
  ids:()=>['jnf'],
  what:'The JNF, founded in 1901, its fundraising, and all 936,000 dunams it held in May 1948, which fall with it.',
  read:'About 83%, and the founding is delayed by about two years.'},
 {id:'policy_macdonald', featTag:'Assumption · upper bound', q:'What if the Passfield White Paper\'s limits had stood, with no MacDonald letter in 1931?',
  ids:()=>['macdonald_letter'],
  drop:()=>['mandate_admin>imm_1933_39'],
  what:'An assumption, marked as such: the certificates of 1933 to 1939, about 175,000 immigrants, are removed as if the 1930 limits had held for the whole decade. That is an upper bound, since some immigration would have continued. The Haavara emigrants stay.',
  read:'About 90% on time even at this upper bound. The letter itself is documented; how much it changed is not. The figure shows how much rode on the reversal if the limits had held.'},
 {id:'policy_doors', featTag:'Assumption', q:'What if the Mandate had contained no promise to facilitate Jewish immigration and land settlement?',
  ids:()=>['lto_1920'],
  drop:()=>['mandate_admin>imm_1919_23','mandate_admin>imm_1924_29','mandate_admin>imm_1930_32','mandate_admin>imm_1933_39','mandate_admin>imm_1940_41','mandate_admin>imm_1942_48'],
  what:'An assumption, marked as such: Article 6 and the instruments that carried it out, the immigration certificates and the land-transfer law, are removed together. Everything else the British state did stays.',
  read:'About 73%, and the founding is delayed. These two policies, more than any single person, are what the Mandate gave the movement in practice.'},
"""
s = s.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('policy tests applied')
