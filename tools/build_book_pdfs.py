#!/usr/bin/env python3
"""Build a downloadable PDF of every library book: dist/israel-web/pdf/<book id>.pdf.

Each PDF is printed from the reader itself, so it carries the same text, figures, network diagrams,
notes and bibliography a reader sees on the site. The reader's buttons become plain text or are removed;
note numbers and contents entries stay clickable inside the PDF, and every source stays a live link.

Every page carries a footer with the title, the author and the site; each book also gets a rights page
and a fingerprint (the SHA-256 of its text), listed in pdf/manifest.json, so a dated copy of the exact
edition can be shown later.

PDFs are cached in dist/pdf_cache (not committed) by a hash of the book's text and this builder's
settings, so an unchanged book is not printed again. Run after tools/build_israel_web.py:
    python3 tools/build_book_pdfs.py            # every book
    python3 tools/build_book_pdfs.py oslo gaza  # only these
"""
import asyncio, hashlib, subprocess, http.server, json, os, re, shutil, socketserver, sys, threading, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'dist', 'israel-web')
OUT = os.path.join(WEB, 'pdf')
CACHE = os.path.join(ROOT, 'dist', 'pdf_cache')
FONTS = os.path.join(ROOT, 'tools', 'pdf_fonts')
VERSION = 'pdf-v1'          # change to reprint every book after a layout change
SITE = 'www.1948scam.com'

src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
LIB = json.loads(re.search(r'<script[^>]*id="book_data"[^>]*>(.*?)</script>', src, re.S).group(1))
AUTHOR = LIB.get('author') or 'Ron Hernandez'
EDITION = LIB.get('edition') or ''
YEAR = str(datetime.date.today().year)

# ---------- fonts: the reader asks Google Fonts; the PDF gets the same families from tools/pdf_fonts ----------
FAM = {'literata': 'Literata', 'eb-garamond': 'EB Garamond', 'inter': 'Inter', 'montserrat': 'Montserrat',
       'newsreader': 'Newsreader', 'courier-prime': 'Courier Prime', 'nunito': 'Nunito'}
UNI = json.load(open(os.path.join(FONTS, 'unicode.json')))
def font_css():
    css, extra = [], []
    for f in sorted(os.listdir(FONTS)):
        m = re.match(r'(.+?)-(latin-ext|latin|greek-ext|greek|hebrew|arabic|symbols|math)-(\d+)-(normal|italic)\.woff2$', f)
        if not m: continue
        pkg, sub, w, st = m.groups(); rng = UNI[pkg][sub]
        if pkg in FAM: css.append((FAM[pkg], f, w, st, rng))
        else: extra.append((f, w, rng))
    out = []
    for fam, f, w, st, rng in css:
        out.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;src:url(/__pdffonts/%s) format('woff2');unicode-range:%s}" % (fam, st, w, f, rng))
    # Hebrew, Arabic and symbol characters: served under every family name, so no stack falls back to an empty box
    for fam in list(FAM.values()) + ['Georgia', 'serif', 'sans-serif']:
        for f, w, rng in extra:
            for st in ('normal', 'italic'):
                out.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;src:url(/__pdffonts/%s) format('woff2');unicode-range:%s}" % (fam, st, w, f, rng))
    return '\n'.join(out)
FONT_CSS = font_css()

