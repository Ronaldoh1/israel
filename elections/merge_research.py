"""Merge researched JSON into data.json. Re-runnable: always starts from gen_data.py output.
Usage: python3 gen_data.py && python3 merge_research.py"""
import json, re, glob, os
B = '/home/claude/el26/'
D = json.load(open(B + 'data.json'))
CI = D['cites']

def recite(obj, pre):
    """prefix every citation key inside obj (any 'c' list) so different candidates' keys never collide"""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == 'c' and isinstance(v, list): obj[k] = [pre + x for x in v]
            else: recite(v, pre)
    elif isinstance(obj, list):
        for x in obj: recite(x, pre)

def add_cites(cites, pre):
    for k, v in cites.items(): CI[pre + k] = v

r = D['races']['AL-SEN']
r['research'] = 'partial'
r['note'] = ('Independent Craig Jelks is campaigning for the seat and has challenged both nominees to debate; his ballot qualification is being confirmed. '
             'Neither nominee had answered the debate challenge as of Oct. 1.')
r['src'] = r.get('src', []) + ['al_jelks']
CI['al_jelks'] = {'t': 'Jelks challenges Senate opponents Wess, Moore to debate — Alabama Political Reporter (Oct 1, 2026)', 'u': 'https://www.alreporter.com/2026/10/01/jelks-challenges-senate-opponents-wess-moore-to-debate/'}

# ---------- Race files: research/<st>-house.json (AL) or <st>-races.json (AK on) ----------
def slug(x): return re.sub(r'[^a-z0-9]+', '-', x.lower()).strip('-')
for hf in sorted(glob.glob(B + 'research/*-house.json') + glob.glob(B + 'research/*-races.json')):
    code = os.path.basename(hf)[:2].upper()
    H = json.load(open(hf)); pre = code.lower() + 'h_'
    add_cites(H.get('cites', {}), pre); recite(H, pre)
    st = next(s for s in D['states'] if s['code'] == code)
    if H.get('map_note'): st['redistricting'] = H['map_note']
    st['research'] = 'partial'
    for rid, d in H['districts'].items():
        race = D['races'][rid]
        if d.get('incumbent'): race['incumbent'] = d['incumbent']
        race['research'] = 'partial'
        if d.get('note'): race['note'] = d['note']
        if d.get('rating'): race['context'] = {'t': 'Race rating: ' + d['rating']['t'], 'c': d['rating'].get('c', [])}
        race['src'] = d.get('c', [])
        for old in race.get('candidates', []): D['cands'].pop(old, None)     # seed list is replaced by the verified ballot
        ids = []
        for cd in d['candidates']:
            cid = rid.lower() + '-' + slug(cd['name'])
            one = cd.get('oneliner')
            if one and 'verify' in one.get('t', '').lower(): one = None    # drop anything the researcher flagged as unverified
            c = dict(id=cid, name=cd['name'], party=cd['party'], race=rid, incumbent=bool(cd.get('incumbent')), research='pending')
            if cd.get('site'): c['links'] = {'site': cd['site']}
            if one: c['profile_line'] = one
            if cd.get('fec_id'): c['fec_id'] = cd['fec_id']
            D['cands'][cid] = c; ids.append(cid)
        race['candidates'] = ids


# ---------- Candidate dossiers: every research/<candidate-id>.json, merged the same way ----------
SKIP = {'keyvotes.json', 'stances.json'}
# candidates who ran for state or local office before (their state filings live on the Alabama FCPA site, unreachable from here)
STATE_HISTORY = {'al-sen-barry-moore', 'al-sen-everett-wess', 'al-01-jerry-carl', 'al-02-rhett-marques', 'al-03-mike-rogers', 'al-05-dale-strong', 'al-06-maurice-mercer'}
def scope_of(o):
    n = (str(o.get('name', '')) + ' ' + str(o.get('note', ''))).lower()
    return None if '2026 cycle' in n else 'career'
