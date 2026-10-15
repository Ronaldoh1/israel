#!/usr/bin/env python3
"""
OTS 2026 Elections: the research pack. Everything a candidate page needs besides money,
for the 1,354 people on the November 3 ballot (ballot_2026.csv in this folder). Nobody else.

Run it on your own computer (Python 3.8+, nothing to install), from this folder:
    FEC_API_KEY=yourkey python3 ots_research_pack.py
(The same free api.data.gov key you use for the FEC also works for congress.gov.)
Options:
    --only wiki,ballotpedia      run only some steps (steps listed below)
    --state GA                   only some states (repeat for more)

Steps, in the order they run:
  ids          Matches sitting and former members of Congress to their official IDs
               (the congress-legislators project). Quick.
  wiki         Wikipedia article text for each candidate: biography, career, controversies.
               Members of Congress are matched by their official ID; everyone else by a search that
               must name the right state and a political role, otherwise nothing is saved.
  photos       Official portraits for members of Congress (public domain); for others, the Wikipedia
               photo with its license and photographer, only when Wikipedia gives a license.
  ballotpedia  The candidate's Ballotpedia page (career, positions, survey answers, campaign links).
  campaign     The candidate's own campaign website: home page and up to 3 issues/priorities pages.
  votes        Every recorded floor vote for anyone who served in Congress since 2007 (Voteview),
               plus a shorter file of votes on major subjects (Israel and the Middle East, Ukraine,
               China, defense, budget, taxes, health care, immigration, elections and certification,
               guns, abortion...). The same subject list for everyone.
  bills        Bills each member sponsored and co-sponsored, with subject and latest action (congress.gov;
               needs the key). Also their current committee seats.
  ethics       House and Senate Ethics Committee reports, letters and press releases that mention the
               candidate's name. These are leads to check, not findings.

Output: a folder called research-pack, one folder per state, one per candidate, plus summary.csv.
Safe to stop and re-run: finished pieces are skipped. If the internet drops, it waits for the
connection to come back (up to an hour) and carries on by itself.
Expect several hours for everything. You can run steps separately with --only.
"""
import csv, html, json, os, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, 'research-pack')
DL = os.path.join(ROOT, '_downloads')
BALLOT = os.path.join(HERE, 'ballot_2026.csv')
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
UA = 'OTS-ballot-research/1.0 (public-records research script; https://github.com/Ronaldoh1)'
BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
STEPS = ['ids', 'wiki', 'photos', 'ballotpedia', 'campaign', 'votes', 'bills', 'ethics']
CONGRESSES = range(110, 120)   # 2007-2026

STATE_NAMES = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',
    'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
POLITICAL = re.compile(r'politic|candidate|congress|senat|representative|governor|legislat|mayor|council|attorney general|secretary of state|'
                       r'treasurer|commissioner|sheriff|judge|state house|assembly|nominee|official|activist|businessm|businessw|executive', re.I)
SUBJECTS = re.compile(r'israel|iran|gaza|palestin|hamas|hezbollah|houthi|west bank|jerusalem|antisemit|anti-semit|boycott|\bbds\b|middle east|'
                      r'ukrain|russia|china|chinese|taiwan|foreign aid|security assistance|national defense authorization|\bndaa\b|'
                      r'appropriation|continuing appropriations|budget|debt limit|debt ceiling|tax|tariff|health care|affordable care|medicare|medicaid|'
                      r'social security|immigra|border|asylum|electoral|certif|capitol|january 6|impeach|voting rights|election|firearm|\bgun|'
                      r'abortion|reproductive|surveillance|fisa|infrastructure|inflation reduction|climate|tiktok|crypto|stock trading', re.I)

# ---------------------------------------------------------------- network
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
OPENER = urllib.request.build_opener(urllib.request.HTTPSHandler(context=CTX))
PATIENCE = 3600

