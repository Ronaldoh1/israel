# Brief: system-architecture diagrams for Book V (The Eye)

Goal: give technical readers real architecture diagrams of the surveillance and data systems in Book V. Each diagram should show the components, the data that moves, the interfaces and identifiers (APIs, feeds, matching keys, standards), and how strong the evidence is for every link. It has to work for engineers who want depth without misleading anyone about what is actually connected.

## The figure format (new type: `fig-arch`; CSS and legend are already in the reader)

```html
<figure class="fig-arch">
<figcaption>Caption that says what system is shown (as of October 2026 where status matters)</figcaption>
<div class="arch">
<section class="ly"><h4>L1 · short layer name</h4>
<p>optional one-line note about the layer</p>
<div class="nodes">
<div class="nd"><b>Component</b><span>What it holds or does</span><code>technical detail: interface, key, standard, contract figure</code></div>
<div class="nd hub"><b>…</b>…</div>      <!-- the hub other systems feed -->
<div class="nd pos"><b>…</b>…</div>      <!-- exists, but no document shows it connected here -->
</div></section>
<p class="lk"><span><i>Documented</i>what moves across this link</span></p>          <!-- solid -->
<p class="lk rep"><span><i>Reported</i>…</span></p>                                    <!-- dashed -->
<p class="lk pos"><span><i>Possible</i>…</span></p>                                    <!-- dotted: join feasible, not shown -->
<p class="lk none"><span><i>Blocked</i>law / court / policy that stops it</span></p>    <!-- red cross -->
<section class="ly">…</section>
</div>
<p class="fig-src">Sources: [cite:key] [cite:key] …</p>
</figure>
```

The worked example is in `book/part1/de28/de28_the_ecosystem_map.html` (the first `fig-arch`). Read it before you start.

- Layers run from top to bottom in the direction the data flows: collection, then identity resolution or lookup, then storage or integration, then analytics or scoring, then decision or action. Use 3–6 layers, 2–6 nodes per layer, and keep node text short. `<code>` is where engineers get their detail: field names, identifiers (SSN, A-number, MAID/IDFA/GAID, IMEI/IMSI, VIN or plate, face template, NCIC record), protocols (RTB bidstream, API, STIX, batch file), standards (EBTS/ANSI-NIST), retention periods, contract numbers and values.
- **Every link label carries a grade.** Use the book's own grades exactly: Documented / Reported / Possible (only for a join between systems, never for a fact about a person) / Blocked. Write "Probable" inside the span text where the part already uses it, with class `lk rep`. A link's grade must match how the part's prose and its "worst-case reading, tested" section grade it. If the diagram makes a link look stronger than the text does, that is a failure.
- No new claims beyond what is sourced. Every fact in a diagram must be in the part's prose or in its research file (`book/research/<part>.json`) with a source key.
  - You **may** add technical depth that makes the diagram better, but only from primary or strong technical sources: DHS/DOJ Privacy Impact Assessments (PIAs) and SORNs, which document data flows, fields and retention; contract records (USAspending, SAM.gov, FPDS); vendor technical documentation; GAO/OIG reports; court filings; and major outlets.
  - To add a source, pipe JSON to `python3 book/research/work/addmany.py` (format: `{"stage":"<part>","entry":"<entry id>","topic":"…","sources":{"<part>_arch_x":{"url":…,"label":…}},"claims":[["claim text","documented|reported",["<part>_arch_x"]]]}`; look at an existing entry in `book/research/work/<part>.work.json` for the exact shape). Then run `python3 book/research/work/finalize.py <part> darkenlight`.
  - Prefix new keys `<part>_arch_`. Verify every URL resolves and actually says what you claim (use WebFetch). If you can't verify a detail, leave it out.
- Put every source key used in the figure in its `fig-src` line.
- Placement: put each diagram right after the paragraph(s) that describe that system, not in a pile at the end. Add one or two plain sentences of prose before or after if needed, in the book's register, so the figure is introduced. No "as the diagram shows" filler.
- Number of diagrams: 2–4 per part, wherever a real system is described. Don't diagram something that is just a list of facts. Where it fits, one diagram per part can be a matching-keys table: a `fig-compare` table with `data-kind="Join keys"` on the `<figure>`, rows as systems, columns as identifiers, cells `class="yes"` where a source documents the system holding that identifier.
- Rules from the library: no mention of research methods, Claude/AI or QOP; the same standard for every party and administration; no conspiracy-coded language ("shadowy", "secret cabal"). This is engineering diagramming in a sober register.
- Don't change existing prose claims or grades. Only add figures and minimal linking sentences.

## Check when done

```
S=/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad
cd /home/claude/israel && bash $S/build.sh > $S/arch_build_$PART.log 2>&1; echo $?
python3 $S/val.py $S/index.before.html de      # must print "all ok"
NODE_PATH=$(npm root -g) node $S/dvtest/arch.js <section_id> $S/dvtest   # renders each fig-arch on phone + desktop; overflow must be false, errs []
```

Look at the phone screenshots (`$S/dvtest/arch_<section>_<i>_p.png`) with the Read tool. Run the build only for your own parts; other agents are building in parallel, so if the build fails because of another file, re-run once.

**Do not git commit**; the coordinator commits. Report back with: each figure added (file, caption, layer count), any new source keys with URLs, and any grade judgement calls you made.
