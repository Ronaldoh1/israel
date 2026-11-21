"""Build the interactive network explorer from network.json.
Writes: <repo>/epstein-network.html (library addendum; scene links are relative)
        and, with --artifact PATH, a standalone copy whose scene links are omitted.
Every edge's 'src' is split on ';' and each part resolved to a link where possible:
library scene id -> index.html#scene=ID; known outlet label -> URL from book/research."""
import json, re, glob, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
d = json.load(open(os.path.join(HERE, 'network.json')))
idx = open(os.path.join(REPO, 'index.html')).read()
scenes = set(re.findall(r'"id":"([a-z0-9_]+)","(?:ch|era)"', idx))
K = {}; KL = {}
for f in glob.glob(os.path.join(REPO, 'book/research/*.json')):
    for e in json.load(open(f)).get('entries', []):
        for s in e.get('sources', []): K[s['key']] = s['url']; KL[s['key']] = s['label']
LABEL = {  # outlet label (prefix) -> research key
 'NYT 2019': 'ep1_nyt_wexner2019', 'Vanity Fair 2003': 'ep1_vf_ward2003', 'Snopes': 'ep7_snopes_barr', 'BI 2025': 'ep1_bi_birthday2025',
 'BI via Yahoo': 'ep7_bi_dalton', 'Rolling Stone (Ward)': 'ep7_rs_ward2021', 'NYT via WYSU': 'ep7_wysu_nyt2025',
 'JPMorgan filing': 'ep7_rappler_jpm2023', 'Reuters, Jun 2023': 'ep7_rappler_jpm2023', 'Guardian, Nov 2025': 'ep6_guardian_reputation',
 'GMA News': 'ep6_gma_seo2026', 'NPR, Aug 2019': 'ep6_npr_media2019', 'NPR, Dec 2018': 'ep6_npr_brown2018',
 'BuzzFeed News': 'ep6_buzzfeed_edge', 'NBC News, 2026': 'ep6_nbc_bannon2026', 'AP via WAMC': 'ep6_ap_ruemmler2026',
 'WBUR': 'ep6_wbur_chomsky2025', 'Mediaite': 'ep5_mediaite_kushner2025', 'PBS NewsHour, Jul 2026': 'ep7_pbs_black2026',
 'PBS, Jul 2026': 'ep7_pbs_black2026', 'Roll Call': 'ep1_rollcall_release2026', 'NYDFS consent order': 'ep3_cnbc_dfs_db2020',
 'Middle East Eye': 'ep5_mee_chs2026', 'FEC filings': 'ep5_gma_donations2019',
}
URL = {
 'Fortune, Feb 2026': 'https://www.fortune.com/2026/02/06/jeffrey-epstein-files-coinbase-blockstream-michael-saylor-brock-pierce/',
 'DL News': 'https://dlnews.com/articles/people-culture/epstein-files-reveal-desire-to-steer-bitcoin-via-its-developers/',
 'Business Insider, 2026': 'https://www.aol.com/news/epstein-planning-major-renovation-private-103501428.html',
 'CNN via AlterNet': 'https://www.alternet.org/epstein-island-abuse/',
 'NBC via AOL, Aug 2019': 'https://www.aol.com/article/news/2019/08/01/jeffrey-epsteins-bizarre-building-private-island-raised-alarm/23784595/',
 'ABC, Feb 2026': 'https://www.goodmorningamerica.com/news/story/victims-settle-case-epsteins-longtime-attorney-accountant-documents-130325546',
 'EFTA00584804': 'https://epsteinexposed.com/documents/efta-efta00584804',
}
import csv as _csv
DS = [(int(r['efta_start'][4:]), int(r['efta_end'][4:]), r['dataset']) for r in _csv.DictReader(open(os.path.join(HERE, 'efta_datasets.csv')))]
def efta_url(part):
    m = re.search(r'EFTA(\d{8})', part)
    if not m: return None
    n = int(m.group(1))
    for a, b, ds in DS:
        if a <= n <= b: return 'https://www.justice.gov/epstein/files/DataSet%%20%s/EFTA%s.pdf' % (ds, m.group(1))
    return None
