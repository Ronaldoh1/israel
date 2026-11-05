"""What-if model for the Epstein network ("what if this node had been removed?").

A disclosed structural model built only from the documented ties in network.json, on the same arithmetic as the
1948 map (book/plan/road_map/viability.py). It is not a measured probability and it names no one as a successor.

The enterprise is Epstein, Maxwell, the companies, trusts and office that carried his business (OFFICE) and the
properties and aircraft they owned. Every documented tie between the enterprise and an outside node is sorted into
one of six channels:
  money in, banking, places & aircraft, staff & operations   (what ran it)
  legal & official cover, access & reputation                  (what protected it)
A channel's strength is 1 - exp(-k C/C0): C is what still connects after a removal, C0 the full record, and k is set
so the full record gives 99%. The chance the operation runs as documented is the product of the four running
channels and of the two cover channels taken as 0.5 + 0.5 x strength (losing all cover halves the chance; cover
protected the operation rather than ran it).

Two decisions are read as decisions (push over push plus resistance, as in the 1948 model): the 2008 federal
non-prosecution deal, and the 2019 federal arrest. Without the deal, a federal case in 2008 is taken to end the
operation's later years, so ties that begin after 2008 drop out in that branch.

The same arithmetic runs in the browser (epstein-network.html, ep_viab_ui.js); run() checks that they agree."""
import json, os, re, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CHANNELS = ['money', 'banking', 'places', 'staff', 'cover', 'access']
LABEL = {'money': 'Money in', 'banking': 'Banking', 'places': 'Places & aircraft', 'staff': 'Staff & operations',
         'cover': 'Legal & official cover', 'access': 'Access & reputation'}
COVER = [4, 5]                    # channel indexes taken as 0.5 + 0.5 x strength
CAL = 0.99
HUBS = ['epstein', 'gmax']
OFFICE = ['kahn', 'indyke', 'hbrk', 'southern_trust', 'financial_trust', 'butterfly_trust', 'epstein_2018_trust',
          'epstein_2019_trust', 'plan_d', 'jege', 'hyperion', 'lsje', 'kyara', 'gratitude', 'maple', 'slk']
OWN_T = {'ownership', 'asset ownership', 'residence', 'trustee', 'corporate office'}
PROBE = {'investigation', 'testimony', 'litigation', 'reporting', 'claim', 'complaint', 'oversight',
         'allegation to Congress', 'forensic review', 'court ruling', 'comparison', 'comparative methodology',
         'communications aggregate', 'flight passenger', 'custody', 'legislation', 'sworn allegation',
         'testimony / interview', 'research lead', 'research provenance', 'research archive / source corpus',
         'document evidence', 'document provenance', 'kinship', "knowledge of spouse's connection", 'document'}
MONEY_IN = {'funding', 'payment', 'contract', 'loan', 'trust grantor', 'client', 'payment instruction'}
BANK_T = {'banking', 'bank accounts'}
STAFF_T = {'employment', 'scheduling', 'travel coordination', 'criminal case', 'employment / office', 'employment / corporate name'}
PLACES_CL = {'places', 'aviation', 'travel'}
STAFF_CL = {'operations', 'vendors'}
SHIELD_IDS = {'npa', 'krischer', 'usvi_edc', 'usvi', 'acosta', 'doj', 'dag_2008', 'menchel'}
OUT_OF_SCOPE = {'origins', 'comparative', 'evidence', 'records', 'research', 'withheld', 'release', 'reporters', 'witnesses'}
SW = {'verified': 1.0, 'reported': 0.6, 'probable': 0.6, 'planned': 0.6, 'scheduled': 0.6}

