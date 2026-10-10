# The Israel Architecture Library: To-Do

This list covers the library only (the books, covers and the Lines chapter). Simulation fixes, Eleven Minutes and elections work are tracked elsewhere.

Status as of 9 October 2026: 2 of 67 volumes written (I, The Baseline; II, The Road to 1948).

---

## 0. Deep rebuild of Volumes I and II (LIBRARY-PROTOCOL.md) — DONE 10 October 2026

- [x] Protocol, figure markup, writer/planner/finisher/audit/edit briefs, coverage check (`tools/book_coverage.py`).
- [x] Chart engine: dashboards and maps drawn inside the book (`tools/charts.js`), standalone modules (`modules/`), JSON data layer for Next.js (`export/`).
- [x] All 14 chapters rebuilt (Baseline 6 + Lines, Road to 1948 Prelude + 6 stages): cross-library pull, blind-spot research (≈1,000 new sourced claims), writing, coverage PASS, independent fact audit, edit. About 320,000 words of prose, 585 figures, 210 sections; every note resolves; no figure overflows on phone or desktop.
- [ ] **Ron reviews Volumes I and II.** His sign-off locks the standard.
- [ ] **Research the gaps the web-search limit cut short** (listed per chapter in `book/part1/<chapter>/_blindspots.md`), among them:
  - Baseline: holy places and the status quo; where "Nakba", "settler colonialism" and "Judea and Samaria" come from; Israeli textbooks and the 2011 Nakba Law; Christian positions beyond Christian Zionism; the Hebrew revival and Arabic; exodus figures for Tunisia, Syria and Lebanon.
  - Prelude: Zahir al-Umar and Jazzar; the Damascus affair; the 1852 Status Quo; Montefiore; Ahad Ha'am's 1891 essay; Arab population by decade; the 1886 Petah Tikva clash.
  - Stage One: the Hebrew revival and the 1913 "language war".
  - Stage Two: Sèvres and Lausanne; the churches on the Mandate; the Syrian General Congress.
  - Stage Three: the kibbutz movement; the Syrian revolt's effect; Haifa harbour; Arab immigration in the 1930s.
  - Stage Four: the Yishuv's response to the Holocaust; the Jewish Brigade; British ministers before Bevin; the Arab League 1944–45; the American Council for Judaism; Tower and Stockade; Bludan.
  - Stage Five: the Arab League's 1945–48 decisions; the date of the US embargo; Arab war dead; Operations Yoav, Hiram and Horev; Security Council Resolution 50.
  - Stage Six: the Tripartite Declaration; refugee compensation in 1951; selective immigration rules; Bedouin and Galilee land.
