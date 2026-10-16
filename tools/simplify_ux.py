#!/usr/bin/env python3
"""Simpler controls and a lighter first visit for the Israel simulation (index.html).

First visit, before: welcome -> Simulation/Library chooser -> Eleven Minutes (full screen) -> 7-step tour
-> swipe tip -> "read it as a book?" banner. Library visitors also got a 6-step library tour.
After: welcome -> chooser -> one small "How to read this" card (three lines, one button).
Eleven Minutes, the full tour and the library tour are still one tap away in the + menu
(and #11minutes links still open Eleven Minutes directly).

Controls, before: Search / Key / Sources / Guide in the header, a floating ? button, an "Event" stepper
in the footer, and a + button whose options stacked off the top of a phone screen.
After: the board, Prev, Next, the progress bar and one + button. The + opens a single labelled menu
(a bottom sheet on phones, a panel on larger screens) that holds everything else, grouped.

Every new string has Spanish and Arabic entries in the simulation's UI dictionaries.
Idempotent. Usage: python3 tools/simplify_ux.py [index.html]"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '<!--SIMPLE-UX-START-->' in s:
    print('simplified controls already applied'); sys.exit(0)

def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('not found exactly %d time(s): ' % count) + old[:100]
    s = s.replace(old, new)

# ---------------------------------------------------------------- fewer first-visit interruptions
# Eleven Minutes opens only when linked (#11minutes) or chosen from the menu, not automatically.
swap("if(!deepLinked() && (location.hash === '#11minutes' || (!seen() && english()))) setTimeout(window.__eleven.open, 420);",
     "if(!deepLinked() && location.hash === '#11minutes') setTimeout(window.__eleven.open, 420);   /* simplified first visit: no automatic opening */")
# the 7-step tour no longer starts by itself; the one-card "How to read this" replaces it
swap("    setTimeout(function(){ startTour(false); }, 950);",
     "    setTimeout(function(){ if(window.otsCoach) window.otsCoach(); }, 950);   /* the full tour stays in + > How it works */")
swap("if(!localStorage.getItem('ots_onboarding_seen_v1_0_0') && window.startTour) window.startTour(false);",
     "if(window.otsCoach) window.otsCoach();")
# no "read it as a book?" banner: the chooser and the + menu already offer the library
swap("  (function waitForSim(){ var n = 0, ok = 0;",
     "  (function waitForSim(){ var n = 0, ok = 0; return;   /* simplified first visit: no banner */")
# no separate swipe tip: the first-visit card mentions swiping on phones
swap("} else if(mob() && !store('ots_swiped') && !store('ots_swipe_hint')){",
     "} else if(false){   /* simplified first visit: the swipe tip is in the first-visit card */")
# the library opens straight to the shelf; its tour stays in the library's own + menu
swap("    if(!ls('ots_library_tour_v2')) setTimeout(function(){ if(view.classList.contains('lib') && view.classList.contains('on')) libTour(false); }, 450);",
     "    /* simplified first visit: the library tour runs only when asked for (+ > How it works) */")

# ---------------------------------------------------------------- copy that described the old controls
swap('<p class="xp-note">Opens with a short introduction and a guided tour.</p>',
     '<p class="xp-note">Scene by scene. Tap a card to read it, then press Next.</p>')
hint_old = re.search(r'<div class="hint">Tap numbered cards for deep detail\.[^<]*</div>', s).group(0)
swap(hint_old, '<div class="hint">Tap a numbered card to read its detail and sources.</div>')

# ---------------------------------------------------------------- the + button opens the new menu
swap('<button class="fab-main" id="fabMain" onclick="toggleFab()" title="Menu">+</button>',
     '<button class="fab-main" id="fabMain" onclick="otsMenu()" title="Menu" aria-haspopup="dialog" aria-controls="otsMenu">+</button>')

BLOCK = r'''<!--SIMPLE-UX-START-->
<style>
/* ===== simplified controls: one + menu, one first-visit card (tools/simplify_ux.py) ===== */
#helpReplayBtn,.hdr-tools,.walkbar,#fabOptions{display:none !important}
#otsMenuBack{position:fixed;inset:0;z-index:2147482990;background:rgba(5,10,24,.55);opacity:0;pointer-events:none;transition:opacity .2s}
#otsMenuBack.on{opacity:1;pointer-events:auto}
#otsMenu{position:fixed;z-index:2147482995;right:20px;bottom:96px;width:min(380px,calc(100vw - 24px));max-height:calc(100vh - 130px);overflow:auto;
  background:#0F1D42;color:#F7F3EC;border:1.5px solid rgba(240,192,64,.55);border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.55);
  padding:14px 14px 16px;opacity:0;transform:translateY(12px);pointer-events:none;transition:opacity .2s,transform .2s;-webkit-overflow-scrolling:touch}
#otsMenu.on{opacity:1;transform:none;pointer-events:auto}
#otsMenu .om-head{display:flex;align-items:center;justify-content:space-between;padding:2px 4px 8px}
#otsMenu .om-title{font:700 20px/1.2 'EB Garamond',Georgia,serif;color:#F0C040}
#otsMenu .om-x{width:44px;height:44px;border-radius:50%;border:1px solid rgba(247,243,236,.25);background:transparent;color:#F7F3EC;font:400 22px/1 system-ui,sans-serif;cursor:pointer}
#otsMenu h5{margin:12px 4px 6px;font:700 13px/1.2 Inter,system-ui,sans-serif;color:rgba(247,243,236,.72);letter-spacing:.02em}
#otsMenu .om-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
#otsMenu .om-it{display:flex;align-items:center;gap:10px;min-height:56px;padding:10px 12px;border-radius:12px;border:1px solid rgba(247,243,236,.16);
  background:rgba(255,255,255,.05);color:#F7F3EC;font:600 15px/1.25 Inter,system-ui,sans-serif;text-align:start;cursor:pointer;text-decoration:none}
#otsMenu .om-it:hover,#otsMenu .om-it:focus-visible{background:rgba(240,192,64,.14);border-color:rgba(240,192,64,.7);outline:none}
#otsMenu .om-it .ic{font-size:22px;line-height:1;flex:none}
#otsMenu .om-it.wide{grid-column:1 / -1}
#otsMenu .om-it[hidden]{display:none}
#fabMain.om-open{transform:rotate(45deg)}
@media (max-width:900px){
  #otsMenu{left:0;right:0;bottom:0;width:auto;max-height:90vh;border-radius:22px 22px 0 0;border-width:1.5px 0 0;
    padding:10px 14px calc(18px + env(safe-area-inset-bottom,0px));transform:translateY(100%)}
  #otsMenu.on{transform:none}
  #otsMenu .om-head::before{content:'';position:absolute;left:50%;top:8px;width:44px;height:5px;margin-left:-22px;border-radius:3px;background:rgba(247,243,236,.3)}
  #otsMenu .om-head{padding-top:12px;padding-bottom:2px}
  #otsMenu h5{margin:8px 4px 5px}
  #otsMenu .om-it{min-height:50px;padding:8px 10px;font-size:14.5px}
  #otsMenu .om-it .ic{font-size:20px}
  #otsMenu .om-x{width:40px;height:40px}
}
/* first-visit card */
#otsCoach{position:fixed;z-index:2147482985;left:50%;bottom:calc(var(--uxFootH,64px) + 22px);transform:translate(-50%,16px);width:min(440px,calc(100vw - 24px));
  background:#0F1D42;color:#F7F3EC;border:1.5px solid #F0C040;border-radius:18px;box-shadow:0 22px 60px rgba(0,0,0,.6);padding:18px 18px 16px;
  opacity:0;pointer-events:none;transition:opacity .25s,transform .25s}
#otsCoach.on{opacity:1;transform:translate(-50%,0);pointer-events:auto}
#otsCoach h4{margin:0 0 10px;font:700 21px/1.2 'EB Garamond',Georgia,serif;color:#F0C040}
#otsCoach ol{list-style:none;margin:0 0 14px;padding:0;display:grid;gap:10px}
#otsCoach li{display:flex;gap:12px;align-items:flex-start;font:500 16px/1.4 Inter,system-ui,sans-serif}
#otsCoach li .n{flex:none;width:26px;height:26px;border-radius:50%;background:#F0C040;color:#0B1530;font:800 14px/26px Inter,system-ui,sans-serif;text-align:center}
#otsCoach .plus{display:inline-flex;margin-inline-start:4px;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;background:#F0C040;color:#0B1530;font:800 16px/1 system-ui,sans-serif;vertical-align:-4px}
#otsCoach .ok{width:100%;min-height:50px;border:0;border-radius:12px;background:#F0C040;color:#0B1530;font:800 17px/1 Inter,system-ui,sans-serif;cursor:pointer}
#otsCoach .only-m{display:none}
@media (max-width:900px){ #otsCoach .only-m{display:inline} #otsCoach .only-d{display:none} #otsCoach{bottom:calc(var(--uxFootH,64px) + 84px)} }
#fabMain.om-pulse{animation:omPulse 1.6s ease-in-out infinite}
@keyframes omPulse{0%,100%{box-shadow:0 0 0 0 rgba(240,192,64,.65)}50%{box-shadow:0 0 0 14px rgba(240,192,64,0)}}
@media (prefers-reduced-motion:reduce){#otsMenu,#otsMenuBack,#otsCoach{transition:none}#fabMain.om-pulse{animation:none}}
</style>
<div id="otsMenuBack" onclick="otsMenu(false)"></div>
<div id="otsMenu" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
  <div class="om-head"><div class="om-title">Menu</div><button class="om-x" type="button" onclick="otsMenu(false)" aria-label="Close">✕</button></div>
  <h5>Explore</h5>
  <div class="om-grid">
    <button class="om-it" type="button" data-a="chapters"><span class="ic">📚</span><span>Chapters</span></button>
    <button class="om-it" type="button" data-a="search"><span class="ic">🔍</span><span>Search</span></button>
    <button class="om-it" type="button" data-a="guide"><span class="ic">🧭</span><span>Walk me through this scene</span></button>
    <button class="om-it" type="button" data-a="book"><span class="ic">📖</span><span>Read it as a book</span></button>
    <button class="om-it" type="button" data-a="dash" hidden><span class="ic">📊</span><span>Dashboard</span></button>
    <button class="om-it" type="button" data-a="map" hidden><span class="ic">🗺️</span><span>Architecture map</span></button>
  </div>
  <h5>This scene</h5>
  <div class="om-grid">
    <button class="om-it" type="button" data-a="sources"><span class="ic">📄</span><span>Sources</span></button>
    <button class="om-it" type="button" data-a="key"><span class="ic">🎨</span><span>What the colors mean</span></button>
  </div>
  <h5>Help and more</h5>
  <div class="om-grid">
    <button class="om-it" type="button" data-a="how"><span class="ic">❓</span><span>How it works</span></button>
    <button class="om-it" type="button" data-a="faq"><span class="ic">💬</span><span>Common questions</span></button>
    <button class="om-it" type="button" data-a="eleven"><span class="ic">⏱️</span><span>Eleven Minutes intro</span></button>
    <button class="om-it" type="button" data-a="lang"><span class="ic">🌐</span><span>Language</span></button>
    <a class="om-it wide" href="https://awakenwithsophia.sophia13.workers.dev/"><span class="ic">🔮</span><span>Back to Sophia</span></a>
  </div>
</div>
<div id="otsCoach" role="dialog" aria-label="How to read this" aria-hidden="true">
  <h4>How to read this</h4>
  <ol>
    <li><span class="n">1</span><span>Tap a numbered card to read who or what it is, with sources.</span></li>
    <li><span class="n">2</span><span><span class="only-d">Press NEXT to go to the next scene.</span><span class="only-m">Press NEXT, or swipe, to go to the next scene.</span></span></li>
    <li><span class="n">3</span><span>Everything else is under this button:<span class="plus" aria-hidden="true">+</span></span></li>
  </ol>
  <button class="ok" type="button" onclick="otsCoachDone()">Got it</button>
</div>
<script>
(function(){
  function $(id){ return document.getElementById(id); }
  function ls(k, v){ try{ if(v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); }catch(e){ return null; } }
  var menu = $('otsMenu'), back = $('otsMenuBack'), fab = $('fabMain');
  function lang(){ var l = (document.documentElement.lang || 'en').toLowerCase(); return l.slice(0, 2); }

  /* ---------- the + menu ---------- */
  window.otsMenu = function(open){
    if(open === undefined) open = !menu.classList.contains('on');
    if(open){
      otsCoachDone();
      try{ $('fabMain').classList.remove('om-pulse'); }catch(e){}
      var d = false, m = false;
      try{ d = !!(window.dashForCurrent && window.dashForCurrent()); }catch(e){}
      try{ m = !!(window.mapForCurrent && window.mapForCurrent()); }catch(e){}
      menu.querySelector('[data-a="dash"]').hidden = !d;
      menu.querySelector('[data-a="map"]').hidden = !m;
      menu.querySelector('[data-a="eleven"]').hidden = lang() !== 'en';   /* Eleven Minutes is written in English */
      try{ if(window.localizeUI) window.localizeUI(menu); }catch(e){}
    }
    menu.classList.toggle('on', open); back.classList.toggle('on', open);
    menu.setAttribute('aria-hidden', open ? 'false' : 'true');
    if(fab){ fab.classList.toggle('om-open', open); fab.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    if(open) setTimeout(function(){ var f = menu.querySelector('.om-it:not([hidden])'); if(f) try{ f.focus({preventScroll:true}); }catch(e){} }, 60);
    else if(fab) try{ fab.focus({preventScroll:true}); }catch(e){}
  };
  var ACT = {
    chapters: function(){ var e = $('era'); if(e) e.click(); else if(window.fabSwitchScene) fabSwitchScene(); },
    search:   function(){ if(window.openRP) openRP(); },
    guide:    function(){ if(window.openGuide) openGuide(); },
    book:     function(){ if(window.openBook) openBook(null); },
    dash:     function(){ if(window.fabDashboard) fabDashboard(); },
    map:      function(){ if(window.fabMap) fabMap(); },
    sources:  function(){ if(window.openSrc) openSrc(); },
    key:      function(){ if(window.openLegend) openLegend(); },
    how:      function(){ if(window.startTour) startTour(true); },
    faq:      function(){ if(window.openRP) openRP(); setTimeout(function(){ if(window.rpSwitch) rpSwitch('faq'); }, 60); },
    eleven:   function(){ if(window.__eleven) window.__eleven.open(); },
    lang:     function(){ if(window.openLangModal) openLangModal(); }
  };
  menu.addEventListener('click', function(e){
    var b = e.target.closest('[data-a]'); if(!b) return;
    otsMenu(false); var f = ACT[b.getAttribute('data-a')]; if(f) setTimeout(f, 120);
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && menu.classList.contains('on')) otsMenu(false); });
  /* the library has its own menu; close this one if the library opens */
  if(window.MutationObserver) new MutationObserver(function(){ if(document.body.classList.contains('book-open') && menu.classList.contains('on')) otsMenu(false); })
    .observe(document.body, {attributes:true, attributeFilter:['class']});

  /* ---------- the one first-visit card ---------- */
  var KEY = 'ots_coach_v1', coach = $('otsCoach'), waiting = false;
  function shown(el){ return el && !el.hidden && getComputedStyle(el).display !== 'none' && !el.classList.contains('hide'); }
  function clear(){
    var b = document.body.classList; if(b.contains('book-open') || b.contains('modal-open') || b.contains('overlay-open')) return false;
    if(shown($('welcomeOverlay')) || shown($('xpChooser'))) return false;
    var x = $('xpChooser'); if(x && x.classList.contains('on')) return false;
    var e = $('elevenOverlay'); if(e && !e.hidden) return false;
    var t = $('tourOverlay'); if(t && t.classList.contains('active')) return false;
    return true;
  }
  window.otsCoach = function(){
    if(ls(KEY) || ls('ots_onboarding_seen_v1_0_0') || waiting) return;   /* seen this, or the old full tour */
    if(/^#(scene|dash|map)=/.test(location.hash || '')) return;           /* arrived by a shared link: let them read */
    waiting = true; var n = 0;
    var iv = setInterval(function(){
      n++; if(ls(KEY) || n > 300){ clearInterval(iv); waiting = false; return; }
      if(!clear()) return;
      clearInterval(iv); waiting = false;
      try{ if(window.localizeUI) window.localizeUI(coach); }catch(e){}
      coach.classList.add('on'); coach.setAttribute('aria-hidden', 'false');
      try{ $('fabMain').classList.add('om-pulse'); }catch(e){}
      setTimeout(function(){ try{ coach.querySelector('.ok').focus({preventScroll:true}); }catch(e){} }, 80);
    }, 700);
  };
  window.otsCoachDone = function(){
    if(!coach.classList.contains('on')) return;
    ls(KEY, '1'); ls('ots_onboarding_seen_v1_0_0', '1');
    coach.classList.remove('on'); coach.setAttribute('aria-hidden', 'true');
    try{ $('fabMain').classList.remove('om-pulse'); }catch(e){}
  };
})();
</script>
<!--SIMPLE-UX-END-->
'''
assert s.count('</body>') == 1
s = s.replace('</body>', BLOCK + '</body>')

# ---------------------------------------------------------------- translations
ES = {
 'Scene by scene. Tap a card to read it, then press Next.': 'Escena por escena. Toca una tarjeta para leerla y luego pulsa Siguiente.',
 'Tap a numbered card to read its detail and sources.': 'Toca una tarjeta numerada para leer el detalle y las fuentes.',
 'Menu': 'Menú', 'Explore': 'Explorar', 'Chapters': 'Capítulos', 'Search': 'Buscar',
 'Walk me through this scene': 'Recórreme esta escena', 'Read it as a book': 'Léelo como libro',
 'Dashboard': 'Panel de datos', 'Architecture map': 'Mapa de la arquitectura', 'This scene': 'Esta escena',
 'Sources': 'Fuentes', 'What the colors mean': 'Qué significan los colores', 'Help and more': 'Ayuda y más',
 'How it works': 'Cómo funciona', 'Common questions': 'Preguntas frecuentes', 'Eleven Minutes intro': 'Introducción: Once minutos',
 'Language': 'Idioma', 'Back to Sophia': 'Volver a Sophia', 'Close': 'Cerrar',
 'How to read this': 'Cómo leer esto',
 'Tap a numbered card to read who or what it is, with sources.': 'Toca una tarjeta numerada para saber quién o qué es, con sus fuentes.',
 'Press NEXT to go to the next scene.': 'Pulsa SIGUIENTE para pasar a la siguiente escena.',
 'Press NEXT, or swipe, to go to the next scene.': 'Pulsa SIGUIENTE, o desliza, para pasar a la siguiente escena.',
 'Everything else is under this button:': 'Todo lo demás está en este botón:',
 'Got it': 'Entendido',
}
AR = {
 'Scene by scene. Tap a card to read it, then press Next.': 'مشهدًا بعد مشهد. اضغط على بطاقة لقراءتها، ثم اضغط «التالي».',
 'Tap a numbered card to read its detail and sources.': 'اضغط على بطاقة مرقّمة لقراءة تفاصيلها ومصادرها.',
 'Menu': 'القائمة', 'Explore': 'استكشف', 'Chapters': 'الفصول', 'Search': 'بحث',
 'Walk me through this scene': 'اشرح لي هذا المشهد خطوة بخطوة', 'Read it as a book': 'اقرأه ككتاب',
 'Dashboard': 'لوحة البيانات', 'Architecture map': 'خريطة البنية', 'This scene': 'هذا المشهد',
 'Sources': 'المصادر', 'What the colors mean': 'معنى الألوان', 'Help and more': 'المساعدة والمزيد',
 'How it works': 'كيف يعمل', 'Common questions': 'الأسئلة الشائعة', 'Eleven Minutes intro': 'مقدمة: إحدى عشرة دقيقة',
 'Language': 'اللغة', 'Back to Sophia': 'العودة إلى صوفيا', 'Close': 'إغلاق',
 'How to read this': 'كيف تقرأ هذا',
 'Tap a numbered card to read who or what it is, with sources.': 'اضغط على بطاقة مرقّمة لتعرف من هو أو ما هو، مع المصادر.',
 'Press NEXT to go to the next scene.': 'اضغط «التالي» للانتقال إلى المشهد التالي.',
 'Press NEXT, or swipe, to go to the next scene.': 'اضغط «التالي» أو اسحب للانتقال إلى المشهد التالي.',
 'Everything else is under this button:': 'كل ما عدا ذلك موجود في هذا الزر:',
 'Got it': 'فهمت',
}
for lang, add in (('es', ES), ('ar', AR)):
    m = re.search(r'(<script type="application/json" id="i18n-%s">)(.*?)(</script>)' % lang, s, re.S)
    d = json.loads(m.group(2))
    for k, v in add.items(): d['ui'][k] = v
    txt = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + txt + s[m.end(2):]

open(P, 'w', encoding='utf-8').write(s)
print('simplified controls applied; %d Spanish and %d Arabic strings added' % (len(ES), len(AR)))
