#!/usr/bin/env python3
"""Keep the Israel simulation embedded in sophia.html identical to index.html.

index.html is the standalone simulation and the file we edit. sophia.html carries an
exact copy of it, base64-encoded in <script type="text/plain" id="il_sim_b64">, which
Sophia decodes into its overlay when the Israel card is opened.

Usage (from the repository root):
  python3 tools/embed_israel.py           # re-embed index.html into sophia.html
  python3 tools/embed_israel.py --check   # exit 1 if the embedded copy is out of date
"""
import base64
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SIM = ROOT / 'dist' / 'index.html' if (ROOT / 'dist' / 'index.html').exists() else ROOT / 'index.html'
HUB = ROOT / 'sophia.html'
OPEN = '<script type="text/plain" id="il_sim_b64">'
CLOSE = '</script>'
INSERT_BEFORE = '<script type="text/plain" id="vt_sim_b64">'


def main() -> int:
    check = '--check' in sys.argv[1:]
    sim = SIM.read_bytes()
    hub = HUB.read_text(encoding='utf-8')
    encoded = base64.b64encode(sim).decode('ascii')

    start = hub.find(OPEN)
    if start >= 0:
        end = hub.index(CLOSE, start + len(OPEN))
        current = hub[start + len(OPEN):end]
        if re.sub(r'\s+', '', current) == encoded:
            print(f'sophia.html is up to date with index.html (sha256 {hashlib.sha256(sim).hexdigest()[:12]}).')
            return 0
        if check:
            print('sophia.html embeds an OUTDATED copy of index.html — run: python3 tools/embed_israel.py')
            return 1
        hub = hub[:start + len(OPEN)] + encoded + hub[end:]
    else:
        if check:
            print('sophia.html has no embedded Israel simulation — run: python3 tools/embed_israel.py')
            return 1
        at = hub.index(INSERT_BEFORE)
        hub = hub[:at] + OPEN + encoded + CLOSE + '\n' + hub[at:]

    HUB.write_text(hub, encoding='utf-8')
    print(f'Embedded index.html ({len(sim):,} bytes, sha256 {hashlib.sha256(sim).hexdigest()[:12]}) '
          f'into sophia.html (now {HUB.stat().st_size:,} bytes).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
