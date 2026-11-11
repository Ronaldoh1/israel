#!/usr/bin/env python3
"""
OTS 2026 Elections: the two record types still missing, for ballot candidates only.

Run it on your own computer (Python 3.8+, nothing to install), from this folder:
    COURTLISTENER_TOKEN=yourtoken python3 ots_ballot_records.py
Options:
    --only courts        run one step (courts, senate)
    --only senate
    --state GA           only some states (repeat for more)

It reads ballot_2026.csv (in this folder): the 1,354 people on the November 3 ballot. Nobody else.

What it pulls:
  1 courts   Federal court dockets and court opinions that name each ballot candidate, from
             CourtListener (free account needed: www.courtlistener.com > sign up > your profile >
             API token). A name search finds namesakes and passing mentions too: every hit is a
             lead that gets checked before anything is published.
  2 senate   Senate financial disclosure reports (annual reports, stock-trade reports, candidate
             reports) for every Senate candidate on the ballot, from efdsearch.senate.gov. No
             account needed. (House candidates' disclosures were already pulled by the 2026 collector.)

Output: a folder called ballot-records, one folder per state, one per candidate:
    ballot-records/GA/ga-sen-jon-ossoff/courts_courtlistener.json
    ballot-records/GA/ga-sen-jon-ossoff/senate_disclosures.json
plus ballot-records/summary.csv (one row per candidate: how many court hits and disclosure reports).

Safe to stop and re-run: finished candidates are skipped. If the internet drops, it waits for the
connection to come back (up to an hour) and carries on by itself.
Takes about 1-2 hours for courts (CourtListener allows about one search a second) and 20 minutes for Senate.
"""
import csv, http.cookiejar, json, os, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.environ.get('OTS_RECORDS_DIR') or os.path.join(HERE, 'ballot-records'))
BALLOT = os.path.join(HERE, 'ballot_2026.csv')
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
CL_SEARCH = 'https://www.courtlistener.com/api/rest/v4/search/'
EFD = 'https://efdsearch.senate.gov'

def log(*a): print(*a, flush=True)
def ssl_ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()
CTX = ssl_ctx()
CERT_HELP = ('\n  SSL certificate problem. On a Mac, open Applications > Python 3.x and double-click'
             '\n  "Install Certificates.command" (or run: pip3 install certifi), then run this again.\n')

class NetworkDown(Exception):
    """the connection stayed down too long; everything finished so far is saved"""

PATIENCE = 3600   # seconds to keep waiting for the connection to come back

def request(opener, url, data=None, headers=None, tries=6):
    """Returns the response bytes, or None for a definite refusal (bad token, not found).
    If the network drops it waits and keeps retrying for up to an hour, then raises NetworkDown."""
    h = {'User-Agent': UA}; h.update(headers or {})
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    busy = 0; down_since = None
    while True:
        try:
            with opener.open(urllib.request.Request(url, data=body, headers=h), timeout=90) as r:
                if down_since: log('    connection is back; continuing')
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                try: ra = int(e.headers.get('Retry-After') or 0)
                except ValueError: ra = 0
                if ra > 300:   # CourtListener's search API allows 125 requests a day; wait for the window to reopen
                    until = time.strftime('%a %H:%M', time.localtime(time.time() + ra + 60))
                    log(f'    daily limit reached (125 searches a day); finished candidates are saved; resuming automatically at {until}')
                    time.sleep(ra + 60); busy = 0; continue
            if e.code == 429 or e.code >= 500:
                busy += 1
                if busy > tries: log(f'    the site kept answering {e.code}; skipping for now'); return None
                wait = 30 * busy; log(f'    site busy ({e.code}); waiting {wait}s'); time.sleep(wait); continue
            if e.code in (401, 403): log(f'    refused ({e.code}): {url}'); return None
            log(f'    HTTP {e.code}: {url}'); return None
        except (ssl.SSLError, ssl.CertificateError):
            log(CERT_HELP); raise SystemExit(1)
        except Exception as e:
            if 'CERTIFICATE' in str(e).upper(): log(CERT_HELP); raise SystemExit(1)
            now = time.time()
            if down_since is None:
                down_since = now; log(f'    connection lost ({getattr(e, "reason", e)}); waiting for it to come back...')
            elif now - down_since > PATIENCE:
                raise NetworkDown()
            time.sleep(30)

def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + '.part', 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(path + '.part', path)

def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
SUFFIX = re.compile(r',?\s+(jr|sr|ii|iii|iv)\.?$', re.I)
def split_name(name):
    n = SUFFIX.sub('', name.replace('"', '').strip())
    parts = [p for p in n.split() if not re.fullmatch(r'[A-Z]\.?', p)]   # drop middle initials
    return (parts[0], parts[-1]) if len(parts) > 1 else (n, n)

