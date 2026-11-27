"""Volume II, Appendix Three: The Architecture in Code. Writes book/part1/rdc/."""
import os, re, json, html
B = '/home/claude/israel/book/part1/rdc/'
os.makedirs(B, exist_ok=True)
MAP = '<a href="road-network.html">network map</a>'

KW = r'@implementation|@interface|@property|@end|@selector|@protocol|return|for|in|int|void|static|id|self|nil|YES|NO|if|else|strong|class'
def hl(code):
    out = []
    for line in code.strip('\n').split('\n'):
        m = re.search(r'//.*$', line)
        body, com = (line[:m.start()], line[m.start():]) if m else (line, '')
        parts = re.split(r'(@"(?:[^"\\]|\\.)*")', body)
        res = ''
        for i, p in enumerate(parts):
            if i % 2:
                res += '<span class="s">' + html.escape(p) + '</span>'; continue
            e = html.escape(p)
            e = re.sub(r'(?<![\w@])(' + KW + r')(?![\w])', r'<span class="k">\1</span>', e)
            e = re.sub(r'(?<![\w>"#])([A-Z][A-Za-z0-9_]+)(?![\w])', r'<span class="t">\1</span>', e)
            e = re.sub(r'\b(\d[\d.,]*)\b(?![^<]*>)', r'<span class="n">\1</span>', e)
            e = re.sub(r'(?<=[ \[])([a-z][A-Za-z0-9_]*):', r'<span class="m">\1</span>:', e)
            res += e
        if com: res += '<span class="c">' + html.escape(com) + '</span>'
        out.append(res)
    return '\n'.join(out)

def panel(fname, cap, code, plain, cites):
    ps = ''.join('<p>' + p + '</p>' for p in plain)
    return (f'<figure class="fig-code"><figcaption>{cap}</figcaption><div class="cbar"><i></i><i></i><i></i><b>{fname}</b></div>'
            f'<pre>{hl(code)}</pre><div class="plain"><h5>In plain language</h5>{ps}</div>'
            f'<p class="fig-src">Sources: {" ".join("[cite:" + c + "]" for c in cites)}</p></figure>')

F = {}
F['_intro.html'] = f"""<p>This appendix shows the architecture of the road to 1948 in two other languages: code and diagrams. The code is Objective-C, the language Apple's software was written in for three decades, whose runtime lets a program change its own behaviour while it runs. Its techniques have names for things institutions do: run before anyone can object, keep a label while changing what it does, speak through an intermediary, route everything through one gateway, extend a scope without ever redrawing it.</p>
<p>Nothing here is new evidence. Every fact in the code comes from the stages of this volume, with its source, and every block of code is followed by the same thing in plain language. The code is a way of seeing the structure; the record is the evidence. The appendix ends with two diagrams, the institutions and their documented ties, and the whole system on one page, and with a list of what the code does not claim.</p>"""
F['_outro.html'] = f"""<p>Read as code, the road to 1948 has a recognisable shape. The program was installed before the people it concerned were asked; its public label stayed a "home" while its implementation became a state; one recognised agency stood between the empire and the movement; the money ran through one bank; and each new line on the map inherited the last without redrawing it. [cite:zionism_founding_1897] [cite:balfour_letter] [cite:rs_md_avalon]</p>
<p>None of that is hidden code or a secret plan. Each step is in a published document, and each is dated and sourced in the stages of this volume. The code is a lens on what the record shows, and the {MAP} is where it can be tested.</p>"""