- [ ] **Verify every quotation from the new research against the original page** (the research tool reads page summaries).
- [ ] **Fix the simulation** where the books found it wrong or self-contradictory (≈230 entries in `SOURCE-CONFLICTS.md`). Priority: the Arab Revolt toll in s07a5 (2,652 Jews / 618 British, attributed to USHMM, unverifiable, every other source gives ~400–415 / 100–200); s10's "750,000 undisputed"; citation keys attached to the wrong claims (oc_ch03, us_s08, iaa_s03).
- [ ] **Replace the Grokipedia citations** in the simulation (7 keys) with primary or neutral sources.
- [ ] **Bring the new research into the simulation** as scenes (`book/research/TO-SIMULATION.md` and the planners' notes in `book/research/*-notes.md`).
- [ ] Fill empty citation labels in the simulation's registry (e.g. `w_arafat`, `wiki_flag_of_israel`, `palquest_wzo`).
- [ ] Ask Ron for Books 0–9 (July–August 2026) and the deliberation file, to use as leads (each fact entered as a sourced research addendum).

## Translations (when the volumes are done)

- [ ] **Translate the finished library into Spanish and Arabic**, volume by volume, once Ron signs off on each one:
  - prose, figures, figure captions, callouts and the Lines chapter
  - the library chrome: shelf, search, menus and labels (the simulation already has ES and AR interface strings to reuse)
  - right-to-left layout for Arabic in the reader and on every figure type (flows, timelines, trees, tables, charts and maps)
  - native-speaker review of each language before release, for register and for technical and religious terms
  - keep citations, numbers, dates and names identical across all three languages, and check this automatically

## 1. Write the remaining volumes (III–LXVII)

- [ ] Write each volume with the same process as I and II:
  1. Extract the sources (`tools/book_extract.py`).
  2. Write to `book/STYLE.md`.
  3. Audit to `book/AUDIT.md`.
  4. Edit to `book/EDIT.md`.
  5. Run the guard script: no new numbers, citations, scene references or names.
- [ ] For each finished volume:
  - Add its chapter id to `done` in `tools/embed_book.py`.
  - Add it as a `books` entry with `status:'ready'` and chapters (or stages).
  - Rebuild with the full pipeline (below).
- [ ] Decide the order of writing. Suggested order: the volumes the Lines chapter points to most often.
  - October 7 and Gaza
  - The 1948 refugees and the CIA estimate
  - Israel aid architecture
  - The Comment Section
  - AIPAC
- [ ] Log every contradiction found inside the simulation in `book/SOURCE-CONFLICTS.md`. Don't resolve them silently.

## 2. Covers (do last, all at once)

- [ ] Once the writing is done, write one ChatGPT image prompt per volume (67), in a single batch with a consistent house style.
- [ ] Save the images to `book/covers/` and set each book's `cover` field. Until then, the CSS cloth covers stay as placeholders.

## 3. The Lines You've Heard (Baseline, Chapter 7): links

Each of the 55 claims ends with "Read more" links to the volume that holds the full record.
- Links to Volumes I and II open inside the library.
- Links to unwritten volumes are labeled "in preparation" and open the matching simulation scene for now.
- The links and labels update automatically when a volume is marked ready and the library is rebuilt.

- [ ] After each volume is written, rebuild and spot-check its Lines links. Confirm each one lands on the right section and the "in preparation" note is gone.
- [ ] Once a volume has its own chapter titles, point links at the best section, not just the first matching scene. Edit `scenes` in `book/lines/plan.json` if needed.
- [ ] When all volumes are done, do a final pass: no "in preparation" notes left (`grep ln-prep index.html` should return nothing).

## 4. The Lines You've Heard: content

- [ ] **Ron: scrape and send the social-media talking points.** Ron is collecting the lines himself from Reddit, X, TikTok and Instagram comments and will drop them into this project. For each one, include the exact wording, where it was seen, and roughly how often. When they arrive, Claude will:
  - match each to an existing Line or flag it as new
  - check new ones against the simulation
  - add a scene where one is missing
  - write the entry and its links
- [ ] **Social listening.** The chapter's list was built from four sources:
  - the platform's own talking-points audit
  - the simulation's "what you were told" lines
  - a published hasbara messaging study
  - the chapter themes of the main "Myths and Facts" handbook

  Reddit and X could not be read from this environment. Options:
  - (a) Run the scrape through the browser in the desktop app.
  - (b) Ron exports posts or threads from the groups he watches.
  - (c) Use a third-party dataset.

  Then add any high-frequency lines that are missing.
- [ ] **Research and build the 17 lines that have no simulation scene yet.** Each needs a scene before it can get an entry, because there are no new facts in the book.
  - Lines aimed at Jews:
    - "Jews control the media, Hollywood and the banks"
    - "The Jews killed Jesus"
    - "Israel or Mossad was behind 9/11"
    - "The Protocols" (forgery history)
    - IDF organ-harvesting claim (separate the 2009 story from the Abu Kabir admissions)
    - "Dual loyalty" (the trope, distinct from lobbying questions)
    - Holocaust denial of the camps and gas chambers
    - "Israelis are the new Nazis" (Holocaust inversion)
  - October 7 and after:
    - The sexual violence reports and the denial of them (the UN Patten report, investigations, disputed accounts)
    - UNRWA staff and October 7 (the Colonna review)
    - "From the river to the sea" (history and competing uses, including Likud's 1977 platform)
    - "Hamas is ISIS" (ideology, aims, documented rivalry)
  - Other lines:
    - "Only progressive state / gay rights in Tel Aviv" and the pinkwashing argument
    - Suez 1956: Sèvres and who struck first
    - Smotrich's Greater Israel map (keep it distinct from Netanyahu's 2023 UN map)
    - "Never Again" universal vs. particular
    - "They elected Hamas" (no vote since 2006; Gaza's age profile)
- [ ] Build a dedicated scene on rockets after the 2005 disengagement. "Israel gave Gaza back and got rockets" currently leans on `dis_s01` only.
- [ ] Review the "beheaded babies" verdict (currently Unsupported). Decide between Unsupported and False against the sources in `o7_s06` and `o7_s08`. Re-check live at the time, because reporting continues.
- [ ] Re-verify every entry tied to live events (Gaza toll, ICJ case, IHRA bills, UNRWA funding) at each rebuild. Add "status as of [date]" where it is missing.

## 5. New conflicts found while writing the Lines chapter

Add these to `book/SOURCE-CONFLICTS.md` and fix them in the simulation:
- [ ] `cia_s14` calls Maxwell a "confirmed" Mossad asset. Other scenes treat this as reported or alleged. Bring it in line.
- [ ] `s19`: Bush campaign spending is given as $14.5M in one place and about $8.5M in another.
- [ ] `gia_s01` and `gia_src_s02` disagree on the Smotrich map.
- [ ] `s10b`: the July 1948 refugee estimate is attributed to both the CIA and the State Department. The documented estimate is the CIA's of 27 July 1948 (97,800 vs 46,800).

## 6. Reader features (nice to have)

- [ ] Spanish and Arabic translations of the written volumes (the simulation already has ES and AR).
- [ ] A share image or screenshot of a passage or a single Line, with a deep link (`#book=ln-<id>`).
- [ ] A filter in the Lines chapter by verdict (False, Misleading, Half true, and so on) and a search across lines.
- [ ] Reading-time estimate per chapter on the contents sheet.

---

## Rebuild pipeline (after any book change)

```
python3 tools/embed_book.py
python3 tools/embed_ux.py
python3 tools/embed_israel.py
python3 tools/eleven_sophia_slide.py
python3 tools/embed_israel.py --check
```
