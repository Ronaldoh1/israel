# Audit-and-fix brief for Book One

You are checking finished book sections against their research source and fixing problems in place. Read /home/claude/israel/book/STYLE.md first for the writing rules.

**Source:** /home/claude/israel/book/src/<STAGE>.json — the whole stage's research (scenes → n, tld, rec, entities[].detail, .expanded, .deep_dive). A fact is supported if it appears anywhere in this stage source file. Nothing from outside that file is allowed, even if true.

**Files:** /home/claude/israel/book/part1/<STAGE>/*.html (your assigned files, including _intro.html and _outro.html where listed).

**For every sentence, check and fix:**
1. Not supported by the stage source → cut the unsupported words, or rewrite the sentence to say only what the source says.
2. A number, date, name or quote that differs from the source → correct it to the source.
3. Certainty upgraded (source says disputed, reported, estimated, unverified, "according to", "one reading") → restore the source's hedge.
4. A generalization about a people or a whole religious group (Jews, Arabs, Christians, Muslims, Catholics…) → narrow it to the named institutions, leaders, organizations or documents the source names.
5. A `[cite:key]` attached to a claim its source passage doesn't support → move it to the sentence it does support, or replace it with the key the source attaches to that claim; if none, remove it. Never invent keys.
6. Where the source contradicts itself, say so briefly in the prose or use the better-documented version and note the discrepancy in your reply. Don't silently pick.

Make minimal edits with the Edit tool; keep the voice, structure and allowed tags (`h2, p, em, strong, blockquote`). Don't rewrite sections that are fine.

**Examples of problems another auditor found (fix these if they're in your files):**
- rd0/s03: "He recorded the moment as a turning point" (source: "He recorded the moment"); "developed over more than a year" (source: "years").
- rd1/s05: the 30–40 million figure carried [cite:wiki_scofield_bible]; source uses wiki_dispensation_theology for it. "Mainline Protestant denominations, most Catholic and Orthodox tradition, and Palestinian Christians have rejected Scofield's framework" overgeneralizes; source: mainline churches "largely do not embrace" it, Catholic tradition "does not endorse" it, explicit rejection by Palestinian Christian leaders (Kairos Palestine 2009).
- rd5/s07j: added "the Central Intelligence Agency would soon add its own warning" — not in source.
- rd5/s10: "Pappé argues that the events meet the UN definition" — source: Pappé argues Plan Dalet meets it.
- rd6/dsp_s01: "unresolved at Lausanne and in every negotiation since" — source: "remains unresolved"; "limited mandate" not in source.
- rd3/_outro: "rose to its Mandate-era peak in 1935" — source gives "over 60,000" in 1935, not a peak.

**Reply** with a short list: file → what you changed (one line each), and any source self-contradictions you noticed. Keep it under 400 words.
