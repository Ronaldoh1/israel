# The Road to 1948 network map, v1 (4 Nov 2026)

**This is an INSTITUTION/SYSTEM-mixed network module.** It covers the people, organizations, states, documents and events of *The Baseline* (ch01) and *The Road to 1948* (rd0–rd6), 1694–1950s. It opens from both books' library cards and from the library menu (`road-network.html`).

## How it was built

1. **Nodes: a curated registry** (`book/plan/road_map/registry.py`), 293 entries.
   - Every entry is an actor, institution, document or event, with alias patterns. Some aliases only apply within one stage, for example "Feinberg" means Abraham Feinberg only from rd4 on, because in rd2 it is Avshalom Feinberg of NILI.
   - No ethnic or religious group is a node.
   - Historians and outlets cited as sources are not nodes.
2. **Candidate ties: the book text** (`build_road.py`).
   - The script splits all ~357,000 words into sentences, and each sentence keeps its own citations.
   - Figure and table cells take the figure's source line.
   - When a sentence names two nodes next to each other with a relationship verb between them (founded, funded, led, wrote to, met, signed, opposed, expelled…), that becomes a typed candidate tie.
   - The simulation scenes' authored connections are added as further candidates.
3. **Review: every typed candidate checked by hand against its sentence** (`review.json`).
   - 434 typed candidates plus the 150 most frequent name pairs were read.
   - Each was accepted, re-typed, reversed, re-pointed to the pair the sentence actually documents, or rejected.
   - Rejections included the Federal Reserve sentence that explicitly says there is *no* link to the Zionist Organization, the "Fourth Congress" that is the Palestine Arab Congress rather than the US Congress, and the "James de Rothschild" who is James Armand (PICA) rather than James Mayer.
4. **Curated layer** (`road_layer.json`): ties the heuristic could not phrase.
   - Weizmann, Sokolow and Sykes drafted the Balfour Declaration; Balfour signed it.
   - The Third Arab Congress created the Arab Executive.
   - The Justice Department ordered the American Zionist Council to register under FARA.
   - Ben-Gurion headed the provisional government.
5. **Per-node profile** (`qop_road.py`): the same stored fields as the Epstein map.
   - Kevin Bacon distance to the two anchors.
   - Bridging rank, with and without the anchors.
   - Role, money ties, short loops.
   - Other library volumes that name the node.
   - Book sections that name it.
   - The nodes it is named together with.

**Statuses**
- *verified*: a tie the book states, with the book's citation.
- *reported*: stated in the book with no citation in that paragraph; the source links to the section.
- *co-mention*: named together in one sentence with no stated tie. These are leads only, never walked or used in any measure.

## First-pass numbers

| | |
|---|---|
| Nodes | 291: 124 people, 71 institutions, 36 governments, 26 documents, 22 events, 12 companies |
| Reviewed ties | 283 (272 sourced, 11 uncited) |
| Named-together leads | 1,129 |
| Nodes with at least one reviewed tie | 203 |
| Short loops | 44 |
| Nodes named in other library volumes | 140 |

**Anchors** (the two most-bridging nodes, chosen by the data): the **Jewish Agency** and the **World Zionist Organization**.

**Top bridges**
- With the anchors: Jewish Agency, WZO, Weizmann, Herzl, UN, Truman, Ben-Gurion, Balfour Declaration, Irgun, the Mandate.
- With the anchors removed: Herzl, the Balfour Declaration, Ben-Gurion, the UN, Truman, Weizmann, the Irgun, Judah Magnes.
- So the map holds together through the movement's two bodies, then through three documents and decisions (Balfour, the Mandate, Resolution 181 via the UN) and a handful of individuals.

## Known gaps (next pass)

- **Money is thin.** Only about 11 funding ties were stated plainly enough for the first pass. The book's money chapters (JCT, JNF, Keren Hayesod, Haavara, Sonneborn and Feinberg, the Export-Import loan) are mostly still in the named-together queue.
- **Arab and Palestinian institutions, the Ottoman side and the British administration** have fewer reviewed ties than the Zionist and American side. The cause is the heuristic, not the book: those chapters use more narrative phrasing. A review pass over those clusters should come next, so the map is not lopsided.
- **The Baseline** is mostly concepts, words and traditions, so it contributes fewer actor ties. Its dissent institutions (Bund, Reform, Neturei Karta, Satmar, Agudah) are on the map.
- **Next step:** review the remaining named-together pairs cluster by cluster and promote the real ties.

## The American layer (4 Nov 2026)

Built by `book/plan/road_map/us_layer.py`, which writes `us_layer.json` (ties) and `book/research/road_us_layer.json` (26 sources). The run added 70 nodes to the registry and 133 curated ties, plus 21 book-sentence ties reviewed in `review.json`. Result: 373 nodes; 430 sourced ties, 35 stated in the book or by a named secondary account, and 1,189 "named together" leads.

