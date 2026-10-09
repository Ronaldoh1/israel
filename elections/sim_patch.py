"""Adds the 2026 Elections portal to the Israel simulation (idempotent).
- new scene el26_s01 at the end of ch38 (AIPAC Money in the 2026 Election)
- portal tile in ch38's opening scene (ap26_s04)
- .card.portal style, goEl26() bridge into Sophia, deep dives, FAQ, tag, citations"""
import json, re, sys
P = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/Israel-simulationv1.0.html'
s = open(P, encoding='utf-8').read()
SOPHIA_LINK = 'https://bit.ly/sophia-v3#elections2026-card'

def block(s, bid):
    m = re.search(r'(<script[^>]*id="%s"[^>]*>)(.*?)(</script>)' % bid, s, re.S); assert m, bid
    return m
def put(s, bid, obj):
    m = block(s, bid)
    txt = json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return s[:m.start(2)] + txt + s[m.end(2):]

BTN = ('<a class="el26-btn" href="' + SOPHIA_LINK + '" target="_blank" rel="noopener" onclick="return goEl26(event)">'
       'See the 2026 races — who funds each candidate →</a>')
PORTAL_DT = ('<div class="el26-m"><div class="el26-k">LIVE · ELECTION DAY NOVEMBER 3, 2026</div>'
  '<b>Every 2026 Senate and House race, state by state.</b> Each candidate gets a page: who they are, what they propose, their documented record on Israel, and every dollar in their FEC filings — small donors, corporate and other PACs, money bundled through AIPAC PAC, and the super PACs, including United Democracy Project, spending to elect or defeat them.'
  '<div class="el26-h">How it is sourced</div>FEC reports and independent-expenditure filings, court dockets, ethics reports, financial disclosures and the Justice Department’s FARA database [cite:el26_fec] [cite:el26_fara]. Charged is not convicted, a relative’s record is not the candidate’s, and a donation is not a vote.'
  '<div class="el26-h">The score</div>Each candidate is scored 1–5 in quarter points on six published parts: Preparation 10% · Funding independence 25% · Votes for people 25% · Honesty with the public 20% · Conflicts & accountability 15% · Record & transparency 5%. Taking corporate or foreign-policy lobby money — AIPAC included — lowers the funding score at any amount and in any cycle. Sitting members are scored on how their key votes lined up with Sophia’s published positions, each one tied to a documented outcome, applied the same way to both parties.'
  + BTN + '</div>')

PORTAL = dict(id='el26_portal', ty='portal', ic='\U0001F5F3️', nm='2026 Elections: Who Funds Your Candidates',
              rl='Every Senate & House race · claims checked, scored 1–5', dt=PORTAL_DT, pu=1)

