# The Epstein Network — QOP Analysis v1
*Run 4 Nov 2026 on the companion graph: 419 nodes and 816 edges. Of the edges, 686 are verified, 46 to-verify, 41 reported, 14 planned, 16 not-established, 11 withheld, 1 probable and 1 scheduled. Internal working document: QOP labels are used here. The published book stays in clean voice.*

**Analysis graph.** Unless a section says otherwise, everything is computed on the **documented-tie graph**: verified edges only, with these excluded:
- probe-type edges (investigations, testimony, complaints, reporting);
- comparison and framework edges;
- flight-passenger counts (transcription only);
- kinship;
- document and evidence nodes.

This leaves 269 nodes and 377 documented ties.

**Subject-type classification (2B.0):** COMPOSITE / MACRO-SYSTEM.
- The component modules are already the book's Parts:
  - origins and money (INSTITUTION + PERSON);
  - banks (INSTITUTION);
  - the Swiss contract (INSTRUMENT);
  - agencies and the 2008 deal (INSTRUMENT + SYSTEM-grade INSTITUTION: the DOJ);
  - the files (INSTRUMENT: the Transparency Act).
- Epstein himself runs the PERSON ceiling.
- The attribution ceiling is set per component. No network-wide average.

---

## Deliberation Ledger

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DELIBERATION LEDGER — THE EPSTEIN NETWORK (QOP v1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENTITIES IN THIS ANALYSIS:
[💼 Southern Trust] [💼 HBRK Associates] [💼 Plan D] [💼 BV70]
[🏦 JPMorgan] [🏦 Deutsche Bank] [🏦 Bank of America] [🏦 FirstBank]
[🏦 Edmond de Rothschild] [🏦 Bank Leumi] [🏛️ USVI EDC] [⚖️ DOJ/SDNY]
[🕵️ FBI] [🕵️ DEA/OCDETF] [🏛️ ICE] [🏰 Wexner] [🏰 Black]
[📡 reputation contractors] [🛕 —none documented—]

POWER STRUCTURE:
[🔱 Sponsors: Wexner · Black · EdR · USVI tax regime]
   → [🌀 Back office: Kahn · Indyke · HBRK · Southern Trust]
   → [💸 Outflows: Ergo/Carbyne · Achrayut · scouts · MC2 · trusts]
   → [↩️ Shield: 2008 NPA · discretion · redaction choices]

KEY MECHANISMS:
[🎭 warning overridden] [🔀 c/o routing through one office]
[🛡️ immunity for "potential co-conspirators"] [📜 contingent fee on a DOJ penalty]
[🔐 investigations that never met] [⛔ survivors exposed / payers unasked]

CLAIM QUALITY KEY:  ✅ CONFIRMED  📰 REPORTED  ⚠️ CONTESTED  ❓ INCONCLUSIVE  ◈ LENS
ESOTERIC LAYER PRESENT: Yes (Section 7, labeled ◈)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 1. Kevin Bacon network (2B.0B §1)

**Tiers by documented degree from Epstein** (documented-tie graph):

| Tier | Nodes | Who is there |
|---|---|---|
| **Direct 1°** | 156 | 107 people, 28 companies, 7 institutions. Maxwell, Wexner, Black, Barak, Thiel, Mandelson, Andrew, Trump, Clinton, Summers, Lutnick, Bannon, Gates, Brunel, Dershowitz, Kellen, Groff, the pilots, Indyke, Kahn… |
| **Operational 2°** | 77 | Dimon, Benjamin de Rothschild, Siad, Nikolic, Acosta, the house staff (Alessi, Rodriguez), the MCC guards, W. Barr, de Jongh, Kushner, Netanyahu, Shuliak, Woody Allen |
| **Strategic 3°** | 14 | Elysium Management, the APO trusts, Bella Klein, Stewart Oldfield, Bank Leumi, Achrayut Leumit, Anixter, Geoffrey Berman, NSA, Putin |
| **4°** | 11 | Mostly Black's administrative layer (LBF Holdings, LDB 2011, Ada Clapp) and archives |

**APEX (where money and authority concentrate).** Documented inflows to Epstein and his vehicles, ranked:
1. US Virgin Islands tax regime: ~$300M in benefits per a JPMorgan filing ✅
2. Leon Black: $158M + $12M (~$170M), plus the $30.5M BV70 loan ✅
3. Les Wexner: power of attorney from 1991; billions in stock sales overseen ✅
4. Edmond de Rothschild: $25M fee contingent on a DOJ penalty ✅

No single apex. The structure is **multi-sponsor, single-broker**: four independent money sources, none connected to another except through Epstein.

**Finding (✅ computed).** Take Epstein and Maxwell out, and the top connectors of the remaining network are:

| Rank | Connector | Betweenness |
|---|---|---|
| 1 | Richard Kahn | 0.44 |
| 2 | Southern Trust | 0.43 |
| 3 | FBI | 0.33 |
| 4 | Ehud Barak | 0.31 |
| 5 | Leon Black | 0.23 |
| 6 | Ergo Ltd. | 0.20 |
| 7 | Paul Morris | 0.20 |
| 8 | Butterfly Trust | 0.20 |
| 9 | Deutsche Bank | 0.19 |

The spine of the network without its founder is the **back office**: one accountant, one lawyer, one shared "c/o HBRK" address, one tax-break company. The network then splits into 80 pieces.

## 2. Circular / recursive pass (🔄 CIRCULAR)

There are 22 short loops that don't pass through Epstein. The ones that matter:

| Loop | Type | Status |
|---|---|---|
| 🔄 Southern Trust → HBRK → Kahn → Southern Trust | Same office runs the company, signs its accounts, receives its wires | ✅ |
| 🔄 Indyke → HBRK → Kahn → trusts (2018/2019 trusts, Butterfly) → Indyke | Trustees, executors and the c/o office are the same two men | ✅ |
| 🔄 TD Bank → Kahn → HBRK → Indyke | Bank SAR closes the loop on the office | ✅ |
| 🔄 Barak → Ergo Ltd. → Carbyne → Barak | Epstein's $1M enters a vehicle "solely owned by EB" | ✅ |
| 🔄 Ergo → Southern Trust → Indyke → Carbyne | The lender's lawyer later fields the "controlling person" question | ✅ |
| 🔄 EdR → EdR Holding → Ruemmler → Latham → EdR | The lawyer Epstein introduced negotiates the penalty his fee depends on | ✅ (documents); motive ❓ |
| 🔄 Coinbase → Pierce → Blockchain Capital → Coinbase | Stake arranged and bought back by the same circle | ✅ |
| 🔄 Maxwell → Blanche → DOJ → BOP → Maxwell | Interview, then the transfer to a lower-security prison | ✅ sequence; any quid pro quo ❓ |

The loop is the finding. Money, signature authority and legal representation circle through two men and one address.

## 3. Institutions layer: stated mission vs documented behavior

| Institution | Stated function | Documented behavior |
|---|---|---|
| JPMorgan | AML compliance; "know your client" | General counsel: "should not be a client" (2011). Kept him two more years ✅ |
| Deutsche Bank | Reputational-risk committee | Committee bypassed by email. 2017 AML case on the Barak wire closed on "Friend". Reference letter to Bank Leumi after the exit notice ✅ |
| FirstBank | Fee policy | "Platinum" status, fees waived, 7+ years ✅ |
| DOJ (2008) | Prosecute federal crimes | Immunity for "any potential co-conspirators". OPR: "poor judgment", no misconduct ✅ |
| OCDETF | Join agencies' cases | DEA, FBI and ICE cases ran side by side and never met ✅. Why ❓ |
| DOJ (2026) | Transparency Act: hide victims, not officials | 43 of 47 victims' names visible; men's names blacked out ✅ |
| USVI EDC | Attract real local business | ~$300M in tax benefits to Epstein companies ✅. Approval records not public ❓ |

## 4. Follow the Money (QOP Part 5A)

**Chain A: sponsor money**
```
INPUT        Black $158–170M · EdR $25M (contingent on DOJ penalty) · USVI tax benefits ~$300M
MECHANISM    "Advisory"/"algorithm"/"estate planning" contracts → Southern Trust & Financial Trust (USVI)
COMPOUNDING  Tax-exempt status (EDC); one office (HBRK) controls signatures, trusts, wires
BENEFICIARY  Epstein; his companies; the office that ran them
DOWNSTREAM   Funds the properties, aircraft companies (JEGE · Hyperion · Plan D) and staff
             through which the abuse was organized (court record)
```

**Chain B: outflows the files now show** ✅
```
Southern Trust → Ergo Ltd. ($1M, Mar 2015) → Carbyne (later sold to Axon for $625M)
HBRK → Achrayut Leumit ($40K, Mar 2017)
Epstein's Deutsche custody account → Daniel Siad (euro instruction, Apr 2014)
JPMorgan account → MC2 Model Management (wire, Nov 2012)
Butterfly Trust → 120 wires, $2.65M (NYDFS)
Plan D ← BV70 ($30.5M note; $10M repaid; rest unpaid at death)
```

**Chain C: the cost** ✅
```
Survivors (about 150 compensated, a floor) → settlements paid by banks and the estate
(JPMorgan $290M; Deutsche $75M; BofA $72.5M) → 2026: ~100 survivors' identities exposed,
death threats, class action against DOJ and Google
```

**Extraction pattern named:** not one of the library's household patterns (debt cycle, fee compounding). An original pattern: **reputation laundering for fees**. The wealthy pay a convicted man for access and outcomes. The money builds the infrastructure. The cost lands on the girls and women at the bottom, twice: in the abuse, and in the 2026 exposure.

## 5. Pattern recognition (Framework D: mechanism, ≥2 precedents, resistance points)

| Mechanism | Epstein instances | Outside precedents | Status |
|---|---|---|---|
| **Warning overridden inside the institution** | JPM 2011; DB 2013 committee bypass; DB 2017 "Friend" | FBI and Nassar (IG 2021); BBC and Savile (2016) | ✅ pattern |
| **Company funds and payroll used for the operation** | HBRK c/o wires; Southern Trust; LSJE payroll; scout payment | Nygård indictment (alleged) | ✅ instance; 1 outside precedent (alleged) |
| **Investigators turned on accusers** | 2009 court motion | Weinstein (Kroll, Black Cube); Nygård (alleged) | ✅ pattern |
| **Recruitment through a legitimate front** | MC2 wire; Siad; "massage" | NXIVM "mentorship group"; Nygård modelling promises | ✅ pattern |
| **Institutions told, did not act** | FBI 1996; 2016 tip to SDNY | Nassar; Savile; Pennsylvania dioceses | ✅ pattern |
| **Officials bought** | **No bribe documented** | García Luna / Sinaloa | ❌ UNSUPPORTED for Epstein (the documented mechanism is access, not cash) |
| **The insider who opens the records** | None has come forward | Guzmán's IT technician | Gap |

**Resistance points:**
- Palm Beach police (2005).
- The survivors' CVRA suit (ruled 2019).
- The Miami Herald (2018).
- USVI and New Mexico.
- The Wyden and Khanna/Massie pressure.
- The Phang v. Blanche injunction (2026).

Each disrupted the mechanism at the point where a decision had been left to discretion.

## 6. ObjC Black Magic: best fit

**NSProxy / forwardInvocation:** every party in the chain forwards to the next, and no one is the answerable party.

```objc
@interface HBRKProxy : NSProxy   // "c/o HBRK Associates, 575 Lexington Ave"
@property (strong) id principal; // Jeffrey Epstein (sole member, president, beneficial owner)
@end
@implementation HBRKProxy
- (void)forwardInvocation:(NSInvocation *)inv {
    // wire, sign, hold title, answer compliance ("Friend")
    [inv invokeWithTarget:self.principal];   // the real actor never appears on the form
}
- (NSMethodSignature *)methodSignatureForSelector:(SEL)sel {
    return [self.principal methodSignatureForSelector:sel];
}
@end
// Southern Trust, Plan D, JEGE, Hyperion, Ergo Ltd.: each another proxy in the chain.
// Indyke, 2019: "I thought we did not want your name associated with this Investment?"
```

**Plain language:**
- The money and the aircraft were held by companies that existed to answer for someone else: Plan D for the G550, JEGE and Hyperion for the other planes, Southern Trust for the fees, and HBRK as the address on the wires.
- When a bank asked a question, the office answered for him.
- When a counterparty asked who controlled the company, his lawyer's first instinct was to keep the name off the paper.

## 7. ◈ INTERPRETIVE LENS (TIER 5): reading the architecture

*This is a symbolic reading of the documented structure, not a documentary claim.*

**◈ Hermetic correspondence ("as above, so below").** The pattern repeats at both scales.
- *Below:* two men, one address, a dozen companies, each pointing to the next.
- *Above:* a federal program built to join cases, under which three agencies ran Epstein cases for years without meeting.
- Read through this lens, the private shell and the public bureaucracy share one design principle: responsibility forwarded until it disappears.

**◈ Double extraction (Monroe / Gnostic frame).** The material chain (Section 4) runs alongside a documented human-cost chain:
- the abuse;
- the 2008 secrecy that the 2019 CVRA ruling found unlawful;
- the 2026 exposure with death threats.

Read through the loosh lens, the mechanism yields fear at the bottom of the hierarchy at every stage, including stages that produced no money at all, such as the release.

**Loosh Index ◈ 8/10.** Interpretive, not a measurement.
- *Why it's high:* the population harmed is documented (about 150 compensated, a floor). The design features that amplify harm are documented: secrecy of the deal from victims, investigators sent at accusers, names published in 2026.
- *Why not 10:* the financial engine was primary, not incidental.

## 8. Pass 5: Dot Connection Matrix (cross-series)

Graph nodes found in other library volumes (exact-name matches):

| Node | Other volumes (mentions) | Cross-series reading |
|---|---|---|
| Palantir / Peter Thiel | The Eye (276), The Test (117), One-Way Mirror (71), Men and the Money (61) | Thiel–Epstein (Valar $40M) is the bridge to the surveillance-state volumes |
| Carbyne / Unit 8200 / Barak | One-Way Mirror (19/28/7) | Carbyne's $1M Epstein seed (now verified) connects the Epstein map to the One-Way Mirror's surveillance-export chapters |
| Donald Trump | 16 volumes | The appointment and pardon layer (Blanche, Bondi, Lutnick, Maxwell's transfer) |
| Elon Musk / Coinbase / Hoffman | DOGE, Exit, Democracy Hasn't Been Tried | The tech-money layer; Coinbase stake (verified) |
| Edmond de Rothschild group | **Vatican Architecture (6)**, Road to 1948 | Vatican vol. XI already tested the chain: a former EdR chief executive became president of the IOR's board in 2026, and the Paris inquiry into Fabrice Aidan does not mention the Vatican. **Chain tested, no Epstein link established.** Slide test: Edmond de Rothschild the 19th-century benefactor (PICA, Road to 1948) ≠ the modern bank ≠ Ariane |
| Barclays | Divine 3+1 (7) | Staley as CEO, 2015–21; City of London chapter |
| FinCEN / Wyden | The Eye (10/9) | The unreleased 4,725 wires sit in the same Treasury system the surveillance volumes describe |
| JPMorgan, Citi, Wells Fargo, BofA | American Dream (4 each) | Same banks, fee-extraction chapters |

**Strongest cross-series thread:** Epstein → Barak → Ergo → Carbyne → Axon, joined to the One-Way Mirror / The Eye surveillance architecture. It is documented at every link. It is **not** evidence of intelligence tasking (❓ / ❌ for that claim).

## 9. What the analysis does NOT support

- **A single principal or handler.** ❓/❌ The structure is multi-sponsor, single-broker. There is no apex beyond Epstein, and no tasking document.
- **"Israeli intelligence operation."** ❌ as a finding. The documents show a private business channel: Barak's Carbyne loan, a political donation, and surveillance brokering in Côte d'Ivoire.
- **Rothschild family control.** ❌ The documents show one bank, one banker, and one DOJ-contingent fee. The 12,000-mention figure is a footer-and-header artifact.
- **Bribery of officials.** ❌ Not documented. Access was the mechanism.
- **Every map tie is a crime.** ❌ A documented tie is not an accusation.

## 10. Next research targets (highest-yield)

1. **Unredacted DEA "Chain Reaction" memo.** The 14 names and the OCDETF participating agencies.
2. **Treasury's 4,725 wires.** Outflows beyond the $1.04M documented to Israeli banks, and all other foreign counterparties.
3. **HBRK's client list.** HBRK said it served other ultra-high-net-worth clients. Who?
4. **USVI EDC approval files.** Who renewed Southern Trust's tax status, on what evidence.
5. **Southern Trust's books.** What the $25M from EdR bought: deliverables, or none.
6. **Pre-1995 flight-log pages, transcribed.** Completes Section 1's counts.

---

## 11. Succession test: remove the hub, see who rebalances (added 4 Nov 2026)

**Question (Ron):** if Epstein is deleted, which node would have to be "injected" at his height to keep the network working? It would need to be someone who knows how the network is connected and run.

**Method.** Run on the documented-tie graph.
1. Remove Epstein, then Epstein + Maxwell.
2. Score every remaining person and entity on four measures:
   - share of Epstein's 154 documented ties reachable within two steps;
   - share of his 60 money/ownership ties reachable within two steps;
   - betweenness after removal;
   - direct overlap.
3. Rerun with the **office** merged: Kahn and Indyke plus the vehicles they documentably controlled as trustees, executors or signers (HBRK, Southern Trust, Financial Trust, the Butterfly and 2018/2019 trusts, Plan D, JEGE, Hyperion, LSJE, Kyara, Gratitude America).
4. Measure "knowledge of operation" as how many of the map's clusters a person reaches within two steps.

**Results ✅ (computed)**

| Removal | Pieces left | Best single replacement covers |
|---|---|---|
| Epstein | 78 | 15 of 154 ties (10%): Butterfly Trust, Paul Morris |
| Epstein + Maxwell | 82 | 15 of 154: Paul Morris; Southern Trust and Barak top the score |
| Epstein, office merged | 76 | **The Kahn–Indyke office: 22 of 154 (14%); betweenness 0.21, twice Maxwell's 0.10; reaches 14 clusters** |

Widest two-step reach across clusters among individuals:
- Barak: 11 clusters.
- Indyke: 10.
- Kahn: 10.
- Wexner: 8.
- Black: 7.
- Maxwell: 6.

**Findings**
1. **No node can rebalance the tree.** ✅ The network is a star, not a balanced tree. No single node holds more than about a tenth of the hub's ties, so removing the hub shatters it rather than rotating a successor into place. Compartmentalisation shows up as structure. Each sponsor, bank and guest knew Epstein, not each other.
2. **The money side had a successor, and it is documented.** ✅ The only position that comes close is the office. It already held signature authority, trusteeships and the c/o address. After August 2019 that is what happened on paper: Kahn and Indyke became co-executors and controlled the estate and its companies until the estate's settlements. They deny any knowledge of or role in the abuse and settled without admission. This is structural position, not an accusation.
3. **The operations side's successor was Maxwell**, the second-strongest node. She was removed by her 2020 arrest and 2021 conviction. No one else in the map holds that position.
4. **The access side had no successor.** The introductions network (Barak, Black, Wexner, the guests) was held together only by Epstein. Barak has the widest cross-cluster reach of any individual, but his ties run through business introductions, not the operation.
5. **Bias warning ❓.** This is an ego network built from Epstein's own record. Other people's independent ties are invisible, so their coverage is understated. A real successor could sit outside the map entirely. That is the limit of what this graph can show.

**What would sharpen the test (graph upgrades):**
- Edge **weights**: dollar amounts, message counts, flight counts.
- **Direction**: who paid whom, who instructed whom.
- **Dates**: start and end of each tie, so succession can be read as "who held the tie at time T".
- Explicit **control edges**: signer, trustee, executor, director.

With those, the same test can run year by year, for example in 2008 (jail) and 2019 (arrest).

### 11b. Role-aware succession (Ron's correction: the two hubs had different jobs)

Epstein and Maxwell held different roles:
- **Epstein:** broker, money and access.
- **Maxwell:** operations, companion, recruitment (her 2021 conviction).

So each position is tested on its own role. Candidates are matched on **role, not sex**. The record puts men in the recruitment function (Brunel; the scout Siad) and women in the money and access function (Ariane de Rothschild, Lynn Forester de Rothschild).

**Epstein's role**
- *Money side:* passes to the Kahn–Indyke office (Section 11). ✅
- *Access side:* no successor. ✅

**Maxwell's role: the graph under-maps her.** She has only 7 documented ties on the map, against 154 for Epstein. Her trial-record role (recruiting, managing staff and houses) is mostly not yet encoded as edges. The best time-series signal is the pilot's log. It is a transcription, so 📰 REPORTED.

Share of Epstein's logged flight legs with each person on board:

| Year | Maxwell | Kellen | Marcinkova | Epstein legs |
|---|---|---|---|---|
| 1996 | 61% | — | — | 113 |
| 1999 | 42% | — | — | 93 |
| 2000 | 58% | — | — | 92 |
| 2001 | 66% | 22% | — | 136 |
| 2002 | 60% | **77%** | — | 120 |
| 2003 | 45% | 74% | 5% | 103 |
| 2004 | 18% | 70% | **79%** | 100 |
| 2005 | 9% | 57% | 57% | 65 |

**Finding 📰 (structural, not an accusation).** In the log, the position at Epstein's side rotated:
- **Maxwell** held it from 1996 to 2002.
- **Sarah Kellen** took it from 2002.
- **Nadia Marcinkova** joined from 2004.
- Maxwell's share fell to 9% by 2005.

Lesley Groff, executive assistant 2001–2019 and scheduler, is the continuity in the office. She does not appear in the flight log.

**The critical qualifier.** The people who rotated into Maxwell's position came from among the young women around Epstein, not from his peers.
- Kellen has said she was herself a victim, abused by Maxwell and two named men. The DOJ did not dispute that she was also a victim.
- All four assistants were named, and immunised, in the 2008 agreement. None has been charged.

So the "injection" at Maxwell's height was filled from inside the pool of people the operation drew in. That is a pattern the book should describe carefully and never as blame.

**To run this properly:** add Maxwell's documented operational ties from the 2021 trial record and court filings. That means staff she supervised, properties she managed, and introductions documented in testimony, each cited. No survivor is to be added unless she has gone public. Then rerun Sections 11 and 11b with dated edges.
