#!/usr/bin/env python3
"""Talking-Point Radar: collects public posts about Israel/Zionism from several platforms, finds which recurring
pro-Israel / Zionist talking points are being repeated, and checks each one against what the Israel module already answers.

  python3 radar.py collect youtube|reddit|bluesky|telegram|gdelt|inbox
  python3 radar.py analyze          -> output/report.html, output/gaps.md, output/report.json

Python 3 standard library only. Keys come from environment variables (run.sh sets them from keys.txt):
  YOUTUBE_API_KEY   REDDIT_CLIENT_ID  REDDIT_CLIENT_SECRET   BSKY_HANDLE  BSKY_APP_PASSWORD
Collected posts go to data/posts/<platform>.jsonl. Running again adds only new posts.
Privacy: only accounts listed as "official" in config/sources.json keep their names. Every other author is stored as a
one-way code (so the report can say "repeated by 40 different accounts" without saying who)."""
import json, os, re, sys, time, hashlib, html, base64, urllib.request, urllib.parse, urllib.error, collections, datetime, glob, secrets
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'config', 'sources.json'), encoding='utf-8'))
DATA = os.path.join(HERE, 'data'); POSTS = os.path.join(DATA, 'posts'); OUT = os.path.join(HERE, 'output')
for d in (POSTS, OUT, os.path.join(DATA, 'inbox'), os.path.join(DATA, 'state')): os.makedirs(d, exist_ok=True)
UA = 'TalkingPointRadar/1.0 (research; contact via github.com/Ronaldoh1)'

class RateLimited(Exception): pass
class Fatal(Exception): pass

def log(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

def salt():
    p = os.path.join(DATA, 'state', 'salt')
    if not os.path.exists(p): open(p, 'w').write(secrets.token_hex(16))
    return open(p).read().strip()
SALT = salt()
OFFICIAL = set(x['name'].lower() for x in CFG['youtube']['official']) | set(x['handle'].lower().lstrip('@') for x in CFG['youtube']['official']) | set(c.lower() for c in CFG['telegram']['official'])
def who(name, official=False):
    if official or (name or '').lower().lstrip('@') in OFFICIAL: return {'author': name, 'official': True}
    return {'author_code': hashlib.sha256((SALT + (name or '?').lower()).encode()).hexdigest()[:12]}

def get(url, headers=None, data=None, tries=6, method=None):
    """HTTP with retries: waits out rate limits and network drops (30s, 1, 2, 4, 8 min)."""
    h = {'User-Agent': UA}; h.update(headers or {})
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=h, method=method)
            with urllib.request.urlopen(req, timeout=60) as r: return r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'replace')[:600]
            if e.code == 429 or (e.code == 403 and 'rateLimit' in body):
                wait = int(e.headers.get('Retry-After') or 0) or 60 * (2 ** i); log('rate limited, waiting', wait, 's'); time.sleep(min(wait, 900)); continue
            if e.code == 403 and 'quotaExceeded' in body: raise RateLimited('YouTube daily quota used up (it resets at midnight Pacific). Run again tomorrow; nothing is lost.')
            if e.code in (500, 502, 503, 504): time.sleep(30 * (2 ** i)); continue
            raise Fatal('HTTP %s for %s: %s' % (e.code, url.split('?')[0], body[:200]))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            log('network problem (%s), retrying' % e); time.sleep(30 * (2 ** i))
    raise Fatal('gave up after %d tries: %s' % (tries, url.split('?')[0]))
def getj(url, **k): return json.loads(get(url, **k))

class Store:
    """Append-only jsonl per platform, de-duplicated by post id."""
    def __init__(self, platform):
        self.p = os.path.join(POSTS, platform + '.jsonl'); self.seen = set(); self.new = 0
        if os.path.exists(self.p):
            for line in open(self.p, encoding='utf-8'):
                try: self.seen.add(json.loads(line)['id'])
                except Exception: pass
        self.f = open(self.p, 'a', encoding='utf-8')
    def add(self, post):
        if not post.get('text') or post['id'] in self.seen: return False
        self.seen.add(post['id']); self.f.write(json.dumps(post, ensure_ascii=False) + '\n'); self.f.flush(); self.new += 1; return True
    def close(self): self.f.close(); return self.new

