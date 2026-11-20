"""Card prompts for every test that leaves less than a 30% chance of a state in 1948, with disclosure cards
on how the map is built and how the chances are computed. Reads the live run written by cards_data.js
(cards2.json) and the stress ranges. Usage: python3 gen_below30_cards.py <scratch dir> <out.md>"""
import json, re, sys, importlib.util
SP = sys.argv[1].rstrip('/') + '/'
spec = importlib.util.spec_from_file_location('gc', SP + 'gen_cards.py'); G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
d, T, S, r, q, card, falls, tiles, MAP = G.d, G.T, G.S, G.r, G.q, G.card, G.falls, G.tiles, G.MAP
st = d['status']; counted = st['verified'] + st['reported']

def tcard(key, pill, head, sub, dark, taken, extra, callout, method, nf=3):
    x = T[key]; on = r(x['rd']['on'])
    hero = f"{MAP}; {dark}; in front of it, an engraved antique-gold probability dial, a circular gauge ring filled crimson to {on} percent of its circumference, with faint light rays behind it."
    cut = (f'Beneath the strip, one line of small white text on a thin gold hairline: "HOW THIS WAS MEASURED: {method}". '
           'If the card gets crowded, cut the first panel to its first line.')
    return on, card(f"{head} ({on}%)", pill, head, sub, hero, f"{on}%", "CHANCE OF A STATE IN 1948", "TAKEN OUT", taken,
                    "WHAT FALLS WITH IT", falls(x, extra, nf), callout, tiles(x), cut)

def removed(n): return f"{n} nodes removed with every tie that ran only through them; the nine channels recounted"
B = lambda s: 'B:' + s
TC = []
TC.append(tcard('movement', "BELOW 30% · THE MOVEMENT", "NO ORGANIZED MOVEMENT", "Remove the Congress, the Agency and their leaders",
  "the central cluster of the map has gone dark, its threads cut by crimson lines",
  ["The Zionist Congress and Organization, the Jewish Agency, the Histadrut", "Herzl, Weizmann, Ben-Gurion and the leaders who ran them"],
  ["Every one of the nine channels falls to zero", "No one is left to carry the money, the land or the force"], "NOTHING ELSE COULD REPLACE THE MOVEMENT",
  removed(T['movement']['n']), 2))
TC.append(tcard('armed', "BELOW 30% · FORCE", "NO ARMED GROUPS", "The Haganah, Irgun, Lehi and the arms network",
  "one dense cluster of nodes is dark and severed by crimson cut lines",
  ["The Haganah, Palmach, Irgun and Lehi", "The arms buyers, smugglers and airlift crews", "The defence levy and the clandestine voyages"],
  ["The arms and force channel falls to zero", "Nothing outside it could fill it"], "NO FORCE, NO STATE, ON ANY DATE", removed(T['armed']['n']), 2))
TC.append(tcard(B('Without the banks and land and finance companies'), "BELOW 30% · FOUND BY SEARCH", "NO BANKS, LAND COMPANIES OR FUNDS", "The houses that raised the money and bought the land",
  "a cluster of gold coin-shaped nodes is dark, money threads cut in crimson",
  ["60 banks, funds and land companies: the Jewish National Fund, PICA, the Anglo-Palestine Bank, Keren Hayesod, the Jewish Colonial Trust and others"],
  ["With all three land buyers gone, no Jewish-held land is left in 1948"], "THE LAND HAD TO BE BOUGHT, AND BANKED",
  "the 60 documented finance nodes removed; land held in 1948 counted in dunams", 3))
TC.append(tcard(B('Without both Jewish National Fund and Land held by other Jewish owners (1948)'), "BELOW 30% · FOUND BY SEARCH", "NO LAND IN JEWISH HANDS", "The National Fund's land and everyone else's",
  "a patchwork of small gold land parcels across the map has gone dark, cut in crimson",
  ["The Jewish National Fund: 936,000 dunams by 1948", "All other Jewish-owned land: PICA's and private buyers', the rest of about 2 million dunams bought by 1948",
   f"With the Mandate government instead of the Fund: {r(T[B('Without both British Mandate administration and Land held by other Jewish owners (1948)')]['rd']['on'])}%"],
  ["The land-held channel falls to zero", "The Mandate's 1920 land law carried most of the Fund's buying, so removing the Mandate government takes that share too"],
  "NO LAND, NO STATE", "land held by Jews in May 1948 counted in dunams (Stein; JNF figures); each holding tied to its buyer", 2))
