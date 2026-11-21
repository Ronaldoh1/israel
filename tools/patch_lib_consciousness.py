#!/usr/bin/env python3
"""Adds the Consciousness section to the library shell (tools/book_block.html), shelved right after The Dark
Enlightenment Architecture. Every title is a planned book or booklet shown as "Coming soon" (dimmed, not clickable),
grouped by shelf, each carrying its labels (Nag Hammadi Library, Ethiopian canon, Dead Sea Scrolls...). The Vatican
Architecture, already written, is shelved here as well as in The Israel Architecture. The catalogue itself lives in
book/plan/consciousness_catalogue.json, so titles can change without touching code. Idempotent.
Usage: python3 tools/patch_lib_consciousness.py [tools/book_block.html]"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'tools', 'book_block.html')
CAT = json.load(open(os.path.join(ROOT, 'book', 'plan', 'consciousness_catalogue.json'), encoding='utf-8'))
s = open(P, encoding='utf-8').read()
START, END = '/*__CONSC_DATA_START__*/', '/*__CONSC_DATA_END__*/'

def items_js():
    out, n = [], 0
    for g in CAT['groups']:
        for b in g['items']:
            n += 1
            out.append({'cs': 1, 'g': g['id'], 'id': 'cs_' + b['id'], 'vol': n, 'status': 'soon', 'ser': CAT['section'], 'kind': b['kind'], 'title': b['title'],
                        'subtitle': b['subtitle'], 'span': b.get('span', ''), 'labels': b.get('labels', []), 'sig': b.get('sig'), 'color': b.get('color') or g['color']})
    groups = [{'id': g['id'], 'h': g['title'], 'note': g.get('note', ''), 'open': bool(g.get('open'))} for g in CAT['groups']]
    return 'var CONSC = ' + json.dumps(out, ensure_ascii=False) + ', CONSC_G = ' + json.dumps(groups, ensure_ascii=False) + ', CONSC_SEC = ' + json.dumps({'h': CAT['section'], 'tag': CAT['tagline'], 'sub': CAT['note'], 'cross': CAT.get('cross', [])}, ensure_ascii=False) + ';'

if START in s:   # refresh the catalogue only
    i, j = s.index(START), s.index(END) + len(END)
    s = s[:i] + START + items_js() + END + s[j:]
    open(P, 'w', encoding='utf-8').write(s); print('consciousness catalogue refreshed'); sys.exit()

def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:70], s.count(old))
    s = s.replace(old, new)

CSS = r'''.lb-cs .tagline{margin:-2px 0 6px;padding-left:16px;font:700 13px/1.3 system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:color-mix(in srgb,var(--sc) 70%,var(--ink))}
.lb-grp{margin:0 0 6px;border-top:1px solid var(--rule)}
.lb-grp>summary{list-style:none;cursor:pointer;display:flex;align-items:baseline;gap:10px;padding:14px 4px 12px;font:600 17px/1.25 var(--serif,Georgia,serif)}
.lb-grp>summary::-webkit-details-marker{display:none}
.lb-grp>summary::before{content:'\25B8';font-size:13px;color:color-mix(in srgb,var(--sc) 70%,var(--ink));transition:transform .15s}
.lb-grp[open]>summary::before{transform:rotate(90deg)}
.lb-grp>summary small{font:500 12.5px/1 system-ui,sans-serif;color:var(--muted)}
.lb-grp>summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.lb-grp .gnote{color:var(--muted);font-style:italic;font-size:14px;margin:-4px 0 12px 4px}
.meta .lbl{display:inline-block;margin:5px 4px 0 0;font:600 10px/1 system-ui,sans-serif;letter-spacing:.04em;color:color-mix(in srgb,var(--sc,var(--accent)) 75%,var(--ink));border:1px solid color-mix(in srgb,var(--sc,var(--accent)) 45%,transparent);border-radius:999px;padding:4px 7px}
@media (prefers-reduced-motion:reduce){.lb-grp>summary::before{transition:none}}'''
sub('.lb-sec .sub{padding-left:16px}\n', '.lb-sec .sub{padding-left:16px}\n' + CSS + '\n')

# booklets and books in this section say what they are on the cover and under it
sub("  function VL(b){ return (b && b.ser ? 'Book ' : 'Volume ') + roman(b.vol); }",
    "  function VL(b){ return b && b.cs ? b.kind + ' ' + roman(b.vol) : (b && b.ser ? 'Book ' : 'Volume ') + roman(b.vol); }")
sub("  function VLs(b){ return (b && b.ser ? 'Book ' : 'Vol. ') + roman(b.vol); }",
    "  function VLs(b){ return b && b.cs ? b.kind + ' ' + roman(b.vol) : (b && b.ser ? 'Book ' : 'Vol. ') + roman(b.vol); }")
sub("var k = BY[b.id] || KEYS[(b.vol || 1) % KEYS.length];", "var k = (b.sig && G[b.sig] ? b.sig : 0) || BY[b.id] || KEYS[(b.vol || 1) % KEYS.length];")
sub("    var col = VCLOTH[b.id] || CLOTH[(b.vol - 1) % CLOTH.length];", "    var col = b.color || VCLOTH[b.id] || CLOTH[(b.vol - 1) % CLOTH.length];")
sub("""        if(b.status !== 'ready') return '<div class="meta soon"><b>' + esc(b.title) + '</b><small>Vol. ' + roman(b.vol) + ' · ' + esc(b.span || '') + '</small><span class="chip">In progress</span></div>';""",
    """        if(b.cs) return '<div class="meta soon"><b>' + esc(b.title) + '</b><small>' + esc(b.kind) + (b.span ? ' · ' + esc(b.span) : '') + '</small><div>' + (b.labels || []).map(function(l){ return '<span class="lbl">' + esc(l) + '</span>'; }).join('') + '</div><span class="chip">Coming soon</span></div>';
        if(b.status !== 'ready') return '<div class="meta soon"><b>' + esc(b.title) + '</b><small>Vol. ' + roman(b.vol) + ' · ' + esc(b.span || '') + '</small><span class="chip">In progress</span></div>';""")

JS = '''  /* ---------- the Consciousness section: planned books and booklets, grouped by shelf (catalogue: book/plan/consciousness_catalogue.json) ---------- */
  ''' + START + items_js() + END + '''
  function csText(b){ return (b.title + ' ' + b.subtitle + ' ' + b.kind + ' ' + (b.labels || []).join(' ') + ' consciousness').toLowerCase(); }
  function csSection(q){
    var cross = BOOKS.filter(function(b){ return CONSC_SEC.cross.indexOf(b.id) >= 0 && (!q || q.split(/\\s+/).every(function(w){ return libText(b).indexOf(w) >= 0; })); });
    var items = CONSC.filter(function(b){ return !q || q.split(/\\s+/).every(function(w){ return csText(b).indexOf(w) >= 0; }); });
    if(!cross.length && !items.length) return '';
    var h = '<section class="lb-sec lb-series lb-cs" style="--sc:#4B3A8C"><h2>' + esc(CONSC_SEC.h) + '</h2><p class="tagline">' + esc(CONSC_SEC.tag) + '</p><p class="sub">' + esc(CONSC_SEC.sub) + '</p>';
    if(cross.length) h += shelf(cross);
    CONSC_G.forEach(function(g){
      var list = items.filter(function(b){ return b.g === g.id; });
      if(!list.length) return;
      var books = list.filter(function(b){ return b.kind === 'Book'; }).length;
      h += '<details class="lb-grp"' + (g.open || q ? ' open' : '') + '><summary>' + esc(g.h) + ' <small>' + (books ? books + (books === 1 ? ' book' : ' books') : '') + (books && list.length > books ? ' · ' : '') + (list.length > books ? (list.length - books) + (list.length - books === 1 ? ' booklet' : ' booklets') : '') + '</small></summary>' + (g.note ? '<p class="gnote">' + esc(g.note) + '</p>' : '') + shelf(list) + '</details>';
    });
    return h + '</section>';
  }
'''
sub('  var SHOW_SOON = 10;', JS + '  var SHOW_SOON = 10;')
sub("""' + shelf(deB) + '</section>' : '') +\n""", """' + shelf(deB) + '</section>' : '') +\n      (csHtml = csSection(q)) +\n""")
sub("    $('lbShelves').innerHTML = (ready.length ?", "    var csHtml = '';\n    $('lbShelves').innerHTML = (ready.length ?")
sub("(!ready.length && !prep.length && !epShelf.length && !deB.length ?", "(!ready.length && !prep.length && !epShelf.length && !deB.length && !csHtml ?")
open(P, 'w', encoding='utf-8').write(s)
print('consciousness section added')