def since_iso(): return (datetime.datetime.utcnow() - datetime.timedelta(days=CFG.get('since_days', 365))).strftime('%Y-%m-%dT%H:%M:%SZ')

# ---------------------------------------------------------------- YouTube (Data API v3, free key, 10,000 units/day)
def collect_youtube():
    key = os.environ.get('YOUTUBE_API_KEY') or raise_(Fatal('no YOUTUBE_API_KEY'))
    Y = CFG['youtube']; st = Store('youtube'); api = 'https://www.googleapis.com/youtube/v3/'
    q = lambda path, **p: getj(api + path + '?' + urllib.parse.urlencode(dict(p, key=key)))
    cache_p = os.path.join(DATA, 'state', 'youtube_channels.json'); cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    videos = []   # (videoId, official name or None)
    for ch in Y['official']:
        cid = cache.get(ch['name'])
        if not cid:
            r = q('channels', part='id,snippet', forHandle=ch['handle'])
            if not r.get('items'):
                r2 = q('search', part='snippet', type='channel', q=ch['name'], maxResults=1)
                cid = r2['items'][0]['snippet']['channelId'] if r2.get('items') else None
                if cid: log('YouTube: handle %s not found; using search result "%s" for %s. CHECK it is the official channel.' % (ch['handle'], r2['items'][0]['snippet']['title'], ch['name']))
            else: cid = r['items'][0]['id']
            if not cid: log('YouTube: could not find', ch['name']); continue
            cache[ch['name']] = cid; json.dump(cache, open(cache_p, 'w'), indent=1)
        up = 'UU' + cid[2:]; tok = None; n = 0; old = False
        while n < Y['videos_per_channel'] and not old:
            r = q('playlistItems', part='snippet', playlistId=up, maxResults=50, **({'pageToken': tok} if tok else {}))
            for it in r.get('items', []):
                sn = it['snippet']; vid = sn['resourceId']['videoId']
                if sn.get('publishedAt', '') < since_iso() or n >= Y['videos_per_channel']: old = True; break
                st.add({'id': 'yt:v:' + vid, 'platform': 'youtube', 'kind': 'video', 'url': 'https://www.youtube.com/watch?v=' + vid, 'date': sn['publishedAt'][:10],
                        'text': sn['title'] + '\n' + sn.get('description', '')[:1500], 'via': ch['name'], **who(ch['name'], True)})
                videos.append((vid, ch['name'])); n += 1
            tok = r.get('nextPageToken')
            if not tok: break
        log('YouTube: %s -> %d videos' % (ch['name'], n))
    done_p = os.path.join(DATA, 'state', 'youtube_searched.json'); done = set(json.load(open(done_p))) if os.path.exists(done_p) else set()
    for term in CFG['searches']:
        if term in done: continue
        r = q('search', part='snippet', type='video', q=term, maxResults=Y['search_videos_per_query'], order='relevance', publishedAfter=since_iso(), relevanceLanguage='en')
        for it in r.get('items', []):
            sn = it['snippet']; vid = it['id']['videoId']
            st.add({'id': 'yt:v:' + vid, 'platform': 'youtube', 'kind': 'video', 'url': 'https://www.youtube.com/watch?v=' + vid, 'date': sn['publishedAt'][:10],
                    'text': sn['title'] + '\n' + sn.get('description', ''), 'via': 'search: ' + term, **who(sn['channelTitle'])})
            videos.append((vid, None))
        done.add(term); json.dump(sorted(done), open(done_p, 'w'))
    cdone_p = os.path.join(DATA, 'state', 'youtube_comments_done.json'); cdone = set(json.load(open(cdone_p))) if os.path.exists(cdone_p) else set()
    for vid, src in videos:
        if vid in cdone: continue
        try: r = q('commentThreads', part='snippet', videoId=vid, maxResults=min(100, Y['comments_per_video']), order='relevance', textFormat='plainText')
        except Fatal as e:
            if 'commentsDisabled' in str(e) or '404' in str(e) or '403' in str(e): cdone.add(vid); continue
            raise
        for it in r.get('items', []):
            c = it['snippet']['topLevelComment']['snippet']
            st.add({'id': 'yt:c:' + it['id'], 'platform': 'youtube', 'kind': 'comment', 'url': 'https://www.youtube.com/watch?v=%s&lc=%s' % (vid, it['id']), 'date': c['publishedAt'][:10],
                    'text': c.get('textDisplay', ''), 'likes': c.get('likeCount', 0), 'via': 'comments on ' + (src or 'search result'), **who(c.get('authorDisplayName'))})
        cdone.add(vid); json.dump(sorted(cdone), open(cdone_p, 'w'))
    return st.close()