SCENE = dict(id='el26_s01', era='YOUR BALLOT', yr='2026', ch='ch38', chn='AIPAC Money in the 2026 Election',
  t='Your Ballot: Who Each Candidate Answers To',
  sub='The money in this chapter, traced to the individual candidates on the November 3 ballot.',
  n='Every figure in this chapter ends up on a specific candidate’s ledger. Sophia’s 2026 Elections module puts each one on its own page, next to who they are and what they have done, with the same score for every party.',
  tld='Campaign money is too tangled for an ordinary voter to follow, so voters have to take candidates at their word.',
  rec='Every federal campaign files its money with the FEC, and every super PAC reports what it spends for or against each candidate. The records are public; the work is putting them on one page per candidate, which is what the 2026 Elections module does [cite:el26_fec] [cite:el26_ie].',
  ents=[
    dict(PORTAL, x=50, y=47),
    dict(id='el26_sources', ty='academic', ic='\U0001F4C2', nm='Where Every Number Comes From', rl='FEC · courts · disclosures · FARA', x=20, y=18,
      dt='Money comes from each campaign’s FEC reports and from Schedule E, where super PACs and other groups report every dollar spent to help or hurt a named candidate [cite:el26_fec] [cite:el26_ie]. AIPAC PAC’s bundled contributions and United Democracy Project’s spending come from their own FEC committee filings [cite:el26_aipacpac] [cite:el26_udp]. Background, legal and financial records come from court dockets, House and Senate ethics reports, personal financial disclosures and the FARA database [cite:el26_fara]. Personal details need two independent sources or one primary record.'),
    dict(id='el26_rubric', ty='academic', ic='⚖️', nm='The 1–5 Score, Fully Published', rl='Six parts · weights shown on every page', x=80, y=18,
      dt='Preparation (10%): years in office, relevant professional work and education, with experience counting more than degrees. Funding independence (25%): flat deductions for ever taking corporate or foreign-policy lobby money (AIPAC included), at any amount and in any cycle, then the size of this cycle’s PAC money, small-donor share and outside spending. Votes for people (25%): for anyone who has voted in Congress, how their key votes lined up with Sophia’s published positions, each tied to a documented outcome. Honesty with the public (20%): a fixed sample of their claims rated against primary records, with extra weight on claims repeated after correction. Conflicts & accountability (15%) and Record & transparency (5%) cover court, ethics and disclosure records. The overall score is the weighted average, rounded to the nearest quarter point.'),
    dict(id='el26_same', ty='event', ic='\U0001F501', nm='Same Rules for Every Party', rl='Democrats, Republicans, independents', x=20, y=80,
      dt='The same sources, the same wording and the same formula apply to every candidate. Corporate PACs, unions, crypto, oil, AIPAC and J Street money all count the same way in the funding score, so the score measures dependence on organized money in general rather than singling out one group. Where pro-Israel money flows to both candidates in a race, both are shown.'),
    dict(id='el26_limits', ty='political', ic='⚠️', nm='What a Donation Does Not Prove', rl='Disclosure is not causation', x=80, y=80,
      dt='A filing shows who chose to fund a campaign. It does not by itself show that the money changed a vote or a position; a page says so only where reporting documents that link. Charges are labelled as charges, not convictions, and a spouse’s or relative’s record is never counted as the candidate’s. The overall score is Sophia’s own published judgment built from documented facts, with all four part scores shown so a reader can recompute it.'),
  ],
  cs=[dict(f='el26_sources', t='el26_portal', ty='causal'), dict(f='el26_rubric', t='el26_portal', ty='causal'),
      dict(f='el26_same', t='el26_portal', ty='formation'), dict(f='el26_limits', t='el26_portal', ty='contested')])

# ---- scenes ----
m = block(s, 'scenedata'); S = json.loads(m.group(2))
ids = {x['id'] for x in S}
if 'el26_s01' not in ids:
    last = max(i for i, x in enumerate(S) if x['ch'] == 'ch38')
    S.insert(last + 1, SCENE)
else:
    S[[i for i, x in enumerate(S) if x['id'] == 'el26_s01'][0]] = SCENE
ch = [x for x in S if x['ch'] == 'ch38']
for i, x in enumerate(ch): x['chpos'] = i + 1; x['chtotal'] = len(ch)
first = next(x for x in S if x['id'] == 'ap26_s04')
first['ents'] = [e for e in first['ents'] if e['id'] != 'el26_portal']
if True:
    first['ents'].append(dict(PORTAL, x=50, y=48))
for e in first['ents']:          # make room for the portal tile in the middle
    if e['id'] == 'what_growth_means': e['x'], e['y'] = 20, 80
    if e['id'] == 'primary_stage':     e['x'], e['y'] = 78, 82
s = put(s, 'scenedata', S)

# CHAPTERS list
cm = re.search(r'(\{"id": "ch38", "name": "AIPAC Money in the 2026 Election", "scenes": \[)([^\]]*)(\])', s); assert cm
if 'el26_s01' not in cm.group(2):
    s = s[:cm.end(2)] + ', "el26_s01"' + s[cm.end(2):]

# ---- citations ----
m = block(s, 'citationdata'); CIT = json.loads(m.group(2))
CIT.update({'el26_fec':'https://www.fec.gov/data/', 'el26_ie':'https://www.fec.gov/data/independent-expenditures/',
            'el26_aipacpac':'https://www.fec.gov/data/committee/C00797670/', 'el26_udp':'https://www.fec.gov/data/committee/C00799031/',
            'el26_fara':'https://efile.fara.gov/ords/fara/f?p=1235:10'})
s = put(s, 'citationdata', CIT)

