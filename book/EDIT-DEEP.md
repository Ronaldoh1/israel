# Editor's brief: the deep rebuild

You are the editor of one chapter of the deep rebuild. Several writers wrote it, a finisher added the opener and closing, and two independent auditors have fact-checked it. Your job is to make it read as one book by one historian, consistent from section to section, without adding facts.

## Read first

- `/home/claude/israel/book/EDIT.md`
- `/home/claude/israel/book/DEEP-BRIEF.md`
- `/home/claude/israel/book/FIGURES.md`
- the whole chapter in manifest order: `_intro`, every section in `/home/claude/israel/book/part1/<CHAPTER>/_manifest.json`, then `_outro`. For ch01, read each `_intro_baseN` before its chapter.
- `/home/claude/israel/book/part1/<CHAPTER>/_conflicts.md`

The fact base is `/home/claude/israel/book/src/<CHAPTER>_deep.json`. Introduce nothing new. Keep every `[cite:]` attached to the claim it supports.

## Tasks

**1. Consistency.** The same fact, figure, name, title, date or dispute must read the same way everywhere in the chapter. When two sections tell the same dispute differently, align them to the fuller and better-sourced telling. Tell it in full in the section that owns it, and refer to it briefly elsewhere. Use one spelling for each name throughout.

**2. Repetition.** Where two sections tell the same event at length, keep the fuller telling in the owning section. Cut the other to a phrase plus `[scene:ID|label]`, keeping to at most three such links per section.

**3. Flow.**
- Each section's first paragraph connects to the one before it.
- No mechanical summaries at section ends.
- Vary sentence length.
- Cut clichés and filler: "it is worth noting", "crucially", "notably", "in other words".
- Cut any internal vocabulary: scene, entity, simulation, tier, deep dive, research addendum.

**4. Figures.**
- Each chapter embeds at most two maps (`fig-map`). If the same map appears more than once, keep it in the section where it fits best.
- No two figures should show the same thing; drop the weaker one.
- Figure titles must be specific.
- Flows have at most 7 steps; tables at most 4 columns; power trees at most 10 boxes.

**5. Links.** Every `[scene:ID|label]` must point to an id that exists in one of the library's manifests (`book/part1/*/_manifest.json`) or in the simulation. Check with `grep -o '"id":"ID"' /home/claude/israel/index.html`. Remove dead links, keeping the label as plain text.

**6. Coverage.** Finish by running `python3 tools/book_coverage.py <CHAPTER> --list`. For each remaining unit, either write it in, if it belongs, or add a set-aside with a reason to `_coverage.json`. Typical reasons:
- unverified and deliberately not printed
- a key from a reading list that isn't attached to any claim
- boilerplate whose substance is already used
- later-period material

Run it again until it prints PASS.

## Reply

Reply in under 400 words with:
- the main changes, by section
- the final word count for the chapter
- the coverage result
- any contradiction you couldn't resolve