for path in sorted(glob.glob(B + 'research/*.json')):
    fn = os.path.basename(path)
    if fn in SKIP or fn.endswith('-votes.json') or fn.endswith('-house.json') or fn.endswith('-races.json'): continue
    cid = fn[:-5]
    if cid not in D['cands']: continue
    R0 = json.load(open(path)); pre = 'k' + re.sub(r'[^a-z0-9]', '', cid)[-14:] + '_'
    add_cites(R0.pop('cites', {}), pre)
    R0.pop('research_notes', None); R0.pop('id', None)
    recite(R0, pre)
    c = D['cands'][cid]
    for k, v in R0.items():
        if k in ('id', 'name', 'party', 'race', 'incumbent', 'research'): continue   # structural fields come from the race list, never from research files
        if v in (None, {}, []) and k not in ('legal', 'foreign', 'democracy', 'money_flags'): continue
        c[k] = v
    c['research'] = 'partial'
    f = c.get('fec')
    if f:
        src = f.get('src')
        pa = None
        if isinstance(src, dict): pa = src.pop('pac_all', None)
        if pa is None: pa = f.pop('pac_all', None)
        else: f.pop('pac_all', None)
        if isinstance(src, dict):
            if pa and not (src.get('pac_biz') or src.get('pac_ideo')): src['pac'] = pa
            for k2 in list(src):
                if src[k2] is None: src.pop(k2)
        if not f.get('history') and isinstance(c.get('money_history'), list): f['history'] = c['money_history']
    I = c.get('israel') or {}
    if I.get('aipac_pac') and I['aipac_pac'].get('amt') and scope_of(I['aipac_pac']): I['aipac_pac']['scope'] = 'career'
    for o in I.get('others', []):
        if scope_of(o): o['scope'] = 'career'
    if c.get('money_flags_note'):
        c.setdefault('checklist', {})['money_history'] = 'news'      # untraced money: never credited as clean
    if cid in STATE_HISTORY and c.get('checklist', {}).get('money_history') == 'done':
        c['checklist']['money_history'] = 'news'   # earlier state/local races: Alabama FCPA filings could not be reached, so the career search is incomplete

# ---------- Key-vote list ----------
if os.path.exists(B + 'research/keyvotes.json'):
    KVD = json.load(open(B + 'research/keyvotes.json'))
    add_cites(KVD.pop('cites', {}), 'kv_'); recite(KVD, 'kv_')
    D['keyvotes'] = KVD

# ---------- Roll-call votes on the key-vote list ----------
FORMER = {'ak-sen-mary-peltola': '2022\u20132025', 'al-01-jerry-carl': '2021\u20132025'}
for vf in glob.glob(B + 'research/*-votes.json'):
    V = json.load(open(vf))
    if 'keyvotes' in D:
        for kv in D['keyvotes']['votes']:
            pm = V.get('party_majority', {}).get(kv['id'])
            if pm: kv['party_majority'] = {k: pm[k] for k in ('R', 'D') if k in pm}
            if V.get('urls', {}).get(kv['id']) and not kv.get('url'): kv['url'] = V['urls'][kv['id']]
    for name, votes in V.get('members', {}).items():
        hits = [c for c in D['cands'].values() if c['name'] == name and c['id'].startswith(os.path.basename(vf).split('-')[0])]
        for c in hits:
            c['votes_kv'] = votes; c['votes_chamber'] = 'senate' if any(k.startswith('s1') for k in votes) else 'house'
            if c['research'] == 'pending': c['research'] = 'partial'
            sen = c['votes_chamber'] == 'senate'
            if sen: c['votes_note'] = {'t': 'Votes cast as a U.S. Senator, from official Senate roll calls.', 'c': ['senate_rolls']}
            elif c['id'] in FORMER: c['votes_note'] = {'t': 'Votes from an earlier term in the U.S. House (' + FORMER[c['id']] + '); not currently in office.', 'c': ['clerk_rolls']}
            elif not c.get('incumbent') and not c['race'].endswith('-SEN'): c['votes_note'] = {'t': 'Votes from an earlier term in the U.S. House; not currently in office.', 'c': ['clerk_rolls']}
            else: c['votes_note'] = {'t': 'Votes cast as a member of the U.S. House, from the House Clerk\u2019s official roll calls.', 'c': ['clerk_rolls']}
