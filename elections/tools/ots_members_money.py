#!/usr/bin/env python3
"""
OTS: who funds the people in office now.
Every current member of the House and Senate, and every current governor, with their full
federal money record across every cycle they have run, from the FEC's own files.

Run it on your own computer (Python 3.8+, nothing to install):
    python3 ots_members_money.py                     # everyone
    python3 ots_members_money.py --state TX          # one state (repeat --state for more)
    python3 ots_members_money.py --since 2000        # fewer cycles, smaller download
    FEC_API_KEY=xxxx python3 ots_members_money.py    # adds employer and conduit detail (free key: api.data.gov/signup)

For each person it records, cycle by cycle:
  - totals (receipts, individuals, PACs, party, self-funding)
  - EVERY contribution and outside expenditure by a committee for or against them, labelled with
    what the giving committee is: corporate PAC, trade association, labor union, lobbyist PAC,
    leadership PAC, party, super PAC, ideological PAC...
  - committees whose own name ties them to another country's policy (Israel, Armenia, India,
    Ukraine, Taiwan, Cuba and every other country, checked the same way), flagged for review
  - committees connected to a firm registered with the Justice Department as a foreign agent (FARA)
With an FEC API key it also adds the top employers of their individual donors per cycle and the
individual donations forwarded to them through foreign-policy PACs that act as conduits (earmarks).

Foreign governments and foreign nationals may not give to US campaigns, so "foreign-policy lobby
money" here means US committees organized around another country's policy, never a foreign state.
A name match is a lead to check, not a finding.

Output: members-data/<STATE>/<person>/ plus members-data/summary.csv (one row per person) and
members-data/foreign_policy_committees.csv (every flagged committee, with the reason it was flagged).
Big downloads are shared with the 2026 collector if it ran next to this folder, and are never
meant to be pushed (the .gitignore leaves them out). Safe to stop and re-run.
"""
import csv, io, json, os, re, ssl, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request, zipfile
from datetime import datetime, timezone

VERSION = '1.0 (2026-10-13)'
ROOT = os.path.abspath('members-data')
SIBLING_DL = [os.path.expanduser('~/Desktop/2026races/2026elections-data/_downloads'), os.path.abspath('2026elections-data/_downloads')]
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
STATES = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY AS DC GU MP PR VI'.split()
LEGISLATORS = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/gh-pages/legislators-current.json'
FEC = 'https://www.fec.gov/files/bulk-downloads/{y}/{f}'
FARA_REGISTRANTS = 'https://efile.fara.gov/bulk/zip/FARA_All_Registrants.csv.zip'
FARA_PRINCIPALS = 'https://efile.fara.gov/bulk/zip/FARA_All_ForeignPrincipals.csv.zip'
API = 'https://api.open.fec.gov/v1'

# Current governors (as of October 2026). Federal money appears only if they ever ran for federal office;
# their state campaign money is in each state's own system and is not collected here.
GOVERNORS = [('AL', 'Kay', 'Ivey'), ('AK', 'Mike', 'Dunleavy'), ('AZ', 'Katie', 'Hobbs'), ('AR', 'Sarah', 'Sanders'),
    ('CA', 'Gavin', 'Newsom'), ('CO', 'Jared', 'Polis'), ('CT', 'Ned', 'Lamont'), ('DE', 'Matt', 'Meyer'), ('FL', 'Ron', 'DeSantis'),
    ('GA', 'Brian', 'Kemp'), ('HI', 'Josh', 'Green'), ('ID', 'Brad', 'Little'), ('IL', 'JB', 'Pritzker'), ('IN', 'Mike', 'Braun'),
    ('IA', 'Kim', 'Reynolds'), ('KS', 'Laura', 'Kelly'), ('KY', 'Andy', 'Beshear'), ('LA', 'Jeff', 'Landry'), ('ME', 'Janet', 'Mills'),
    ('MD', 'Wes', 'Moore'), ('MA', 'Maura', 'Healey'), ('MI', 'Gretchen', 'Whitmer'), ('MN', 'Tim', 'Walz'), ('MS', 'Tate', 'Reeves'),
    ('MO', 'Mike', 'Kehoe'), ('MT', 'Greg', 'Gianforte'), ('NE', 'Jim', 'Pillen'), ('NV', 'Joe', 'Lombardo'), ('NH', 'Kelly', 'Ayotte'),
    ('NJ', 'Mikie', 'Sherrill'), ('NM', 'Michelle', 'Lujan Grisham'), ('NY', 'Kathy', 'Hochul'), ('NC', 'Josh', 'Stein'),
    ('ND', 'Kelly', 'Armstrong'), ('OH', 'Mike', 'DeWine'), ('OK', 'Kevin', 'Stitt'), ('OR', 'Tina', 'Kotek'), ('PA', 'Josh', 'Shapiro'),
    ('RI', 'Dan', 'McKee'), ('SC', 'Henry', 'McMaster'), ('SD', 'Larry', 'Rhoden'), ('TN', 'Bill', 'Lee'), ('TX', 'Greg', 'Abbott'),
    ('UT', 'Spencer', 'Cox'), ('VT', 'Phil', 'Scott'), ('VA', 'Abigail', 'Spanberger'), ('WA', 'Bob', 'Ferguson'),
    ('WV', 'Patrick', 'Morrisey'), ('WI', 'Tony', 'Evers'), ('WY', 'Mark', 'Gordon')]

