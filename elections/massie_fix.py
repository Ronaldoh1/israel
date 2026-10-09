"""Correct every Massie figure in the Israel simulation to the FEC-based record (idempotent).
Sources: Louisville Public Media (Jul 17, 2026, FEC filings): UDP $4.1M, RJC Victory Fund $3.9M (= $8M pro-Israel PACs),
MAGA KY $7.4M, ~$37M total. Al Jazeera (May 18, 2026): MAGA KY's top funder Paul Singer; took Preserve America PAC money.
Kentucky Lantern (Oct 18, 2025): Trump endorsed Gallrein Oct 17, 2025 citing the Iran strikes and the OBBBA vote.
Rolling Stone (Apr 2024): Massie co-sponsored Greene's motion to vacate (he did not file it)."""
import json, re, sys
P = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/Israel-simulationv1.0.html'
s = open(P, encoding='utf-8').read()
def blk(bid):
    m = re.search(r'(<script[^>]*id="%s"[^>]*>)(.*?)(</script>)' % bid, s, re.S); return m
def load(bid): return json.loads(blk(bid).group(2))
def put(bid, obj):
    global s
    m = blk(bid); t = json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + t + s[m.end(2):]

CIT = load('citationdata')
CIT.update({
 'aljazeera_massie_spending_0518': 'https://www.aljazeera.com/news/2026/5/18/massie-race-breaks-spending-record-as-pro-israel-groups-target-trump-critic',
 'kylantern_trump_gallrein': 'https://kentuckylantern.com/?p=34843',
 'rollingstone_massie_vacate': 'https://www.rollingstone.com/politics/politics-news/thomas-massie-marjorie-taylor-greene-bid-oust-mike-johnson-1235005320/'})
put('citationdata', CIT)
LBL = {'aljazeera_massie_spending_0518': 'Al Jazeera — Massie race breaks spending record (May 18, 2026)',
       'kylantern_trump_gallrein': 'Kentucky Lantern — Trump endorses Gallrein (Oct 18, 2025)',
       'rollingstone_massie_vacate': 'Rolling Stone — Massie backs Greene’s motion to oust Johnson (Apr 2024)',
       'lpm_massie_gallrein_funding': 'Louisville Public Media — who funded the $37M Massie-Gallrein race (Jul 17, 2026)'}
for k, v in LBL.items():
    i = s.index('CITE_LABELS = {'); seg = s[i:i + 600000]
    if '"%s":' % k not in seg: s = s.replace('CITE_LABELS = {', 'CITE_LABELS = {' + json.dumps(k) + ': ' + json.dumps(v, ensure_ascii=False) + ', ', 1)

MONEY = ('AIPAC’s super PAC UDP spent $4.1 million and the RJC Victory Fund $3.9 million against him — $8 million from pro-Israel PACs — '
         'while Trump-aligned MAGA KY spent $7.4 million; MAGA KY’s top funder is Paul Singer, and it took money from the Adelson-funded Preserve America PAC.')
SC = load('scenedata')
def ent(sid, eid): return next(e for x in SC if x['id'] == sid for e in x['ents'] if e['id'] == eid)
e = ent('s19', 'mas')
e['rl'] = '$8M pro-Israel PACs · $7.4M MAGA KY'
e['dt'] = ('Rep. Thomas Massie (R-KY-4). Targeted for defeat in his 2026 primary: ' + MONEY + ' '
  'He lost the May 19, 2026 primary to Trump-endorsed Ed Gallrein, 54.9% to 45.1%, in the most expensive House primary on record (about $37 million in all). '
  'IMPORTANT MULTI-CAUSE ANALYSIS: The targeting was not solely about Massie’s Israel-related votes (though he voted against multiple Israel-related packages). '
  'Trump endorsed Gallrein on Oct. 17, 2025, citing Massie’s opposition to the Iran strikes and his vote against the 2025 tax-and-spending law. '
  'The pro-Israel spending converged with Trump’s hostility. Naming both causes is analytical honesty. The convergence itself is the pattern — when a member deviates from BOTH AIPAC AND Trump alignment, they get targeted from both directions at once. '
  '[cite:lpm_massie_gallrein_funding] [cite:aljazeera_massie_spending_0518] [cite:kylantern_trump_gallrein] [cite:opensecrets_udp]')
