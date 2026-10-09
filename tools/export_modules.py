"""Standalone modules and a data layer for a future site (Next.js / Vercel).

Reads window.DASHBOARDS and window.MAPS out of index.html and writes:
  modules/dashboards/<id>.html, modules/maps/<id>.html  self-contained pages (charts.js + charts.css + data inline)
  modules/index.html                                     a list of them all
  export/dashboards.json, export/maps.json               the raw data
  export/README.md                                       the data shapes, for whoever builds React components from them
export/library.json (the book payload) is written by tools/embed_book.py, byte for byte what it embeds.
Usage: python3 tools/export_modules.py [index.html]"""
import html, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')
s = open(IDX, encoding='utf-8').read()

def grab(marker):
    i = s.find(marker)
    assert i >= 0, marker + ' not found in ' + IDX
    i += len(marker)
    while s[i] in ' =\n': i += 1
    return json.JSONDecoder().raw_decode(s, i)[0]

DASH = grab('window.DASHBOARDS =')
MAPS = grab('window.MAPS=')
# the simulation's openDashboard() appends an empty "Sources" tab at run time; it is not part of the data
for d in DASH.values():
    d['tabs'] = [t for t in d.get('tabs', []) if not (t.get('name') == 'Sources' and not t.get('sections'))]

JS = open(os.path.join(ROOT, 'tools', 'charts.js'), encoding='utf-8').read()
CSS = open(os.path.join(ROOT, 'tools', 'charts.css'), encoding='utf-8').read()
assert '</script' not in JS.lower() and '</style' not in CSS.lower()

PAGE_CSS = """
:root{--paper:#F3EDE1;--ink:#26221C;--muted:#6E6457;--rule:#D8CDB9;--accent:#8A2D1F;--fig:#1B2A4A;--figline:#B8862B;--card:#FBF8F1;color-scheme:light}
:root[data-theme="night"]{--paper:#141519;--ink:#DDD6C8;--muted:#9B9384;--rule:#34322D;--accent:#E3A375;--fig:#A9BCE0;--figline:#C9A15A;--card:#1C1D22;color-scheme:dark}
@media (prefers-color-scheme:dark){:root:not([data-theme="paper"]){--paper:#141519;--ink:#DDD6C8;--muted:#9B9384;--rule:#34322D;--accent:#E3A375;--fig:#A9BCE0;--figline:#C9A15A;--card:#1C1D22;color-scheme:dark}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.55 'Literata',Georgia,'Times New Roman',serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:820px;margin:0 auto;padding:18px 16px 40px}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0 0 18px;font:600 13px/1.2 system-ui,-apple-system,'Segoe UI',sans-serif}
.top a{color:var(--accent);text-decoration:none}
.top button{min-height:40px;border:1px solid var(--rule);background:transparent;color:var(--ink);border-radius:999px;padding:0 14px;font:inherit;cursor:pointer}
.top button:hover{border-color:var(--ink)}
.sheet{background:var(--card);border:1px solid var(--rule);border-radius:6px;padding:20px 18px}
.otsc .otsc-dt{font-size:clamp(26px,5vw,36px)}
.otsc-tabs{margin-left:-18px !important;margin-right:-18px !important;padding:0 10px}
footer{margin:28px 0 0;text-align:center;color:var(--muted);font:500 13px/1.5 system-ui,-apple-system,sans-serif;letter-spacing:.02em}
.list{list-style:none;margin:0;padding:0}
.list li{border-bottom:1px solid var(--rule);padding:12px 0}
.list a{color:var(--ink);font-weight:600;text-decoration:none;font-size:17px}
.list a:hover{color:var(--accent)}
.list small{display:block;color:var(--muted);font:400 13.5px/1.45 system-ui,-apple-system,sans-serif;margin-top:3px}
h1.idx{font-size:clamp(28px,6vw,42px);line-height:1.1;margin:.2em 0 .3em}
h2.idx{font-size:21px;margin:28px 0 6px}
@media (max-width:520px){.sheet{padding:16px 14px}.otsc-tabs{margin-left:-14px !important;margin-right:-14px !important}}
"""
THEME_JS = """(function(){var r=document.documentElement,b=document.getElementById('theme');
function cur(){return r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'night':'paper');}
function show(){b.textContent='Page: '+(cur()==='night'?'Night':'Paper');}
try{var t=localStorage.getItem('otsc_theme');if(t)r.setAttribute('data-theme',t);}catch(e){}
show();b.addEventListener('click',function(){var n=cur()==='night'?'paper':'night';r.setAttribute('data-theme',n);try{localStorage.setItem('otsc_theme',n);}catch(e){}show();});
try{matchMedia('(prefers-color-scheme: dark)').addEventListener('change',show);}catch(e){}})();"""
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400&display=swap" rel="stylesheet">'
FOOT = '<footer>observe.the.system · Observe. Collapse. Reignite.</footer>'