TC.append(tcard('rothus', "BELOW 30% · TWO PILLARS", "NO ROTHSCHILDS, NO UNITED STATES", "The two largest sources of money and backing",
  "two large clusters are dark, cut away by crimson lines",
  ["Every Rothschild house and heir, and PICA", "The US government, Congress, the American organizations and donors"],
  [], "THE TWO LARGEST SUPPORTS, GONE TOGETHER", removed(T['rothus']['n'])))
TC.append(tcard('roth_web', "BELOW 30% · ASSUMPTION", "THE ROTHSCHILDS AND EVERYONE TIED TO THEM", "An upper bound, not a finding",
  "one bright cluster and every node it touches are dark, cut in crimson",
  ["The family, and every person and body with a documented tie to it", "That list includes Herzl, Weizmann, Balfour and the Jewish Agency"],
  ["Assumes all of them would have vanished with the family; the record does not show that", f"On the documented record alone: {r(T['roth']['rd']['on'])}%"],
  "CLOSER TO REMOVING THE MOVEMENT THAN A FAMILY", "the assumption that everyone tied to the family falls with it; labelled as such on the map", 2))
TC.append(tcard('roth_web_inst', "BELOW 30% · ASSUMPTION", "THE ROTHSCHILDS AND THEIR INSTITUTIONS", "The people stay; the bodies tied to them go",
  "one bright cluster and the institutions around it are dark, cut in crimson",
  ["The family", "Every institution and wealth vehicle with a documented tie to it, including the Jewish Agency and the British Parliament"],
  ["Assumes none of those bodies had support apart from the family", "The money channel falls to 77%"],
  "AN ASSUMPTION, NOT THE RECORD", "the assumption that every tied institution falls with the family; labelled as such on the map", 2))
TC.append(tcard('d_all', "BELOW 30% · OFTEN DENIED", "EVERY DENIED PART, AT ONCE", "The record that is usually played down",
  "scattered nodes across the whole map are dark and severed",
  ["The imperial sponsor", "The pressured votes", "Money and access to Truman", "Irgun and Lehi", "Arms from abroad", "The Transfer Agreement", "Absentee land sales", "Plan Dalet"],
  ["Without Britain the rest still cut it to 48%"], "NO SINGLE DENIAL CARRIED IT ALL; TOGETHER THEY DID", removed(T['d_all']['n'])))
TC.append(tcard('roth_decl', "BELOW 30% · ASSUMPTION", "NO ROTHSCHILDS, NO DECLARATION", "If Britain would not have issued it without them",
  "one bright cluster is dark and a parchment node beside it is cut in crimson",
  ["The family", "And the Balfour Declaration, on the assumption it needed its addressee"],
  ["The record shows the letter was addressed to Walter Rothschild and that he worked on the draft", "It does not show Britain would have withheld it otherwise", f"With the Declaration standing: {r(T['roth']['rd']['on'])}%"],
  "AN ASSUMPTION ABOUT ONE LETTER", "the assumption that the Declaration depended on its addressee; labelled as such on the map", 3))
TC.append(tcard('roth_pre', "BELOW 30% · BEFORE HERZL", "NO ROTHSCHILDS, NO EARLY NETWORK", "The family and everything before 1897",
  "an old, deep cluster at the root of the map is dark, its threads cut in crimson",
  ["Every Rothschild house and heir", "The Lovers of Zion, the Odessa Committee, the Alliance and the early donors and colonies", f"With Herzl removed too: {r(T['roth_herzl_pre']['rd']['on'])}%"],
  ["The cost is time: decades of settlement work no one else was funding", "Herzl himself adds only about two points"], "THE ROOTS OF THE MONEY, CUT", removed(T['roth_pre']['n']), 2))
