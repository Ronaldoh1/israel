#!/usr/bin/env python3
"""Count the real scenes and entities inside every Sophia module and write them into sophia.html.

Card faces ("ENTITIES MAPPED") used to take their number from each card's description text, and when
a description had no "N entities" phrase the code counted scenes instead, so many cards were wrong.
This tool opens every module, counts what is actually there, and writes MODULE_COUNTS into sophia.html:

  MODULE_COUNTS = { <overlay key>: [scenes, entities], ... }

  scenes   = number of scenes (each scene's `ents` array)
  entities = number of entity cards across all scenes (the figure every module's own text uses)

The Israel simulation is hosted separately; its count comes from index.html (the English scene data).
Modules without an entity map (2026 Elections lists candidates; Hidden Math is an essay) are left out,
and their cards keep their own figure.

Run before tools/build_sophia_dist.py (that build calls it). Usage: python3 tools/count_entities.py [--report]"""
import base64, json, os, re, sys, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'sophia.html')
ISRAEL = os.path.join(ROOT, 'index.html')
START, END = '/*MODULE_COUNTS:start*/', '/*MODULE_COUNTS:end*/'


def _arrays_after(h, key_re):
    """every [...] that follows a key match, bracket-matched with strings respected"""
    out = []
    for m in re.finditer(key_re, h):
        i = m.end()
        while i < len(h) and h[i] in ' \t\r\n': i += 1
        if i >= len(h) or h[i] != '[': continue
        depth = 0; j = i; q = None; esc = False
        while j < len(h):
            c = h[j]
            if q:
                if esc: esc = False
                elif c == '\\': esc = True
                elif c == q: q = None
            elif c in '"\'`': q = c
            elif c in '[{': depth += 1
            elif c in ']}':
                depth -= 1
                if depth == 0: break
            j += 1
        out.append(h[i:j + 1])
    return out


def _top_objects(arr):
    n = 0; depth = 0; q = None; esc = False
    for c in arr:
        if q:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == q: q = None
            continue
        if c in '"\'`': q = c
        elif c in '[{':
            depth += 1
            if depth == 2 and c == '{': n += 1
        elif c in ']}': depth -= 1
    return n


def count(h):
    arrs = _arrays_after(h, r'''["']?\bents["']?\s*:''')
    return len(arrs), sum(_top_objects(a) for a in arrs)


def source_modules(s):
    for m in re.finditer(r'<script type="text/plain" id="([A-Za-z0-9_]+_sim_b64)"[^>]*>(.*?)</script>', s, re.S):
        raw = base64.b64decode(re.sub(r'\s+', '', m.group(2)))
        if raw[:1] == b'\x78':
            try: raw = zlib.decompress(raw)
            except zlib.error: pass
        yield m.group(1), raw.decode('utf-8', 'replace')


def overlay_keys(s):
    """overlay key -> module element id, from openSimOverlay's map"""
    return {k: b for k, b in re.findall(r"\b([A-Za-z0-9_]+)\s*:\s*\{\s*b64\s*:\s*'([A-Za-z0-9_]+_sim_b64)'", s)}


def build(s):
    by_b64 = {k: count(h) for k, h in source_modules(s)}
    res = {}
    for key, b64 in overlay_keys(s).items():
        c = by_b64.get(b64)
        if c and c[1] > 0: res[key] = list(c)
    if os.path.exists(ISRAEL):
        h = open(ISRAEL, encoding='utf-8').read()
        m = re.search(r'<script[^>]*id="scenedata"[^>]*>(.*?)</script>', h, re.S)
        if m:
            c = count(m.group(1))
            if c[1] > 0: res['israel'] = list(c)
    return res, by_b64


def inject(s, res):
    blob = START + json.dumps(res, sort_keys=True, separators=(',', ':')) + END
    if START in s:
        a = s.index(START); b = s.index(END) + len(END)
        return s[:a] + blob + s[b:]
    anchor = 'const DATA = ['
    assert s.count(anchor) == 1, 'DATA anchor not found exactly once'
    return s.replace(anchor, 'const MODULE_COUNTS = ' + blob + ';\n' + anchor)


if __name__ == '__main__':
    s = open(SRC, encoding='utf-8').read()
    res, by_b64 = build(s)
    new = inject(s, res)
    if new != s: open(SRC, 'w', encoding='utf-8').write(new)
    no_ents = sorted(k for k, v in by_b64.items() if v[1] == 0)
    print('MODULE_COUNTS: %d modules, %s entities in total; no entity map: %s'
          % (len(res), f"{sum(v[1] for v in res.values()):,}", ', '.join(no_ents) or 'none'))
    if '--report' in sys.argv:
        for k in sorted(res): print('  %-22s %4d scenes %6d entities' % (k, res[k][0], res[k][1]))
