import json, re
SP = '/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/'
d = json.load(open(SP + 'cards2.json'))
S = json.load(open(SP + 'stress_ranges.json'))
T = {}
for x in d['T']:
    if x['k'] in ('T', 'D'): T.setdefault(x['id'], x)
    else: T['B:' + x['label']] = x
LAB = d['labels']; CH = d['channels']
CL = {'money':'money','land':'land and settlers','force':'arms and force','diplomacy':'diplomacy and law','organization':'organization','recognition':'recognition','legitimacy':'legitimacy','people':'people','holdings':'land-held'}

PAL = ("Ultra-premium vertical social card, 1080×1920px (9:16), cinematic editorial poster quality. Palette, exactly four colors: deep ink-indigo background #0B1026 graded to #161E45; signal crimson #D7263D for bars, callouts and cut lines; brilliant white #FFFFFF for type; antique-gold foil #E8B44A with real foil sheen and highlights for numbers, borders and premium touches. Rich, deeply saturated — NOT pastel, NOT faded, NOT vintage. High contrast, glossy depth, subtle film grain, soft cinematic vignette.")
CTA = ("CTA block, bottom quarter, in this order: a full-width crimson bar with the white heavy-caps line \"RUN EVERY TEST YOURSELF\"; then the hero URL \"www.tinyurl.com/1948scam\" as the largest text after the headline, thick antique-gold foil lettering with metallic shine on a deep-indigo pill with a glowing gold outline; then smaller white text \"The full library → www.tinyurl.com/thetruthlibrary\"; then two social pills side by side: \"TikTok @chosenron13\" with a small gold tag \"PRIMARY\", and \"Instagram @chosen.ron13\".")
END = "All text spelled exactly as written, razor-sharp and fully legible, high contrast. No gray or faded text. No people, no faces, no real logos."
MAP = "a glowing constellation-style network map of hundreds of small gold nodes joined by fine gold threads, lit cinematically and fading into the background"

def q(xs): return ' · '.join(f'"{x}"' for x in xs)
def r(x): return int(round(x + 1e-9))

def dec_name(n):
    n = re.sub(r'^The ', '', n); n = re.sub(r'\s*\([^)]*\)$', '', n)
    return n[0].upper() + n[1:]

def falls(x, extra, limit=4):
    out = list(extra)
    for nm, c in x['dec']:
        if c < 50 and len(out) < limit: out.append(f'{dec_name(nm)}: {c}%')
    for i, p in enumerate(x['pc']):
        if p < 90 and len(out) < limit: out.append(f'The {CL[CH[i]]} channel falls to {p}%')
    return out[:limit]

def tiles(x):
    rd = x['rd']
    reb = 'NO ONE LEFT' if rd.get('nocarrier') else ('NONE' if rd['delay'] < 1 else ('OVER A CENTURY' if rd['delay'] > 100 else f"{r(rd['delay'])} YEARS"))
    ret = str(rd['retry']) if rd.get('retry') else 'NONE BETTER THAN 1948'
    return (f'Then a strip of four glossy indigo tiles with foil numbers and white labels: "{r(rd["ever"])}%" / "EVER", '
            f'"{r(rd["lost"] or 0)} {"YR" if r(rd["lost"] or 0)==1 else "YRS"}" / "WORK LOST", "{reb}" / "TO REBUILD", "{ret}" / "BEST YEAR TO RETRY".')

def card(title, pill, head, sub, hero, stat, cap, p1t, p1, p2t, p2, callout, strip='', cut='If the card gets crowded, cut the second panel first.'):
    body = (f"{PAL}\n\nHero, top third: {hero}\n\nType: a small crimson pill with a gold foil edge and white small caps \"{pill}\"; the headline in huge, heavy condensed sans (Montserrat Black), white with a thin gold foil edge and soft drop shadow: \"{head}\"; beneath it a gold foil italic serif subhead: \"{sub}\".\n\n"
            f"Anchor stat: a giant antique-gold foil number \"{stat}\" with the white small-caps caption \"{cap}\".\n\n"
            f"Panel (translucent indigo glass, thin gold border, small gold node icons as bullets), titled \"{p1t}\": {q(p1)}. Second panel, titled \"{p2t}\": {q(p2)}. " + (strip + ' ' if strip else '') + cut +
            f"\n\nCallout: one full-width crimson bar with white heavy caps: \"{callout}\".\n\n{CTA}\n\n{END}")
    return f"## {title}\n\n```\n{body}\n```\n"