LAST = {'status': None}
def online():
    """is the internet up? (used to tell a dead website apart from a dropped connection)"""
    for u in ('https://en.wikipedia.org/static/favicon/wikipedia.ico', 'https://www.google.com/favicon.ico'):
        try:
            with OPENER.open(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=15): return True
        except urllib.error.HTTPError: return True
        except Exception: pass
    return False

class NetworkDown(Exception):
    """the connection stayed down too long; everything finished so far is saved"""

def fetch(url, headers=None, dest=None, tries=5, timeout=60, browser=False):
    """bytes (or the saved path with dest), or None for a definite failure (404, refused, site keeps erroring).
    Waits up to an hour for a dropped connection, then raises NetworkDown."""
    if dest and os.path.exists(dest) and os.path.getsize(dest) > 0: return dest
    h = {'User-Agent': BROWSER_UA if browser else UA, 'Accept': '*/*'}; h.update(headers or {})
    busy = 0; down_since = None; LAST['status'] = None
    while True:
        try:
            with OPENER.open(urllib.request.Request(url, headers=h), timeout=timeout) as r:
                LAST['status'] = r.status
                if down_since: log('    connection is back; continuing')
                if not dest: return r.read(8_000_000)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest + '.part', 'wb') as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b: break
                        f.write(b)
                os.replace(dest + '.part', dest); return dest
        except urllib.error.HTTPError as e:
            LAST['status'] = e.code
            if e.code == 429 or e.code >= 500:
                busy += 1
                if busy > tries: return None
                time.sleep(20 * busy); continue
            return None
        except (ssl.SSLError, ssl.CertificateError):
            log(CERT_HELP); raise SystemExit(1)
        except Exception as e:
            if 'CERTIFICATE' in str(e).upper(): log(CERT_HELP); raise SystemExit(1)
            # a dead or slow website is not the internet being down: check a known site before waiting
            if online():
                if down_since: log('    connection is back; continuing'); down_since = None
                busy += 1
                if busy > 2: LAST['status'] = 'unreachable'; return None
                time.sleep(3); continue
            if down_since is None:
                down_since = time.time(); log(f'    connection lost ({getattr(e, "reason", e)}); waiting for it to come back...')
            elif time.time() - down_since > PATIENCE:
                raise NetworkDown()
            time.sleep(30)

def get_json(url, **kw):
    b = fetch(url, **kw)
    if b is None: return None
    try: return json.loads(b)
    except ValueError: return None

def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + '.part', 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(path + '.part', path)
def wtext(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + '.part', 'w', encoding='utf-8') as f: f.write(s)
    os.replace(path + '.part', path)
def rjson(path, default=None):
    try: return json.load(open(path, encoding='utf-8'))
    except Exception: return default

