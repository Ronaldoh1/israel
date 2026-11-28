#!/usr/bin/env python3
"""Make the network maps open fast, on phones above all (27 Nov 2026).

On each map page (road-network.html, epstein-network.html, de-network.html):
1. d3 is served from this site (vendor/d3-7.8.5.min.js) instead of a third-party CDN, so a phone makes no extra
   connection before the map can start.
2. The first view no longer computes its layout in the browser. tools/build_map_layouts.py lays each default view out
   once, at build time, and stores the positions in the page (window.MAP_LAYOUT, keyed by a hash of exactly which nodes
   and ties are shown). When the view being drawn matches a stored one, the nodes are placed and the physics is skipped;
   any other view (another start node, depth or filter) lays itself out as before.
3. On touch screens the settling animation after a change stops after 3 seconds instead of 8.
4. The Road to 1948 map opens on "Up to 1948"; readers can switch to Both or After 1948.
Idempotent. Usage: python3 tools/patch_map_speed.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['road-network.html', 'epstein-network.html', 'de-network.html']
CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>'
LOCAL = '<script src="vendor/d3-7.8.5.min.js"></script>'
HASH = ("/* a short, stable fingerprint of the nodes and ties in a view; stored layouts are keyed by it (tools/build_map_layouts.py) */\n"
        "function mapHash(s){ let h=2166136261>>>0; for(let i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } return h.toString(36)+'_'+s.length.toString(36); }\n")
for name in PAGES:
    p = os.path.join(ROOT, name)
    s = open(p, encoding='utf-8').read(); s0 = s
    # 1. d3 from this site
    if CDN in s: s = s.replace(CDN, LOCAL)
    s = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/d3/7\.8\.5/d3\.min\.js"[^>]*></script>', LOCAL, s)
    # the stored layouts sit right after d3, before the map's own code
    if 'id="map-layout"' not in s:
        s = s.replace(LOCAL, LOCAL + '\n<script id="map-layout">window.MAP_LAYOUT={};</script>', 1)
    # 2. place stored layouts and skip the physics
    if 'function mapHash(' not in s:
        assert s.count('function draw(soft){') == 1, name
        s = s.replace('function draw(soft){', HASH + 'function draw(soft){', 1)
    if 'window.__mapSig' not in s:
        a = "  const sig=ids.join('|')+'#'+links.map(l=>l.i).join(',');\n"
        assert s.count(a) == 1, name + ' sig'
        s = s.replace(a, a + "  const _lh=mapHash(sig), _lay=(window.MAP_LAYOUT||{})[_lh]; window.__mapSig=_lh;\n"
                             "  const _pre=!!_lay&&needFit&&nodes.every(n=>_lay[n.id]);   /* a view laid out at build time: place it, no physics */\n"
                             "  if(_pre) nodes.forEach(n=>{ const q=_lay[n.id]; n.x=W/2+q[0]; n.y=H/2+q[1]; n.vx=0; n.vy=0; });\n", 1)
        b = re.search(r"  if\(needFit\|\|reduce\)\{ for\(let k=0;k<", s)
        assert b, name + ' ticks'
        s = s[:b.start()] + "  if(_pre){ sim.alpha(0); sim.stop(); paint(); }\n  else " + s[b.start() + 2:]
    # 3. shorter settling on touch screens
    s = s.replace("  simDeadline=Date.now()+8000;", "  simDeadline=Date.now()+(matchMedia('(pointer:coarse)').matches?3000:8000);")
    # 5. the loop search (a full search of every verified cycle) runs after the map is on screen, not before
    a = "  const L=findLoops();\n"
    if a in s:
        s = s.replace(a, "  const _lk=$('root').value+'|'+E.length; let L=(_lc&&_lc.k===_lk)?_lc.v:null, _lp=!L;\n"
                         "  if(_lp){ L=[]; (window.requestIdleCallback||setTimeout)(()=>{ findLoops(); if($('side').querySelector('.loops-pending')) intro(); }, {timeout:1500}); }\n", 1)
        b = '<div class="sec">${L.length} loops in verified ties (start node left out)</div>'
        assert s.count(b) == 1, name + ' loops header'
        s = s.replace(b, '<div class="sec${_lp?\' loops-pending\':\'\'}">${_lp?\'Finding loops in verified ties…\':L.length+\' loops in verified ties (start node left out)\'}</div>', 1)
    # 6. the record panel's header follows its content once per frame, not once per change (each change forced a full layout)
    a = "new MutationObserver(()=>{ const s=$('side'); const k=s.querySelector('.kind'), h=s.querySelector('h2');\n  $('gk').textContent=k?k.textContent:'Record'; $('gt').textContent=h?h.textContent:'Tap a node to read its record'; s.scrollTop=0; })"
    if a in s:
        s = s.replace(a, "let _moF=0; new MutationObserver(()=>{ if(_moF) return; _moF=requestAnimationFrame(()=>{ _moF=0; const s=$('side'); const k=s.querySelector('.kind'), h=s.querySelector('h2');\n  $('gk').textContent=k?k.textContent:'Record'; $('gt').textContent=h?h.textContent:'Tap a node to read its record'; s.scrollTop=0; }); })", 1)
    # 7. the loop list shows its first 60 entries, with a button for the rest (thousands of entries were laid out on every open)
    a = "  L.forEach((l,j)=>{ h+=`<li data-l=\"${j}\" tabindex=\"0\">${l.c.map(x=>esc(N.get(x).name)).join(' → ')}</li>`; });\n"
    if a in s:
        s = s.replace(a, "  const _cap=window._allLoops?L.length:60;\n"
                         "  L.slice(0,_cap).forEach((l,j)=>{ h+=`<li data-l=\"${j}\" tabindex=\"0\">${l.c.map(x=>esc(N.get(x).name)).join(' → ')}</li>`; });\n"
                         "  if(L.length>_cap) h+=`<li class=\"loops-more\" role=\"button\" tabindex=\"0\" style=\"list-style:none;font-weight:600;cursor:pointer\">Show all ${L.length} loops</li>`;\n", 1)
        b = "  $('side').querySelectorAll('[data-l]').forEach(el=>{"
        assert s.count(b) == 1, name + ' loop handlers'
        s = s.replace(b, "  { const mb=$('side').querySelector('.loops-more'); if(mb){ const more=()=>{ window._allLoops=true; intro(); }; mb.onclick=more; mb.onkeydown=ev=>{ if(ev.key==='Enter') more(); }; } }\n" + b, 1)
    # 4. the Road map opens on the years up to 1948
    if name == 'road-network.html':
        s = s.replace("let ERA='both', AFTER_NB=new Set();", "let ERA='before', AFTER_NB=new Set();")
        s = s.replace('<button type="button" data-era="before">Up to 1948</button><button type="button" data-era="both" class="on">Both</button>',
                      '<button type="button" data-era="before" class="on">Up to 1948</button><button type="button" data-era="both">Both</button>')
        assert "let ERA='before'" in s and 'data-era="before" class="on"' in s
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s); print(name, 'patched')
    else:
        print(name, 'already patched')
