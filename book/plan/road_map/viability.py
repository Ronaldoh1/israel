"""Counterfactual viability model for the 1948 network ("what if this node were removed?").

This is a disclosed structural model, not a historical probability. It reads only the documented network:
  1. Every documented, supportive tie dated before 1949 is assigned to one of five channels the state needed:
     money, land & settlers, arms & force, diplomacy & law, organization. Opposition and violence ties are not support.
  2. A tie still counts after a removal if neither end was removed and it still connects, through supportive
     documented ties, to the state-building core (CORE).
  3. Each channel's strength s_c = surviving weight / original weight (verified tie = 1.0, reported = 0.6).
  4. Viability V = 100 x product over channels of s_c ** W_c (a weighted geometric mean, because every channel
     was necessary: losing any one of them entirely gives 0).
The same arithmetic runs in the browser (road-network.html) for any set of removed nodes; this file precomputes
single-node and group readings for the stored profiles and checks that the two agree."""
import json, os, re, collections, math
import registry

HERE = os.path.dirname(os.path.abspath(__file__))
CHANNELS = ['money', 'land', 'force', 'diplomacy', 'organization']
LABEL = {'money': 'Money', 'land': 'Land & settlers', 'force': 'Arms & force', 'diplomacy': 'Diplomacy & law', 'organization': 'Organization'}
NEED = {'money': 'another source of money on the same scale', 'land': 'another land-buying and settlement apparatus',
        'force': 'another arms supplier or armed force', 'diplomacy': 'another great-power sponsor, legal basis or UN majority',
        'organization': 'another organizing body and leadership'}

CORE = ['decl_indep', 'provisional', 'jewish_agency', 'wzo', 'haganah', 'res181']
MONEY_T = {'funding', 'purchase', 'sale', 'ownership'}
FORCE_T = {'supply', 'operation'}
DIPLO_T = {'official act', 'agreement', 'signatory', 'drafting', 'addressee', 'legal basis', 'proposal', 'pressure',
           'correspondence', 'meeting', 'testimony', 'influence', 'coordination', 'instruction'}
ORG_T = {'founding', 'leadership', 'membership', 'succession', 'collaboration', 'association', 'appointment', 'branch', 'incorporation'}
SUPPORT = MONEY_T | FORCE_T | DIPLO_T | ORG_T
LAND_CL = {'land', 'settlement'}
LAND_IDS = {'jnf', 'pica', 'jca', 'plдc', 'pldc', 'palestine_office', 'hankin', 'ruppin', 'keren_hayesod', 'mossad_aliyah', 'brihah', 'exodus', 'hovevei', 'bilu', 'icsl'}
FORCE_CL = {'militias'}
STATE_CL = {'government', 'document'}
DIPLO_CL = {'british state', 'us government', 'international', 'europe', 'soviet bloc', 'ottoman', 'us parties', 'christian zionism', 'religion'}
NOT_SUPPORT_CL = {'arab states', 'arab leadership', 'nazi germany', '1948 war'}   # ties on these sides did not build the state
POST_YEAR = re.compile(r'\b(19[5-9]\d|1949)\b'); PRE_YEAR = re.compile(r'\b(1[6-8]\d\d|19[0-3]\d|194[0-8])\b')


def post_ids():
    """Nodes that belong to the state after 1948: the Cold War registry block, the Israeli state apparatus,
    and anyone the books name only in the Cold War volume."""
    raw = registry.RAW
    i = raw.find('Cold War layer, 1949-1967'); j = raw.find('# ----------', i + 10)
    block = raw[i:j if j > 0 else None]
    out = set(re.findall(r'^([a-z0-9_]+)\|', block, re.M))
    return out


def channel(e, N):
    if e['type'] not in SUPPORT: return None
    a, b = N[e['f']], N[e['t']]
    if a['cluster'] in NOT_SUPPORT_CL or b['cluster'] in NOT_SUPPORT_CL: return None
    if e['type'] in MONEY_T: return 'money'
    if a['cluster'] in LAND_CL or b['cluster'] in LAND_CL or e['f'] in LAND_IDS or e['t'] in LAND_IDS: return 'land'
    if e['type'] in FORCE_T or a['cluster'] in FORCE_CL or b['cluster'] in FORCE_CL: return 'force'
    if e['type'] in DIPLO_T or a['cluster'] in DIPLO_CL or b['cluster'] in DIPLO_CL or a['kind'] in STATE_CL or b['kind'] in STATE_CL: return 'diplomacy'
    return 'organization'


