#!/usr/bin/env python3
"""Adds the media-pass tests to the Road to 1948 map. Run after patch_media_pass3.py. Idempotent.
Usage: python3 tools/patch_media_tests.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if "id:'media_campaign'" in s:
    print('media tests already applied'); sys.exit(0)
anchor = " {id:'haavara_out',"
assert s.count(anchor) == 1
T = r""" {id:'media_campaign', featTag:'Featured test · media', q:'What if there had been no American public campaign: no mail and telegram drive on the White House, no 1947 opinion swing?',
  drop:()=>['azec>truman','us_public_1947>truman'],
  what:'Only the two documented ties from public pressure to the president: the American Zionist Emergency Council\'s mail and telegram campaign, and the 1947 opinion polls. The Council\'s diplomatic work and every other tie stay.',
  read:'READ_CAMPAIGN'},
 {id:'media_press', q:'What if the movement\'s own press had never existed: no Die Welt, no news agency, no Palestine Post?',
  ids:()=>['die_welt','jta_news','palestine_post'].filter(x=>N.get(x)),
  what:'Herzl\'s weekly Die Welt, the Jewish Telegraphic Agency and the Palestine Post. The record ties none of them directly to a decision, so they carry no weight.',
  read:'READ_PRESS'},
"""
s = s.replace(anchor, T + anchor)
open(P, 'w', encoding='utf-8').write(s)
print('media tests applied')