CI['senate_rolls'] = {'t': 'U.S. Senate \u2014 roll-call votes (senate.gov)', 'u': 'https://www.senate.gov/legislative/votes_new.htm'}
CI['clerk_rolls'] = {'t': 'Office of the Clerk, U.S. House of Representatives \u2014 roll-call votes', 'u': 'https://clerk.house.gov/Votes'}

# ---------- Sophia's published key-vote positions ----------
if os.path.exists(B + 'research/stances.json'):
    SD = json.load(open(B + 'research/stances.json'))
    add_cites(SD.pop('cites', {}), 'st_'); recite(SD, 'st_')
    D['stances'] = SD

# ---------- case study: Thomas Massie ----------
for k, v in {'theintercept': ('Thomas Massie loses primary \u2014 The Intercept (May 19, 2026)', 'https://theintercept.com/2026/05/19/thomas-massie-loses-election-results-trump-aipac-kentucky/'),
             'aljazeera': ('Trump critic Massie defeated: takeaways \u2014 Al Jazeera (May 20, 2026)', 'https://www.aljazeera.com/news/2026/5/20/trump-critic-massie-defeated-takeaways-from-us-primary-election-results'),
             'lpm': ('A record-shattering $37M was spent on Kentucky\u2019s Massie-Gallrein race \u2014 Louisville Public Media (Jul 17, 2026)', 'https://www.lpm.org/news/2026-07-17/a-record-shattering-37m-was-spent-on-kentuckys-massie-gallrein-race-heres-who-funded-it'),
             'pbs': ('Massie\u2019s loss leaves no doubt about Trump\u2019s power over the GOP \u2014 PBS NewsHour (May 2026)', 'https://www.pbs.org/newshour/politics/massies-loss-leaves-no-doubt-about-trumps-power-over-the-gop-6-takeaways-from-tuesdays-primaries'),
             'notus': ('Massie-Gallrein primary spending and donors \u2014 NOTUS (2026)', 'https://www.notus.org/2026-election/massie-gallrein-primary-spending-donors'),
             'mee': ('Anti-AIPAC congressman unseated in most expensive House primary ever \u2014 Middle East Eye (2026)', 'https://www.middleeasteye.net/news/anti-aipac-congressman-unseated-most-expensive-house-primary-ever'),
             'wapo': ('Thomas Massie faces Ed Gallrein in Kentucky GOP primary with massive spending \u2014 Washington Post (May 19, 2026)', 'https://www.washingtonpost.com/politics/2026/05/19/thomas-massie-faces-ed-gallrein-kentucky-gop-primary-with-massive-spending/'),
             'trackaipac': ('Track AIPAC \u2014 candidates', 'https://www.trackaipac.com/candidates'),
             'aj0518': ('Massie race breaks spending record as pro-Israel groups target Trump critic \u2014 Al Jazeera (May 18, 2026)', 'https://www.aljazeera.com/news/2026/5/18/massie-race-breaks-spending-record-as-pro-israel-groups-target-trump-critic'),
             'kylantern': ('Trump endorses Shelby County Republican to challenge Thomas Massie \u2014 Kentucky Lantern (Oct 18, 2025)', 'https://kentuckylantern.com/?p=34843')}.items():
    CI['ms_' + k] = {'t': v[0], 'u': v[1]}
