#!/usr/bin/env python3
"""
OTS: pro-Israel committee money, cycle by cycle, from the FEC's own bulk files.

For each election cycle (default 2016-2026) it reads the FEC file of every committee-to-candidate transaction
(pas2: contributions, earmarked pass-throughs and independent expenditures for or against candidates), keeps the
transactions made by pro-Israel committees, and writes:
  committees.csv            every committee counted, with how it was matched (review this list first)
  by_cycle.csv              totals per cycle and channel (direct, earmarked, spent for, spent against, other)
  by_committee.csv          totals per committee per cycle and channel
  top_<cycle>_<chamber>_<party>.csv   top 25 recipients of direct + earmarked money, per chamber and party
  ie_<cycle>.csv            every candidate a pro-Israel committee spent for or against, largest first
  summary.md                a readable overview of all of the above

Run it on your own computer (Python 3.8+, nothing to install), from the scripts folder:
    python3 ots_proisrael_cycles.py                          2016-2026
    python3 ots_proisrael_cycles.py --cycles 2020,2022,2024  some cycles only
Downloads per cycle: committees (cm, ~1 MB), candidates (cn, ~1 MB), committee-to-candidate transactions
(pas2, ~10-60 MB). Files already present in the bulk folder are reused. Safe to stop and re-run.

The committee list is a starting point, not a verdict: it combines a fixed list of known pro-Israel committees with
a name search, and prints both so a person can remove false matches (edit EXCLUDE below) before quoting any total.
Every figure is a lead to verify against fec.gov, never a finding on its own.
"""
import csv, io, os, re, ssl, sys, time, urllib.error, urllib.request, zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.environ.get('OTS_PROISRAEL_DIR') or os.path.join(HERE, '..', 'data', 'proisrael-cycles'))
BULK = os.path.abspath(os.environ.get('OTS_BULK_DIR') or os.path.join(HERE, '..', 'data', 'fec-bulk'))
FEC = 'https://www.fec.gov/files/bulk-downloads/{y}/{f}'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

# Known pro-Israel committees (FEC ids). Name matching below adds the rest; edit both lists freely.
KNOWN = {
    'C00797670': 'AIPAC PAC',
    'C00799031': 'United Democracy Project (AIPAC super PAC)',
    'C00699470': 'Pro-Israel America PAC',
    'C00127811': 'U.S. Israel PAC (USI PAC)',
    'C00429571': 'Democrats for Israel',
    'C00264564': "Women's Pro-Israel National PAC",
}
NAME_RX = re.compile(r'(\bISRAEL|NORPAC|NORTH JERSEY PAC|\bJ ?STREET|JSTREETPAC|DEMOCRATIC MAJORITY FOR ISRAEL|REPUBLICAN JEWISH COALITION|'
                     r'\bRJC\b|UNITED DEMOCRACY PROJECT|ZIONIS|JACPAC|PRO[- ]?ISRAEL|FRIENDS OF ISRAEL)', re.I)
NOT_RX = re.compile(r'(PALESTIN|\bARAB\b|ANTI[- ]?ZION|JEWISH VOICE FOR PEACE|IF NOT NOW)', re.I)
EXCLUDE = set()   # add committee ids here to drop false matches after reviewing committees.csv

CM = 'CMTE_ID CMTE_NM TRES_NM CMTE_ST1 CMTE_ST2 CMTE_CITY CMTE_ST CMTE_ZIP CMTE_DSGN CMTE_TP CMTE_PTY_AFFILIATION CMTE_FILING_FREQ ORG_TP CONNECTED_ORG_NM CAND_ID'.split()
CN = 'CAND_ID CAND_NAME CAND_PTY_AFFILIATION CAND_ELECTION_YR CAND_OFFICE_ST CAND_OFFICE CAND_OFFICE_DISTRICT CAND_ICI CAND_STATUS CAND_PCC CAND_ST1 CAND_ST2 CAND_CITY CAND_ST CAND_ZIP'.split()
PAS2 = 'CMTE_ID AMNDT_IND RPT_TP TRANSACTION_PGI IMAGE_NUM TRANSACTION_TP ENTITY_TP NAME CITY STATE ZIP_CODE EMPLOYER OCCUPATION TRANSACTION_DT TRANSACTION_AMT OTHER_ID CAND_ID TRAN_ID FILE_NUM MEMO_CD MEMO_TEXT SUB_ID'.split()
# FEC transaction types in pas2 and the channel each belongs to
CHANNEL = {'24K': 'direct', '24Z': 'direct', '24I': 'earmarked', '24T': 'earmarked', '24E': 'spent_for', '24A': 'spent_against',
           '24C': 'other', '24F': 'spent_for', '24N': 'spent_against', '24R': 'other', '24U': 'other'}
