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
