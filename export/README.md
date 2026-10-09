# Data export: the Israel Architecture

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
