# Planner's brief: preparing a chapter for the deep rebuild

You are preparing one chapter of *The Israel Architecture* library for its deep rebuild. Writers will work only from what you prepare, so the plan must be complete.

Read these first:
- `/home/claude/israel/book/LIBRARY-PROTOCOL.md` (all of it)
- `/home/claude/israel/book/DEEP-BRIEF.md`
- `/home/claude/israel/book/FIGURES.md`
- The finished example for Stage Two: `/home/claude/israel/book/part1/rd2/_manifest.json`, `/home/claude/israel/book/part1/rd2/_blindspots.md`, and `/home/claude/israel/book/research/vol2.json` (look at its structure; you don't need to read every claim).

## Your inputs

- `book/src/<CHAPTER>.json`: the chapter's own scenes, with all their research.
- `book/plan/<CHAPTER>_candidates.json`: scenes elsewhere in the simulation that overlap your chapter's dates or share its people. Read the ones that look relevant in full: run `python3 -c "import json,re;..."` against `/home/claude/israel/index.html` (the `scenedata`, `expanded-en` and `deepdive-en` script tags), or run `python3 tools/book_extract.py` with a scratch output.
- `book/plan/pre1950_outside.json`: all 84 scenes outside Volumes I and II dated before 1950. Check every one for relevance to your chapter.
- `book/plan/visuals.json`: the simulation's dashboards (with their individual panels) and maps.
- `already_claimed_by_other_chapters` in your candidates file: scenes another chapter already tells in full. Don't draw them; link to them.

## What you produce (all inside `/home/claude/israel/book/`)

### 1. `part1/<CHAPTER>/_blindspots.md`
Use the same three parts as Stage Two's.
- **The period checklist.** What any authoritative history of this period or theme covers: events, documents, people, institutions, laws, wars, turning points, and the numbers that matter. Mark each item:
  - covered (give the scene id)
  - researched now
  - out of scope, with where it is covered
- **The series blind-spot list** from protocol section 4, applied to this chapter.
- **Unverified.** What your research could not confirm, kept out of the prose.

### 2. `research/<CHAPTER>.json`: live research for the gaps
- Use the same structure as `vol2.json`. `"volume"` is `"road1948"` for Volume II or `"baseline"` for Volume I. Each entry has `"stage": "<CHAPTER>"`.
- Research each gap live with WebSearch and WebFetch. Every claim must come from a page you fetched, and you record its URL. Never rely on memory.
- Prefer sources in this order: primary documents, then scholarship and reference works, then established neutral, Israeli or Palestinian outlets. Never use conspiracy sites, Grokipedia, or Wikipedia as the only source for a number.
- Record disputes with both positions. Be even-handed. Never generalize about a people or religion.
- Citation keys are `rs_<CHAPTER>_...`: lowercase, unique, and every claim must cite a key defined in its own entry.
- Aim for the gaps that matter most to a serious reader of this period: roughly 6–12 topics, each with 6–15 precise dated claims.
- Also write `research/<CHAPTER>-notes.md`: per topic, what the sources agree on, where they disagree, and what you could not verify.

### 3. `part1/<CHAPTER>/_manifest.json`
- Use the same shape as Stage Two's: `chapter`, `title`, and `sections` in **historical order**.
- Every scene in the chapter's own list must appear as a section's `scene` or in a `draws` list.
- Each section has these fields:
  - `s`: the section id. Use the scene id when the section is built on a scene; use a new id `<CHAPTER>_<slug>` for a section built only on research.
  - `scene`: its main scene, if it has one.
  - `draws`: other scenes it tells. These can be other scenes from this chapter that belong together, or scenes from elsewhere in the simulation.
  - `research`: entry ids from your research file.
  - `writer`: a letter. Group 3–5 sections per writer, by time period. A writer should have roughly 5,000–9,000 words of source material.
  - `brief`: 2–5 sentences. Say what the section must cover, in what order, which disputes it must present from both sides, and which figures it needs. Name the dashboard panels by `ref` (e.g. `money_1948:Dollar Flows:0`) and the maps by id where they fit. The section must discuss their numbers.
- Pull in every relevant scene from elsewhere in the simulation. Where a scene's main subject belongs to a later period, put it in `draws` with a brief that says to tell only the part that falls in this chapter and link forward.
- Merge two of the chapter's own scenes into one section only when they tell the same story. Otherwise keep one section per scene.

### Volume I, The Baseline (chapter id `ch01`): a different shape
`ch01`'s manifest has `"chapters"` instead of `"sections"`:
```json
{"chapter":"ch01","title":"The Baseline","chapters":[{"id":"base1","title":"…","intro":"one or two sentences","sections":[…]} , …]}
```
- Keep the current six thematic chapters unless the material clearly argues for a change:
  1. Getting Your Bearings
  2. The Land Before the State
  3. Words and Names
  4. Peoples and Traditions
  5. Two Displacements
  6. How the Story Is Taught
- The Baseline is thematic, so draw relevant scenes from anywhere in the simulation on its themes, by subject rather than date. Examples: the Semitic languages and peoples, antisemitism as a word and as a hatred, the Mizrahi exodus, coexistence, Christian Zionism, the curriculum, the Ottoman order (`me_s01`).
- Section ids are unique across all six chapters.
- The Lines chapter is separate; don't plan it.

## When you finish

Validate your JSON with `python3 -m json.tool`. Check that every own scene is placed, every research key is unique and cited, and every dashboard `ref` exists in `visuals.json`.

Then reply in under 300 words:
- sections and writers
- scenes drawn from elsewhere
- research topics, with claim and source counts
- the biggest gaps you found
- what you could not verify
