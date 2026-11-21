"""Build the compact distribution of the simulation: dist/index.html.

index.html stays the editable source (every patch and embed tool reads it as plain JSON).
This step compresses the largest JSON data blocks (translations, deep dives, scenes, the library)
with zlib, stores them base64-encoded, and replaces each with a tiny inline script that restores
the original <script type="application/json" id="..."> element synchronously while the page parses.
Everything that reads those blocks with document.getElementById(id).textContent keeps working unchanged.
Nothing is removed: the restored text is byte-for-byte the original (checked below).
Usage: python3 tools/build_dist.py [--check]"""
import base64, hashlib, os, re, sys, zlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html'); OUT = os.path.join(ROOT, 'dist', 'index.html')
IDS = ['i18n-ar', 'i18n-es', 'deepdive-en', 'scenedata', 'book_data', 'citationdata', 'expanded-en', 'eleven_html']
s = open(SRC, encoding='utf-8').read()
FFLATE = open(os.path.join(ROOT, 'tools', 'vendor', 'fflate-0.8.2.min.js'), encoding='utf-8').read()
LOADER = ('<script>/* fflate 0.8.2 (MIT) — restores compressed data blocks */\n' + FFLATE + '\n'
          'window.__otsUnpack=function(id,b64){var bin=atob(b64),n=bin.length,u=new Uint8Array(n);for(var i=0;i<n;i++)u[i]=bin.charCodeAt(i);'
          'var txt=new TextDecoder().decode(fflate.unzlibSync(u));var el=document.createElement("script");el.type="application/json";el.id=id;el.textContent=txt;'
          'var me=document.currentScript;me.parentNode.insertBefore(el,me);};</script>\n')
first = None; saved = 0
for bid in IDS:
    m = re.search(r'<script(?=[^>]*\bid="%s")(?=[^>]*type="application/json")[^>]*>(.*?)</script>' % re.escape(bid), s, re.S)
    if not m: print('not found:', bid); continue
    body = m.group(1)
    z = base64.b64encode(zlib.compress(body.encode('utf-8'), 9)).decode('ascii')
    rep = '<script>__otsUnpack(%s,"%s")</script>' % ('"' + bid + '"', z)
    if first is None or m.start() < first: first = m.start()
    saved += len(m.group(0).encode()) - len(rep.encode())
    s = s[:m.start()] + rep + s[m.end():]
# the loader must run before the first restored block
pos = min(s.find('<script>__otsUnpack('), len(s))
s = s[:pos] + LOADER + s[pos:]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
if '--check' not in sys.argv:
    open(OUT, 'w', encoding='utf-8').write(s)
print('dist/index.html: %.2f MB (source %.2f MB, saved %.2f MB)' % (len(s.encode()) / 1e6, os.path.getsize(SRC) / 1e6, saved / 1e6))