def test_card(key, pill, head, sub, dark, taken, extra, callout, n_falls=3):
    x = T[key]; on = r(x['rd']['on'])
    hero = f"{MAP}; {dark}; in front of it, an engraved antique-gold probability dial, a circular gauge ring filled crimson to {on} percent of its circumference, with faint light rays behind it."
    return on, card(f"{head} ({on}%)", pill, head, sub, hero, f"{on}%", "CHANCE OF A STATE IN 1948", "TAKEN OUT", taken, "WHAT FALLS WITH IT",
                    falls(x, extra, n_falls), callout, tiles(x), 'If the card gets crowded, cut the first panel to its first line.')

cards = []
nodes, edges = d['nodes'], d['edges']; st = d['status']; counted = st['verified'] + st['reported']
M = []
M.append(card("Card 1 — The Road To 1948, Mapped", "THE METHOD · 1 OF 6", "THE ROAD TO 1948, MAPPED", "Every person, body and document, 1840 to 1948",
  f"{MAP}, with faint light rays behind it.", f"{nodes:,}", "PEOPLE, BODIES, DOCUMENTS AND EVENTS", "WHAT IS ON IT",
  [f"{edges:,} ties between them", f"{counted:,} counted: {st['verified']:,} verified, {st['reported']} reported", f"{st['co-mention']:,} shared mentions shown, never counted", "Every tie links to its source"],
  "HOW TO USE IT", ["Tap any node for its record", "Remove any node, or any group, and the map recounts everything"], "EVERY TIE HAS A SOURCE YOU CAN OPEN"))
M.append(card("Card 2 — Nine Things A State Needed", "THE METHOD · 2 OF 6", "NINE THINGS A STATE NEEDED", "All nine at once, or no state",
  "nine engraved gold pillars standing in a row on a dark indigo plinth, each with a glowing gold band, a fine network of threads running between their capitals, cinematic light from above.",
  "9", "CHANNELS, ALL REQUIRED", "THE CHANNELS",
  ["Money, in documented 1948 dollars (counted twice)", "Land and settlers", "Arms and force", "Diplomacy and law", "Organization", "Recognition", "Legitimacy: the case made to the powers", "People: the immigrants", "Land held in 1948"],
  "HOW THEY COMBINE", ["Each channel counts only what is still tied to the core: the Agency, the Haganah, the declaration, the UN vote", "The chance of a state is the nine multiplied together"],
  "ONE EMPTY CHANNEL AND THE WHOLE STATE FAILS"))
M.append(card("Card 3 — How The Chance Is Set", "THE METHOD · 3 OF 6", "HOW THE CHANCE IS SET", "The full record reads 93 percent",
  "an engraved antique-gold probability dial, its gauge ring filled to 93 percent, floating in front of a faint glowing network map, light rays behind it.",
  "93%", "THE FULL RECORD, NOTHING REMOVED", "WHEN A NODE IS REMOVED",
  ["Its ties go, and everything left cut off from the core goes with it", "Each channel is recounted; full strength reads 99%"],
  "THE CHAIN REACTION", ["Seven key decisions are re-weighed: documented push against documented resistance", "Push aimed at one man does not pass to his successor", "Allied states keep their vote only at their bloc's measured independence", "Resolution 181 still needs two-thirds"],
  "REMOVE ONE LINK AND WHAT HUNG ON IT FALLS TOO"))