def data_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

def page(title, desc, back, body_js, data):
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n%s\n<style>%s\n%s</style>\n</head>\n<body>\n'
            '<div class="wrap"><div class="top">%s<button type="button" id="theme">Page</button></div>'
            '<main class="sheet" id="root"></main>%s</div>\n'
            '<script type="application/json" id="data">%s</script>\n<script>%s</script>\n<script>%s\n%s</script>\n</body>\n</html>\n') % (
        html.escape(title), html.escape(desc or ''), FONT, CSS, PAGE_CSS, ('<a href="%s">%s</a>' % back) if back else '<span>observe.the.system</span>', FOOT, data_json(data), JS, THEME_JS, body_js)

out_d = os.path.join(ROOT, 'modules', 'dashboards'); out_m = os.path.join(ROOT, 'modules', 'maps'); out_x = os.path.join(ROOT, 'export')
for p in (out_d, out_m, out_x): os.makedirs(p, exist_ok=True)

DASH_JS = "var d=JSON.parse(document.getElementById('data').textContent),r=document.getElementById('root');r.innerHTML=OTSCharts.dashboard(d,{level:'h1'});OTSCharts.wire(r);"
MAP_JS = "var m=JSON.parse(document.getElementById('data').textContent),r=document.getElementById('root');r.innerHTML=OTSCharts.map(m,{header:true,level:'h1',steps:true});"
for k, d in DASH.items():
    open(os.path.join(out_d, k + '.html'), 'w', encoding='utf-8').write(page(d['title'], d.get('sub', ''), ('../index.html', '← All modules'), DASH_JS, d))
for k, m in MAPS.items():
    open(os.path.join(out_m, k + '.html'), 'w', encoding='utf-8').write(page(m['title'], m.get('sub', ''), ('../index.html', '← All modules'), MAP_JS, m))

def li(href, t, sub): return '<li><a href="%s">%s</a><small>%s</small></li>' % (href, html.escape(t), html.escape(sub or ''))
idx_body = ('<p class="otsc-eyebrow" style="font:700 11px/1.3 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0">Observe The System</p>'
            '<h1 class="idx">The Israel Architecture: dashboards and maps</h1><p style="color:var(--muted);font-style:italic;margin:0">Each module is a single page that works on its own. Every figure comes from a cited scene in the simulation.</p>'
            '<h2 class="idx">Dashboards (%d)</h2><ul class="list">%s</ul><h2 class="idx">Maps (%d)</h2><ul class="list">%s</ul>') % (
    len(DASH), ''.join(li('dashboards/%s.html' % k, d['title'], d.get('sub')) for k, d in DASH.items()),
    len(MAPS), ''.join(li('maps/%s.html' % k, ('Network: ' if m.get('kind') == 'network' else 'Flow: ') + m['title'], m.get('sub')) for k, m in MAPS.items()))
idx = page('The Israel Architecture: modules', 'Standalone dashboards and maps from the Israel Architecture simulation.', None,
           "document.getElementById('root').innerHTML=JSON.parse(document.getElementById('data').textContent);", idx_body)
open(os.path.join(ROOT, 'modules', 'index.html'), 'w', encoding='utf-8').write(idx)