def raise_(e): raise e

# ---------------------------------------------------------------- Reddit (official API, app-only sign-in)
def collect_reddit():
    cid, sec = os.environ.get('REDDIT_CLIENT_ID'), os.environ.get('REDDIT_CLIENT_SECRET')
    if not (cid and sec): raise Fatal('no REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET')
    tok = json.loads(get('https://www.reddit.com/api/v1/access_token', data=b'grant_type=client_credentials',
                         headers={'Authorization': 'Basic ' + base64.b64encode(('%s:%s' % (cid, sec)).encode()).decode()}, method='POST'))['access_token']
    H = {'Authorization': 'bearer ' + tok}; st = Store('reddit'); R = CFG['reddit']
    def rq(path, **p): time.sleep(1.1); return getj('https://oauth.reddit.com' + path + '?' + urllib.parse.urlencode(dict(p, raw_json=1)), headers=H)
    def add_post(d, via):
        st.add({'id': 'rd:' + d['name'], 'platform': 'reddit', 'kind': 'post', 'url': 'https://www.reddit.com' + d['permalink'], 'date': time.strftime('%Y-%m-%d', time.gmtime(d['created_utc'])),
                'text': (d.get('title', '') + '\n' + d.get('selftext', '')).strip(), 'likes': d.get('score', 0), 'via': via, 'sub': d.get('subreddit'), **who(d.get('author'))})
    threads = []
    for sub in R['subreddits']:
        for term in CFG['searches']:
            r = rq('/r/%s/search' % sub, q=term, restrict_sr=1, sort='relevance', t='year', limit=min(100, R['posts_per_search']))
            for c in r['data']['children']: add_post(c['data'], 'r/%s search: %s' % (sub, term)); threads.append((c['data'].get('num_comments', 0), c['data']['permalink']))
        log('Reddit: r/%s searched' % sub)
    threads.sort(reverse=True); done_p = os.path.join(DATA, 'state', 'reddit_threads_done.json'); done = set(json.load(open(done_p))) if os.path.exists(done_p) else set()
    for _, link in [t for t in dict((t[1], t) for t in threads).values()][:R['comments_from_top_threads'] * len(R['subreddits'])]:
        if link in done: continue
        r = rq(link.rstrip('/') + '.json', limit=200, depth=4, sort='top')
        def walk(ch):
            for c in ch:
                if c.get('kind') != 't1': continue
                d = c['data']
                st.add({'id': 'rd:' + d['name'], 'platform': 'reddit', 'kind': 'comment', 'url': 'https://www.reddit.com' + d.get('permalink', link), 'date': time.strftime('%Y-%m-%d', time.gmtime(d['created_utc'])),
                        'text': d.get('body', ''), 'likes': d.get('score', 0), 'via': 'thread', 'sub': d.get('subreddit'), **who(d.get('author'))})
                if isinstance(d.get('replies'), dict): walk(d['replies']['data']['children'])
        if isinstance(r, list) and len(r) > 1: walk(r[1]['data']['children'])
        done.add(link); json.dump(sorted(done), open(done_p, 'w'))
    return st.close()