def resolve(src, base):
    out = []
    for part in [p.strip() for p in src.split(';') if p.strip()]:
        if part in scenes:
            out.append({'t': 'library scene', 'u': (base + 'index.html#scene=' + part) if base is not None else None}); continue
        if part in K:
            out.append({'t': KL[part], 'u': K[part]}); continue
        u = None
        for lab, k in LABEL.items():
            if part.startswith(lab): u = K.get(k); break
        if not u:
            for lab, v in URL.items():
                if part.startswith(lab): u = v; break
        if not u: u = efta_url(part)
        out.append({'t': part, 'u': u})
    return out
import subprocess as _sp
for _f in ('ep_viab_ui.js', 'ep_tests_ui.js'):   # a syntax error in either script would blank the whole page
    _r = _sp.run(['node', '--check', os.path.join(HERE, _f)], capture_output=True, text=True)
    assert _r.returncode == 0, _r.stderr
import ep_viability as _vb
_M = _vb.model(json.loads(json.dumps(d)))


def build(base):
    D = {'built': d['built'], 'qop_meta': d.get('qop_meta', {}), 'whatif_meta': d.get('whatif_meta'), 'viab': _M,
         'nodes': d['nodes'], 'edges': [dict(e, refs=e.get('refs') or resolve(e['src'], base)) for e in d['edges']]}
    t = open(os.path.join(HERE, 'graph_explorer_template.html')).read()
    R = [
        ('function delPanel(r){', 'function delPanel0(r){'),
        ('/* ---------- graph ---------- */', open(os.path.join(HERE, 'ep_viab_ui.js'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'ep_tests_ui.js'), encoding='utf-8').read() + '\n/* ---------- graph ---------- */'),
        ("  h+=`<dt>Sources</dt>", "  if(q.whatif) h+=`<dt>If removed</dt><dd>${esc(q.whatif.verdict)}: ${q.whatif.P}% runs${q.whatif.drop>=0.5?' (down '+q.whatif.drop+')':''}${q.whatif.deal!=null&&q.whatif.deal<100?' · 2008 deal '+q.whatif.deal+'% as likely':''}${q.whatif.account!=null&&q.whatif.account<100?' · brought to account '+q.whatif.account+'% as likely':''}</dd>`;\n  h+=`<dt>Sources</dt>"),
        ("ops:q=>q.succession?Math.round(q.succession.operations_cover*100):0,", "ops:q=>q.succession?Math.round(q.succession.operations_cover*100):0, whatif:q=>q.whatif?q.whatif.P:100,"),
        ("efta cover ops sponsor.", "efta cover ops sponsor whatif."),
        ("$('reset').onclick=()=>{ removed.clear();", "$('reset').onclick=()=>{ removed.clear(); vLS(VKEY,null); setTimeout(vPill,0);"),
    ]
    for a, b in R:
        assert a in t, a[:60]
        t = t.replace(a, b, 1)
    return t.replace('__DATA__', json.dumps(D, ensure_ascii=False).replace('</', '<\\/'))
_page = build('')
if not _page.lstrip().lower().startswith('<!doctype'):   # the v1 template was a fragment; the Library of Truth template is a full page
    _page = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + _page + '\n</html>\n'
open(os.path.join(REPO, 'epstein-network.html'), 'w').write(_page)
if '--artifact' in sys.argv:
    open(sys.argv[sys.argv.index('--artifact') + 1], 'w').write(build(None))
linked = sum(1 for e in d['edges'] for r in resolve(e['src'], '') if r['u'])
total = sum(len(resolve(e['src'], '')) for e in d['edges'])
print('built', len(d['nodes']), 'nodes', len(d['edges']), 'edges; source parts linked', linked, 'of', total)
