# israel

| File | What it is |
|---|---|
| `index.html` | **The Israel Architecture Simulation**: the standalone file. This is the one to edit. |
| `sophia.html` | Sophia, the hub of all modules. It carries an **embedded copy** of `index.html` (`<script id="il_sim_b64">`) so it works as a single file. |
| `tools/embed_israel.py` | Re-embeds `index.html` into `sophia.html`. |

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
