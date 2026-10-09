# The Israel Architecture Library: Build Protocol

**Version 1.0 · locked 9 October 2026**

This protocol governs every volume in the library. The library is meant to be the center of the documented record on the architecture of Israel. Every volume should be complete from end to end, sourced line by line, and written so that a careful reader leaves with no confusion and finds no error.

Volumes I (*The Baseline*) and II (*The Road to 1948*) are rebuilt first, to this standard. Once Ron approves them, they become the reference: every later volume is measured against them.

This protocol sits on top of three existing files. Where this protocol asks for more, it wins.
- `book/STYLE.md` (voice and markup)
- `book/AUDIT.md` (fact audit)
- `book/EDIT.md` (editorial pass)

---

## 1. Why a second pass: the gap in the first drafts

The first drafts of Volumes I and II were written to a summary standard of 450–800 words per section, from each section's own scene only. A measurement on 9 October 2026 found the following.

| Measure | First drafts |
|---|---|
| Research words in the 150 source scenes (narration, entity detail, expanded text, deep dives) | 209,980 |
| Words written | 91,999 (44%) |
| Deep-dive sections substantially used | 836 of 2,442 (34%) |
| Distinct figures (numbers) carried into the prose | 80% |
| Citations carried | 100% |
| Pre-1950 scenes elsewhere in the simulation that the two volumes never drew on | 84 |

Those 84 scenes include:
- The Ottoman order before the borders, the three wartime promises, the Cairo Conference, and oil and the route to India (`me_s01`–`me_s07`, `or_s01`)
- The 1945 meeting before the state and the FBI watching in 1947–48 (`fis_s01`–`fis_s04`)
- The Shai and the OSS, and the CIA's opposition in 1948 (`cia_s01`, `cia_s02`)
- The Bitter Lake meeting (`isa_src_s01`)
- The two banks of the Jordan (`ijr_src_s04`)
- Jinnah's telegram (`ipk_s07`)
- Vatican non-recognition (`vat_s01`)
- Palestinian political origins (`hma_src_s02`)
- Lebanon's 1948 (`ilb_s01`, `ilb_s02`)
- Others

Some topics any serious history of the period covers are thin or missing from the research itself:
- Ernest Bevin: no scene
- the Faisal–Weizmann agreement of 1919: none
- the Muslim-Christian Associations: none
- 'Izz al-Din al-Qassam: only outside the volumes
- the kibbutz movement: thin

The first drafts were accurate, but they were not yet complete. This protocol closes both gaps: the research we already have that went unused, and the research we have not done yet.

---

## 2. The fact base: what a volume may say

A fact can enter a volume from three places only. Every fact carries a citation that resolves to a working source.

1. **The simulation: every scene relevant to the volume, not just its own chapter.**
   - A volume draws on all 960 scenes.
   - The writer runs a *cross-library pull*: every scene whose dates fall in the volume's period, and every scene that shares its people, institutions, documents or places.
   - Scenes from other chapters are woven in where they belong in the story.
   - A scene whose main subject belongs to a later volume is summarized briefly and linked forward with `[scene:ID|label]`.

2. **Research addenda: new research that fills a blind spot.** These live in `book/research/<volume>.json`.
   - Each entry is a claim, a date, a source URL, a citation key and label, and the date it was verified.
   - Each entry also carries a note on how strong the evidence is: primary document, named reporting, disputed, or not established.
   - Addenda are researched live, never from memory. The preferred sources are primary documents, then scholarship, then neutral or Israeli and Palestinian reporting. Conspiracy sites are never used.
   - Every addendum is also queued to become a simulation scene (`book/research/TO-SIMULATION.md`), so the simulation and the library stay one record.

3. **Ron's earlier work: Books 0–9 (July–August 2026), the deliberation file and the Project research docs.**
   - These are leads, not citations.
   - A fact from them is used only when it is traced to a citable source and entered as a research addendum.

Nothing enters from the writer's general knowledge, however certain it seems. If a point is needed and not yet researched, it goes to the addenda first.

---