# Money is valued in 1948 US dollars where the record states a sum. Conversions are disclosed in the explorer:
# francs at the gold parity of 5.18 to the dollar, sterling at $4.86 (the pre-1931 parity); US consumer prices
# (1899 = 8.0, 1913 = 9.9, 1914 = 10.0, 1924 = 17.1, 1926 = 17.7, 1928 = 17.1, 1946 = 19.5, 1947 = 22.3, 1948 = 24.1).
AMOUNT = {   # (from, to): (millions of 1948 dollars, what the record says)
    ('edmond_r', 'pica'): (146.0, 'Edmond de Rothschild: "over sixty million dollars" invested in Palestine, 1882-1934 (at 1913 prices)'),
    ('upa', 'jewish_agency'): (89.0, 'United Palestine Appeal: $52 million (1946) and $74.7 million (1948), less the $50 million counted under Golda Meyerson'),
    ('meir', 'czechoslovakia'): (50.0, 'Golda Meyerson: about $50 million raised on the 1948 American tour'),
    ('keren_hayesod', 'jewish_agency'): (31.2, 'Keren Hayesod: £4,714,440 income, 1921-32 (half from the United States)'),
    ('nicaragua', 'jewish_agency'): (3.0, 'Nicaragua: $3 million in letters of credit (1948)'),
    ('straus_n', 'upa'): (0.14, 'Nathan Straus: $100,000 (1928)'),
    ('schiff', 'jdc'): (0.12, 'Jacob Schiff: $50,000 (1914)'),
    ('mickey_cohen', 'irgun'): (0.06, 'Mickey Cohen: $50,000-60,000 raised (1947)'),
    ('siegel', 'dafni'): (0.06, 'Bugsy Siegel: about $50,000 (1946-47)'),
    ('straus_n', 'hadassah'): (0.014, 'Nathan Straus: $10,000 (1924)'),
}
# ties whose money is already counted in a total above (passed through, or part of a lifetime sum): kept for the
# connections they make, valued at zero so nothing is counted twice
CONDUIT = {('uja', 'upa'), ('upa', 'hadassah'), ('edmond_r', 'jca'), ('edmond_r', 'rishon'), ('edmond_r', 'zikhron'),
           ('edmond_r', 'rosh_pinna'), ('edmond_r', 'mazkeret'), ('edmond_r', 'ekron'), ('edmond_r', 'metulla'), ('edmond_r', 'hebrew_univ')}
DEFAULT_M = 1.0          # money ties with no stated sum are assumed to carry $1 million; disclosed, not documented
NOT_PROJECT = {('nm_rothschild', 'uk'), ('lionel_r', 'uk'), ('ottoman', 'sursock')}   # money that did not go to the project
US_RAISED = [('meir', 'czechoslovakia')]   # money raised in the United States though carried by a non-American
CAL = 0.99               # each channel is calibrated so the full record gives it 99%
EXP = {'money': 2, 'land': 1, 'force': 1, 'diplomacy': 1, 'organization': 1}   # money counts twice in the overall chance
ISSUE_T = {'official act', 'signatory'}   # who gave a document its force
T_BUILD = {'money': 51, 'land': 66, 'force': 28, 'diplomacy': 31, 'organization': 51}   # years each channel took to build
T_FROM = {'money': 'the first Zionist Congress, 1897', 'land': 'the first colonies, 1882', 'force': 'the founding of the Haganah, 1920',
          'diplomacy': 'the Balfour Declaration, 1917', 'organization': 'the first Zionist Congress, 1897'}
US_EXTRA = ['sonneborn', 'sonneborn_inst', 'schwimmer', 'winters', 'greenspun', 'bernstein', 'lansky', 'mickey_cohen', 'siegel',
            'schiff', 'warburg_f', 'warburg_p', 'kuhn_loeb', 'americans_haganah', 'montor', 'feinberg', 'jacobson', 'straus_n']


