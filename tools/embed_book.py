"""Book mode for the Israel simulation. Assembles book/part1/<chapter>/*.html into one JSON payload and
injects tools/book_block.html into index.html. Idempotent: replaces its own block.
Usage: python3 tools/embed_book.py [index.html]"""
import json, os, re, sys
IDX = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(IDX, encoding='utf-8').read()
CH = json.loads(re.search(r'window\.CHAPTERS = (\[.*?\]);\n', s, re.S).group(1))

META = [  # chapter id, label, title, span
  ('ch01', 'Prologue', 'The Ground Before the Flag', 'The words, the land and the people, before the story begins'),
  ('rd0', 'Prelude', 'The Board Before the Game', '1694–1896'),
  ('rd1', 'Stage One', 'Conceive', '1896–1917'),
  ('rd2', 'Stage Two', 'Secure', '1917–1922'),
  ('rd3', 'Stage Three', 'Build', '1922–1936'),
  ('rd4', 'Stage Four', 'Pivot to America', '1936–1945'),
  ('rd5', 'Stage Five', 'Execute', '1945–1948'),
  ('rd6', 'Stage Six', 'Consolidate and Account', '1948–1950s'),
]

def read(p):
    return open(p, encoding='utf-8').read().strip() if os.path.exists(p) else ''

book = {
  'series': 'Observe The System',
  'title': 'The Israel Architecture',
  'subtitle': 'Book One: The Stages to 1948',
  'note': 'The documented record, told in order, with every claim tied to its source. Tap a note number to see it, a name in a figure for its detail, or the + button for contents, bookmarks and notes.',
  'chapters': [],
}
for cid, label, title, span in META:
    d = os.path.join(ROOT, 'book', 'part1', cid)
    order = next(c for c in CH if c['id'] == cid)['scenes']
    secs = []
    for sid in order:
        t = read(os.path.join(d, sid + '.html'))
        if not t: continue
        m = re.match(r'\s*<h2>(.*?)</h2>\s*', t, re.S)
        h = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else sid
        secs.append({'s': sid, 'h': h, 'html': t[m.end():] if m else t})
    book['chapters'].append({'id': cid, 'label': label, 'title': title, 'span': span,
                             'intro': read(os.path.join(d, '_intro.html')), 'outro': read(os.path.join(d, '_outro.html')), 'sections': secs})

payload = json.dumps(book, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
block = open(os.path.join(ROOT, 'tools', 'book_block.html'), encoding='utf-8').read().strip()
block = block.replace('__BOOK_JSON__', payload) + '\n'
s = re.sub(r'<!--BOOK-START-->.*?<!--BOOK-END-->\n?', '', s, flags=re.S)
i = s.find('<!--UX-START-->')
if i < 0: i = s.find('<!--ELEVEN-START-->')
if i < 0: i = s.rfind('</body>')
s = s[:i] + block + s[i:]
open(IDX, 'w', encoding='utf-8').write(s)
n = sum(len(c['sections']) for c in book['chapters'])
w = sum(len(re.sub(r'<[^>]+>|\[cite:[^\]]+\]', ' ', x['html']).split()) for c in book['chapters'] for x in c['sections'])
print('book embedded:', len(book['chapters']), 'chapters,', n, 'sections, ~%d words,' % w, len(payload) // 1024, 'KB')