## 3. Coverage: nothing in the research is left out by accident

For every chapter, a **coverage ledger** (`book/part1/<chapter>/_coverage.json`) is generated before writing and checked after. It lists every unit of research in scope:
- each scene's narration, its "what you were told" and "what the record shows" pair, and every entity's detail and expanded text
- every deep-dive section
- every figure (number), date, named person, institution and document
- every citation
- every link between entities

When the chapter is done, each unit is marked as one of:
- **used**, with the section it appears in
- **moved**, with the volume and section where it belongs better
- **set aside**, with a one-line reason (for example: duplicated elsewhere, or superseded by a better-documented figure that is logged in SOURCE-CONFLICTS.md)

**Thresholds for "done":**
- 100% of citations used
- 100% of deep-dive sections used, moved or set aside with a reason
- At least 95% of distinct figures and dates carried
- Every named entity used or accounted for

The coverage script (`tools/book_coverage.py`) reports these. A chapter that misses a threshold is not finished.

---

## 4. Blind spots: what a serious historian would expect to find

Before writing, each chapter runs three checks. The results are written down in `_blindspots.md` in the chapter folder.

1. **The period checklist.** List what any authoritative history of this period covers: the events, documents, people, commissions, wars, laws and turning points. Mark each item:
   - covered by the simulation
   - researched now into the addenda
   - deliberately out of scope, with the reason and where it is covered instead

2. **The series blind-spot list.** These come from the earlier series audit and apply wherever they are relevant.
   - Palestinian political agency, including rivalries and choices: Husseini–Nashashibi, al-Husseini's wartime alliance with the Axis, the decisions of Arab leaders
   - The strongest version of the Zionist case, stated fairly in its own terms
   - Jewish dissent from Zionism, from Reform, the Bund, Ahad Ha'am, Magnes, Buber and Arendt
   - The Jews of the Arab world and Iran, and the Mizrahi exodus
   - Real antisemitism, named plainly, wherever it is part of the story
   - Palestinian citizens of Israel, from 1948 onward
   - Key terms examined rather than assumed ("colonialism", "transfer", "terrorism", "Semitic")
   - Convergence, not conspiracy: show which power acted, for what interest, and who opposed it inside the same government
   - Where money followed political alignment, and where it did not
   - Sources kept independent: no load-bearing claim rests on a single outlet or a single advocate

3. **The reader's questions.** For each section, list the three to five questions a curious reader would ask next. Each one is answered in that section, or the section says plainly that the record does not answer it.

---

## 5. Depth and structure

**Length follows the research, never padding.**
- A section built on a rich scene with deep dives runs about 1,500–3,000 words. A thin one stays short.
- A chapter (or stage) typically runs 12,000–25,000 words.
- If a section feels short, the fix is to pull more research or add addenda, not to add adjectives.

**Every chapter has:**
- An **opener** that sets the period, the question the chapter answers, and the state of things at its start.
- **Sections** in historical order. A cross-library scene is placed where it happened in time, not where it sits in the simulation.
- In each section, as the material allows:
  - the narrative, in historical order: what happened, who decided it, and why it mattered
  - the mechanism: how the structure worked, and who could and could not act
  - the money: who paid, through what channel, and who benefited
  - the dispute: what historians argue about, with each side's evidence and the strongest version of each case
  - the gap: what the record does not settle, said plainly
- **The claim and the record** box wherever the simulation pairs a common claim with the documented record.
- A **closing synthesis**: the architecture as it stood at the end of the chapter, with one synthesis diagram that shows the whole structure.

**Precision rules:**
- Every number keeps its unit, its date and its source.
- Every estimate says it is an estimate and gives its range.
- Wherever two sources disagree, both appear, and the disagreement is logged in SOURCE-CONFLICTS.md.
- Sworn testimony, official documents, named reporting and later recollection are each identified as what they are.
- Nothing is upgraded in certainty, and nothing is softened.

---

## 6. Diagrams