# Money is weighted by the sum the record states, in millions of dollars; a money tie with no stated sum counts $1M
# (an assumption, disclosed in the explorer). Banking ties are weighted by the years the account ran, 3 if unstated.
AMOUNT = {
    ('black', 'epstein'): (170.0, 'Leon Black: $158M plus $12M in fees, 2012-17 (about $170M by the Senate Finance count)'),
    ('wexner', 'epstein'): (100.0, 'Les Wexner: assets worth roughly $100M obtained through the relationship (New York Times count), including the Manhattan house'),
    ('rothschild_group', 'epstein'): (25.0, 'Edmond de Rothschild group: $25M fee agreed in 2015, tied to the size of its DOJ penalty'),
    ('hoffenberg', 'epstein'): (3.8, 'Steven Hoffenberg: a $25,000-a-month consultancy (about $1.8M over 1987-93) and a $2M loan never repaid'),
    ('bv70', 'plan_d'): (30.5, "Black's BV70: loans of $22.5M and $8M to Plan D, 2017"),
}
PAYERS = {'wexner', 'black', 'rothschild_group', 'bv70', 'dubin', 'sinofsky', 'hoffenberg'}   # documented as paying him (Kahn named five paying clients)
CONDUIT = {('black', 'southern_trust'), ('black', 'gratitude'), ('wexner', 'nyc_house'), ('wexner', 'maple')}   # inside a total above
DEFAULT_M = 1.0
DEFAULT_BANK_YEARS = 3
Y0, Y1 = 1991, 2019   # the operation's span on this record: Wexner's power of attorney (1991) to the arrest (2019)

DECISIONS = [
    {'id': 'npa', 'name': 'The 2008 federal deal (non-prosecution agreement)', 'decider': 'acosta', 'successor': '*', 'year': 2008,
     'levers': ['lefkowitz', 'starr', 'dershowitz', 'sanchez', 'roy_black', 'goldberger', 'menchel', 'krischer', 'dag_2008'],
     'oppose': ['villafana', 'reiter', 'fbi'],
     'weights': {},
     'effects': {'remove': ['npa'], 'after': 2008},
     'why': 'Push: the defence team (Lefkowitz, Starr, Dershowitz, Sanchez, Roy Black, Goldberger), Menchel, who negotiated the plea route, the state attorney Krischer, whose 2006 grand jury brought a lesser charge, and the Deputy Attorney General\'s office, which declined to intervene. Resistance: the line prosecutor Marie Villafaña (a 60-count draft indictment), the Palm Beach police chief Michael Reiter and the FBI case agents.'},
    {'id': 'arrest', 'name': 'The 2019 federal arrest (SDNY)', 'decider': 'berman', 'successor': '*', 'year': 2019,
     'levers': ['herald_series', 'jkbrown', 'miami_herald', 'marra', 'giuffre', 'boies'],
     'oppose': ['npa'],
     'weights': {'herald_series': 2},
     'effects': {},
     'why': 'Push: the Miami Herald\'s "Perversion of Justice" series (counted twice, because the record credits the 2019 arrest largely to it), its reporter Julie K. Brown and the paper, Judge Marra\'s February 2019 ruling that the deal broke the victims\' rights law, and Virginia Giuffre\'s litigation with her lawyer David Boies. Resistance: the 2008 deal itself, whose immunity the defence argued barred a new federal case.'},
]
TIED = {'acosta': ['lefkowitz'], 'berman': []}   # push aimed at the decider personally (Lefkowitz's breakfast and letters to Acosta)
UNKNOWN_SUCCESSOR = 1