D['cases'] = {'massie': {
  'kicker': 'Kentucky 4th District \u00b7 Republican primary, May 19, 2026',
  'title': 'Thomas Massie: what happens when a member votes the record, not the money',
  'lede': {'t': 'A seven-term Republican who took no pro-Israel PAC money, voted against Israel aid packages, and broke with the President on his signature tax bill, the Iran war and the Epstein files. He lost his primary to Trump-backed challenger Ed Gallrein, 54.9% to 45.1%, in the most expensive House primary on record.', 'c': ['ms_theintercept', 'ms_aljazeera']},
  'kpis': [['$0', 'Pro-Israel PAC money he took'], ['$8M', 'Pro-Israel PACs spent against him (UDP $4.1M, RJC Victory Fund $3.9M)'], ['$7.4M', 'Trump-aligned MAGA KY spent against him'], ['~$37M', 'Total spent in the race, a House primary record']],
  'sections': [
    {'h': 'His record', 'p': [{'t': 'Massie was consistently one of the few Republicans voting against Israel-related funding and resolutions, and he introduced legislation to require AIPAC to register as a foreign agent. He voted against the 2025 tax-and-spending law, opposed the war with Iran, and pushed to release the Epstein files over the administration\u2019s objections.', 'c': ['ms_theintercept', 'ms_pbs', 'ms_trackaipac']}]},
    {'h': 'Who spent against him', 'p': [{'t': 'AIPAC\u2019s United Democracy Project spent $4.1 million and the RJC Victory Fund $3.9 million against him, $8 million from pro-Israel PACs in all, according to FEC filings. Trump-aligned MAGA KY spent $7.4 million; its top funder is Paul Singer, and it took money from the Adelson-funded Preserve America PAC. Massie named AIPAC, the Republican Jewish Coalition and Christians United for Israel, with individual megadonors, as roughly 95% of the outside money against him. AIPAC described the result as defeating an anti-Israel incumbent.', 'c': ['ms_lpm', 'ms_aj0518', 'ms_notus', 'ms_mee']},
                                     {'t': 'President Trump endorsed Gallrein on October 17, 2025, citing Massie\u2019s opposition to the Iran strikes and his vote against the 2025 tax-and-spending law. AP and others named Trump\u2019s opposition as the key factor in the outcome.', 'c': ['ms_kylantern', 'ms_pbs', 'ms_wapo']}]},
    {'h': 'Why it matters for every page in this guide', 'p': [{'t': 'The money a candidate takes and the votes they cast are connected to what happens when they cross the people paying for campaigns. Massie\u2019s race shows the cost of crossing two forces at once: a President demanding loyalty on his agenda, and the best-funded foreign-policy lobby in American politics. When you see a candidate who voted with the President on every key vote and took the money, this case is the other side of that choice.', 'c': ['ms_theintercept']}]}],
  'discipline': [{'t': 'The record shows both forces spent heavily against him; it does not let anyone separate how much each one decided the result. The outcome was multi-causal, and both causes are named here on purpose.', 'c': ['ms_pbs', 'ms_lpm']},
                 {'t': 'Losing does not prove he was right, and the spending against him does not prove anyone\u2019s motive beyond what the groups said publicly. What it documents is what crossing them cost.', 'c': []}]}}

# ---------- States marked complete (every race has full candidate dossiers) ----------
COMPLETE_STATES = {'AL', 'AK', 'AZ'}
_st = D['states'] if isinstance(D['states'], list) else list(D['states'].values())
_cands = D['cands'] if isinstance(D['cands'], dict) else {c['id']: c for c in D['cands']}
_races = D['races'] if isinstance(D['races'], dict) else {r['id']: r for r in D['races']}
for st in _st:
    if st['code'] in COMPLETE_STATES:
        st['research'] = 'complete'
        for rid, r in _races.items():
            if r['state'] == st['code']:
                r['research'] = 'complete'
                for cid in r['candidates']:
                    if cid in _cands: _cands[cid]['research'] = 'complete'

json.dump(D, open(B + 'data.json', 'w'), ensure_ascii=False, indent=0)
print('cands', len(D['cands']), 'cites', len(CI))