**Sub-networks**

1. **US Zionist organizations, 1897–1948**
   - Federation of American Zionists (Gottheil, Wise), then Brandeis's wartime committee, then the ZOA.
   - American Palestine Committee (Neumann, 1932; ZOA-funded; two-thirds of the Senate as members), merged in 1946 into the American Christian Palestine Committee.
   - JDC and the 1914 Relief Committee (Schiff, Felix Warburg, Louis Marshall).
2. **FARA**
   - 1939: Jewish Agency registration (reported by IRmep).
   - 25 Feb 1948: order to the ZOA, dropped after it changed its constitution.
   - 1962: order to the American Zionist Council, and its tie to AIPAC (later).
3. **Intelligence**
   - Shiloah: Jewish Agency Political Department (1936); OSS ties in the Second World War; arranged the Sonneborn meeting; named by Ben-Gurion in 1949; first head of the Mossad (1951).
   - Kollek: liaison to MI5; Haganah representative in Washington, 1947–48; Hotel Fourteen; Angleton, 1950.
   - FBI under Hoover: Americans for Haganah, the Voorhis Act and the Neutrality Acts, 1947–48.
   - Schwimmer: convicted in 1950.
   - Lansky, Siegel and Cohen (reported, Rockaway/Tablet).
4. **1944 convention**
   - Hannegan, Walker, Pauley, Flynn, Kelly, Allen; Byrnes passed over; Roosevelt's letters; ballot results.
   - No Zionist or Jewish organization is named in the record of the swap.
5. **White House and State Department, 1945–48**
   - Roosevelt's letter to Ibn Saud of 5 Apr 1945.
   - Policy Planning Staff report of 19 Jan 1948: oil, the Soviets, and the view that partition "cannot be implemented without the use of force".
   - The 12 May 1948 meeting (Marshall: "I would vote against the President").
   - Recognition at 6:11 p.m. on 14 May.
   - Administration notes on lobbying Liberia, Haiti and the Philippines before the vote.
   - Export-Import Bank loan of $100M (reported, Aug 1948).
6. **Money**
   - Rothschild agents in America: Phillips, Cohen, the Josephs, then Belmont from 1837. Belmont chaired the DNC, 1860–72.
   - 1895 Morgan–Belmont gold contract.
   - Kuhn, Loeb under Schiff.
   - Jekyll Island (1910), the Aldrich Plan, the Federal Reserve Act (1913), Paul Warburg on the Board (1916–18).
   - The Baseline's s04ga finding stands: no documented institutional or financial link between the Fed and the Zionist Organization or its funds.

**1917–19 groundwork**
- Brandeis as Weizmann's channel to Wilson (Barda 2022, a working paper).
- Lansing's letter of December 1917 and Wilson's "very unwilling" agreement.
- The Faisal–Frankfurter letter of 3 Mar 1919.

**Open leads for the next pass**
- The Jewish Agency's 1939 FARA filing itself.
- OSS files on the Jewish Agency.
- Bernstein's FBI file.
- Aramco and the oil companies' lobbying, 1947–48.
- Baruch and other figures alleged to have pressed delegations at the UN.
- Morgenthau Jr. and the War Refugee Board.
- Christian Zionist organizations after 1946.

## The world layer (4 Nov 2026, second pass)

Built by `book/plan/road_map/world_layer.py`, which writes `world_layer.json` and `book/research/road_world_layer.json`. The pass added 55 nodes and 115 ties; most cite the book's own sources, plus 6 new outside sources. 33 extractor candidates were reviewed. Result: 425 nodes, 554 sourced ties, 44 reported.

**Congress**
- 1922 Lodge–Fish resolution: Glazer's lobbying, the State Department's opposition, Harding's signature, and Sokolow's meeting with Harding.
- 1944: the Wright–Compton and Wagner–Taft resolutions; the Emergency Council's letter campaign; Lazaron's opposition; deferrals by Marshall, Stimson and the State Department; Stimson's letter to Taft.
- Both 1944 platforms: Taft and Silver (Republican), Celler and Wise (Democratic).
- The 1945 concurrent resolution; Bloom and Celler.
- No documented money from Zionist organizations to members of Congress before 1948 was found. That is stated in the node note.

**Watchers**
- Bergson's committee registered under FARA (June 1944).
- The FBI investigated at the State Department's request; Waldman and Goldmann urged Bergson's deportation.
- The OSS Palestine desk.
- The Shai (1940).

**Arms**
- Transit through Czechoslovakia, Panama, Mexico, Canada and France: 800 shipments, about 2,400 tons.
- Schwimmer's two cover airlines; the Winters and Greenspun convictions and pardons.
- Meyerson's $50M.
- Czechoslovakia: Operation Balak from Žatec (Zebra) to Nikšić in Yugoslavia; the Avia fighters; Široký's figure of $14.5M; Stalin's consent.
- Nicaragua: $3M in letters of credit.
- France's secret arms for the Altalena (153M francs, approved by Bidault).
- Britain's supply to the Arab air forces.

