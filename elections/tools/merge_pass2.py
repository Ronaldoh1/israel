#!/usr/bin/env python3
"""Merge the members-money second pass (ots_members_money_pass2.py) into the module: money given to each sitting
member's leadership PAC and joint fundraising committees by other committees, by kind of committee.

Usage: python3 merge_pass2.py <members-data dir> <data_states.json in> <data_states.json out>

Adds c.cmoney.lpac = {n_lp, n_jfc, lp, jfc, kinds:[[label, amount]], fp:[[committee, country, amount]], top:[[committee, kind, amount]]}
for candidates that already carry c.cmoney (matched by merge_members.py).
Rules: only receipts reported by the member's leadership PAC and joint fundraisers count (the file also lists what those
committees gave to others, and transfers between them; those are not money coming in); memo entries are dropped; an amended row ('A') that repeats an original row (same date, amount, giver and
recipient committee) is dropped as a duplicate. Lobbyists' LD-203 reports are NOT merged here: the pull is incomplete
and the raw reports repeat each contribution across amendments and match namesakes, so they need cleaning first."""
import csv, json, os, sys, collections

MD, SRC, OUT = sys.argv[1:4]
D = json.load(open(SRC, encoding='utf-8'))
C = D['cands']
summ = {r['id']: r for r in csv.DictReader(open(os.path.join(MD, 'summary.csv'), encoding='utf-8'))}
NOT_FP = ('NATIONAL TURKEY FEDERATION', 'CYPRUS AMAX', 'CYMAX', 'AFGHANISTAN & IRAQ VETERANS')
KIND = {'Corporate PAC': 'Corporate PACs', 'Lobbyist/registrant PAC': 'PACs of registered lobbyists', 'Trade association PAC': 'Trade, membership and co-op PACs',
        'Membership organization PAC': 'Trade, membership and co-op PACs', 'Cooperative PAC': 'Trade, membership and co-op PACs', 'Labor PAC': 'Labor union PACs',
        'Nonconnected (ideological/issue) PAC': 'Ideological and issue PACs', 'Super PAC / hybrid PAC': 'Super PACs and hybrid PACs', 'Leadership PAC': "Other politicians' leadership PACs",
        'Candidate committee / joint fundraiser': 'Campaigns and joint fundraisers', 'Party': 'Party committees'}
ORDER = ['PACs of registered lobbyists', 'Corporate PACs', 'Trade, membership and co-op PACs', 'Labor union PACs', 'Ideological and issue PACs',
         'Super PACs and hybrid PACs', "Other politicians' leadership PACs", 'Campaigns and joint fundraisers', 'Party committees', 'Other committees']

by_mid = {c['cmoney']['mid']: cid for cid, c in C.items() if c.get('cmoney', {}).get('mid')}
stats = collections.Counter()
for mid, m in summ.items():
    f = os.path.join(MD, m['state'], mid, 'money_into_leadership_pac_and_jfc.csv')
    if not os.path.exists(f): continue
    cid = by_mid.get(mid)
    if not cid: stats['no matching candidate'] += 1; continue
    # receipts the member's committees reported; the same file also lists what those committees gave to others
    # (24K, 24Z..., where the 'from' column holds the recipient) and transfers between them
    RECEIPTS = ('Contribution received from a committee', 'In-kind contribution received', 'Contribution from an unregistered committee')
    rows = [r for r in csv.DictReader(open(f, encoding='utf-8')) if r.get('memo') != 'X' and r.get('what') in RECEIPTS]
    orig = {(r['date'], r['amount'], r['from_committee_id'], r['into_committee']) for r in rows if r.get('amended') != 'A'}
    keep = [r for r in rows if r.get('amended') != 'A' or (r['date'], r['amount'], r['from_committee_id'], r['into_committee']) not in orig]
    # leave out transfers among the member's own committees (campaign, leadership PAC, joint fundraisers)
    own = set()
    pj = os.path.join(MD, m['state'], mid, 'profile.json')
    if os.path.exists(pj): own |= {x.split()[0] for x in json.load(open(pj)).get('principal_committees', [])}
    ljp = os.path.join(MD, m['state'], mid, 'leadership_and_joint_committees.json')
    if os.path.exists(ljp): lj0 = json.load(open(ljp)); own |= set(lj0.get('leadership_pacs') or {}) | set(lj0.get('joint_fundraisers') or {})
    sur = m['name'].split()[-1].upper()
    keep = [r for r in keep if r['from_committee_id'] not in own and not (r['from_kind'] == 'Candidate committee / joint fundraiser' and sur in r['from'].upper())]
    if not keep: continue
    lp = sum(float(r['amount']) for r in keep if r['committee_role'] == 'leadership PAC')
    jf = sum(float(r['amount']) for r in keep if r['committee_role'] != 'leadership PAC')
    kinds = collections.Counter(); givers = collections.Counter(); gk = {}; fp = collections.Counter(); fpc = {}
    for r in keep:
        a = float(r['amount']); lab = KIND.get(r['from_kind'], 'Other committees')
        kinds[lab] += a; givers[r['from']] += a; gk[r['from']] = lab
        if r.get('foreign_policy_country') and not any(k in r['from'].upper() for k in NOT_FP):
            fp[r['from']] += a; fpc[r['from']] = r['foreign_policy_country']
    lj = json.load(open(os.path.join(MD, m['state'], mid, 'leadership_and_joint_committees.json'))) if os.path.exists(os.path.join(MD, m['state'], mid, 'leadership_and_joint_committees.json')) else {}
    C[cid]['cmoney']['lpac'] = {
        'n_lp': len(lj.get('leadership_pacs') or {}), 'n_jfc': len(lj.get('joint_fundraisers') or {}),
        'lp': round(lp), 'jfc': round(jf),
        'kinds': [[k, round(kinds[k])] for k in ORDER if round(kinds.get(k, 0)) > 0],
        'fp': [[n, fpc[n], round(a)] for n, a in fp.most_common(6) if round(a) > 0],
        'top': [[n, gk[n], round(a)] for n, a in givers.most_common(8) if round(a) > 0]}
    stats['merged'] += 1
D['meta']['lpac_src'] = 'ots_members_money_pass2.py, FEC bulk files, run 2026-10-19'
json.dump(D, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(dict(stats))
