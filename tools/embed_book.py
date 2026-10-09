"""The Israel Architecture library: book mode for the Israel simulation.
Each simulation chapter is a volume. Volumes with written text live in book/part1/<chapter>/*.html;
every other chapter appears on the shelf as "in preparation" and opens in the simulation.
Injects tools/book_block.html into index.html (idempotent).
Usage: python3 tools/embed_book.py [index.html]"""
import json, os, re, sys
IDX = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(IDX, encoding='utf-8').read()
CH = json.loads(re.search(r'window\.CHAPTERS = (\[.*?\]);\n', s, re.S).group(1))
SC = {x['id']: x for x in json.loads(re.search(r'<script id="scenedata" type="application/json">(.*?)</script>', s, re.S).group(1))}

def read(p):
    return open(p, encoding='utf-8').read().strip() if os.path.exists(p) else ''

def section(cid, sid):
    t = read(os.path.join(ROOT, 'book', 'part1', cid, sid + '.html'))
    if not t: return None
    m = re.match(r'\s*<h2>(.*?)</h2>\s*', t, re.S)
    return {'s': sid, 'h': re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else sid, 'html': t[m.end():] if m else t}

def span(ids):
    lo = hi = None; bce = None
    for sid in ids:
        y = str(SC.get(sid, {}).get('yr', ''))
        b = re.search(r'(\d+)\s*BCE', y, re.I)
        if b: bce = b.group(1)
        for v in re.findall(r'\b(1[0-9]\d\d|20\d\d)\b', y):
            v = int(v); lo = v if lo is None or v < lo else lo; hi = v if hi is None or v > hi else hi
    a = (bce + ' BCE') if bce else lo
    if a is None: return ''
    return '%s–%s' % (a, hi) if hi and str(hi) != str(a) else str(a)

def split_name(n):
    i = n.find(' — ')
    return (n[:i], n[i + 3:]) if i > 0 else (n, '')

# ---- Volume I: The Baseline (every scene before the Road to 1948), grouped into chapters ----
BASE = [
  ('Getting Your Bearings', "Before the history, the ground rules: how this book weighs evidence, where the places in the story are, who the Palestinians are in law today, and what the most argued-over words actually mean.", ['sk_s00', 'pr_s01', 'pr_s02', 'pr_s03']),
  ('The Land Before the State', "Three thousand years in brief, the Ottoman province that was named, counted and governed, and two peoples whose histories in this land are both real.", ['ah_s01', 's00h', 's00i']),
  ('Words and Names', "Where “Semitic” and “antisemitism” came from, how a word can be used to stop a question, and what the names and symbols at the center of this story actually say.", ['s00b', 's00b0', 's00b1', 's00f', 's00g', 's00d']),
  ('Peoples and Traditions', "The Jewish lineages, the difference between a religion and a political movement, the long record of dissent from within, the Christian argument over one verse, and centuries of coexistence.", ['s00b2', 's00c', 's00b3', 'gx_s05', 's00e']),
  ('Two Displacements', "Two great movements of people in the middle of the twentieth century, and why they were not one even exchange.", ['s00e2', 's00e3']),
  ('How the Story Is Told', "Who shapes what most people learn about this history: classrooms, coordinated campaigns, platform rules, and the historians themselves.", ['s00a', 's00a3', 's00a2', 'hd_s01']),
]
ch01 = next(c for c in CH if c['id'] == 'ch01')['scenes']
grouped = [x for g in BASE for x in g[2]]
missing = [x for x in ch01 if x not in grouped]
assert not missing, 'Baseline scenes not placed in a chapter: %s' % missing
base_chapters = []
for i, (title, intro, ids) in enumerate(BASE):
    secs = [x for x in (section('ch01', sid) for sid in ids) if x]
    base_chapters.append({'id': 'base%d' % (i + 1), 'label': 'Chapter %d' % (i + 1), 'title': title, 'span': '', 'intro': '<p>' + intro + '</p>', 'outro': '', 'sections': secs})
