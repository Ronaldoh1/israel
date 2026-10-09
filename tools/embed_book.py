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

def sections_for(cid, order):
    """A chapter's sections. If book/part1/<cid>/_manifest.json exists (the deep rebuild), it sets the order,
    each section's main scene and the other scenes it draws on; otherwise one section per scene in simulation order."""
    mp = os.path.join(ROOT, 'book', 'part1', cid, '_manifest.json')
    if not os.path.exists(mp):
        return [x for x in (section(cid, sid) for sid in order) if x]
    out = []
    for m in json.load(open(mp, encoding='utf-8'))['sections']:
        x = section(cid, m['s'])
        if not x: continue
        if m.get('scene') and m['scene'] != m['s']: x['scene'] = m['scene']
        if m.get('draws'): x['draws'] = [d for d in m['draws'] if d in SC]
        out.append(x)
    return out

# sources found by the library's own research: book/research/*.json -> {key: [url, label]}
CITES = {}
for fn in sorted(os.listdir(os.path.join(ROOT, 'book', 'research'))) if os.path.isdir(os.path.join(ROOT, 'book', 'research')) else []:
    if fn.endswith('.json'):
        for e in json.load(open(os.path.join(ROOT, 'book', 'research', fn), encoding='utf-8')).get('entries', []):
            for c in e.get('sources', []):
                CITES[c['key']] = [c['url'], c['label']]

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
_bm = os.path.join(ROOT, 'book', 'part1', 'ch01', '_manifest.json')
_bman = json.load(open(_bm, encoding='utf-8')) if os.path.exists(_bm) else None
DEEP_BASE = bool(_bman and 'chapters' in _bman and any(os.path.exists(os.path.join(ROOT, 'book', 'part1', 'ch01', x['s'] + '.html')) and x['s'].startswith('ch01_') for c in _bman['chapters'] for x in c['sections']))
if DEEP_BASE:  # the deep rebuild: chapters, order and drawn scenes come from the manifest
    for i, bc in enumerate(_bman['chapters']):
        secs = []
        for m in bc['sections']:
            x = section('ch01', m['s'])
            if not x: continue
            if m.get('scene') and m['scene'] != m['s']: x['scene'] = m['scene']
            if m.get('draws'): x['draws'] = [d for d in m['draws'] if d in SC]
            secs.append(x)
        intro = read(os.path.join(ROOT, 'book', 'part1', 'ch01', '_intro_%s.html' % bc['id'])) or '<p>' + bc.get('intro', '') + '</p>'
        base_chapters.append({'id': bc['id'], 'label': 'Chapter %d' % (i + 1), 'title': bc['title'], 'span': '', 'intro': intro, 'outro': '', 'sections': secs})
for i, (title, intro, ids) in enumerate([] if DEEP_BASE else BASE):
    secs = [x for x in (section('ch01', sid) for sid in ids) if x]
    base_chapters.append({'id': 'base%d' % (i + 1), 'label': 'Chapter %d' % (i + 1), 'title': title, 'span': '', 'intro': '<p>' + intro + '</p>', 'outro': '', 'sections': secs})