tb = d['tbuild']
M.append(card("Card 4 — The Cost Of Starting Over", "THE METHOD · 4 OF 6", "THE COST OF STARTING OVER", "What falls out of 1948 must be rebuilt later",
  "a cracked engraved gold hourglass on an indigo plinth, sand still falling, a faint network map glowing behind it.",
  f"{r(d['hazard']*100)}%", "OF THE CHANCE LOST FOR EVERY YEAR OF DELAY", "WHAT IS COUNTED",
  ["Work lost: the years only that actor did, with the documented substitute who could have taken over, and from when",
   f"Rebuilding at the pace each channel was first built: money {tb[0]} years, land {tb[1]}, force {tb[2]}, people {tb[7]}"],
  "WHY IT IS A BEST CASE", ["The map rebuilds each channel in parallel", "In life the same people and money had to rebuild everything at once", "So every delay here is the shortest it could be"],
  "EVERY YEAR LATE, THE WINDOW CLOSES FURTHER"))
M.append(card("Card 5 — How To Read A Test Card", "THE METHOD · 5 OF 6", "HOW TO READ A TEST CARD", "Four numbers and a verdict",
  "an engraved gold dial beside four glossy indigo tiles with gold foil numbers, floating above a faint glowing network map.",
  "85%", "IN 1948 OR MORE: ON TIME", "THE NUMBERS",
  ["In 1948: the chance of a state on 14 May 1948", "Ever: the best later chance, as the window closes", "Work lost: years no one else could do", "To rebuild: time to restore what fell"],
  "THE VERDICTS", ["85% or more in 1948: on time", "70% in 1948, or 75% ever: likely, but delayed", "55% or more ever: possible, with great difficulty", "30% or more ever: unlikely", "Below: not possible on this record"],
  "A RESULT OF THE RECORD, NOT A PROPHECY"))
def rg(k): v = S[k]; return f"{v[1]}–{v[2]}%"
M.append(card("Card 6 — How Sturdy Are The Figures", "THE METHOD · 6 OF 6", "HOW STURDY ARE THE FIGURES", "Every weight pushed to half and to double",
  "an engraved antique-gold balance scale on an indigo plinth, its two pans level, a faint glowing network map behind it, light rays from above.",
  rg('base').replace('%', ' %').replace(' %', '%'), "THE FULL RECORD, EVERY WEIGHT HALVED OR DOUBLED", "WHAT WAS TESTED",
  ["Each of the nine channels counted half and double", "Reported ties counted at 0.3 and at full weight", "British training counted ten times", "Each single source left out in turn"],
  "WHAT HELD", [f"Britain {S['britain'][0]}% (range {rg('britain')})", f"United States {S['us'][0]}% ({rg('us')})", f"Rothschilds {S['roth'][0]}% ({rg('roth')})", f"Balfour {S['balfour'][0]}% ({rg('balfour')})", "The order of the findings held"],
  "THE RANKING HELD; THE EXACT FIGURES ARE A RANGE"))
open(SP + 'method_cards.md', 'w').write('\n'.join(M))

B = lambda lbl: 'B:' + lbl
TC = []
TC.append(test_card('movement', "TEST · THE MOVEMENT ITSELF", "NO ORGANIZED MOVEMENT", "Remove the Congress, the Agency and their leaders",
  "the central cluster of the map has gone dark, its threads cut by crimson lines", ["The World Zionist Organization, the Jewish Agency, the Zionist Congress and the leaders who ran them"],
  ["Every channel collapses", "No one is left to pursue a state"], "NOTHING ELSE COULD REPLACE THE MOVEMENT", 2))
TC.append(test_card('armed', "TEST · FORCE", "NO ARMED GROUPS", "The Haganah, Irgun, Lehi and the arms network",
  "one dense cluster of nodes is dark and severed by crimson cut lines", ["The Haganah, Palmach, Irgun and Lehi", "The arms buyers and smugglers"],
  ["The force channel is empty", "Nothing outside it could fill it"], "NO FORCE, NO STATE, ON ANY DATE", 2))
