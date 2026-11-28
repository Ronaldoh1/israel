"""Export the Epstein network as a self-contained package (same shape as Ron's Network Intelligence v1.0):
nodes.csv, edges.csv, sources.csv, network.json (edges carry resolved source links), index.html (the explorer),
plus the code to edit and rebuild it. Usage: python3 export_package.py OUTDIR"""
import csv, json, os, shutil, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]
spec = importlib.util.spec_from_file_location('bx', os.path.join(HERE, 'build_explorer.py'))
argv = sys.argv; sys.argv = [argv[0]]; bx = importlib.util.module_from_spec(spec); spec.loader.exec_module(bx); sys.argv = argv
d = bx.d
edges = [dict(e, refs=bx.resolve(e['src'], None)) for e in d['edges']]
os.makedirs(os.path.join(OUT, 'code'), exist_ok=True)
json.dump({'built': d['built'], 'nodes': d['nodes'], 'edges': edges}, open(os.path.join(OUT, 'network.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(OUT, 'nodes.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'label', 'type', 'cluster', 'level', 'detail', 'money_or_protection_source'])
    for n in d['nodes']: w.writerow([n['id'], n['name'], n['kind'], n['cluster'], n.get('tier', ''), n['note'], 'yes' if n.get('sponsor') else ''])
srcs = {}
with open(os.path.join(OUT, 'edges.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'source', 'target', 'rel', 'kind', 'status', 'source_ids', 'source_text'])
    for i, e in enumerate(edges, 1):
        ids = []
        for r in e['refs']:
            key = r['u'] or r['t']
            if key not in srcs: srcs[key] = ('S%d' % (len(srcs) + 1), r['t'], r['u'] or '')
            ids.append(srcs[key][0])
        w.writerow(['E%03d' % i, e['f'], e['t'], e['label'], e['type'], e['status'], ';'.join(ids), e['src']])
with open(os.path.join(OUT, 'sources.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'title', 'url'])
    for k, (sid, t, u) in srcs.items(): w.writerow([sid, t, u])
open(os.path.join(OUT, 'index.html'), 'w').write(bx.build(None))
for fn in ['build_data.py', 'build_explorer.py', 'graph_explorer_template.html', 'graph_walk.py', 'export_package.py']:
    shutil.copy(os.path.join(HERE, fn), os.path.join(OUT, 'code', fn))
open(os.path.join(OUT, 'code', 'rebuild_html.py'), 'w').write('''"""Rebuild index.html from network.json and the template, with no other files needed.
Usage (from the package folder): python3 code/rebuild_html.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(H)
d = json.load(open(os.path.join(P, 'network.json')))
for e in d['edges']: e.setdefault('refs', [{'t': p.strip(), 'u': None} for p in e['src'].split(';') if p.strip()])
t = open(os.path.join(H, 'graph_explorer_template.html')).read()
open(os.path.join(P, 'index.html'), 'w').write(t.replace('__DATA__', json.dumps(d, ensure_ascii=False).replace('</', '<\\\\/')))
print('index.html rebuilt:', len(d['nodes']), 'nodes,', len(d['edges']), 'edges')
''')
open(os.path.join(OUT, 'code', 'analyze.py'), 'w').write('''"""Graph analysis over network.json (pip install networkx).
Removes the centre (Epstein, Maxwell), keeps verified, non-probe, non-kinship ties, then reports
components, betweenness, and whether named pairs still connect. Usage: python3 code/analyze.py"""
import json, os, networkx as nx
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(P, 'network.json')))
PROBE = {'investigation','testimony','litigation','reporting','claim','complaint','oversight','allegation to Congress','forensic review','court ruling'}
G = nx.Graph()
for e in d['edges']:
    if e['status'] == 'verified' and e['type'] not in PROBE and e['type'] != 'kinship': G.add_edge(e['f'], e['t'])
H = G.copy(); H.remove_nodes_from(['epstein', 'gmax'])
cs = sorted(nx.connected_components(H), key=len, reverse=True)
print('largest pieces without Epstein and Maxwell:', [len(c) for c in cs[:5]])
bc = nx.betweenness_centrality(H)
print('strongest connectors:'); [print('  %-22s %.3f' % kv) for kv in sorted(bc.items(), key=lambda x: -x[1])[:10]]
for a, b in [('jpm','deutsche'), ('jpm','bofa'), ('rothschild_group','jpm'), ('black','jpm'), ('wexner','barak')]:
    try: print(a, '->', b, ':', ' > '.join(nx.shortest_path(H, a, b)))
    except Exception: print(a, '->', b, ': no path without Epstein')
''')
open(os.path.join(OUT, 'README.md'), 'w').write('''# The Epstein Architecture — network package

Built %s. %d nodes, %d edges. Same shape as Network Intelligence v1.0.

| File | What it is |
|---|---|
| `index.html` | The interactive explorer. Open it in any browser; works offline. |
| `network.json` | Every node and edge; each edge carries its resolved source links (`refs`). |
| `nodes.csv` / `edges.csv` / `sources.csv` | The same data as spreadsheets. `edges.source_ids` point into `sources.csv`. |
| `code/build_data.py` | The source of truth in the repo: every node `n(...)` and edge `e(...)` with status and source. |
| `code/rebuild_html.py` | Rebuilds `index.html` from `network.json` alone. |
| `code/analyze.py` | networkx analysis: components, connectors, paths with Epstein removed. |
| `code/graph_walk.py` | Breadth-first walk, backward walk, loops (writes graph_report.md). |
| `code/build_explorer.py`, `code/export_package.py` | Repo builders (need the library repo for source resolution). |

Edge status: `verified` (documented) · `to-verify` (reported or a lead) · `not-established` (claim the record does not support) · `withheld` (records known to exist, not released) · `probable`.

Rules: ties come from documents only, never identity; family members are separate nodes joined by a kinship edge; a contract, an invoice and a transfer are different events; a suspicious-activity report is not a finding; investigations and testimony are probes, not ties, and are left out of loops and connector analysis.

To edit: change the data in `network.json` (or `build_data.py` in the repo), then `python3 code/rebuild_html.py`.
''' % (d['built'], len(d['nodes']), len(edges)))
print('package:', OUT, len(d['nodes']), 'nodes', len(edges), 'edges', len(srcs), 'sources')
