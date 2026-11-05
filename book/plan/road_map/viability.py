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
CHANNELS = ['money', 'land', 'force', 'diplomacy', 'organization', 'recognition']
NC = len(CHANNELS)
LABEL = {'money': 'Money', 'land': 'Land & settlers', 'force': 'Arms & force', 'diplomacy': 'Diplomacy & law', 'organization': 'Organization', 'recognition': 'Recognition'}
NEED = {'money': 'another source of money on the same scale', 'land': 'another land-buying and settlement apparatus',
        'force': 'another arms supplier or armed force', 'diplomacy': 'another great-power sponsor, legal basis or UN majority',
        'organization': 'another organizing body and leadership',
        'recognition': 'another route to recognition as a state (a new UN majority, or recognition by the great powers)'}

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
    try: out |= set(json.load(open(os.path.join(HERE, 'global_layer.json'))).get('post', []))   # the global layer after 1948
    except Exception: pass
    return out


def channel(e, N):
    if e['type'] == 'recognition' or (e['f'], e['t']) == ('res181', 'decl_indep'): return 'recognition'
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
EXP = {'money': 2, 'land': 1, 'force': 1, 'diplomacy': 1, 'organization': 1, 'recognition': 1}
REC_UN = 22.0           # Resolution 181 in force: the UN's legal basis, weighed as much as all the 1948 recognitions together
GREAT = {'us_gov': 3, 'ussr': 3}   # a great power's recognition weighs three; any other state's, one
VOTE_MODE = 'abstain'   # a removed yes-vote counts as an abstention ('against' is the harsher reading, offered in the explorer)   # money counts twice in the overall chance
ISSUE_T = {'official act', 'signatory'}
CARRIERS = ['wzo', 'jewish_agency', 'yishuv']
# --- lost years: the work an actor did over time, and whether anyone documented could have taken it over ---
Y0, Y1 = 1882, 1948          # the build-up years, from the first colonies to the founding
SPAN_T = Y1 - Y0             # 66
YEAR_CH = [0, 1, 2, 3, 4]    # recognition is a 1947-48 event, so it is not spread over years
MOVEMENT_SIDE = {'zionist movement', 'us lobby', 'finance', 'rothschild', 'land', 'settlement', 'militias', 'christian zionism', 'israel state'}
ACTOR_KINDS = {'person', 'institution', 'company', 'government'}
YR = re.compile(r'\b(1[6-9]\d\d)\b'); LIFE = re.compile(r'\(\s*(?:b\.\s*)?1[6-9]\d\d\s*[–-]\s*(?:1[6-9]\d\d|\d\d)?\s*\)')   # the bodies that pursued the state; with all of them gone there is no project left
HAZARD = 0.02            # each year of delay loses 2% of the chance: the 1947-48 window (end of the Mandate, the UN vote, post-war
                         # sympathy, Soviet and American support at once) was not going to stay open
HORIZONS = [10, 30]      # readings: founded by 1958, and within a generation (by 1978)
VERDICT = [(85, 'on', 'Happens on time, in 1948'), (70, 'on', 'Still likely, but delayed'), (75, 'ever', 'Still likely, but delayed'), (55, 'ever', 'Possible, with great difficulty'),
           (30, 'ever', 'Unlikely'), (0, 'ever', 'Not possible on this record')]   # who gave a document its force
