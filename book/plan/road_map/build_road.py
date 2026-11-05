"""Build the 1948 network (The Baseline + The Road to 1948) -> network.json.

Nodes come from registry.py (curated actors, institutions, documents, events).
Edges come from two sources, both already sourced in the library:
  1. the book text: a sentence that names two nodes and states a relationship (founded, funded,
     wrote to, signed, led, opposed, expelled...) becomes a typed edge; its citations are the edge's sources;
  2. the simulation scenes: an authored connection between two scene cards that map to nodes.
A sentence that names two nodes without a stated relationship is kept as 'co-mention', a lead only,
never used for analysis. Curated corrections live in road_layer.json.
"""
import json, os, re, glob, html, collections
import registry

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
STAGES = ['ch01'] + ['rd%d' % i for i in range(7)] + ['cw%d' % i for i in range(1, 7)]
BOOK_OF = {'ch01': 'The Baseline'} | {('rd%d' % i): 'The Road to 1948' for i in range(7)} | {('cw%d' % i): 'The Cold War Architecture' for i in range(1, 7)}

NODES = registry.load()
NID = {n['id']: n for n in NODES}

# ---- alias matcher (longest alias first; stage-scoped aliases only in that stage) ----
PATS = []
for n in NODES:
    for a, st in n['aliases']:
        PATS.append((len(re.sub(r'\\.|\(\?.*?\)', 'x', a)), re.compile(r'(?<![\w-])' + a + r'(?![\w])'), n['id'], st))
PATS.sort(key=lambda x: -x[0])


def find(text, stage):
    taken = [False] * len(text); hits = []
    for _, p, nid, st in PATS:
        if st and st != stage: continue
        for m in p.finditer(text):
            a, b = m.span()
            if a == b or any(taken[a:b]): continue
            for k in range(a, b): taken[k] = True
            hits.append((a, b, nid))
    hits.sort()
    return hits


# ---- relation typing from the words between two mentions ----
REL = [
    ('funding', r'\b(fund(?:ed|s|ing)?|financ\w*|paid|pay(?:s|ing)?|donat\w*|raised|loan\w*|lent|bought|purchas\w*|sold|sell\w*|invest\w*|bankroll\w*|subsidi\w*|grant(?:ed)? .{0,20}(?:£|\$))'),
    ('founding', r'\b(found(?:ed|er|ers|ing)|establish\w*|creat(?:ed|ing)|set up|incorporat\w*|co-found\w*|launched|organi[sz]ed)\b'),
    ('correspondence', r'\b(wrote|writ(?:es|ing)|letter|addressed|cabl\w*|telegram\w*|memo\w*|petition\w*|message)\b'),
    ('meeting', r'\b(met|meet(?:s|ing)?|negotiat\w*|talks|audience|received|visited|conferr\w*|discussed)\b'),
    ('agreement', r'\b(sign(?:ed|ing|atory)|agreement|agreed|treaty|accord|deal|contract\w*|concession)\b'),
    ('leadership', r'\b(led|lead(?:s|ing|er)|head(?:ed|s)?|chair\w*|president|director|secretary|appoint\w*|named .{0,15}as|succeed\w*|commanded|command(?:er)?|governor|minister)\b'),
    ('membership', r'\b(member\w*|joined|serv(?:ed|ing)|worked for|employ\w*|staff|delegate|represent\w*|agent)\b'),
    ('opposition', r'\b(oppos\w*|against|reject\w*|refus\w*|veto\w*|condemn\w*|protest\w*|denounc\w*|resist\w*|blocked|split from|broke with|fought)\b'),
    ('violence', r'\b(attack\w*|bomb\w*|kill\w*|murder\w*|massacr\w*|expel\w*|expuls\w*|assassinat\w*|captur\w*|destroy\w*|raid\w*|shot)\b'),
    ('official act', r'\b(issu\w*|approv\w*|adopt\w*|ratif\w*|recogni[sz]\w*|vot(?:ed|e|ing)|enact\w*|passed|endors\w*|incorporated into|award\w*|promis\w*|declar\w*|announc\w*|annex\w*)\b'),
    ('pressure', r'\b(lobb\w*|press(?:ed|ure)|urg\w*|persuad\w*|pushed|campaign\w*|demand\w*|warn\w*|advis\w*)\b'),
    ('supply', r'\b(arms|weapons|rifles|aircraft|planes|shipped|smuggl\w*|procur\w*|supplied|airlift\w*)\b'),
]
REL = [(t, re.compile(p, re.I)) for t, p in REL]


def rel(between, whole):
    for t, p in REL:
        if p.search(between): return t
    return None


