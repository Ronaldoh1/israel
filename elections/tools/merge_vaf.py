#!/usr/bin/env python3
"""Merge the Vote America First build pack (Ron's Mac, Oct 2026) into the 2026 Elections module data.

Usage: python3 merge_vaf.py <pack_dir> <data_states.json in> <data_states.json out>

Adds, for every ballot candidate, only what the records show, without overwriting hand-researched fields:
  photo            licensed portrait URL (official congressional portraits, Wikimedia)
  links            campaign site, Ballotpedia, Wikipedia
  wiki             opening paragraph of the matched Wikipedia article (attributed, linked)
  votes_kv         key-vote positions, from the member's full roll-call record (sitting/former members)
  vstats           attendance in the current Congress, from the same record
  recordx          missed_pct and FEC filing record (RFAI notices), where not already researched
  effectiveness    bills sponsored and enacted in the 119th Congress; committee seats
  politifact       PolitiFact scorecard counts (display only; not used in the score)
  ethics_docs      House/Senate Ethics Committee documents whose titles name the candidate
  fec_notices      FEC requests for additional information (RFAI) sent to their committees
  deep             2026 money detail: itemized donors, in-state share, earmarks, outside groups and who funds them
Nothing from court-name matches is published: a docket under the same name is a lead, not a finding."""
import csv, glob, json, os, re, sys, collections

PACK, SRC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
RP = os.path.join(PACK, 'data', 'research-pack')
MD = os.path.join(PACK, 'data', 'money-deep')
D = json.load(open(SRC, encoding='utf-8'))
C = D['cands']
KV = D['keyvotes']['votes']
KVKEY = {(k['congress'], k['chamber'], int(k['roll'])): k['id'] for k in KV}
CURRENT = 119
stats = collections.Counter()

def jload(p):
    try: return json.load(open(p, encoding='utf-8'))
    except Exception: return None

def lead(text, cap=700):
    """First paragraph of a Wikipedia article, cut at a sentence boundary."""
    if not text: return ''
    para = text.strip().split('\n')[0].strip()
    if len(para) <= cap: return para
    cut = para[:cap]; i = max(cut.rfind('. '), cut.rfind('.)'))
    return (cut[:i + 1] if i > 200 else cut.rstrip() + '…')

PF = ['true', 'mostly true', 'half true', 'mostly false', 'false', 'pants on fire']
def politifact(j):
    t = (j or {}).get('profile_text') or ''
    if not t or not j.get('url'): return None
    out = {}
    for lab in PF:
        m = re.search(r'\n' + re.escape(lab) + r'\s*\n\s*\d+%\s*\n\s*(\d+) Checks', t, re.I)
        if m: out[lab] = int(m.group(1))
    if not out or not sum(out.values()): return None
    return {'u': j['url'], 'counts': out}

def folder(cid):
    st = cid[:2].upper()
    p = os.path.join(RP, st, cid)
    return p if os.path.isdir(p) else None

def money(cid):
    for p in glob.glob(os.path.join(MD, '*', cid, 'money_deep.json')):
        return jload(p)
    return None

def short_outside(rows, n=6):
    rows = sorted(rows or [], key=lambda r: -(r.get('amount') or 0))[:n]
    out = []
    for r in rows:
        f = r.get('funders') or {}
        out.append([r.get('name', ''), round(r.get('amount') or 0), bool(r.get('discloses_donors_to_fec')),
                    [[x[0], x[1]] for x in (f.get('donors_organizations') or [])[:3]],
                    [[x[0], x[1], x[2] if len(x) > 2 else ''] for x in (f.get('donors_individual') or [])[:3]],
                    r.get('type', '')])
    return out

