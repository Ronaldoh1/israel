"""Build road-network.html from the shared explorer template (book/plan/epstein_map/graph_explorer_template.html).
The template is the Epstein explorer; this script swaps in the 1948 data, wording and the 'event' kind.
Usage: python3 build_explorer_road.py [OUT]  (default: repo root road-network.html)"""
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
SECS = set(os.path.basename(f)[:-5] for st in ['ch01'] + ['rd%d' % i for i in range(7)] for f in glob.glob(os.path.join(REPO, 'book/part1', st, '*.html')))
scenes = set(re.findall(r'"id":"([a-z0-9_]+)","(?:ch|era)"', idx))


def resolve(src):
    out = []
    for part in [p.strip() for p in src.split(';') if p.strip()]:
        if part in K: out.append({'t': KL.get(part, part), 'u': K[part]})
        elif part in SECS: out.append({'t': 'the book, section', 'u': 'index.html#book=' + part})
        elif part in scenes: out.append({'t': 'library scene', 'u': 'index.html#scene=' + part})
        else: out.append({'t': part, 'u': None})
    return out


unres = sum(1 for e in d['edges'] for r in resolve(e['src']) if not r['u'])
D = {'built': d['built'], 'qop_meta': d['qop_meta'], 'nodes': d['nodes'], 'edges': [dict(e, refs=resolve(e['src'])) for e in d['edges']]}
t = open(os.path.join(REPO, 'book/plan/epstein_map/graph_explorer_template.html'), encoding='utf-8').read()
A, B = d['qop_meta']['anchor_names']
R = [
    ('<title>The Epstein Network 🕸️ Interactive Graph · The Library of Truth ✨</title>', '<title>The Road to 1948 Network 🕸️ Interactive Graph · The Library of Truth ✨</title>'),
    ('<h1>The Epstein Network 🕸️ <span>Interactive Graph</span></h1>', '<h1>The Road to 1948 🕸️ <span>Network Map</span></h1>'),
    ('href="index.html#library"', 'href="index.html#library"'),
    # kinds: add 'event'
    ('--k-document:#e083ab;', '--k-document:#e083ab; --k-event:#e6c25a;'),
    ('--k-document:#a0476b;', '--k-document:#a0476b; --k-event:#8a6a0a;'),
    ("const KINDS = ['person','company','institution','government','place','document'];", "const KINDS = ['person','institution','company','government','document','event','place'];"),
    # status vocabulary: co-mention plays the part of 'not established' (shown only on request, never walked)
    ("'not-established'", "'co-mention'"), ('s-not-established', 's-co-mention'),
    ('<span>Not established</span>', '<span>Named together</span>'),
    ('<span>To verify</span>', '<span>Stated, uncited</span>'),
    ('<label class="chip"><input id="wh" type="checkbox" checked><span>Withheld</span></label>', '<label class="chip" style="display:none"><input id="wh" type="checkbox" checked><span>Withheld</span></label>'),
    ("E.forEach(e=>{ if((e.f!==id&&e.t!==id)||e.status==='co-mention') return; (e.f===id?out++:inn++);", "E.forEach(e=>{ if(e.f!==id&&e.t!==id) return; if(e.status==='co-mention'){ wh++; return; } (e.f===id?out++:inn++);"),
    ("<small>to verify</small>", "<small>uncited</small>"),
    ("<small>withheld</small>", "<small>named with</small>"),
    ("Keys: tier epstein maxwell role kind cluster ties edges verified leads withheld rank bridge flights island money loops volume volumes function sources efta cover ops sponsor.", "Keys: tier epstein maxwell role kind cluster ties edges verified rank bridge money loops volume volumes sources book mentions."),
    ("<dt>From Epstein</dt>", "<dt>From " + A + "</dt>"), ("<dt>From Maxwell</dt>", "<dt>From " + B + "</dt>"),
    ("' with Epstein and Maxwell removed'", "' with the " + A + " and the " + B + " removed'"),
    ("const QHELP='Keys: tier epstein maxwell", "const QHELP='Keys: tier agency wzo"),
    ("epstein:q=>q.kb_epstein, maxwell:q=>q.kb_maxwell,", "agency:q=>q.kb_epstein, wzo:q=>q.kb_maxwell, book:q=>(q.sections||[]).join(' '), mentions:q=>q.mentions||0,"),
    ("n.id==='epstein'?' selected':''", "n.id==='herzl'?' selected':''"),

]
for a, b in R:
    if a not in t: print('template text not found:', a[:70])
    t = t.replace(a, b)
# lede
t = re.sub(r'<p class="lede">[\s\S]*?</p>\s*<p class="lede">[\s\S]*?</p>',
    '<p class="lede">The people, organizations, states, documents and events of The Baseline and The Road to 1948, from the Bank of England in 1694 to the armistices of 1949. '
    'Every solid line is a tie stated in the book and checked against its sentence, with the book\'s own source attached: founded, funded, led, wrote to, signed, opposed, expelled. '
    '“Named together” shows where the book names two nodes in one sentence without stating a tie; those are leads, never used for analysis. '
    'No ethnic or religious group is a node: ties come from documents, not identity.</p>', t, count=1)
# profile: link to the book sections that name the node
t = t.replace("  h+=`<dt>Sources</dt>", "  if(q.sections&&q.sections.length) h+=`<dt>In the book</dt><dd>${q.sections.slice(0,6).map(s=>`<a href=\"index.html#book=${esc(s)}\" target=\"_blank\" rel=\"noopener\">${esc(s)}</a>`).join(', ')}${q.mentions?' · named '+q.mentions+' times':''}</dd>`;\n  h+=`<dt>Sources</dt>")
t = t.replace("${q.sources.distinct} distinct, ${q.sources.doj_efta} DOJ release documents", "${q.sources.distinct} distinct sources behind its ties")
t = t.replace("if(q.open_leads.length) h+=`<dt>Open leads</dt>", "if(q.open_leads.length) h+=`<dt>Named together with</dt>")
t = t.replace("An edge is a document: a payment, contract, email, flight, appointment or filing. Solid = verified; dashed = lead to verify; thick purple = withheld (a document known to exist and not released); dotted red = not established, shown only when switched on and never used to walk.",
              "An edge is a tie the book states, with the book's source: founded, funded, led, wrote to, signed, opposed. Solid = sourced; dashed = stated in the book without a citation in that paragraph; dotted = named together in one sentence with no stated tie, shown only when switched on and never used to walk.")
t = re.sub(r"placeholder='e\.g\. tier:1[^']*'", "placeholder='e.g. role:finance ties>2   or   tier:1   or   volume:\"Vatican\"   or   Rothschild'", t)
t = t.replace('__DATA__', json.dumps(D, ensure_ascii=False).replace('</', '<\\/'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'road-network.html')
open(out, 'w', encoding='utf-8').write(t)
print('built', out, len(d['nodes']), 'nodes', len(d['edges']), 'edges; unresolved source parts', unres)
