#!/usr/bin/env python3
"""The Israel simulation is no longer embedded in sophia.html.

It is hosted on its own at https://israel.sophia13.workers.dev/ (deploy dist/index.html there), and
Sophia opens it in a new tab through window.openIsraelSim(), passing #book, #book=<volume>, #11minutes
or ?lang=es|ar as needed. This tool now only checks that sophia.html carries no stale embedded copy
and still has the link.

Usage (from the repository root):
  python3 tools/embed_israel.py           # remove an embedded copy if one is present
  python3 tools/embed_israel.py --check   # exit 1 if a copy is embedded or the link is missing
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HUB = ROOT / 'sophia.html'
URL = 'https://israel.sophia13.workers.dev/'

def main() -> int:
    hub = HUB.read_text(encoding='utf-8')
    embedded = re.search(r'<script type="text/plain" id="il_sim_b64">.*?</script>\n?', hub, re.S)
    if URL not in hub:
        print('sophia.html does not link to the hosted Israel simulation (' + URL + ').'); return 1
    if embedded:
        if '--check' in sys.argv[1:]:
            print('sophia.html still embeds a copy of the Israel simulation — run: python3 tools/embed_israel.py'); return 1
        HUB.write_text(hub[:embedded.start()] + hub[embedded.end():], encoding='utf-8')
        print('removed the embedded copy; Sophia links to ' + URL)
        return 0
    print('sophia.html links to the hosted Israel simulation (' + URL + '); nothing embedded.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