class Cand:
    def __init__(self, r):
        self.race, self.state, self.office, self.name = r['race'], r['state'], r['office'], r['name']
        self.incumbent = (r.get('incumbent') or '').strip().lower() == 'yes'
        self.id = r['data_id'] or '%s-%s' % (r['race'].lower(), slug(r['name']))
        self.first, self.last = split_name(r['name'])
        self.full = SUFFIX.sub('', r['name'].replace('"', '').strip())
    def folder(self): return os.path.join(ROOT, self.state, self.id)

# ---------------------------------------------------------------- 1. courts
def run_courts(cands, token):
    log('\n[1/2] Federal court records (CourtListener)')
    if not token:
        log('  skipped: no token. Make a free account at www.courtlistener.com, copy the API token from your profile, then run:'
            '\n  COURTLISTENER_TOKEN=yourtoken python3 ots_ballot_records.py --only courts'); return
    op = urllib.request.build_opener(urllib.request.HTTPSHandler(context=CTX))
    H = {'Authorization': f'Token {token}', 'Accept': 'application/json'}
    todo = [c for c in cands if not os.path.exists(os.path.join(c.folder(), 'courts_courtlistener.json'))]
    # highest-stakes first: Senate and governor races, then sitting members of Congress, then everyone else
    todo.sort(key=lambda c: (0 if c.office in ('senate', 'governor') else 1 if c.incumbent else 2))
    log(f'  {len(cands) - len(todo)} already done, {len(todo)} to search')
    for i, c in enumerate(todo, 1):
        short = f'{c.first} {c.last}'
        q = f'"{short}"' if short == c.full else f'"{c.full}" OR "{short}"'
        out = {'candidate': c.name, 'race': c.race, 'searched_on': NOW, 'query': q,
               'note': 'Exact-name full-text search. Hits include namesakes and passing mentions; each needs a check before use.'}
        # one search per candidate (federal dockets, which include the parties to every case) to fit the 125-a-day limit;
        # set CL_TYPES=ro to also search opinions
        for typ, label in [(t, {'r': 'federal_dockets', 'o': 'opinions'}[t]) for t in (os.environ.get('CL_TYPES') or 'r') if t in 'ro']:
            b = request(op, CL_SEARCH + '?' + urllib.parse.urlencode({'q': q, 'type': typ, 'order_by': 'dateFiled desc'}), headers=H)
            if b is None: out[label] = 'search failed'; continue
            d = json.loads(b)
            out[label + '_count'] = d.get('count')
            out[label] = [{'case': x.get('caseName'), 'court': x.get('court') or x.get('court_id'), 'filed': x.get('dateFiled'),
                           'docket': x.get('docketNumber'), 'url': 'https://www.courtlistener.com' + (x.get('absolute_url') or '')}
                          for x in (d.get('results') or [])[:25]]
            time.sleep(1.2)
        if 'search failed' in (out.get('federal_dockets'), out.get('opinions')):
            log(f'  {c.name}: a search failed; it will be retried next run'); continue
        wjson(os.path.join(c.folder(), 'courts_courtlistener.json'), out)
        if i % 25 == 0: log(f'  {i} of {len(todo)}')
    log('  done')

# ---------------------------------------------------------------- 2. Senate financial disclosures
def efd_session():
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar), urllib.request.HTTPSHandler(context=CTX))
    page = request(op, EFD + '/search/home/')
    if page is None: return None, None
    m = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', page)
    if not m: return None, None
    # accept the site's terms of use (the same checkbox you tick in the browser)
    request(op, EFD + '/search/home/', data={'prohibition_agreement': '1', 'csrfmiddlewaretoken': m.group(1).decode()},
            headers={'Referer': EFD + '/search/home/'})
    tok = next((ck.value for ck in jar if ck.name == 'csrftoken'), None)
    return op, tok

