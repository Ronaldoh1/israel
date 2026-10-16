#!/usr/bin/env python3
"""Build the hosted version of the Israel simulation: dist/israel-web/index.html plus small data files.

dist/index.html (tools/build_dist.py) is one 10.8 MB file; single uploads that large stall on Cloudflare.
Here each compressed data block (translations, deep dives, scenes, the library, citations) moves out
into dist/israel-web/d/<id>.<n> pieces of at most 1 MB of raw zlib bytes. The inline restore call
becomes __otsFetch(id, n), which loads the pieces with a synchronous same-origin request while the
page parses, then restores the <script type="application/json"> element exactly as before, so every
reader of those blocks keeps working unchanged. The restored text is checked byte for byte here.

dist/index.html stays the single-file version for opening locally (requests do not work from file://).
Run after tools/build_dist.py. Usage: python3 tools/build_israel_web.py"""
import base64, os, re, shutil, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'dist', 'index.html')
ORIG = os.path.join(ROOT, 'index.html')
OUT = os.path.join(ROOT, 'dist', 'israel-web')
PIECE = 1_000_000

s = open(SRC, encoding='utf-8').read()
orig = open(ORIG, encoding='utf-8').read()
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'd'))

FETCH = ('window.__otsFetch=function(id,n){var parts=[],total=0;'
         'for(var k=0;k<n;k++){var x=new XMLHttpRequest();x.open("GET","d/"+id+"."+k,false);'
         'x.overrideMimeType("text/plain; charset=x-user-defined");x.send(null);'
         'if(x.status!==200&&x.status!==0)throw new Error("data "+id+"."+k+": HTTP "+x.status);'
         'var t=x.responseText,u=new Uint8Array(t.length);for(var i=0;i<t.length;i++)u[i]=t.charCodeAt(i)&255;parts.push(u);total+=u.length;}'
         'var all=new Uint8Array(total),o=0;parts.forEach(function(p){all.set(p,o);o+=p.length;});'
         'var txt=new TextDecoder().decode(fflate.unzlibSync(all));var el=document.createElement("script");'
         'el.type="application/json";el.id=id;el.textContent=txt;var me=document.currentScript;me.parentNode.insertBefore(el,me);};')
anchor = 'window.__otsUnpack=function'
assert s.count(anchor) == 1, 'loader not found; run tools/build_dist.py first'
s = s.replace(anchor, FETCH + anchor)

files = 0
def out(m):
    global files
    bid, b64 = m.group(1), m.group(2)
    raw = base64.b64decode(b64)
    # must restore to exactly the source block
    om = re.search(r'<script(?=[^>]*\bid="%s")(?=[^>]*type="application/json")[^>]*>(.*?)</script>' % re.escape(bid), orig, re.S)
    assert om and zlib.decompress(raw).decode('utf-8') == om.group(1), 'block %s does not round-trip' % bid
    pieces = [raw[i:i + PIECE] for i in range(0, len(raw), PIECE)]
    for k, p in enumerate(pieces):
        open(os.path.join(OUT, 'd', '%s.%d' % (bid, k)), 'wb').write(p); files += 1
    return '<script>__otsFetch("%s",%d)</script>' % (bid, len(pieces))
s, n = re.subn(r'<script>__otsUnpack\("([A-Za-z0-9_-]+)","([A-Za-z0-9+/=]+)"\)</script>', out, s)
assert n >= 8, 'expected the compressed blocks, found %d' % n
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(s)
big = max(os.path.getsize(os.path.join(OUT, 'd', f)) for f in os.listdir(os.path.join(OUT, 'd')))
print('dist/israel-web/index.html: %.2f MB; %d data blocks in %d files (largest %.2f MB)'
      % (os.path.getsize(os.path.join(OUT, 'index.html')) / 1e6, n, files, big / 1e6))
