#!/usr/bin/env python3
"""Test readings rewritten to the figures of the 27 Nov 2026 audit (cause and effect before 1948, lost work counted from 1882,
substitutes from the same circle, lost years counted across all channels, the full money record). Also: the money groups take
in the new streams, two private-capital tests are added, and a test removes Edmond de Rothschild entirely. Idempotent.

Usage: python3 tools/patch_test_texts_nov27.py [road-network.html]"""
import os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
s = open(P, encoding='utf-8').read()
if 'nov27_texts' in s:
    print('texts already updated'); sys.exit(0)
js = lambda t: t.replace('\\', '\\\\').replace("'", "\\'")

def set_field(tid, field, text):
    global s
    i = s.find("{id:'%s'," % tid); assert i >= 0, tid
    j = s.find(field + ":'", i); assert j > i, (tid, field)
    k = j + len(field) + 2
    while True:
        if s[k] == '\\': k += 2; continue
        if s[k] == "'": break
        k += 1
    s = s[:j + len(field) + 2] + js(text) + s[k:]

def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)

READ = {
 'roth_web': "About 13% on time and 32% ever, with about 42 years of work lost. Read this as an upper bound under a stated assumption, not as a finding: it supposes that everyone with a documented tie to the family would have vanished with it, Herzl, Weizmann, Balfour and the Jewish Agency among them. The record shows these people and bodies met, were funded by or wrote to the family; it does not show they depended on it. The family alone gives about 64%.",
 'roth_decl': "About 28% on time and 42% ever, with about 38 years of work lost. This is an assumption, not a finding: the record shows the Declaration was addressed to Walter and drafted with his help, not that Britain would have withheld it from anyone else. Without that assumption, removing the family gives about 64%.",
 'roth_cascade': "About 64%, the same as removing the family alone: the map already drops what is cut off from the core, so following the cut-offs adds nothing. Most of the loss is Edmond's early money and land, about 15 years of the movement's work.",
 'roth_web_inst': "About 27% on time and 42% ever. Most of the drop in the web test comes from bodies rather than individuals, but this too assumes none of those bodies had support apart from the family, which the record does not show.",
 'pre_all': "About 72%, with about 12 years of work lost. Documented ties only. Nearly all of the drop comes from Hovevei Zion, Pinsker and Levontin, and the money and settlement of the 1880s that grew from them.",
 'roth_pre': "About 46% on time and 55% ever, with about 24 years lost. Documented ties only: nothing here assumes anyone else would have vanished. The loss is the founding decades: Edmond's colonies and money, and the first organizers.",
 'roth_herzl_pre': "About 23% on time and 39% ever, with about 31 years lost. Documented ties only. Without Herzl the same removal gives about 46%: the extra drop is his, because the movement he organized carried the money and land work that came after.",
 'pre_trigger': "About 76% on time, with about 9 years lost. This is an assumption: the sources say Hovevei Zion and Auto-Emancipation were founded in response to the pogroms, so the test removes them with the events. The loss is the movement's first decade.",
 'pre_new_all': "About 76%, with about 9 years lost. Almost all of it is the 1881 pogroms and the May Laws: they are documented causes of Hovevei Zion, BILU and Pinsker's Auto-Emancipation, so taking them out weakens the first organizers. The other nodes added from outside sources carry little weight.",
 'pre_pogroms_1881': "About 83%, with about 5 years of work lost. The pogroms are documented causes of Hovevei Zion, BILU and Pinsker's Auto-Emancipation; without them those bodies keep only their other causes, and the movement's first years are weaker.",
 'pre_may_laws': "About 91%, with about a year lost. The May Laws are one of the documented causes of Hovevei Zion and BILU, beside the pogroms, so removing them alone weakens the first organizers only a little.",
 'ottoman_neutral': "About 37% on time and 48% ever: unlikely, with about 26 years lost. Without the Ottoman entry into the war there is no British conquest, no Declaration and no Mandate, and immigration and settlement stay at the Ottoman-era pace. It is one of the largest single contingencies on the map.",
 'media_campaign': "About 92% on time, down from about 93. Truman wrote that he had never faced as much pressure and propaganda, but on this map the campaign is one source of legitimacy among several, and the founding does not depend on it.",
 'yishuv_inst': "About 79% on time, with about 8 years lost. These institutions gave the Yishuv a government, a shared language, universities, medicine and trade unions; without them the organization and money channels are weaker, but the movement abroad and the Mandate still carry the founding, later.",
 'case_secular': "About 62% on time and 67% ever: possible, with great difficulty, about 8 years late. With its political leaders absent, the religious Zionist bodies and outside support carry part of the work, but the movement's land held and its organization fall to about half.",
 'case_empire_bank': "About 15% on time and 34% at any later date, with about 38 years of work lost: unlikely. Britain alone leaves about 32%, the Rothschild family alone about 64%; together they take the framework and the early money and land at once.",
 'case_us_gov': "About 36% on time and 54% at any later date: unlikely. American money and arms still flow, but without the American government the UN vote, recognition and diplomatic backing fall away, and on this record those weigh more than the money.",
 'm_roth': "About 79%, with about 6 years of work lost: still likely, but delayed. Edmond's money came first: from 1882, when almost no one else was paying, it bought the land and built the colonies, and the colonies and PICA go with it. But it is about 11% of the money the map now counts, and from 1919 private and immigrant capital and the fund drives brought far more. Removing Edmond entirely, money and actions, gives about 70%.",
 'm_wealthy': "About 79%, about 6 years late. Almost all of the effect is the Rothschild money; the other wealthy donors together move the figure by less than a point.",
 'm_us': "About 91%: almost no change. American money is about 12% of the money on the map, about as much as Edmond's, but most of it came late, in the 1940s, after the ground was built. Meyerson's $50 million in 1948 was raised for arms when the state was months away.",
 'm_haavara': "About 93%, no change. The transfer brought a large sum in the 1930s, about 4% of the money on the map, but the state did not depend on it.",
 'm_own': "About 88%, about 2 years late. The movement's own funds, with the JNF's collections and the wartime fund drives, are about a fifth of the money on the map: real and widely given, but not what the founding depended on. Unrecorded giving is not counted, so this most likely understates them.",
 'm_only_roth': "About 13% on time and 16% ever: not possible on this record. One family's money came first and mattered most in the early decades, but on its own it is about a tenth of what the founding cost.",
 'm_only_us': "About 13% on time and 19% ever: not possible on this record. The American money came late, and on its own it cannot carry the founding.",
 'm_only_own': "About 28% on time and 35% ever: unlikely. With the JNF's collections and the wartime drives the movement raised about a fifth of the money itself, not enough to pay for a state.",
}
for k, v in READ.items(): set_field(k, 'read', v)
for a, b in [("About 1% on time and 14% at any later date: not possible on this record. With the three removed", "About 1% on time and 13% at any later date: not possible on this record. With the three removed"),
             ("About 1% on time and 16% at any later date: not possible on this record. The movement had money", "About 1% on time and 14% at any later date: not possible on this record. The movement had money"),
             ("About 77% on time, three years late.", "About 78% on time, about four years late."),
             ("the chance falls to about 32% (54% ever)", "the chance falls to about 36% (54% ever)"),
             ("About 83%, and the founding is delayed by about two years.", "About 81%, and the founding is delayed by about two years.")]:
    rep(a, b)