CHANNELS = ['direct', 'earmarked', 'spent_for', 'spent_against', 'other']

def log(*a): print(*a, flush=True)
def _ctx():
    try:
        import certifi; return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()
CTX = _ctx()

def fetch(url, dest, tries=8):
    if os.path.exists(dest) and os.path.getsize(dest) > 0: return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    for i in range(1, tries + 1):
        try:
            log(f'    downloading {os.path.basename(dest)}')
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), context=CTX, timeout=300) as r, open(dest + '.part', 'wb') as f:
                while True:
                    b = r.read(1 << 20)
                    if not b: break
                    f.write(b)
            os.replace(dest + '.part', dest); return dest
        except urllib.error.HTTPError as e:
            if e.code == 404: log(f'    not published: {url}'); return None
            wait = 30 * i; log(f'    FEC answered {e.code}; waiting {wait}s'); time.sleep(wait)
        except (ssl.SSLError, ssl.CertificateError):
            log('\n  SSL certificate problem. On a Mac, open Applications > Python 3.x and double-click "Install Certificates.command", then run this again.\n'); raise SystemExit(1)
        except Exception as e:
            wait = min(300, 20 * i); log(f'    connection problem ({e}); waiting {wait}s'); time.sleep(wait)
    log(f'    gave up on {url} for now; run again later'); return None

def bulk(y, stem):
    yy = str(y)[2:]
    for cand in (os.path.join(BULK, str(y), f'{stem}{yy}.zip'), os.path.join(BULK, f'{stem}{yy}.zip')):
        if os.path.exists(cand) and os.path.getsize(cand) > 0: return cand
    return fetch(FEC.format(y=y, f=f'{stem}{yy}.zip'), os.path.join(BULK, str(y), f'{stem}{yy}.zip'))

def rows(path, cols):
    try: z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        log(f'    {os.path.basename(path)} is damaged; deleting it so the next run downloads it again'); os.remove(path); return
    name = [n for n in z.namelist() if not n.endswith('/')][0]
    with z.open(name) as fh:
        for line in io.TextIOWrapper(fh, encoding='latin-1', newline=''):
            p = line.rstrip('\r\n').split('|')
            if len(p) < len(cols): p += [''] * (len(cols) - len(p))
            yield dict(zip(cols, p))

def money(x):
    try: return float(x or 0)
    except ValueError: return 0.0

