#!/usr/bin/env python3
"""Add the "Download the PDF" links to the library (27 Nov 2026).

Each written book gets a PDF link on its library shelf card and on its title page, next to "Contents".
The files themselves are made by tools/build_book_pdfs.py into dist/israel-web/pdf/<book id>.pdf.
Idempotent: running it twice changes nothing. Usage: python3 tools/patch_pdf_links.py"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'tools', 'book_block.html')   # the library's source; embed_book.py copies it into index.html
s = open(P, encoding='utf-8').read()
n0 = s

PDF = "'<a class=\"lb-pdf\" href=\"pdf/' + esc(b.id) + '.pdf\" download onclick=\"event.stopPropagation()\" aria-label=\"Download ' + esc(b.title) + ' as a PDF\">Download PDF</a>'"
A = "(MAPS[b.id] ? '<button class=\"lb-map\" type=\"button\" data-epmap=\"' + b.id + '\" aria-label=\"Explore the ' + esc(MAPS[b.id].n) + '\">🏷️ 🕸 Network map</button>' : '')"
if 'class="lb-pdf"' not in s:
    assert s.count(A) == 1, 'shelf map button not found'
    s = s.replace(A, A + ' + ' + PDF, 1)

B = "    if(!low) h += '<button class=\"alt\" type=\"button\" data-go-id=\"contents\">Contents</button>' +"
if 'class="alt bk-pdf"' not in s:
    assert s.count(B) == 1, 'start card not found'
    s = s.replace(B, B + "\n      '<a class=\"alt bk-pdf\" href=\"pdf/' + esc(BOOK.id) + '.pdf\" download>Download the PDF</a>' +", 1)

C = '#bookView[data-theme="night"] .lb-metas .lb-map{color:#F0A28F;border-color:#F0A28F}'
CSS = ('\n.lb-pdf{display:inline-flex;align-items:center;margin:7px 0 0 6px;padding:6px 11px;border:1px solid #8A6A22;border-radius:999px;'
       'background:color-mix(in srgb,#B8862B 10%,transparent);color:#7A5A12;font:650 12px/1.2 system-ui,sans-serif;text-decoration:none;vertical-align:top}'
       '\n.lb-pdf::before{content:"";width:9px;height:11px;margin-right:6px;background:currentColor;'
       'clip-path:polygon(35% 0,65% 0,65% 45%,90% 45%,50% 85%,10% 45%,35% 45%);flex:none}'
       '\n.lb-metas .lb-pdf:hover{background:color-mix(in srgb,#B8862B 20%,transparent)}'
       '\n#bookView[data-theme="night"] .lb-metas .lb-pdf{color:#E3B65A;border-color:#E3B65A}'
       '\n.bk-go a.alt{text-decoration:none}')
if '.lb-pdf{' not in s:
    assert s.count(C) == 1, 'library style anchor not found'
    s = s.replace(C, C + CSS, 1)

if s != n0:
    open(P, 'w', encoding='utf-8').write(s); print('book_block.html: PDF links added')
else:
    print('book_block.html: PDF links already present')