OLD_S = re.compile(r"with total spending reaching \$32-37 million; pro-Israel groups, including AIPAC's United Democracy Project, contributed a documented \$9-9\.4 million specifically against Massie, alongside substantial Trump-aligned spending( \(MAGA KY alone spent \$7\.4 million\))?\.")
NEW_S = ('with about $37 million spent in all; pro-Israel groups spent $8 million against Massie — $4.1 million from AIPAC’s United Democracy Project and $3.9 million from the RJC Victory Fund — '
         'alongside $7.4 million from Trump-aligned MAGA KY, whose top funder is Paul Singer.')
m2 = ent('s19c', 'massie'); m2['dt'] = OLD_S.sub(NEW_S, m2['dt'])
if '[cite:aljazeera_massie_spending_0518]' not in m2['dt']: m2['dt'] += ' [cite:aljazeera_massie_spending_0518]'
c9 = ent('cm_s09', 'cm9_massie')
c9['dt'] = ('Most expensive House primary ever (about $37M in all; $32.6M in ads). Pro-Israel PACs spent $8M against him (UDP $4.1M, RJC Victory Fund $3.9M), and pro-Israel groups bought about half the advertising backing Gallrein, per AdImpact. '
            'AIPAC: ‘defeating anti-Israel incumbent.’ [cite:pbs_massie_takeaways] [cite:lpm_massie_gallrein_funding] [cite:notus_massie_money] [cite:mee_massie_aipac]')
put('scenedata', SC)

DD = load('deepdive-en')
d = DD['s19']['mas']
d['subtitle'] = ('KY-4 Republican primary, May 19, 2026. $8M from pro-Israel PACs and $7.4M from Trump-aligned MAGA KY in the most expensive House primary on record. '
                 'Massie lost, 54.9% to 45.1%. Both forces are on the record.')
d['lead'] = ('Thomas Massie represented Kentucky’s 4th district from 2012. In 2026 he faced the most expensive U.S. House primary ever recorded, about $37 million in all. '
             'Two documented forces were arrayed against him: $8 million from pro-Israel PACs (AIPAC’s United Democracy Project and the RJC Victory Fund), and President Trump, who endorsed his challenger and whose allies’ super PAC, MAGA KY, spent $7.4 million. '
             'He lost. Attributing the result to AIPAC alone would overstate the case; attributing it entirely to Trump would understate it.')