TC.append(test_card(B('Without the banks and land and finance companies'), "TEST · FOUND BY SEARCH", "NO BANKS, LAND COMPANIES OR FUNDS", "The houses that raised the money and bought the land",
  "a cluster of gold coin-shaped nodes is dark, money threads cut in crimson", ["The Jewish National Fund, PICA, the Anglo-Palestine Bank, Keren Hayesod, the land company and the other finance houses"],
  [], "THE LAND HAD TO BE BOUGHT, AND BANKED", 3))
TC.append(test_card('rothus', "TEST · TWO PILLARS", "NO ROTHSCHILDS, NO UNITED STATES", "The two largest sources of money and backing",
  "two large clusters are dark, cut away by crimson lines", ["Every Rothschild house and heir", "The US government, Congress, lobby and donors"], [], "THE TWO LARGEST SUPPORTS, GONE TOGETHER"))
TC.append(test_card('d_all', "TEST · OFTEN DENIED", "EVERY DENIED PART, AT ONCE", "The record that is usually played down",
  "scattered nodes across the whole map are dark and severed", ["The imperial sponsor", "The pressured votes", "Money and access to Truman", "Irgun and Lehi", "Arms from abroad", "The Transfer Agreement", "Absentee land sales", "Plan Dalet"],
  ["Without Britain the rest still cut it to 48%"], "NO SINGLE DENIAL CARRIED IT ALL; TOGETHER THEY DID"))
TC.append(test_card('roth_pre', "TEST · BEFORE HERZL", "NO ROTHSCHILDS, NO EARLY NETWORK", "The family and everything before 1897",
  "an old, deep cluster at the root of the map is dark, its threads cut in crimson", ["Every Rothschild house and heir", "The Lovers of Zion, the Odessa Committee, the Alliance and the early donors and colonies", f"With Herzl removed too: {r(T['roth_herzl_pre']['rd']['on'])}%"],
  ["The cost is time: decades of settlement work that no one else was funding", "Herzl himself adds only about two points"], "THE ROOTS OF THE MONEY, CUT"))
TC.append(test_card(B('Without Palestine Jewish Colonization Association (PICA), Jewish Agency and Anglo-Palestine Company (Bank Leumi)'), "TEST · FOUND BY SEARCH", "THREE INSTITUTIONS", "The land company, the Agency and the bank",
  "three bright central nodes are dark, severed by crimson lines", ["PICA (the Rothschild land company)", "The Jewish Agency", "The Anglo-Palestine Bank (or the Zionist Congress: " + str(r(T[B('Without Palestine Jewish Colonization Association (PICA), Jewish Agency and Zionist Congress')]['rd']['on'])) + "%)"],
  [], "THREE NODES, AND THE MONEY CHANNEL CRACKS"))
TC.append(test_card('us', "TEST · ONE COUNTRY", "THE UNITED STATES STAYS OUT", "Government, Congress, lobby and money",
  "the whole American cluster is dark, severed by crimson lines", ["The US government and Congress", "The American Zionist organizations", "American donors and arms buyers"], [], "WITHOUT AMERICA: UNLIKELY IN 1948"))
TC.append(test_card(B('Without the British government and the American Zionist organizations'), "TEST · FOUND BY SEARCH", "NO LONDON, NO AMERICAN ORGANIZERS", "The sponsor and the organizers who pressed Washington",
  "two clusters on either side of an ocean are dark, severed by crimson lines", ["The British government and Mandate", "The American Zionist organizations"],
  [], "THE FRAMEWORK AND THE PRESSURE, BOTH GONE"))