# ---- Baseline, last chapter: The Lines You've Heard (claims checked, with links to where the full record lives) ----
CH_OF = {sid: c['id'] for c in CH for sid in c['scenes']}
def roman(n):
    out = ''
    for v, r in ((50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
        while n >= v: out += r; n -= v
    return out
DRAWN = {}  # scenes from other chapters that a written volume now tells in full
for _cid in ['ch01'] + ['rd%d' % i for i in range(7)]:
    _mp = os.path.join(ROOT, 'book', 'part1', _cid, '_manifest.json')
    if os.path.exists(_mp):
        _mj = json.load(open(_mp, encoding='utf-8'))
        for _m in _mj.get('sections') or [x for c in _mj.get('chapters', []) for x in c['sections']]:
            for _d in _m.get('draws', []): DRAWN.setdefault(_d, _cid)
def volume_label(sid):
    cid = DRAWN.get(sid) if CH_OF.get(sid) not in ('ch01',) and not str(CH_OF.get(sid, '')).startswith('rd') and sid in DRAWN else CH_OF.get(sid)
    if cid == 'ch01': return 'Volume I, The Baseline', True
    if cid and cid.startswith('rd'): return 'Volume II, The Road to 1948', True
    n = 3
    for c in CH:
        if c['id'] in ('ch01',) or c['id'].startswith('rd') or not c['scenes']: continue
        if c['id'] == cid: return 'Volume %s, %s' % (roman(n), split_name(c['name'])[0]), False
        n += 1
    return 'the simulation', False
VCLS = {'False': 'f', 'Misleading': 'm', 'Half true': 'h', 'True, with limits': 't', "Depends on what's said": 'd', 'Unsupported': 'u', 'False, aimed the other way': 'o'}
plan_p = os.path.join(ROOT, 'book', 'lines', 'plan.json')
if os.path.exists(plan_p):
    plan = json.load(open(plan_p, encoding='utf-8'))
    secs = []
    for ti, th in enumerate(plan['themes']):
        h = '<p class="first">' + th.get('intro', '') + '</p>'
        for c in th['claims']:
            body = read(os.path.join(ROOT, 'book', 'lines', 'entries', c['id'] + '.html'))
            if not body: continue
            more = []; prep = False
            for sid in c['scenes'][:2]:
                if sid not in SC: continue
                vl, ready = volume_label(sid); prep = prep or not ready
                more.append('[scene:%s|%s: %s]' % (sid, vl, SC[sid]['t'].split(' — ')[0]))
            if prep: more[-1] += ' <span class="ln-prep">(%s in preparation; opens in the simulation for now)</span>' % ('volume' if all(not volume_label(x)[1] for x in c['scenes'][:2] if x in SC) else 'one volume')
            h += ('<div class="bk-line" id="ln-%s"><p class="ln-q">%s</p><span class="ln-v ln-%s">%s</span>%s<p class="ln-more"><span>Read more</span> %s</p></div>'
                  % (c['id'], c['claim'], VCLS.get(c['verdict'], 'd'), c['verdict'], body, ' · '.join(more)))
        secs.append({'s': 'lines_%d' % (ti + 1), 'h': th['title'], 'html': h})
    base_chapters.append({'id': 'base_lines', 'label': 'Chapter %d' % (len(base_chapters) + 1), 'title': "The Lines You've Heard", 'span': 'A field guide to the claims repeated most online',
        'intro': "<p>You now have the ground under the story. This chapter is a field guide to the lines you will meet in comment sections, posts and arguments. Each one is checked briefly against the record, with a verdict and a pointer to the volume that holds the full account. The same standard applies to every line, including the ones aimed at Jews.</p>",
        'outro': '', 'sections': secs})
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
                 'sections': sections_for(cid, order)})

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

lib = {'cites': CITES, 'title': 'The Israel Architecture', 'tagline': 'A library of the documented record, in reading order. Every volume ties each claim to its source.',
       'note': 'The documented record, told in order, with every claim tied to its source. Tap a note number to see it, a name in a figure for its detail, or the + button for contents, bookmarks and notes.',
       'books': books}
payload = json.dumps(lib, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
# the same payload, byte for byte, for the future site (export/library.json; '<\\/' is a valid JSON escape)
os.makedirs(os.path.join(ROOT, 'export'), exist_ok=True)
open(os.path.join(ROOT, 'export', 'library.json'), 'w', encoding='utf-8').write(payload)

def inline_asset(name):
    t = open(os.path.join(ROOT, 'tools', name), encoding='utf-8').read().strip()
    assert '</script' not in t.lower() and '</style' not in t.lower(), name + ' must not close its own tag'
    return t
block = open(os.path.join(ROOT, 'tools', 'book_block.html'), encoding='utf-8').read().strip()
for ph, name in (('/*__CHARTS_CSS__*/', 'charts.css'), ('/*__CHARTS_JS__*/', 'charts.js')):
    assert block.count(ph) == 1, 'placeholder %s missing from book_block.html' % ph
    block = block.replace(ph, inline_asset(name))
block = block.replace('__BOOK_JSON__', payload) + '\n'
s = re.sub(r'<!--BOOK-START-->.*?<!--BOOK-END-->\n?', '', s, flags=re.S)
i = s.find('<!--UX-START-->')
if i < 0: i = s.find('<!--ELEVEN-START-->')
if i < 0: i = s.rfind('</body>')
s = s[:i] + block + s[i:]
open(IDX, 'w', encoding='utf-8').write(s)
ready = [b for b in books if b['status'] == 'ready']
print('library embedded: %d volumes (%d ready: %s), %d KB' % (len(books), len(ready), ', '.join('%s %d ch/%d sec' % (b['title'], len(b['chapters']), sum(len(c['sections']) for c in b['chapters'])) for b in ready), len(payload) // 1024))