Readers should be able to see the architecture, not only read about it. The reader renders these figure types from plain markup. Every figure is numbered automatically, carries a caption, and ends with its source note. A figure may show only what the cited sources show.

| Figure | When to use it | Markup |
|---|---|---|
| **Network** (automatic) | Every section with two or more entities and documented ties | Built from the scene; no markup needed |
| **Process flow** | A mechanism, a procedure, a chain of decisions | `<figure class="fig-flow">` with an `<ol>` of steps |
| **Money chain** | Who paid, through what, compounding how, to whose benefit, at whose cost | `<figure class="fig-money">` with five `<li>` steps |
| **Timeline** | A sequence of dated events | `<figure class="fig-time">` with `<li><time>` entries |
| **Comparison** | Two documents, two promises, a claim against the record, before and after | `<figure class="fig-compare">` with a `<table>` |
| **Power structure** | Who sat above whom, and who answered to whom | `<figure class="fig-tree">` with nested `<ul>` |
| **Key figures** | The handful of numbers a section turns on | `<figure class="fig-stats">` with `<dl>` |

**Minimum per chapter:**
- one power-structure or synthesis figure
- one timeline
- a process or money figure for every section whose subject is a mechanism or a flow of money
- a comparison wherever two accounts or two documents are set side by side

Exact markup is specified in `book/FIGURES.md`.

Figures stay legible at phone width: at most 7 steps in a flow, at most 4 columns in a table, and labels under about 60 characters.

---

## 7. Voice and the lines we hold

- **The voice is a historian writing for an intelligent general reader**, as set out in STYLE.md: measured, specific, past tense for events, vivid through documents and dates, not adjectives.
- **No internal vocabulary appears in the prose.** No tiers, protocol names or "the simulation".
- **Never generalize about a people or a religion.** Claims are tied to named states, institutions, movements, documents and individuals.
  - Zionism is not Judaism.
  - Naming an elite is analysis; smearing a people is not.
- **Hold both directions to one standard.** A false or unsupported claim aimed at Jews and a false or unsupported claim aimed at Palestinians are treated the same way.
- **Interpretive and symbolic readings** are kept, and labeled as readings in a clearly marked passage. They are never presented as findings.
- **Live matters** (court cases, laws, investigations, death tolls) carry "as of [date]" and are re-checked at every rebuild.

---

## 8. The build sequence and its gates

Each chapter moves through these steps in order. It cannot move to the next step until the current gate is passed.

| Step | Output | Gate |
|---|---|---|
| 1. Extract | `book/src/<chapter>.json` plus the cross-library pull | All in-scope scenes listed |
| 2. Coverage ledger | `_coverage.json` | Generated |
| 3. Blind-spot pass | `_blindspots.md` plus `book/research/<volume>.json` | Every checklist item marked; every addendum has a live source URL |
| 4. Outline | `_outline.md`: sections, order, which research goes where, which figures | Every coverage unit assigned |
| 5. Write | Section files | STYLE.md and this protocol |
| 6. Coverage check | `tools/book_coverage.py` report | Thresholds in section 3 met |
| 7. Fact audit | A separate auditor who did not write the chapter | Every sentence traced to the fact base; nothing upgraded |
| 8. Editorial pass | EDIT.md | Reads as one author; no repetition across sections |
| 9. Render test | Phone (390 px) and desktop screenshots of every figure | No overflow; figures legible; links work |
| 10. Ron's review | Chapter sent for sign-off | Approved, or changes made |
| 11. Lock | Commit; mark ready in `embed_book.py` | Lines links update automatically |

---

## 9. Definition of done for a volume

- [ ] Every chapter passed all eleven gates.
- [ ] Coverage thresholds were met; every set-aside item has a reason.
- [ ] Blind-spot checklists are complete; every addendum is queued for the simulation.
- [ ] Figure minimums are met, and every figure has a source note.
- [ ] Every disagreement between sources appears in the prose and in SOURCE-CONFLICTS.md.
- [ ] The Lines chapter links that point at this volume have been checked.
- [ ] Ron has signed off.

---

*Observe. Collapse. Reignite.*
