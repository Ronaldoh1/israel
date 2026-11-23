/* The Library of Truth: static site + reach counter.
   Static files are served from ./public. Two small endpoints keep counts in a D1 table:
     POST /api/hit   {"k":"site"} or {"k":"b:<book id>"}  -> adds one
     GET  /api/stats                                       -> {base, site, books:{id:n}, since}
   The browser sends at most one hit per key per day; nothing personal is stored. */
const BASE = 10000;            // starting figure for reach before the counter began (set by the site owner)
const SINCE = '2026-11-23';    // the day counting began
const KEY = /^(site|b:[a-z0-9_\-]{1,60})$/;
let ready = false;

async function init(db) {
  if (ready) return;
  await db.exec('CREATE TABLE IF NOT EXISTS counts (k TEXT PRIMARY KEY, n INTEGER NOT NULL DEFAULT 0)');
  ready = true;
}
function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...extra } });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === '/api/hit') {
      if (req.method !== 'POST') return json({ ok: false }, 405);
      let k = null;
      try { k = (await req.json()).k; } catch (e) {}
      if (typeof k !== 'string' || !KEY.test(k)) return json({ ok: false }, 400);
      await init(env.DB);
      await env.DB.prepare('INSERT INTO counts (k, n) VALUES (?, 1) ON CONFLICT(k) DO UPDATE SET n = n + 1').bind(k).run();
      return json({ ok: true }, 200, { 'Cache-Control': 'no-store' });
    }
    if (url.pathname === '/api/stats') {
      await init(env.DB);
      const { results } = await env.DB.prepare('SELECT k, n FROM counts').all();
      let site = 0; const books = {};
      for (const r of results || []) { if (r.k === 'site') site = r.n; else if (r.k.startsWith('b:')) books[r.k.slice(2)] = r.n; }
      return json({ base: BASE, site, books, since: SINCE }, 200, { 'Cache-Control': 'public, max-age=60' });
    }
    return env.ASSETS.fetch(req);
  },
};
