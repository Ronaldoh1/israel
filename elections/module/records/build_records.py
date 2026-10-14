"""Compact public-records profiles for every 2026 FEC filer, from Ron's ots_2026_collect.py run.

Input:  /home/claude/data26/x/<ST>/candidates.csv and one folder per candidate.
Output: records.json  {id: profile}  and  records_summary.json (counts for the build notes).

Rules (same standard for every candidate):
- Committee money is classified from the FEC's own committee fields (organization type, committee type,
  designation). Organization type wins (a corporate PAC that is also a lobbyist/registrant PAC stays corporate,
  with the lobbyist flag kept separately).
- Committees organized around another country's policy are found by the same test for every country:
  a named list (NORPAC, AIPAC, United Democracy Project, J Street, JACPAC, DMFI, ANCA, US-Cuba Democracy)
  or a country word in the committee or connected-organization name. Every such match is a lead with its reason.
- FARA: only exact first-and-last-name matches are kept, and they are labelled same-name leads, never findings.
- Independent expenditures (24E for, 24A against) are outside money and kept apart from contributions."""
import csv, glob, json, os, re, sys, collections
ROOT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/data26/x'
OUT = os.path.dirname(os.path.abspath(__file__))

COUNTRIES = ['Afghanistan', 'Afghan', 'Albania', 'Albanian', 'Algeria', 'Algerian', 'Armenia', 'Armenian', 'Azerbaijan', 'Azerbaijani', 'Bangladesh',
    'Bangladeshi', 'Belarus', 'Belarusian', 'Bosnia', 'Bosnian', 'Brazil', 'Brazilian', 'Cambodia', 'Cambodian', 'China', 'Chinese', 'Colombia', 'Colombian',
    'Croatia', 'Croatian', 'Cuba', 'Cuban', 'Cyprus', 'Cypriot', 'Egypt', 'Egyptian', 'Eritrea', 'Eritrean', 'Ethiopia', 'Ethiopian', 'Ghana', 'Ghanaian',
    'Greece', 'Greek', 'Hellenic', 'Haiti', 'Haitian', 'India', 'Indonesia', 'Indonesian', 'Iran', 'Iranian', 'Persian', 'Iraq', 'Iraqi', 'Ireland',
    'Irish', 'Israel', 'Israeli', 'Zionist', 'Italy', 'Italian', 'Japan', 'Japanese', 'Kashmir', 'Kashmiri', 'Kazakhstan', 'Korea', 'Korean', 'Kosovo',
    'Kurdish', 'Kurdistan', 'Lebanon', 'Lebanese', 'Libya', 'Libyan', 'Lithuania', 'Lithuanian', 'Latvia', 'Latvian', 'Estonia', 'Estonian', 'Baltic',
    'Moldova', 'Morocco', 'Moroccan', 'Nepal', 'Nepali', 'Nigeria', 'Nigerian', 'Pakistan', 'Pakistani', 'Palestine', 'Palestinian', 'Philippines',
    'Philippine', 'Filipino', 'Poland', 'Polish', 'Qatar', 'Qatari', 'Russia', 'Russian', 'Saudi', 'Serbia', 'Serbian', 'Somalia', 'Somali',
    'Sri Lanka', 'Sri Lankan', 'Sudan', 'Sudanese', 'Syria', 'Syrian', 'Taiwan', 'Taiwanese', 'Tibet', 'Tibetan', 'Turkey', 'Turkish', 'Ukraine',
    'Ukrainian', 'Uyghur', 'Venezuela', 'Venezuelan', 'Vietnam', 'Vietnamese', 'Yemen', 'Yemeni', 'Arab', 'Emirates', 'Emirati']
