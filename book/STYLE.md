# The Israel Architecture — Book One: The Stages to 1948
## Writing brief for each section

You are writing part of an online history book drawn from a research simulation. The simulation already holds the research: each "scene" has a narration (`n`), a "what we were told" line (`tld`), a "what the record shows" line (`rec`), and entities with details, expanded details and deep dives. Your job is to turn your assigned scenes into book prose, as a careful historian would write it.

### The one hard rule: no new facts
Use only facts that appear in your source file. Do not add names, dates, numbers, quotations or events from your own knowledge, even if you are sure of them. If the source is thin on something, the prose stays thin on it. If the source marks something as disputed, contested, reported or unverified, the prose says so in plain words ("historians disagree," "according to," "this has not been confirmed"). Never upgrade a claim's certainty. Keep numbers exactly as given.

### Citations
The source text carries citation markers like `[cite:herzl_judenstaat]`. Keep them. Put each marker right after the sentence it supports, exactly as written. Every paragraph that states facts drawn from a source passage that had a citation should carry that citation. Don't invent citation keys. Use only keys that appear in your source file.

### Cross-references
To point the reader to another scene, write `[scene:SCENE_ID|short label]`, e.g. `[scene:s06|the Balfour Declaration]`. Use only scene IDs listed in `all_scene_titles_in_stage` or that appear in your source text. Use them sparingly, at most two per section.

### Voice
- A historian writing for an intelligent general reader. Third person, past tense for events, measured and precise. Vivid through specifics (a date, a sum, a named person, a document's own words), never through adjectives or outrage.
- Narrative, not a list. Connect each scene to what came before and what it made possible. Explain why something mattered.
- Where the record contradicts what is commonly taught (`tld` vs `rec`), make that contrast clear in the prose. Don't label it "told" and "record"; write it as a historian would ("The familiar account holds that… The documents tell a different story.").
- No internal research vocabulary: never write "tier," "CONFIRMED," "REPORTED," "QOP," "entity," "scene," "node," "Kevin Bacon," "Pass 1," "the simulation," or "this module." Refer to the work as "this book" if you must.
- No code. Some scenes are titled "The Machine in Code" or show Objective-C. For those, write a short section titled "The mechanism, in plain terms" from the plain-language explanation only.
- Some scenes offer a symbolic, esoteric or interpretive reading (e.g. a reading of the name IS-RA-EL). Keep them, but frame them plainly as one interpretation: "One symbolic reading holds…", and say it is a reading, not a documented finding.
- When a scene names a fairness point or "the other side" (critics, disputes, where the research could be wrong), keep it. Balance is part of the book's credibility.
- Keep any claim about a group of people tied to documented institutions, movements, states and named individuals. Never generalize about Jews, Arabs, Christians or any people as a group.
- Plain, readable sentences. Vary length. Avoid clichés ("a tapestry," "in a world where," "little did they know"). No rhetorical questions in a row. No exclamation marks.

### Length
- Each scene becomes one section of about **450–800 words**, longer where the source is rich (deep dives), shorter where it is thin. Never pad.
- If `write_intro` is true: a stage introduction of 150–250 words that sets the period and the question the stage answers.
- If `write_outro` is true: a closing passage of 120–220 words, "What this stage built," summarizing what was in place by the end of the stage. Use `all_scene_titles_in_stage` for scope, but state only facts from your own source file.

### Output: one file per section
Write files into `/home/claude/israel/book/part1/<STAGE>/` (create the folder; STAGE is the stage id, e.g. `rd1`):
- One file per assigned scene, named `<SCENE_ID>.html`. First line: `<h2>Section heading</h2>`. A good heading is short and specific (it may adapt the scene title; drop internal jargon). Then the prose as `<p>` paragraphs. Allowed tags only: `<h2>`, `<p>`, `<em>`, `<strong>`, `<blockquote>` (for a document's own words, quoted exactly as in the source). No other HTML, no classes, no inline styles.
- If you write the intro: `_intro.html` (paragraphs only, no heading).
- If you write the outro: `_outro.html` (paragraphs only, no heading).

### Before you finish
Re-read each file once against the source: every number, date and name must match; every citation marker must be a real key from the file; nothing added. Then reply with a one-line summary: files written and approximate total words.