TC.append(test_card(B('Without US Government and British Mandate administration, plus any one of: British War Cabinet, Balfour Declaration (1917), British Government, League of Nations, Mandate for Palestine (1922)'), "TEST · FOUND BY SEARCH", "WASHINGTON AND THE BRITISH CHAIN", "Remove the US government and two British links",
  "a chain of five gold nodes with links snapped in crimson, the rest dimmed", ["The US government", "The Mandate administration", "Any one of: War Cabinet, Balfour Declaration, British government, League of Nations, Mandate"],
  [], "ONE LINK BREAKS THE WHOLE BRITISH CHAIN"))
TC.append(test_card(B('Without the US government'), "TEST · ONE GOVERNMENT", "WASHINGTON STAYS OUT", "The American state alone; lobby and donors stay",
  "one large government node is dark, the threads of the Americas around it severed in crimson", ["The US government: the vote, the pressure, the recognition", "Congress, the lobby and donors stay"], [], "WITHOUT THE AMERICAN STATE, THE VOTE FAILS"))
TC.append(test_card(B('Without the states that voted for partition'), "TEST · FOUND BY SEARCH", "THE 33 YES VOTES", "Every state that voted for Resolution 181",
  "a ring of 33 small gold nodes, all dark", ["All 33 states that voted for partition on 29 Nov 1947"], ["No resolution, no international basis"], "NO VOTE, NO LEGAL BASIS IN 1948"))
TC.append(test_card('roth', "TEST · ONE FAMILY", "THE ROTHSCHILDS PLAY NO PART", "The family, the Paris house, or Edmond alone",
  "one bright cluster of nodes is dark, its money threads cut in crimson",
  [f"Every Rothschild house and heir: {r(T['roth']['rd']['on'])}%", f"The Paris house: {r(T['roth_paris']['rd']['on'])}%", f"Edmond alone: {r(T['edmond']['rd']['on'])}%", f"Their funding only: {r(T['rothmoney']['rd']['on'])}%"],
  ["The cost is time: the colonies Edmond funded from 1882, when almost no one else did", "PICA's land, about 500,000 dunams in 1934, is lost with them; private buyers' land is not"], "ONE MAN'S MONEY CARRIED DECADES OF IT", 3))
TC.append(test_card('britain', "TEST · ONE GOVERNMENT", "NO IMPERIAL SPONSOR", "The British state that issued, held and enforced",
  "the British cluster is dark, severed by crimson lines", ["The War Cabinet, the Mandate government, Parliament and officials"], [], f"{r(T['britain']['rd']['lost'])} YEARS OF WORK BUILT INSIDE AN EMPIRE"))
TC.append(test_card('ottoman_neutral', "TEST · ASSUMPTION", "THE OTTOMANS STAY OUT OF THE WAR", "No war, so no British war aim in Palestine",
  "the old imperial cluster at one edge glows unbroken while the British threads into Palestine are cut in crimson", ["The Ottoman entry into the First World War, October 1914", "And with it the British conquest of Palestine"],
  ["No British war aim in Palestine: no Declaration, no Mandate", "The money, the settlers already there and the later American and Soviet decisions remain"], "THE LARGEST SINGLE TURN OF CHANCE ON THE MAP"))
TC.append(test_card('balfour', "TEST · ONE DOCUMENT", "NO BALFOUR DECLARATION", "Or a Declaration that needed Walter Rothschild",
  "a single glowing parchment node at the center is dark, its threads cut in crimson", ["The letter of 2 November 1917", f"Same result if it could not issue without its addressee: {r(T['walter']['rd']['on'])}%"],
  ["No Mandate built on it", "Immigration and settlement at the Ottoman pace"], f"ONE LETTER, {r(T['balfour']['rd']['lost'])} YEARS"))
TC.append(test_card('moscow', "TEST · ONE COUNTRY", "ONLY MOSCOW BACKS IT", "Washington stays out as a state",
  "one large node is dark; the threads of the Americas around it flicker", ["The US government as a state; lobby, donors and Congress stay"], ["The American bloc keeps its vote only at its own independence"], "MOSCOW ALONE CANNOT CARRY TWO-THIRDS", 3))