COUNTRY_RX = re.compile(r'\b(' + '|'.join(sorted(COUNTRIES, key=len, reverse=True)) + r')\b', re.I)
NAMED = [(r'\bNORPAC\b', 'Israel'), (r'\bAIPAC\b|AMERICAN ISRAEL PUBLIC AFFAIRS', 'Israel'), (r'UNITED DEMOCRACY PROJECT', 'Israel'),
         (r'\bJ STREET', 'Israel'), (r'JOINT ACTION COMMITTEE FOR POLITICAL AFFAIRS|\bJACPAC\b', 'Israel'), (r'DEMOCRATIC MAJORITY FOR ISRAEL', 'Israel'),
         (r'ARMENIAN NATIONAL COMMITTEE|\bANCA\b', 'Armenia'), (r'US.?CUBA DEMOCRACY', 'Cuba')]
LOCALISH = re.compile(r'\b(BANK|INC|CORP|COMPANY|LLC|RESTAURANT|EMPLOYEES|AIRLINES|MOTOR|TOYOTA|HONDA|NISSAN|HYUNDAI|SAMSUNG|COUNTY|CITY OF|INDIANA|INDIAN RIVER)\b', re.I)
CONTRIB = {'24K', '24Z', '24C', '24F', '24N', '24R'}   # 24E/24A are independent expenditures, counted separately

def kind_of(r):
    ct, ds, ot = r['donor_committee_type'], r['donor_designation'], r['donor_organization_type']
    if ct.startswith('Party'): return 'party'
    if ot in ('Corporation', 'Corporation without capital stock'): return 'corporate'
    if ot == 'Trade association': return 'trade'
    if ot == 'Labor organization': return 'labor'
    if ot == 'Membership organization': return 'membership'
    if ot == 'Cooperative': return 'coop'
    if ds == 'Leadership PAC': return 'leadership'
    if ct.endswith('campaign') or ds in ("Candidate's principal campaign committee", 'Authorized by a candidate', 'Joint fundraiser'): return 'candidate'
    if 'Super PAC' in ct or 'Hybrid' in ct or 'Independent expenditor' in ct: return 'superpac'
    return 'ideological'

NOT_COUNTRY = re.compile(r'NATIONAL TURKEY FEDERATION|\bTURPAC\b|WILD TURKEY|INDIANA\b', re.I)   # a poultry trade group, a state
CRITICAL = re.compile(r'ANTI.?ZIONIST|AGAINST AIPAC', re.I)   # organized against a country's lobby, not for it
ADJ = {'Afghan': 'Afghanistan', 'Albanian': 'Albania', 'Algerian': 'Algeria', 'Armenian': 'Armenia', 'Azerbaijani': 'Azerbaijan', 'Bangladeshi': 'Bangladesh',
       'Belarusian': 'Belarus', 'Bosnian': 'Bosnia', 'Brazilian': 'Brazil', 'Cambodian': 'Cambodia', 'Chinese': 'China', 'Colombian': 'Colombia', 'Croatian': 'Croatia',
       'Cuban': 'Cuba', 'Cypriot': 'Cyprus', 'Egyptian': 'Egypt', 'Eritrean': 'Eritrea', 'Ethiopian': 'Ethiopia', 'Ghanaian': 'Ghana', 'Greek': 'Greece', 'Hellenic': 'Greece',
       'Haitian': 'Haiti', 'Indonesian': 'Indonesia', 'Iranian': 'Iran', 'Persian': 'Iran', 'Iraqi': 'Iraq', 'Irish': 'Ireland', 'Israeli': 'Israel', 'Zionist': 'Israel',
       'Italian': 'Italy', 'Japanese': 'Japan', 'Kashmiri': 'Kashmir', 'Korean': 'Korea', 'Kurdish': 'Kurdistan', 'Lebanese': 'Lebanon', 'Libyan': 'Libya',
       'Lithuanian': 'Lithuania', 'Latvian': 'Latvia', 'Estonian': 'Estonia', 'Moroccan': 'Morocco', 'Nepali': 'Nepal', 'Nigerian': 'Nigeria', 'Pakistani': 'Pakistan',
       'Palestinian': 'Palestine', 'Philippine': 'Philippines', 'Filipino': 'Philippines', 'Polish': 'Poland', 'Qatari': 'Qatar', 'Russian': 'Russia', 'Serbian': 'Serbia',
       'Somali': 'Somalia', 'Sri Lankan': 'Sri Lanka', 'Sudanese': 'Sudan', 'Syrian': 'Syria', 'Taiwanese': 'Taiwan', 'Tibetan': 'Tibet', 'Turkish': 'Turkey',
       'Ukrainian': 'Ukraine', 'Venezuelan': 'Venezuela', 'Vietnamese': 'Vietnam', 'Yemeni': 'Yemen', 'Emirati': 'UAE', 'Emirates': 'UAE', 'Arab': 'Arab world'}

