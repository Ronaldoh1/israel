/* OTSGeo: a small map renderer shared by the simulation's dashboards and the library's figures.
   The basemap (window.OTS_GEO, from tools/geo_base.json) is one equirectangular drawing of Europe, Africa and Asia;
   each panel crops it with its own viewBox, so a regional view costs nothing extra.
   Panel data: {type:'geomap', view:[lon0, lon1, lat0, lat1], families:{id:[label, colour]},
                points:[{id, n, name, family, lat, lon, place, lang, since, today}], routes:[{from, to, label, family}], note}
   Badges that would overlap are pushed apart, with a thin leader line back to the true place. */
(function(){
  'use strict';
  var UID = 0;
  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function render(s){
    var G = window.OTS_GEO; if(!G) return '';
    var v = s.view || [G.lon0, G.lon0 + G.W / G.k, G.lat1 - G.H / G.k, G.lat1];
    var x0 = (v[0] - G.lon0) * G.k, x1 = (v[1] - G.lon0) * G.k, y0 = (G.lat1 - v[3]) * G.k, y1 = (G.lat1 - v[2]) * G.k, W = x1 - x0, H = y1 - y0;
    var u = W / 360, r = 10.5 * u, id = 'geo' + (++UID), F = s.families || {};
    function P(p){ return [(p.lon - G.lon0) * G.k, (G.lat1 - p.lat) * G.k]; }
    function col(f){ return (F[f] || [f, '#5A6170'])[1]; }
    var byId = {}; (s.points || []).forEach(function(p){ byId[p.id] = p; });
    var dests = (s.points || []).filter(function(p){ return p.dest && p.lon >= v[0] - 1 && p.lon <= v[1] + 1 && p.lat >= v[2] && p.lat <= v[3]; });
    var inView = (s.points || []).filter(function(p){ return p.n && p.lon >= v[0] && p.lon <= v[1] && p.lat >= v[2] && p.lat <= v[3]; });
    /* badge positions: start at the place, push overlapping badges apart */
    var B = inView.map(function(p){ var q = P(p); return {p:p, x:q[0], y:q[1], ox:q[0], oy:q[1]}; });
    for(var it = 0; it < 160; it++){ var moved = false;
      for(var i = 0; i < B.length; i++) for(var j = i + 1; j < B.length; j++){
        var a = B[i], b = B[j], dx = b.x - a.x, dy = b.y - a.y, d = Math.sqrt(dx * dx + dy * dy), need = 2 * r + 2 * u;
        if(d < need){ moved = true; if(d < 0.01){ dx = 1; dy = 0.3; d = 1.04; } var m = (need - d) / 2 / d; a.x -= dx * m; a.y -= dy * m; b.x += dx * m; b.y += dy * m; } }
      B.forEach(function(q){ q.x = Math.max(x0 + r + u, Math.min(x1 - r - u, q.x)); q.y = Math.max(y0 + r + u, Math.min(y1 - r - u, q.y)); });
      if(!moved) break; }
    var o = '<svg class="geo-svg" viewBox="' + x0.toFixed(1) + ' ' + y0.toFixed(1) + ' ' + W.toFixed(1) + ' ' + H.toFixed(1) + '" role="img" aria-label="' + esc(s.title || 'Map') + '">';
    o += '<rect x="' + x0 + '" y="' + y0 + '" width="' + W + '" height="' + H + '" class="geo-sea"/>';
    o += '<path class="geo-land" d="' + G.land + '" style="stroke-width:' + (0.8 * u).toFixed(2) + '"/><path class="geo-bord" d="' + G.borders + '" style="stroke-width:' + (0.6 * u).toFixed(2) + '"/>';
    /* routes: a curved arrow from one place to another, in the colour of the family that moved */
    (s.routes || []).forEach(function(rt){ var A = byId[rt.from], Z = byId[rt.to]; if(!A || !Z) return;
      var a = P(A), z = P(Z), mx = (a[0] + z[0]) / 2, my = (a[1] + z[1]) / 2, dx = z[0] - a[0], dy = z[1] - a[1], L = Math.sqrt(dx * dx + dy * dy) || 1;
      var cx = mx - dy / L * L * 0.18, cy = my + dx / L * L * 0.18, c = col(rt.family || A.family);
      var ex = z[0] - (z[0] - cx) / Math.sqrt(Math.pow(z[0] - cx, 2) + Math.pow(z[1] - cy, 2)) * r * 1.05, ey = z[1] - (z[1] - cy) / Math.sqrt(Math.pow(z[0] - cx, 2) + Math.pow(z[1] - cy, 2)) * r * 1.05;
      var ang = Math.atan2(ey - cy, ex - cx), h = 7 * u;
      o += '<path d="M' + a[0].toFixed(1) + ' ' + a[1].toFixed(1) + ' Q' + cx.toFixed(1) + ' ' + cy.toFixed(1) + ' ' + ex.toFixed(1) + ' ' + ey.toFixed(1) + '" fill="none" stroke="' + c + '" stroke-width="' + (2.4 * u).toFixed(2) + '" stroke-dasharray="' + (6 * u).toFixed(1) + ' ' + (3.5 * u).toFixed(1) + '" opacity=".9"/>';
      o += '<path d="M' + ex.toFixed(1) + ' ' + ey.toFixed(1) + ' L' + (ex - h * Math.cos(ang - 0.45)).toFixed(1) + ' ' + (ey - h * Math.sin(ang - 0.45)).toFixed(1) + ' L' + (ex - h * Math.cos(ang + 0.45)).toFixed(1) + ' ' + (ey - h * Math.sin(ang + 0.45)).toFixed(1) + 'Z" fill="' + c + '"/>'; });
    dests.forEach(function(p){ var q = P(p), d = 4.2 * u, right = p.side ? p.side !== 'left' : q[0] < x1 - 70 * u, tx = right ? q[0] + 7 * u : q[0] - 7 * u;
      o += '<path d="M' + q[0].toFixed(1) + ' ' + (q[1] - d).toFixed(1) + ' l' + d.toFixed(1) + ' ' + d.toFixed(1) + ' l' + (-d).toFixed(1) + ' ' + d.toFixed(1) + ' l' + (-d).toFixed(1) + ' ' + (-d).toFixed(1) + 'Z" class="geo-dest"/>' +
        '<text x="' + tx.toFixed(1) + '" y="' + (q[1] + 3.6 * u).toFixed(1) + '" text-anchor="' + (right ? 'start' : 'end') + '" class="geo-dlab" style="font:italic 600 ' + (10.5 * u).toFixed(1) + 'px Georgia,serif;stroke-width:' + (3 * u).toFixed(1) + '">' + esc(p.name) + '</text>'; });
    B.forEach(function(q){ if(Math.abs(q.x - q.ox) + Math.abs(q.y - q.oy) > 2 * u) o += '<line x1="' + q.ox.toFixed(1) + '" y1="' + q.oy.toFixed(1) + '" x2="' + q.x.toFixed(1) + '" y2="' + q.y.toFixed(1) + '" class="geo-lead" style="stroke-width:' + (0.9 * u).toFixed(2) + '"/>';
      o += '<circle cx="' + q.ox.toFixed(1) + '" cy="' + q.oy.toFixed(1) + '" r="' + (2.2 * u).toFixed(1) + '" fill="' + col(q.p.family) + '"/>'; });
    B.forEach(function(q){ o += '<g class="geo-b" data-geo-n="' + q.p.n + '" data-geo-g="' + id + '" tabindex="0" role="button" aria-label="' + esc(q.p.n + '. ' + q.p.name) + '"><circle cx="' + q.x.toFixed(1) + '" cy="' + q.y.toFixed(1) + '" r="' + r.toFixed(1) + '" fill="' + col(q.p.family) + '" stroke="#fff" stroke-width="' + (1.6 * u).toFixed(2) + '"/>' +
      '<text x="' + q.x.toFixed(1) + '" y="' + (q.y + r * 0.38).toFixed(1) + '" text-anchor="middle" fill="#fff" style="font:700 ' + (r * 1.05).toFixed(1) + 'px system-ui,-apple-system,sans-serif">' + q.p.n + '</text></g>'; });
    o += '</svg>';
    var fams = Object.keys(F).filter(function(f){ return inView.some(function(p){ return p.family === f; }); });
    var leg = '<div class="geo-leg">' + fams.map(function(f){ return '<span><i style="background:' + col(f) + '"></i>' + esc(F[f][0]) + '</span>'; }).join('') + '</div>';
    var key = '<ol class="geo-key">' + inView.slice().sort(function(a, b){ return a.n - b.n; }).map(function(p){
      return '<li data-geo-k="' + p.n + '" data-geo-g="' + id + '"><span class="geo-n" style="background:' + col(p.family) + '">' + p.n + '</span><span><b>' + esc(p.name) + '</b>' + (p.place ? ' · ' + esc(p.place) : '') +
        '<small>' + [p.lang, p.since, p.today ? 'Today: ' + p.today : ''].filter(Boolean).map(esc).join(' · ') + '</small></span></li>'; }).join('') + '</ol>';
    var rts = (s.routes || []).filter(function(rt){ return byId[rt.from] && byId[rt.to]; });
    var rl = rts.length ? '<ul class="geo-routes">' + rts.map(function(rt){ return '<li><i style="border-color:' + col(rt.family || byId[rt.from].family) + '"></i>' + esc(rt.label) + '</li>'; }).join('') + '</ul>' : '';
    return '<div class="geo-wrap"><div class="geo-mapbox">' + o + '<div class="geo-tip" role="status" hidden></div></div>' + leg + rl + key + (s.note ? '<p class="geo-note">' + esc(s.note) + '</p>' : '') + '</div>';
  }
  /* tap a badge: show its entry over the map, and mark it in the key */
  document.addEventListener('click', function(e){
    var x = e.target.closest && e.target.closest('.geo-tip-x'); if(x){ var t0 = x.closest('.geo-tip'); t0.hidden = true; return; }
    var b = e.target.closest && e.target.closest('.geo-b'); if(!b) return;
    var wrap = b.closest('.geo-wrap'), li = wrap && wrap.querySelector('[data-geo-k="' + b.getAttribute('data-geo-n') + '"]'); if(!li) return;
    [].forEach.call(wrap.querySelectorAll('.geo-key li.hit'), function(z){ z.classList.remove('hit'); });
    li.classList.add('hit');
    var tip = wrap.querySelector('.geo-tip'); if(tip){ tip.innerHTML = '<button type="button" class="geo-tip-x" aria-label="Close">✕</button>' + li.innerHTML; tip.hidden = false; }
  });
  document.addEventListener('keydown', function(e){ if((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('geo-b')){ e.preventDefault(); e.target.dispatchEvent(new MouseEvent('click', {bubbles:true})); } });
  window.OTSGeo = {render:render};
})();