def wcsv(path, head, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(head); w.writerows(data)

def fmt(n): return f'${n:,.0f}'

def main():
    cycles = [2016, 2018, 2020, 2022, 2024, 2026]
    if '--cycles' in sys.argv: cycles = [int(c) for c in sys.argv[sys.argv.index('--cycles') + 1].split(',')]
    log(f'OTS pro-Israel committee money, cycles {cycles}. Output: {OUT}')
    committees = {}            # id -> (name, type, how matched, first cycle seen)
    by_cycle = defaultdict(lambda: defaultdict(float)); by_cycle_n = defaultdict(lambda: defaultdict(int))
    by_cmte = defaultdict(lambda: defaultdict(float))
    memo_seen = defaultdict(float)
    summary = []
    for y in cycles:
        log(f'\n[{y}]')
        cm, cn, p2 = bulk(y, 'cm'), bulk(y, 'cn'), bulk(y, 'pas2')
        if not (cm and cn and p2): log('    missing files; this cycle is skipped this run'); continue
        cmte = {}
        for r in rows(cm, CM):
            cid, nm = r['CMTE_ID'], r['CMTE_NM']
            if cid in EXCLUDE: continue
            if cid in KNOWN: how = 'known list'
            elif NAME_RX.search(nm) and not NOT_RX.search(nm): how = 'name match'
            else: continue
            cmte[cid] = nm
            committees.setdefault(cid, [nm, r['CMTE_TP'], how, y])
        cand = {r['CAND_ID']: r for r in rows(cn, CN)}
        recv = defaultdict(lambda: defaultdict(float)); ie = defaultdict(lambda: defaultdict(float))
        seen = set()
        for r in rows(p2, PAS2):
            if r['CMTE_ID'] not in cmte: continue
            if r['SUB_ID'] in seen: continue
            seen.add(r['SUB_ID'])
            ch = CHANNEL.get(r['TRANSACTION_TP'], 'other'); amt = money(r['TRANSACTION_AMT'])
            memo = r['MEMO_CD'] == 'X'
            if memo and ch == 'direct':      # memo lines repeat money reported elsewhere; keep them out of direct totals
                memo_seen[(y, r['TRANSACTION_TP'])] += amt; continue
            by_cycle[y][ch] += amt; by_cycle_n[y][ch] += 1
            by_cmte[(y, r['CMTE_ID'])][ch] += amt
            cid = r['CAND_ID']
            if not cid: continue
            if ch in ('direct', 'earmarked'): recv[cid][ch] += amt
            elif ch in ('spent_for', 'spent_against'): ie[cid][ch] += amt
        def who(cid):
            c = cand.get(cid, {})
            office = {'H': 'House', 'S': 'Senate', 'P': 'President'}.get(c.get('CAND_OFFICE', ''), '?')
            seat = c.get('CAND_OFFICE_ST', '') + (('-' + c.get('CAND_OFFICE_DISTRICT', '')) if office == 'House' else '')
            return c.get('CAND_NAME', cid), c.get('CAND_PTY_AFFILIATION', ''), office, seat
        summary.append(f'\n## {y}\n')
        summary.append('| Channel | Total | Transactions |\n|---|---|---|')
        for ch in CHANNELS: summary.append(f'| {ch} | {fmt(by_cycle[y][ch])} | {by_cycle_n[y][ch]:,} |')
        for office in ('Senate', 'House'):
            for party, label in (('DEM', 'Democrats'), ('REP', 'Republicans')):
                lst = []
                for cid, v in recv.items():
                    nm, pty, off, seat = who(cid)
                    if off == office and pty == party: lst.append((v['direct'] + v['earmarked'], v['direct'], v['earmarked'], nm, seat, cid))
                lst.sort(reverse=True)
                top = lst[:25]
                wcsv(os.path.join(OUT, f'top_{y}_{office.lower()}_{party.lower()}.csv'), ['rank', 'candidate', 'seat', 'cand_id', 'total', 'direct', 'earmarked'],
                     [[i + 1, t[3], t[4], t[5], round(t[0], 2), round(t[1], 2), round(t[2], 2)] for i, t in enumerate(top)])
                if top:
                    summary.append(f'\n**{office} {label}, top 10 (direct + earmarked)**\n')
                    for i, t in enumerate(top[:10]): summary.append(f'{i + 1}. {t[3]} ({t[4]}): {fmt(t[0])}  (direct {fmt(t[1])}, earmarked {fmt(t[2])})')
        iel = []
        for cid, v in ie.items():
            nm, pty, off, seat = who(cid)
            iel.append((v['spent_for'] + v['spent_against'], v['spent_for'], v['spent_against'], nm, pty, off, seat, cid))
        iel.sort(reverse=True)
        wcsv(os.path.join(OUT, f'ie_{y}.csv'), ['candidate', 'party', 'office', 'seat', 'cand_id', 'spent_for', 'spent_against'],
             [[t[3], t[4], t[5], t[6], t[7], round(t[1], 2), round(t[2], 2)] for t in iel])
        if iel:
            summary.append('\n**Largest independent spending, for or against (top 10)**\n')
            for t in iel[:10]: summary.append(f'- {t[3]} ({t[4]}, {t[5]} {t[6]}): for {fmt(t[1])}, against {fmt(t[2])}')
        log(f'    {len(cmte)} committees; direct {fmt(by_cycle[y]["direct"])}, earmarked {fmt(by_cycle[y]["earmarked"])}, '
            f'spent for {fmt(by_cycle[y]["spent_for"])}, against {fmt(by_cycle[y]["spent_against"])}')
    wcsv(os.path.join(OUT, 'committees.csv'), ['cmte_id', 'name', 'fec_type', 'how_matched', 'first_cycle_seen'],
         sorted([[k] + v for k, v in committees.items()], key=lambda r: (r[3], r[1])))
    wcsv(os.path.join(OUT, 'by_cycle.csv'), ['cycle'] + CHANNELS, [[y] + [round(by_cycle[y][c], 2) for c in CHANNELS] for y in cycles])
    wcsv(os.path.join(OUT, 'by_committee.csv'), ['cycle', 'cmte_id', 'name'] + CHANNELS,
         sorted([[y, cid, committees.get(cid, [''])[0]] + [round(v[c], 2) for c in CHANNELS] for (y, cid), v in by_cmte.items()],
                key=lambda r: (r[0], -sum(r[3:]))))
    head = ['# Pro-Israel committee money, cycle by cycle (FEC bulk files)\n',
            f'Committees counted: {len(committees)} (see committees.csv; review name matches before quoting).',
            'Channels: direct = contributions (24K, 24Z, non-memo); earmarked = pass-throughs (24I, 24T); spent_for / spent_against = independent expenditures and communication costs.',
            'Memo-only direct lines skipped: ' + ', '.join(f'{y} {t}: {fmt(v)}' for (y, t), v in sorted(memo_seen.items())) if memo_seen else 'Memo-only direct lines skipped: none.']
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'summary.md'), 'w', encoding='utf-8') as f: f.write('\n'.join(head + summary) + '\n')
    log(f'\nDone. Read {os.path.join(OUT, "summary.md")} first, then committees.csv.')

if __name__ == '__main__':
    main()
