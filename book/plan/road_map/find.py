"""find.py REGEX [STAGE]: print matching book sentences with their citations (for curating road_layer.json)"""
import sys, re, build_road as b
pat = re.compile(sys.argv[1]); st = sys.argv[2] if len(sys.argv) > 2 else None
for s_, sec, txt in b.corpus():
    if st and s_ != st: continue
    for s in b.sentences(txt):
        if pat.search(s['t']): print(sec, '|', s['t'][:260], '|', ';'.join(s['c']))