F['rdc_key.html'] = """<h2>How to Read the Code</h2>
<p>Each section takes one technique from the Objective-C runtime, shows it at work on one documented part of the road, and translates it back. Five techniques are used, one per mechanism, and the last code section runs them together as one program.</p>
<figure class="fig-compare">
<figcaption>The five techniques and what each names in the record</figcaption>
<table>
<thead><tr><th>Technique</th><th>What it does in software</th><th>What it names on the road to 1948</th></tr></thead>
<tbody>
<tr><td><code>+load</code></td><td>Runs as the program loads, before any of its own code can opt in or object</td><td>Commitments installed before the people they concerned had any say: Basel, Balfour, the Mandate</td></tr>
<tr><td>Method swizzling</td><td>Keeps a method's public name while swapping what it does</td><td>A "home" in the public language, a state in the program</td></tr>
<tr><td><code>NSProxy</code></td><td>An object that stands in for another and forwards every message to it</td><td>The Jewish Agency, recognised by the Mandate, standing between the government and the movement</td></tr>
<tr><td><code>objc_msgSend</code></td><td>The one function every message passes through</td><td>One bank carrying the movement's money</td></tr>
<tr><td>Inheritance without override</td><td>A new class takes everything from the old one and changes nothing it was given</td><td>Partition, the armistice lines and 1967, each built on the last</td></tr>
</tbody>
</table>
<p class="fig-src">Technique names are those of Apple's Objective-C runtime. The mechanisms are documented in the stages of this volume.</p>
</figure>
<p>Two rules hold throughout. The metaphor illuminates and never replaces: where the code and the record differ, the record wins. And the code describes structures, not intentions: a technique that fits what an institution did says nothing about what anyone privately meant.</p>"""

F['rdc_load.html'] = "<h2>+load: Installed Before Anyone Could Object</h2>\n<p>In Objective-C, a class's <code>+load</code> method runs as the program starts, before the program's own code has run a single line. Nothing written later can stop it; by the time the program begins, the class is already in place.</p>\n" + panel(
 'MandatePalestine.m', 'The founding commitments, loaded before the population was consulted',
 r'''
@implementation MandatePalestine

+ (void)load {
  // 29-31 Aug 1897, Basel
  [ZionistOrg adopt:
    @"a home in Palestine"];
    // "secured under public law"

  // 2 Nov 1917: a cabinet letter
  // addressed to Lord Rothschild
  [BritishCabinet declare:
    @"a national home"];
    // "for the Jewish people"

  // 1922: written into the Mandate
  [Mandate article:2
    duty:@"secure the national home"];
  [Mandate article:4
    recognise:JewishAgency.class];
  [Mandate article:6
    duty:@"facilitate immigration"];
}

@end

int main(void) {
  // Aug 1922, Nablus: the majority
  // answers only now
  [ArabCongress
    boycott:LegislativeCouncil];
  // 1923: members to be chosen by
  // the High Commissioner; rejected
  [Britain offer:ArabAgency];
  return 0;  // already loaded
}
''',
 ['The programme was adopted at Basel in 1897, the promise made by a British cabinet in 1917, and both were written into the Mandate in 1922: Article 2 made Britain responsible for securing the national home, Article 4 recognised a Jewish agency as a public body, and Article 6 required Britain to facilitate Jewish immigration.',
  'Palestine\'s Arabs, about nine-tenths of the population, had not been asked. Their answer came afterwards, at the Fifth Palestine Arab Congress in Nablus in August 1922, which boycotted the elections to the Legislative Council; Britain then offered an "Arab Agency" whose members its High Commissioner would choose. The framework was already in force.'],
 ['zionism_founding_1897', 'balfour_letter', 'rs_md_avalon', 'rs_lc_cojs_boycott', 'rs_lc_albright', 'rs_lc_cojs_arabagency']) + """
<p>This is the first link of the case set out in The Case: the commitments that carried the movement were made in London and Geneva, about a country whose majority had no part in making them. [cite:balfour_letter]</p>"""