T_BUILD = {'money': 51, 'land': 66, 'force': 28, 'diplomacy': 31, 'organization': 51, 'recognition': 3}   # years each channel took to build
T_FROM = {'money': 'the first Zionist Congress, 1897', 'land': 'the first colonies, 1882', 'force': 'the founding of the Haganah, 1920',
          'diplomacy': 'the Balfour Declaration, 1917', 'organization': 'the first Zionist Congress, 1897', 'recognition': 'the founding of the UN, 1945'}
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
        elif c == 5: v = REC_UN if (f, t) == ('res181', 'decl_indep') else w * GREAT.get(f, 1)
        else: v = w * (cf[f] + cf[t]) / 2
        edges.append([f, t, c, w, round(v, 4)])
    issuers = collections.defaultdict(set)
    for e in d['edges']:
        if e['status'] in ('verified', 'reported') and e['type'] in ISSUE_T and N[e['t']]['kind'] == 'document' and e['f'] not in post and e['t'] not in post and e['t'] not in ('res181', 'decl_indep'):
            issuers[e['t']].add(e['f'])
    groups = collections.OrderedDict()
    groups['Rothschild family and houses'] = sorted(n['id'] for n in d['nodes'] if n['cluster'] == 'rothschild')
    us = sorted(n['id'] for n in d['nodes'] if n['cluster'] in ('us government', 'us lobby', 'us parties') and n['id'] not in post)
    groups['Without the United States'] = sorted(set(us) | {x for x in US_EXTRA if x in N})
    for cl, name in [('british state', 'British government'), ('us government', 'US government'), ('us lobby', 'American Zionist organizations'),
                     ('soviet bloc', 'Soviet bloc'), ('finance', 'Finance and banks'), ('zionist movement', 'The Zionist movement (organizations and leaders)'),
                     ('militias', 'Armed groups and arms network'), ('religion', 'Religious institutions'), ('christian zionism', 'Christian Zionism')]:
        groups[name] = sorted(n['id'] for n in d['nodes'] if n['cluster'] == cl and n['id'] not in post)
    groups['The United Nations'] = [x for x in ['un', 'unga', 'unsc', 'unscop'] if x in N]
    groups['Countries that voted for partition'] = sorted({e['f'] for e in d['edges'] if e['t'] == 'res181' and e['type'] == 'vote for'})
    groups['France'] = [x for x in ['france_gov', 'cambon', 'cambon_letter', 'bidault', 'millerand', 'berthelot', 'picot', 'clemenceau'] if x in N]
    groups['The Vatican'] = [x for x in ['vatican', 'pius10', 'pius12', 'benedict15', 'gasparri', 'merry_del_val', 'agliardi', 'tardini', 'maglione'] if x in N]
    core = [c for c in CORE if c in N]
    seen0 = reach({'edges': edges, 'core': core}, set())
    edges = [e for e in edges if e[0] in seen0 or e[1] in seen0]
    cap0 = [0.0] * NC
    for e in edges: cap0[e[2]] += e[4]
    amounts = {f + '>' + t: [v, txt] for (f, t), (v, txt) in AMOUNT.items()}
    labs = collections.defaultdict(list)
    for e in d['edges']:
        if e['status'] in ('verified', 'reported'): labs[(e['f'], e['t'])].append(e.get('label', ''))
    span = collections.defaultdict(list)
    for f, t, c, w, v in edges:
        for lab in labs[(f, t)]:
            ys = [int(y) for y in YR.findall(LIFE.sub('', lab)) if Y0 <= int(y) <= Y1]
            span[f] += ys; span[t] += ys
    actors = {i: [min(span[i]), max(span[i]), 'm' if N[i]['cluster'] in MOVEMENT_SIDE else 's'] for i in span
              if i in N and span[i] and N[i]['kind'] in ACTOR_KINDS}
    vote = {k: sorted({e['f'] for e in d['edges'] if e['t'] == 'res181' and e['type'] == ty}) for k, ty in [('yes', 'vote for'), ('no', 'vote against'), ('abstain', 'abstention')]}
    return {'channels': CHANNELS, 'labels': LABEL, 'need': NEED, 'core': core, 'edges': edges, 'groups': groups, 'vote': vote, 'vote_mode': VOTE_MODE,
            'issuers': {k: sorted(v) for k, v in issuers.items()}, 'exp': [EXP[c] for c in CHANNELS],
            'conduit': [f + '>' + t for f, t in CONDUIT], 'carriers': [c for c in CARRIERS if c in N],
            'actors': actors, 'y0': Y0, 'y1': Y1, 'year_ch': YEAR_CH, 'hazard': HAZARD, 'horizons': HORIZONS, 'verdict': VERDICT,
            'cap0': [round(x, 4) for x in cap0], 'cal': CAL, 'tbuild': [T_BUILD[c] for c in CHANNELS], 'tfrom': [T_FROM[c] for c in CHANNELS],
            'amounts': amounts, 'default_m': DEFAULT_M, 'drop': {'Without the United States': [f + '>' + t for f, t in US_RAISED]}}


def vote181(M, out, mode=None):
    """Resolution 181 needs two-thirds of the votes cast (abstentions not counted): yes >= 2 x no. A removed no-vote does not
    vote; a removed yes-vote abstains, or, in the harsher reading, votes against."""
    mode = mode or M.get('vote_mode', 'abstain'); yes = set(M['vote']['yes']); no = set(M['vote']['no'])
    y = len(yes - out); n = len(no - out) + (len(yes & out) if mode == 'against' else 0)
    return {'yes': y, 'no': n, 'abstain': len(M['vote']['abstain']) + len(no & out) + (len(yes & out) if mode != 'against' else 0),
            'passes': y >= 2 * n and not ({'un', 'unga'} & out), 'need': 2 * n, 'un_gone': bool({'un', 'unga'} & out)}


