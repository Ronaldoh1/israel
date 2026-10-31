"""Build one dossier per person for The Names (Epstein Architecture, Part 5).
Searches everything the library already holds:
  - index.html: every scene's narration (n / told / record) and every entity (name, role, detail, expanded, deep dive)
  - sophia.html: every embedded simulation module (base64, optionally zlib), as text paragraphs
  - book/plan/ep_*.md and book/plan/sources/*.md: the book's research files and Ron's source documents
Writes book/plan/names/<slug>.md (passages grouped by source, with scene ids) and book/plan/names/INDEX.md.
Usage: python3 tools/names_dossiers.py"""
import base64, glob, html, json, os, re, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'book/plan/names')

# name -> search patterns (regex, case-sensitive on surnames to avoid noise)
PEOPLE = {
 # A
 'Jeffrey Epstein': [r'\bEpstein\b'], 'Ghislaine Maxwell': [r'Ghislaine'], 'Robert Maxwell': [r'Robert Maxwell', r'Maxwell, Robert', r'\bMirror Group\b'],
 'Les Wexner': [r'Wexner'], 'Leon Black': [r'Leon Black'], 'Jes Staley': [r'Staley'], 'Sultan bin Sulayem': [r'Sulayem'],
 'Donald Trump': [r'\bTrump\b'], 'Melania Trump': [r'Melania'], 'Bill Clinton': [r'Bill Clinton', r'President Clinton'],
 'Hillary Clinton': [r'Hillary'], 'Howard Lutnick': [r'Lutnick'], 'Larry Summers': [r'Summers\b'], 'Steve Bannon': [r'Bannon'],
 'Bill Gates': [r'\bGates\b(?! Foundation)', r'Bill Gates'], 'Elon Musk': [r'Elon Musk', r'\bMusk\b(?!, Kimbal)'], 'Peter Thiel': [r'Thiel'],
 'Reid Hoffman': [r'Hoffman\b'], 'Andrew Mountbatten-Windsor': [r'Prince Andrew', r'Mountbatten-Windsor', r'Duke of York'],
 'Peter Mandelson': [r'Mandelson'], 'Ehud Barak': [r'(?<!Aharon )\bBarak\b(?! Hiram)(?! Obama)'], 'Thorbjorn Jagland': [r'Jagland'],
 'Alexander Acosta': [r'Acosta'], 'Alan Dershowitz': [r'Dershowitz'], 'Jean-Luc Brunel': [r'Brunel'],
 # B
 'Steven Hoffenberg': [r'Hoffenberg'], 'Fabrice Aidan': [r'Aidan\b'], 'Tom Pritzker': [r'Pritzker'], 'Glenn Dubin': [r'Dubin'],
 'Brock Pierce': [r'Brock Pierce'], 'Boris Nikolic': [r'Nikolic'], 'Larry Ellison': [r'Larry Ellison', r'Ellison\b(?=[^.]{0,80}(Oracle|Epstein|Barak|TBI|Blair))'], 'Kimbal Musk': [r'Kimbal'],
 'Steve Tisch': [r'Tisch'], 'Casey Wasserman': [r'Wasserman\b'], 'Brad Karp': [r'Brad Karp'], 'Kathy Ruemmler': [r'Ruemmler'],
 'Bill Richardson': [r'Richardson'], 'George Mitchell': [r'George Mitchell'], 'Stacey Plaskett': [r'Plaskett'], 'Mehmet Oz': [r'Mehmet Oz', r'\bDr\.? Oz\b'],
 'Mona Juul': [r'Mona Juul', r'\bJuul\b'], 'Terje Rod-Larsen': [r'R[øo]d-Larsen'], 'Miroslav Lajcak': [r'Laj[cč][aá]k'], 'Jack Lang': [r'Jack Lang'],
 'Borge Brende': [r'Brende'], 'Morgan McSweeney': [r'McSweeney'], 'Joanna Rubinstein': [r'Joanna Rubinstein'],
 'Sarah Ferguson': [r'Sarah Ferguson', r'Fergie'], 'Mette-Marit': [r'Mette-Marit'], 'Noam Chomsky': [r'Chomsky'], 'Woody Allen': [r'Woody Allen'],
 'Richard Branson': [r'Branson'], 'Marvin Minsky': [r'Minsky'], 'Joi Ito': [r'Joi Ito'], 'Martin Nowak': [r'Nowak'],
 'Lee Smolin': [r'Smolin'], 'David Gelernter': [r'Gelernter'], 'Peter Attia': [r'Attia'], 'Al Seckel': [r'Seckel'],
 'Darren Indyke': [r'Indyke'], 'Richard Kahn': [r'Richard Kahn', r'\bKahn\b'], 'Marie Villafana': [r'Villafa[ñn]a'],
 'Kenneth Marra': [r'Marra\b'], 'Roy Black': [r'Roy Black'], 'Barry Krischer': [r'Krischer'], 'Michael Reiter': [r'Reiter'],
 'Pam Bondi': [r'Bondi'], 'Todd Blanche': [r'Blanche'], 'Kash Patel': [r'Kash Patel'],
 # C
 'Sarah Kellen': [r'Kellen'], 'Lesley Groff': [r'Groff'], 'Adriana Ross': [r'Adriana Ross', r'Mucinska'], 'Nadia Marcinko': [r'Marcinko'],
 'Juan Alessi': [r'Alessi'], 'Alfredo Rodriguez': [r'Alfredo Rodriguez'], 'Larry Visoski': [r'Visoski'], 'David Rodgers': [r'David Rodgers'],
 'Merwin Dela Cruz': [r'Dela Cruz'], 'William Riley': [r'William Riley'], 'Paul Lavery': [r'Lavery'], 'Thomas Massie': [r'Massie'],
 'Ro Khanna': [r'Khanna'], 'Mike Johnson': [r'Speaker Johnson', r'Mike Johnson'], 'Tova Noel': [r'Tova Noel', r'\bNoel\b'],
 'Efrain Reyes': [r'Efrain Reyes'], 'Mark Middleton': [r'Middleton'], 'Michael Freeman': [r'Freeman'], 'Daniel Siad': [r'Siad'],
 # The people who told
 'Maria Farmer': [r'Maria Farmer'], 'Annie Farmer': [r'Annie Farmer'], 'Virginia Giuffre': [r'Giuffre', r'Virginia Roberts'],
 'Johanna Sjoberg': [r'Sjoberg'], 'Courtney Wild': [r'Courtney Wild'], 'Cheri Pierson': [r'Cheri Pierson'], 'Lisa Phillips': [r'Lisa Phillips'],
 'Vicky Ward': [r'Vicky Ward'], 'Julie K. Brown': [r'Julie K\.? Brown', r'Julie Brown'],
}
DEPTH = {}
for n in list(PEOPLE)[:25]: DEPTH[n] = 'A'
for n in list(PEOPLE)[25:70]: DEPTH[n] = 'B'
for n in list(PEOPLE)[70:89]: DEPTH[n] = 'C'
for n in list(PEOPLE)[89:]: DEPTH[n] = 'told'