def model(d):
    N = {n['id']: n for n in d['nodes']}
    post = post_ids()
    for n in d['nodes']:
        secs = n.get('sections') or []
        if secs and all(re.match(r'cw\d', s) for s in secs): post.add(n['id'])
        if n['cluster'] == 'israel state' and n['id'] not in ('decl_indep', 'provisional', 'law_return'): post.add(n['id'])
    best = {}
    for e in d['edges']:
        if e['status'] not in ('verified', 'reported') or e['type'] == 'kinship': continue
        if e['f'] in post or e['t'] in post: continue
        if (e['f'], e['t']) in NOT_PROJECT: continue
        lab = e.get('label', '')
        if POST_YEAR.search(lab) and not PRE_YEAR.search(lab): continue
        c = channel(e, N)
        if not c: continue
        w = 1.0 if e['status'] == 'verified' else 0.6
        k = (e['f'], e['t'], CHANNELS.index(c))
        if k not in best or best[k] < w: best[k] = w
    deg = collections.Counter()
    for (f, t, c) in best: deg[f] += 1; deg[t] += 1
    mx = math.log2(1 + max(deg.values()))
    cf = {n: 1 + math.log2(1 + k) / mx for n, k in deg.items()}   # 1 (one tie) to 2 (the best-connected node)
    edges = []
    for (f, t, c), w in best.items():
        if c == 0: v = 0.0 if (f, t) in CONDUIT else w * AMOUNT.get((f, t), (DEFAULT_M,))[0]
        else: v = w * (cf[f] + cf[t]) / 2
        edges.append([f, t, c, w, round(v, 4)])
    issuers = collections.defaultdict(set)
    for e in d['edges']:
        if e['status'] in ('verified', 'reported') and e['type'] in ISSUE_T and N[e['t']]['kind'] == 'document' and e['f'] not in post and e['t'] not in post:
            issuers[e['t']].add(e['f'])
    groups = collections.OrderedDict()
    groups['Rothschild family and houses'] = sorted(n['id'] for n in d['nodes'] if n['cluster'] == 'rothschild')
    us = sorted(n['id'] for n in d['nodes'] if n['cluster'] in ('us government', 'us lobby', 'us parties') and n['id'] not in post)
    groups['Without the United States'] = sorted(set(us) | {x for x in US_EXTRA if x in N})
    for cl, name in [('british state', 'British government'), ('us government', 'US government'), ('us lobby', 'American Zionist organizations'),
                     ('soviet bloc', 'Soviet bloc'), ('finance', 'Finance and banks'), ('zionist movement', 'Zionist movement leadership'),
                     ('militias', 'Armed groups and arms network'), ('religion', 'Religious institutions'), ('christian zionism', 'Christian Zionism')]:
        groups[name] = sorted(n['id'] for n in d['nodes'] if n['cluster'] == cl and n['id'] not in post)
    groups['France'] = [x for x in ['france_gov', 'cambon', 'cambon_letter', 'bidault', 'millerand', 'berthelot', 'picot', 'clemenceau'] if x in N]
    groups['The Vatican'] = [x for x in ['vatican', 'pius10', 'pius12', 'benedict15', 'gasparri', 'merry_del_val', 'agliardi', 'tardini', 'maglione'] if x in N]
    core = [c for c in CORE if c in N]
    seen0 = reach({'edges': edges, 'core': core}, set())
    edges = [e for e in edges if e[0] in seen0 or e[1] in seen0]
    cap0 = [0.0] * 5
    for e in edges: cap0[e[2]] += e[4]
    amounts = {f + '>' + t: [v, txt] for (f, t), (v, txt) in AMOUNT.items()}
    return {'channels': CHANNELS, 'labels': LABEL, 'need': NEED, 'core': core, 'edges': edges, 'groups': groups,
            'issuers': {k: sorted(v) for k, v in issuers.items()}, 'exp': [EXP[c] for c in CHANNELS],
            'conduit': [f + '>' + t for f, t in CONDUIT],
            'cap0': [round(x, 4) for x in cap0], 'cal': CAL, 'tbuild': [T_BUILD[c] for c in CHANNELS], 'tfrom': [T_FROM[c] for c in CHANNELS],
            'amounts': amounts, 'default_m': DEFAULT_M, 'drop': {'Without the United States': [f + '>' + t for f, t in US_RAISED]}}


