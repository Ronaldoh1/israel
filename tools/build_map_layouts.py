#!/usr/bin/env python3
"""Lay out each network map's opening views once, at build time, and store the positions in the page (27 Nov 2026).

For every map page it opens the page in a headless browser, at a desktop size and a phone size, lets the layout
settle fully, and records each node's position relative to the centre, keyed by a fingerprint of the exact nodes and
ties on screen (see tools/patch_map_speed.py). The Road to 1948 map is laid out for each of its three year settings.
A phone opening the map then places the nodes directly instead of computing the layout.

Run after any change to a map's data (the stored layouts of a changed view simply stop matching, and that view falls
back to laying itself out), and before tools/build_israel_web.py. Usage: python3 tools/build_map_layouts.py [page ...]"""
import asyncio, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = sys.argv[1:] or ['road-network.html', 'epstein-network.html', 'de-network.html']
D3 = open(os.path.join(ROOT, 'tools', 'vendor', 'd3-7.8.5.min.js'), 'rb').read()
VIEWS = {'road-network.html': ['before', 'both', 'after']}
RX = re.compile(r'<script id="map-layout">window\.MAP_LAYOUT=.*?;</script>', re.S)

CAPTURE = r"""
(era) => {
  if (era && typeof setEra === 'function') setEra(era);
  sim.stop(); for (let k = 0; k < 600; k++) sim.tick();
  const W = svg.node().clientWidth || 600, H = svg.node().clientHeight || 600, out = {};
  live.forEach((n, id) => { if (isFinite(n.x) && isFinite(n.y)) out[id] = [Math.round((n.x - W / 2) * 10) / 10, Math.round((n.y - H / 2) * 10) / 10]; });
  return {sig: window.__mapSig, pos: out, n: live.size};
}
"""

async def layouts(p, name, html):
    stripped = RX.sub('<script id="map-layout">window.MAP_LAYOUT={};</script>', html)
    found = {}
    for vp in ({'viewport': {'width': 1280, 'height': 800}}, dict(p.devices['iPhone 13'])):
        vp.pop('default_browser_type', None)
        br = await p.chromium.launch(); ctx = await br.new_context(**vp)
        async def route(r):
            u = r.request.url
            if u.endswith('/' + name) or u.endswith('/' + name + '?'): return await r.fulfill(status=200, content_type='text/html', body=stripped)
            if 'd3-7.8.5.min.js' in u: return await r.fulfill(status=200, content_type='application/javascript', body=D3)
            return await r.abort()
        await ctx.route('**/*', route)
        for era in VIEWS.get(name, [None]):
            pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('http://maps.local/' + name, wait_until='load')
            await pg.wait_for_function('typeof sim !== "undefined" && sim && window.__mapSig', timeout=120000)
            r = await pg.evaluate(CAPTURE, era)
            assert not errs, errs
            found[r['sig']] = r['pos']
            print('  %-22s %-7s %-10s %4d nodes  key %s' % (name, era or '-', 'phone' if vp.get('is_mobile') else 'desktop', r['n'], r['sig']))
            await pg.close()
        await br.close()
    return found

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        for name in PAGES:
            path = os.path.join(ROOT, name)
            html = open(path, encoding='utf-8').read()
            assert 'id="map-layout"' in html, name + ': run tools/patch_map_speed.py first'
            L = await layouts(p, name, html)
            blob = json.dumps(L, separators=(',', ':'))
            html = RX.sub(lambda m: '<script id="map-layout">window.MAP_LAYOUT=' + blob + ';</script>', html, count=1)
            open(path, 'w', encoding='utf-8').write(html)
            print('%s: %d stored views, %d KB' % (name, len(L), len(blob) // 1024))

asyncio.run(main())