GROUPS = {
    'The banks': ['jpm', 'deutsche', 'bofa', 'goldman', 'hsbc', 'wells', 'firstbank', 'tdbank', 'citi', 'ubs', 'bank_leumi', 'deutsche_us', 'schwab'],
    'The defence lawyers (2005-08)': ['lefkowitz', 'starr', 'dershowitz', 'sanchez', 'roy_black', 'goldberger'],
    'The properties': ['nyc_house', 'palm_beach', 'lsj', 'gsj', 'zorro', 'paris_apt', 'apt66'],
    'The aircraft and pilots': ['n212je', 'n908je', 'n909je', 'jege', 'plan_d', 'hyperion', 'shmitka_air', 'visoski', 'rodgers'],
    'The reputation managers': ['seckel', 'ph_seo', 'osborne', 'siegal', 'couri_hay'],
    'The big payers (Wexner and Black)': ['wexner', 'black', 'bv70'],
    'The Miami Herald and its series': ['herald_series', 'jkbrown', 'miami_herald'],
    'The office (Indyke, Kahn and their firms)': ['indyke', 'kahn', 'hbrk', 'hyperion', 'slk', 'bella_klein'],
}
VERDICT = [(85, 'Runs as documented'), (65, 'Runs, but weakened'), (40, 'Badly crippled'), (15, 'Very unlikely to run'), (0, 'Does not run on this record')]
YEAR = re.compile(r'\b(19[6-9]\d|20[0-2]\d)\b')


YEAR_FIX = {('gmax', 'epstein'): 1994, ('brunel', 'epstein'): 0}   # the conduct, not the later conviction or death


def first_year(e):
    if (e['f'], e['t']) in YEAR_FIX: return YEAR_FIX[(e['f'], e['t'])]
    m = YEAR.findall(e['label'])
    return int(m[0]) if m else None


def bank_years(e):
    m = re.search(r'\b(19\d\d|20\d\d)\s*[–-]\s*(19\d\d|20\d\d)\b', e['label'])
    if m: return max(1, int(m.group(2)) - int(m.group(1)))
    m = re.search(r'from (19\d\d|20\d\d)', e['label'])
    if m: return max(1, 2019 - int(m.group(1)))
    return DEFAULT_BANK_YEARS


def enterprise(d):
    E = d['edges']; ent = set(HUBS) | set(OFFICE); owner = {}
    ch = True
    while ch:
        ch = False
        for e in E:
            if e['type'] in OWN_T and e['f'] in ent and e['t'] not in ent and e['status'] == 'verified' \
                    and d['N'][e['t']]['kind'] in ('place', 'company', 'trust', 'institution', 'project') and e['t'] not in ('valar', 'carbyne', 'coinbase'):
                ent.add(e['t']); owner[e['t']] = e['f']; ch = True
    for x in OFFICE: owner.setdefault(x, 'epstein')
    return ent, owner


def channel(e, N, ent):
    f, t = e['f'], e['t']
    if e['type'] in PROBE or e['status'] not in SW: return None
    fi, ti = f in ent, t in ent
    if not (fi or ti): return None
    if fi and ti:   # inside the enterprise: its assets, and its office
        if f in HUBS and t in HUBS: return 'staff'
        a, b = N[f], N[t]
        if b['kind'] == 'place' or b['cluster'] == 'aviation' or a['kind'] == 'place': return 'places'
        if (f in HUBS or t in HUBS) and (e['type'] in STAFF_T | {'office', 'ownership', 'trustee'}): return 'staff'
        return None
    x = t if fi else f; X = N[x]
    if X['kind'] == 'document' or X['cluster'] in OUT_OF_SCOPE: return None
    if e['type'] in BANK_T: return 'banking'
    if x in SHIELD_IDS or e['type'] in ('legal representation', 'government grant', 'favour') or (X['cluster'] == 'justice' and e['type'] in ('official act', 'contract', 'agreement')): return 'cover'
    if (f, t) in AMOUNT or (e['type'] in MONEY_IN and f in PAYERS): return 'money'
    if X['cluster'] in PLACES_CL or X['kind'] == 'place': return 'places'
    if X['cluster'] in STAFF_CL or e['type'] in STAFF_T: return 'staff'
    return 'access'