WHAT = {
 'm_all': "Every money tie on the map, about $1.38 billion in 1948 dollars from 1882 to 1948 (about $19.3 billion in today's dollars, each sum converted from the year it was given): the Rothschild colonies, the fund drives, the Haavara transfer, private and immigrant capital, the JNF's collections, the Jewish Agency's wartime budget, Hadassah, the 1948 tour, the movement's dues and tins. The people, the land, the arms, the diplomacy and the organisation all stay.",
 'm_roth': "The money of Edmond de Rothschild and his son James Armand: the colonies from 1882, the land company PICA, \"over sixty million dollars\" by 1934 at 1913 prices, about $2 billion in today's dollars. About 11% of the money on the map. What the money built, the colonies and PICA, goes with it; the family's other ties stay.",
 'm_wealthy': "Every individual donor of wealth on the map, among them Edmond and James de Rothschild, Jacob Schiff, Felix Warburg, Israel Sieff, Simon Marks, Alfred Mond and Nathan Straus. About 11% of the money on the map.",
 'm_us': "The American fund drives (the United Palestine Appeal, the United Jewish Appeal, the Joint Distribution Committee), Hadassah, Golda Meyerson's 1948 tour, the arms buyers and the American donors. About 12% of the money on the map, about as much as the Rothschilds'.",
 'm_haavara': "The Haavara agreement of 1933 between Zionist bodies and the German economics ministry, which let German Jews move about 105 million Reichsmarks, about $35 million, as German goods through the Anglo-Palestine Bank. About 4% of the money on the map.",
 'm_own': "The shekel membership dues, the Jewish Colonial Trust, the Jewish National Fund's collections and its Blue Box tins, Keren Hayesod, the Kofer HaYishuv defence levy, the wartime fund drives and the Jewish Agency's own funds. About 21% of the money on the map.",
}
for k, v in WHAT.items(): set_field(k, 'what', v)
# the money groups take in the new streams; two private-capital tests
rep("const VM_OWN=['shekel','jct','jnf','blue_box','keren_hayesod','kofer','jewish_agency','herzl','sacher'];",
    "const VM_OWN=['shekel','jct','jnf','blue_box','keren_hayesod','kofer','jewish_agency','herzl','sacher','jnf_collections','wartime_appeals'];\nconst VM_PRIV=['private_capital_interwar','private_capital_war'];")