# ---- sentence splitter that keeps each sentence's own citations ----
ABBR = r'(?:St|Mr|Mrs|Dr|Sir|Gen|Col|Lt|Capt|Rev|No|vol|pp|p|c|ca|Jr|Sr|U\.S|U\.N|U\.K|e\.g|i\.e|Co|Ltd|Inc|vs|Mt|Ft|Hon)'
def sentences(txt):
    out = []; buf = ''; i = 0
    parts = re.split(r'(\[cite:[^\]]+\])', txt)
    seq = []
    for p in parts:
        if p.startswith('[cite:'): seq.append(('c', p[6:-1]))
        else:
            for piece in re.split(r'(?:(?<=[.!?])|(?<=[.!?]["”’)]))\s+(?=[A-Z“"‘(])', p):
                seq.append(('t', piece))
    cur = {'t': '', 'c': []}
    for k, v in seq:
        if k == 'c': cur['c'].append(v); continue
        if cur['t'] and (cur['c'] or re.search(r'[.!?]["”’)]?\s*$', cur['t'])) and not re.search(r'\b' + ABBR + r'\.\s*$', cur['t']):
            out.append(cur); cur = {'t': '', 'c': []}
        cur['t'] = (cur['t'] + ' ' + v).strip() if cur['t'] else v.strip()
    if cur['t']: out.append(cur)
    # a sentence without its own citation takes the next citation in the same paragraph (the book cites at the end of a run)
    nxt = []
    for x in reversed(out):
        if x['c']: nxt = x['c']
        elif nxt: x['c'] = nxt[:1]; x['inherit'] = True
    return out


def corpus():
    for st in STAGES:
        for f in sorted(glob.glob(os.path.join(ROOT, 'book/part1', st, '*.html'))):
            sec = os.path.basename(f)[:-5]
            if sec.startswith('_'): continue
            t = open(f, encoding='utf-8').read()
            # figures and tables: each cell takes the figure's own source line
            for fig in re.findall(r'<figure[\s\S]*?</figure>', t):
                fs = ' '.join(re.findall(r'\[cite:[^\]]+\]', ' '.join(re.findall(r'<p class="fig-src">([\s\S]*?)</p>', fig))))
                for row in re.findall(r'<(tr|li|div class="[^"]*(?:node|step|item|ev)[^"]*")[^>]*>([\s\S]*?)</(?:tr|li|div)>', fig):
                    cell = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', row[1])).split())
                    if cell and fs: yield st, sec, cell.rstrip('.') + '. ' + fs
            t = re.sub(r'<figure[\s\S]*?</figure>', '', t)
            for blk in re.findall(r'<(p|li|td|blockquote)[^>]*>([\s\S]*?)</\1>', t):
                txt = ' '.join(html.unescape(re.sub(r'<[^>]+>', '', blk[1])).split())
                txt = re.sub(r'\[scene:[^\]|]+\|([^\]]+)\]', r'\1', txt)
                if txt: yield st, sec, txt


