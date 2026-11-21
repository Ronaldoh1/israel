#!/bin/sh
# Rebuild the Epstein map data and write it into the live page, keeping the page's current interface code.
# (build_explorer.py's template predates interface changes made directly in epstein-network.html, so only the DATA line is taken from it.)
set -e
cd "$(dirname "$0")/.."
cp epstein-network.html /tmp/ep_live_page.html
( cd book/plan/epstein_map && python3 build_data.py && python3 build_explorer.py )
python3 - <<'PY'
import json
def part(p):
    s=open(p,encoding='utf-8').read(); k=s.find('const DATA = ')+13; D,end=json.JSONDecoder().raw_decode(s,k); return s,k,end
nb,kb,eb=part('epstein-network.html'); ol,ko,eo=part('/tmp/ep_live_page.html')
open('epstein-network.html','w',encoding='utf-8').write(ol[:ko]+nb[kb:eb]+ol[eo:])
print('DATA spliced into the live page')
PY