json.dump(DASH, open(os.path.join(out_x, 'dashboards.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(MAPS, open(os.path.join(out_x, 'maps.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

README = r"""# Data export: the Israel Architecture

Three JSON files, all regenerated from `index.html` by the build. `dashboards.json` and `maps.json` come from
`tools/export_modules.py`; `library.json` comes from `tools/embed_book.py` and is byte-for-byte the payload the
single-file app embeds (it escapes `</` as `<\/`, which is valid JSON). `tools/charts.js` is a working reference
renderer for the first two; the standalone pages in `modules/` show its output.

## dashboards.json

An object keyed by dashboard id (`aid_arms`, `congress_money`, …). Each value is
`{title, sub, tabs: [{name, sections: [panel, …]}], sources: [[label, url], …]}`; `url` may be an empty string,
in which case show the label without a link. A panel is a tagged union on `type`:

| type | fields | notes |
|---|---|---|
| `kpis` | `items: [[value, label]]` | `value` is a display string ("~$300B"); `label` may hold `<b>`/`<i>` |
| `explain` | `title, icon, paras: [html]` | prose; `paras` may hold `<b>`/`<i>`; `icon` is an emoji |
| `note` | `html` | a short prose note, `<b>`/`<i>` allowed |
| `hbar` | `title, cap?, unit, data: [[label, value, colour?, valueLabel?]], highlight?, labelW?` | `highlight: n` marks the first n rows (n = 0 marks none); `colour` is a hex override; `valueLabel` replaces the formatted number |
| `stacked` | `title, cap?, unit, series: [name], data: [[label, [v1, v2, …]]], labelW?, colors?` | one bar per row, one segment per series |
| `line` | `title, cap?, unit?, data: [[x, y, yLabel?]]` | `x` is numeric (usually a year; in one panel, a day count) |
| `donut` | `title, cap?, unit?, center, centerSub, data: [[label, value, colour?, valueLabel?]]` | `colour` may be `null` |
| `pair` | `title, cap?, a, b, max?, data: [[label, aValue, bValue, aLabel, bLabel, note]]` | with `max`, every row shares one 0–max scale; without it each row is scaled on its own, because rows mix units |
| `table` | `title, cap?, cols: [..], rows: [[..]], num?, highlight?, foot?` | `num: true` right-aligns columns after the first; `highlight: n` marks the first n rows |
| `flow` | `title, kicker?, cap?, steps: [[pill, title, note]], loop?` | a vertical list of steps; `loop` is a closing "feedback" line |
| `grid` | `items: [panel]` | lay the child panels side by side when there is room |

`unit` is one of `''`, `'$'` (raw dollars, shown as $1.2M), `'$B'`, `'$M'`, `'%'`, or a word (`'years'`).
Whenever a label string is supplied (`valueLabel`, `yLabel`, `aLabel`), show it exactly as given: it carries
the source's own rounding and qualifiers ("~", "+", ranges). Plot the numeric value. Hex colours were chosen
for the simulation's light theme; map them to your theme palette rather than using them literally.

## maps.json

An object keyed by map id. Each value is `{kind: 'flow' | 'network', title, sub, H, nodes, edges, steps}`.
`nodes: [{id, l, s, x, y, sc?, k?}]`: `l` is the label, `s` a one-line subtitle, `x` in 0–400 and `y` in 0–`H`
(a portrait canvas, about 400 × 500–850), `sc` the simulation scene that documents the node, and `k` an
optional role: `israel` (the State of Israel, drawn inverted), `center` (the subject of a network map) or
`origin` (where a flow begins). `edges: [{f, t, l, k}]` run from node `f` to node `t` with a short label; `k`
is `money`, `authority`, `tie` (a documented relationship), `loop` (feedback or pressure) or `blocked` (a
claimed link the record does not support; draw it dashed and say so). For network maps, the number of steps
from the `israel` node, counted over every edge except `blocked`, is shown as a badge (1°, 2°, …).
`steps: [{t, x, show: [id], hl: [id], sc, ed}]` drive the step-through: `t` a title, `x` the narration, `show`
the nodes visible at that step, `hl` the ones highlighted.

## library.json

The reading-mode payload: `{cites: {key: [url, label]}, title, tagline, note, books: [...]}`. A book is
`{id, vol, status: 'ready' | 'preparing', title, subtitle, span, …}`; ready books add `intro` (HTML),
`unit` and `chapters: [{id, label, title, span, intro, outro, outroTitle?, sections}]`, and a section is
`{s, h, html, scene?, draws?}`. Section HTML uses three inline markers the reader resolves at render time:
`[cite:key]` (a numbered note, looked up in `cites` or the simulation's own citation table),
`[scene:id|label]` (a cross-reference to a simulation scene), and the figure tags documented in
`book/FIGURES.md`, including `<figure class="fig-dash" data-ref="DASHBOARD_ID:TAB NAME:INDEX">` and
`<figure class="fig-map" data-map="MAP_ID">`, which pull a panel or a map from the two files above.
Preparing books carry only shelf metadata (`count`, `first`, `keywords`).
"""
open(os.path.join(out_x, 'README.md'), 'w', encoding='utf-8').write(README)
print('modules: %d dashboards, %d maps -> modules/; export/dashboards.json, export/maps.json, export/README.md' % (len(DASH), len(MAPS)))