# ---------------------------------------------------------------- Bluesky (open network; app password recommended)
def collect_bluesky():
    h, pw = os.environ.get('BSKY_HANDLE'), os.environ.get('BSKY_APP_PASSWORD'); H = {}; base = 'https://public.api.bsky.app'
    if h and pw:
        s = json.loads(get('https://bsky.social/xrpc/com.atproto.server.createSession', data=json.dumps({'identifier': h, 'password': pw}).encode(), headers={'Content-Type': 'application/json'}, method='POST'))
        H = {'Authorization': 'Bearer ' + s['accessJwt']}; base = 'https://bsky.social'
    st = Store('bluesky')
    for term in CFG['searches']:
        cur, n = None, 0
        while n < CFG['bluesky']['per_search']:
            p = {'q': term, 'limit': 100, 'since': since_iso()}
            if cur: p['cursor'] = cur
            try: r = getj(base + '/xrpc/app.bsky.feed.searchPosts?' + urllib.parse.urlencode(p), headers=H)
            except Fatal as e:
                if '403' in str(e) or '401' in str(e): raise Fatal('Bluesky search needs signing in: add BSKY_HANDLE and an app password (Settings > Privacy and security > App passwords).')
                raise
            for x in r.get('posts', []):
                a = x['author']['handle']; rkey = x['uri'].split('/')[-1]
                st.add({'id': 'bs:' + x['uri'], 'platform': 'bluesky', 'kind': 'post', 'url': 'https://bsky.app/profile/%s/post/%s' % (x['author']['did'], rkey), 'date': x['record'].get('createdAt', '')[:10],
                        'text': x['record'].get('text', ''), 'likes': x.get('likeCount', 0), 'via': 'search: ' + term, **who(a)}); n += 1
            cur = r.get('cursor'); time.sleep(0.5)
            if not cur or not r.get('posts'): break
        log('Bluesky: %s -> %d' % (term, n))
    return st.close()

# ---------------------------------------------------------------- Telegram (public channel web pages, no sign-in)
def collect_telegram():
    st = Store('telegram')
    for ch in CFG['telegram']['official']:
        before, n = None, 0
        while n < CFG['telegram']['messages_per_channel']:
            try: page = get('https://t.me/s/%s' % ch + ('?before=%s' % before if before else ''))
            except Fatal as e: log('Telegram: %s not reachable (%s)' % (ch, e)); break
            msgs = []
            for blk in page.split('tgme_widget_message_wrap')[1:]:
                pm, tm = re.search(r'data-post="([^"]+)"', blk), re.search(r'<time[^>]*datetime="([^"]+)"', blk)
                bm = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', blk, re.S)
                if pm: msgs.append((pm.group(1), bm.group(1) if bm else '', tm.group(1) if tm else ''))
            if not msgs:
                if not n: log('Telegram: %s has no public preview (check the name)' % ch)
                break
            for post, body, dt in msgs:
                txt = html.unescape(re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>', '\n', body or ''))).strip()
                st.add({'id': 'tg:' + post, 'platform': 'telegram', 'kind': 'post', 'url': 'https://t.me/' + post, 'date': dt[:10], 'text': txt, 'via': ch, **who(ch, True)}); n += 1
            ids = [int(p.split('/')[-1]) for p, _, _ in msgs if p.split('/')[-1].isdigit()]
            if not ids or min(ids) <= 1 or (msgs[0][2] and msgs[0][2][:10] < since_iso()[:10]): break
            before = min(ids); time.sleep(2)
        log('Telegram: %s -> %d' % (ch, n))
    return st.close()

# ---------------------------------------------------------------- GDELT (worldwide news headlines, free, no key)
def collect_gdelt():
    st = Store('news')
    for term in CFG['searches']:
        qs = '"%s"' % term if ' ' in term else term
        url = 'https://api.gdeltproject.org/api/v2/doc/doc?' + urllib.parse.urlencode({'query': qs + ' sourcelang:english', 'mode': 'artlist', 'maxrecords': CFG['gdelt']['per_search'], 'format': 'json', 'timespan': CFG['gdelt']['timespan']})
        try: r = json.loads(get(url) or '{}')
        except ValueError: r = {}
        for a in r.get('articles', []):
            st.add({'id': 'nw:' + a['url'], 'platform': 'news', 'kind': 'headline', 'url': a['url'], 'date': (lambda d: d[:4] + '-' + d[4:6] + '-' + d[6:8] if len(d) >= 8 else '')(a.get('seendate', '')), 'text': a.get('title', ''), 'via': a.get('domain'), 'author': a.get('domain'), 'official': False})
        time.sleep(6)
    return st.close()

# ---------------------------------------------------------------- Inbox: anything you paste (TikTok, Instagram, X comments, DMs...)
def collect_inbox():
    st = Store('inbox')
    for f in sorted(glob.glob(os.path.join(DATA, 'inbox', '*.txt'))):
        raw = open(f, encoding='utf-8', errors='replace').read(); src = os.path.basename(f)[:-4]
        for i, chunk in enumerate(re.split(r'\n-{3,}\s*\n', raw)):
            chunk = chunk.strip()
            if not chunk: continue
            m = re.match(r'(https?://\S+)\s*\n', chunk); url = m.group(1) if m else ''
            text = chunk[m.end():] if m else chunk
            st.add({'id': 'in:' + hashlib.sha1(text.encode()).hexdigest()[:16], 'platform': 'inbox', 'kind': 'pasted', 'url': url, 'date': time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(f))),
                    'text': text, 'via': src, **who(src + ':' + str(i))})
    return st.close()