class Text(HTMLParser):
    """visible text of a page, without scripts, styles, menus and footers"""
    SKIP = {'script', 'style', 'noscript', 'svg', 'nav', 'footer', 'header', 'form', 'iframe'}
    BLOCK = {'p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'tr', 'section', 'article', 'blockquote'}
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0; self.links = []; self._a = None
    def handle_starttag(self, t, a):
        if t in self.SKIP: self.skip += 1
        if t in self.BLOCK: self.out.append('\n')
        if t == 'a': self._a = [dict(a).get('href') or '', '']
    def handle_endtag(self, t):
        if t in self.SKIP and self.skip: self.skip -= 1
        if t == 'a' and self._a: self.links.append(tuple(self._a)); self._a = None
    def handle_data(self, d):
        if self._a is not None: self._a[1] += d
        if not self.skip: self.out.append(d)
    def text(self):
        s = re.sub(r'[ \t\r\f\v]+', ' ', ''.join(self.out))
        return re.sub(r'\n\s*\n+', '\n\n', s).strip()
def page_text(b):
    p = Text()
    try: p.feed(b.decode('utf-8', 'replace'))
    except Exception: pass
    return p.text(), p.links

# ---------------------------------------------------------------- candidates
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
SUFFIX = re.compile(r',?\s+(jr|sr|ii|iii|iv)\.?$', re.I)
class Cand:
    def __init__(self, r):
        self.race, self.state, self.office, self.name, self.party = r['race'], r['state'], r['office'], r['name'], r['party']
        self.id = r['data_id'] or '%s-%s' % (r['race'].lower(), slug(r['name']))
        self.incumbent = r['incumbent'] == 'yes'
        self.fec = set(x for x in re.split(r'[;,\s]+', r['fec_ids']) if x)
        clean = SUFFIX.sub('', r['name'].replace('"', '').strip())
        parts = [p for p in clean.split() if not re.fullmatch(r'[A-Z]\.?', p)]
        self.first, self.last, self.full = parts[0], parts[-1], clean
        self.bioguide = None; self.wiki_title = None
    def path(self, *f): return os.path.join(ROOT, self.state, self.id, *f)
    def statename(self): return STATE_NAMES.get(self.state, self.state)

# ---------------------------------------------------------------- 1. ids
LEG = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/gh-pages/{f}'
def run_ids(cands):
    log('\n[ids] Matching members of Congress to their official IDs')
    people = []
    for f in ('legislators-current.json', 'legislators-historical.json'):
        p = fetch(LEG.format(f=f), dest=os.path.join(DL, f))
        if not p: log(f'  could not download {f}; members will be matched by name search only'); continue
        people += json.load(open(p, encoding='utf-8'))
    byfec = {}
    for m in people:
        for x in m['id'].get('fec', []) or []: byfec[x] = m
    n = 0
    for c in cands:
        m = next((byfec[x] for x in c.fec if x in byfec), None)
        if not m: continue
        if (m['name'].get('last', '').lower() != c.last.lower() and c.last.lower() not in m['name'].get('official_full', '').lower()): continue
        terms = [{'type': t['type'], 'state': t['state'], 'district': t.get('district'), 'start': t['start'], 'end': t['end'], 'party': t.get('party')} for t in m['terms']]
        wjson(c.path('ids.json'), {'candidate': c.name, 'matched_by': 'FEC id ' + ', '.join(sorted(c.fec & set(m['id'].get('fec', [])))),
                                   'ids': m['id'], 'name': m['name'], 'bio': m.get('bio', {}), 'terms': terms})
        n += 1
    log(f'  {n} candidates have served in Congress')
def load_ids(cands):
    for c in cands:
        d = rjson(c.path('ids.json'))
        if d: c.bioguide = d['ids'].get('bioguide'); c.wiki_title = d['ids'].get('wikipedia')

# ---------------------------------------------------------------- 2. Wikipedia
WAPI = 'https://en.wikipedia.org/w/api.php?'
def wiki_page(title):
    d = get_json(WAPI + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'redirects': 1, 'titles': title,
                 'prop': 'extracts|pageimages|pageprops|info', 'explaintext': 1, 'piprop': 'original|name', 'inprop': 'url'}))
    if not d: return None
    pg = next(iter(d.get('query', {}).get('pages', {}).values()), {})
    if 'missing' in pg or not pg.get('extract'): return None
    if 'disambiguation' in (pg.get('pageprops') or {}): return None
    return pg