def foreign_policy(name, org, ct=''):
    s = name + ' ' + org
    if NOT_COUNTRY.search(s): return '', ''
    c, why = _fp(name, org, ct)
    if c and CRITICAL.search(s): why = 'organized against this country\'s lobby'
    return c, why

def _fp(name, org, ct=''):
    s = name + ' ' + org
    for rx, c in NAMED:
        if re.search(rx, s, re.I): return c, 'named'
    m = COUNTRY_RX.search(name) or COUNTRY_RX.search(org)
    if m and not ct.endswith('campaign'):
        w = m.group(1).title(); return ADJ.get(w, w), 'country word' + (' (may be a company or local group)' if LOCALISH.search(s) else '')
    return '', ''

def f(x):
    try: return float(x or 0)
    except ValueError: return 0.0

def norm(s): return re.sub(r'[^a-z ]', '', (s or '').lower()).split()

def fara_exact(name, j):
    toks = norm(name)
    if len(toks) < 2: return []
    first, last = toks[0], toks[-1]
    out = []
    for m in j.get('name_matches', []):
        r = m['row']
        fn, ln = norm(r.get('Short Form First Name', '')), norm(r.get('Short Form Last Name', ''))
        if fn and ln and fn[0] == first and ln[-1] == last:
            out.append({'who': (r.get('Short Form First Name', '') + ' ' + r.get('Short Form Last Name', '')).strip(),
                        'registrant': r.get('Registrant Name', ''), 'reg': r.get('Registration Number', ''),
                        'from': r.get('Short Form Date', ''), 'to': r.get('Short Form Termination Date', '')})
    return out