# ---------------------------------------------------------------- Analysis
TOPIC = re.compile(r'israel|zionis|palestin|gaza|west bank|judea|hamas|idf|jerusalem|jewish state|jews|antisemit|hasbara|aipac|nakba|1948', re.I)
STOP = set('the a an and or of to in on for is are was were be been it its this that these those with as at by from but not no so if then than they them their there here we you i he she his her our your my me us do does did have has had will would can could should just about into over more most some any all what which who whom why how when where also only very much many like get got one two'.split())
def norm_words(t): return re.findall(r"[a-z0-9']+", t.lower())
def analyze():
    TP = json.load(open(os.path.join(HERE, 'config', 'talking_points.json'), encoding='utf-8'))
    COV = json.load(open(os.path.join(HERE, 'config', 'coverage.json'), encoding='utf-8'))['points']
    pts = [(p, [re.compile(x, re.I) for x in p['say']]) for p in TP['points']]
    rebut = re.compile(r'\b(?:%s)\b' % '|'.join(re.escape(x) for x in TP['rebut_markers']), re.I)
    posts = []
    for f in glob.glob(os.path.join(POSTS, '*.jsonl')):
        for line in open(f, encoding='utf-8'):
            try: posts.append(json.loads(line))
            except Exception: pass
    agg = {p['id']: {'repeat': 0, 'rebut': 0, 'authors': set(), 'official': collections.Counter(), 'platforms': collections.Counter(), 'months': collections.Counter(), 'examples': []} for p, _ in pts}
    unmatched = []
    for x in posts:
        t = x['text']; hit = False
        for p, rs in pts:
            m = next((r.search(t) for r in rs if r.search(t)), None)
            if not m: continue
            hit = True; a = agg[p['id']]; is_reb = bool(rebut.search(t))
            a['rebut' if is_reb else 'repeat'] += 1; a['authors'].add(x.get('author') or x.get('author_code')); a['platforms'][x['platform']] += 1; a['months'][x.get('date', '')[:7]] += 1
            if x.get('official'): a['official'][x.get('author')] += 1
            if not is_reb:
                s = max(0, m.start() - 160); a['examples'].append({'score': (x.get('likes') or 0) + (500 if x.get('official') else 0), 'url': x.get('url'), 'platform': x['platform'], 'date': x.get('date'),
                                   'who': x.get('author') if x.get('official') else None, 'snip': ('…' if s else '') + t[s:m.end() + 220].replace('\n', ' ') + ('…' if m.end() + 220 < len(t) else '')})
        if not hit and TOPIC.search(t) and x['platform'] != 'news': unmatched.append(x)
    # Emerging phrases: 3-5 word runs repeated by many different accounts among on-topic posts that matched no known point.
    grams = collections.defaultdict(set); gex = {}
    for x in unmatched:
        w = norm_words(x['text']); who_ = x.get('author') or x.get('author_code')
        for n in (3, 4, 5):
            for i in range(len(w) - n + 1):
                g = w[i:i + n]
                if g[0] in STOP or g[-1] in STOP or sum(1 for z in g if z not in STOP) < 2: continue
                k = ' '.join(g); grams[k].add(who_); gex.setdefault(k, x)
    emerging = sorted(((len(v), k) for k, v in grams.items() if len(v) >= 3), reverse=True)
    kept = []
    for n, k in emerging:
        ws = set(k.split())
        if any(len(ws & set(kk.split())) >= 2 for _, kk, _ in kept): continue
        ex = gex[k]; kept.append((n, k, {'url': ex.get('url'), 'platform': ex['platform'], 'snip': ex['text'][:300].replace('\n', ' ')}))
        if len(kept) >= 60: break
    rows = []
    for p, _ in pts:
        a = agg[p['id']]; c = COV.get(p['id'], {'level': 'missing', 'top': []})
        a['examples'].sort(key=lambda e: -e['score'])
        rows.append({'id': p['id'], 'group': p['group'], 'label': p['label'], 'repeat': a['repeat'], 'rebut': a['rebut'], 'accounts': len(a['authors']),
                     'official': dict(a['official'].most_common(6)), 'platforms': dict(a['platforms']), 'months': dict(sorted(a['months'].items())),
                     'coverage': c['level'], 'where': [{'id': h['id'], 'title': h['title'], 'kind': h['kind']} for h in c['top'][:4]], 'examples': a['examples'][:6]})
    rank = {'missing': 0, 'touched': 1, 'answered': 2}
    rows.sort(key=lambda r: (-r['accounts'], rank[r['coverage']]))
    summary = {'built': time.strftime('%Y-%m-%d %H:%M'), 'posts': len(posts), 'by_platform': dict(collections.Counter(x['platform'] for x in posts)), 'unmatched_on_topic': len(unmatched)}
    json.dump({'summary': summary, 'points': rows, 'emerging': [{'accounts': n, 'phrase': k, 'example': e} for n, k, e in kept]}, open(os.path.join(OUT, 'report.json'), 'w'), indent=1, ensure_ascii=False)
    write_gaps(summary, rows, kept); write_html(summary, rows, kept)
    log('Report written: output/report.html, output/gaps.md (%d posts, %d on-topic posts matched no known talking point)' % (len(posts), len(unmatched)))