TAG = re.compile(r'<[^>]+>')
def clean(t): return re.sub(r'\s+', ' ', html.unescape(TAG.sub(' ', t or ''))).strip()

def paras(text):
    for p in re.split(r'\n\s*\n|(?<=[.!?])\s{2,}', text):
        p = clean(p)
        if len(p) > 40: yield p

def sentences_around(text, rx, width=1):
    """the sentence(s) containing a match plus `width` sentences either side"""
    ss = re.split(r'(?<=[.!?])\s+', text)
    hit = [i for i, s in enumerate(ss) if rx.search(s)]
    keep = sorted({j for i in hit for j in range(max(0, i - width), min(len(ss), i + width + 1))})
    out, last = [], -2
    for j in keep:
        out.append(('… ' if j != last + 1 else '') + ss[j]); last = j
    return ' '.join(out).strip()

def load_index():
    s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    g = lambda p: json.loads(re.search(p, s, re.S).group(1))
    D = g(r'<script id="scenedata" type="application/json">(.*?)</script>')
    EX = g(r'<script id="expanded-en" type="application/json">(.*?)</script>')
    DD = g(r'<script id="deepdive-en" type="application/json">(.*?)</script>')
    for x in D:
        sid = x['id']; title = '%s · %s (%s)' % (sid, clean(x.get('t')), x.get('yr', ''))
        for k in ('n', 'tld', 'rec'):
            if x.get(k): yield 'library', title, k, clean(x[k])
        for e in x.get('ents', []):
            head = '%s (%s)' % (clean(e.get('nm')), clean(e.get('rl')))
            body = ' '.join(filter(None, [clean(e.get('dt')), clean((EX.get(sid, {}).get(e['id']) or {}).get('dt'))]))
            d = DD.get(sid, {}).get(e['id'])
            if d: body += ' ' + ' '.join(clean(q.get('body')) for q in d.get('sections', []))
            yield 'library', title, head, body

