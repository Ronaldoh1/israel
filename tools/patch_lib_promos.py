#!/usr/bin/env python3
"""Two dismissible banners at the top of the library (index.html): the two network maps, and the Esoteric Guardian
videos on the Epstein shelf. Dismissing hides a banner until the page is loaded again (kept in memory only), so they
show on every visit. The map tiles use the library's own data-epmap handler (same window). Idempotent.
Usage: python3 tools/patch_lib_promos.py [index.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if 'lb-promos' in s:
    print('already patched'); sys.exit()

CSS = r'''
.lb-promos{display:grid;gap:14px;max-width:980px;margin:6px auto 22px}
.lb-promo{position:relative;border-radius:16px;padding:20px 20px 18px;color:#F4EFE3;background:radial-gradient(120% 140% at 100% 0%,#1E2A5C 0%,#0B1026 62%);border:1px solid rgba(232,180,74,.55);box-shadow:0 14px 36px rgba(11,16,38,.28),inset 0 1px 0 rgba(255,255,255,.06);font-family:var(--serif,'EB Garamond',Georgia,serif);overflow:hidden}
.lb-promo.vid{background:radial-gradient(120% 160% at 0% 0%,#3A1020 0%,#14091A 58%,#0B1026 100%);border-color:rgba(215,38,61,.6)}
.lb-promo .px{position:absolute;z-index:3;top:8px;right:8px;width:36px;height:36px;border:0;border-radius:50%;background:rgba(255,255,255,.08);color:#F4EFE3;font-size:20px;line-height:1;cursor:pointer;display:grid;place-items:center}
.lb-promo .px:hover{background:rgba(255,255,255,.18)}
.lb-promo .px:focus-visible,.lb-promo .pm:focus-visible,.lb-promo .pv:focus-visible{outline:2px solid #E8B44A;outline-offset:2px}
.lb-promo .pk{font-size:14px;font-style:italic;color:#E8B44A;margin:0 44px 4px 0}
.lb-promo h3{font-size:clamp(22px,3.4vw,30px);line-height:1.12;margin:0 44px 14px 0;font-weight:700;color:#FFF}
.lb-promo .maps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.lb-promo .pm{display:flex;gap:12px;align-items:center;text-align:left;width:100%;padding:12px;border-radius:12px;border:1px solid rgba(232,180,74,.35);background:rgba(255,255,255,.04);color:inherit;font:inherit;cursor:pointer}
.lb-promo .pm:hover{background:rgba(232,180,74,.10);border-color:#E8B44A}
.lb-promo .pm svg{flex:none;width:52px;height:52px}
.lb-promo .pm b{display:block;font-size:18px;line-height:1.2;color:#FFF}
.lb-promo .pm small{display:block;font-family:var(--sans,system-ui,sans-serif);font-size:13px;line-height:1.4;color:#D9D2C2;margin-top:3px}
.lb-promo .pm .go{display:inline-block;margin-top:6px;font-family:var(--sans,system-ui,sans-serif);font-size:13px;font-weight:700;color:#E8B44A}
.lb-promo .vrow{display:flex;gap:16px;align-items:center}
.lb-promo .vthumb{flex:none;width:168px;aspect-ratio:16/9;border-radius:10px;overflow:hidden;position:relative;background:#000;border:1px solid rgba(215,38,61,.5)}
.lb-promo .vthumb img{width:100%;height:100%;object-fit:cover;display:block;opacity:.88}
.lb-promo .vthumb span{position:absolute;inset:0;display:grid;place-items:center}
.lb-promo .vtx{min-width:0}
.lb-promo .vtx p{font-family:var(--sans,system-ui,sans-serif);font-size:14px;line-height:1.45;color:#D9D2C2;margin:0 0 12px}
.lb-promo .pv{display:inline-flex;align-items:center;min-height:42px;padding:9px 18px;border-radius:999px;border:0;background:#D7263D;color:#FFF;font-family:var(--sans,system-ui,sans-serif);font-size:14px;font-weight:700;cursor:pointer}
.lb-promo .pv:hover{filter:brightness(1.1)}
.lb-flash{animation:lbFlash 1.6s ease-out 1}
@keyframes lbFlash{0%{box-shadow:0 0 0 0 rgba(215,38,61,.9)}100%{box-shadow:0 0 0 18px rgba(215,38,61,0)}}
@media (max-width:640px){.lb-promo{padding:16px 14px 14px}.lb-promo .maps{grid-template-columns:1fr}.lb-promo .vrow{flex-direction:column;align-items:stretch}.lb-promo .vthumb{width:100%}}
@media (prefers-reduced-motion:reduce){.lb-flash{animation:none}}
'''
anchor = '.lb-hd p{'
i = s.index(anchor); j = s.index('\n', i)
s = s[:j + 1] + CSS.strip() + '\n' + s[j + 1:]

NET = ('<svg viewBox="0 0 52 52" aria-hidden="true"><g stroke="#E8B44A" stroke-width="1.4" fill="none" opacity=".75">'
       '<path d="M26 26L10 12M26 26L42 10M26 26L44 34M26 26L14 42M26 26L30 46M10 12L42 10M44 34L30 46"/></g>'
       '<g fill="#E8B44A"><circle cx="26" cy="26" r="5"/><circle cx="10" cy="12" r="3"/><circle cx="42" cy="10" r="3"/>'
       '<circle cx="44" cy="34" r="3"/><circle cx="14" cy="42" r="3"/><circle cx="30" cy="46" r="3"/></g>%s</svg>')
NET_EP = NET % '<circle cx="26" cy="26" r="9" fill="none" stroke="#D7263D" stroke-width="1.6"/>'
NET_IS = NET % '<circle cx="26" cy="26" r="9" fill="none" stroke="#F4EFE3" stroke-width="1.2" stroke-dasharray="2 2"/>'
JS = r'''
  /* ---------- banners at the top of the library: dismissed ones stay hidden until the page is loaded again ---------- */
  var PROMO_X = {};
  function promos(){
    var h = '';
    if(!PROMO_X.maps) h += '<section class="lb-promo" data-promo="maps" aria-label="The network maps"><button class="px" type="button" data-promo-x="maps" aria-label="Dismiss this banner">×</button>' +
      '<p class="pk">Interactive, every tie with its source</p><h3>Explore the network maps</h3><div class="maps">' +
      '<button class="pm" type="button" data-epmap="epstein">NET_EP<span><b>The Epstein Network Map</b><small>Who built, paid for and protected the operation, and what happens when any part is taken away.</small><span class="go">Open the map</span></span></button>' +
      '<button class="pm" type="button" data-epmap="road1948">NET_IS<span><b>The Israel Network Map</b><small>The Road to 1948 and After: founders, funds, states and documents from 1694 to 1967.</small><span class="go">Open the map</span></span></button>' +
      '</div></section>';
    if(!PROMO_X.vids) h += '<section class="lb-promo vid" data-promo="vids" aria-label="Videos by Esoteric Guardian"><button class="px" type="button" data-promo-x="vids" aria-label="Dismiss this banner">×</button>' +
      '<div class="vrow"><div class="vthumb" aria-hidden="true"><img src="https://img.youtube.com/vi/6MgmsmTqA0M/hqdefault.jpg" alt="" loading="lazy" onerror="this.remove()"><span><svg width="46" height="46" viewBox="0 0 64 64"><circle cx="32" cy="32" r="29" fill="rgba(11,16,38,.55)" stroke="#F5D88E" stroke-width="2.2"/><path d="M26 20.5L45.5 32L26 43.5Z" fill="#F5D88E"/></svg></span></div>' +
      '<div class="vtx"><p class="pk">Videos by Esoteric Guardian</p><h3>Epstein Network: The Occult Infrastructure</h3><p>Six videos on the symbolism and esoteric readings around the Epstein network, on the Epstein shelf of this library. Outside videos: each is the creator\'s own view.</p>' +
      '<button class="pv" type="button" data-promo-vid="1">See the videos</button></div></div></section>';
    return h ? '<div class="lb-promos" id="lbPromos">' + h + '</div>' : '';
  }
'''.replace('NET_EP', NET_EP).replace('NET_IS', NET_IS)
anchor = '  function toLibrary(){'
s = s.replace(anchor, JS.rstrip('\n') + '\n' + anchor, 1)

old = "lib.innerHTML = '<div class=\"lb-wrap\"><div class=\"lb-top\">"
i = s.index(old)
k = s.index("'<div class=\"lb-hd\">", i)
s = s[:k] + "promos() + " + s[k:]

old = "  lib.addEventListener('click', function(e){"
new = old + '''
    var px = e.target.closest('[data-promo-x]'); if(px){ var id = px.getAttribute('data-promo-x'); PROMO_X[id] = 1; var el = px.closest('.lb-promo'), box = el && el.parentNode; if(el) el.remove(); if(box && !box.children.length) box.remove(); return; }
    if(e.target.closest('[data-promo-vid]')){ var v = lib.querySelector('.lb-ep .lb-vid'); if(!v){ libQ = ''; var q = $('lbQ'); if(q) q.value = ''; renderLib(); v = lib.querySelector('.lb-ep .lb-vid'); }
      if(v){ v.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block:'center'}); v.classList.remove('lb-flash'); void v.offsetWidth; v.classList.add('lb-flash'); setTimeout(function(){ try{ v.focus({preventScroll:true}); }catch(err){} }, 600); } return; }'''
assert old in s
s = s.replace(old, new, 1)
open(P, 'w', encoding='utf-8').write(s)
print('library banners added')