for cid, c in C.items():
    fd = folder(cid)
    if not fd: stats['no_folder'] += 1; continue
    stats['folders'] += 1
    # photo
    ph = jload(os.path.join(fd, 'photo.json')) or {}
    if ph.get('source') and not (c.get('photo') or {}).get('src'):
        c['photo'] = {'src': ph['source'], 'page': ph.get('license_url') or ph['source'],
                      'credit': (ph.get('credit') or 'source') + (' (' + ph['license'] + ')' if ph.get('license') else '')}
        stats['photo'] += 1
    # links
    L = c.setdefault('links', {})
    bp = jload(os.path.join(fd, 'ballotpedia.json')) or {}
    cs = jload(os.path.join(fd, 'campaign_site.json')) or {}
    site = cs.get('home') or (bp.get('links') or {}).get('campaign website')
    if site and not L.get('site'): L['site'] = site; stats['site'] += 1
    if bp.get('url') and not L.get('ballotpedia'): L['ballotpedia'] = bp['url']
    wk = jload(os.path.join(fd, 'wikipedia.json')) or {}
    if wk.get('url'):
        L.setdefault('wikipedia', wk['url'])
        t = lead(wk.get('text'))
        if t: c['wiki'] = {'t': t, 'u': wk['url'], 'title': wk.get('title') or c['name'], 'matched_by': wk.get('matched_by', '')}; stats['wiki'] += 1
    if not L: c.pop('links')
    # votes
    vp = os.path.join(fd, 'votes_all.csv')
    if os.path.exists(vp):
        rows = list(csv.DictReader(open(vp, encoding='utf-8')))
        kv, chamber_n = {}, collections.Counter()
        cur = [r for r in rows if r.get('congress') == str(CURRENT)]
        for r in rows:
            ch = (r.get('chamber') or '').lower()
            try: key = (int(r['congress']), ch, int(r['rollcall']))
            except (ValueError, KeyError): continue
            if key in KVKEY: kv[KVKEY[key]] = r.get('vote', ''); chamber_n[ch] += 1
        if kv and not c.get('votes_kv'):
            c['votes_kv'] = kv; c['votes_chamber'] = chamber_n.most_common(1)[0][0]
            c['votes_note'] = 'Positions from the official roll-call record (Voteview / House Clerk / Senate), matched by roll-call number.'
            stats['votes_kv'] += 1
        if cur:
            ch = collections.Counter((r.get('chamber') or '').lower() for r in cur).most_common(1)[0][0]
            cc = [r for r in cur if (r.get('chamber') or '').lower() == ch]
            missed = sum(1 for r in cc if re.search(r'not voting|absent', r.get('vote', ''), re.I))
            pct = round(missed / len(cc) * 100, 1) if cc else None
            c['vstats'] = {'congress': CURRENT, 'chamber': ch, 'n': len(cc), 'missed': missed, 'pct': pct,
                           'first': min(r['date'] for r in cc), 'last': max(r['date'] for r in cc)}
            rx = c.setdefault('recordx', {})
            if rx.get('missed_pct') is None and len(cc) >= 50:
                rx['missed_pct'] = pct; rx.setdefault('period', f'{CURRENT}th Congress'); rx['added'] = (rx.get('added', '') + ' Missed-vote rate: ' + str(missed) + ' of ' + str(len(cc)) + ' roll calls in the ' + str(CURRENT) + 'th Congress, from the official roll-call record (Oct 18, 2026).').strip(); stats['missed_pct'] += 1
    # bills and committees
    bl = jload(os.path.join(fd, 'bills.json'))
    cm = jload(os.path.join(fd, 'committees.json'))
    if (bl or cm) and not c.get('effectiveness'):
        E = {}
        if bl:
            sp = [b for b in bl.get('sponsored', []) if b and b[0] == CURRENT]
            law = [b for b in sp if re.search(r'became public law|signed by president', str(b[7] or ''), re.I)]
            E.update({'sponsored': len(sp), 'law': len(law), 'congress': f'{CURRENT}th', 'laws': [[b[1] + ' ' + str(b[2]), b[4]] for b in law][:12],
                      'src': 'congress.gov'})
        if cm:
            E['committees'] = [s['committee'].replace('House Committee on ', '').replace('Senate Committee on ', '') + (' (' + s['title'] + ')' if s.get('title') else '')
                               for s in cm.get('seats', []) if ':' not in s['committee']]
        c['effectiveness'] = E; stats['effectiveness'] += 1
    # FEC filing record
    fr = jload(os.path.join(fd, 'fec_filing_record.json'))
    if fr is not None:
        notes = fr.get('rfai_notices') or []
        c['fec_notices'] = [[n.get('date', '')[:10], n.get('report', ''), n.get('pdf', '')] for n in sorted(notes, key=lambda n: n.get('date', ''), reverse=True)][:8]
        c['fec_notices_n'] = len(notes)
        rx = c.setdefault('recordx', {})
        if not rx.get('fec'):
            rx['fec'] = 'notices' if notes else 'clean'; stats['fec_record'] += 1
            rx['added'] = (rx.get('added', '') + ' FEC filing record: ' + (str(len(notes)) + ' requests for additional information (RFAI) to their committees' if notes else 'no requests for additional information') + ', from FEC filings (Oct 17, 2026).').strip()
    # ethics
    et = jload(os.path.join(fd, 'ethics.json')) or {}
    if et.get('matches'): c['ethics_docs'] = [[m.get('title', ''), m.get('url', ''), m.get('source', '')] for m in et['matches']]; stats['ethics_docs'] += 1
    # PolitiFact
    pf = politifact(jload(os.path.join(fd, 'factchecks.json')))
    if pf: c['politifact'] = pf; stats['politifact'] += 1
    # money detail
    m = money(cid)
    if m:
        cy = (m.get('cycles') or {}).get('2026') or {}
        dn = cy.get('donors') or {}; out = cy.get('outside') or {}; fl = m.get('flags') or {}
        q = cy.get('quarters') or {}
        qmain = max(q.values(), key=len) if q else []
        deep = {'thru': (m.get('collected') or '')[:10],
                'itemized': dn.get('itemized_individual_total'), 'instate': dn.get('instate_share'),
                'top': [[x[0], x[1], x[2]] for x in (dn.get('top_donors') or [])[:10]],
                'earmarks': fl.get('lobby_leads') or [],
                'for': short_outside(out.get('support')), 'against': short_outside(out.get('oppose')),
                'nondisc': fl.get('non_disclosing_outside_spending') or 0,
                'q': [[r[0], r[2], r[3]] for r in qmain]}
        if any([deep['itemized'], deep['top'], deep['for'], deep['against'], deep['earmarks']]):
            c['deep'] = deep; stats['deep'] += 1

D['meta']['vaf_merged'] = '2026-10-18'
json.dump(D, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(dict(stats))
