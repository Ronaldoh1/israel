"""Build de-network.html from the shared explorer template (book/plan/epstein_map/graph_explorer_template.html).
The template is the Epstein explorer; this script swaps in the Dark Enlightenment data and wording.
Usage: python3 build_explorer_de.py [OUT]  (default: repo root de-network.html)"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
d = json.load(open(os.path.join(HERE, 'network.json')))
K = {}; KL = {}
for f in glob.glob(os.path.join(REPO, 'book/research/*.json')):
    for e in json.load(open(f)).get('entries', []):
        for s in e.get('sources', []): K[s['key']] = s['url']; KL[s['key']] = s['label']
idx = open(os.path.join(REPO, 'index.html'), encoding='utf-8').read()
m = re.search(r'<script id="citationdata" type="application/json">(.*?)</script>', idx, re.S)
if m:
    for k, v in json.loads(m.group(1)).items(): K.setdefault(k, v if isinstance(v, str) else v[0])
m = re.search(r'<script id="citelabels" type="application/json">(.*?)</script>', idx, re.S)
if m:
    for k, v in json.loads(m.group(1)).items(): KL.setdefault(k, v)
import build_de
SECS = set(os.path.basename(f)[:-5] for st in build_de.STAGES for f in glob.glob(os.path.join(REPO, 'book/part1', st, '*.html')))
scenes = set(re.findall(r'"id":"([a-z0-9_]+)","(?:ch|era)"', idx))


SECFILE = {os.path.basename(f)[:-5]: f for st in build_de.STAGES for f in glob.glob(os.path.join(REPO, 'book/part1', st, '*.html'))}
def sec_sources(sec, n=3):
    """27 Nov 2026: a tie sourced only to a book section also carries that section's first sources, so every tie resolves."""
    keys = []
    for k in re.findall(r'\[cite:([A-Za-z0-9_]+)\]', open(SECFILE[sec], encoding='utf-8').read()):
        if k in K and k not in keys: keys.append(k)
    return [{'t': KL.get(k, k), 'u': K[k]} for k in keys[:n]]


def resolve(src):
    out = []
    for part in [p.strip() for p in src.split(';') if p.strip()]:
        if part in K: out.append({'t': KL.get(part, part), 'u': K[part]})
        elif part in SECS: out.append({'t': 'the book, section', 'u': 'index.html#book=' + part}); out.extend(sec_sources(part))
        elif part in scenes: out.append({'t': 'library scene', 'u': 'index.html#scene=' + part})
        else: out.append({'t': part, 'u': None})
    return out


unres = sum(1 for e in d['edges'] for r in resolve(e['src']) if not r['u'])
D = {'built': d['built'], 'qop_meta': d['qop_meta'], 'nodes': d['nodes'], 'edges': [dict(e, refs=e.get('refs') or resolve(e['src'])) for e in d['edges']]}
t = open(os.path.join(REPO, 'book/plan/epstein_map/graph_explorer_template.html'), encoding='utf-8').read()
A, B = d['qop_meta']['anchor_names']
R = [
    ('<title>The Epstein Network 🕸️ Interactive Graph · The Library of Truth ✨</title>', '<title>The Dark Enlightenment Network 🕸️ Network Map · The Library of Truth ✨</title>'),
    ('<h1>The Epstein Network 🕸️ <span>Interactive Graph</span></h1>', '<h1>The Dark Enlightenment 🕸️ <span>Network Map</span></h1>'),
    ('--k-document:#e083ab;', '--k-document:#e083ab; --k-event:#e6c25a;'),
    ('--k-document:#a0476b;', '--k-document:#a0476b; --k-event:#8a6a0a;'),
    ("const KINDS = ['person','company','institution','government','place','document'];", "const KINDS = ['person','company','institution','government','document','event','place'];"),
    ("'not-established'", "'co-mention'"), ('s-not-established', 's-co-mention'),
    ('<span>Not established</span>', '<span>Named together</span>'),
    ('<span>To verify</span>', '<span>Stated, uncited</span>'),
    ('<label class="chip"><input id="wh" type="checkbox" checked><span>Withheld</span></label>', '<label class="chip" style="display:none"><input id="wh" type="checkbox" checked><span>Withheld</span></label>'),
    ("E.forEach(e=>{ if((e.f!==id&&e.t!==id)||e.status==='co-mention') return; (e.f===id?out++:inn++);", "E.forEach(e=>{ if(e.f!==id&&e.t!==id) return; if(e.status==='co-mention'){ wh++; return; } (e.f===id?out++:inn++);"),
    ("<small>to verify</small>", "<small>uncited</small>"),
    ("<small>withheld</small>", "<small>named with</small>"),
    ("Keys: tier epstein maxwell role kind cluster ties edges verified leads withheld rank bridge flights island money loops volume volumes function sources efta cover ops sponsor.", "Keys: tier thiel palantir role kind cluster ties edges verified rank bridge money loops volume volumes sources book mentions."),
    ("<dt>From Epstein</dt>", "<dt>From " + A + "</dt>"), ("<dt>From Maxwell</dt>", "<dt>From " + B + "</dt>"),
    ("' with Epstein and Maxwell removed'", "' with " + A + " and " + B + " removed'"),
    ("epstein:q=>q.kb_epstein, maxwell:q=>q.kb_maxwell,", "thiel:q=>q.kb_epstein, palantir:q=>q.kb_maxwell, book:q=>(q.sections||[]).join(' '), mentions:q=>q.mentions||0,"),
    ("n.id==='epstein'?' selected':''", "n.id==='thiel'?' selected':''"),
]
for a, b in R:
    if a not in t: print('template text not found:', a[:70])
    t = t.replace(a, b)
