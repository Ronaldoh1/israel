# Road to 1948 network map: coverage plan (19 Nov 2026)

Goal: an end-to-end picture of every pathway that moved the movement forward (and every force that pushed back), from the first written idea to May 1948, each tie documented, then re-test and stress-test the model.

One research pass per pathway. Each pass ends with: nodes and ties added (sources on every tie), tests rerun, figures checked against the book, appendix updated, bundle shipped.

## Pathway inventory and current coverage

| # | Pathway | Examples | On the map now |
|---|---|---|---|
| 1 | **People: immigration and population** | Aliyot 1882–1948; certificates and labour schedules; clandestine immigration; doors closed elsewhere (US 1924, Évian 1938) | Missing as a channel; only Mossad LeAliyah Bet/Bricha, filed under land |
| 2 | **Policy and legal instruments** | Ottoman Land Code 1858; Mandate Arts 2, 4, 6, 11, 22; Land Transfer Ordinance 1920; White Papers 1922/1930/1939; MacDonald letter 1931; concessions (electricity 1921, Dead Sea 1930); Permanent Mandates Commission | Many on the map with zero weight |
| 3 | **Media, information and propaganda (both sides)** | Die Welt 1897; Manchester Guardian/C. P. Scott; JTA 1917; Palestine Post 1932; British wartime use of the Balfour Declaration; AZEC campaign 1943–48; We Will Never Die 1943; Exodus as publicity; Arab Office 1945; Arab press | Scott and Die Welt only |
| 4 | **Religious institutions** | Churches and missions (London Jews Society 1809, Jerusalem bishopric 1841); dispensationalist networks; Christian Council on Palestine 1942; rabbinate and synagogues (Mizrachi 1902; Agudat Israel and Reform opposition); the Vatican (opposition) | Partly (Christian committees, Scofield, Darby) |
| 5 | **Lobbying and electoral politics** | AZEC; Brandeis and Frankfurter access; Weizmann's British access; the Bergson group; the New York vote and the 1948 election; congressional resolutions | Partly |
| 6 | **Outside military training and intelligence** | NILI 1915–17; Jewish Legion; Special Night Squads 1938; British training of the Palmach 1941; Jewish Brigade 1944; Polish training of the Irgun | Partly |
| 7 | **Economy and infrastructure** | Concessions; Histadrut economy; citrus; British wartime military spending in Palestine; capital imports | Partly |
| 8 | **International bodies and expert reports** | League of Nations; Permanent Mandates Commission; Hope Simpson 1930; Peel 1937 (partition idea); Woodhead 1938; UNSCOP 1947 | Partly |
| 9 | **Counterforces** | Arab opposition and revolts; British reversals; Jewish anti-Zionists; State Department; the Vatican | Recorded as stance, not weighed |
| 10 | **Contingency and timing** | Ottoman collapse; two world wars; British exhaustion 1947; onset of the Cold War | Implicit |

Already done: money and central banks (Nov 2026), legitimacy channel (Nov 2026), pre-1897 network (Nov 2026).

## Pass log
- **Pass 1, people channel: done 19 Nov 2026 (v80).** 9 nodes, 19 ties (13 weighted, in thousands of people); Mandate certificates, Haavara and the clandestine voyages carry their documented shares; the US 1924 Act and the 1939 White Paper recorded without weight. Baseline unchanged (93.2%). New tests: no Mandate certificates 78%, no Fifth Aliyah 87%, no pre-1914 immigration 93%, no Fourth Aliyah 92%, no clandestine voyages 93%. British government 45% -> 38%. Flag for the stress test: the saturating curve is probably too gentle for population.
- **Pass 2, policy instruments and land held: done 19 Nov 2026 (v81).** Ninth channel, land held (thousands of dunams, total 2,000): JNF 936 (22 by 1920 + 914 under the Land Transfer Ordinance, which carries that share), PICA 500 (1934, rough), private buyers and companies 564 (remainder). New nodes: other_holdings, private_land, MacDonald letter, Permanent Mandates Commission. Weighted: Article 4 -> Jewish Agency, MacDonald letter -> Weizmann. Recorded without weight: Churchill White Paper 1922, 1940 Land Transfers Regulations, PMC 1939 verdict, Sursock sales. Tests: no land law 86%, no JNF 83%, Passfield stands (upper bound) 90%, no Mandate immigration and land promise (assumption) 73%. Rothschild documented figure 34% -> 30% (PICA land now counted); British government 38% -> 35%; Edmond's heirs 83% -> 74%. Ten stale map readings refreshed (tools/patch_read_refresh_pass2.py), including d_all's sub-figure, which was already wrong in v78 (said 40%, computed 49%). Card set claude/road1948-probability-cards.md is now stale: regenerate after the stress test.
- **Pass 3, media and public campaigns (both sides): done 19 Nov 2026 (v82).** New nodes: We Will Never Die (1943), JTA (1917), Palestine Post (1932), Gershon Agron, American public opinion 1947. Weighted in legitimacy: AZEC -> Truman (mail and telegram campaign, Truman's memoir and Pepper letter), 1947 opinion -> Truman (reported). Recorded without weight: the movement's press, the pageant (rescue aim), the Balfour propaganda motive (disputed), the Arab Office's 1946 case (to be weighed in the counterforces pass). Baseline unchanged. Tests: no public campaign 92.5%, no movement press 93%. Spreading the legitimacy channel moved: survivors' case 87 -> 88, Christian/public support 88 -> 89, US 25 -> 24, FDR pledge 83 -> 82, unknown Democrat 86 -> 85, Dewey 91 -> 89, Truman 90.5 -> 89. Readings refreshed by tools/patch_read_refresh_pass3.py. New limit in the appendix: persuasion with no documented tie is unmeasured.
- **1944 swap detail: done 19 Nov 2026 (v83).** 11 July White House meeting, Wallace's China/USSR mission, the 20 July adjournment, the 1946 Madison Square Garden speech (no weight). Tests: convention not adjourned 89%; Wallace's support discounted (assumption) 85%. No Zionist tie found among the six party leaders or the chairman; the documented Zionist activity at the convention was the platform plank (Wise, Goldstein, Celler, Littell; Rosenman for a weak plank). Volume I gained "Descent is not a deed" and "Who held the pen" (v84).
- **Pass 4, religious institutions: done 19 Nov 2026 (v85).** New: London Jews Society (1809), Jerusalem bishopric (1841), Chief Rabbinate (1921), Columbus Platform (1937), status quo letter (1947), Sonnenfeld; ties for de Haan's lobbying and his killing by the Haganah (1924). All without weight. Tests: no religious Jewish support 93%; no religious bodies at all 90%. Diagnostic: removing every religious opponent moves the chance by under 0.1 point in the wrong direction (opposition ties counted as network capacity); fix in the counterforces pass, recorded in rd7_limits.

## Order agreed with Ron
1. People channel
2. Policy instruments with stated effects
3. Media (both sides) into the legitimacy channel
4. Religious institutions
5. Remaining pathways (5–10), one pass each
6. Final coverage audit, then a stress test of the model: weight sensitivity, leave-one-source-out, and a check that no result depends on a single undocumented assumption

## Standing rules for every pass
- Ties only where a document states one party acting on another; causes and beliefs that the record does not tie to a decision are recorded but weightless, and the book says so.
- Both sides under the same rules (supporters and opponents).
- Kinship is not a tie; identity is never a tie.
- New channels are normalized so the baseline and unrelated tests stay fixed; every shift is reported.
- A probabilistic counterfactual cannot be "airtight"; the aim is transparent, reproducible and robust, with every weight disclosed.