TC.append(tcard(B('Without Palestine Jewish Colonization Association (PICA), Jewish Agency and Anglo-Palestine Company (Bank Leumi)'), "BELOW 30% · FOUND BY SEARCH", "THREE INSTITUTIONS", "The land company, the Agency and the bank",
  "three bright central nodes are dark, severed by crimson lines",
  ["PICA (the Rothschild land company)", "The Jewish Agency", "The Anglo-Palestine Bank", f"Or the Zionist Congress in place of the bank: {r(T[B('Without Palestine Jewish Colonization Association (PICA), Jewish Agency and Zionist Congress')]['rd']['on'])}%", "Each alone: 83 to 89%"],
  [], "THREE NODES, AND THE MONEY CHANNEL CRACKS", "3 nodes removed; found by testing all 2,600 triples among the 26 costliest nodes"))
TC.append(tcard('us', "BELOW 30% · ONE COUNTRY", "THE UNITED STATES STAYS OUT", "Government, Congress, lobby and money",
  "the whole American cluster is dark, severed by crimson lines",
  ["The US government and Congress", "The American Zionist organizations", "American donors and arms buyers"], [], "WITHOUT AMERICA: UNLIKELY IN 1948", removed(T['us']['n'])))
TC.append(tcard(B('Without the British government and the Soviet bloc'), "BELOW 30% · FOUND BY SEARCH", "NO LONDON, NO MOSCOW", "The empire that built the frame and the bloc that armed it",
  "two clusters at opposite edges of the map are dark, severed by crimson lines",
  ["The British government and Mandate", "The Soviet Union and its bloc, Czechoslovakia's arms included", f"Alone: Britain {r(T['britain']['rd']['on'])}%, the Soviet bloc {r(T['soviet']['rd']['on'])}%"],
  [], "THE FRAME AND THE RIFLES, BOTH GONE", "the two documented groups removed together; found by testing all 105 pairs of groups"))
TC.append(tcard(B('Without the British government and the American Zionist organizations'), "BELOW 30% · FOUND BY SEARCH", "NO LONDON, NO AMERICAN ORGANIZERS", "The sponsor and the organizers who pressed Washington",
  "two clusters on either side of an ocean are dark, severed by crimson lines",
  ["The British government and Mandate", "The American Zionist organizations, from the Emergency Council to the appeals", f"Britain alone: {r(T['britain']['rd']['on'])}%"],
  [], "THE FRAMEWORK AND THE PRESSURE, BOTH GONE", "the two documented groups removed together; found by testing all 105 pairs of groups"))
TC.append(tcard(B('Without Palestine Jewish Colonization Association (PICA), Czechoslovakia (arms supplier) and Jewish Agency'), "BELOW 30% · FOUND BY SEARCH", "CZECH ARMS AND TWO INSTITUTIONS", "The rifles of 1948, the land company, the Agency",
  "three nodes far apart are dark, severed by crimson lines",
  ["Czechoslovakia as arms supplier", "PICA", "The Jewish Agency", "Each alone: 83 to 85%"], ["Close to half the rifles in hand on 14 May, gone"],
  "NO RIFLES, NO LAND COMPANY, NO AGENCY", "3 nodes removed; found by testing all 2,600 triples among the 26 costliest nodes"))
TC.sort(key=lambda x: x[0])

ranges = S
D = []
D.append(card("Disclosure 1 — How The Map Was Built", "HOW IT WORKS · 1 OF 5", "HOW THE MAP WAS BUILT", "Every tie has a source you can open",
  f"{MAP}; a small parchment source tag glows on each gold thread, with faint light rays behind it.", f"{counted:,}", "TIES COUNTED, EACH WITH ITS SOURCE",
  "WHAT IS ON IT", [f"{d['nodes']} people, bodies, documents and events, 1840 to 1948", f"{d['edges']:,} ties in all", f"{st['verified']:,} verified: a document states one party acting on another", f"{st['reported']} reported by a named outlet: counted at 60%", f"{st['co-mention']:,} named together only: shown, never counted"],
  "THE RULES", ["Both sides under the same rules, supporters and opponents", "Kinship is never a tie; identity is never a tie", "Opposition counts against decisions, never as support", "Twelve research passes, one per pathway, 1882 to 1948"],
  "NO SOURCE, NO WEIGHT"))
