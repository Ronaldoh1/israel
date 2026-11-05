"""Lighten sophia.html's embedded images (run once; safe to re-run).
1. The hero wordmark PNG (2.3 MB) becomes inline SVG from tools/sophia_logo_svg.py: vector, sharp at any size.
2. Photos that can't be drawn in code (bio banner, archive hero banners, tradition banner) are re-encoded as WebP.
Usage: python3 tools/sophia_assets.py"""
import base64, io, os, re, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from sophia_logo_svg import logo
P = os.path.join(ROOT, 'sophia.html')
s = open(P, encoding='utf-8').read(); before = len(s)

# 1. wordmark
s, n = re.subn(r'<img class="hero-logo reveal" src="data:image/png;base64,[^"]+" alt="[^"]*">', lambda m: logo(), s)
if not n:
    s, n2 = re.subn(r'<svg class="hero-logo reveal".*?</svg>', lambda m: logo(), s, flags=re.S)   # refresh an earlier SVG
    print('wordmark: refreshed' if n2 else 'wordmark: NOT FOUND')
else: print('wordmark: PNG replaced with SVG')

# 2. photos -> WebP
def webp(b64, q):
    im = Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB'); out = io.BytesIO()
    im.save(out, 'WEBP', quality=q, method=6); return base64.b64encode(out.getvalue()).decode()
def sub_img(cls, q):
    global s
    pat = re.compile(r'(<img class="%s[^"]*" src=")data:image/(?:png|jpeg);base64,([^"]+)(")' % re.escape(cls))
    k = 0
    for m in list(pat.finditer(s)):
        s = s.replace(m.group(0), m.group(1) + 'data:image/webp;base64,' + webp(m.group(2), q) + m.group(3), 1); k += 1
    print(f'{cls}: {k} re-encoded')
sub_img('bio-banner', 84)
sub_img('hero-banner-img', 82)
m = re.search(r'(<script type="text/plain" id="tradition_banner">\s*)data:image/(?:png|jpeg);base64,([^<\s]+)', s)
if m:
    s = s.replace(m.group(0), m.group(1) + 'data:image/webp;base64,' + webp(m.group(2), 86), 1); print('tradition_banner: re-encoded')
open(P, 'w', encoding='utf-8').write(s)
print('sophia.html: %.2f MB -> %.2f MB' % (before / 1e6, len(s) / 1e6))
