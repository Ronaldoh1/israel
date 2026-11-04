# The Road to 1948 network map, v1 (4 Nov 2026)

**This is an INSTITUTION/SYSTEM-mixed network module.** It covers the people, organizations, states, documents and events of *The Baseline* (ch01) and *The Road to 1948* (rd0–rd6), 1694–1950s. It opens from both books' library cards and from the library menu (`road-network.html`).

## How it was built

1. **Nodes: a curated registry** (`book/plan/road_map/registry.py`), 293 entries.
   - Every entry is an actor, institution, document or event, with alias patterns. Some aliases only apply within one stage, for example "Feinberg" means Abraham Feinberg only from rd4 on, because in rd2 it is Avshalom Feinberg of NILI.
   - No ethnic or religious group is a node.
   - Historians and outlets cited as sources are not nodes.
2. **Candidate ties: the book text** (`build_road.py`).
   - The script splits all ~357,000 words into sentences, and each sentence keeps its own citations.
   - Figure and table cells take the figure's source line.
   - When a sentence names two nodes next to each other with a relationship verb between them (founded, funded, led, wrote to, met, signed, opposed, expelled…), that becomes a typed candidate tie.
   - The simulation scenes' authored connections are added as further candidates.
3. **Review: every typed candidate checked by hand against its sentence** (`review.json`).
   - 434 typed candidates plus the 150 most frequent name pairs were read.
   - Each was accepted, re-typed, reversed, re-pointed to the pair the sentence actually documents, or rejected.
   - Rejections included the Federal Reserve sentence that explicitly says there is *no* link to the Zionist Organization, the "Fourth Congress" that is the Palestine Arab Congress rather than the US Congress, and the "James de Rothschild" who is James Armand (PICA) rather than James Mayer.
4. **Curated layer** (`road_layer.json`): ties the heuristic could not phrase.
   - Weizmann, Sokolow and Sykes drafted the Balfour Declaration; Balfour signed it.
   - The Third Arab Congress created the Arab Executive.
   - The Justice Department ordered the American Zionist Council to register under FARA.
   - Ben-Gurion headed the provisional government.
5. **Per-node profile** (`qop_road.py`): the same stored fields as the Epstein map.
   - Kevin Bacon distance to the two anchors.
   - Bridging rank, with and without the anchors.
   - Role, money ties, short loops.
   - Other library volumes that name the node.
   - Book sections that name it.
   - The nodes it is named together with.

**Statuses**
- *verified*: a tie the book states, with the book's citation.
- *reported*: stated in the book with no citation in that paragraph; the source links to the section.
- *co-mention*: named together in one sentence with no stated tie. These are leads only, never walked or used in any measure.

## First-pass numbers

| | |
|---|---|
| Nodes | 291: 124 people, 71 institutions, 36 governments, 26 documents, 22 events, 12 companies |
| Reviewed ties | 283 (272 sourced, 11 uncited) |
| Named-together leads | 1,129 |
| Nodes with at least one reviewed tie | 203 |
| Short loops | 44 |
| Nodes named in other library volumes | 140 |

**Anchors** (the two most-bridging nodes, chosen by the data): the **Jewish Agency** and the **World Zionist Organization**.

**Top bridges**
- With the anchors: Jewish Agency, WZO, Weizmann, Herzl, UN, Truman, Ben-Gurion, Balfour Declaration, Irgun, the Mandate.
- With the anchors removed: Herzl, the Balfour Declaration, Ben-Gurion, the UN, Truman, Weizmann, the Irgun, Judah Magnes.
- So the map holds together through the movement's two bodies, then through three documents and decisions (Balfour, the Mandate, Resolution 181 via the UN) and a handful of individuals.

## Known gaps (next pass)

- **Money is thin.** Only about 11 funding ties were stated plainly enough for the first pass. The book's money chapters (JCT, JNF, Keren Hayesod, Haavara, Sonneborn and Feinberg, the Export-Import loan) are mostly still in the named-together queue.
- **Arab and Palestinian institutions, the Ottoman side and the British administration** have fewer reviewed ties than the Zionist and American side. The cause is the heuristic, not the book: those chapters use more narrative phrasing. A review pass over those clusters should come next, so the map is not lopsided.
- **The Baseline** is mostly concepts, words and traditions, so it contributes fewer actor ties. Its dissent institutions (Bund, Reform, Neturei Karta, Satmar, Agudah) are on the map.
- **Next step:** review the remaining named-together pairs cluster by cluster and promote the real ties.