# Committees organized around another country's policy, found by their own name or connected organization.
# The same test is applied to every country; each match is written out with its reason for review.
COUNTRIES = ['Afghanistan', 'Afghan', 'Albania', 'Albanian', 'Algeria', 'Algerian', 'Armenia', 'Armenian', 'Azerbaijan', 'Azerbaijani', 'Bangladesh',
    'Bangladeshi', 'Belarus', 'Belarusian', 'Bosnia', 'Bosnian', 'Brazil', 'Brazilian', 'Cambodia', 'Cambodian', 'China', 'Chinese', 'Colombia', 'Colombian',
    'Croatia', 'Croatian', 'Cuba', 'Cuban', 'Cyprus', 'Cypriot', 'Egypt', 'Egyptian', 'Eritrea', 'Eritrean', 'Ethiopia', 'Ethiopian', 'Ghana', 'Ghanaian',
    'Greece', 'Greek', 'Hellenic', 'Haiti', 'Haitian', 'India', 'Indo', 'Indonesia', 'Indonesian', 'Iran', 'Iranian', 'Persian', 'Iraq', 'Iraqi', 'Ireland',
    'Irish', 'Israel', 'Israeli', 'Zionist', 'Italy', 'Italian', 'Japan', 'Japanese', 'Kashmir', 'Kashmiri', 'Kazakhstan', 'Korea', 'Korean', 'Kosovo',
    'Kurdish', 'Kurdistan', 'Lebanon', 'Lebanese', 'Libya', 'Libyan', 'Lithuania', 'Lithuanian', 'Latvia', 'Latvian', 'Estonia', 'Estonian', 'Baltic',
    'Moldova', 'Morocco', 'Moroccan', 'Nepal', 'Nepali', 'Nigeria', 'Nigerian', 'Pakistan', 'Pakistani', 'Palestine', 'Palestinian', 'Philippines',
    'Philippine', 'Filipino', 'Poland', 'Polish', 'Qatar', 'Qatari', 'Russia', 'Russian', 'Saudi', 'Serbia', 'Serbian', 'Somalia', 'Somali',
    'Sri Lanka', 'Sri Lankan', 'Sudan', 'Sudanese', 'Syria', 'Syrian', 'Taiwan', 'Taiwanese', 'Tibet', 'Tibetan', 'Turkey', 'Turkish', 'Ukraine',
    'Ukrainian', 'Uyghur', 'Venezuela', 'Venezuelan', 'Vietnam', 'Vietnamese', 'Yemen', 'Yemeni', 'Arab', 'Emirates', 'Emirati']
COUNTRY_RX = re.compile(r'\b(' + '|'.join(sorted(COUNTRIES, key=len, reverse=True)) + r')\b', re.I)
# Committees whose names don't name a country but which describe themselves as organized around a country's policy.
# Discovery only: like every country-word match, each one is a lead to verify against the committee's own stated purpose.
NAMED = {r'\bNORPAC\b': 'Israel', r'\bAIPAC\b|AMERICAN ISRAEL PUBLIC AFFAIRS': 'Israel', r'UNITED DEMOCRACY PROJECT': 'Israel',
         r'\bJ STREET': 'Israel', r'JOINT ACTION COMMITTEE FOR POLITICAL AFFAIRS|\bJACPAC\b': 'Israel', r'DEMOCRATIC MAJORITY FOR ISRAEL': 'Israel',
         r'ARMENIAN NATIONAL COMMITTEE|\bANCA\b': 'Armenia', r'US.?CUBA DEMOCRACY': 'Cuba'}
# words that make a country-named committee a business or local group rather than a foreign-policy lobby: kept, but marked
LOCALISH = re.compile(r'\b(BANK|INC|CORP|COMPANY|LLC|RESTAURANT|EMPLOYEES|AIRLINES|MOTOR|TOYOTA|HONDA|NISSAN|HYUNDAI|SAMSUNG|COUNTY|CITY OF)\b', re.I)