d['sections'] = [
 {'heading': 'The Congressman', 'body':
  '<div class="dd-timeline">'
  '<div class="dd-timeline-item"><div class="dd-timeline-date">2012</div><div class="dd-timeline-body">MIT-trained engineer and former Lewis County Judge-Executive; wins the KY-4 House seat.</div></div>'
  '<div class="dd-timeline-item"><div class="dd-timeline-date">2012–2025</div><div class="dd-timeline-body">Among the most consistent libertarian-Republican votes in the House, frequently voting no on foreign aid packages, surveillance authorizations and Israel-related resolutions.</div></div>'
  '<div class="dd-timeline-item"><div class="dd-timeline-date">Apr 2024</div><div class="dd-timeline-body">Co-sponsors Rep. Marjorie Taylor Greene’s motion to remove Speaker Mike Johnson. [cite:rollingstone_massie_vacate]</div></div>'
  '<div class="dd-timeline-item"><div class="dd-timeline-date">2025</div><div class="dd-timeline-body">Votes against the One Big Beautiful Bill Act, opposes the strikes on Iran, and pushes to release the Epstein files. Introduces a bill to require AIPAC to register as a foreign agent.</div></div>'
  '<div class="dd-timeline-item"><div class="dd-timeline-date">Oct 17, 2025</div><div class="dd-timeline-body">Trump endorses Ed Gallrein, saying Massie “only votes against the Republican Party.” [cite:kylantern_trump_gallrein]</div></div>'
  '<div class="dd-timeline-item"><div class="dd-timeline-date">May 19, 2026</div><div class="dd-timeline-body"><strong>Loses the primary to Gallrein, 54.9% to 45.1%.</strong> [cite:theintercept_massie_loses_2026]</div></div></div>'},
 {'heading': 'The Spending — What the FEC Filings Show', 'body':
  '<p>Totals from FEC filings, as compiled by Louisville Public Media in July 2026 and Al Jazeera in May 2026:</p>'
  '<table class="dd-compare"><thead><tr><th>Spender</th><th>Amount</th><th>Note</th></tr></thead><tbody>'
  '<tr><td class="dd-attr">United Democracy Project (AIPAC)</td><td>$4.1M</td><td>Mostly attack ads against Massie</td></tr>'
  '<tr><td class="dd-attr">RJC Victory Fund</td><td>$3.9M</td><td>Mostly positive ads for Gallrein</td></tr>'
  '<tr><td class="dd-attr">Pro-Israel PACs combined</td><td><strong>$8M</strong></td><td>UDP + RJC Victory Fund</td></tr>'
  '<tr><td class="dd-attr">MAGA KY</td><td>$7.4M</td><td>Trump-aligned; top funder Paul Singer; took money from the Adelson-funded Preserve America PAC</td></tr>'
  '<tr><td class="dd-attr">Whole race</td><td>about $37M</td><td>Most expensive House primary on record</td></tr></tbody></table>'
  '<p>Al Jazeera added UDP, the RJC Victory Fund and MAGA KY together for a combined $15.5 million from three pro-Israel-linked PACs. Earlier versions of this simulation reported $15.8 million and $9–9.4 million; both are replaced here by the FEC-based figures. [cite:lpm_massie_gallrein_funding] [cite:aljazeera_massie_spending_0518]</p>'},
 {'heading': 'The Trump Co-Cause — What Must Be Preserved', 'body':
  '<p>Attributing the result entirely to AIPAC would be inaccurate. Trump endorsed Gallrein seven months before the primary, citing Massie’s opposition to the Iran strikes and his vote against the 2025 tax law, and AP and others named Trump’s opposition as the key factor in the outcome. [cite:kylantern_trump_gallrein] [cite:pbs_massie_takeaways]</p>'
  '<aside class="dd-callout"><strong>Convergence, not a single hidden hand</strong>Two documented forces: $8 million from pro-Israel PACs, which AIPAC described as “defeating anti-Israel incumbent Thomas Massie,” and the President’s endorsement plus a $7.4 million allied super PAC. Both are real and both are material. The record does not let anyone separate how much each one decided the result.</aside>'},
 {'heading': 'What the Republican-Side Targeting Shows', 'body':
  '<ul><li><strong>The mechanism is not partisan.</strong> The same primary-spending tool used against Democrats Jamaal Bowman and Cori Bush in 2024 was used against a Republican incumbent in 2026.</li>'
  '<li><strong>The deterrent is now on the record.</strong> Every member who criticizes AIPAC by name can see what the most prominent Republican critic faced.</li>'
  '<li><strong>Insulation has limits.</strong> Massie survived for years on small donors and district loyalty; record spending combined with a sitting President’s opposition ended that.</li></ul>'},
 d['sections'][5] if len(d['sections']) > 5 and d['sections'][5]['heading'].startswith('Effects') else {'heading': 'Effects on Palestine and the Region', 'body': ''},
 {'heading': 'Discipline — Preserving Both Drivers', 'body':
  '<div class="dd-discipline"><strong class="dd-disc-label">What the Massie case demands</strong>'
  '<p>Documented: pro-Israel PACs spent $8 million against Massie; Trump endorsed his challenger; an allied super PAC spent $7.4 million; he lost 54.9% to 45.1%.</p>'
  '<p>Refused: framing this as sole-cause AIPAC. Trump’s endorsement and public attacks are independently sufficient causes.</p>'
  '<p>Also refused: framing this as sole-cause Trump. $8 million from pro-Israel PACs against a member who criticized AIPAC by name and filed a bill to make it register as a foreign agent is not incidental. With Bowman ($14.5M in 2024) and Bush ($8.5M in 2024), the pattern is systematic.</p>'
  '<p>The disciplined statement: both drivers operated, both are documented, and the outcome was over-determined. Every single-cause attribution understates the actual architecture.</p></div>'}]
d['sections'] = [x for x in d['sections'] if x.get('body')]
d['connections'] = [c if c.get('ent') != 'udp' else {'scene': 's19', 'ent': 'udp', 'label': 'UDP Super PAC — $4.1M against Massie'} for c in d.get('connections', [])]