LBL = {'el26_fec':'FEC — campaign finance data','el26_ie':'FEC — independent expenditures','el26_aipacpac':'FEC — AIPAC PAC filings','el26_udp':'FEC — United Democracy Project filings','el26_fara':'DOJ — FARA database'}
for k, v in LBL.items():
    if '"%s":' % k not in s[s.index('CITE_LABELS = {'):s.index('CITE_LABELS = {') + 400000]:
        s = s.replace('CITE_LABELS = {', 'CITE_LABELS = {' + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False) + ', ', 1)

# ---- deep dives ----
m = block(s, 'deepdive-en'); DD = json.loads(m.group(2))
rub = ('<table class="dd-table"><tr><th>Part</th><th>Weight</th><th>How it is calculated</th></tr>'
  '<tr><td>Preparation</td><td>10%</td><td>Office years, relevant professional work and education (experience counts more than degrees), converted to 1\u20135.</td></tr>'
  '<tr><td>Funding independence</td><td>25%</td><td>Starts at a neutral 3. \u22120.75 for ever taking corporate or industry money and \u22120.75 for ever taking foreign-policy lobby money (AIPAC included), at any amount, in any cycle; +0.75 each only when a complete career search finds none. Then \u22120.25 per 5% of receipts from PACs, party committees and bundling (no cap), small donors (+0.5 at 50%+, \u22120.75 under 10%), and outside spending to help (\u22121 when it exceeds the campaign\u2019s own receipts).</td></tr>'
  '<tr><td>Votes for people</td><td>25%</td><td>For anyone who has voted in Congress: share of scored key votes matching Sophia\u2019s published position, each tied to a documented outcome; missed votes count against. Same positions for both parties.</td></tr>'
  '<tr><td>Honesty with the public</td><td>20%</td><td>Starts at 3. A fixed, rule-chosen claim sample: true +0.25 (up to +2), partly true \u22120.25, misleading \u22120.5, false \u22121, repeated after correction \u22120.5 more, unverifiable claims about their own record \u22120.1. No caps; at least 5 checkable claims required.</td></tr>'
  '<tr><td>Conflicts & accountability</td><td>15%</td><td>Scored only after courts, ethics, disclosures, FARA and certification records are searched. Convictions, civil liability, ethics findings, foreign payments, votes to reject certified election results (both parties) and committee-related stock trades each count, with no caps.</td></tr>'
  '<tr><td>Record & transparency</td><td>5%</td><td>Average of at least two of: missed-vote rate, financial-disclosure timeliness and FEC filing record.</td></tr>'
  '</table><p>Every part except Preparation starts from a neutral 3; unknown is never scored as clean; parts that rest on news-only searches are marked provisional.</p>')
DD.setdefault('el26_s01', {})['el26_portal'] = dict(
  title='2026 Elections: Who Funds Your Candidates', subtitle='Sophia · Collapse pillar · every federal race on the November 3 ballot',
  lead='This chapter follows the money at the level of committees and cycles. The 2026 Elections module follows it to the individual candidate: one page per person, built from public filings, with a score anyone can recompute.',
  sections=[
    dict(heading='What each candidate page shows', body='<p>A 60-second brief generated from the record. Who they are — upbringing, education and career from the public record. Their claims about themselves and their campaign, checked against documents, with claims repeated after correction flagged. What they said against how they voted, and last campaign’s promises against what happened. What they propose, with each position linked to where it was said. Their documented record on Israel: AIPAC endorsement, money bundled through AIPAC PAC, United Democracy Project spending for or against, other pro-Israel PACs, recorded votes and statements. Every dollar in the FEC filings, split into small donors, larger donors, PACs, party money and self-funding, plus outside spending by group and who funds those groups. Stock trades in industries their committees oversee, bills passed, lobbying ties, votes on certifying election results, and whether they face voters in debates and town halls. Foreign business ties and the legal and financial record, with status labels taken from the court or agency record.</p>'),
    dict(heading='The rubric', body=rub + '<p>The overall score is the weighted average, rounded to the nearest quarter point. A candidate is scored only after all four parts have been researched.</p>'),
    dict(heading='Open it', body='<p>' + BTN + '</p>'),
    dict(heading='Discipline — What the Record Shows and Does Not', body='<div class="dd-discipline"><p>The filings show who funded a campaign and who spent around it. They do not by themselves show that money changed any vote or position. The overall score is Sophia’s published judgment built from documented facts; it is not a fact in itself, which is why every part score and weight is shown with it.</p></div>')],
  connections=[dict(scene='ap26_s00', ent='topline', label='→ The $104M topline'), dict(scene='ap26_s02', ent='udp', label='→ AIPAC PAC vs. UDP')])