F['rdc_swizzle.html'] = "<h2>Method Swizzling: A Home That Ran as a State</h2>\n<p>Swizzling swaps the code behind a method while its name stays the same. Every caller still asks for the same thing and gets something different, and nothing on the surface changes.</p>\n" + panel(
 'NationalHome.m', 'The public word and the program behind it',
 r'''
@implementation NationalHome
- (void)build {
  // the published word: a "home"
  // (Basel 1897, Balfour 1917)
}
- (void)build_state {
  // the programme of Herzl's
  // The Jewish State, 1896
}
@end

static void install(void) {
  Method home = class_getInstanceMethod(
    NationalHome.class,
    @selector(build));
  Method state = class_getInstanceMethod(
    NationalHome.class,
    @selector(build_state));
  method_exchangeImplementations(
    home, state);
}

// 1922 White Paper: not "as Jewish
//   as England is English"
//   -> the label holds
// 1942 Biltmore: "a Jewish
//   Commonwealth"
//   -> the program shows
// 1948 [nationalHome build]
//   returns a State
''',
 ['Herzl\'s pamphlet of 1896 was called The Jewish State and argued for one. The programme adopted at Basel a year later asked instead for "a home", and the Balfour letter of 1917 promised a "national home". In 1922 Britain\'s White Paper stated that Palestine would not become "as Jewish as England is English."',
  'In May 1942 the Biltmore Program called openly for a "Jewish Commonwealth", the movement\'s first explicit public demand for statehood, best read as the culmination of the institution-building before it rather than its start. Six years later the "home" was a state.',
  'The swap was not secret: Herzl\'s title was public from the start. What the technique names is the documented gap between the word used in public commitments and the program those commitments carried.'],
 ['herzl_judenstaat_1896', 'zionism_founding_1897', 'balfour_letter', 'wiki_churchill_wp_1922', 'biltmore_wiki', 'biltmore_medoff'])

F['rdc_proxy.html'] = "<h2>NSProxy: The Agency in Between</h2>\n<p>An <code>NSProxy</code> is an object that is not the real thing. It stands in for another object and forwards every message it receives to that object. Whoever talks to the proxy is really talking to what stands behind it.</p>\n" + panel(
 'JewishAgency.m', 'One recognised body between the Mandate government and the movement',
 r'''
@interface JewishAgency : NSProxy
// the Zionist Organization;
// the Agency itself from 1929
@property (strong) id target;
@end

@implementation JewishAgency
- (void)forwardInvocation:
    (NSInvocation *)call {
  [call invokeWithTarget:self.target];
}
@end

// The Administration addresses it...
[mandateGov consult:jewishAgency
  on:@"the national home"]; // Art. 4
[mandateGov arrange:jewishAgency
  for:@"public works"];     // Art. 11

// ...and it forwards to the movement
// and the force it commanded:
[jewishAgency command:Haganah];
  // parity command from 1931
[jewishAgency.chairman declareState];
  // Ben-Gurion, 14 May 1948
''',
 ['Article 4 of the Mandate recognised "an appropriate Jewish agency" as a public body to advise and cooperate with the Administration, and Article 11 let the Administration make arrangements with it for public works. The Zionist Organization filled the role, and the Jewish Agency proper was established in 1929.',
  'The Haganah came under a parity command in 1931. David Ben-Gurion, chairman of the Jewish Agency Executive and the de facto head of the Jewish community of Palestine, declared the state on 14 May 1948. The body the Mandate recognised as its partner became the state\'s government in waiting.',
  'There was no Arab equivalent. Britain offered an Arab Agency in 1923, with members its High Commissioner would choose, and the offer was rejected in October 1923.'],
 ['rs_md_avalon', 'wiki_palestine_office', 'rs_rd3_ej_haganah', 'mexico_arms_1948', 'rs_rd5_jvl_declaration', 'rs_lc_cojs_arabagency'])

F['rdc_dispatch.html'] = "<h2>objc_msgSend: One Bank for the Movement's Money</h2>\n<p>In Objective-C every message between objects passes through one function, <code>objc_msgSend</code>. Whoever controls that function controls every call.</p>\n" + panel(
 'MovementBank.m', 'The money ran through one institution',
 r'''
// 1899 the Jewish Colonial Trust:
//      the movement's bank
// 1902 its Palestine arm, later the
//      Anglo-Palestine Bank
id objc_msgSend(id bank, SEL op, ...);

for (Transfer *t in movementMoney) {
  objc_msgSend(AngloPalestineBank,
    @selector(settle:), t);
}

// 1933-39 Haavara: about 105 million
//   Reichsmarks of German goods
objc_msgSend(AngloPalestineBank,
  @selector(settle:), haavara);

// 1950-51 renamed Bank Leumi
''',
 ['The Jewish Colonial Trust was founded as the movement\'s bank, and its Palestine company became the Anglo-Palestine Bank around 1930 and Bank Leumi in 1950–51. The Anglo-Palestine Bank carried the movement\'s money under the Mandate.',
  'The transfer agreement of 1933 with Nazi Germany, Haavara, moved about 105 million Reichsmarks of German goods by the outbreak of war, about 15 percent of all the documented money on the network map. On the map, taking all the money out leaves no state; taking out the Rothschilds\' money alone cuts the chance in 1948 to about 36 percent.'],
 ['jewishencyclopedia_colonial_trust', 'apc_wiki', 'wiki_palestine_pound', 'wiki_haavara_agreement', 'rs_rd3_frus1939_d828'])

