#!/usr/bin/env python3
"""Record corrections to the simulation's scene, card and deep-dive text (index.html), October 2026.

Found by the Volume II Rothschild research (book/research/vol2_wealth_*.json) and a reader's challenge
("who was the first Zionist?"):
- Herzl's "At Basel I founded the Jewish State" was glossed as "it did not exist as a political project
  before that"; the idea and the settlement societies were older (Alkalai from the 1840s, Hovevei Zion
  from 1882). Basel created the organized international movement.
- The Rothschilds' capital "around 1875" was given as £8-10 million; Ferguson's figures (via reviews) are
  £9.5m in 1852 and £34m in 1874.
- Walter Rothschild: his presidency of the Zionist Federation is disputed; he was not "politically
  inactive" (he sent the July 1917 draft and objected to a safeguard); the Chief Rabbi story and the
  "diaries at Tring" claim are unsourced; Weizmann was not WZO president in 1917.
- Edmond de Rothschild opposed Herzl's political Zionism, but not "at the 1897 Congress".
- A new FAQ answer: who was the first Zionist?
Idempotent. Run after embed_book.py and before simplify_ux.py. Usage: python3 tools/patch_record_fixes.py [index.html]"""
import sys

P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if 'RECORDFIX-2026-10' in s:
    print('record fixes already applied'); sys.exit(0)

def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('found %d time(s), expected %d: ' % (s.count(old), count)) + old[:110]
    s = s.replace(old, new)

BASEL = ("Founded — his word. The idea was older: from the 1840s the Sephardi rabbi Yehuda Alkalai urged settlement in the land, "
         "and from 1882 the Hovevei Zion societies organized it [cite:w_alkalai] [cite:w_hovevei]; what Basel created was the organized, international political movement.")
swap("Founded — his word — meaning it did not exist as a political project before that. Full scene at [4].", BASEL + " Full scene at [4].")
swap("Founded — his word — meaning it did not exist as a political project before that moment.", BASEL)

# capital and papal loans (deep dive)
swap("This is documented in Vatican financial archives and is one of the historical curiosities of the era",
     "Historians document these loans, one of the historical curiosities of the era")
swap("<p>Ferguson's scholarship documents that by around 1875 the collective Rothschild capital was roughly equivalent to £8-10 million (about £1 billion in modern equivalent — substantial, but not the \\\"half of world wealth\\\" of the mythology).",
     "<p>On Niall Ferguson's figures, as reviews of his history report them, the combined capital of the houses was £9.5 million in 1852 and £34 million in 1874, after which it grew little — very large for its day, but not the \\\"half of world wealth\\\" of the mythology.")

# s06: Lord Walter Rothschild
swap("The Balfour Declaration was formally addressed to him specifically because he held the presidency of the British Zionist Federation at the time — a position of symbolic representation rather than one reflecting deep personal involvement in drafting or negotiating the letter's content, which was handled primarily by Chaim Weizmann and Nahum Sokolow.",
     "The letter was addressed to him, for passing on to the Zionist Federation, chiefly because of his standing: the Rothschild Archive calls him the unofficial leader of the British Jewish community, and the community's elected leaders had publicly opposed political Zionism in May 1917. Some accounts say he presided over the British Zionist Federation; others give that office to Weizmann, so the point is disputed. He was not a bystander: he sent Balfour the Zionist draft of July 1917 and objected to one of the final safeguards. The drafting and negotiation were handled primarily by Chaim Weizmann and Nahum Sokolow.")
swap("chosen for a specific, documented institutional reason — his Federation presidency — not for personal political influence",
     "chosen for documented reasons — his standing as the recognized head of British Jewry, and possibly a Federation office the sources dispute — not for personal political influence")
swap("and who separately opposed Herzl's political Zionism at the 1897 Congress", "and who separately opposed Herzl's political Zionism")

# s01: Lord Walter Rothschild
swap(" His personal correspondence and diaries — held at the Natural History Museum, Tring — show a man far more animated by ornithology than by international politics.",
     " His life's work was zoology, not politics; he left the family bank in 1908 to pursue it.")