def model(d):
    N = {n['id']: n for n in d['nodes']}; d['N'] = N
    ent, owner = enterprise(d)
    rows = []; used = set()
    for e in d['edges']:
        c = channel(e, N, ent)
        if not c: continue
        s = SW[e['status']]
        if c == 'money':
            key = (e['f'], e['t'])
            w = 0.0 if key in CONDUIT else (AMOUNT[key][0] if key in AMOUNT and key not in used else DEFAULT_M)
            used.add(key)
        elif c == 'banking': w = bank_years(e)
        else: w = 1.0
        y = first_year(e)
        if y and y > Y1: continue   # after his death (property sales, settlements): not the operation
        rows.append([e['f'], e['t'], CHANNELS.index(c), round(w * s, 3), y or 0])
    cap0 = [0.0] * len(CHANNELS)
    for r in rows: cap0[r[2]] += r[3]
    del d['N']
    return {'channels': CHANNELS, 'labels': LABEL, 'cover': COVER, 'cal': CAL, 'hubs': HUBS, 'ent': sorted(ent), 'owner': owner,
            'edges': rows, 'cap0': [round(x, 3) for x in cap0], 'decisions': DECISIONS, 'tied': TIED, 'unknown_successor': UNKNOWN_SUCCESSOR,
            'groups': GROUPS, 'verdict': VERDICT, 'amounts': {f + '>' + t: v for (f, t), v in AMOUNT.items()}, 'default_m': DEFAULT_M,
            'default_bank_years': DEFAULT_BANK_YEARS, 'y0': Y0, 'y1': Y1}


def alive_ent(M, removed):
    """An owned company, trust or asset falls with the hub (or chain) that owned it."""
    out = set()
    for x in M['ent']:
        if x in removed: continue
        o, ok, seen = M['owner'].get(x), True, set()
        while o and o not in seen:
            seen.add(o)
            if o in removed: ok = False; break
            o = M['owner'].get(o)
        if ok: out.add(x)
    return out


def decision_chance(M, D, removed):
    dec = D['decider']
    if dec in removed: dec = D.get('successor') if D.get('successor') and D.get('successor') not in removed else None
    if not dec: return 0.0, None
    W = D.get('weights', {})
    S = sum(W.get(l, 1) for l in D['levers'] if l not in removed and not (dec != D['decider'] and l in M['tied'].get(D['decider'], [])))
    O = sum(W.get(o, 1) for o in D['oppose'] if o not in removed)
    if dec != D['decider']: S += M['unknown_successor']; O += M['unknown_successor']
    return (S / (S + O) if S + O else 0.0), dec


def base(M, removed, after=None):
    live = alive_ent(M, removed)
    k = -math.log(1 - M['cal'])
    cap = [0.0] * len(M['channels'])
    for f, t, c, w, y in M['edges']:
        if f in removed or t in removed: continue
        if not (f in live or t in live): continue
        if f in M['ent'] and f not in live: continue
        if t in M['ent'] and t not in live: continue
        if after and y and y > after: continue
        cap[c] += w
    hubs_gone = all(h in removed for h in M['hubs'])
    if hubs_gone: cap = [0.0] * len(cap)
    pc = [1 - math.exp(-k * x / x0) if x0 else 1 for x, x0 in zip(cap, M['cap0'])]
    # money is a stock built over time: each year from 1991 to 2019 is read against the money in by that year
    yrs = []
    for Y in range(M['y0'], M['y1'] + 1):
        if hubs_gone or (after and Y > after): yrs.append(0.0); continue
        s = s0 = 0.0
        for f, t, c, w, y in M['edges']:
            if c != 0 or (y and y > Y): continue
            s0 += w
            if f in removed or t in removed or (f in M['ent'] and f not in live) or (t in M['ent'] and t not in live): continue
            s += w
        yrs.append(1 - math.exp(-k * s / s0) if s0 else 1)
    pc[0] = sum(yrs) / len(yrs)
    eff = [0.5 + 0.5 * p if i in M['cover'] else p for i, p in enumerate(pc)]
    P = 100 * math.prod(eff)
    return {'P': P, 'pc': pc, 'cap': cap, 'hubs_gone': hubs_gone}