def run_senate(cands):
    log('\n[2/2] Senate financial disclosures (efdsearch.senate.gov)')
    sen = [c for c in cands if c.office == 'senate']
    todo = [c for c in sen if not os.path.exists(os.path.join(c.folder(), 'senate_disclosures.json'))]
    log(f'  {len(sen)} Senate candidates on the ballot; {len(sen) - len(todo)} already done, {len(todo)} to search')
    if not todo: return
    op, tok = efd_session()
    if not op or not tok:
        log('  Could not open efdsearch.senate.gov (the site may be down or its sign-in page changed).'
            '\n  Try again later. If it keeps failing, tell Claude and paste the message above.'); return
    for i, c in enumerate(todo, 1):
        rows, start, ok = [], 0, False
        while True:
            b = request(op, EFD + '/search/report/data/', headers={'Referer': EFD + '/search/', 'X-CSRFToken': tok},
                        data={'start': str(start), 'length': '100', 'report_types': '[]', 'filer_types': '[]',
                              'submitted_start_date': '01/01/2012 00:00:00', 'submitted_end_date': '',
                              'candidate_state': '', 'senator_state': '', 'office_id': '',
                              'first_name': '', 'last_name': c.last, 'csrfmiddlewaretoken': tok})
            if b is None: break
            try: d = json.loads(b)
            except ValueError:
                op, tok = efd_session(); break            # session expired: renew, retry this person next run
            for r in d.get('data', []):
                link = re.search(r'href="([^"]+)"[^>]*>([^<]+)<', r[3] or '')
                rows.append({'first': r[0], 'last': r[1], 'filer': r[2], 'report': link.group(2).strip() if link else re.sub('<[^>]+>', '', r[3] or ''),
                             'url': EFD + link.group(1) if link else '', 'filed': r[4]})
            start += 100
            if start >= int(d.get('recordsFiltered') or 0): ok = True; break
            time.sleep(1)
        if not ok:
            log(f'  {c.name}: search failed; it will be retried next run')
            if not op: log('  Lost the connection to efdsearch.senate.gov; run the script again later.'); return
            continue
        f3 = c.first[:3].lower()
        mine = [r for r in rows if (r['first'] or '').lower().startswith(f3) or f3 in (r['filer'] or '').lower()]
        wjson(os.path.join(c.folder(), 'senate_disclosures.json'),
              {'candidate': c.name, 'race': c.race, 'searched_on': NOW, 'searched_last_name': c.last,
               'note': 'Reports filed under this last name whose first name matches. Other filers with the same last name are in "same_last_name_other".',
               'reports': mine, 'same_last_name_other': [r for r in rows if r not in mine]})
        time.sleep(1.5)
        if i % 10 == 0: log(f'  {i} of {len(todo)}')
    log('  done')

# ---------------------------------------------------------------- summary
def write_summary(cands):
    out = []
    for c in cands:
        ct = os.path.join(c.folder(), 'courts_courtlistener.json'); sd = os.path.join(c.folder(), 'senate_disclosures.json')
        C = json.load(open(ct, encoding='utf-8')) if os.path.exists(ct) else {}
        S = json.load(open(sd, encoding='utf-8')) if os.path.exists(sd) else {}
        out.append([c.race, c.name, c.id, C.get('federal_dockets_count', ''), C.get('opinions_count', ''),
                    len(S.get('reports', [])) if S else ('' if c.office != 'senate' else 'not yet')])
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, 'summary.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['race', 'name', 'id', 'court_dockets', 'court_opinions', 'senate_disclosure_reports']); w.writerows(out)
    with open(os.path.join(ROOT, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(f'Pulled by ots_ballot_records.py on {NOW}, for the {len(cands)} candidates in ballot_2026.csv.\n'
                'Court hits are name matches (leads to check), not findings.\n')

def main():
    a = sys.argv[1:]
    if not os.path.exists(BALLOT): log('ballot_2026.csv must be in the same folder as this script.'); return
    only = set(a[a.index('--only') + 1].split(',')) if '--only' in a else {'courts', 'senate'}
    states = {a[i + 1].upper() for i, x in enumerate(a) if x == '--state'}
    cands = [Cand(r) for r in csv.DictReader(open(BALLOT, encoding='utf-8')) if not states or r['state'] in states]
    log(f'OTS ballot records: {len(cands)} ballot candidates, saving to {ROOT}')
    done = False
    try:
        if 'courts' in only: run_courts(cands, os.environ.get('COURTLISTENER_TOKEN') or (a[a.index('--token') + 1] if '--token' in a else None))
        if 'senate' in only: run_senate(cands)
        done = True
    except NetworkDown:
        log('\nThe internet connection was down for over an hour, so the script stopped.'
            '\nEverything finished so far is saved. Run the same command again to continue where it left off.')
    except KeyboardInterrupt:
        log('\nStopped. Everything finished so far is saved. Run the same command again to continue.')
    write_summary([Cand(r) for r in csv.DictReader(open(BALLOT, encoding='utf-8'))] if states else cands)
    if not done: sys.exit(2)
    log(f'\nFinished. Results are in {ROOT}'
        '\nTo send them: zip the ballot-records folder (right-click > Compress), then upload it as a release, for example:'
        '\n  gh release create ballot-records ballot-records.zip -R Ronaldoh1/2026electiondata -t "Ballot records" -n "Courts and Senate disclosures"')

if __name__ == '__main__':
    main()
