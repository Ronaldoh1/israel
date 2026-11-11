# Finisher's brief: chapter openers, closing synthesis and coverage

The sections of your chapter have been written to the deep standard. You finish the chapter in two parts.

**Read first:**
- `/home/claude/israel/book/DEEP-BRIEF.md` (and the files it lists)
- `/home/claude/israel/book/LIBRARY-PROTOCOL.md`
- `/home/claude/israel/book/FIGURES.md`
- the chapter manifest `/home/claude/israel/book/part1/<CHAPTER>/_manifest.json`
- every section file, read in manifest order

The fact base is `/home/claude/israel/book/src/<CHAPTER>_deep.json`, plus what the sections already say. Introduce nothing new.

Use the finished Stage Two as the model for tone and shape: `/home/claude/israel/book/part1/rd2/_intro.html` and `_outro.html`.

## 1. Openers and closing

### Volume II stages (rd0–rd6)

**`_intro.html`** (400–700 words; no heading; `<p>` paragraphs). Cover:
- where things stood at the start of the stage
- the question the stage answers
- the main actors on every side
- a brief map of what the reader will meet, written as prose

End with one timeline figure of the stage's turning points (at most 9 entries).

**`_outro.html`** (700–1,100 words; no heading; the reader titles it "What this stage built"). A historian's synthesis of the architecture at the end of the stage, layer by layer:
- legal
- administrative
- institutional and financial
- the Palestinian Arab side
- regional
- American

Say what was settled, what was contested (each side's strongest case) and what the record leaves open. Include:
- a power-structure figure (`fig-tree`, at most 10 boxes)
- a comparison figure: who had secured what, and been refused what, by the end of the stage

**rd6 only:** its outro closes the whole of Volume II. Synthesize the full road from 1694 to the 1950s in 900–1,400 words.

### Volume I, The Baseline (ch01)

Write one opener per thematic chapter as `_intro_<chapter id>.html`, for base1 to base6 (200–400 words each). Each one:
- says what the chapter establishes and why it comes here
- gives a brief map of its sections

Also rewrite:
- `_intro.html`: the volume introduction, 400–600 words. Say what the Baseline is for: clearing the ground before the history, so the reader starts with the facts, the definitions and the ways the story is told.
- `_outro.html`: the reader titles it "What the Baseline establishes", 600–900 words. Synthesize what a reader now knows for certain, what remains disputed, and what the volumes ahead will test.

The Lines chapter is separate; don't touch it.

## 2. Coverage

Run `python3 tools/book_coverage.py <CHAPTER> --list`. For every unit reported missing, do one of the following:
1. **It belongs in this chapter:** write it into the right section, following the deep brief, with minimal additions.
2. **It is legitimately out of scope:** add it to `/home/claude/israel/book/part1/<CHAPTER>/_coverage.json` under `"set_aside"`, using the unit id exactly as printed (`cite:key`, `number:1942`, `deepdive:scene/entity/n`), with a one-line reason. Typical reasons:
   - "later-period material from a drawn scene; told in volume X"
   - "citation attached to the wrong claim in the simulation (logged in SOURCE-CONFLICTS)"
   - "boilerplate restating the entity detail, which is used in section Y"
   - "figure from a dashboard row with no scene source"

Keep any existing entries in that file. Run the script again until it prints PASS.

Then list every source contradiction the chapter's prose presents (the places where it gives two versions of a fact) in `/home/claude/israel/book/part1/<CHAPTER>/_conflicts.md`, one line each, with the scene ids involved. Other agents are editing `SOURCE-CONFLICTS.md` at the same time, so don't edit it; the conflicts will be merged into it afterwards.

Reply in under 400 words with:
- word counts for the files you wrote
- the figures in them
- the final coverage result
- how many units you wrote in and how many you set aside
- the three most important contradictions in the chapter