F['rdc_inherit.html'] = "<h2>Inheritance Without Override: Each Line Built on the Last</h2>\n<p>A subclass inherits everything from the class above it. If it overrides nothing, every limit the parent set still stands on paper and none of them is applied; the new class simply adds what it does.</p>\n" + panel(
 'TheLines.m', 'Partition, armistice and occupation as a chain of classes',
 r'''
@interface FoundingScope : NSObject
// Balfour, 1917
- (void)protectRightsOf:
    (id)existingNonJewishCommunities;
@end

// 1947: about 55-56% of the land
@interface Partition181
  : FoundingScope @end
// 1949: about 78%
@interface Armistice1949
  : Partition181 @end
// 1967: the rest (Stage Seven)
@interface Occupation1967
  : Armistice1949 @end

// No subclass overrides
// -protectRightsOf:
// Every class inherits the clause;
// none calls it.
''',
 ['The Balfour letter promised that nothing would be done to prejudice "the civil and religious rights of existing non-Jewish communities." Resolution 181 in 1947 gave the proposed Jewish state about 55 to 56 percent of the territory, when land in Jewish ownership was about 7 percent. By the armistices of 1949 about 78 percent of Mandate Palestine was under Israeli control, and in June 1967 Israel took the rest.',
  'Each line was built on the one before and none was formally redrawn by those who held the land. Roughly 700,000 to 750,000 Palestinians were displaced in the war of 1947–49, and the clause about their rights stayed in the founding letter.'],
 ['balfour_letter', 'britannica_res181', 'rs_rd5_yusuf_2002', 'morris_1948', 'rs_rd6_mfa_armistice_map', 'wiki_six_day_war', 'wiki_nakba'])

F['rdc_program.html'] = f"<h2>The Whole Program</h2>\n<p>The five techniques ran at the same time, inside one larger structure: a state needs money, land, people, arms, diplomacy, organisation and recognition, and the {MAP} treats each as necessary. Written as one program, with the map's own results as its output:</p>\n" + panel(
 'Road1948.m', 'The road to 1948 as one program, with the network map\'s results',
 r'''
int main(void) {
  [MandatePalestine load];
  [NationalHome install];
  id agency = [JewishAgency
    proxyFor:zionistOrganization];
  route(movementMoney,
        AngloPalestineBank);

  double chance = 1.0;
  for (Channel *c in @[money, land,
        people, arms, diplomacy,
        organisation, recognition]) {
    chance *= [c strength];
    // any channel at zero: no state
  }
  NSLog(@"State in 1948: %.0f%%",
        chance * 100);
  return 0;
}

// Output on the record, 26 Nov 2026
// full record ............ 93%
// no money ...............  0%
// no armed groups ........  0%
// no Rothschilds ......... 34%
// no British backing ..... 36%
// no United States ....... 25%
// no immigrants .......... 17%
//   (every power kept)
// no great power .........  1%
''',
 ['The map counts what a state needed and multiplies the parts, so the absence of any one of them is fatal. On the full record the chance of a state in 1948 is about 93 percent. Take away all the money or all the armed groups and it is zero; take away the Rothschilds and it falls to about a third; take away British backing or the United States and it falls further.',
  'It also limits the case: without the immigrants, with every power kept, the chance is 17 percent. The powers did not found the state alone; the people who came through the door they held open were needed too.'],
 ['zionism_founding_1897', 'balfour_letter', 'pp_mandate_text']) + f"""
<p>The tests are live on the {MAP}, under Tests, where each can be run and read in full.</p>"""