CN = 'CAND_ID CAND_NAME CAND_PTY_AFFILIATION CAND_ELECTION_YR CAND_OFFICE_ST CAND_OFFICE CAND_OFFICE_DISTRICT CAND_ICI CAND_STATUS CAND_PCC CAND_ST1 CAND_ST2 CAND_CITY CAND_ST CAND_ZIP'.split()
WEBALL = 'CAND_ID CAND_NAME CAND_ICI PTY_CD CAND_PTY_AFFILIATION TTL_RECEIPTS TRANS_FROM_AUTH TTL_DISB TRANS_TO_AUTH COH_BOP COH_COP CAND_CONTRIB CAND_LOANS OTHER_LOANS CAND_LOAN_REPAY OTHER_LOAN_REPAY DEBTS_OWED_BY TTL_INDIV_CONTRIB CAND_OFFICE_ST CAND_OFFICE_DISTRICT SPEC_ELECTION PRIM_ELECTION RUN_ELECTION GEN_ELECTION GEN_ELECTION_PRECENT OTHER_POL_CMTE_CONTRIB POL_PTY_CONTRIB CVG_END_DT INDIV_REFUNDS CMTE_REFUNDS'.split()
CM = 'CMTE_ID CMTE_NM TRES_NM CMTE_ST1 CMTE_ST2 CMTE_CITY CMTE_ST CMTE_ZIP CMTE_DSGN CMTE_TP CMTE_PTY_AFFILIATION CMTE_FILING_FREQ ORG_TP CONNECTED_ORG_NM CAND_ID'.split()
ORG_TP = {'C': 'Corporation', 'L': 'Labor organization', 'M': 'Membership organization', 'T': 'Trade association', 'V': 'Cooperative', 'W': 'Corporation without capital stock'}
CMTE_TP = {'Q': 'PAC', 'N': 'PAC (nonqualified)', 'O': 'Super PAC', 'U': 'Single-candidate super PAC', 'V': 'Hybrid PAC', 'W': 'Hybrid PAC (nonqualified)',
           'X': 'Party (nonqualified)', 'Y': 'Party', 'Z': 'National party nonfederal account', 'H': 'House campaign', 'S': 'Senate campaign',
           'P': 'Presidential campaign', 'C': 'Communication cost', 'D': 'Delegate committee', 'E': 'Electioneering communication', 'I': 'Independent expenditor'}
CMTE_DSGN = {'A': 'Authorized by a candidate', 'B': 'Lobbyist/registrant PAC', 'D': 'Leadership PAC', 'J': 'Joint fundraiser', 'P': 'Principal campaign committee', 'U': 'Unauthorized'}
TX_TP = {'24K': 'Contribution', '24Z': 'In-kind contribution', '24E': 'Independent expenditure FOR', '24A': 'Independent expenditure AGAINST',
         '24C': 'Coordinated party expenditure', '24F': 'Communication cost FOR', '24N': 'Communication cost AGAINST', '24R': 'Recount', '24U': 'Contribution (unregistered)'}

# ---------------------------------------------------------------- helpers
def log(*a): print(*a, flush=True)
def _ctx():
    try:
        import certifi; return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()
CTX = _ctx()
CERT_HELP = ('\n  SSL certificate problem. On a Mac, open Applications > Python 3.x and double-click "Install Certificates.command"'
             '\n  (or run: pip3 install certifi), then run this again.\n')

class NetworkDown(Exception):
    """the connection stayed down; nothing partial gets saved, and running the same command again continues"""

def fetch(url, dest=None, headers=None, tries=4, quiet=False, patience=1800):
    """GET a URL to bytes, or stream it to a file (re-uses a finished file). Returns None only for a definite answer
    such as 'not found'. If the connection drops it waits up to `patience` seconds for it to come back, then raises NetworkDown."""
    if dest and os.path.exists(dest) and os.path.getsize(dest) > 0: return dest
    h = {'User-Agent': UA, 'Accept': '*/*'}; h.update(headers or {})
    i = 0; down_since = None; k = 0
    while i < tries:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), context=CTX, timeout=180) as r:
                if not dest: return r.read()
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                total = int(r.headers.get('Content-Length') or 0); got = 0; last = time.time()
                with open(dest + '.part', 'wb') as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b: break
                        f.write(b); got += len(b)
                        if total > 20e6 and time.time() - last > 5: log(f'      {got / 1e6:.0f} of {total / 1e6:.0f} MB'); last = time.time()
            os.replace(dest + '.part', dest); return dest
        except urllib.error.HTTPError as e:
            down_since = None
            if e.code == 429 or e.code >= 500:
                i += 1; wait = 30 * i; log(f'    busy ({e.code}); waiting {wait}s'); time.sleep(wait); continue
            if not quiet: log(f'    HTTP {e.code}: {url.split("api_key=")[0]}')
            return None
        except (ssl.SSLError, ssl.CertificateError):
            log(CERT_HELP); raise SystemExit(1)
        except Exception as e:
            if isinstance(getattr(e, 'reason', None), ssl.SSLError) or 'CERTIFICATE' in str(e).upper(): log(CERT_HELP); raise SystemExit(1)
            down_since = down_since or time.time()
            if time.time() - down_since > patience: raise NetworkDown(str(getattr(e, 'reason', e)))
            wait = min(60, 5 * 2 ** k); k += 1
            log(f'    connection problem ({getattr(e, "reason", e)}); waiting {wait}s for it to come back'); time.sleep(wait)
    raise NetworkDown(f'the server kept answering "busy" for {url.split("?")[0]}')

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z ]+', ' ', s.replace('-', ' ')).split()
def slug(s): return '-'.join(norm(s)) or 'x'
def money(x):
    try: return round(float(x or 0), 2)
    except ValueError: return 0.0
