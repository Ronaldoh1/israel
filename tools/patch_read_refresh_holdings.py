#!/usr/bin/env python3
"""Refresh the map readings whose figures moved after the holdings-reach fix (tools/patch_holdings_reach.py)
and a stale British-sponsor figure found in the same check. Figures from a live run on 19 Nov 2026.
Idempotent: each replacement applies only if the old text is present.
Usage: python3 tools/patch_read_refresh_holdings.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
R = [
 ("the documented-only tests are: the family alone, about 34%; the family plus everything the map shows cut off from the core once they are gone, about 34%. Taking out only the institutions and wealth vehicles among the 24 (people stay) gives about 11%; taking out only the people gives about 26%. The jump from 34% to 10% therefore",
  "the documented-only tests are: the family alone, about 34%; the family plus everything the map shows cut off from the core once they are gone, about 34%. Taking out only the institutions and wealth vehicles tied to them (people stay) gives about 11%; taking out only the people gives about 26%. The jump from 34% to 10% therefore"),
 ("About 9%. Read this as an upper bound", "About 10%. Read this as an upper bound"),
 ("About 16% on time and about 33% ever, with about 51 years of lost time against 39 for the family alone.",
  "About 18% on time and about 33% ever, with about 51 years of lost time against 39 for the family alone."),
 ("About 30%, the same as removing the family alone.", "About 34%, the same as removing the family alone."),
 ("About 10%. Most of the drop in the featured test", "About 11%. Most of the drop in the featured test"),
 ("About 20% on time and about 35% ever, with about 48 years lost.", "About 23% on time and about 36% ever, with about 47 years lost."),
 ("About 19% on time and about 34% ever, with about 49 years lost. Documented ties only. Compare with the family alone, about 30%:",
  "About 21% on time and about 35% ever, with about 49 years lost. Documented ties only. Compare with the family alone, about 34%:"),
 ("About 44% on time and about 49% ever: unlikely, with about 26 years lost.", "About 43% on time and about 49% ever: unlikely, with about 26 years lost."),
 ("Without the British state the chance of a state in 1948 falls to about 47%, and 28 years of work are lost.",
  "Without the British state the chance of a state in 1948 falls to about 36%, and 28 years of work are lost."),
 ("About 14% for 1948 and about 35% ever: unlikely.", "About 13% for 1948 and about 35% ever: unlikely."),
]
n = 0
for a, b in R:
    if a in s: s = s.replace(a, b); n += 1
open(P, 'w', encoding='utf-8').write(s)
print('readings refreshed:', n)