def run_wiki(cands):
    log('\n[wiki] Wikipedia articles')
    todo = [c for c in cands if not os.path.exists(c.path('wikipedia.json'))]
    log(f'  {len(cands) - len(todo)} done, {len(todo)} to look up')
    found = 0
    for i, c in enumerate(todo, 1):
        pg, how = None, ''
        if c.wiki_title:
            pg = wiki_page(c.wiki_title); how = 'official congressional ID record'
        if not pg:
            for q in (f'"{c.full}" {c.statename()}', f'{c.first} {c.last} {c.statename()} politician'):
                s = get_json(WAPI + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': q, 'srlimit': 5}))
                for hit in (s or {}).get('query', {}).get('search', []):
                    t = hit['title']
                    if c.last.lower() not in t.lower() or re.search(r'election|list of|district', t, re.I): continue
                    p = wiki_page(t)
                    if not p: continue
                    head = p['extract'][:4000]
                    if c.statename() in head and POLITICAL.search(head) and c.first[:3].lower() in head.lower():
                        pg, how = p, 'name search; article names the state and a political role (check it is the same person)'; break
                if pg: break
                time.sleep(0.3)
        if pg:
            found += 1
            wjson(c.path('wikipedia.json'), {'candidate': c.name, 'race': c.race, 'retrieved': NOW, 'title': pg['title'], 'url': pg.get('fullurl'),
                                            'matched_by': how, 'wikidata': (pg.get('pageprops') or {}).get('wikibase_item'),
                                            'image_file': pg.get('pageimage'), 'text': pg['extract'][:150000]})
        else:
            wjson(c.path('wikipedia.json'), {'candidate': c.name, 'race': c.race, 'retrieved': NOW, 'title': None,
                                            'note': 'No Wikipedia article found that clearly matches this candidate.'})
        time.sleep(0.3)
        if i % 50 == 0: log(f'  {i} of {len(todo)} ({found} found)')
    log('  done')

# ---------------------------------------------------------------- 3. photos
def run_photos(cands):
    log('\n[photos] Photos with their license')
    todo = [c for c in cands if not os.path.exists(c.path('photo.json'))]
    log(f'  {len(cands) - len(todo)} done, {len(todo)} to check')
    for i, c in enumerate(todo, 1):
        meta = None
        if c.bioguide:
            u = f'https://raw.githubusercontent.com/unitedstates/images/gh-pages/congress/450x550/{c.bioguide}.jpg'
            if fetch(u, dest=c.path('photo.jpg')):
                meta = {'source': u, 'license': 'Public domain (official congressional portrait)', 'credit': 'U.S. Congress'}
        if not meta:
            if not os.path.exists(c.path('wikipedia.json')): continue    # run the wiki step first; this one is retried later
            w = rjson(c.path('wikipedia.json'), {})
            if w.get('image_file'):
                d = get_json(WAPI + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'titles': 'File:' + w['image_file'],
                             'prop': 'imageinfo', 'iiprop': 'url|extmetadata', 'iiurlwidth': 400}))
                ii = (next(iter((d or {}).get('query', {}).get('pages', {}).values()), {}).get('imageinfo') or [{}])[0]
                em = ii.get('extmetadata') or {}
                lic = (em.get('LicenseShortName') or {}).get('value', '')
                if lic and ii.get('thumburl') and fetch(ii['thumburl'], dest=c.path('photo.jpg')):
                    meta = {'source': ii.get('descriptionurl'), 'license': lic, 'license_url': (em.get('LicenseUrl') or {}).get('value', ''),
                            'credit': re.sub('<[^>]+>', '', (em.get('Artist') or {}).get('value', '')).strip()}
        wjson(c.path('photo.json'), meta or {'note': 'No licensed photo found.'})
        if i % 100 == 0: log(f'  {i} of {len(todo)}')
    log('  done')

