# Writer's brief: the deep rebuild of a library chapter

You are writing sections of a history book: *The Israel Architecture*, a library of the documented record. This rebuild replaces earlier summary-depth drafts with the full, deep version. The reader should finish each section fully informed, with no confusion and nothing left out that the research holds.

Before you start, read these three files in full:
1. `/home/claude/israel/book/STYLE.md`: the voice and the hard rule against new facts. Its length guidance (450–800 words) is **replaced** by the length rules below.
2. `/home/claude/israel/book/LIBRARY-PROTOCOL.md`, sections 2, 5, 6 and 7.
3. `/home/claude/israel/book/FIGURES.md`: figure markup.

## Your fact base: one file

`/home/claude/israel/book/src/<CHAPTER>_deep.json` contains:
- `sections`: the chapter outline. Each section has an id, its main scene, the scenes it draws on from other chapters, its research entries, a brief, and the writer it is assigned to.
- `scenes`: the research for every scene in the chapter. Each has its narration `n`, `tld` ("what people are told") and `rec` ("what the record shows"), and every entity's `detail`, `expanded` and `deep_dive`.
- `research`: new research addenda, verified live. Each claim carries a `strength`:
  - **primary**: an original document. Can be stated directly.
  - **scholarship**: a reference work or scholar. Can be stated directly or attributed.
  - **reported**: attribute it ("according to …").
  - **disputed**: present the dispute, never one side as fact. The entry's `disputes` list gives the positions.
- `citation_labels`: every citation key you may use.

Use only facts from this file: no names, dates, numbers, quotations or events from your own knowledge, however sure you are. Keep every number exactly as given. Never upgrade or soften certainty.

## Using all of it

For each section assigned to you, the material to use is:
- its main scene: everything in it, including every entity's detail, expanded text and every deep-dive section
- the scenes listed in its `draws`
- the research entries listed in its `research`

**Use all of it.** Every figure, date, named person, document and citation in that material belongs in your prose. The one exception is a fact that clearly belongs to another section of this chapter (check the other sections' briefs): mention it in a phrase and link to that section. If you leave something out for any reason, list it in your reply with the reason.

A deep-dive section that you leave out is a gap in the book. A scene drawn from another chapter whose main subject belongs to a later period gets told briefly, as far as it touches this chapter, and linked: `[scene:ID|label]`.

## What each section must do

Work these in as the material allows. Use plain prose, not labeled sub-sections, except for figure captions.
- **Narrative.** What happened, in time order, who decided it, and why it mattered then and after.
- **Mechanism.** How the structure worked: who had the power to act, through what instrument, and who could not act.
- **Money**, where the material has it: who paid, through what channel, who gained, and who bore the cost.
- **The dispute.** Where historians or sources disagree, give each side's evidence and the strongest form of each case. Where Israeli and Palestinian, Zionist and Arab, or British and Arab readings differ, give both fairly.
- **The gap.** What the record does not settle, stated plainly, near the end of the section.
- **The claim and the record.** A box above each section already shows the scene's "what you were told / what the record shows" pair. Don't repeat it word for word; engage with it in the prose, the way a historian answers a common misconception.

**Figures.** Follow FIGURES.md. Include the figures named in the section's brief, plus any others that make a mechanism, sequence or comparison clearer. Every figure ends with its `[cite:]` sources and shows only what they support. Most rich sections carry one or two figures. The network diagram is drawn automatically, so don't make one.

**Length follows the material.** A section built on a rich scene with deep dives runs about 1,500–3,000 words. A section on a thin scene with research addenda runs about 900–1,800. Never pad. If you run short, you have probably left material unused, so go back to the source.

**Voice.** A historian writing for an intelligent general reader:
- precise, measured, specific
- vivid through documents, dates and sums, not adjectives
- no internal vocabulary: never "tier", "scene", "entity", "the simulation", "research addendum" or "deep dive"
- never generalize about a people or religion

## Markup

The first line is `<h2>Section heading</h2>`. After that use only these tags:
- `<p>`, `<em>`, `<strong>`, `<blockquote>`
- figure markup exactly as in FIGURES.md: `figure`, `figcaption`, `ol`, `ul`, `li`, `b`, `time`, `table`, `thead`, `tbody`, `tr`, `th`, `td`, `dl`, `div`, `dt`, `dd`, `p class="fig-src"`

Rules for citations and links:
- Citations: `[cite:key]` right after the sentence it supports, using keys from `citation_labels` only. Research keys start with `rs_`.
- Cross-references: `[scene:ID|label]`. Use either a section id from this chapter's outline, or a scene id from the file. Use at most three per section.

Write each section to `/home/claude/israel/book/part1/<CHAPTER>/<section id>.html`, replacing any earlier draft completely.

## Before you finish

Re-read each file against the source. Check:
- every number, date, name and quotation matches
- every citation key exists and is attached to the claim it supports
- disputed claims are written as disputed
- nothing has been added

Then reply with:
- for each file: its word count and number of figures
- anything you left out, with the reason
- any place where the sources contradict each other (give both versions)
