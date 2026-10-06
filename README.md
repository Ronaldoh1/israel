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