base_chapters[-1]['outro'] = read(os.path.join(ROOT, 'book', 'part1', 'ch01', '_outro.html'))
base_chapters[-1]['outroTitle'] = 'What the Baseline establishes'

# ---- Volume II: The Road to 1948, in stages ----
STAGES = [('rd0', 'Prelude', 'The Board Before the Game', '1694–1896'), ('rd1', 'Stage One', 'Conceive', '1896–1917'), ('rd2', 'Stage Two', 'Secure', '1917–1922'),
          ('rd3', 'Stage Three', 'Build', '1922–1936'), ('rd4', 'Stage Four', 'Pivot to America', '1936–1945'), ('rd5', 'Stage Five', 'Execute', '1945–1948'),
          ('rd6', 'Stage Six', 'Consolidate and Account', '1948–1950s')]
road = []
for cid, label, title, sp in STAGES:
    order = next(c for c in CH if c['id'] == cid)['scenes']
    road.append({'id': cid, 'label': label, 'title': title, 'span': sp, 'intro': read(os.path.join(ROOT, 'book', 'part1', cid, '_intro.html')),
                 'outro': read(os.path.join(ROOT, 'book', 'part1', cid, '_outro.html')), 'outroTitle': 'What this stage built',
                 'sections': [x for x in (section(cid, sid) for sid in order) if x]})

books = [
  {'id': 'baseline', 'vol': 1, 'status': 'ready', 'title': 'The Baseline', 'subtitle': 'The Ground Before the Flag', 'span': 'Antiquity to today', 'eraKey': -3000, 'unit': 'chapters',
   'intro': read(os.path.join(ROOT, 'book', 'part1', 'ch01', '_intro.html')), 'chapters': base_chapters, 'first': ch01[0]},
  {'id': 'road1948', 'vol': 2, 'status': 'ready', 'title': 'The Road to 1948', 'subtitle': 'The Stages That Built a State', 'span': '1694–1950s', 'unit': 'stages',
   'intro': '', 'chapters': road, 'first': 'bc_s01'},
]
done = {'ch01', 'rd0', 'rd1', 'rd2', 'rd3', 'rd4', 'rd5', 'rd6'}
vol = 3
for c in CH:
    if c['id'] in done or not c['scenes']: continue
    t, sub = split_name(c['name'])
    books.append({'id': c['id'], 'vol': vol, 'status': 'preparing', 'title': t, 'subtitle': sub, 'span': span(c['scenes']), 'count': len(c['scenes']), 'first': c['scenes'][0],
                  'keywords': ' '.join(SC[x]['t'] for x in c['scenes'] if x in SC)})
    vol += 1

lib = {'title': 'The Israel Architecture', 'tagline': 'A library of the documented record, in reading order. Every volume ties each claim to its source.',
       'note': 'The documented record, told in order, with every claim tied to its source. Tap a note number to see it, a name in a figure for its detail, or the + button for contents, bookmarks and notes.',
       'books': books}
payload = json.dumps(lib, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
block = open(os.path.join(ROOT, 'tools', 'book_block.html'), encoding='utf-8').read().strip().replace('__BOOK_JSON__', payload) + '\n'
s = re.sub(r'<!--BOOK-START-->.*?<!--BOOK-END-->\n?', '', s, flags=re.S)
i = s.find('<!--UX-START-->')
if i < 0: i = s.find('<!--ELEVEN-START-->')
if i < 0: i = s.rfind('</body>')
s = s[:i] + block + s[i:]
open(IDX, 'w', encoding='utf-8').write(s)
ready = [b for b in books if b['status'] == 'ready']
print('library embedded: %d volumes (%d ready: %s), %d KB' % (len(books), len(ready), ', '.join('%s %d ch/%d sec' % (b['title'], len(b['chapters']), sum(len(c['sections']) for c in b['chapters'])) for b in ready), len(payload) // 1024))