def lost_force(M, removed, mode=None):
    """Documents whose every issuer (official act or signature) is removed lose their force, and count as removed;
    repeated until nothing changes, so a treaty resting on a fallen document falls too only if its own issuers fall."""
    out = set(removed); ch = True
    while ch:
        ch = False
        for doc, iss in M['issuers'].items():
            if doc not in out and iss and all(i in out for i in iss): out.add(doc); ch = True
        if 'res181' not in out and M.get('vote') and not vote181(M, out, mode)['passes']: out.add('res181'); ch = True
    return out


def lost_years(M, removed, drop=()):
    """Years of the movement's work lost. Each actor (person, organization, government) is active from its first to its last
    dated supporting tie. In each year, the share of a channel's active work that an actor carried and lost (removed, or its
    ties cut) is covered by the strongest documented actor on the same side (the movement and its backers, or states) already
    active that year, up to that actor's own weight in the channel. What no one could cover is lost; a year counts as lost in
    proportion to the worst-hit channel. Returns the total, the lost share per year, and each actor's own loss and best substitute."""
    A = M['actors']; NCh = len(M['channels'])
    cap = {i: [0.0] * NCh for i in A}; live = {i: [0.0] * NCh for i in A}; avail = {i: [0.0] * NCh for i in A}
    for f, t, c, w, v in M['edges']:
        dropped = (f + '>' + t) in drop
        for x in (f, t):
            if x in cap:
                cap[x][c] += v
                # an actor loses a tie's work if it is removed itself, or the tie is cut; a partner of a removed actor does not
                # (the removed actor's own loss already stands for that tie)
                if not (x in removed or dropped): live[x][c] += v
                if not (f in removed or t in removed or dropped): avail[x][c] += v
    # a substitute can only bring what it had apart from the removed actors (PICA's money was Edmond's money)
    order = {k: sorted((i for i in A if avail[i][k] > 0), key=lambda i: -avail[i][k]) for k in M['year_ch']}
    total, per, who = 0.0, {}, {}
    for y in range(M['y0'], M['y1'] + 1):
        act = [i for i in A if A[i][0] <= y <= A[i][1]]
        F = []
        for k in M['year_ch']:
            tot = sum(cap[i][k] for i in act)
            if not tot: F.append(0); continue
            lost = 0.0
            for a in act:
                l = cap[a][k] - live[a][k]
                if l <= 1e-9: continue
                sub = next((b for b in order[k] if b != a and b not in removed and A[b][2] == A[a][2] and A[b][0] <= y), None)
                cov = min(1.0, avail[sub][k] / l) if sub else 0.0
                lost += l / tot * (1 - cov)
                r = who.setdefault(a, {'s': A[a][0], 'e': A[a][1], 'years': 0.0, 'ch': None, 'subs': {}, 'w': 0.0, 'yk': {}})
                if l / tot > r['w']: r.update(ch=k, w=l / tot)
                r['yk'][k] = r['yk'].get(k, 0.0) + l / tot * (1 - cov)
                r['years'] = r['yk'].get(r['ch'], 0.0)   # years lost in the actor's main role
                if sub:   # the best substitute per channel: who, how much of the role, and from when
                    q = r['subs'].get(k)
                    if q is None or cov > q[1]: r['subs'][k] = [sub, round(cov, 2), A[sub][0]]
            F.append(min(1.0, lost))
        f = max(F) if F else 0
        per[y] = round(f, 3); total += f
    return total, per, who


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


def score(M, removed, drop=(), mode=None):
    """Capacity still connected to the core, per channel, turned into a probability by saturation:
    P_c = 1 - exp(-C_c / K_c), with K_c set so the full record gives CAL. Overall P = product of the five (all were needed).
    Delay: years to rebuild the lost share at the pace the channel was originally built."""
    removed = lost_force(M, set(removed), mode)
    seen = reach(M, removed, drop)
    cap = [0.0] * NC; ties = [0] * NC; ties0 = [0] * NC
    for f, t, c, w, v in M['edges']:
        ties0[c] += 1
        if f in removed or t in removed or (f + '>' + t) in drop: continue
        if f in seen or t in seen: cap[c] += v; ties[c] += 1
    nocarrier = all(c in removed for c in M.get('carriers', []))
    if nocarrier: cap = [0.0] * NC
    import math
    k = -math.log(1 - M['cal'])
    P = [1 - math.exp(-k * cap[i] / M['cap0'][i]) if M['cap0'][i] else 1 for i in range(NC)]
    tot = 100.0
    for i, p in enumerate(P): tot *= p ** M['exp'][i]
    L = lost_years(M, removed, drop)[0] if (drop or any(x in M['actors'] for x in removed)) else 0.0
    tau = max(0.0, 1 - L / SPAN_T)
    tot *= tau
    r = [cap[i] / M['cap0'][i] if M['cap0'][i] else 1 for i in range(NC)]
    delay = [M['tbuild'][i] * (1 - r[i]) for i in range(NC)]
    return {'P': tot, 'pc': P, 'share': r, 'delay': delay, 'cap': cap, 'ties': ties, 'ties0': ties0, 'removed': removed, 'nocarrier': nocarrier, 'lost_years': L, 'tau': tau}


