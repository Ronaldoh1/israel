#!/usr/bin/env python3
"""Refreshes test readings whose figures moved after the media pass (computed 19 Nov 2026). Idempotent.
Usage: python3 tools/patch_read_refresh_pass3.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
REP = [
 ("read:'About 91%, little change. Dewey had declared", "read:'About 89%, little change. Dewey had declared"),
 ("read:'About 86% on time and about 89% ever. An unknown president", "read:'About 85% on time and about 88% ever. An unknown president"),
 ("read:'About 87% on time, down from about 93. This measures one thing", "read:'About 88% on time, down from about 93. This measures one thing"),
 ("read:'About 88% on time. The Lodge-Fish resolution", "read:'About 89% on time. The Lodge-Fish resolution"),
 ("read:'READ_CAMPAIGN'", "read:'About 92.5% on time, down from about 93. Truman wrote that he had never faced as much pressure and propaganda, but on this map the campaign is one source of legitimacy among many: the survivors\\' case, the UN committee and Congress carry the same channel. The campaign\\'s real effect may have run through votes and through Truman\\'s advisers, which the electoral pass weighs separately.'"),
 ("read:'READ_PRESS'", "read:'About 93%, no change. The press carried the movement\\'s case to readers and editors, but the record ties no decision to it directly, so on this map it has no weight. That is a limit of the method, not a finding that the press did nothing.'"),
]
n = 0
for a, b in REP:
    if b in s and a not in s:
        continue
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b); n += 1
open(P, 'w', encoding='utf-8').write(s)
print('readings refreshed:', n)