# ---------- the print layout ----------
PRINT_CSS = r"""
@page{size:Letter;margin:0.85in 0.9in 0.95in}
@page :first{margin:0}
html,body{overflow:visible !important;height:auto !important;background:#fff !important}
body>*:not(#bookView){display:none !important}
#bookView{position:static !important;display:block !important;inset:auto !important;overflow:visible !important;height:auto !important;--fs:11.4pt !important;--paper:#fff;background:#fff !important}
#bookView .bk-head,#bookView .bk-fab,#bookView .bk-sheet,#bookView .bk-shade,#bookView .bk-toast,#bookView .bk-bar,#bookView .bk-pop,#bookView .lt-ov,#bookView .bk-prog{display:none !important}
#bookView .bk-scroll{position:static !important;overflow:visible !important;height:auto !important;inset:auto !important}
#bookView .bk-page{max-width:none !important;width:auto !important;padding:0 !important;margin:0 !important;transform:none !important;column-count:auto !important;font-size:11.4pt !important;line-height:1.5 !important;user-select:text !important;cursor:auto !important}
.bk-acts,.bk-keep,.bk-go,.bk-next,.bk-pdf,.otsc-open,button.otsc,.bk-start,.bk-fl{display:none !important}
#bookView .bk-leaf{break-before:auto !important;break-after:auto !important}
#bookView .bk-cc,#bookView #bk-credits,#bookView #bk-rights,#bookView #bk-contents,#bookView #bk-figkey,#bookView .bk-open,#bookView .bk-notes,#bookView .bk-bib{break-before:page !important;page-break-before:always !important}
#bookView .bk-cc{break-after:page !important;page-break-after:always !important}
#bookView .bk-full{height:auto !important;overflow:visible !important}
#bookView .bk-cc{min-height:9.1in !important;height:9.1in !important;margin:0 !important;padding:0 0.4in !important;box-sizing:border-box;display:flex !important;flex-direction:column;justify-content:center;overflow:hidden !important}
#bookView .bk-bt{height:11in !important;min-height:0 !important;margin:0 !important;padding:0.9in !important;box-sizing:border-box;display:flex !important;flex-direction:column;justify-content:center;break-after:page !important;overflow:hidden !important}
#bookView{--paper:#fff !important;--card:#fff !important}
#bookView .bk-scroll,#bookView .bk-page{background:#fff !important}
#bookView h1,#bookView h2,#bookView h3,#bookView h4,#bookView h5,#bookView h6{break-after:avoid !important;page-break-after:avoid !important}
#bookView .bk-out{break-inside:avoid-page}
figure,.bk-myth,table,tr,.bk-fig svg,.dd-flow{break-inside:avoid}
figure{max-width:100% !important}
#bookView .bk-fig>svg{display:block;max-width:4.6in;max-height:5.2in;margin:0 auto}
.tw{overflow:visible !important}
table.stackable td::before{display:none !important}
p{orphans:3;widows:3}
a{color:inherit;text-decoration:none}
.bk-notes a,.bk-bib a,.fig-src a{color:#1B2A4A;text-decoration:underline;text-decoration-thickness:.5px;word-break:break-word}
.bk-n{color:#8A2D1F !important}
.bk-cn .pg,.bk-cn .ld,.bk-cc .pp{display:none !important}
.bk-cn button,.bk-cn a.r{all:unset;display:block;cursor:auto}
#bk-rights{font-size:.86em;line-height:1.5}
#bk-rights h2{margin-top:0}
#bk-rights .fp{font-family:'Courier Prime','Courier New',monospace;font-size:.84em;word-break:break-all}
details.bk-read{display:block}
details.bk-read>summary{list-style:none;font-weight:600}
details.bk-read>summary::-webkit-details-marker{display:none}
"""

PREP_JS = r"""
(meta) => {
  const pg = document.getElementById('bkPage');
  /* the start card and every button that only works on the site */
  pg.querySelectorAll('.bk-go,.bk-acts,.bk-keep,.bk-next,.otsc-open').forEach(e => e.remove());
  /* contents entries become links to their place in the PDF */
  pg.querySelectorAll('#bk-contents button.r').forEach(b => {
    const a = document.createElement('a'); a.className = 'r';
    const id = b.getAttribute('data-go') ? 'bk-' + b.getAttribute('data-go') : b.getAttribute('data-ch') != null ? 'bk-ch-' + b.getAttribute('data-ch') : b.getAttribute('data-go-id') === 'intro' ? 'bk-intro' : '';
    if (id) a.href = '#' + id; a.innerHTML = b.innerHTML; b.replaceWith(a);
  });
  pg.querySelectorAll('#bk-contents p.d').forEach(p => { if (/Page numbers count/.test(p.textContent)) p.remove(); });
  /* links into the simulation are plain words in print */
  pg.querySelectorAll('a.bk-x').forEach(a => { const s = document.createElement('span'); s.textContent = a.textContent; a.replaceWith(s); });
  pg.querySelectorAll('button').forEach(b => { const s = document.createElement('span'); s.innerHTML = b.innerHTML; b.replaceWith(s); });
  /* diagram captions written for a screen */
  pg.querySelectorAll('figcaption').forEach(c => { c.innerHTML = c.innerHTML.replace(/\s*Tap a name for the detail and its sources\./, ''); });
  pg.querySelectorAll('details').forEach(d => d.open = true);
  pg.querySelectorAll('.bk-read summary').forEach(s => { s.textContent = 'The diagram in words'; });
  pg.querySelectorAll('p.how').forEach(p => p.remove());
  /* the rights page, after the credits */
  const r = document.createElement('section'); r.id = 'bk-rights'; r.className = 'bk-fm';
  r.innerHTML = meta.rights; const cred = document.getElementById('bk-credits');
  if (cred) cred.after(r); else pg.prepend(r);
  document.title = meta.title;
  return {chars: pg.textContent.length, figs: pg.querySelectorAll('figure').length};
}
"""

