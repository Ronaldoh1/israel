"""Compute a stored analysis profile ("qop") for every node in network.json.

Run after build_data.py (it calls this at the end). Each node gets node['qop'] holding:
  tier / kb (documented degrees from Epstein and from Maxwell) / path to Epstein /
  tie counts by status / centrality (with and without the two hubs) / role /
  money in and out / short loops / role-aware succession coverage / flight-log counts /
  other library volumes that mention the node / source mix / open leads / framework functions.
Everything is computed from documented ties only, so the profile can be queried without recomputation.
"""
import json, os, re, glob, collections
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
PROBE = {'investigation', 'testimony', 'litigation', 'reporting', 'claim', 'complaint', 'oversight',
         'allegation to Congress', 'forensic review', 'court ruling', 'comparison', 'comparative methodology',
         'communications aggregate', 'flight passenger', 'custody'}
MONEY = {'funding', 'payment', 'loan', 'banking', 'investment', 'government grant', 'ownership', 'contract',
         'trustee', 'trust beneficiary change'}
OPS = {'employment', 'office', 'travel coordination', 'introduction', 'criminal case'}
HUBS = ['epstein', 'gmax']
OFFICE = ['kahn', 'indyke', 'hbrk', 'southern_trust', 'financial_trust', 'butterfly_trust', 'epstein_2018_trust',
          'epstein_2019_trust', 'plan_d', 'jege', 'hyperion', 'lsje', 'kyara', 'gratitude']