def zip_rows(path, cols):
    try: z = zipfile.ZipFile(path)
    except zipfile.BadZipFile: return
    m = [n for n in z.namelist() if n.lower().endswith(('.txt', '.csv'))]
    if not m: return
    with z.open(m[0]) as f:
        for line in io.TextIOWrapper(f, encoding='latin-1', newline=''):
            v = line.rstrip('\r\n').split('|')
            yield v if cols is None else dict(zip(cols, v))
def wcsv(path, head, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f: w = csv.writer(f); w.writerow(head); w.writerows(rows)
def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1, ensure_ascii=False)

class Person:
    def __init__(self, pid, first, last, state, role, district='', party='', fec_ids=(), extra=None):
        self.id, self.first, self.last, self.state, self.role, self.district, self.party = pid, first, last, state, role, district, party
        self.fec_ids = set(fec_ids); self.pcc = set(); self.extra = extra or {}
        self.f = (norm(first) or [''])[0]; self.l = norm(last) or ['?']
    def name(self): return f'{self.first} {self.last}'
    def folder(self): return os.path.join(ROOT, self.state, self.id)
    def matches(self, toks):
        if not all(x in toks for x in self.l): return False
        f = self.f
        return any(t == f or t == f[:1] or (len(t) >= 3 and len(f) >= 3 and (t.startswith(f[:3]) or f.startswith(t))) for t in toks)

# ---------------------------------------------------------------- who is in office
def load_people(states):
    log('Loading current members of Congress')
    raw = fetch(LEGISLATORS)
    if not raw: log('  could not download the current-members list (github.com). Check your connection and run again.'); raise SystemExit(1)
    people = []
    for m in json.loads(raw):
        t = m['terms'][-1]
        if t['state'] not in states: continue
        n = m['name']; first = n.get('nickname') or n.get('first'); last = n.get('last')
        role = 'senator' if t['type'] == 'sen' else 'representative'
        pid = f"{t['state'].lower()}-{'sen' if role == 'senator' else str(t.get('district', '')).zfill(2)}-{slug(first + ' ' + last)}"
        people.append(Person(pid, first, last, t['state'], role, '' if role == 'senator' else str(t.get('district', '')), t.get('party', ''),
                             m['id'].get('fec') or [], {'bioguide': m['id'].get('bioguide'), 'serving_since': m['terms'][0]['start'],
                                                        'terms': len(m['terms']), 'official_name': n.get('official_full', '')}))
    for st, first, last in GOVERNORS:
        if st in states: people.append(Person(f'{st.lower()}-gov-{slug(first + " " + last)}', first, last, st, 'governor'))
    log(f'  {sum(1 for p in people if p.role != "governor")} members of Congress and {sum(1 for p in people if p.role == "governor")} governors')
    return people

# ---------------------------------------------------------------- national lookups
def fec_file(dl, y, f): return fetch(FEC.format(y=y, f=f), os.path.join(dl, 'fec', str(y), f), quiet=True)

def find_ids(people, dl, cycles):
    """add every FEC candidate ID (any office, any cycle) that matches each person by name and state; record principal committees"""
    by = {}
    for p in people: by.setdefault((p.state, p.l[-1]), []).append(p)
    known = {i: p for p in people for i in p.fec_ids}
    for y in cycles:
        path = fec_file(dl, y, f'cn{str(y)[2:]}.zip')
        if not path: continue
        for r in zip_rows(path, CN):
            cid = r.get('CAND_ID', '')
            p = known.get(cid)
            if not p:
                for q in by.get((r.get('CAND_OFFICE_ST', ''), (norm(r.get('CAND_NAME', '').split(',')[0]) or ['?'])[-1]), []):
                    if q.matches(set(norm(r.get('CAND_NAME', '')))): p = q; break
            if p:
                p.fec_ids.add(cid); known[cid] = p
                if r.get('CAND_PCC'): p.pcc.add((y, r['CAND_PCC']))