def readings(M, R):
    """Five readings of the same removal: on time (1948), by 1958, by 1978, ever, and a verdict.
    A later founding waits while each lost channel is rebuilt at the pace it was first built (a channel with nothing left cannot
    regrow from inside the record); the chance at year t is the chance with what has been rebuilt by then, discounted by the
    closing window, e^(-HAZARD x t). 'By year Y' and 'ever' take the best year up to Y (or 100 years), and never less than 1948's."""
    k = -math.log(1 - M['cal']); P0 = R['P'] / 100; D = max(max(R['delay']), R.get('lost_years', 0)); Lmin = math.ceil(R.get('lost_years', 0))
    def P_at(shares):
        p = 1.0
        for i, sh in enumerate(shares): p *= (1 - math.exp(-k * sh)) ** M['exp'][i]
        return p
    # the movement itself survives (keeps raising money and organizing) even where the state is delayed or blocked
    out = {'on': round(100 * P0, 1), 'delay': round(D, 1), 'survive': round(100 * R['pc'][0] ** 2 * R['pc'][4], 1), 'lost': round(R.get('lost_years', 0), 1)}
    best, t_best = 0.0, 0
    for t in range(1, 101):    # the best later attempt by year t: capacity rebuilt so far, discounted by the closing window
        sh = [min(1, s + t / M['tbuild'][i]) if s > 0.001 else 0 for i, s in enumerate(R['share'])]
        p = P_at(sh) * math.exp(-HAZARD * t) if t >= Lmin else 0.0
        if p > best: best, t_best = p, t
        if t in HORIZONS: out['by%d' % (1948 + t)] = round(100 * max(P0, best), 1)
    out['ever'] = round(100 * max(P0, best), 1); out['retry'] = 1948 + t_best if best > P0 else None
    for cut, key, txt in VERDICT:
        if out[key] >= cut: out['verdict'] = txt; break
    return out


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
    own = collections.defaultdict(lambda: [0.0] * NC)
    for f, t, c, w, v in M['edges']:
        own[f][c] += v; own[t][c] += v
    for n in d['nodes']:
        R = score(M, {n['id']}); k = min(range(NC), key=lambda i: R['pc'][i])
        n.setdefault('qop', {})['viability'] = {
            'V': round(R['P'], 1), 'rating': rating(R['P']), 'weakest': CHANNELS[k], 'channels': [round(x, 3) for x in R['pc']],
            'delay': round(max(R['delay']), 1), 'drop': round(R0['P'] - R['P'], 1), 'read': readings(M, R),
            'weight': [round(own[n['id']][i] / M['cap0'][i], 3) if M['cap0'][i] else 0 for i in range(NC)]}
    G = {}
    for name, ids in M['groups'].items():
        R = score(M, set(ids), set(M['drop'].get(name, []))); k = min(range(NC), key=lambda i: R['pc'][i])
        G[name] = {'V': round(R['P'], 1), 'rating': rating(R['P']), 'weakest': CHANNELS[k], 'n': len(ids), 'delay': round(max(R['delay']), 1),
                   'channels': [round(x, 3) for x in R['pc']], 'money_m': round(R['cap'][0], 2), 'read': readings(M, R)}
    d['viability_meta'] = {'baseline': round(R0['P'], 1), 'edges_counted': len(M['edges']), 'money_m': round(M['cap0'][0], 2),
                           'per_channel': dict(collections.Counter(CHANNELS[e[2]] for e in M['edges'])), 'groups': G}
    json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
    return d, M


if __name__ == '__main__':
    d, M = run()
    print(d['viability_meta'])
    top = sorted(d['nodes'], key=lambda n: n['qop']['viability']['V'])[:20]
    for n in top: print(n['id'], n['qop']['viability'])