DD['ap26_s04'] = DD.get('ap26_s04', {}); DD['ap26_s04']['el26_portal'] = DD['el26_s01']['el26_portal']
s = put(s, 'deepdive-en', DD)

# ---- CSS + bridge function ----
CSS = """
.card.portal{border:2px solid #F0B93E;background:linear-gradient(160deg,#16294a 0%,#0d1728 100%);color:#FCF9F2;animation:el26Glow 2.8s ease-in-out infinite}
.card.portal .nm{color:#FFD873}.card.portal .rl{color:#FCF9F2;opacity:.92}.card.portal .badge{background:#F0B93E;color:#0d1728}
@keyframes el26Glow{0%,100%{box-shadow:0 0 0 0 rgba(240,185,62,.55),0 6px 18px rgba(13,23,40,.35)}50%{box-shadow:0 0 0 8px rgba(240,185,62,0),0 6px 26px rgba(240,185,62,.45)}}
@media (prefers-reduced-motion:reduce){.card.portal{animation:none}}
.el26-m{white-space:normal}.el26-k{font:800 11px/1.2 var(--sans,Inter,sans-serif);letter-spacing:.12em;color:#B8791E;margin-bottom:8px}
.el26-h{font:800 12px/1.2 var(--sans,Inter,sans-serif);letter-spacing:.1em;text-transform:uppercase;margin:14px 0 4px;color:#1B2A4A}
.el26-btn{display:block;margin:16px 0 4px;padding:13px 16px;border-radius:999px;background:#F0B93E;color:#0d1728 !important;font:800 14px/1.25 var(--sans,Inter,sans-serif);text-align:center;text-decoration:none;box-shadow:0 4px 14px rgba(240,185,62,.4)}
"""
if '.card.portal{' not in s:
    k = s.index('.card.financial{'); s = s[:k] + CSS.strip() + '\n' + s[k:]
if '.dd-table{' not in s:
    k = s.index('.card.financial{')
    s = s[:k] + '.dd-table{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 10px}.dd-table th,.dd-table td{border-bottom:1px solid rgba(27,42,74,.18);padding:8px 6px;text-align:left;vertical-align:top}.dd-table th{font:800 11px/1.2 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase}\n' + s[k:]
JS = """
// 2026 Elections bridge: inside Sophia, close this simulation and land on the pulsing Collapse card; standalone, the link opens Sophia.
function goEl26(ev){
  try{ if(window.parent && window.parent !== window && typeof window.parent.goElections2026 === 'function'){
    if(ev) ev.preventDefault(); window.parent.goElections2026(false); return false; } }catch(e){}
  return true;
}
window.goEl26 = goEl26;
"""
if 'function goEl26' not in s:
    k = s.index('function showEntity(e){'); s = s[:k] + JS.strip() + '\n' + s[k:]

# ---- FAQ + tag ----
if "el26_s01" not in s[s.index('var RP_FAQ'):s.index('var RP_FAQ') + 4000]:
    FAQ = ("  {q:'Which 2026 candidates take AIPAC, corporate or other PAC money?',\n"
           "   a:'Sophia\\'s 2026 Elections module has a page for every Senate and House candidate on the November 3 ballot, built from FEC filings: small donors, PACs, money bundled through AIPAC PAC, and outside spending such as United Democracy Project\\'s. Each candidate is scored 1–5 on a published rubric, and money from any organized interest counts the same way.',\n"
           "   scenes:['el26_s01','ap26_s00','ap26_s02']},\n")
    s = s.replace('var RP_FAQ = [\n', 'var RP_FAQ = [\n' + FAQ, 1)
if "label:'2026 Midterms'" not in s:
    s = s.replace("var RP_TAGS = [\n", "var RP_TAGS = [\n  {label:'2026 Midterms', kw:['2026 election','2026 elections','midterm','midterms','united democracy project','your ballot']},\n", 1)

open(P, 'w', encoding='utf-8').write(s)
print('ok', len(S), 'scenes')