rep("const VM_US=['upa','uja','jdc','meir',", "const VM_US=['hadassah_members','upa','uja','jdc','meir',")
NEW = (" {id:'m_private', q:'What if no private and immigrant capital had come?', drop:()=>vMoneyDrop(e=>VM_PRIV.includes(e[0])),\n"
       "  what:'" + js("The money Jewish immigrants brought with them and private investors sent: about P£75 million from 1919 to 1939 and about P£19 million in 1940-44, estimated from documented totals (three-quarters of Jewish capital imports between the wars were private, about half in the war years). About 52% of the money on the map, the largest single stream.") + "',\n"
       "  read:'" + js("About 70% on time, with about 5 years lost: still likely, but delayed. Private and immigrant capital built the Jewish economy of the 1920s and 1930s, its groves, building and industry. The founding survives without it because the movement's funds, the Rothschild money and the American appeals remain, but later.") + "'},\n"
       " {id:'m_only_private', q:'What if private and immigrant capital had been the only money?', drop:()=>vMoneyDrop(e=>!VM_PRIV.includes(e[0])),\n"
       "  what:'" + js("Every documented money tie except private and immigrant capital: the Rothschild money, the fund drives, the Haavara transfer, the movement's own funds.") + "',\n"
       "  read:'" + js("0%, at any date: not possible. Private capital arrived only from 1919, so the founding decades have no money at all, and the movement's own institutions have nothing to run on.") + "'},\n")
rep(" {id:'m_only_roth',", NEW + " {id:'m_only_roth',")
i = s.find("function vMoneyList(){"); j = s.find("<p class=\"vtxt\">", i); k2 = s.find("</p>", j)
s = s[:j] + "<p class=\"vtxt\">" + js("The map records about $1.38 billion in 1948 dollars flowing into the founding from 1882 to 1948, about $19.3 billion in today's dollars when each sum is converted from the year it was given: about $647 million in sums the record states (about $9.1 billion today), about $709 million of private and immigrant capital estimated from documented totals (about $9.9 billion today), and about $20 million assumed at $1 million or less for each tie whose sum the record does not give. These tests take money out by its source, or keep only one source, while the people and their other ties stay; what the money itself built goes with it. Taking out all of it gives 0% by the map's own design, since a state needs money as it needs arms; the tests after it show which money mattered, and why timing counts as much as size.").replace("\\'", "'") + s[k2:]
# Edmond removed entirely
EDA = (" {id:'edmond_all', q:'What if Edmond de Rothschild had never been in the picture, his money and his actions together?', ids:()=>['edmond_r'],\n"
       "  what:'" + js("Edmond de Rothschild and everything the record ties only to him: his money, the colonies he rescued and founded from 1882, the Carmel wine company, PICA (which he founded and paid for in 1924), his dealings with the Ottomans and his part in the Jewish Agency. His son James and the rest of the family stay.") + "',\n"
       "  read:'" + js("About 70% on time, with about 13 years of the movement's work lost: still likely, but delayed. From 1882 he was nearly the whole effort, and his colonies were part of the base the Second Aliyah came to; without them those years are lost, and the later farm money that stood on his land is weaker. How much being first should weigh is a choice the record cannot settle: counting each year by its worst-hit area of work instead of all of them together gives about 40% and 35 years. Herzl, removed the same way, gives about 69%: the founders of the movement's politics and of its first ground count about the same.") + "'},\n")
rep(" {id:'edmond',", EDA + " {id:'edmond',")
for _a, _b in [("whether the strongest documented actor on the same side, already founded, could have done it:", "whether the strongest documented actor from the same circle, already founded, could have done it (another Zionist leader for a Zionist leader, another Rothschild for a Rothschild):"),
               ("A channel starts counting once its record reaches 5% of its 1948 total, because before that the record is too thin to say a year was lost", "Every year counts, from 1882, the first"),
               ("A year counts as lost in proportion to the worst-hit channel's shortfall", "A year counts as lost in proportion to the share of the movement's work, all channels together, that is missing; and what grew from a removed part (the funds the Zionist Organization founded, the farm money planted on a landowner's land) weakens with it")]:
    s = s.replace(_a, _b)
s = s.replace('Its own share of the network: ', 'Share of each channel lost with it, counting what depended on it: ')
s = s.replace('/* ---------- survival model', '/* nov27_texts */\n/* ---------- survival model', 1)
open(P, 'w', encoding='utf-8').write(s)
print('test texts updated')