def committees(dl, cycles):
    cm = {}
    for y in cycles:
        path = fec_file(dl, y, f'cm{str(y)[2:]}.zip')
        if not path: continue
        for r in zip_rows(path, CM):
            if r.get('CMTE_ID'): cm[r['CMTE_ID']] = r
    return cm

def fara_firms(dl):
    """registered foreign agents and the countries of their foreign principals"""
    firms = {}
    def rows(url):
        p = fetch(url, os.path.join(dl, 'fara', url.rsplit('/', 1)[1]))
        if not p: return []
        try: z = zipfile.ZipFile(p)
        except zipfile.BadZipFile: return []
        out = []
        for m in z.namelist():
            if m.lower().endswith('.csv'): out += list(csv.DictReader(io.TextIOWrapper(z.open(m), encoding='utf-8', errors='replace')))
        return out
    regs = rows(FARA_REGISTRANTS); pr = rows(FARA_PRINCIPALS)
    key = lambda d, *ks: next((d[k] for k in d if any(x.lower() == k.lower().strip() for x in ks)), '')
    countries = {}
    for r in pr:
        countries.setdefault(key(r, 'Registration Number', 'Registration_Number'), set()).add(key(r, 'Country/Location Represented', 'Country', 'Country Name'))
    for r in regs:
        num = key(r, 'Registration Number', 'Registration_Number'); nm = key(r, 'Name', 'Registrant Name', 'Registrant_Name')
        if nm: firms[' '.join(norm(nm))] = {'name': nm, 'registration': num, 'countries': sorted(c for c in countries.get(num, []) if c)}
    log(f'  FARA: {len(firms)} registrants' if firms else '  FARA files unavailable; the foreign-agent cross-check is skipped')
    return firms

def classify(cm, fara):
    """what each committee is; and whether it is tied to another country's policy or to a registered foreign agent"""
    info = {}
    for cid, r in cm.items():
        nm, org = r.get('CMTE_NM', ''), r.get('CONNECTED_ORG_NM', '')
        tp, ds, ot = r.get('CMTE_TP', ''), r.get('CMTE_DSGN', ''), r.get('ORG_TP', '')
        if tp in ('X', 'Y', 'Z'): kind = 'Party'
        elif ds == 'D': kind = 'Leadership PAC'
        elif ds == 'B': kind = 'Lobbyist/registrant PAC'
        elif ot in ('C', 'W'): kind = 'Corporate PAC'
        elif ot == 'T': kind = 'Trade association PAC'
        elif ot == 'L': kind = 'Labor PAC'
        elif ot == 'M': kind = 'Membership organization PAC'
        elif ot == 'V': kind = 'Cooperative PAC'
        elif tp in ('O', 'U', 'V', 'W'): kind = 'Super PAC / hybrid PAC'
        elif tp in ('H', 'S', 'P') or ds in ('A', 'P', 'J'): kind = 'Candidate committee / joint fundraiser'
        elif tp in ('Q', 'N'): kind = 'Nonconnected (ideological/issue) PAC'
        else: kind = CMTE_TP.get(tp, 'Other')
        fp, why = '', ''
        for rx, country in NAMED.items():
            if re.search(rx, nm + ' ' + org, re.I): fp, why = country, f'named committee ({rx})'; break
        if not fp:
            m = COUNTRY_RX.search(nm) or COUNTRY_RX.search(org)
            if m and not (tp in ('H', 'S', 'P') or ds in ('A', 'P')):
                fp, why = m.group(1).title(), 'country word in its name' + (' (looks like a company or local group: check)' if LOCALISH.search(nm + ' ' + org) else '')
        fa = fara.get(' '.join(norm(org))) or fara.get(' '.join(norm(nm)))
        info[cid] = {'name': nm, 'connected_org': org, 'kind': kind, 'type': CMTE_TP.get(tp, tp), 'designation': CMTE_DSGN.get(ds, ds),
                     'org_type': ORG_TP.get(ot, ot), 'foreign_policy': fp, 'foreign_policy_reason': why,
                     'fara_registrant': fa['name'] if fa else '', 'fara_countries': '; '.join(fa['countries']) if fa else ''}
    return info

