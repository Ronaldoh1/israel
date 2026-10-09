# israel

| File | What it is |
|---|---|
| `index.html` | **The Israel Architecture Simulation**: the standalone file. This is the one to edit. |
| `sophia.html` | Sophia, the hub of all modules. It carries an **embedded copy** of `index.html` (`<script id="il_sim_b64">`) so it works as a single file. |
| `tools/embed_israel.py` | Re-embeds `index.html` into `sophia.html`. |
| `elections-2026.html` | **2026 Elections** module (Collapse pillar), standalone. Also embedded in `sophia.html` (`<script id="el26_sim_b64">`). |
| `elections/` | Source for the elections module: `app.html` template, `gen_data.py` → `merge_research.py` → `build.py`, research dossiers in `elections/research/`, and `sophia_patch.py` (re-embeds the module and the Israel simulation into Sophia). |

## After every change to `index.html`

```sh
python3 tools/embed_israel.py          # copy the current index.html into sophia.html
python3 tools/embed_israel.py --check  # verify: exits 1 if sophia.html is out of date
```

Commit `index.html` and `sophia.html` together.

## Sophia pillar cards (Observe, Collapse, Reignite)

Root cards compute their figures from their children when the page loads (`propagateLiveTotals()` in `sophia.html`):

- **Entities mapped**: the sum over every *live* child module (a `NAV_ROOTS` / `NAV_TREE` leaf with `sim` and no `soon`, or an enabled sub-archive entry), read from the child's `"N entities"` (or `"N scenes"`) description.
- **Footer**: `N live modules · M coming`.
- **Description**: a root card's `desc` can embed `{modules}`, `{scenes}`, `{entities}` and `{deepdives}`, which are filled from the children, e.g. `'{modules} live — {scenes} and {entities} between them.'`

Adding or updating a child module (its `sim`, `soon` flag or the counts in its `desc`) updates its root card automatically. Avoid typing child totals into a root card's description; use the tokens instead.

## 2026 Elections module

Build (scripts expect the folder at `/home/claude/el26`; copy or symlink it there):

```sh
python3 gen_data.py && python3 merge_research.py && python3 build.py   # -> elections-2026.html
python3 sophia_patch.py sophia.html elections-2026.html index.html     # embed into Sophia
```

States marked complete are listed in `COMPLETE_STATES` in `merge_research.py` (currently Alabama and Alaska). Overall 1–5 scores show as **Pending** until every record behind them has been searched.