t = re.sub(r'<p class="lede">[\s\S]*?</p>\s*<p class="lede">[\s\S]*?</p>',
    '<p class="lede">The people, companies, funds, agencies, texts, courts and events of the eight volumes of The Dark Enlightenment, from the writers (Yarvin, Land, Hoppe, Carlyle) to the money (Thiel, Musk, the super PACs), the offices (Vance, DOGE, the White House), the contractors (Palantir and the data vendors), the enforcement agencies, the charter cities and the courts. '
    'Every solid line is a tie stated in the book and checked against its sentence, with the book\'s own source attached: founded, funded, invested, employed, wrote, cited, contracted, sued. '
    'A writer is tied to a person only by authorship, citation, publication, funding, employment or their own words, never by resemblance or shared venue. '
    '“Named together” shows where the book names two nodes in one sentence without stating a tie; those are leads, never used for analysis. '
    'No group of followers, believers or any identity group is a node: ties come from documents, not identity.</p>', t, count=1)
t = t.replace("  h+=`<dt>Sources</dt>", "  if(q.sections&&q.sections.length) h+=`<dt>In the book</dt><dd>${q.sections.slice(0,6).map(s=>`<a href=\"index.html#book=${esc(s)}\" target=\"_blank\" rel=\"noopener\">${esc(s)}</a>`).join(', ')}${q.mentions?' · named '+q.mentions+' times':''}</dd>`;\n  h+=`<dt>Sources</dt>", 1)
t = t.replace("${q.sources.distinct} distinct, ${q.sources.doj_efta} DOJ release documents", "${q.sources.distinct} distinct sources behind its ties")
t = t.replace("if(q.open_leads.length) h+=`<dt>Open leads</dt>", "if(q.open_leads.length) h+=`<dt>Named together with</dt>")
t = t.replace("An edge is a document: a payment, contract, email, flight, appointment or filing. Solid = verified; dashed = lead to verify; thick purple = withheld (a document known to exist and not released); dotted red = not established, shown only when switched on and never used to walk.",
              "An edge is a tie the book states, with the book's source: founded, funded, invested, employed, wrote, cited, contracted, sued. Solid = sourced; dashed = stated in the book without a citation in that paragraph; dotted = named together in one sentence with no stated tie, shown only when switched on and never used to walk.")
t = re.sub(r"placeholder='e\.g\. tier:1[^']*'", "placeholder='e.g. role:DOGE ties>2   or   tier:1   or   cluster:surveillance   or   Yarvin'", t)
t = t.replace('__DATA__', json.dumps(D, ensure_ascii=False).replace('</', '<\\/'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'de-network.html')
# 27 Nov 2026: keep code edited on the live page; a rebuild replaces only its data
if os.path.exists(out) and 'const DATA = ' in open(out, encoding='utf-8').read():
    _old = open(out, encoding='utf-8').read(); _k = _old.find('const DATA = ') + len('const DATA = '); _, _e = json.JSONDecoder().raw_decode(_old, _k)
    _nk = t.find('const DATA = ') + len('const DATA = '); _, _ne = json.JSONDecoder().raw_decode(t, _nk)
    t = _old[:_k] + t[_nk:_ne] + _old[_e:]
open(out, 'w', encoding='utf-8').write(t)
print('built', out, len(d['nodes']), 'nodes', len(d['edges']), 'edges; unresolved source parts', unres)