D.append(card("Disclosure 2 — How A Chance Is Computed", "HOW IT WORKS · 2 OF 5", "HOW A CHANCE IS COMPUTED", "Nine channels, multiplied together",
  "nine engraved gold gauges in a row on an indigo plinth, each filled almost to the top, their needles joined by a fine gold thread to one large dial reading 93 percent.",
  "93%", "THE FULL RECORD, NOTHING REMOVED", "THE NINE CHANNELS",
  ["Money in documented 1948 dollars (counted twice)", "Land and settlers · Arms and force · Diplomacy and law", "Organization · Recognition · Legitimacy", "People: immigrants in thousands", "Land held in 1948, in dunams"],
  "THE ARITHMETIC", ["Each channel sums the weight of its documented ties", "Strength rises with weight and levels off: the full record reads 99% per channel", "The chance of a state is the channels multiplied: 93% for the full record", "One empty channel makes the whole product zero"],
  "EVERY WEIGHT IS DISCLOSED ON THE MAP"))
D.append(card("Disclosure 3 — The Chain Reaction", "HOW IT WORKS · 3 OF 5", "THE CHAIN REACTION", "What happens when a part is removed",
  "a row of engraved gold dominoes on an indigo plinth, the first ones fallen, a faint glowing network map behind them.",
  "7", "KEY DECISIONS RE-WEIGHED IN EVERY TEST", "WHEN A NODE IS REMOVED",
  ["Its ties go", "Whatever is left cut off from the core goes too: the Agency, the Haganah, the declaration, the UN vote", "A document whose every issuer is gone is never issued"],
  "THE DECISIONS", ["Balfour, the Mandate, the UN referral, the US vote, US recognition, Soviet support, Czech arms", "Each weighs documented push against documented resistance", "Push aimed at one man does not pass to his successor", "Without their leader, allied states keep only their measured independence: the Americas one vote in three, Western Europe about one in four, the Soviet side one in five", "Resolution 181 still needs two-thirds"],
  "REMOVE ONE LINK AND WHAT HUNG ON IT FALLS TOO"))
tb = d['tbuild']
D.append(card("Disclosure 4 — Time, Delay And The Verdicts", "HOW IT WORKS · 4 OF 5", "TIME, DELAY AND THE VERDICTS", "A later state is a weaker state",
  "a cracked engraved gold hourglass on an indigo plinth, sand still falling, beside a gold dial, a faint network map glowing behind them.",
  f"{r(d['hazard']*100)}%", "OF THE CHANCE LOST FOR EVERY YEAR OF DELAY", "THE NUMBERS ON EACH CARD",
  ["In 1948: the chance on 14 May 1948", "Ever: the best later chance as the window closes", "Work lost: years only the removed part did, after its documented substitute", f"To rebuild: at the pace each channel was first built, money {tb[0]} years, force {tb[2]}, people {tb[7]}"],
  "THE VERDICTS", ["85% or more in 1948: on time", "70% in 1948, or 75% ever: likely, but delayed", "55% or more ever: possible, with great difficulty", "30% or more ever: unlikely", "Below that: not possible on this record"],
  "BELOW 30%: NOT IN 1948 ON THIS RECORD"))