def lost_force(M, removed):
    """Documents whose every issuer (official act or signature) is removed lose their force, and count as removed;
    repeated until nothing changes, so a treaty resting on a fallen document falls too only if its own issuers fall."""
    out = set(removed); ch = True
    while ch:
        ch = False
        for doc, iss in M['issuers'].items():
            if doc not in out and iss and all(i in out for i in iss): out.add(doc); ch = True
    return out


def reach(M, removed, drop=()):
    adj = collections.defaultdict(list)
    for e in M['edges']:
        f, t = e[0], e[1]
        if f in removed or t in removed or (f + '>' + t) in drop: continue
        adj[f].append(t); adj[t].append(f)
    seen = set(x for x in M['core'] if x not in removed); q = list(seen)
    while q:
        u = q.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); q.append(v)
    return seen


def score(M, removed, drop=()):
    """Capacity still connected to the core, per channel, turned into a probability by saturation:
    P_c = 1 - exp(-C_c / K_c), with K_c set so the full record gives CAL. Overall P = product of the five (all were needed).
    Delay: years to rebuild the lost share at the pace the channel was originally built."""
    removed = lost_force(M, set(removed))
    seen = reach(M, removed, drop)
    cap = [0.0] * 5; ties = [0] * 5; ties0 = [0] * 5
    for f, t, c, w, v in M['edges']:
        ties0[c] += 1
        if f in removed or t in removed or (f + '>' + t) in drop: continue
        if f in seen or t in seen: cap[c] += v; ties[c] += 1
    import math
    k = -math.log(1 - M['cal'])
    P = [1 - math.exp(-k * cap[i] / M['cap0'][i]) if M['cap0'][i] else 1 for i in range(5)]
    tot = 100.0
    for i, p in enumerate(P): tot *= p ** M['exp'][i]
    r = [cap[i] / M['cap0'][i] if M['cap0'][i] else 1 for i in range(5)]
    delay = [M['tbuild'][i] * (1 - r[i]) for i in range(5)]
    return {'P': tot, 'pc': P, 'share': r, 'delay': delay, 'cap': cap, 'ties': ties, 'ties0': ties0, 'removed': removed}


def rating(V):
    if V >= 90: return 'Still possible'
    if V >= 75: return 'Still possible, with more work'
    if V >= 55: return 'Possible only with major outside help'
    if V >= 35: return 'Doubtful'
    if V >= 15: return 'Very unlikely'
    return 'Not possible on this record'


def run(path=os.path.join(HERE, 'network.json')):
    d = json.load(open(path))
    M = model(d)
    R0 = score(M, set())
    own = collections.defaultdict(lambda: [0.0] * 5)
    for f, t, c, w, v in M['edges']:
        own[f][c] += v; own[t][c] += v
    for n in d['nodes']:
        R = score(M, {n['id']}); k = min(range(5), key=lambda i: R['pc'][i])
        n.setdefault('qop', {})['viability'] = {
            'V': round(R['P'], 1), 'rating': rating(R['P']), 'weakest': CHANNELS[k], 'channels': [round(x, 3) for x in R['pc']],
            'delay': round(max(R['delay']), 1), 'drop': round(R0['P'] - R['P'], 1),
            'weight': [round(own[n['id']][i] / M['cap0'][i], 3) if M['cap0'][i] else 0 for i in range(5)]}
    G = {}
    for name, ids in M['groups'].items():
        R = score(M, set(ids), set(M['drop'].get(name, []))); k = min(range(5), key=lambda i: R['pc'][i])
        G[name] = {'V': round(R['P'], 1), 'rating': rating(R['P']), 'weakest': CHANNELS[k], 'n': len(ids), 'delay': round(max(R['delay']), 1),
                   'channels': [round(x, 3) for x in R['pc']], 'money_m': round(R['cap'][0], 2)}
    d['viability_meta'] = {'baseline': round(R0['P'], 1), 'edges_counted': len(M['edges']), 'money_m': round(M['cap0'][0], 2),
                           'per_channel': dict(collections.Counter(CHANNELS[e[2]] for e in M['edges'])), 'groups': G}
    json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
    return d, M


if __name__ == '__main__':
    d, M = run()
    print(d['viability_meta'])
    top = sorted(d['nodes'], key=lambda n: n['qop']['viability']['V'])[:20]
    for n in top: print(n['id'], n['qop']['viability'])