# ---------------------------------------------------------------- the money, per person
def collect(people, dl, cycles, info):
    ids = {i: p for p in people for i in p.fec_ids}
    totals = {p.id: [] for p in people}; tx = {p.id: [] for p in people}
    for y in cycles:
        path = fec_file(dl, y, f'weball{str(y)[2:]}.zip')
        if path:
            for r in zip_rows(path, WEBALL):
                p = ids.get(r.get('CAND_ID'))
                if p: totals[p.id].append({'cycle': y, 'fec_id': r['CAND_ID'], 'receipts': money(r['TTL_RECEIPTS']), 'individuals': money(r['TTL_INDIV_CONTRIB']),
                    'pacs_and_committees': money(r['OTHER_POL_CMTE_CONTRIB']), 'party': money(r['POL_PTY_CONTRIB']), 'self': money(r['CAND_CONTRIB']),
                    'candidate_loans': money(r['CAND_LOANS']), 'spent': money(r['TTL_DISB']), 'cash_on_hand': money(r['COH_COP']), 'through': r['CVG_END_DT'],
                    'general_result': r['GEN_ELECTION']})
        path = fec_file(dl, y, f'pas2{str(y)[2:]}.zip')
        if not path: continue
        log(f'  reading committee money {y}')
        for v in zip_rows(path, None):
            if len(v) < 17: continue
            p = ids.get(v[16])
            if not p: continue
            c = info.get(v[0], {})
            tx[p.id].append([y, v[13], money(v[14]), TX_TP.get(v[5], v[5]), v[0], c.get('name') or v[7], c.get('kind', ''), c.get('connected_org', ''),
                             c.get('foreign_policy', ''), c.get('fara_registrant', ''), c.get('fara_countries', ''), v[16],
                             f'https://docquery.fec.gov/cgi-bin/fecimg/?{v[4]}' if v[4] else ''])
    return totals, tx

def api_get(path, key, **q):
    q['api_key'] = key
    b = fetch(f'{API}{path}?{urllib.parse.urlencode(q)}', headers={'Accept': 'application/json'})
    time.sleep(3.7)   # stays under the API's 1,000 calls an hour
    return json.loads(b) if b else None

def api_extras(people, key, info, since, used, dl):
    """1) individual donations forwarded through foreign-policy PACs acting as conduits (earmarks), for everyone;
       2) top employers of each person's individual donors, cycle by cycle. Both resumable."""
    start = max(since, 2008)
    cm_to_p = {}
    for p in people:
        for _, cmte in p.pcc: cm_to_p[cmte] = p
    conduits = sorted(cid for cid, c in info.items() if cid in used and c['foreign_policy'] and c['type'] in ('PAC', 'PAC (nonqualified)'))
    log(f'\nFEC API 1/2: earmarked donations through {len(conduits)} flagged foreign-policy PACs (every recipient, since {start})')
    ear = {p.id: [] for p in people}; allrows = []; incomplete = []
    for n, cid in enumerate(conduits, 1):
        ok = True
        cache = os.path.join(dl, 'fec_api', f'conduit2_{cid}_{start}.json')
        if os.path.exists(cache):
            rows = json.load(open(cache))
        else:
            rows, last, pages, ok = [], {}, 0, True
            while True:
                d = api_get('/schedules/schedule_b/', key, committee_id=cid, min_date=f'{start}-01-01', per_page=100, sort='-disbursement_date', **last)
                if d is None: ok = False; break
                if not d.get('results'): break
                for r in d['results']:
                    rows.append([r.get('disbursement_date', '')[:10], money(r.get('disbursement_amount')), r.get('recipient_committee_id') or '',
                                 r.get('recipient_name') or '', r.get('disbursement_description') or r.get('memo_text') or '', r.get('memo_code') or '', r.get('pdf_url') or ''])
                pages += 1
                if pages % 25 == 0: log(f'    {info[cid]["name"]}: {len(rows)} rows so far')
                li = (d.get('pagination') or {}).get('last_indexes')
                if not li: break
                last = li
            if ok:
                os.makedirs(os.path.dirname(cache), exist_ok=True); json.dump(rows, open(cache, 'w'))
            else:
                incomplete.append(info[cid]['name'])
        log(f'  {n} of {len(conduits)}: {info[cid]["name"]} ({info[cid]["foreign_policy"]}): {len(rows)} disbursements' + ('' if ok else ' (INCOMPLETE: not saved, retried next run)'))
        for r in rows:
            p = cm_to_p.get(r[2])
            allrows.append([r[0], r[1], cid, info[cid]['name'], info[cid]['foreign_policy'], r[2], r[3], p.id if p else '', r[4], r[5], r[6]])
            if p: ear[p.id].append([r[0], r[1], cid, info[cid]['name'], info[cid]['foreign_policy'], r[4], r[5], r[6]])
    wcsv(os.path.join(ROOT, 'foreign_policy_pac_disbursements.csv'), ['date', 'amount', 'pac_id', 'pac', 'country', 'recipient_committee', 'recipient',
         'official', 'description', 'memo_code', 'filing'], allrows)
    totals = {}
    for p in people:
        if ear[p.id]:
            wcsv(os.path.join(p.folder(), 'foreign_policy_conduit_transfers.csv'),
                 ['date', 'amount', 'conduit_id', 'conduit', 'country', 'description', 'memo_code', 'filing'], ear[p.id])
            totals[p.id] = round(sum(r[1] for r in ear[p.id] if 'EARMARK' in (r[5] or '').upper() or r[6] == 'X'), 2)
    add_column('flagged_foreign_policy_earmarks_api', totals)
    if incomplete: log(f'  {len(incomplete)} PAC list(s) incomplete and not saved; run again to finish them: ' + '; '.join(incomplete))
    log(f'\nFEC API 2/2: top donor employers per cycle (about 4 seconds per lookup; safe to stop and re-run)')
    todo = [p for p in people if p.pcc and not os.path.exists(os.path.join(p.folder(), 'donor_employers_by_cycle.csv'))]
    for i, p in enumerate(todo, 1):
        rows, ok = [], True
        for y, cmte in sorted(p.pcc):
            if y < start: continue
            d = api_get('/schedules/schedule_a/by_employer/', key, committee_id=cmte, cycle=y, sort='-total', per_page=20)
            if d is None: ok = False; continue
            for r in d.get('results', []): rows.append([y, cmte, r.get('employer'), money(r.get('total')), r.get('count')])
        if ok: wcsv(os.path.join(p.folder(), 'donor_employers_by_cycle.csv'), ['cycle', 'committee', 'employer', 'total', 'donations'], rows)
        if i % 20 == 0: log(f'  {i} of {len(todo)}')

