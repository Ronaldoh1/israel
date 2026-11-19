#!/usr/bin/env python3
"""Refreshes test readings in the Road to 1948 map whose quoted figures moved after the legitimacy, people
and land-held channels were added (computed 19 Nov 2026). Idempotent: each replacement applies once.
Usage: python3 tools/patch_read_refresh_pass2.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
REP = [
 ("read:'About 10%. Read this as an upper bound", "read:'About 9%. Read this as an upper bound"),
 ("read:'About 18% on time and about 33% ever, with about 51 years", "read:'About 16% on time and about 33% ever, with about 51 years"),
 ("read:'About 34%, almost the same as removing the family alone.", "read:'About 30%, the same as removing the family alone."),
 ("read:'About 11%. Most of the drop", "read:'About 10%. Most of the drop"),
 ("read:'About 23% on time and about 36% ever, with about 48 years lost.", "read:'About 20% on time and about 35% ever, with about 48 years lost."),
 ("read:'About 21% on time and about 35% ever, with about 49 years lost. Documented ties only. Compare with the family alone, about 34%:", "read:'About 19% on time and about 34% ever, with about 49 years lost. Documented ties only. Compare with the family alone, about 30%:"),
 ("read:'About 92%, almost no change. Dewey had declared", "read:'About 91%, little change. Dewey had declared"),
 ("read:'About 87%, with about five years of delay. An unknown president", "read:'About 86% on time and about 89% ever. An unknown president"),
 ("read:'About 91%. The acts are documented,", "read:'About 92%. The acts are documented,"),
 ("read:'About 20% for 1948 and about 42% ever: unlikely. Without the British sponsor the same parts together still cut the chance to about 40%.", "read:'About 14% for 1948 and about 35% ever: unlikely. Without the British sponsor the same parts together still cut the chance to about 48%."),
]
n = 0
for a, b in REP:
    if b in s and a not in s:
        continue
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b); n += 1
open(P, 'w', encoding='utf-8').write(s)
print('readings refreshed:', n)