D.append(card("Disclosure 5 — What The Figures Cannot Tell You", "HOW IT WORKS · 5 OF 5", "WHAT THE FIGURES CANNOT TELL YOU", "A measure of the record, not a prophecy",
  "an engraved antique-gold balance scale on an indigo plinth, its two pans level, a faint glowing network map behind it, light rays from above.",
  f"{ranges['base'][1]}–{ranges['base'][2]}%", "THE FULL RECORD, EVERY WEIGHT HALVED OR DOUBLED", "STRESS-TESTED",
  [f"Britain {ranges['britain'][0]}% (range {ranges['britain'][1]}–{ranges['britain'][2]}%)", f"United States {ranges['us'][0]}% ({ranges['us'][1]}–{ranges['us'][2]}%)", f"Rothschilds {ranges['roth'][0]}% ({ranges['roth'][1]}–{ranges['roth'][2]}%)", "Each source left out in turn; the order held"],
  "THE LIMITS", ["Assumptions are labelled on every card that uses one", "Persuasion with no documented route to a decision is not counted", "It measures the founding, not the war or the expulsions after it", "Counted on a straight line, population would weigh more"],
  "READ THE FIGURES AGAINST EACH OTHER"))

SHORT = {"NO ORGANIZED MOVEMENT": "No organized movement", "NO ARMED GROUPS": "No armed groups", "NO BANKS, LAND COMPANIES OR FUNDS": "No banks, land companies or funds",
 "NO LAND IN JEWISH HANDS": "No land in Jewish hands", "NO ROTHSCHILDS, NO UNITED STATES": "No Rothschilds, no United States",
 "THE ROTHSCHILDS AND EVERYONE TIED TO THEM": "Rothschilds and everyone tied to them (assumption)", "THE ROTHSCHILDS AND THEIR INSTITUTIONS": "Rothschilds and their institutions (assumption)",
 "EVERY DENIED PART, AT ONCE": "Every often-denied part at once", "NO ROTHSCHILDS, NO DECLARATION": "No Rothschilds, no Declaration (assumption)",
 "NO ROTHSCHILDS, NO EARLY NETWORK": "No Rothschilds, no network before 1897", "THREE INSTITUTIONS": "PICA, the Agency and the bank",
 "THE UNITED STATES STAYS OUT": "The United States stays out", "NO LONDON, NO MOSCOW": "No London, no Moscow",
 "NO LONDON, NO AMERICAN ORGANIZERS": "No London, no American organizers", "CZECH ARMS AND TWO INSTITUTIONS": "Czech arms, PICA and the Agency"}
rows = []
for on, c in TC:
    head = re.search(r'^## (.*) \(\d+%\)', c, re.M).group(1)
    rows.append(f"{SHORT.get(head, head)}: {on}%")
IDX = card("Index — Below The Line", "BELOW 30% · ALL RESULTS", "BELOW THE LINE", "Every test under a 30% chance of a state in 1948",
  "a tall engraved gold thermometer-style gauge on the left edge with a bright crimson line at 30 percent, a faint glowing network map behind it.",
  str(len(TC)), "RESULTS UNDER 30%", "LOWEST FIRST", rows[:8], "AND", rows[8:] + ["No single person or institution falls below 30%: the lowest is Edmond de Rothschild, 35%"],
  "IT TOOK WHOLE CATEGORIES, NOT ONE NAME", cut='If the card gets crowded, set both panels in two narrow columns; never cut a result.')

hdr = f"""# Below 30% — card prompts (ChatGPT image generation)

Built 19 November 2026 from the live network map (v95). Every test that leaves less than a 30% chance of a state in 1948, lowest first, with five cards that disclose how the map was built and how each chance is computed, and an index card. One prompt per card; paste each code block into ChatGPT image generation.

**Order to post:** Disclosure 1–5, then the index, then the test cards. Each test card also carries a one-line note on how that result was measured.

**Theme:** ink-indigo, signal crimson, antique-gold foil, white (same as the probability set). **CTA on every card:** www.tinyurl.com/1948scam, www.tinyurl.com/thetruthlibrary, TikTok @chosenron13 (primary), Instagram @chosen.ron13.

**Re-check before posting:** figures as of 19 Nov 2026 (v95); they move whenever the map changes. Three cards rest on assumptions and say so (tagged ASSUMPTION).

"""
body = '\n'.join(D) + '\n' + IDX + '\n' + '\n'.join(re.sub(r'^## ', f'## Test {i} — ', c, count=1) for i, (on, c) in enumerate(TC, 1))
open(sys.argv[2], 'w').write(hdr + body)
print(len(D), len(TC)); print('\n'.join(rows))