# ---------------------------------------------------------------- 4. Ballotpedia
def run_ballotpedia(cands):
    log('\n[ballotpedia] Ballotpedia pages')
    todo = [c for c in cands if not os.path.exists(c.path('ballotpedia.json'))]
    log(f'  {len(cands) - len(todo)} done, {len(todo)} to look up')
    blocked = 0
    for i, c in enumerate(todo, 1):
        got = None; statuses = []
        for t in (c.full, f'{c.full} ({c.statename()})', f'{c.first} {c.last}', f'{c.first} {c.last} ({c.statename()})'):
            url = 'https://ballotpedia.org/' + urllib.parse.quote(t.replace(' ', '_'))
            b = fetch(url, browser=True); statuses.append(LAST['status'])
            if b is None: continue
            s = b.decode('utf-8', 'replace')
            body = s[s.find('id="mw-content-text"'):] if 'id="mw-content-text"' in s else s
            body = body[:body.find('id="catlinks"')] if 'id="catlinks"' in body else body
            txt, links = page_text(body.encode())
            if c.statename() in txt and '2026' in txt and 'may refer to' not in txt[:2000]:
                web = {}
                for href, label in links:
                    l = label.strip().lower()
                    if href.startswith('http') and 'ballotpedia' not in href and re.search(r'campaign website|official website|personal website|campaign facebook|campaign x|campaign twitter|campaign instagram', l):
                        web.setdefault(l, href)
                got = {'candidate': c.name, 'race': c.race, 'retrieved': NOW, 'url': url, 'links': web, 'text': txt[:120000]}
                break
            time.sleep(1)
        if statuses and all(x in (403, 429, 'unreachable') for x in statuses):
            blocked += 1                      # refused, not missing: write nothing so the next run tries again
        else:
            blocked = 0
            wjson(c.path('ballotpedia.json'), got or {'candidate': c.name, 'race': c.race, 'retrieved': NOW, 'url': None, 'note': 'No matching Ballotpedia page found.'})
        if blocked >= 8:
            log('  Ballotpedia is not answering this script (it may be blocking automated visits). Skipping this step;'
                '\n  run it again later with --only ballotpedia,campaign; it continues where it stopped.'); return
        time.sleep(1.5)
        if i % 50 == 0: log(f'  {i} of {len(todo)}')
    log('  done')

# ---------------------------------------------------------------- 5. campaign websites
ISSUE = re.compile(r'issue|priorit|platform|polic|vision|agenda|plan|stand|position|values|about|meet', re.I)
def run_campaign(cands):
    log('\n[campaign] Campaign websites')
    todo = [c for c in cands if not os.path.exists(c.path('campaign_site.json'))]
    log(f'  {len(cands) - len(todo)} done, {len(todo)} to visit')
    for i, c in enumerate(todo, 1):
        if not os.path.exists(c.path('ballotpedia.json')): continue    # needs the ballotpedia step first; retried later
        bp = rjson(c.path('ballotpedia.json'), {}).get('links') or {}
        home = bp.get('campaign website') or next((v for k, v in bp.items() if 'campaign website' in k), None) or bp.get('official website')
        if not home:
            wjson(c.path('campaign_site.json'), {'candidate': c.name, 'note': 'No campaign website listed on Ballotpedia.'}); continue
        pages = []
        b = fetch(home, browser=True, timeout=30)
        if b:
            txt, links = page_text(b); pages.append({'url': home, 'text': txt[:40000]})
            host = urllib.parse.urlparse(home).netloc.replace('www.', '')
            seen = {home.rstrip('/')}
            for href, label in links:
                u = urllib.parse.urljoin(home, href).split('#')[0].rstrip('/')
                if u in seen or host not in urllib.parse.urlparse(u).netloc or not (ISSUE.search(label or '') or ISSUE.search(urllib.parse.urlparse(u).path)): continue
                if re.search(r'donat|contribut|volunteer|shop|store|privacy|login|cart|\.pdf$|\.jpg$', u, re.I): continue
                seen.add(u)
                b2 = fetch(u, browser=True, timeout=30)
                if b2: pages.append({'url': u, 'text': page_text(b2)[0][:40000]})
                if len(pages) >= 4: break
                time.sleep(0.5)
        wjson(c.path('campaign_site.json'), {'candidate': c.name, 'race': c.race, 'retrieved': NOW, 'home': home, 'pages': pages,
                                             'note': '' if pages else 'The website did not load.'})
        if i % 50 == 0: log(f'  {i} of {len(todo)}')
    log('  done')