def fix_text(t):
    t = t.replace('In 2026 cycle, Thomas Massie (R-KY) faces $15.8M primary spending — though the Trump-Massie feud is a documented co-cause, so causal attribution to AIPAC alone',
                  'In 2026, Thomas Massie (R-KY) faced $8M from pro-Israel PACs (UDP $4.1M, RJC Victory Fund $3.9M) and lost his primary — though Trump’s endorsement of his challenger is a documented co-cause, so causal attribution to AIPAC alone')
    t = t.replace('<div class="dd-timeline-date">2026 cycle (in progress)</div><div class="dd-timeline-body">UDP-linked spending has already exceeded prior cycles. Massie targeting in KY-4 reaches <strong>$15.8M</strong> — the most expensive single House primary in US history, though the Trump feud is a documented co-cause',
                  '<div class="dd-timeline-date">2026 cycle</div><div class="dd-timeline-body">UDP spent <strong>$4.1M</strong> against Massie in KY-4 (with the RJC Victory Fund, $8M from pro-Israel PACs) in the most expensive House primary on record; he lost on May 19. Trump’s endorsement of his challenger is a documented co-cause')
    t = t.replace('Massie 2026 targeting — $15.8M, but Trump feud is co-cause', 'Massie 2026 — $8M from pro-Israel PACs; Trump’s endorsement a co-cause')
    return t
def walk(o):
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list): return [walk(v) for v in o]
    if isinstance(o, str): return fix_text(o)
    return o
for k in ('aipac', 'udp'):
    DD['s19'][k] = walk(DD['s19'][k])
mm = DD.get('s19c', {}).get('massie')
if mm:
    for sec in mm['sections']: sec['body'] = OLD_S.sub(NEW_S, sec['body'])
put('deepdive-en', DD)

AR = load('i18n-ar')
a = AR['scenes']['s19']['ents']['mas']
a['rl'] = '8 ملايين دولار من لجان مؤيدة لإسرائيل · 7.4 مليون من MAGA KY'
a['dt'] = ('النائب توماس ماسي (جمهوري، الدائرة 4 في كنتاكي). استُهدف لإسقاطه في انتخاباته التمهيدية عام 2026: أنفقت لجنة UDP التابعة لأيباك 4.1 مليون دولار وصندوق RJC Victory Fund 3.9 مليون دولار ضده — أي 8 ملايين دولار من لجان مؤيدة لإسرائيل — '
           'بينما أنفقت لجنة MAGA KY المتحالفة مع ترامب 7.4 مليون دولار؛ وأكبر مموليها بول سينغر، وتلقت أموالًا من لجنة Preserve America التي تموّلها عائلة أديلسون. '
           'خسر ماسي الانتخابات التمهيدية في 19 مايو 2026 أمام إد غالراين المدعوم من ترامب بنسبة 54.9% مقابل 45.1%، في أغلى انتخابات تمهيدية لمجلس النواب على الإطلاق (نحو 37 مليون دولار). '
           'تحليل مهم متعدد الأسباب: لم يكن الاستهداف بسبب تصويته في القضايا المتعلقة بإسرائيل وحده؛ فقد أيّد ترامب منافسه في 17 أكتوبر 2025 مستشهدًا بمعارضة ماسي للضربات على إيران وتصويته ضد قانون الضرائب والإنفاق لعام 2025. '
           'تلاقى الإنفاق المؤيد لإسرائيل مع عداء ترامب، وتسمية السببين معًا هي الأمانة التحليلية. [cite:lpm_massie_gallrein_funding] [cite:aljazeera_massie_spending_0518] [cite:kylantern_trump_gallrein]')
am = AR['scenes'].get('s19c', {}).get('ents', {}).get('massie')
if am:
    am['dt'] = re.sub(r'إذ بلغ إجمالي الإنفاق 32-37 مليون دولار؛ وأسهمت جماعات مؤيدة لإسرائيل، منها «مشروع الديمقراطية المتحدة» التابع لأيباك، بمبلغ موثّق قدره 9-9\.4 مليون دولار ضد ماسي تحديدًا، إلى جانب إنفاق كبير من جهات متحالفة مع ترامب \(أنفقت MAGA KY وحدها 7\.4 مليون دولار\)\.',
                      'إذ بلغ إجمالي الإنفاق نحو 37 مليون دولار؛ وأنفقت جماعات مؤيدة لإسرائيل 8 ملايين دولار ضد ماسي — 4.1 مليون من «مشروع الديمقراطية المتحدة» التابع لأيباك و3.9 مليون من صندوق RJC Victory Fund — إلى جانب 7.4 مليون دولار من لجنة MAGA KY المتحالفة مع ترامب، وأكبر مموليها بول سينغر.', am['dt'])
put('i18n-ar', AR)

open(P, 'w', encoding='utf-8').write(s)
left = [p for p in ['15.8M', '$15.8', '9-9.4', '9–9.4'] if p in s]
print('remaining old figures:', left)