# entity diagram: 2 columns x 5 rows, long ties routed in the right gutter
W, bw, bh, gx, gy, top = 404, 166, 84, 34, 44, 10
xl, xr = 4, 4 + 166 + 34
def box(x, y, cls, name, lines):
    t = f'<g class="eb {cls}"><rect class="b" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6"/><rect class="h" x="{x}" y="{y}" width="{bw}" height="24" rx="6"/><rect class="h" x="{x}" y="{y+14}" width="{bw}" height="10"/>'
    t += f'<text class="hn" x="{x+8}" y="{y+16.5}">{html.escape(name)}</text>'
    for i, l in enumerate(lines):
        t += f'<text x="{x+8}" y="{y+41+i*15.5}">{html.escape(l)}</text>'
    return t + '</g>'
def ry(r): return top + r * (bh + gy)
boxes = [
 (xl, ry(0), 'pw', 'British Cabinet', ['Balfour letter, 1917', 'to Lord Rothschild', 'majority not asked']),
 (xr, ry(0), '', 'Zionist Organization', ['founded at Basel, 1897', 'program: "a home"', 'funds and bank, 1899-1920']),
 (xl, ry(1), 'pw', 'Mandate government', ['in force 1923-1948', 'Art. 2: national home', 'Art. 6: immigration']),
 (xr, ry(1), '', 'Jewish Agency', ['recognised by Art. 4', 'established 1929', 'chairman: Ben-Gurion']),
 (xl, ry(2), '', 'Edmond de Rothschild', ['colonies from 1882', 'land company PICA', '36% of mapped money']),
 (xr, ry(2), '', 'Funds and bank', ['JNF, Keren Hayesod', 'Anglo-Palestine Bank', 'Haavara, 1933-39']),
 (xl, ry(3), 'pw', 'UN General Assembly', ['Resolution 181, 1947', 'Jewish state: 55-56%', 'Jewish-owned land: ~7%']),
 (xr, ry(3), '', 'Haganah', ['founded June 1920', 'parity command, 1931', 'held by 1949: ~78%']),
 (xl, ry(4), 'pw', 'US government', ['UN vote, Nov 1947', 'recognition, 14 May 1948', '11 minutes after']),
 (xr, ry(4), 'st', 'State of Israel', ['declared 14 May 1948', 'by the Agency chairman', '700,000+ displaced']),
]
cx = lambda x: x + bw / 2
H = ry(4) + bh + 8
R = xr + bw
rels = [
 (f'M{cx(xl)} {ry(0)+bh} V{ry(1)}', (cx(xl), ry(0)+bh+gy/2), 1, ''),
 (f'M{xl+bw} {ry(1)+bh/2} H{xr}', (xl+bw+gx/2, ry(1)+bh/2), 2, ''),
 (f'M{cx(xr)} {ry(0)+bh} V{ry(1)}', (cx(xr), ry(0)+bh+gy/2), 3, ''),
 (f'M{R} {ry(0)+bh*0.3} H{R+12} V{ry(2)+bh*0.3} H{R}', (R+12, ry(1)+bh*0.15), 4, ''),
 (f'M{xl+bw} {ry(2)+bh/2} H{xr}', (xl+bw+gx/2, ry(2)+bh/2), 5, 'mn'),
 (f'M{R} {ry(1)+bh*0.75} H{R+26} V{ry(3)+bh*0.5} H{R}', (R+26, ry(2)+bh*0.62), 6, ''),
 (f'M{xl+bw} {ry(3)+bh*0.8} L{xr} {ry(4)+bh*0.2}', (xl+bw+gx/2, (ry(3)+bh*0.8+ry(4)+bh*0.2)/2), 7, ''),
 (f'M{cx(xr)} {ry(3)+bh} V{ry(4)}', (cx(xr), ry(3)+bh+gy/2), 8, ''),
 (f'M{xl+bw} {ry(4)+bh/2} H{xr}', (xl+bw+gx/2, ry(4)+bh/2), 9, ''),
]
svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Entity diagram of the institutions on the road to 1948 and their documented ties">'
for p, _, n, c in rels: svg += f'<path class="rl {c}" d="{p}"/>'
for b in boxes: svg += box(*b)
for _, (x, y), n, c in rels: svg += f'<g class="rn"><circle cx="{x}" cy="{y}" r="9"/><text x="{x}" y="{y+4}" text-anchor="middle">{n}</text></g>'
svg += '</svg>'
items = [
 'British Cabinet → Mandate government: the Balfour letter was written into the Mandate, whose Article 2 made Britain responsible for the national home. [cite:balfour_letter] [cite:rs_md_avalon]',
 'Mandate government ↔ Jewish Agency: Article 4 recognised a Jewish agency as a public body to advise and cooperate with the Administration; Article 11 allowed arrangements with it for public works. [cite:rs_md_avalon]',
 'Zionist Organization → Jewish Agency: the Organization served as the recognised agency, and the Jewish Agency proper was established in 1929. [cite:wiki_palestine_office]',
 'Zionist Organization → funds and bank: the Jewish Colonial Trust, its Palestine bank (later the Anglo-Palestine Bank), the Jewish National Fund and Keren Hayesod. [cite:jewishencyclopedia_colonial_trust] [cite:apc_wiki]',
 'Edmond de Rothschild → the land and the colonies (dashed red: money): from 1882, through his own administration and later the land company PICA, separate from the Organization\'s funds; about 36 percent of all documented money on the map. [cite:rs_rd0_ej_edmond]',
 'Jewish Agency → Haganah: the armed force came under a parity command in 1931. [cite:rs_rd3_ej_haganah]',
 'UN General Assembly → State of Israel: Resolution 181 of November 1947 gave the proposed Jewish state about 55 to 56 percent of the territory. [cite:britannica_res181] [cite:rs_rd5_yusuf_2002]',
 'Haganah → State of Israel: by the armistices of 1949 about 78 percent of Mandate Palestine was under Israeli control; roughly 700,000 to 750,000 Palestinians had been displaced. [cite:morris_1948] [cite:wiki_nakba]',
 'US government → State of Israel: the United States extended de facto recognition eleven minutes after Ben-Gurion declared the state on 14 May 1948. [cite:trumanlibrary_recognition] [cite:rs_rd5_jvl_declaration]',
]
F['rdc_entities.html'] = f"""<h2>The Institutions as Entities</h2>
<p>An entity diagram draws each institution as a box with its key attributes, and each documented tie as a numbered line. On the left are the powers: the British cabinet, the Mandate government, the United Nations and the American government. On the right is the movement and what it built. The red box at the end is the state.</p>
<figure class="fig-erd"><figcaption>The road to 1948 as entities and documented ties</figcaption>{svg}
<ol class="rels">{''.join('<li>' + x + '</li>' for x in items)}</ol></figure>
<p>Read down the right column and the movement builds its own institutions; read across and each step depends on a power on the left. That is the shape the {MAP} measures: the movement and the powers together, neither alone.</p>"""

