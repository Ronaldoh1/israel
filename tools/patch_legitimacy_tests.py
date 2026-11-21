#!/usr/bin/env python3
"""Adds the legitimacy and central-bank tests to the Road to 1948 map's Tests panel and updates the
theology test's reading. Run after patch_legitimacy_channel.py. Idempotent.
Usage: python3 tools/patch_legitimacy_tests.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if "id:'legit_holocaust'" in s:
    print('legitimacy tests already applied'); sys.exit(0)
old_read = "read:'About 92%: as mapped, organized Christian Zionism was a small direct contributor."
new_read = "read:'About 90%: as mapped, organized Christian Zionism was a modest direct contributor. Since November 2026 its documented push (Blackstone\\'s 1916 memorial to Wilson, and the Christian committees\\' work for the 1945 congressional resolution) counts in the legitimacy channel; the 1891 Memorial carries no weight because the record states no route from it to the founding bodies."
assert s.count(old_read) == 1
s = s.replace(old_read, new_read)
anchor = " {id:'un', q:'What if the UN vote had never happened?'"
assert s.count(anchor) == 1
tests = r""" {id:'legit_holocaust', feat:true, featTag:'Featured test · legitimacy channel', q:'What if there had been no Holocaust survivors\' case to make: no camps of survivors, no Harrison Report, and no inquiries that followed?',
  ids:()=>['holocaust'],
  what:'The Holocaust as the map holds it, which is only through its documented legitimacy ties: the Jewish displaced persons, the Harrison Report of August 1945 and its route to Truman, the Exodus survivors and the UN committee\'s visits to the camps and to Haifa. The displaced persons and the Harrison Report fall with it. Everything else stays, including Truman, the Exodus operation and the UN committee.',
  read:'About 87% on time, down from about 93. This measures one thing: the legitimacy the survivors\' case lent the founding, as the record ties it to Truman, the Anglo-American Committee and the UN committee. It cannot measure how the Holocaust changed everything else (immigration, money, arms and the will of the movement itself), so it is a floor, not the Holocaust\'s full weight.'},
 {id:'legit_christian_us', q:'What if American public and Christian support had been absent: no Christian committees, no Blackstone memorials, no congressional endorsements?',
  ids:()=>['apc','ccp','acpc','blackstone','blackstone_1891','lodge_fish'].filter(x=>N.get(x)),
  what:'The American Palestine Committee, the Christian Council on Palestine and their 1946 merger, William Blackstone and his memorials of 1891 and 1916, and the 1922 Lodge-Fish resolution. The 1945 congressional resolution and Truman stay.',
  read:'About 88% on time. The Lodge-Fish resolution also carries diplomatic weight, so part of the drop is diplomacy, not legitimacy alone.'},
 {id:'haavara_out', q:'What if the Haavara transfer agreement had never been made?',
  ids:()=>['haavara'],
  what:'The 1933 transfer agreement with Nazi Germany under which about 60,000 German Jews moved part of their capital to Palestine, 105 million Reichsmarks by 1939. The Reichsbank, Germany\'s central bank, supplied about £P2.6 million of the £P8.1 million transferred, roughly a third; the map cannot separate that share, so this test removes the whole transfer.',
  read:'About 91% on time: the transfer was a real but modest share of the movement\'s money. This is the only documented route by which a central bank\'s money reached the movement before 1948.'},
 {id:'central_banks', q:'What if every central bank with a documented tie had stayed out?',
  ids:()=>['reichsbank','banque_france','pcb','fed','fed_act','bank_england'].filter(x=>N.get(x)),
  what:'The Reichsbank, the Banque de France, the Palestine Currency Board, the Federal Reserve and its founding act, and the Bank of England. The Haavara transfer itself stays, since it was made with the Reich Economics Ministry and run through the Anglo-Palestine Bank.',
  read:'About 93%: the central banks themselves carry almost no weight: the Federal Reserve has no documented tie to the movement\'s funds, the Bank of England none to its decisions, and the Banque de France connects only through a Rothschild regent. The money that a central bank did supply, the Reichsbank\'s share of the Haavara transfer, is measured by the test above.'},
"""
s = s.replace(anchor, tests + anchor)

# UI: seven channels where the legitimacy channel applies; the other homelands are measured on the original six
for a, b, n in [("<h4>The six channels</h4>", "<h4>The seven channels</h4>", 2),
                ("<h3 class=\"vsec\">The six channels</h3>", "<h3 class=\"vsec\">The seven channels</h3>", 1),
                ("${VB.channels.map(c=>{ const [s,why]=a.share[c];", "${VB.channels.filter(c=>a.share[c]).map(c=>{ const [s,why]=a.share[c];", 1),
                ("Added from outside sources, not from the book; each tie shows its links.", "Added from outside sources; now told in the Road to 1948 prelude, Before Herzl: The First Network. Each tie shows its links.", 8)]:
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s)
print('legitimacy tests applied')