def add_column(name, values):
    path = os.path.join(ROOT, 'summary.csv')
    rows = list(csv.reader(open(path, encoding='utf-8')))
    if name in rows[0]: k = rows[0].index(name)
    else: rows[0].append(name); k = len(rows[0]) - 1
    for r in rows[1:]:
        while len(r) <= k: r.append('')
        r[k] = values.get(r[0], 0)
    wcsv(path, rows[0], rows[1:])

# ---------------------------------------------------------------- output
def write(people, totals, tx, info):
    used = set(); summ = []
    for p in people:
        T = sorted(totals[p.id], key=lambda t: t['cycle']); X = sorted(tx[p.id], key=lambda r: (r[0], r[1]))
        if p.fec_ids or p.role != 'governor':
            wjson(os.path.join(p.folder(), 'profile.json'), {'name': p.name(), 'role': p.role, 'state': p.state, 'district': p.district, 'party': p.party,
                  'fec_ids': sorted(p.fec_ids), 'principal_committees': sorted(f'{c} ({y})' for y, c in p.pcc), **p.extra, 'cycles': T,
                  'note': 'Governors: only federal campaigns appear here; state campaign money is not included.' if p.role == 'governor' else ''})
            wcsv(os.path.join(p.folder(), 'committee_money.csv'), ['cycle', 'date', 'amount', 'what', 'committee_id', 'committee', 'committee_kind', 'connected_org',
                 'foreign_policy_country', 'fara_registrant', 'fara_countries', 'to_fec_id', 'filing'], X)
        given = [r for r in X if r[3] in ('Contribution', 'In-kind contribution', 'Contribution (unregistered)')]
        s = lambda rows: round(sum(r[2] for r in rows), 2)
        by_kind = {}
        for r in given: by_kind[r[6]] = by_kind.get(r[6], 0) + r[2]
        fp_given = [r for r in given if r[8]]; fp_for = [r for r in X if r[8] and 'FOR' in r[3]]; fp_against = [r for r in X if r[8] and 'AGAINST' in r[3]]
        fp_c = {}
        for r in fp_given + fp_for: fp_c[r[8]] = fp_c.get(r[8], 0) + r[2]
        for r in X: used.add(r[4])
        summ.append([p.id, p.name(), p.role, p.state, p.district, p.party, p.extra.get('serving_since', ''), ' '.join(sorted(p.fec_ids)),
                     f"{T[0]['cycle']}-{T[-1]['cycle']}" if T else '', len({t['cycle'] for t in T}), round(sum(t['receipts'] for t in T), 2),
                     round(sum(t['individuals'] for t in T), 2), round(sum(t['pacs_and_committees'] for t in T), 2), s(given),
                     round(by_kind.get('Corporate PAC', 0), 2), round(by_kind.get('Trade association PAC', 0), 2), round(by_kind.get('Lobbyist/registrant PAC', 0), 2),
                     round(by_kind.get('Labor PAC', 0), 2), round(by_kind.get('Leadership PAC', 0), 2), round(by_kind.get('Party', 0), 2),
                     round(by_kind.get('Nonconnected (ideological/issue) PAC', 0), 2), s(fp_given), s(fp_for), s(fp_against),
                     '; '.join(f'{k} ${v:,.0f}' for k, v in sorted(fp_c.items(), key=lambda kv: -kv[1])), s([r for r in given if r[9]]),
                     s([r for r in X if 'FOR' in r[3]]), s([r for r in X if 'AGAINST' in r[3]])])
    wcsv(os.path.join(ROOT, 'summary.csv'), ['id', 'name', 'role', 'state', 'district', 'party', 'serving_since', 'fec_ids', 'cycles_span', 'cycles_with_money',
         'career_receipts', 'career_from_individuals', 'career_from_pacs_and_committees', 'committee_contributions_itemized', 'corporate_pacs', 'trade_association_pacs',
         'lobbyist_pacs', 'labor_pacs', 'leadership_pacs', 'party_committees', 'ideological_issue_pacs', 'flagged_foreign_policy_pacs_gave', 'flagged_foreign_policy_spent_for',
         'flagged_foreign_policy_spent_against', 'flagged_foreign_policy_by_country', 'from_pacs_tied_to_registered_foreign_agents', 'all_outside_spending_for',
         'all_outside_spending_against'], sorted(summ, key=lambda r: (r[3], r[2], r[4], r[1])))
    fl = [[cid, c['name'], c['connected_org'], c['kind'], c['foreign_policy'], c['foreign_policy_reason'], c['fara_registrant'], c['fara_countries']]
          for cid, c in info.items() if (c['foreign_policy'] or c['fara_registrant']) and cid in used]
    wcsv(os.path.join(ROOT, 'foreign_policy_committees.csv'), ['committee_id', 'committee', 'connected_org', 'kind', 'country', 'why_flagged', 'fara_registrant',
         'fara_countries'], sorted(fl, key=lambda r: (r[4], r[1])))
    with open(os.path.join(ROOT, '.gitignore'), 'w') as f: f.write('_downloads/\n*.part\n.DS_Store\n')
    wjson(os.path.join(ROOT, 'manifest.json'), {'script': 'ots_members_money.py ' + VERSION, 'run_at': NOW, 'people': len(people),
          'sources': {'members': LEGISLATORS, 'fec_bulk': FEC.format(y='{cycle}', f='...'), 'fara': [FARA_REGISTRANTS, FARA_PRINCIPALS]}})
    return used