TC.append(test_card('d_arms', "TEST · OFTEN DENIED", "NO ARMS FROM ABROAD", "British training, the secret US network, Czech arms",
  "the arms cluster is dark, threads crossing an ocean cut in crimson", ["British arming of Jewish forces 1936-39", "The Sonneborn network and smugglers", "Czech rifles before 15 May"],
  ["Close to half the rifles of 14 May, gone"], "NOT DAVID ALONE: THE ARMS CAME FROM ABROAD"))
TC.append(test_card('pre_all', "TEST · BEFORE HERZL", "NO NETWORK BEFORE 1897", "Forerunners, organizers, donors and the Alliance",
  "the oldest cluster at the root of the map is dark", ["Kalischer and Hess, the Lovers of Zion, the Odessa Committee, the Alliance Israélite Universelle and the early donors"],
  ["Almost all of the loss is the settlement money, not the ideas"], "THE EARLY MONEY MATTERED, NOT THE EARLY IDEAS"))
TC.append(test_card('policy_doors', "TEST · ASSUMPTION", "NO OPEN DOOR IN THE MANDATE", "No promise to facilitate immigration and land settlement",
  "a gold gate in the center of the map is shut, its threads cut in crimson", ["Articles 4 and 6 of the Mandate: the Jewish Agency's standing and the duty to facilitate immigration and close settlement"],
  ["Immigration and land buying at a fraction of the Mandate pace"], "THE MANDATE'S WORDING OPENED THE DOOR"))
TC.append(test_card('people_mandate', "TEST · PEOPLE", "NO IMMIGRATION CERTIFICATES", "Everything else Britain did, kept",
  "a stream of small gold nodes flowing into the map is cut by a crimson line", ["The certificates the Mandate government issued for Jewish immigration"], ["Under a straight-line population curve: " + str(S['people_mandate'][3]) + "%"], "THE PERMITS FILLED THE COUNTRY"))
TC.append(test_card('latam_bloc', "TEST · ASSUMPTION", "NO LATIN AMERICAN BLOC", "If García Granados and Fabregat had not organized it",
  "a cluster of thirteen small gold nodes in the western half of the map flickers, some cut in crimson", ["The organizing of the Latin American states by Guatemala's and Uruguay's delegates on UNSCOP", "Their states abstain instead (an upper bound)"],
  ["The vote fails 22 to 13"], "THIRTEEN VOTES MADE THE TWO-THIRDS"))
alts = {a[0]: a[2] for a in d['alts']}
def pct(v): return ('%.1f' % v) if v else '0'
TC.append((0.5, card("ANYWHERE BUT THE HOLY LAND (0–2%)", "TEST · THE THEOLOGY SHIELD", "ANYWHERE BUT THE HOLY LAND", "Every other homeland the movement weighed",
  "a dark indigo globe engraved in gold linework with eight small crimson pins scattered across Africa, the Americas, Siberia and the Indian Ocean, and one glowing gold pin on Palestine, light rays behind it.",
  "0–2%", "CHANCE OF A STATE, EVERY OTHER LAND", "THE OTHER LANDS",
  [f"Uganda offer, 1903: {pct(alts['east_africa'])}%", f"El Arish, 1902-03: {pct(alts['el_arish'])}%", "Argentina, Birobidzhan, Madagascar, Alaska, Sosúa, Suriname: 0%"],
  "WHY", ["No Christian or Jewish religious pull to draw money, settlers and powers", "The Zionist Congress rejected Uganda in 1905: it was not Zion", f"The Christian attachment alone, removed: {r(T['theology']['rd']['on'])}%"],
  "THE CHOICE OF LAND WAS THE SHIELD")))
TC.sort(key=lambda x: x[0])
out = []
for i, (on, c) in enumerate(TC, start=7):
    out.append(re.sub(r'^## ', f'## Card {i} — ', c, count=1))
open(SP + 'test_cards.md', 'w').write('\n'.join(out))
print(len(M), len(TC))
for on, c in TC: print(on, c.split('\n')[0])