rec = {}; summ = collections.Counter(); fpall = collections.Counter()
for st in sorted(d for d in os.listdir(ROOT) if re.fullmatch(r'[A-Z]{2}', d)):
    for c in csv.DictReader(open(os.path.join(ROOT, st, 'candidates.csv'), encoding='utf-8')):
        d = os.path.join(ROOT, st, c['id']); p = {'st': st, 'name': c['name'], 'office': c['office'], 'dist': c['district'], 'party': c['party'],
                                                   'ico': c['incumbent_challenger_open'], 'fec': [x for x in c['fec_ids'].split(';') if x], 'mod': c['in_module'] == 'yes'}
        summ['candidates'] += 1
        try: t = json.load(open(os.path.join(d, 'fec_totals.json')))
        except Exception: t = {}
        p['cyc'] = [[y['cycle'], round(y['receipts']), round(y['individuals']), round(y['pacs_and_committees']), round(y['party']), round(y['self'] + y.get('candidate_loans', 0)),
                     round(y['spent']), round(y['cash_on_hand']), y.get('through', '')] for y in t.get('cycles', [])]
        if p['cyc']: summ['with_money'] += 1
        # committee contributions
        by = collections.defaultdict(float); by26 = collections.defaultdict(float); lob = 0.0; donors = {}
        fp = {}; ie_by = collections.defaultdict(float)
        path = os.path.join(d, 'fec_committee_contributions.csv')
        if os.path.exists(path):
            for r in csv.DictReader(open(path, encoding='utf-8')):
                amt = f(r['amount']); cyc = int(r['cycle'] or 0); tt = r['transaction_type']
                nm, org = r['donor_committee'], r['connected_organization']
                fc, why = foreign_policy(nm, org if org != 'NONE' else '', r['donor_committee_type'])
                if tt in ('24E', '24A'):
                    ie_by[(nm, 'S' if tt == '24E' else 'O', fc)] += amt; continue
                if tt not in CONTRIB: continue
                k = kind_of(r); by[k] += amt
                if cyc == 2026: by26[k] += amt
                if r['donor_designation'] == 'Lobbyist/registrant PAC': lob += amt
                dk = r['donor_committee_id']
                e = donors.setdefault(dk, [nm, k, 0.0, 0, cyc, cyc]); e[2] += amt; e[3] += 1; e[4] = min(e[4], cyc); e[5] = max(e[5], cyc)
                if fc:
                    g = fp.setdefault(dk, [nm, fc, why, 0.0, cyc, cyc]); g[3] += amt; g[4] = min(g[4], cyc); g[5] = max(g[5], cyc)
        p['pac'] = {k: round(v) for k, v in by.items() if v}
        p['pac26'] = {k: round(v) for k, v in by26.items() if v}
        p['lob'] = round(lob)
        p['top'] = [[e[0], e[1], round(e[2]), e[3], e[4], e[5]] for e in sorted(donors.values(), key=lambda e: -e[2])[:10]]
        p['fp'] = [[g[0], g[1], g[2], round(g[3]), g[4], g[5]] for g in sorted(fp.values(), key=lambda g: -g[3])]
        for g in p['fp']: fpall[g[1]] += g[3]
        if p['fp']: summ['with_fp_money'] += 1
        # outside spending 2026
        sp = collections.defaultdict(float); sfor = sag = 0.0
        path = os.path.join(d, 'fec_outside_spending_2026.csv')
        if os.path.exists(path):
            for r in csv.DictReader(open(path, encoding='utf-8')):
                amt = f(r['amount']); so = r['support_or_oppose']
                fc, _ = foreign_policy(r['spender'], '')
                sp[(r['spender'], so, fc)] += amt
                if so == 'S': sfor += amt
                elif so == 'O': sag += amt
        p['ie'] = {'for': round(sfor), 'against': round(sag), 'by': [[k[0], k[1], round(v), k[2]] for k, v in sorted(sp.items(), key=lambda kv: -kv[1])[:10]]}
        p['ie_hist'] = [[k[0], k[1], round(v), k[2]] for k, v in sorted(ie_by.items(), key=lambda kv: -kv[1])[:8]]
        if sfor or sag: summ['with_outside'] += 1
        # FARA (exact names only)
        try: p['fara'] = fara_exact(c['name'], json.load(open(os.path.join(d, 'fara.json'))))
        except Exception: p['fara'] = []
        if p['fara']: summ['fara_exact'] += 1
        # certification votes
        try:
            cv = json.load(open(os.path.join(d, 'certification_votes.json')))
            p['cert'] = [[v['date'], v['chamber'], v['objection'], v['vote']] for v in cv.get('votes', [])]
        except Exception: p['cert'] = []
        if p['cert']: summ['with_cert'] += 1
        # House financial disclosures (links to the Clerk's PDFs)
        path = os.path.join(d, 'house_disclosures', 'index.csv')
        p['fd'] = [[r['year'], r['type_label'], r['filed'], r['url']] for r in csv.DictReader(open(path, encoding='utf-8'))] if os.path.exists(path) else []
        if p['fd']: summ['with_disclosures'] += 1
        rec[c['id']] = p

json.dump(rec, open(os.path.join(OUT, 'records.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
summ['foreign_policy_money_by_country'] = dict(fpall.most_common())
json.dump(summ, open(os.path.join(OUT, 'records_summary.json'), 'w'), indent=1)
print(json.dumps(summ, indent=1)[:1500]); print('records.json %.1f MB' % (os.path.getsize(os.path.join(OUT, 'records.json')) / 1e6))