F['rdc_system.html'] = f"""<h2>The System on One Page</h2>
<p>The same road as a layered system: what went in, the institutions that carried it, the decisions that made it law, and what came out in 1948 and after.</p>
<figure class="fig-arch"><figcaption>The road to 1948 as a system, with the network map's results</figcaption>
<div class="arch">
<section class="ly"><h4>L1 · inputs</h4>
<div class="nodes">
<div class="nd"><b>Money</b><span>About $404 million documented, 1882–1948</span><code>none: 0% · no Rothschild money: 36%</code></div>
<div class="nd"><b>People</b><span>Immigration, most of it on Mandate certificates</span><code>none: 17% · no certificates: 78%</code></div>
<div class="nd"><b>Land</b><span>Bought by PICA and the JNF; about 7% owned by 1947</span><code>held by 1949: about 78%</code></div>
<div class="nd"><b>Arms</b><span>The Haganah and its arms network</span><code>no armed groups: 0%</code></div>
<div class="nd"><b>Legitimacy</b><span>Faith, the survivors' case, public support</span><code>all of it: 48%</code></div>
</div></section>
<p class="lk"><span><i>Documented</i>carried by the movement's institutions</span></p>
<section class="ly"><h4>L2 · institutions</h4>
<div class="nodes">
<div class="nd"><b>Zionist Organization</b><span>Basel, 1897</span><code>no organized movement: 0%</code></div>
<div class="nd hub"><b>Jewish Agency</b><span>Recognised by the Mandate, Article 4</span><code>the proxy between empire and movement</code></div>
<div class="nd"><b>Anglo-Palestine Bank</b><span>The movement's money, Haavara included</span><code>one dispatch point</code></div>
</div></section>
<p class="lk"><span><i>Documented</i>made law and policy by the powers</span></p>
<section class="ly"><h4>L3 · decisions by the powers</h4>
<div class="nodes">
<div class="nd"><b>Balfour, 1917</b><span>A "national home"</span><code>no British backing: 36%</code></div>
<div class="nd"><b>The Mandate, 1922</b><span>Articles 2, 4 and 6</span><code>installed before the majority was asked</code></div>
<div class="nd"><b>Resolution 181, 1947</b><span>Partition, 55–56% to the Jewish state</span><code>no United States: about 25%</code></div>
</div></section>
<p class="lk"><span><i>Documented</i>14 May 1948</span></p>
<section class="ly"><h4>L4 · output</h4>
<div class="nodes">
<div class="nd hub"><b>The State of Israel</b><span>Declared 14 May 1948, recognised by the United States the same day</span><code>full record: 93%</code></div>
<div class="nd"><b>The displacement</b><span>Roughly 700,000 to 750,000 Palestinians</span><code>without it the refugee question goes (Stage Seven)</code></div>
</div></section>
<p class="lk rep"><span><i>Documented</i>what followed, in red on the map</span></p>
<section class="ly"><h4>L5 · after 1948</h4>
<div class="nodes">
<div class="nd"><b>Occupation, 1967</b><span>Settlements, uprisings, the peace plans</span><code>without it: 19 of 51 later events lose every cause</code></div>
<div class="nd"><b>The patron</b><span>About $298 billion in American aid, 1946–2024</span><code>45 vetoes by December 2023</code></div>
<div class="nd pos"><b>Iran</b><span>Rooted in the coup of 1953, not in the founding</span><code>the chain the founding does not explain</code></div>
</div></section>
</div>
<p class="fig-src">Sources: the {MAP}, Tests, as of 26 November 2026; [cite:zionism_founding_1897] [cite:balfour_letter] [cite:rs_md_avalon] [cite:britannica_res181] [cite:morris_1948] [cite:trumanlibrary_recognition] [cite:wiki_nakba] [cite:dv4_crs_aid_2025] [cite:ccga_vetoes] [cite:w_1953_coup]</p>
</figure>"""

