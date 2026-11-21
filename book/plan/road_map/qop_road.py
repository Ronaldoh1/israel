"""Stored per-node profile ("qop") for the 1948 network, same fields as the Epstein map so one explorer serves both.
kb_epstein / kb_maxwell hold the distance to this map's two anchors (ANCHORS), chosen as the two
most-bridging nodes of the documented-tie graph. Only reviewed ties count (verified or reported, never co-mentions)."""
import json, os, re, glob, collections
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
MONEY = {'funding', 'purchase', 'sale', 'ownership'}
ROLE = {'zionist movement': 'movement leadership', 'finance': 'finance and land', 'land': 'finance and land', 'rothschild': 'finance and land',
        'british state': 'British state', 'international': 'international body or instrument', 'israel state': 'Israeli state',
        'militias': 'armed organization', 'ottoman': 'Ottoman state', 'arab leadership': 'Palestinian Arab leadership',
        'arab states': 'Arab states', 'us government': 'US government', 'us lobby': 'American organizing', 'nazi germany': 'Nazi Germany',
        'europe': 'European powers', 'soviet bloc': 'Soviet bloc', 'religion': 'religious institution or dissent',
        'christian zionism': 'Christian Zionism', '1948 war': '1948 war', 'settlement': 'colony or settlement', 'intelligence': 'intelligence', 'us parties': 'US party politics', 'cold war': 'Cold War event or pact'}


def run(path=os.path.join(HERE, 'network.json')):
    d = json.load(open(path))
    N = {x['id']: x for x in d['nodes']}
    E = d['edges']
    G = nx.Graph()
    for e in E:
        if e['status'] in ('verified', 'reported') and e['type'] != 'kinship':
            G.add_edge(e['f'], e['t'], type=e['type'])
    bc = nx.betweenness_centrality(G)
    A, B = [k for k, _ in sorted(bc.items(), key=lambda x: -x[1])[:2]]
    dA = nx.single_source_shortest_path_length(G, A); dB = nx.single_source_shortest_path_length(G, B)
    pA = nx.single_source_shortest_path(G, A)
    H = G.copy(); H.remove_nodes_from([A, B]); bcH = nx.betweenness_centrality(H)
    rank = {k: i + 1 for i, (k, _) in enumerate(sorted(bc.items(), key=lambda x: -x[1]))}
    rankH = {k: i + 1 for i, (k, _) in enumerate(sorted(bcH.items(), key=lambda x: -x[1]))}
    loops = collections.defaultdict(list)
    for c in nx.cycle_basis(G):
        if 3 <= len(c) <= 5:
            s = ' – '.join(N[x]['name'] for x in c)
            for x in c: loops[x].append(s)
    # other library volumes that name the node (cross-series)
    V = json.load(open(os.path.join(REPO, 'book/plan/volumes.json')))
    st2vol = {}
    for k, v in V.items():
        if k.startswith('_') or not isinstance(v, dict): continue
        for c in v.get('stages', []): st2vol[c['id'] if isinstance(c, dict) else c] = v.get('title', k)
    text = collections.defaultdict(str)
    for dd in glob.glob(os.path.join(REPO, 'book/part1/*/')):
        st = dd.rstrip('/').split('/')[-1]
        vol = st2vol.get(st)
        if not vol: continue
        for f in glob.glob(dd + '*.html'): text[vol] += ' ' + re.sub(r'<[^>]+>', ' ', open(f, errors='replace').read())
    tier = {0: 'anchor', 1: 'Direct 1°', 2: 'Operational 2°', 3: 'Strategic 3°'}
    for n in d['nodes']:
        i = n['id']; mine = [e for e in E if i in (e['f'], e['t'])]
        st = collections.Counter(e['status'] for e in mine)
        srcs = set(p.strip() for e in mine if e['status'] != 'co-mention' for p in str(e.get('src', '')).split(';') if p.strip())
        k = dA.get(i)
        q = {'tier': tier.get(k, '4°+' if k is not None else 'no reviewed tie yet'),
             'kb_epstein': k, 'kb_maxwell': dB.get(i),
             'path_epstein': [N[x]['name'] for x in pA.get(i, [])][::-1] if k else [],
             'ties': {'total': len(mine) - st['co-mention'], 'verified': st['verified'], 'reported': st['reported'], 'to_verify': st['to-verify'],
                      'withheld': 0, 'not_established': st['co-mention'], 'documented': G.degree(i) if i in G else 0},
             'centrality': {'betweenness': round(bc.get(i, 0), 4), 'rank': rank.get(i),
                            'betweenness_without_hubs': round(bcH.get(i, 0), 4), 'rank_without_hubs': rankH.get(i)},
             'role': ROLE.get(n['cluster'], n['cluster']),
             'money_in': [f"{N[e['f']]['name']}: {e['label'][:140]}" for e in mine if e['t'] == i and e['type'] in MONEY and e['status'] != 'co-mention'][:6],
             'money_out': [f"{N[e['t']]['name']}: {e['label'][:140]}" for e in mine if e['f'] == i and e['type'] in MONEY and e['status'] != 'co-mention'][:6],
             'loops': loops.get(i, [])[:6], 'succession': None, 'flight': None, 'volumes': {},
             'sources': {'distinct': len(srcs), 'doj_efta': 0},
             'open_leads': [f"{N[e['t'] if e['f'] == i else e['f']]['name']}" for e in sorted(mine, key=lambda e: -e.get('n', 1)) if e['status'] == 'co-mention'][:8],
             'functions': [], 'sections': n.get('sections', []), 'mentions': n.get('mentions', 0)}
        nm = re.sub(r'\s*\(.*?\)', '', n['name']).split(' / ')[0].strip()
        if len(nm) >= 5:
            pat = re.compile(r'\b' + re.escape(nm) + r'\b')
            for vol, t in text.items():
                c = len(pat.findall(t))
                if c: q['volumes'][vol] = c
        n['qop'] = q
    d['qop_meta'] = {'graph': 'reviewed ties (verified or reported), kinship excluded', 'nodes': G.number_of_nodes(), 'edges': G.number_of_edges(),
                     'anchors': [A, B], 'anchor_names': [N[A]['name'], N[B]['name']]}
    json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
    return d


if __name__ == '__main__':
    d = run(); print(d['qop_meta'])