def write_gaps(S, rows, kept):
    L = ['# Talking points the module does not fully answer yet', '', 'Built %s from %d posts (%s).' % (S['built'], S['posts'], ', '.join('%s %d' % kv for kv in S['by_platform'].items())), '',
         '"Accounts" = how many different accounts repeated it (rebuttals not counted). Coverage is a keyword check of the module, so read the places it lists before deciding.', '']
    for lev, title in (('missing', 'Not in the module at all'), ('touched', 'Mentioned in passing, not answered')):
        L += ['## ' + title, '']
        quiet = [r['label'] for r in rows if r['coverage'] == lev and not r['accounts']]
        for r in [r for r in rows if r['coverage'] == lev and r['accounts']]:
            L.append('- **%s** — %d accounts, %d posts%s' % (r['label'], r['accounts'], r['repeat'], ('; official: ' + ', '.join(r['official'])) if r['official'] else ''))
            for e in r['examples'][:3]: L.append('  - %s %s: "%s"' % (e['platform'], e['url'] or '', e['snip'][:240]))
        if quiet: L.append('- Not seen in the collected posts yet: ' + '; '.join(quiet))
        L.append('')
    L += ['## Answered, ranked by how often it is repeated', '']
    for r in [r for r in rows if r['coverage'] == 'answered'][:25]:
        L.append('- %s — %d accounts · module: %s' % (r['label'], r['accounts'], ', '.join(w['id'] for w in r['where'][:3])))
    L += ['', '## New phrases (repeated by 3+ accounts, not matching any known talking point)', '', 'Read these: the ones that are real arguments become new entries in config/talking_points.json.', '']
    for n, k, e in kept: L.append('- "%s" — %d accounts · e.g. %s' % (k, n, e['url'] or e['platform']))
    open(os.path.join(OUT, 'gaps.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

def write_html(S, rows, kept):
    E = lambda s: html.escape(str(s if s is not None else ''))
    col = {'missing': '#B3261E', 'touched': '#A15C00', 'answered': '#1B6B3A'}; lab = {'missing': 'Not in module', 'touched': 'Mentioned only', 'answered': 'Answered'}
    mx = max([r['accounts'] for r in rows] + [1])
    body = []
    for r in rows:
        if not (r['accounts'] or r['rebut']): continue
        ex = ''.join('<li><span class="pf">%s%s</span> %s <a href="%s" target="_blank" rel="noopener">open</a></li>' % (E(e['platform']), (' · ' + E(e['who'])) if e['who'] else '', E(e['snip']), E(e['url'])) for e in r['examples'][:4])
        wh = ', '.join(E(w['id']) + ' <span class="t">' + E(w['title'][:50]) + '</span>' for w in r['where'][:3]) or 'nowhere yet'
        off = ('<p class="off">Official accounts pushing it: ' + ', '.join('%s (%d)' % (E(k), v) for k, v in r['official'].items()) + '</p>') if r['official'] else ''
        body.append('<details class="tp"><summary><span class="bar"><i style="width:%.0f%%"></i></span><span class="lb">%s</span><span class="n">%d accounts</span><span class="cv" style="background:%s">%s</span></summary>'
                    '<div class="in"><p class="meta">%d posts repeat it · %d rebut it · %s</p>%s<p class="wh">In the module: %s</p><ul>%s</ul></div></details>'
                    % (100.0 * r['accounts'] / mx, E(r['label']), r['accounts'], col[r['coverage']], lab[r['coverage']], r['repeat'], r['rebut'], ' · '.join('%s %d' % (E(k), v) for k, v in r['platforms'].items()), off, wh, ex))
    em = ''.join('<li><b>"%s"</b> <span class="n">%d accounts</span> <a href="%s" target="_blank" rel="noopener">example</a><br><small>%s</small></li>' % (E(k), n, E(e['url']), E(e['snip'][:200])) for n, k, e in kept)
    gaps = sum(1 for r in rows if r['coverage'] != 'answered' and r['accounts'])
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Talking-Point Radar</title><style>
:root{--bg:#F6F4EF;--ink:#1B2A4A;--card:#fff;--line:#DCD6C8;--acc:#C9912B}@media(prefers-color-scheme:dark){:root{--bg:#10151F;--ink:#E9E4D8;--card:#18202E;--line:#2C3648}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Georgia,serif}main{max-width:860px;margin:auto;padding:24px 16px 80px}h1{font:800 30px/1.1 system-ui,sans-serif;margin:0 0 6px}
.sum{font:14px system-ui,sans-serif;margin:0 0 22px}h2{font:700 19px system-ui,sans-serif;margin:30px 0 10px}.tp{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:0 0 8px}
summary{display:grid;grid-template-columns:70px 1fr auto auto;gap:10px;align-items:center;padding:10px 12px;cursor:pointer;font:14px system-ui,sans-serif}.bar{height:8px;background:var(--line);border-radius:4px;overflow:hidden}.bar i{display:block;height:100%;background:var(--acc)}
.lb{font-weight:600}.n{white-space:nowrap;font-size:13px}.cv{color:#fff;border-radius:4px;padding:2px 7px;font-size:12px;white-space:nowrap}.in{padding:0 14px 12px;font-size:14px}.meta,.wh,.off{font:13px system-ui,sans-serif;margin:6px 0}.t{opacity:.85}
ul{padding-left:18px}li{margin:6px 0}.pf{font:600 12px system-ui,sans-serif;color:var(--acc)}a{color:inherit}@media(max-width:560px){summary{grid-template-columns:1fr auto}.bar,.n{display:none}}
</style></head><body><main><h1>Talking-Point Radar</h1><p class="sum">@@BUILT@@ · @@POSTS@@ posts collected (@@PLAT@@). @@GAPS@@ recurring talking points found in the posts are not yet fully answered by the module. Tap a row to see examples and where the module answers it.</p>
<h2>Recurring talking points, most-repeated first</h2>@@BODY@@<h2>New phrases to review</h2><p class="sum">Repeated by three or more different accounts in on-topic posts that matched none of the known talking points. Real arguments here should be added to the list.</p><ul>@@EM@@</ul></main></body></html>'''
    for k, v in zip(['@@BUILT@@', '@@POSTS@@', '@@PLAT@@', '@@GAPS@@', '@@BODY@@', '@@EM@@'], [E(S['built']), S['posts'], ', '.join('%s %d' % (E(k), v) for k, v in S['by_platform'].items()), gaps, ''.join(body), em]): page = page.replace(k, str(v))
    open(os.path.join(OUT, 'report.html'), 'w', encoding='utf-8').write(page)

if __name__ == '__main__':
    cmd = sys.argv[1:] or ['help']
    try:
        if cmd[0] == 'collect':
            n = {'youtube': collect_youtube, 'reddit': collect_reddit, 'bluesky': collect_bluesky, 'telegram': collect_telegram, 'gdelt': collect_gdelt, 'inbox': collect_inbox}[cmd[1]]()
            log('%s: %d new posts' % (cmd[1], n))
        elif cmd[0] == 'analyze': analyze()
        else: print(__doc__)
    except RateLimited as e: log(str(e)); sys.exit(3)
    except Fatal as e: log('STOPPED:', e); sys.exit(2)