def load_sophia():
    s = open(os.path.join(ROOT, 'sophia.html'), encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'<script type="text/plain" id="([A-Za-z0-9_]+_sim_b64)"[^>]*>(.*?)</script>', s, re.S):
        raw = base64.b64decode(re.sub(r'\s+', '', m.group(2)))
        if raw[:1] == b'\x78':
            try: raw = zlib.decompress(raw)
            except zlib.error: pass
        t = raw.decode('utf-8', 'replace')
        # pull string values out of embedded JSON/JS; fall back to visible text
        chunks = re.findall(r'"(?:dt|n|tld|rec|body|lead|detail|text|desc|summary)"\s*:\s*"((?:[^"\\]|\\.){60,})"', t)
        if not chunks: chunks = list(paras(TAG.sub('\n\n', t)))
        for c in chunks:
            try: c = json.loads('"%s"' % c)
            except Exception: pass
            yield 'sophia', m.group(1).replace('_sim_b64', ''), '', clean(c)

def load_files():
    for f in sorted(glob.glob(os.path.join(ROOT, 'book/plan/ep_*.md')) + glob.glob(os.path.join(ROOT, 'book/plan/sources/*.md')) + glob.glob(os.path.join(ROOT, 'book/plan/sources/*.txt'))):
        if 'THE_NAMES' in f: continue
        name = os.path.relpath(f, os.path.join(ROOT, 'book/plan'))
        for p in paras(open(f, encoding='utf-8').read()):
            yield 'files', name, '', p

def main():
    os.makedirs(OUT, exist_ok=True)
    corpus = list(load_index()) + list(load_sophia()) + list(load_files())
    seen = set(); docs = []
    for src, where, head, text in corpus:
        key = (src, text[:200])
        if text and key not in seen: seen.add(key); docs.append((src, where, head, text))
    index = []
    for name, pats in PEOPLE.items():
        rx = re.compile('|'.join(pats))
        hits = {'library': [], 'sophia': [], 'files': []}
        for src, where, head, text in docs:
            if rx.search(text) or rx.search(head):
                ex = text if len(text) <= 900 else sentences_around(text, rx)
                hits[src].append((where, head, ex))
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        with open(os.path.join(OUT, slug + '.md'), 'w', encoding='utf-8') as f:
            f.write('# Dossier: %s (depth %s)\n*Everything the library already holds that mentions this person, for writing The Names. '
                    'Generated by tools/names_dossiers.py. Raw material: verify every fact against its cited source before use.*\n\n' % (name, DEPTH[name]))
            for src, label in (('library', 'Library scenes (index.html)'), ('sophia', 'Sophia modules (sophia.html)'), ('files', 'Book research files and Ron\'s sources')):
                f.write('## %s · %d passages\n\n' % (label, len(hits[src])))
                for where, head, ex in hits[src]:
                    f.write('- **%s**%s: %s\n' % (where, (' · ' + head) if head else '', ex))
                f.write('\n')
        index.append((DEPTH[name], name, slug, len(hits['library']), len(hits['sophia']), len(hits['files'])))
    with open(os.path.join(OUT, 'INDEX.md'), 'w', encoding='utf-8') as f:
        f.write('# The Names: dossier index\n*Passages found per person, by source. Low counts mark people who need new research before their entry can be written.*\n\n')
        f.write('| Depth | Person | Library | Sophia | Files | Dossier |\n|---|---|---|---|---|---|\n')
        for d, n, s, a, b, c in index:
            f.write('| %s | %s | %d | %d | %d | [%s.md](%s.md) |\n' % (d, n, a, b, c, s, s))
    print(len(docs), 'passages searched;', len(index), 'dossiers')
    for row in index: print(*row[:2], row[3:])

if __name__ == '__main__':
    main()