# ---------------------------------------------------------------- 6. votes (Voteview)
VV = 'https://voteview.com/static/data/out/{kind}/{ch}{n}_{kind}.csv'
CAST = {1: 'Yea', 2: 'Yea (paired)', 3: 'Yea (announced)', 4: 'Nay (announced)', 5: 'Nay (paired)', 6: 'Nay', 7: 'Present', 8: 'Present', 9: 'Not voting', 0: 'Not a member'}
def run_votes(cands):
    log('\n[votes] Floor votes since 2007 (Voteview)')
    members = [c for c in cands if c.bioguide]
    todo = [c for c in members if not os.path.exists(c.path('votes_all.csv'))]
    log(f'  {len(members)} candidates served in Congress; {len(members) - len(todo)} done, {len(todo)} to do')
    if not todo: return
    want = {c.bioguide: c for c in todo}
    rows = {c.bioguide: [] for c in todo}
    os.makedirs(os.path.join(ROOT, '_rollcalls'), exist_ok=True)
    for n in CONGRESSES:
        for ch in ('H', 'S'):
            mp = fetch(VV.format(kind='members', ch=ch, n=n), dest=os.path.join(DL, f'{ch}{n}_members.csv'))
            rp = fetch(VV.format(kind='rollcalls', ch=ch, n=n), dest=os.path.join(DL, f'{ch}{n}_rollcalls.csv'))
            vp = fetch(VV.format(kind='votes', ch=ch, n=n), dest=os.path.join(DL, f'{ch}{n}_votes.csv'))
            if not (mp and rp and vp): log(f'  could not download Voteview files for {ch}{n}; skipping that Congress'); continue
            icp = {}
            for r in csv.DictReader(open(mp, encoding='utf-8')):
                if r.get('bioguide_id') in want: icp[r['icpsr']] = r['bioguide_id']
            if not icp: continue
            rc = {r['rollnumber']: r for r in csv.DictReader(open(rp, encoding='utf-8'))}
            for r in csv.DictReader(open(vp, encoding='utf-8')):
                b = icp.get(r['icpsr'])
                if not b: continue
                m = rc.get(r['rollnumber'], {})
                rows[b].append([n, 'House' if ch == 'H' else 'Senate', r['rollnumber'], m.get('date', ''), m.get('bill_number', ''),
                                m.get('vote_question', ''), (m.get('vote_desc') or m.get('dtl_desc') or '')[:300], m.get('vote_result', ''),
                                CAST.get(int(float(r['cast_code'] or 0)), r['cast_code'])])
            log(f'  {ch}{n}: done')
    head = ['congress', 'chamber', 'rollcall', 'date', 'bill', 'question', 'description', 'result', 'vote']
    for b, rr in rows.items():
        c = want[b]
        with open(c.path('votes_all.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(head); w.writerows(rr)
        with open(c.path('votes_major_subjects.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(head)
            w.writerows([r for r in rr if SUBJECTS.search(' '.join(str(x) for x in r[4:7]))])
    log('  done')

# ---------------------------------------------------------------- 7. bills and committees (congress.gov)
CG = 'https://api.congress.gov/v3/member/{b}/{kind}?format=json&limit=250&api_key={k}'
def run_bills(cands, key):
    log('\n[bills] Bills sponsored and co-sponsored (congress.gov), and committee seats')
    members = [c for c in cands if c.bioguide]
    # committees: no key needed
    cm = fetch(LEG.format(f='committee-membership-current.json'), dest=os.path.join(DL, 'committee-membership-current.json'))
    cn = fetch(LEG.format(f='committees-current.json'), dest=os.path.join(DL, 'committees-current.json'))
    if cm and cn:
        names = {}
        for x in json.load(open(cn, encoding='utf-8')):
            names[x['thomas_id']] = x['name']
            for s in x.get('subcommittees', []): names[x['thomas_id'] + s['thomas_id']] = x['name'] + ': ' + s['name']
        seats = {}
        for cid, mm in json.load(open(cm, encoding='utf-8')).items():
            for m in mm: seats.setdefault(m.get('bioguide'), []).append({'committee': names.get(cid, cid), 'title': m.get('title', ''), 'rank': m.get('rank')})
        for c in members:
            if c.bioguide in seats: wjson(c.path('committees.json'), {'retrieved': NOW, 'seats': seats[c.bioguide]})
    if not key:
        log('  bills skipped: no key. Run with FEC_API_KEY=yourkey (the same api.data.gov key works for congress.gov).'); return
    todo = [c for c in members if not os.path.exists(c.path('bills.json'))]
    log(f'  {len(members) - len(todo)} done, {len(todo)} to do')
    for i, c in enumerate(todo, 1):
        out = {'candidate': c.name, 'bioguide': c.bioguide, 'retrieved': NOW,
               'columns': ['congress', 'type', 'number', 'introduced', 'title', 'subject', 'latest_action_date', 'latest_action']}
        ok = True
        for kind, field in (('sponsored-legislation', 'sponsored'), ('cosponsored-legislation', 'cosponsored')):
            url, items = CG.format(b=c.bioguide, kind=kind, k=key), []
            while url:
                d = get_json(url)
                if d is None: ok = False; break
                for x in d.get(kind.replace('-l', 'L'), []) or []:
                    la = x.get('latestAction') or {}
                    items.append([x.get('congress'), x.get('type'), x.get('number'), x.get('introducedDate'), (x.get('title') or '')[:300],
                                  (x.get('policyArea') or {}).get('name', ''), la.get('actionDate', ''), (la.get('text') or '')[:200]])
                nxt = (d.get('pagination') or {}).get('next')
                url = (nxt + ('&' if '?' in nxt else '?') + 'api_key=' + key) if nxt and 'api_key=' not in nxt else nxt
                time.sleep(0.8)
            out[field] = items
        if not ok: log(f'  {c.name}: congress.gov did not answer; it will be retried next run'); continue
        wjson(c.path('bills.json'), out)
        if i % 25 == 0: log(f'  {i} of {len(todo)}')
    log('  done')

# ---------------------------------------------------------------- 8. ethics committees
ETHICS_INDEX = [('house_reports', 'https://ethics.house.gov/reports?page={p}'),
                ('house_press', 'https://ethics.house.gov/press-releases?page={p}'),
                ('senate_letters', 'https://www.ethics.senate.gov/public/index.cfm/publicletters')]
def run_ethics(cands):
    log('\n[ethics] House and Senate Ethics Committee documents')
    idx_path = os.path.join(DL, 'ethics_index.json')
    idx = rjson(idx_path)
    if not idx:
        idx = []
        for label, pat in ETHICS_INDEX:
            seen, before = set(), -1
            for p in range(0, 80 if '{p}' in pat else 1):
                b = fetch(pat.format(p=p), browser=True)
                if b is None: break
                base = pat.format(p=p)
                for href, text in page_text(b)[1]:
                    t = ' '.join(text.split())
                    if len(t) < 12: continue
                    u = urllib.parse.urljoin(base, href)
                    if u in seen: continue
                    seen.add(u); idx.append({'source': label, 'title': t, 'url': u})
                if len(seen) == before: break
                before = len(seen); time.sleep(1)
            log(f'  {label}: {len(seen)} documents listed')
        if not idx: log('  the ethics committee sites did not answer; try this step again later'); return
        wjson(idx_path, idx)
    n = 0
    for c in cands:
        hits = [d for d in idx if re.search(r'\b' + re.escape(c.last) + r'\b', d['title'], re.I)]
        strong = [d for d in hits if re.search(r'\b' + re.escape(c.first[:4]), d['title'], re.I) or re.search(r'\b(rep|sen|representative|senator)\.?\s+' + re.escape(c.last), d['title'], re.I)]
        wjson(c.path('ethics.json'), {'candidate': c.name, 'retrieved': NOW,
              'note': 'Ethics Committee documents whose titles name this candidate. Leads to check, not findings. "last_name_only" can be someone else with the same surname.',
              'matches': strong, 'last_name_only': [d for d in hits if d not in strong]})
        n += bool(strong)
    log(f'  {n} candidates are named in an ethics committee document title')

# ---------------------------------------------------------------- summary
def write_summary(cands):
    rows = []
    for c in cands:
        w = rjson(c.path('wikipedia.json'), {}); bp = rjson(c.path('ballotpedia.json'), {}); cs = rjson(c.path('campaign_site.json'), {})
        ph = rjson(c.path('photo.json'), {}); bl = rjson(c.path('bills.json'), {}); et = rjson(c.path('ethics.json'), {})
        nv = sum(1 for _ in open(c.path('votes_all.csv'), encoding='utf-8')) - 1 if os.path.exists(c.path('votes_all.csv')) else ''
        rows.append([c.race, c.name, c.id, c.bioguide or '', 'yes' if w.get('title') else ('no' if w else ''), 'yes' if bp.get('url') else ('no' if bp else ''),
                     len(cs.get('pages', [])) if cs else '', 'yes' if ph.get('license') else ('no' if ph else ''), nv,
                     len(bl.get('sponsored', [])) if bl else '', len(et.get('matches', [])) if et else ''])
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, 'summary.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['race', 'name', 'id', 'bioguide', 'wikipedia', 'ballotpedia', 'campaign_pages', 'photo', 'votes', 'bills_sponsored', 'ethics_mentions'])
        w.writerows(rows)
    wtext(os.path.join(ROOT, 'README.txt'), f'Research pack for the {len(cands)} candidates in ballot_2026.csv. Last run {NOW}.\n'
          'Name matches (Wikipedia by search, ethics documents) are leads to check, not findings.\n'
          'The _downloads folder holds shared source files and does not need to be uploaded.\n')

def main():
    a = sys.argv[1:]
    if not os.path.exists(BALLOT): log('ballot_2026.csv must be in the same folder as this script.'); return
    only = a[a.index('--only') + 1].split(',') if '--only' in a else STEPS
    bad = [s for s in only if s not in STEPS]
    if bad: log('Unknown step(s):', ', '.join(bad), '\nSteps:', ', '.join(STEPS)); return
    states = {a[i + 1].upper() for i, x in enumerate(a) if x == '--state'}
    key = os.environ.get('FEC_API_KEY') or os.environ.get('CONGRESS_API_KEY') or (a[a.index('--key') + 1] if '--key' in a else None)
    cands = [Cand(r) for r in csv.DictReader(open(BALLOT, encoding='utf-8')) if not states or r['state'] in states]
    log(f'OTS research pack: {len(cands)} ballot candidates, saving to {ROOT}')
    done = False
    try:
        if 'ids' in only or not any(os.path.exists(c.path('ids.json')) for c in cands): run_ids(cands)
        load_ids(cands)
        for s in only:
            if s == 'ids': continue
            {'wiki': run_wiki, 'photos': run_photos, 'ballotpedia': run_ballotpedia, 'campaign': run_campaign,
             'votes': run_votes, 'ethics': run_ethics}.get(s, lambda cc: run_bills(cc, key))(cands)
        done = True
    except NetworkDown:
        log('\nThe internet connection was down for over an hour, so the script stopped.'
            '\nEverything finished so far is saved. Run the same command again to continue where it left off.')
    except KeyboardInterrupt:
        log('\nStopped. Everything finished so far is saved. Run the same command again to continue.')
    write_summary(cands)
    if not done: sys.exit(2)
    log(f'\nFinished. Results are in {ROOT}'
        '\nTo send them: move the _downloads folder out of research-pack (it is big and not needed), right-click research-pack > Compress, then:'
        '\n  gh release create research-pack research-pack.zip -R Ronaldoh1/2026electiondata -t "Research pack"')

if __name__ == '__main__':
    main()
