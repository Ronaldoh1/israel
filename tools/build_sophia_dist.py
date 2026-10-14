"""Build the compact distribution of the Sophia hub: dist/sophia.html.

sophia.html stays the editable source: tools/embed_israel.py and every module embed write into it
as plain base64 in <script type="text/plain" id="*_sim_b64">. This step replaces each module's
base64 with base64(zlib(raw module HTML)), marks the element data-z="1", and patches Sophia's single
decoder (b64ToBytes) to inflate marked blobs with fflate. Unmarked blobs still decode as before,
so a partly compressed file keeps working.

Nothing is removed: every module is inflated again here and compared byte for byte with the original.
Usage: python3 tools/build_sophia_dist.py [--check]"""
import base64, os, re, sys, zlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'sophia.html'); OUT = os.path.join(ROOT, 'dist', 'sophia.html')
FFLATE = open(os.path.join(ROOT, 'tools', 'vendor', 'fflate-0.8.2.min.js'), encoding='utf-8').read()

s = open(SRC, encoding='utf-8').read()
OLD_DEC = """    const bin = atob(el.textContent.trim());
    const bytes = new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++) bytes[i]=bin.charCodeAt(i);
    return bytes;"""
NEW_DEC = """    const bin = atob(el.textContent.trim());
    const bytes = new Uint8Array(bin.length);
    for(let i=0;i<bin.length;i++) bytes[i]=bin.charCodeAt(i);
    /* compressed modules (tools/build_sophia_dist.py) are zlib streams marked data-z="1" */
    return el.getAttribute('data-z') === '1' ? fflate.unzlibSync(bytes) : bytes;"""
assert s.count(OLD_DEC) == 1, 'decoder not found exactly once; update this tool to match sophia.html'
s = s.replace(OLD_DEC, NEW_DEC)

pat = re.compile(r'<script type="text/plain" id="([A-Za-z0-9_]+_sim_b64)">(.*?)</script>', re.S)
out = []; pos = 0; n = 0; before = after = 0
for m in pat.finditer(s):
    raw = base64.b64decode(re.sub(r'\s+', '', m.group(2)))
    z = zlib.compress(raw, 9)
    assert zlib.decompress(z) == raw, m.group(1)
    enc = base64.b64encode(z).decode('ascii')
    out.append(s[pos:m.start()]); out.append('<script type="text/plain" id="%s" data-z="1">%s</script>' % (m.group(1), enc))
    pos = m.end(); n += 1; before += len(m.group(2)); after += len(enc)
out.append(s[pos:]); s = ''.join(out)

# fflate must be defined before any module opens; put it right before the overlay wiring script
anchor = '/* ============ SIM OVERLAY WIRING ============ */'
i = s.index(anchor); i = s.rfind('<script>', 0, i)
s = s[:i] + '<script>/* fflate 0.8.2 (MIT): inflates compressed modules */\n' + FFLATE + '\n</script>\n' + s[i:]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
if '--check' not in sys.argv:
    open(OUT, 'w', encoding='utf-8').write(s)
print('dist/sophia.html: %.2f MB (source %.2f MB); %d modules compressed, %.2f MB -> %.2f MB'
      % (len(s.encode()) / 1e6, os.path.getsize(SRC) / 1e6, n, before / 1e6, after / 1e6))