def main():
    ev = collections.defaultdict(list)          # (f, t, type) -> [(sentence, cites, sec)]
    mentions = collections.defaultdict(collections.Counter)  # node -> sec counts
    first = {}
    for st, sec, txt in corpus():
        for s in sentences(txt):
            text = s['t']
            hits = find(text, st)
            ids = []
            for a, b, nid in hits:
                mentions[nid][sec] += 1
                if nid not in first and s['c']: first[nid] = (text, s['c'], sec)
                if not ids or ids[-1][2] != nid: ids.append((a, b, nid))
            seen = set()
            for x in range(len(ids)):
                for y in range(x + 1, min(len(ids), x + 3)):
                    a, b = ids[x], ids[y]
                    if a[2] == b[2] or (a[2], b[2]) in seen: continue
                    seen.add((a[2], b[2]))
                    between = text[a[1]:b[0]]
                    t = rel(between, text) if (len(between) < 110 and y == x + 1) else None
                    f_, t_ = a[2], b[2]
                    if t and re.search(r'\b(?:was|were|been|being)\s+\w+ed\b.*\bby\b|\bby\b', between) and t in ('founding', 'funding', 'leadership', 'official act', 'violence', 'opposition'):
                        f_, t_ = t_, f_
                    ev[(f_, t_, t or 'co-mention')].append((text, s['c'], sec))

    # ---- scene connections ----
    idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    CH = json.loads(re.search(r'window\.CHAPTERS = (\[.*?\]);\n', idx, re.S).group(1))
    SC = {x['id']: x for x in json.loads(re.search(r'<script id="scenedata" type="application/json">(.*?)</script>', idx, re.S).group(1))}
    scen = [(c['id'], sid) for c in CH if c['id'] in STAGES for sid in c['scenes']]
    notes = {}
    CTY = {'financial': 'funding', 'formation': 'founding', 'political': 'political', 'covert': 'covert', 'authority': 'official act',
           'violent': 'violence', 'dynastic': 'kinship', 'military': 'supply', 'media': 'media', 'tie': 'association'}
    for st, sid in scen:
        sc = SC.get(sid)
        if not sc: continue
        emap = {}
        for e in sc['ents']:
            h = find(e['nm'], st)
            if len(h) == 1 or (h and len({x[2] for x in h}) == 1):
                emap[e['id']] = h[0][2]
                if h[0][2] not in notes and len(e.get('dt', '')) > 80 and (h[0][1] - h[0][0]) >= len(e['nm'].split(' — ')[0].split(',')[0]) - 6:
                    notes[h[0][2]] = re.sub(r'\[(?:cite:|scene:)[^\]]*\]', '', e['dt']).strip()
        for c in sc.get('cs', []):
            f, t = emap.get(c['f']), emap.get(c['t'])
            if f and t and f != t and c.get('ty') in CTY:
                ev[(f, t, CTY[c['ty']])].append((sc['t'] + ': ' + sc.get('sub', ''), [sid], sid))

    # ---- assemble ----
    used = {n for k in ev for n in k[:2]} | set(mentions)
    nodes = []
    for n in NODES:
        if n['id'] not in used: continue
        secs = mentions[n['id']]
        note = notes.get(n['id'])
        if not note and n['id'] in first:
            note = first[n['id']][0]
        books = sorted({BOOK_OF[s] for s in STAGES for sec in secs if sec.startswith(s + '_') or sec.split('_')[0] == s}) or []
        nodes.append({'id': n['id'], 'name': n['name'], 'kind': n['kind'], 'cluster': n['cluster'], 'note': (note or '')[:700],
                      'mentions': sum(secs.values()), 'sections': [s for s, _ in secs.most_common(8)]})
    edges = []
    for (f, t, ty), L in ev.items():
        L.sort(key=lambda x: (not x[1], len(x[0])))
        best = L[0]
        cites = []
        for x in L:
            for c in x[1]:
                if c not in cites: cites.append(c)
        lab = best[0] if len(best[0]) <= 260 else best[0][:257].rsplit(' ', 1)[0] + '…'
        status = 'co-mention' if ty == 'co-mention' else ('verified' if best[1] else 'to-verify')
        edges.append({'f': f, 't': t, 'label': lab, 'type': ty, 'status': status, 'src': '; '.join(cites[:6]),
                      'n': len(L), 'sec': best[2]})
    # my review of every typed candidate against its sentence (review.json): A accept, X not a tie,
    # T:type retype, DT:type reverse and retype, R:f>t:type the sentence documents a different pair
    rv = json.load(open(os.path.join(HERE, 'review.json'))) if os.path.exists(os.path.join(HERE, 'review.json')) else {}
    for e in edges:
        d = rv.get(e['f'] + '>' + e['t'] + '|' + e['type'])
        if e['type'] == 'co-mention' and d is None: continue
        if d is None: e['status'] = 'to-verify'; continue
        if d == 'X': e['type'] = 'co-mention'; e['status'] = 'co-mention'; continue
        if d.startswith('DT:'): e['f'], e['t'] = e['t'], e['f']; e['type'] = d[3:]
        elif d.startswith('T:'): e['type'] = d[2:]
        elif d.startswith('R:'):
            pair, ty = d[2:].rsplit(':', 1); e['f'], e['t'] = pair.split('>'); e['type'] = ty
        if e['src']: e['status'] = 'verified'
        else: e['status'] = 'reported'; e['src'] = e['sec']   # stated in the book, no citation in that paragraph: links to the section
    # collapse duplicates created by retyping
    seen = {}
    for e in edges:
        k = (e['f'], e['t'], e['type'])
        if k in seen and e['type'] != 'co-mention':
            seen[k]['n'] += e['n']; continue
        seen.setdefault(k, e)
    edges = list(seen.values())
    # curated corrections
    for lp in [os.path.join(HERE, x) for x in ('road_layer.json', 'us_layer.json', 'world_layer.json', 'cold_layer.json', 'history_layer.json', 'funding_layer.json', 'un_layer.json', 'global_layer.json')]:
        if not os.path.exists(lp): continue
        L = json.load(open(lp))
        rm = {tuple(x) for x in L.get('remove_edges', [])}
        edges = [e for e in edges if (e['f'], e['t'], e['type']) not in rm]
        ids = {n['id'] for n in nodes}
        for e in L.get('edges', []):
            edges.append(dict({'n': 1, 'sec': ''}, **e))
        for i, txt in L.get('node_notes', {}).items():
            app = i.startswith('+'); i = i.lstrip('+')   # '+id' appends to the note already there
            for n in nodes:
                if n['id'] == i: n['note'] = ((n.get('note') or '') + ' ' + txt).strip() if app else txt
    have = {n['id'] for n in nodes}
    for e in edges:
        for x in (e['f'], e['t']):
            if x not in have:
                n = NID[x]; have.add(x)
                nodes.append({'id': x, 'name': n['name'], 'kind': n['kind'], 'cluster': n['cluster'], 'note': notes.get(x, ''), 'mentions': 0, 'sections': []})
    json.dump({'built': '2026-11-04', 'title': 'The Road to 1948 Network', 'nodes': nodes, 'edges': edges},
              open(os.path.join(HERE, 'network.json'), 'w'), ensure_ascii=False, indent=1)
    c = collections.Counter(e['status'] for e in edges); ct = collections.Counter(e['type'] for e in edges)
    print(len(nodes), 'nodes', len(edges), 'edges', dict(c)); print(dict(ct.most_common()))


if __name__ == '__main__':
    main()
    import qop_road; print('profiles', qop_road.run()['qop_meta'])
    import viability; print('viability', viability.run()[0]['viability_meta']['groups']['Rothschild family and houses'])
