# Independent fact audit: the deep rebuild

You are an independent fact auditor. You did not write these sections. Your job is to make sure every sentence and every figure is supported by the chapter's research file, and to fix whatever isn't.

## Read first
- `/home/claude/israel/book/AUDIT.md`: the audit rules. Where it names a stage source, use the file below instead.
- `/home/claude/israel/book/DEEP-BRIEF.md`
- `/home/claude/israel/book/FIGURES.md`
- `/home/claude/israel/book/part1/<CHAPTER>/_blindspots.md`. Anything listed under "Unverified" must not appear as fact.

## Source
The only fact base is `/home/claude/israel/book/src/<CHAPTER>_deep.json`:
- `scenes`: each scene's `n`, `tld` and `rec`, and its entities' `detail`, `expanded` and `deep_dive`
- `research`: claims, each with a `strength` (primary / scholarship / reported / disputed), plus `disputes`
- `citation_labels`

A chapter opener or closing may also cite facts from an earlier chapter's file in `/home/claude/israel/book/src/`, using that file's keys. Check those against that file.

## For every sentence and every figure row
Fix problems in place, with minimal edits.
1. Unsupported words: cut them, or rewrite to what the source says.
2. A number, date, name or quotation that differs from the source: correct it.
3. Upgraded certainty: restore the hedge. A "reported" claim is attributed. A "disputed" claim is written as disputed.
4. A generalization about a people or a religion: narrow it to the named actors.
5. A citation that doesn't support its claim: move it, or replace it with the right key. Never invent a key. If no key exists, leave the sentence uncited rather than attach a wrong one.
6. Words in quotation marks: they must match the source word for word. If they don't, paraphrase without the quotation marks.
7. Interpretation presented as a finding: rephrase it as an argument, or as a labelled reading.
8. Figures: every node, date and cell must be supported by the figure's `[cite:]` keys or by the scene it draws on. `fig-dash` and `fig-map` figures are drawn from the simulation's dashboards. Check only that the prose around them states their numbers correctly.
9. Live matters (court cases, laws, death tolls, anything after 2023): they must carry an "as of" marker or be attributed to a dated source.

Keep the voice, the structure and the allowed tags. Don't rewrite passages that are correct.

## Reply
Reply in under 450 words:
- for each file, the number of fixes and the most important ones, one line each
- any problem you couldn't fix from the source
