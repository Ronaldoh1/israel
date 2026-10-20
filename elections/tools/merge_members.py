#!/usr/bin/env python3
"""Merge the members-money pull (ots_members_money.py, extras-data/members-data) into the 2026 Elections module data.

Usage: python3 merge_members.py <members-data dir> <ballot_2026.csv> <data_states.json in> <data_states.json out>

For every candidate on the ballot who is a current member of Congress (or a governor with FEC history), adds `cmoney`:
  span, since      cycles with FEC money; date first sworn in
  cyc              per cycle: [cycle, receipts, from individuals, from PACs and committees, self-funding + candidate loans, through]
  tot              career [receipts, individuals, PACs and committees]
  kinds            career direct gifts from committees, by kind of committee [label, amount, note]
  top              ten largest committee givers, career [name, kind, amount]
  isr              PACs focused on Israel policy: money to their campaigns as those PACs reported it
                   (direct gifts and donations they forwarded as conduits, net of refunds) [name, amount, n]
  isr_ie           the same PACs' outside spending [name, for, against]
  oth              other PACs named for a country or diaspora community [name, country, amount]
  out              all outside spending {for, against, topf:[[name, amt]], topa:[[name, amt]]}
Only the candidate's own FEC ids (as listed on the ballot file) are counted, so a namesake's committee is never mixed in.
Every figure is a lead from the FEC's own files, not a finding about anyone's motives."""
import csv, json, os, re, sys, collections

MD, BALLOT, SRC, OUT = sys.argv[1:5]
D = json.load(open(SRC, encoding='utf-8'))
C = D['cands']
FEC = re.compile(r'[HSP]\d[A-Z0-9]{2}\d{5}')

def f(x):
    try: return float(x or 0)
    except ValueError: return 0.0
def rows(p):
    try: return list(csv.DictReader(open(p, encoding='utf-8')))
    except FileNotFoundError: return []

# ballot FEC ids -> candidate ids (to keep namesakes apart)
owner = collections.defaultdict(set)
ballot = list(csv.DictReader(open(BALLOT, encoding='utf-8')))
for b in ballot:
    for x in FEC.findall(b['fec_ids']): owner[x].add(b['data_id'])

# candidate lookup by state + office + surname, for ids that differ between files (Nick/Nicholas, Abe/Abraham)
OFFICE = {'representative': 'house', 'senator': 'sen', 'governor': 'gov'}
def surname(n): return re.sub(r'[^a-z]', '', (re.sub(r',?\s+(jr\.?|sr\.?|ii|iii|iv)$', '', n.strip(), flags=re.I).split() or [''])[-1].lower())
by_seat = collections.defaultdict(list)
for cid, c in C.items():
    if not c.get('incumbent'): continue
    st = cid[:2]; kind = 'sen' if '-sen-' in cid else 'gov' if '-gov-' in cid else 'house'
    by_seat[(st, kind, surname(c['name']))].append(cid)

# PAC classification (names are the FEC's own; adjust lists after review)
NOT_FOREIGN_POLICY = ('NATIONAL TURKEY FEDERATION', 'CYPRUS AMAX', 'CYMAX', 'AFGHANISTAN & IRAQ VETERANS')
OPPOSES_ISRAEL_LOBBY = ('CITIZENS AGAINST AIPAC', 'ANTI-ZIONIST')
def fp_country(name, country):
    n = (name or '').upper()
    if not country or any(k in n for k in NOT_FOREIGN_POLICY): return ''
    if any(k in n for k in OPPOSES_ISRAEL_LOBBY): return 'oppose'
    return country
