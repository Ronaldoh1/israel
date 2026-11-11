# Epstein network map: data and vault

- `build_data.py`: the source of truth. Every node and edge, with status (`verified` / `to-verify` / `not-established`) and a source. Edit here.
- `network.json`: written by `build_data.py`. It feeds the vault and, later, the library's clickable map (Appendix A of *The Epstein Architecture*).
- `make_vault.py OUTDIR`: builds the Obsidian vault (notes, `Network.canvas`, graph colours, Loops, To Verify, clusters).

Rebuild: `python3 build_data.py && python3 make_vault.py <outdir>`

Rules encoded in the data:
- Family members get separate nodes linked by a kinship edge.
- The Israel node carries state acts only.
- Intelligence claims appear only as `not-established` edges.
- Investigation, testimony and litigation edges are excluded from loop detection.