def main():
    a = sys.argv[1:]
    states = [a[i + 1].upper() for i, x in enumerate(a) if x == '--state'] or STATES
    since = int(a[a.index('--since') + 1]) if '--since' in a else 1980
    cycles = list(range(since - since % 2, 2028, 2))
    key = os.environ.get('FEC_API_KEY') or (a[a.index('--fec-key') + 1] if '--fec-key' in a else None)
    dl = next((d for d in SIBLING_DL if os.path.isdir(d)), os.path.join(ROOT, '_downloads'))
    log(f'OTS members money {VERSION}: cycles {cycles[0]}-{cycles[-1]}, saving to {ROOT}\n  downloads: {dl}')
    people = load_people(set(states))
    log('\nMatching every FEC candidate record (any office, any cycle)'); find_ids(people, dl, cycles)
    log(f'  {sum(1 for p in people if p.fec_ids)} of {len(people)} people have federal campaign records')
    log('\nCommittee directory and foreign-agent registrations'); info = classify(committees(dl, cycles), fara_firms(dl))
    log(f'  {len(info)} committees; {sum(1 for c in info.values() if c["foreign_policy"])} tied by name to another country; '
        f'{sum(1 for c in info.values() if c["fara_registrant"])} connected to a registered foreign agent')
    log('\nCollecting money'); totals, tx = collect(people, dl, cycles, info)
    used = write(people, totals, tx, info)
    if key: api_extras(people, key, info, since, used, dl)
    else: log('\n(No FEC_API_KEY: skipped donor employers and conduit earmarks. Free key: https://api.data.gov/signup/)')
    log(f'\nFinished: {len(people)} people in {ROOT}\n  Start with summary.csv and foreign_policy_committees.csv.'
        f'\n\nTo share it:\n  cd "{ROOT}"\n  git init -b main; git add -A; git commit -m "Members money {NOW}"'
        f'\n  git remote add origin git@github.com:Ronaldoh1/<repo>.git; git push -u origin main')

if __name__ == '__main__':
    try:
        main()
    except NetworkDown as e:
        log(f'\nThe internet connection was down for 30 minutes ({e}).\nEverything finished so far is saved. When you are back online,'
            ' run the same command again in the same folder: it skips what is already done and continues.')
        raise SystemExit(2)