F['rdc_limits.html'] = """<h2>What the Code Does Not Claim</h2>
<p>The code in this appendix is a vocabulary, not a finding. It does not claim that the institutions on the road to 1948 were literally software, that a hidden program ran beneath them, or that the people in them coordinated in secret. Each step it names was public: Herzl published his title, the Basel programme and the Balfour letter were printed, the Mandate's articles were law, the transfer agreement was signed and reported, and the lines of 1947 and 1949 were drawn on published maps. [cite:herzl_judenstaat_1896] [cite:balfour_letter] [cite:rs_md_avalon] [cite:wiki_haavara_agreement]</p>
<p>Nor does it describe anyone's intentions. A technique that fits what an institution did says nothing about what a person in it believed or meant, and nothing here is about Jews as a people: the subjects are named institutions, named documents and named decisions. The code is useful because it puts a name to a shape, a commitment installed before the affected could object, a label kept while the program changed, one body forwarding for another, one gateway for the money, a line inherited and never redrawn. The same shapes can be looked for in any other record. Where the code and the record disagree, the record wins.</p>"""

for k, v in F.items(): open(B + k, 'w', encoding='utf-8').write(v.strip() + '\n')
json.dump({'chapter': 'rdc', 'title': 'Appendix Three: The Architecture in Code',
           'sections': [{'s': s, 'draws': [], 'research': []} for s in ['rdc_key', 'rdc_load', 'rdc_swizzle', 'rdc_proxy', 'rdc_dispatch', 'rdc_inherit', 'rdc_program', 'rdc_entities', 'rdc_system', 'rdc_limits']]},
          open(B + '_manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', len(F))