def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def book_hash(b):
    return hashlib.sha256((VERSION + PRINT_CSS + PREP_JS + json.dumps(b, sort_keys=True, ensure_ascii=False)).encode('utf-8')).hexdigest()

def text_hash(b):
    """The fingerprint printed in the book: the SHA-256 of the book's own text, independent of layout."""
    return hashlib.sha256(json.dumps(b, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()

def rights_html(b, fp):
    t = esc(b['title'])
    return ('<h2>Rights and permissions</h2>'
            '<p>© ' + YEAR + ' ' + esc(AUTHOR) + '. All rights reserved. <i>' + t + '</i> is part of <i>The Israel Architecture</i>, '
            'published free by Observe The System through the Library of Truth ✨.</p>'
            '<p><b>You may</b> read, print and share this PDF unaltered and in full; quote short passages with credit to '
            + esc(AUTHOR) + ' and a link to ' + SITE + '; and link to any part of the book.</p>'
            '<p><b>You may not</b>, without written permission, republish the book or substantial parts of it under another name, '
            'sell it, alter it, or present its research, structure, figures or diagrams as your own work. The sources it cites belong to '
            'their own authors and are open to everyone; what is protected here is this book\'s writing, selection, arrangement and figures.</p>'
            '<p><b>To cite this book:</b> ' + esc(AUTHOR) + ', <i>' + t + '</i>, The Israel Architecture, ' + VL(b) + ' (Observe The System, '
            + esc(EDITION) + '), ' + SITE + '.</p>'
            '<p><b>Permissions and corrections:</b> TikTok @chosenron13 · Instagram @chosen.ron13 · ' + SITE + '</p>'
            '<p><b>This edition:</b> ' + esc(EDITION) + '. Fingerprint of its text (SHA-256), listed with the date at ' + SITE + '/pdf/manifest.json:</p>'
            '<p class="fp">' + fp + '</p>')

def VL(b):
    v = b.get('vol')
    if not v: return 'a volume of the library'
    n = int(v); vals = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    r = ''
    for a, s in vals:
        while n >= a: r += s; n -= a
    return ('Volume ' + r) if not b.get('ser') else (esc(b['ser']) + ', Volume ' + r)

def footer(b):
    return ('<div style="width:100%;font-family:Inter,Arial,sans-serif;font-size:7.5pt;color:#5F5A52;padding:0 0.9in;display:flex;justify-content:space-between">'
            '<span>' + esc(b['title']) + ' · ' + esc(AUTHOR) + ' · ' + SITE + '</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')

# ---------- a local server for dist/israel-web ----------
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
def serve():
    h = lambda *a, **k: Quiet(*a, directory=WEB, **k)
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h); s.daemon_threads = True
    threading.Thread(target=s.serve_forever, daemon=True).start(); return s

async def run(books):
    from playwright.async_api import async_playwright
    srv = serve(); base = 'http://127.0.0.1:%d/' % srv.server_address[1]
    from pypdf import PdfReader, PdfWriter
    results = {}
    async with async_playwright() as p:
        br = await p.chromium.launch()
        ctx = await br.new_context(viewport={'width': 1000, 'height': 1300})
        async def route(r):
            u = r.request.url
            if u.startswith(base): return await r.continue_()
            if '/__pdffonts/' in u:
                f = os.path.join(FONTS, os.path.basename(u.split('?')[0]))
                return await r.fulfill(status=200, content_type='font/woff2', body=open(f, 'rb').read())
            if 'fonts.googleapis.com/css' in u: return await r.fulfill(status=200, content_type='text/css', body=FONT_CSS)
            return await r.abort()
        await ctx.route('**/*', route)
        for b in books:
            key = book_hash(b); cached = os.path.join(CACHE, '%s.%s.pdf' % (b['id'], key[:16]))
            fp = text_hash(b)
            if not os.path.exists(cached):
                pg = await ctx.new_page()
                first = b['chapters'][0]['sections'][0]['s']
                await pg.goto(base + 'index.html#book=' + first, wait_until='load', timeout=180000)
                await pg.wait_for_function('n => document.querySelectorAll("#bkPage .bk-chap").length === n', arg=len(b['chapters']), timeout=180000)
                await pg.add_style_tag(content=PRINT_CSS)
                info = await pg.evaluate(PREP_JS, {'title': b['title'] + ' · ' + AUTHOR, 'rights': rights_html(b, fp)})
                await pg.evaluate('document.fonts.ready.then(()=>1)')
                await pg.wait_for_timeout(500)
                tmp = cached + '.tmp'
                await pg.pdf(path=tmp, format='Letter', print_background=True, display_header_footer=True,
                             header_template='<span></span>', footer_template=footer(b), prefer_css_page_size=True, outline=True, tagged=True)
                await pg.close()
                w = PdfWriter(clone_from=PdfReader(tmp))
                w.add_metadata({'/Title': b['title'] + (' — ' + b['subtitle'] if b.get('subtitle') else ''), '/Author': AUTHOR,
                                '/Subject': 'The Israel Architecture, ' + VL(b) + ' · ' + EDITION,
                                '/Keywords': 'Library of Truth; Observe The System; ' + SITE + '; text sha256 ' + fp,
                                '/Creator': 'Observe The System', '/Producer': 'Observe The System', '/Copyright': '© ' + YEAR + ' ' + AUTHOR})
                w.write(tmp + '2'); os.remove(tmp)
                # object streams and maximum compression roughly halve the file; the result is checked before use
                subprocess.run(['qpdf', '--object-streams=generate', '--compression-level=9', '--recompress-flate', tmp + '2', cached], check=True)
                subprocess.run(['qpdf', '--check', cached], check=True, capture_output=True); os.remove(tmp + '2')
                print('printed %-16s %5d pages  %6.1f MB  %d figures' % (b['id'], len(PdfReader(cached).pages), os.path.getsize(cached) / 1e6, info['figs']), flush=True)
            else:
                print('cached  %-16s' % b['id'], flush=True)
            shutil.copy(cached, os.path.join(OUT, b['id'] + '.pdf'))
            results[b['id']] = {'title': b['title'], 'file': 'pdf/' + b['id'] + '.pdf', 'pages': len(PdfReader(cached).pages),
                                'bytes': os.path.getsize(cached), 'text_sha256': fp,
                                'pdf_sha256': hashlib.sha256(open(cached, 'rb').read()).hexdigest()}
        await br.close()
    srv.shutdown()
    return results

def main():
    assert os.path.exists(os.path.join(WEB, 'index.html')), 'run tools/build_israel_web.py first'
    os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
    want = sys.argv[1:]
    books = [b for b in LIB['books'] if b.get('status') == 'ready' and (not want or b['id'] in want)]
    res = asyncio.run(run(books))
    man_p = os.path.join(ROOT, 'book', 'pdf_manifest.json')   # committed, so first-published dates survive every rebuild
    man = json.load(open(man_p)) if os.path.exists(man_p) else {}
    old = man.get('books', {})
    for k, v in res.items():
        v['dated'] = old.get(k, {}).get('dated') if old.get(k, {}).get('text_sha256') == v['text_sha256'] else datetime.date.today().isoformat()
        old[k] = v
    man = {'author': AUTHOR, 'edition': EDITION, 'site': SITE,
           'note': 'Each book\'s text fingerprint (SHA-256) and the date that edition was first published here.', 'books': old}
    json.dump(man, open(man_p, 'w'), indent=1, ensure_ascii=False)
    shutil.copy(man_p, os.path.join(OUT, 'manifest.json'))
    # keep the cache to the current editions only
    keep = {'%s.%s.pdf' % (b['id'], book_hash(b)[:16]) for b in LIB['books']}
    for f in os.listdir(CACHE):
        if f.endswith('.pdf') and f not in keep: os.remove(os.path.join(CACHE, f))
    print('%d PDFs in dist/israel-web/pdf, %.1f MB' % (len(old), sum(v['bytes'] for v in old.values()) / 1e6))

if __name__ == '__main__':
    main()