def run(path=os.path.join(HERE, 'network.json')):
    d = json.load(open(path))
    N = {x['id']: x for x in d['nodes']}
    E = d['edges']
    isdoc = lambda i: N[i]['kind'] == 'document' or N[i]['cluster'] in ('comparative', 'evidence', 'records', 'research')

    G = nx.Graph()
    for e in E:
        if e['status'] == 'verified' and e['type'] not in PROBE and e['type'] != 'kinship' \
                and not isdoc(e['f']) and not isdoc(e['t']):
            G.add_edge(e['f'], e['t'], type=e['type'], label=e['label'])

    dE = nx.single_source_shortest_path_length(G, 'epstein') if 'epstein' in G else {}
    dM = nx.single_source_shortest_path_length(G, 'gmax') if 'gmax' in G else {}
    paths = nx.single_source_shortest_path(G, 'epstein') if 'epstein' in G else {}
    bc = nx.betweenness_centrality(G)
    H = G.copy(); H.remove_nodes_from([h for h in HUBS if h in H])
    bcH = nx.betweenness_centrality(H)
    rank = {k: i + 1 for i, (k, _) in enumerate(sorted(bc.items(), key=lambda x: -x[1]))}
    rankH = {k: i + 1 for i, (k, _) in enumerate(sorted(bcH.items(), key=lambda x: -x[1]))}

    # loops (cycle basis, length 3-5) not passing through Epstein
    G2 = G.copy()
    if 'epstein' in G2: G2.remove_node('epstein')
    loops = collections.defaultdict(list)
    for c in nx.cycle_basis(G2):
        if 3 <= len(c) <= 5:
            s = ' – '.join(N[x]['name'] for x in c)
            for x in c: loops[x].append(s)

    # role-aware succession: coverage of each hub's role neighbourhood within 2 steps, hubs removed
    def role_nb(hub, kinds):
        return {x for x in G[hub] if x not in HUBS and G[hub][x]['type'] in kinds} if hub in G else set()
    broker_all = (set(G['epstein']) - set(HUBS)) if 'epstein' in G else set()
    broker_money = role_nb('epstein', MONEY)
    ops_nb = role_nb('gmax', OPS | {'association', 'correspondence'}) | role_nb('epstein', OPS)

    def cover(c, target):
        if c not in H or not target: return 0
        sp = nx.single_source_shortest_path_length(H, c, cutoff=2)
        return round(len([x for x in sp if x in target]) / len(target), 3)

    flights = {}
    fp = os.path.join(HERE, 'flight_counts.json')
    if os.path.exists(fp): flights = json.load(open(fp))

    # other library volumes that mention the node by exact name
    vols = {}
    V = json.load(open(os.path.join(REPO, 'book/plan/volumes.json')))
    st2vol = {}
    for k, v in V.items():
        if k.startswith('_') or not isinstance(v, dict): continue
        for c in v.get('stages', []):
            st2vol[c['id'] if isinstance(c, dict) else c] = v.get('title', k)
    text = collections.defaultdict(str)
    for dd in glob.glob(os.path.join(REPO, 'book/part1/*/')):
        st = dd.rstrip('/').split('/')[-1]
        if st.startswith('ep'): continue
        vol = st2vol.get(st)
        if not vol: continue
        for f in glob.glob(dd + '*.html'): text[vol] += ' ' + re.sub(r'<[^>]+>', ' ', open(f, errors='replace').read())

    fn_of = collections.defaultdict(list)
    for e in E:
        if e['f'].startswith('fn_') and e['type'] == 'comparative methodology' and e['t'] in N:
            fn_of[e['t']].append(N[e['f']]['name'].replace('Function: ', ''))

    def role(n):
        c, k, i = n['cluster'], n['kind'], n['id']
        if i in HUBS: return 'hub'
        if i in OFFICE: return 'back office / vehicle'
        if n.get('sponsor') or i in ('wexner', 'black', 'edr', 'edr_holding', 'usvi_edc', 'ariane'): return 'sponsor / payer'
        if c in ('finance', 'money', 'crypto', 'investment'): return 'finance'
        if c in ('operations', 'aviation', 'places'): return 'operations / logistics'
        if c in ('justice', 'state', 'witnesses') or k == 'government': return 'official / agency'
        if c in ('reporters', 'reputation'): return 'media / reputation'
        if c == 'comparative': return 'comparison framework'
        if k == 'document' or c in ('evidence', 'records', 'research'): return 'evidence / record'
        return 'access / association'

    tier_name = {0: 'hub', 1: 'Direct 1°', 2: 'Operational 2°', 3: 'Strategic 3°'}
    for n in d['nodes']:
        i = n['id']
        st = collections.Counter(e['status'] for e in E if i in (e['f'], e['t']))
        mine = [e for e in E if i in (e['f'], e['t'])]
        srcs = set(p.strip() for e in mine for p in str(e.get('src', '')).split(';') if p.strip())
        k = dE.get(i)
        q = {
            'tier': 'hub' if i in HUBS else tier_name.get(k, '4°+' if k is not None else ('off the documented-tie map (record, comparison or unverified ties only)' if i not in G else 'unconnected to Epstein')),
            'kb_epstein': k, 'kb_maxwell': dM.get(i),
            'path_epstein': [N[x]['name'] for x in paths.get(i, [])][::-1] if k else [],
            'ties': {'total': len(mine), 'verified': st['verified'], 'reported': st['reported'] + st['planned'] + st['probable'] + st['scheduled'],
                     'to_verify': st['to-verify'], 'withheld': st['withheld'], 'not_established': st['not-established'],
                     'documented': G.degree(i) if i in G else 0},
            'centrality': {'betweenness': round(bc.get(i, 0), 4), 'rank': rank.get(i),
                           'betweenness_without_hubs': round(bcH.get(i, 0), 4), 'rank_without_hubs': rankH.get(i)},
            'role': role(n),
            'money_in': [f"{N[e['f']]['name']}: {e['label']}" for e in mine if e['t'] == i and e['type'] in MONEY and e['status'] == 'verified' and not isdoc(e['f'])][:8],
            'money_out': [f"{N[e['t']]['name']}: {e['label']}" for e in mine if e['f'] == i and e['type'] in MONEY and e['status'] == 'verified' and not isdoc(e['t'])][:8],
            'loops': loops.get(i, [])[:6],
            'succession': {'broker_cover': cover(i, broker_all), 'broker_money_cover': cover(i, broker_money),
                           'operations_cover': cover(i, ops_nb)} if i not in HUBS and n['kind'] != 'document' else None,
            'flight': flights.get(i),
            'volumes': {},
            'sources': {'distinct': len(srcs), 'doj_efta': sum(1 for s in srcs if re.search(r'EFTA\d{8}', s))},
            'open_leads': [f"{N[e['t'] if e['f'] == i else e['f']]['name']}: {e['label']}" for e in mine if e['status'] == 'to-verify'][:6],
            'functions': fn_of.get(i, []),
        }
        nm = re.sub(r'\s*\(.*?\)', '', n['name']).strip()
        if len(nm) >= 6 and n['kind'] in ('person', 'company', 'institution', 'government', 'trust') and i not in HUBS:
            pat = re.compile(r'\b' + re.escape(nm) + r'\b')
            for vol, t in text.items():
                c = len(pat.findall(t))
                if c: q['volumes'][vol] = c
        n['qop'] = q
    d['qop_meta'] = {'graph': 'documented ties: verified, non-probe, non-kinship, no document nodes',
                     'nodes': G.number_of_nodes(), 'edges': G.number_of_edges(),
                     'broker_neighbours': len(broker_all), 'operations_neighbours': len(ops_nb)}
    json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
    return d


if __name__ == '__main__':
    d = run()
    print('qop profiles:', sum(1 for n in d['nodes'] if 'qop' in n), d['qop_meta'])