KIND = [
    ('Lobbyist/registrant PAC', 'PACs of registered lobbyists', 'Mostly company and industry PACs whose sponsor is registered to lobby Congress'),
    ('Corporate PAC', 'Corporate PACs', ''),
    ('Trade association PAC', 'Trade, membership and co-op PACs', ''),
    ('Membership organization PAC', None, ''), ('Cooperative PAC', None, ''),
    ('Labor PAC', 'Labor union PACs', ''),
    ('Nonconnected (ideological/issue) PAC', 'Ideological and issue PACs', ''),
    ('Super PAC / hybrid PAC', 'Super PACs and hybrid PACs (direct gifts)', ''),
    ('Leadership PAC', "Other politicians' leadership PACs", ''),
    ('Candidate committee / joint fundraiser', 'Other campaigns and joint fundraisers', ''),
    ('Party', 'Party committees', ''),
]
KLAB = {}
last = None
for k, lab, note in KIND:
    if lab: last = (lab, note)
    KLAB[k] = last
GIFT = ('Contribution', 'In-kind contribution')
FOR = ('Independent expenditure FOR', 'Communication cost FOR')
AGN = ('Independent expenditure AGAINST', 'Communication cost AGAINST')

summary = rows(os.path.join(MD, 'summary.csv'))
stats = collections.Counter()
for m in summary:
    ids = set(FEC.findall(m['fec_ids']))
    cands = set()
    for x in ids: cands |= owner.get(x, set())
    cands &= set(C)
    if m['id'] in C: cands = {m['id']}
    if len(cands) != 1:
        st = m['state'].lower(); kind = OFFICE.get(m['role'], 'house')
        hit = by_seat.get((st, kind, surname(m['name'])), [])
        cands = set(hit) if len(hit) == 1 else set()
    if len(cands) != 1: stats['not on ballot'] += 1; continue
    cid = cands.pop(); c = C[cid]
    # keep only FEC ids that are not assigned to a different ballot candidate
    mine = {x for x in ids if not (owner.get(x) and cid not in owner[x] and m['id'] not in owner[x])}
    dropped = ids - mine
    folder = os.path.join(MD, m['state'], m['id'])
    try: prof = json.load(open(os.path.join(folder, 'profile.json'), encoding='utf-8'))
    except FileNotFoundError: prof = {}
    cyc = [cy for cy in prof.get('cycles', []) if cy.get('fec_id') in mine]
    if not cyc or not sum(f(cy.get('receipts')) for cy in cyc): stats['no FEC money'] += 1; continue
    cm = [r for r in rows(os.path.join(folder, 'committee_money.csv')) if r.get('to_fec_id', '').strip() in mine]
    CM = {}
    CM['since'] = prof.get('serving_since') or m.get('serving_since') or ''
    years = sorted(int(cy['cycle']) for cy in cyc)
    CM['span'] = f'{years[0]}–{years[-1]}'
    CM['cyc'] = [[int(cy['cycle']), round(f(cy['receipts'])), round(f(cy['individuals'])), round(f(cy['pacs_and_committees'])),
                  round(f(cy.get('self')) + f(cy.get('candidate_loans'))), cy.get('through', '')] for cy in sorted(cyc, key=lambda x: int(x['cycle']))]
    CM['tot'] = [sum(x[1] for x in CM['cyc']), sum(x[2] for x in CM['cyc']), sum(x[3] for x in CM['cyc'])]
    # gifts by kind and top givers
    kinds = collections.Counter(); knote = {}; givers = collections.Counter(); gkind = {}
    for r in cm:
        if r['what'] in GIFT:
            a = f(r['amount']); lab = KLAB.get(r['committee_kind'], ('Other committees', ''))
            kinds[lab[0]] += a; knote[lab[0]] = lab[1]; givers[r['committee']] += a; gkind[r['committee']] = r['committee_kind']
    order = [lab for _, lab, _ in KIND if lab] + ['Other committees']
    CM['kinds'] = [[lab, round(kinds[lab]), knote.get(lab, '')] for lab in order if round(kinds.get(lab, 0)) > 0]
    CM['top'] = [[n, gkind.get(n, ''), round(a)] for n, a in givers.most_common(10) if a > 0]
    # Israel-policy and other country PACs
    api = collections.Counter(); apin = collections.Counter(); pas = collections.Counter(); pasn = collections.Counter(); ctry = {}
    for r in rows(os.path.join(folder, 'foreign_policy_conduit_transfers.csv')):
        if r.get('memo_code') == 'X' and 'EARMARK' not in (r.get('description') or '').upper(): continue
        k = fp_country(r['conduit'], r['country'])
        if not k: continue
        api[r['conduit']] += f(r['amount']); apin[r['conduit']] += 1; ctry[r['conduit']] = k
    ie = collections.defaultdict(lambda: [0.0, 0.0])
    fara = collections.defaultdict(lambda: [ '', '', 0.0])
    for r in cm:
        k = fp_country(r['committee'], r['foreign_policy_country'])
        a = f(r['amount'])
        if k and r['what'] in GIFT: pas[r['committee']] += a; pasn[r['committee']] += 1; ctry[r['committee']] = k
        if k and r['what'] in FOR: ie[(r['committee'], k)][0] += a
        if k and r['what'] in AGN: ie[(r['committee'], k)][1] += a
        if r.get('fara_registrant') and r['what'] in GIFT:
            x = fara[r['committee']]; x[0] = r['fara_registrant']; x[1] = r.get('fara_countries', ''); x[2] += a
    fp = {}
    for n in set(api) | set(pas):
        use_api = api[n] >= pas[n]
        fp[n] = (ctry[n], api[n] if use_api else pas[n], apin[n] if use_api else pasn[n])
    isr = sorted([[n, round(a), k] for n, (c2, a, k) in fp.items() if c2 == 'Israel' and round(a)], key=lambda x: -x[1])
    opp = sorted([[n, round(a), k] for n, (c2, a, k) in fp.items() if c2 == 'oppose' and round(a)], key=lambda x: -x[1])
    oth = sorted([[n, c2, round(a)] for n, (c2, a, k) in fp.items() if c2 not in ('Israel', 'oppose') and round(a)], key=lambda x: -x[2])
    if isr: CM['isr'] = isr
    if opp: CM['isr_opp'] = opp
    if oth: CM['oth'] = oth[:8]
    iie = sorted([[n, round(v[0]), round(v[1])] for (n, k), v in ie.items() if k == 'Israel' and (round(v[0]) or round(v[1]))], key=lambda x: -(x[1] + x[2]))
    oie = sorted([[n, round(v[0]), round(v[1])] for (n, k), v in ie.items() if k == 'oppose' and (round(v[0]) or round(v[1]))], key=lambda x: -(x[1] + x[2]))
    if iie: CM['isr_ie'] = iie
    if oie: CM['isr_opp_ie'] = oie
    fr = sorted([[n, v[0], v[1], round(v[2])] for n, v in fara.items() if round(v[2]) > 0], key=lambda x: -x[3])
    # FARA-registrant PACs are not published: the registrant match includes long-terminated registrations (e.g. 1970s), too noisy to show
    # all outside spending
    of = collections.Counter(); oa = collections.Counter()
    for r in cm:
        if r['what'] in FOR: of[r['committee']] += f(r['amount'])
        elif r['what'] in AGN: oa[r['committee']] += f(r['amount'])
    if of or oa:
        CM['out'] = {'for': round(sum(of.values())), 'against': round(sum(oa.values())),
                     'topf': [[n, round(a)] for n, a in of.most_common(5) if a > 0], 'topa': [[n, round(a)] for n, a in oa.most_common(5) if a > 0]}
    if dropped: CM['note'] = 'Committees of a namesake on the ballot (' + ', '.join(sorted(dropped)) + ') are not counted.'
    for k in ('cyc', 'tot', 'kinds', 'top', 'isr_ie', 'isr_opp_ie', 'since'): CM.pop(k, None)   # the records section already shows these
    if CM.get('out'): CM['out'] = {'for': CM['out']['for'], 'against': CM['out']['against']}
    CM['mid'] = m['id']
    c['cmoney'] = CM; stats['merged'] += 1
    if isr: stats['with Israel-policy PAC money'] += 1
    if dropped: stats['namesake ids dropped'] += 1

D['meta']['cmoney_src'] = 'ots_members_money.py, FEC bulk files and FEC API, run 2026-10-18'
json.dump(D, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(dict(stats))
