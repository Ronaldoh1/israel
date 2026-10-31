"""Breadth-first expansion, backward walk and loop detection over network.json.
Usage: python3 graph_walk.py [root] [max_depth]   -> writes graph_report.md
Rules: 'not-established' edges are listed but never walked; probe-type edges
(investigation, testimony, litigation, reporting, claim, complaint, oversight,
allegation to Congress) are not ties between people and are left out of loops."""
import json, sys
from collections import defaultdict, deque

d = json.load(open('network.json'))
N = {n['id']: n for n in d['nodes']}
E = d['edges']
root = sys.argv[1] if len(sys.argv) > 1 else 'epstein'
maxd = int(sys.argv[2]) if len(sys.argv) > 2 else 4
PROBE = {'investigation', 'testimony', 'litigation', 'reporting', 'claim', 'complaint',
         'oversight', 'allegation to Congress', 'forensic review', 'court ruling'}

walk = [e for e in E if e['status'] != 'not-established']
adj = defaultdict(list)          # undirected, for expansion
inb = defaultdict(list)          # directed: who sent something to x
for e in walk:
    adj[e['f']].append((e['t'], e)); adj[e['t']].append((e['f'], e))
    inb[e['t']].append(e)

# 1. breadth-first expansion
depth = {root: 0}; parent = {}
q = deque([root])
while q:
    u = q.popleft()
    if depth[u] >= maxd: continue
    for v, e in sorted(adj[u], key=lambda x: x[0]):
        if v not in depth:
            depth[v] = depth[u] + 1; parent[v] = (u, e); q.append(v)
layers = defaultdict(list)
for k, v in depth.items(): layers[v].append(k)

# 2. backward walk: follow inbound edges upward from root until nothing sends further
up_seen = {root}; up_rows = []
q = deque([(root, 0)])
while q:
    u, k = q.popleft()
    for e in inb[u]:
        if e['type'] in PROBE: continue
        s = e['f']
        up_rows.append((k + 1, s, u, e))
        if s not in up_seen:
            up_seen.add(s); q.append((s, k + 1))
stops = sorted({s for _, s, _, _ in up_rows if not [x for x in inb[s] if x['type'] not in PROBE]})

# 3. loops: simple cycles of length 3-5 in the undirected tie graph, root excluded
tie = defaultdict(set)
for e in walk:
    if e['type'] in PROBE or e['status'] != 'verified': continue
    if root in (e['f'], e['t']): continue
    tie[e['f']].add(e['t']); tie[e['t']].add(e['f'])
loops = set()
def dfs(start, cur, path):
    for v in tie[cur]:
        if v == start and len(path) >= 3:
            c = path[:]; i = c.index(min(c)); c = c[i:] + c[:i]
            if c[1] > c[-1]: c = [c[0]] + c[1:][::-1]
            loops.add(tuple(c))
        elif v not in path and len(path) < 5 and v > start:
            dfs(start, v, path + [v])
for s in tie: dfs(s, s, [s])
def only_kin(c):
    ts = []
    for a, b in zip(c, c[1:] + c[:1]):
        ts += [e['type'] for e in walk if {e['f'], e['t']} == {a, b}]
    return set(ts) <= {'kinship', 'office', 'ownership'}
loops = [c for c in loops if not only_kin(c)]

nm = lambda i: N[i]['name']
L = [f'# Network walk from {nm(root)}', '', f'{len(N)} nodes, {len(E)} edges; walked {len(walk)} (not-established edges excluded).', '',
     '## 1. Breadth-first expansion', '']
for k in sorted(layers):
    L.append(f'**Depth {k}** ({len(layers[k])}): ' + ', '.join(sorted(nm(i) for i in layers[k])))
    L.append('')
L += ['## 2. Backward walk (who sent what, upward)', '', '| Step | From | To | Tie | Status | Source |', '|---|---|---|---|---|---|']
for k, s, t, e in sorted(up_rows, key=lambda r: (r[0], r[1])):
    L.append(f"| {k} | {nm(s)} | {nm(t)} | {e['label']} | {e['status']} | {e['src']} |")
L += ['', '**Where the upward walk stops** (nothing documented sends to these): ' + ', '.join(nm(s) for s in stops), '',
      '## 3. Loops (verified ties, root excluded, 3–5 steps)', '']
for c in sorted(loops, key=len):
    L.append('- ' + ' → '.join(nm(i) for i in c) + ' → ' + nm(c[0]))
L += ['', '## 4. Not-established edges (listed, never walked)', '']
for e in E:
    if e['status'] == 'not-established':
        L.append(f"- {nm(e['f'])} → {nm(e['t'])}: {e['label']} ({e['src']})")
L += ['', '## 5. Unreached from the root', '', ', '.join(sorted(nm(i) for i in N if i not in depth)) or 'none']
open('graph_report.md', 'w').write('\n'.join(L) + '\n')
print('depths', {k: len(v) for k, v in sorted(layers.items())}, '| upward rows', len(up_rows), '| stops', len(stops), '| loops', len(loops))
