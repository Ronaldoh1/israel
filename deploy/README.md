# Deploy bundle

Every bundle = `dist/israel-web` copied to `public/`, plus this folder's `wrangler.jsonc` and `src/worker.js`
(from v129 on; earlier bundles used an assets-only wrangler.jsonc).

The worker serves the static site and the reach counter:
- `POST /api/hit` with `{"k":"site"}` or `{"k":"b:<book id>"}` adds one (the browser sends at most one per key per day).
- `GET /api/stats` returns `{base, site, books, since}`; the library shows `base + site` as "people reached"
  and each book's count as "N readers".
- Counts live in a Cloudflare D1 database bound as `DB` (`israel-stats`). Wrangler (4.45+) creates it on the
  first deploy; no database id is needed in the config. The table is created by the worker on first use.
- `BASE = 10000` is a starting figure set by the site owner on 2026-11-23 for reach before counting began
  (video views were over 300,000); book counts start at zero.