def score(M, removed):
    removed = set(removed)
    if 'epstein' in removed:   # no Epstein: nothing of his to shield or bring to account
        R = base(M, removed); R.update({'deal': None, 'arrest': None, 'account': None, 'decisions': []}); return R
    D1, D2 = M['decisions']
    p1_0 = decision_chance(M, D1, set())[0]; p1, d1 = decision_chance(M, D1, removed); r1 = min(1, p1 / p1_0) if p1_0 else 1
    p2_0 = decision_chance(M, D2, set())[0]; p2, d2 = decision_chance(M, D2, removed); r2 = min(1, p2 / p2_0) if p2_0 else 1
    if 'npa' in removed: r1 = 0.0
    with_deal = base(M, removed)
    without = base(M, removed | {'npa'}, after=2008)
    P = r1 * with_deal['P'] + (1 - r1) * without['P']
    pc = [r1 * a + (1 - r1) * b for a, b in zip(with_deal['pc'], without['pc'])]
    account = (1 - r1) + r1 * r2   # no deal: a federal case in 2008; with the deal: the 2019 arrest
    return {'P': P, 'pc': pc, 'cap': with_deal['cap'], 'deal': r1, 'arrest': r2, 'account': account, 'hubs_gone': False,
            'decisions': [{'id': D1['id'], 'name': D1['name'], 'chance': round(r1, 4), 'decider': d1},
                          {'id': D2['id'], 'name': D2['name'], 'chance': round(r2, 4), 'decider': d2}]}


def verdict(P):
    for cut, txt in VERDICT:
        if P >= cut: return txt


def run(path=os.path.join(HERE, 'network.json')):
    d = json.load(open(path))
    M = model(d)
    R0 = score(M, set())
    for n in d['nodes']:
        if n['kind'] == 'document' or n['id'] in ('npa',): pass
        R = score(M, {n['id']})
        n.setdefault('qop', {})['whatif'] = {'P': round(R['P'], 1), 'drop': round(R0['P'] - R['P'], 1), 'verdict': verdict(R['P']),
                                            'pc': [round(x, 3) for x in R['pc']], 'deal': None if R['deal'] is None else round(100 * R['deal']), 'account': None if R['account'] is None else round(100 * R['account']),
                                            'weakest': min(range(len(CHANNELS)), key=lambda i: R['pc'][i])}
    d['whatif_meta'] = {'P0': round(R0['P'], 1), 'deal0': round(100 * R0['deal']), 'account0': round(100 * R0['account']), 'ties': len(M['edges'])}
    json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
    return d, M


if __name__ == '__main__':
    d, M = run()
    R0 = score(M, set())
    print('ties', len(M['edges']), 'cap0', M['cap0'], 'P0 %.1f' % R0['P'], 'deal', R0['deal'], 'account', round(R0['account'], 3))
    cnt = collections.Counter(CHANNELS[r[2]] for r in M['edges']); print(cnt)
    for ids in [['epstein'], ['gmax'], ['epstein', 'gmax'], ['wexner'], ['black'], ['jpm'], ['acosta'], ['npa'], ['herald_series', 'jkbrown', 'miami_herald'], ['giuffre'], M['groups']['The banks'], M['groups']['The defence lawyers (2005-08)'], M['groups']['The reputation managers'], M['groups']['The aircraft and pilots'], M['groups']['The properties'], ['usvi_edc', 'usvi'], ['berman']]:
        R = score(M, set(ids))
        print(','.join(ids)[:50].ljust(50), 'P %5.1f' % R['P'], verdict(R['P']).ljust(26), 'deal %s' % (R['deal'] is not None and round(100 * R['deal'])), 'account %s' % (R['account'] is not None and round(100 * R['account'])), ' '.join('%s %d' % (c[:4], round(100 * p)) for c, p in zip(CHANNELS, R['pc'])))
    top = sorted((n for n in d['nodes'] if n['id'] not in HUBS), key=lambda n: -n['qop']['whatif']['drop'])[:15]
    for n in top: print(n['id'], n['qop']['whatif']['P'], n['qop']['whatif']['verdict'])