**Aliyah Bet**
- The Mossad LeAliyah Bet (1938); Brihah through Italy, France, Yugoslavia and Greece; the Exodus; the Cyprus camps.

**UN vote and recognitions**
- Gromyko (May 1947); the USSR's vote and its de jure recognition (17 May 1948).
- Aranha's postponement; pressure on Haiti, Liberia and the Philippines (Firestone reported); Romulo; Cuba.
- UNSCOP's eleven members and Sandström; García Granados's Latin American lobby; Guatemala first in Latin America.
- Britain's recognition (Jan 1949).

**Before 1948**
- The Cambon letter (June 1917).
- Poland–Irgun arms and training, 1937–39 (reported, from the Irgun's own history).
- Smuts and the Balfour drafting; South Africa's recognition.

**Conflicts kept visible**
- The ZOA FARA order of 1948 (Wikipedia) against the book's statement that the apparatus was not asked to register before 1962.
- Schwimmer's pardon year: 2000 or 2001.
- Winters's pardon: Bush 2008, or Clinton 2001.

## The Cold War layer (4 Nov 2026, third pass): the map now runs to June 1967

**What changed**
- The corpus now includes The Cold War Architecture (cw1–cw6), 99 sections. The map is retitled "The Road to 1948 and After" and is linked from the Cold War volume.
- 65 Cold War nodes were added to the registry.
- `cold_layer.py` writes `cold_layer.json` (75 ties) and `book/research/road_cold_layer.json` (6 new sources). Its ties mostly cite the Cold War volume's own keys.
- 225 extractor candidates were reviewed: 69 accepted, the rest kept as named-together leads.
- Result: 487 nodes, 689 sourced ties, 47 reported.

**Money: who paid for the new state**
- US aid, 1949–59: $652.9M, economic only.
- Israel Bonds (1951): $52M in the first year, and 35% of the development budget within six years.
- Luxembourg reparations: $845M, or 3.5bn plus 0.45bn marks.
- The first US grant (1951): $65M or about $68.8M. Douglas and Taft sponsored it, and Kenen worked the Senate floor; Feinberg went to McGhee "at the Suggestion of the President".
- The Bank of Israel (Knesset law, 24 Aug 1954; state-owned; Horowitz governor; succeeded the Anglo-Palestine Bank's note issue).
- The Knesset building, from a £1.25M James de Rothschild bequest (1966).

**The lobby and FARA**
- Kenen founded AIPAC's predecessor (1951/53/54); Eban suggested the move (reported).
- 1962: the DOJ order to the AZC under RFK, never enforced to completion.
- Jewish Agency money to the AZC: $5,100,001.02, 1955–62 (Senate record), against Barda's figure of $1.5M.
- 1963: the Fulbright inquiry, Part 9 (Hammer, Boukstein, Neumann). The American Section was already a FARA registrant.
- The Near East Report was funded through Council purchases.

**Intelligence**
- Ben-Gurion's 13 Dec 1949 directive founding the Mossad.
- Harel at the Shin Bet; Aman.
- Angleton's control of the CIA's Israel account from 1954.
- Operation Susannah (1954), which targeted US information libraries in Cairo and Alexandria.

**Nuclear**
- Peres was delegated the programme in 1955; France supplied the reactor (1956).
- The Kennedy–Ben-Gurion and Kennedy–Eshkol letters (1963); Johnson's continued pressure.
- NUMEC (Shapiro): 93.8 kg of U-235 unexplained. The CIA's 1968 sampling report near Dimona is reported; the evidence is "strong but not incontrovertible."
- Bar-Joseph's claim that Germany was the "major funder" of Dimona is contested.

**German arms**
- Peres and Strauss (1957); Adenauer's 240M DM list (1962); 150 M48 tanks with US kits (1964).

**Oil**
- Max Ball and Eliahu Epstein (1948). Gendzier: "not oil versus Israel but oil and Israel."

**Advocacy around 1948**
- The Nation Associates (Kirchwey) dossiers to the UN on the Arab Higher Committee's Axis ties (May 1947) and on Farouk (June 1948).

**JFK**
- The node note gives the documented disputes.
- The Warren Commission and the HSCA identified no link to the assassination. Cohen and Hersh draw none. The book (s11c) treats the date as timing only, and the map records it as a date, not a tie.

**Rothschild after 1948**
- The node note on James Armand: visible institutions only (PICA to the JNF, Yad Hanadiv, the Knesset building). No document shows Rothschild ownership or control of the Bank of Israel.

## Whole-network view and the historical layer (4 Nov 2026, fourth pass)

**View.** Ron saw about 20 nodes because the map opened on Herzl at depth 1. The template now has an "All" depth and a "Whole network" button, and the Road map opens on the whole documented network: 482 nodes and 859 ties on screen. Hub labels scale with zoom. The Epstein map keeps depth 1 by default but gains the same button.

**Layers and names**
- `history_layer.py` adds 99 ties and 11 sources:
  - The Rothschild family and its five houses: Frankfurt, Vienna, London, Naples, Paris. This covers the generations to Victor and Guy.
  - Lionel in the Commons (1858) and the Suez Canal loan; Natty's peerage (1885).
  - Lionel Nathan's anti-Zionist League of British Jews (1917).
  - Chamberlain and the Uganda offer.
  - The War Cabinet and the drafters of the declaration: Milner, Amery, Ormsby-Gore, Curzon's memo, Cecil, Graham, the Montagu memo, the Samuel memo.
  - San Remo: Lloyd George, Curzon, Millerand, Berthelot, Nitti, Matsui, Hankey.
  - All the High Commissioners.
  - The Vatican: Agliardi, Merry del Val, Pius X, Benedict XV, Gasparri's note against the Mandate, Pacelli/Pius XII, Tardini, Maglione, Paul VI.
- A name pass over all three volumes added about 60 actors the books name: Komer, Bundy, Rostow, Byroade, Harman, Couve de Murville, Pineau, Bourgès-Maunoury, Szold, Lipsky, Golomb, Tehomi, Shamir, Rosenwald, Weitz, Kaufmann, Lowenthal, Gibli, Bergmann, Globke and others.
- 62 more candidates were reviewed.

**Result.** 588 nodes; 815 sourced ties plus 57 reported (872 documented); 493 nodes with at least one documented tie. For comparison, the Epstein map has 419 nodes and about 800 ties.

## Pass: removal model v2 (Nov 2026)

What the "Remove a node" tool computes now:
- **Money is weighted in 1948 dollars** where the record states a sum: Golda Meyerson's 1948 tour (about $50M), Edmond de Rothschild's 15M francs to the JCA in 1899 (about $8.7M in 1948 dollars), Nicaragua's $3M letters of credit, Schiff's $50,000 in 1914, Cohen's and Siegel's roughly $50,000 each. Money ties with no stated sum are assumed at $1M. That is a disclosed assumption. Money that didn't go to the project is left out (Rothschild loans to the British treasury, the Suez purchase, the Ottoman sale to the Sursocks).
- **Every removal is recalculated** across the whole network. A tie only counts if it still connects to the state-building core.
- **Probability per channel:** 1 − e^(−k·C/C₀), calibrated so the full record gives 99% per channel. Overall chance = the product of the five channels (95% on the full record).
- **Delay:** the lost share of each channel is rebuilt at the pace it was first built. The delay shown is the longest of the five.

Readings:

| Removed | Chance | Rating | Rebuild delay | Weakest channel |
|---|---|---|---|---|
| Rothschild family and houses | 90% | Still possible, with more work | about 16 years | land |
| Without the United States | 56% | Possible only with major outside help | about 37 years | money: $22M of $79M left |
| Zionist movement leadership | 54% | Doubtful | | |
| Armed groups | 0% | Not possible on this record | | |
| Golda Meyerson alone | 78% | | | |

## Pass: funding layer and model v3 (5 Nov 2026)

New funding ties (funding_layer.py, 23 ties, live sources):
- **Herzl:** paid for Die Welt himself (1897). The movement's own money came from shekel dues and the Jewish Colonial Trust share sale (£2M of capital, over 100,000 applicants by May 1899). Hirsch, Albert Rothschild and Edmond declined to fund his plan.
- **Keren Hayesod:** £4,714,440 from 1921 to 1932, about half of it from the US.
- **UJA:** $102M in 1946 and $150M in 1948. The UPA's share was $52M in 1946 and $74.7M in 1948.
- **Edmond de Rothschild:** "over sixty million dollars" invested in Palestine (JTA, 1934). PICA held about 500,000 dunams.
- **Smaller funds:**
  - JNF: 936,000 dunams by statehood.
  - Nathan Straus: $100,000 to the UPA, directed to Hadassah (1928), and $10,000 (1924).
  - Kofer HaYishuv: a levy from 1938 that funded the Haganah.
  - JDC: capital for the Palestine Economic Corporation (1925).
- **The Balfour Declaration:** the 1924 Anglo-American Convention gave US consent to the Mandate, which carried the declaration. Weizmann's "greatest House in Jewry" letter to Walter Rothschild is added.

Model v3:
- **Money counts twice** in the overall chance, and money ties are weighted by their stated sums in 1948 dollars. Pass-through money is counted once.
- **Connections count:** each non-money tie is multiplied by how connected its two ends are (1× to 2×).
- **Documents need force:** a document loses its force when every body that issued or signed it is removed.
- Full record = 94%.

Readings:

| Removed | Chance | Rating | Delay |
|---|---|---|---|
| Rothschild family and houses | 79% | Still possible, with more work | about 22 years |
| Edmond alone | 81% | | about 22 years |
| Without the United States | 65% | Possible only with major outside help | about 22 years |
| Finance and banks | 65% | | about 33 years |
| Zionist movement leadership | 60% | | |
| Walter Rothschild alone | 94% | | |

Removing Walter alone barely moves the chance. The declaration's force came from the War Cabinet, Balfour and the British government, with endorsement from Wilson and Congress, so it survives without its addressee.

UI:
- Tap a node, then use **Remove from the network**. A results window shows the outcome.
- Removals are saved until you reset the graph.
- A first-visit explainer covers the method and lists the heaviest nodes.
- On phones, pinch-to-zoom works even when it starts on a node.

## Pass: five readings per removal (5 Nov 2026)

Every removal now gives five readings:
1. **On time:** founded in 1948.
2. **By 1958.**
3. **Ever becomes a state:** the lost capacity is rebuilt at its historical pace, but each year of waiting costs 2% as the 1947–48 window closes. The best year is chosen, and the result is never below the 1948 figure.
4. **The movement itself survives:** money (counted twice) times organization.
5. **Time to rebuild what was lost.**

Verdict scale:

| Verdict | Rule |
|---|---|
| Happens on time | on-time chance ≥85% |
| Still likely, but delayed | on-time ≥70%, or ever ≥75% |
| Possible, with great difficulty | ever ≥55% |
| Unlikely | ever ≥30% |
| Not possible on this record | below that |

Readings:

| Removed | On time | By 1958 | Ever | Movement survives | Rebuild | Verdict |
|---|---|---|---|---|---|---|
| Without the United States | 65% | 72% | 72% | 80% | ~22 yrs | Possible, with great difficulty (best retry 1955) |
| Rothschild family and houses | 79% | | 79% | 84% | ~22 yrs | Still likely, but delayed |
| Zionist movement leadership | 60% | | 67% | 70% | ~33 yrs | Possible, with great difficulty |
| Finance and banks | 65% | | 69% | 75% | | Possible, with great difficulty |
| Armed groups | 0% | | 0% | 97% | | Not possible on this record (the movement survives, but its state is blocked) |

## Pass: combined removals and the signal light (5 Nov 2026)

Removals accumulate, and every reading is recalculated for the whole removed set together.

Each change (removing or restoring a node or a group) shows a signal at the top of the screen:
- **Green:** happens on time.
- **Yellow:** still likely but delayed, or possible with great difficulty.
- **Red:** unlikely, or not possible on this record.

The signal shows the verdict, the on-time chance with its change, the ever chance and movement survival. It dismisses itself after 6.5 seconds, has an X, can be swiped up on a phone, and pauses while the mouse is over it. Tapping it opens the full window for everything removed.

Combined readings:

| Removed together | On time | Ever | Verdict |
|---|---|---|---|
| Rothschild family | 79% | 79% | Still likely, but delayed |
| Rothschild family + Herzl | 78% | 78% | Still likely, but delayed |
| Rothschild family + Herzl + Weizmann | 76% | 77% | Still likely, but delayed |
| Rothschild family + the United States | 11% | 52% | Unlikely (best retry 1969; rebuild about 45 years) |

## Pass: the UN layer and the partition vote (5 Nov 2026)

New layer (un_layer.py, 103 ties, 36 new nodes):
- **The UN:** Charter signed 26 Jun 1945 by 50 countries; the UN came into existence 24 Oct 1945.
- **UNSCOP:** formed May 1947, with its members. Its majority report (3 Sep 1947) proposed partition with economic union.
- **The vote:** all 57 members' votes on Resolution 181 (29 Nov 1947), 33 for, 13 against, 10 abstaining. Siam was absent after its credentials were cancelled.
- **The reported pressure campaign:**
  - Philippines: a phone call from Washington.
  - Haiti: a $5M loan.
  - Liberia: pressure from Firestone and threatened aid cuts.
  - France: Baruch implied that US aid could be blocked.
  - A telegram from 26 senators to wavering countries.
  - Lovett's "bribes and threats" report.
  - Zemurray's reported pressure on Central American states.
  - The three-day postponement.
  - Nehru's bribery claim.
  - Arab threats of an oil embargo.
- **Recognitions in 1948:** 18 states with dates. The US was first, de facto on 14 May; the USSR was the first de jure, on 17 May.
- **The Declaration:** it cites Resolution 181 among its legal bases, and was signed by the Provisional State Council.
- **UN admission:** Resolution 273, 11 May 1949, 37–12–9.

Model:
- **A sixth channel, recognition.** Resolution 181 in force is weighted 22, as much as all the 1948 recognitions together. The US and USSR are weighted 3 each, every other recognizing state 1. Lost recognition is rebuilt over 3 years.
- **The vote rule.** Resolution 181 passes only if the votes for are at least twice the votes against (two-thirds of votes cast), and only if the UN and the General Assembly remain. A removed yes-vote counts as an abstention by default; the user can switch to "votes against". A removed no-vote does not vote.
- Full record = 93%.

Readings:

| Removed | Vote | On time | Verdict |
|---|---|---|---|
| The UN | no vote held | 84% | Still likely, but delayed |
| Philippines, Haiti, Liberia (as abstentions) | 30–13, passes | 93% | Happens on time |
| Philippines, Haiti, Liberia (as votes against) | 30–16, fails | 84% | Still likely, but delayed |
| Countries that voted for partition | fails | 52% | Still likely, but delayed (ever 87%) |
| Rothschilds + US | | 31% | Possible, with great difficulty |

## Pass: the global layer after 1948, and the Tests panel (5 Nov 2026)

**Global layer** (global_layer.py, 73 ties, 9 nodes; kept out of the 1948 model):
- Israeli aid to Africa from the late 1950s, aimed in part at UN votes ("important for Israel to try to win as many African votes as possible"), and the African break with Israel in 1973.
- ELNET (2007).
- The Israel Allies Foundation's caucuses in foreign parliaments.
- The state-funded campaigns: Kela Shlomo (128M shekels approved in 2018), Concert (25M shekels a year from 2022) and Voices of Israel (contract ended 2024). The ministry's own director general: "failed by every conceivable parameter".
- US Security Council vetoes (46 by 2023), and the 1982 Syrian move to review Israel's UN status, with the US threat to withdraw from the UN.
- Resolution 3379 (1975, 72–35–32), with the votes of every country already in the map, and its revocation in 1991 (46/86).

**New rule.** The state needs someone to pursue it. If the Zionist Organization, the Jewish Agency and the Va'ad Leumi are all removed, every channel counts as empty. The cluster group is renamed "The Zionist movement (organizations and leaders)".

**Tests panel** (a Tests chip in the mode row, and "Run a test" under Tools). There are 14 computed tests, each with a ring showing the 1948 chance and the verdict colour. Tapping a test runs it on the whole map: the removed nodes pulse out, cut ties flash red, and nodes cut off from the core get red dashed rings. A full assessment opens in the side panel. There is also one reading of the post-1948 record (US veto and UN standing).

| Test | On time | Ever | Verdict |
|---|---|---|---|
| Herzl | 93% | 93% | Happens on time |
| Zionism never organized | 0% | | Not possible |
| Rothschild money | 81% | | Still likely, but delayed (~22 yrs) |
| Rothschilds entirely | 78% | | Still likely, but delayed |
| Edmond's land and colonies | 80% | | Still likely, but delayed |
| Balfour Declaration | 93% | | Happens on time |
| Britain | 92% | | Happens on time |
| United States | 65% | | Possible, with great difficulty |
| UN vote | 84% | | Still likely, but delayed (vote fails) |
| Three pressured votes against | 84% | | Still likely, but delayed (vote fails) |
| Soviet bloc | 89% | | Happens on time |
| American money | 81% | | Still likely, but delayed |
| Armed groups | 0% | | Not possible |
| Rothschilds + US | 11% | 51% | Unlikely |

## Pass: lost years and substitutes (5 Nov 2026)

The model now counts the years of work an actor carried, and whether anyone documented could have taken it over.

**How it works:**
- **Active years.** Every person, organization and government is active from its first to its last dated supporting tie (birth and death dates are ignored).
- **Year by year.** For each year from 1882 to 1948 and each channel (money, land, force, diplomacy, organization), the model takes the share of that year's work the removed actors carried. That share is covered by the strongest documented actor on the same side (the movement and its backers, or the states) who was already active that year. A substitute covers at most its own documented weight in the channel, and counts only what it had apart from the removed actors: PICA's money was Edmond's.
- **Lost years.** What nobody could cover is lost. Each year counts as lost in proportion to the worst-hit channel.
- **Effect on the chances.** The on-time chance is multiplied by (1 − lost years / 66). A later founding cannot come before the lost years are made up. The delay is the longer of the channel rebuild time and the lost years.

**Readings:**

| Removed | On time | Ever | Years lost | Verdict | Detail |
|---|---|---|---|---|---|
| Edmond de Rothschild | 54% | 60% | ~22 | Possible, with great difficulty | Nobody could cover his money before the Jewish Agency in 1902 (86% of the role) |
| Herzl | 82% | | ~8 | Still likely, but delayed | His diplomacy was only partly covered (Jewish Agency from 1902, 43%) |
| Walter Rothschild | 93% | | 0 | | Weizmann was doing the same work at the same time |
| Rothschild family | 53% | 60% | ~22 | Possible, with great difficulty | |
| United States | 60% | 71% | ~4 | Possible, with great difficulty | |
| Rothschilds + US | 5% | 45% | ~35 | Unlikely | |
| Zionist movement | 0% | | | Not possible | |
| Armed groups | 0% | | | Not possible | |

## Pass: power of states, the Mandate as framework, stricter reading (5 Nov 2026)

**Power of states.** The five great powers named in the UN Charter are weighted by their 1950 GDP (Maddison), relative to France: US 6.6, USSR 2.31, UK 1.58, China 1.11, France 1. This applies to their diplomatic and recognition ties; every other state weighs 1. Fox (1944) named the US, the USSR and the UK as the "super-powers". Resolution 181 in force counts as much as all the 1948 recognitions together.

**Incorporation.** A document that wrote another into its text falls with it: the Mandate falls with the Balfour Declaration.

**The Mandate as a framework.**
- The Jewish population grew about 21,900 a year under the Mandate (83,794 in 1922 to 630,000 in 1947), against about 2,200 a year under Ottoman rule (24,000 in 1882 to 94,000 in 1914) (Jewish Virtual Library).
- Without the Mandate, 90% of the land-and-settlers work of 1920–1948 counts as lost years.
- The Mandate also needs its Mandatory power, Britain.
- Caveat: part of the faster growth came from persecution in Europe in the 1930s, which this credits to the Mandate.

**Stricter reading** (a switch, off by default): a document cannot be issued without its named addressee. It is added as the test "What if the Declaration needed Walter Rothschild?".

**Readings:**

| Removed | On time | Verdict | Notes |
|---|---|---|---|
| Balfour Declaration | 56% | Possible, with great difficulty | ~26 years lost |
| Britain | 55% | Possible, with great difficulty | |
| United States | 32% | Possible, with great difficulty | ever 64% |
| Walter Rothschild (stricter reading) | 56% | Possible, with great difficulty | |
| Walter Rothschild (default) | 93% | Happens on time | |
| Rothschilds | 53% | Possible, with great difficulty | |
| Rothschilds + US | 3% | Unlikely | ever 42% |
| Herzl | 89% | Happens on time | ~3 years lost |

## Pass: the presidents (5 Nov 2026)

**Presidents layer** (president_layer.py, 7 ties, 2 nodes):
- **FDR's hidden heart failure.** Bruenn, 28 Mar 1944: "acute congestive heart failure", kept "a guarded secret". FDR died 12 Apr 1945.
- **The 1944 running mate.** Party leaders' health concerns (History.com). Lahey memo of 10 July 1944, unpublished for six decades.
- **Wallace.** Ballot figures; "a supporter of Zionism"; met Ben-Gurion and Begin, Oct 1947; promised to end the arms embargo.
- **Feinberg.** His own account (Truman Library oral history, 1973): a $100,000 pledge for the whistle-stop tour; "without Truman, Israel would have had very difficult days"; the trip "would have been made one way or another".
- **Wilson's hidden stroke** (2 Oct 1919), the comparable earlier case.

**New tests:**

| Test | On time | Ever | Verdict | Why |
|---|---|---|---|---|
| Truman never vice president | 92% | | Happens on time | Wallace, a documented supporter, would have been president |
| Roosevelt healthy and keeping his 5 Apr 1945 pledge to Ibn Saud | 76% | 89% | Still likely, but delayed (~5 yrs) | No US vote, pressure or recognition; the Philippines, Haiti and Liberia vote no; partition fails 29–16 |

New model features: a country can keep its record but not vote (novote), or vote against (flip).

## Pass: key decisions read holistically (5 Nov 2026)

Three decisions are now modelled as decisions:
- the Balfour Declaration (decided by the War Cabinet);
- the US vote and pressure for partition, Nov 1947 (decided by Truman);
- US recognition, 14 May 1948 (decided by Truman).

**How a decision is read:**
- Each decision has a curated list of the people and bodies who pushed for it and who resisted it, all from ties on the map dated before the decision.
- Its chance of happening = push / (push + resistance), relative to the full record.
- If the decider is removed, the documented successor decides (Wallace in Truman's place). A test can also name the decider (Roosevelt in the healthy-Roosevelt test).
- Pressure aimed at the man (anyone with a direct tie to him) does not pass to the successor without the successor's own tie to that person. Resistance stays.
- The successor's own documented position counts for or against: Wallace +2 as a supporter, Roosevelt −1 for his 5 Apr 1945 pledge.
- The overall chance averages over whether each decision happens, combining every outcome.

**Readings:**

| Removed | Decision chance (vs record) | On time | Ever | Verdict |
|---|---|---|---|---|
| Truman | Recognition under Wallace 52%; partition vote holds | 92% | | Happens on time |
| Healthy Roosevelt (pledge kept) | Recognition 26%; partition vote and pressure 69% | 87% | 91% | Happens on time |
| United States (whole) | | 25% | 64% | Possible, with great difficulty |

The overall chance moves less than the decision chances because the USSR recognized Israel three days after the US, and the UN basis remains.

The build now checks both scripts with `node --check` before writing the page.

## Pass: blocs follow their leaders (5 Nov 2026)

**Blocs, from treaties of the time:**
- **The Americas:** the Rio Pact (2 Sept 1947). 15 members voted in 1947, and 67% voted with the US.
- **Western Europe:** the Marshall Plan accord (April 1948). 11 members voted, and 73% voted with the US.
- **The Soviet side:** the Soviet republics and Moscow's allies. 5 members voted, and 80% voted with the USSR.

**The rule.** If a bloc's leader is out (removed, or not voting for partition), each member that followed it keeps its yes vote and its 1948 recognition only at the bloc's independence (1 − follow share). The vote's pass probability is then computed exactly, and enters the holistic mixture as a pseudo-decision. The same rule applies to both blocs.

**Readings:**

| Removed | On time | Ever | Verdict | Vote passes |
|---|---|---|---|---|
| US government alone | 64% | 89% | Still likely, but delayed | 0.17% |
| USSR alone | 93% | | Happens on time | |
| Without the United States (group) | 20% | 64% | Possible, with great difficulty | |
| Healthy Roosevelt | 84% | | Still likely, but delayed | |

New test: "What if only Moscow had backed partition, and Washington had stayed out?"

## Pass: rebuilding scales with what remains (5 Nov 2026)

What is lost is rebuilt by the network that is left: share_t = s × (1 + t/T). Full rebuild time = T × (1 − s)/s, capped at 200 years. A network left at half rebuilds at half the original pace.

**Readings:**

| Removed | On time | Ever | Verdict |
|---|---|---|---|
| Without the United States | 20% | 45% | Unlikely (rebuild over a century) |
| Only Moscow backs partition | 64% | 81% | Still likely, but delayed |
| Moscow alone out | 93% | | Happens on time |
| Rothschilds + US | 2% | 13% | Not possible on this record |
| Rothschilds | 52% | 58% | Possible, with great difficulty |

## Pass: lost years dated by year, four more key decisions, other homelands, the book appendix (5 Nov 2026)

**Lost years, for every node.** Each tie's work sits in the years it was done (stated ranges for the large sums; else its labels' years; undated ties spread over the actor's span). Documented founding/end dates override tie-read spans (Jewish Agency 1929, Palestine Office 1908–21, Herzl 1895–1904, Hankin 1890–1945, Va'ad Leumi 1920, etc.). A substitute covers a year only up to the yearly work it had shown by then. Knock-on: uncovered work is a shortfall against everything built so far and keeps counting until later work outgrows it; a channel counts once its record reaches 5% of its 1948 total.

**Key decisions now seven:** + League approval of the Mandate (1922), Britain to the UN (Feb 1947; Attlee as successor), Soviet support (Stalin; unnamed successor), Czechoslovak arms (1948). A successor with no documented position adds one unit to each side; no decider left means the decision is not taken. New ties in decision_layer.py (11), new nodes Masaryk and Avriel.

**Other homelands** (alt_homeland.py, Tests panel): Argentina under 1%, British East Africa about 2%; shares are disclosed judgments on the same six channels.

**Readings:**

| Removed / test | On time | Ever | Years lost | Verdict |
|---|---|---|---|---|
| Edmond de Rothschild | 28% | 39% | 43 | Unlikely (was 54%, 21 yrs) |
| Rothschild family | 27% | 39% | 43 | Unlikely |
| Without the United States | 22% | 46% | 14 | Unlikely |
| Britain | 48% | 53% | 28 | Unlikely |
| Balfour Declaration | 56% | 56% | 26 | Possible, with great difficulty |
| Only Moscow (US government out) | 64% | 81% | 0 | Still likely, but delayed |
| Stalin | 93% | 93% | 0 | Happens on time |
| Czechoslovak arms | 91% | 91% | 0 | Happens on time |
| Rothschilds + US | 1% | 13% | 45 | Not possible on this record |
| Yishuv institutions (Va'ad Leumi) | 93% | | 0 | Happens on time (was 60%, an artifact of the old rule) |

Browser and Python agree on 143 sampled nodes. Book: new appendix "The Map and the Tests" in The Road to 1948 (book/part1/rd7, six sections).

## Pass: the other homelands as Appendix Two (5 Nov 2026)

Eight alternatives, in the order raised, each told from its documents and scored on the six channels (same formula; shares are disclosed judgments): Argentina under 1%, El Arish about 1%, British East Africa about 2%, Birobidzhan under 1% (peak about 46,000-50,000 Jews), Madagascar 0 (a deportation plan, never an offer), Alaska under 1%, Sosúa under 1% (peak about 500), Suriname under 1% (approved 1947, suspended Aug 1948). Finding: by 1914 only Ethiopia and Liberia were outside European rule in Africa; no land combined a willing ruler, no resident population, and Jews willing to go. Book: The Road to 1948 now has Appendix One (The Map and the Tests, rd7) and Appendix Two (The Other Homelands, rd8, ten sections).