swap("<p>The choice of recipient for the November 2, 1917 letter was political theater. Britain needed the letter to <em>appear<\\/em> to be addressed to \\\"the Jewish people\\\" via a representative figure. Walter Rothschild was chosen because:<\\/p><ol><li><strong>Highest-visibility Rothschild in Britain.<\\/strong> The family name carried public weight; his title (2nd Baron) gave it institutional gravitas.<\\/li><li><strong>Politically inactive.<\\/strong> He would not push back, negotiate terms, or insert himself into policy. He would sign for receipt.<\\/li><li><strong>Symbolic association with Jewish leadership.<\\/strong> Both Chaim Weizmann and other Zionist figures had cultivated his sympathies as honorary president of the British Zionist Federation from 1915. But he was not the drafter.<\\/li><li><strong>Available.<\\/strong> The alternative — addressing the letter to the Chief Rabbi of Britain, Joseph Hertz — was rejected because Hertz was theologically Orthodox and might complicate the secular political framing.<\\/li><\\/ol><p>The letter appeared over Balfour's signature. It was drafted by Weizmann, Sokolow, and Sykes over nine months. It served three named British imperial interests (Suez / Russia / US mobilization). Walter Rothschild's role was to receive it.<\\/p>",
     "<p>The record gives these reasons for the address line, and leaves one question open:<\\/p><ol><li><strong>Rank and name.<\\/strong> He inherited the title in 1915, and with it, in the Rothschild Archive's words, the place of unofficial leader of the British Jewish community. The government wrote to the head of British Jewry by rank, not to an elected leader.<\\/li><li><strong>The elected leaders were opposed.<\\/strong> In May 1917 the presidents of the Board of Deputies and the Anglo-Jewish Association publicly opposed political Zionism; the Board then censured their statement, 56 votes to 51, and its president resigned.<\\/li><li><strong>The Zionists had no address.<\\/strong> Nahum Sokolow is quoted as saying the Zionists had no address while Walter had a very fine one, at 148 Piccadilly. Weizmann, an immigrant chemistry lecturer, was not the movement's most senior figure.<\\/li><li><strong>What officials believed.<\\/strong> Historians such as Jonathan Schneer document that British ministers believed, wrongly, in a Jewish financial and political power they hoped to win over; the Rothschild name stood for it in their minds. No record shows a payment or loan in exchange for the letter.<\\/li><\\/ol><p>He was not a bystander: he sent Balfour the Zionist draft of July 1917 and objected to one of the final safeguards. Whether he also presided over the British Zionist Federation is disputed. The final text was negotiated by Weizmann, Sokolow and Sykes and appeared over Balfour's signature, in service of British imperial interests (Suez / Russia / US mobilization).<\\/p>")
swap("<span>Russian-born chemist · WZO president · drafted<\\/span>", "<span>Russian-born chemist · Zionist leader in Britain · drafted<\\/span>")
swap("<span>Received it. Passed it to the WZO.<\\/span>", "<span>Sent the July draft; received the letter for the Zionist Federation.<\\/span>")
swap("<p>Walter is <em>fifth<\\/em> in the chain — the terminal recipient.", "<p>Walter is <em>fifth<\\/em> in the chain — the recipient, though he had offered an early draft that ministers cut back.")
swap("<td class=\\\"dd-attr\\\">Position on Herzl?<\\/td><td>Distant / uninvolved<\\/td>", "<td class=\\\"dd-attr\\\">Position on Herzl?<\\/td><td>Not documented here<\\/td>")
swap("<td class=\\\"dd-attr\\\">Zionist role<\\/td><td>Honorary; ceremonial<\\/td>", "<td class=\\\"dd-attr\\\">Zionist role<\\/td><td>Sent the July 1917 draft; Federation office disputed<\\/td>")
swap(" — the recent AIPAC-connected legislative pattern documented in FEC filings.<\\/li>", ".<\\/li>")
swap("It shows Walter Rothschild as terminal recipient of a document drafted by others, in service of imperial interests he did not set, addressed to him for reasons of symbolic representation.",
     "It shows Walter Rothschild as the recipient of a document whose final text others negotiated, in service of imperial interests he did not set, addressed to him for his standing; he had offered an early draft.")
swap("He did not do this. He signed for the envelope.", "He did not do this alone, and he did not write the final text.")
swap("Walter did not shape policy. His cousin Edmond", "Walter did not set the policy; ministers cut back the draft he sent. His cousin Edmond")

# FAQ: who was the first Zionist
swap("""  {q:'How did President Truman come to recognize Israel, and why so fast?',""",
"""  {q:'Who was the first Zionist? Wasn\\'t it Herzl?', /*RECORDFIX-2026-10*/
   a:'Not Herzl. The call for an organized return came decades before him. From the 1840s Yehuda Alkalai, a Sephardi rabbi in Semlin near Belgrade, urged practical settlement in the land as a step toward redemption; in 1862 Rabbi Zvi Hirsch Kalischer and the socialist Moses Hess made their own cases; after the pogroms of 1881-82 Leon Pinsker called for a territory of their own, not necessarily Palestine, the Hovevei Zion societies and the BILU pioneers organized, and Edmond de Rothschild began funding colonies in 1882. Nathan Birnbaum coined the word Zionism in 1890. What Herzl built, at Basel in 1897, was the organized international movement, with its own congress, diplomacy and bank, and even then Palestine was not the only option: he weighed Argentina, and the movement debated a British offer in East Africa in 1903. Who came first moves the start date; it does not change how the state was built.',
   scenes:['ideo_s01','s03','s04']},
  {q:'How did President Truman come to recognize Israel, and why so fast?',""")

open(P, 'w', encoding='utf-8').write(s)
print('record fixes applied')
