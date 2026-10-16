#!/usr/bin/env python3
"""Clear scene controls, a card stepper that follows the reader, and told-vs-record as a window (index.html).

- Footer: "◂ Previous scene", a card stepper ("◂ Card 2 of 4 ▸"), the progress bar, and a gold
  "Next scene ▸". On phones: progress bar, then the card stepper, then the two scene buttons.
- The card stepper goes 1, 2, 3 … through the scene's cards. Tapping any card out of order moves the
  stepper to it, so the arrows carry on from there. An open card has "Previous card / Next card" buttons;
  on the last card the button becomes "Next scene".
- Card numbers are larger.
- The right-hand panel (and the phone's "Told vs. Record" button) is gone. Each scene opens with a window:
  "What they told you" (red) and "What the record shows" (green), with a switch to stop it opening by
  itself. It is always in + > This scene > What they told you vs. the record.
Run after tools/simplify_ux.py. Idempotent. Usage: python3 tools/scene_controls.py [index.html]"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '<!--SCENECTL-START-->' in s:
    print('scene controls already applied'); sys.exit(0)

def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('not found exactly %d time(s): ' % count) + old[:100]
    s = s.replace(old, new)

# ---------------------------------------------------------------- footer markup
swap('''      <div class="walkbar" title="Step through this scene's events one by one">
        <span class="wlabel">Event</span>
        <button class="wbtn" id="walkPrev" onclick="walkStep(-1)" disabled>◂</button>
        <span class="wpos"><span id="walkPos">—</span>/<span id="walkTotal">0</span></span>
        <button class="wbtn" id="walkNext" onclick="walkStep(1)">▸</button>
      </div>''',
'''      <div class="walkbar" role="group" aria-label="Cards in this scene">
        <button class="wbtn" id="walkPrev" onclick="walkStep(-1)" disabled aria-label="Previous card">◂</button>
        <button type="button" class="wplay" id="walkPlay" onclick="walkStep(1)"><span class="pi" aria-hidden="true">▶</span><span>Play scene</span></button>
        <span class="wpos"><span id="walkTxt">Cards</span><span class="wl-raw" hidden><span id="walkPos">—</span>/<span id="walkTotal">0</span></span></span>
        <button class="wbtn" id="walkNext" onclick="walkStep(1)" aria-label="Next card">▸</button>
      </div>''')
swap('<button class="btn" id="btnPrev" onclick="go(-1)" disabled>◂ PREV</button>',
     '<button class="btn" id="btnPrev" onclick="go(-1)" disabled>◂ Previous scene</button>')
swap('<button class="btn" id="btnNext" onclick="go(1)">NEXT ▸</button>',
     '<button class="btn" id="btnNext" onclick="go(1)">Next scene ▸</button>')

# ---------------------------------------------------------------- previous / next card inside an open card
swap('''      <button class="modal-expand-btn" onclick="openDeepDive()">⬡ See Full Event Analysis &amp; Synthesis →</button>
    </div>
  </div>
</div>''',
'''      <button class="modal-expand-btn" onclick="openDeepDive()">⬡ See Full Event Analysis &amp; Synthesis →</button>
    </div>
    <div class="m-walk"><button type="button" id="mwPrev" onclick="walkStep(-1)">◂ Previous card</button><span id="mwPos"></span><button type="button" id="mwNext" onclick="otsCardNext()">Next card ▸</button></div>
  </div>
</div>''')

# ---------------------------------------------------------------- the stepper follows a tapped card
swap('''function showEntity(e){
  curEnt = e;
  const sc = S[cur];''',
'''function showEntity(e){
  curEnt = e;
  const sc = S[cur];
  { const wi = sc.ents.indexOf(e); if(wi >= 0) walkIndex = wi; }   /* a tapped card becomes the stepper's position */''')
swap('''  focusEntity(e.id);

  // Deep-dive button when a rich deep-dive exists OR body is substantial''',
'''  focusEntity(e.id);
  updateWalkControls();

  // Deep-dive button when a rich deep-dive exists OR body is substantial''')

BLOCK = r'''<!--SCENECTL-START-->
<style>
/* ===== scene controls and told-vs-record window (tools/scene_controls.py) ===== */
aside.side,#sheetToggle,.sheet-backdrop,#panelToggleBtn{display:none !important}
main{grid-template-columns:1fr !important}
/* footer: Previous scene · card stepper · progress · Next scene */
footer .brand{display:none !important}
footer{display:grid !important;grid-template-columns:auto auto minmax(0,1fr) auto !important;grid-template-areas:"prev walk scrub next" !important;gap:14px !important;align-items:center}
footer > .btns{display:contents !important}
#btnPrev{grid-area:prev}
footer .walkbar{grid-area:walk}
footer .scrubwrap{grid-area:scrub !important;order:0 !important}
#btnNext{grid-area:next}
footer .brand{grid-area:brand}
#btnPrev,#btnNext{font:800 14px/1 Inter,system-ui,sans-serif !important;letter-spacing:.01em !important;min-height:46px !important;padding:0 18px !important;border-radius:10px !important;text-transform:none}
#btnPrev{background:transparent !important;border:1.5px solid rgba(240,192,64,.6) !important;color:var(--cream) !important}
#btnPrev:disabled{opacity:.4}
#btnNext{background:var(--gold) !important;border:1.5px solid var(--gold) !important;color:#0B1530 !important;box-shadow:0 4px 16px rgba(240,192,64,.3)}
#btnNext:disabled{opacity:.45}
footer .walkbar{display:flex !important;align-items:center;gap:8px;background:rgba(240,192,64,.10) !important;border:1.5px solid rgba(240,192,64,.55) !important;border-radius:12px !important;padding:4px !important}
footer .walkbar .wbtn{width:42px !important;height:38px !important;border-radius:8px !important;font-size:16px !important;background:#1B2A4A !important;border:1px solid rgba(240,192,64,.5) !important;color:var(--cream) !important}
footer .walkbar .wbtn:disabled{opacity:.35}
footer .walkbar .wpos{min-width:104px !important;font:800 14px/1.1 Inter,system-ui,sans-serif !important;color:var(--cream) !important;text-align:center;white-space:nowrap}
@media (min-width:901px){ .fab-wrap{bottom:calc(var(--uxFootH,72px) + 16px) !important;right:22px !important} #otsMenu{bottom:calc(var(--uxFootH,72px) + 78px) !important;max-height:calc(100vh - var(--uxFootH,72px) - 110px) !important} }
footer .walkbar .wplay{display:none;align-items:center;justify-content:center;gap:10px;min-height:38px;padding:0 20px;border:0;border-radius:8px;background:var(--gold);color:#0B1530;font:800 15px/1 Inter,system-ui,sans-serif;cursor:pointer;white-space:nowrap;box-shadow:0 0 0 0 rgba(240,192,64,.6);animation:wpPulse 2.2s ease-in-out 3}
footer .walkbar .wplay .pi{font-size:13px}
footer .walkbar.idle .wplay{display:inline-flex}
footer .walkbar.idle .wbtn,footer .walkbar.idle .wpos{display:none !important}
footer:has(.walkbar.idle) #btnNext{background:transparent !important;color:var(--cream) !important;border-color:rgba(240,192,64,.75) !important;box-shadow:none}
@keyframes wpPulse{0%,100%{box-shadow:0 0 0 0 rgba(240,192,64,.55)}50%{box-shadow:0 0 0 10px rgba(240,192,64,0)}}
@media (prefers-reduced-motion:reduce){footer .walkbar .wplay{animation:none}}
/* larger card numbers */
.entity .badge{width:30px !important;height:30px !important;font-size:14px !important;top:-12px !important;left:-12px !important;border-width:2.5px !important;box-shadow:0 2px 8px rgba(0,0,0,.45)}
.entity.focused .badge{background:#fff !important;transform:scale(1.08)}
/* previous / next card inside an open card */
.m-walk{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:14px;padding-top:12px;border-top:1px solid rgba(27,42,74,.18)}
.m-walk button{min-height:44px;padding:0 14px;border-radius:10px;border:1.5px solid #1B2A4A;background:transparent;color:#1B2A4A;font:800 14px/1 Inter,system-ui,sans-serif;cursor:pointer}
.m-walk #mwNext{background:#1B2A4A;color:#F7F3EC}
.m-walk button:disabled{opacity:.35;cursor:default}
.m-walk #mwPos{font:700 13px/1 Inter,system-ui,sans-serif;color:#5A6478;white-space:nowrap}
@media (max-width:900px){
  footer{grid-template-columns:1fr 1fr !important;grid-template-areas:"scrub scrub" "walk walk" "prev next" !important;gap:8px !important}
  footer .brand{display:none !important}
  footer .walkbar{justify-content:space-between}
  footer .walkbar .wplay{width:100%;min-height:42px;font-size:16px}
  footer .walkbar .wbtn{width:56px !important;height:42px !important}
  #btnPrev,#btnNext{width:100%;padding:0 10px !important;font-size:14.5px !important}
  .narration{padding-bottom:12px !important;padding-inline-end:84px !important}
  .m-walk button{padding:0 10px;font-size:13.5px}
}
/* told-vs-record window */
#trBack{position:fixed;inset:0;z-index:2147482970;background:rgba(5,10,24,.6);opacity:0;pointer-events:none;transition:opacity .2s}
#trBack.on{opacity:1;pointer-events:auto}
#trModal{position:fixed;z-index:2147482975;left:50%;top:50%;width:min(620px,calc(100vw - 24px));max-height:calc(100vh - 40px);overflow:auto;
  transform:translate(-50%,-46%);opacity:0;pointer-events:none;transition:opacity .2s,transform .2s;
  background:#0F1D42;color:#F7F3EC;border:1.5px solid rgba(240,192,64,.55);border-radius:18px;box-shadow:0 24px 70px rgba(0,0,0,.6);padding:18px 18px 16px}
#trModal.on{opacity:1;transform:translate(-50%,-50%);pointer-events:auto}
#trModal .tr-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:12px}
#trModal .tr-ttl{font:700 21px/1.25 'EB Garamond',Georgia,serif;color:#F0C040}
#trModal .tr-x{flex:none;width:42px;height:42px;border-radius:50%;border:1px solid rgba(247,243,236,.25);background:transparent;color:#F7F3EC;font:400 20px/1 system-ui,sans-serif;cursor:pointer}
#trModal .tr-box{background:#F7F3EC;color:#1E2433;border-radius:12px;padding:14px 16px;margin-bottom:12px;border-inline-start:6px solid}
#trModal .tr-told{border-color:#D33A3A}
#trModal .tr-rec{border-color:#1E9E5A;background:#EEF8F1}
#trModal .tr-h{display:flex;align-items:center;gap:8px;font:800 14px/1.2 Inter,system-ui,sans-serif;margin-bottom:8px}
#trModal .tr-told .tr-h{color:#B32626}
#trModal .tr-rec .tr-h{color:#14784A}
#trModal .tr-h .dot{width:10px;height:10px;border-radius:50%;flex:none}
#trModal .tr-told .dot{background:#D33A3A}
#trModal .tr-rec .dot{background:#1E9E5A}
#trModal .tr-t{font:400 18px/1.55 'EB Garamond',Georgia,serif}
#trModal .tr-told .tr-t{font-style:italic}
#trModal .tr-foot{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;position:sticky;bottom:-16px;margin:4px -18px -16px;padding:12px 18px 16px;background:#0F1D42;border-top:1px solid rgba(247,243,236,.12);box-shadow:0 -10px 20px rgba(15,29,66,.9)}
#trModal label{display:flex;align-items:center;gap:8px;font:600 14px/1.3 Inter,system-ui,sans-serif;color:rgba(247,243,236,.85);cursor:pointer}
#trModal label input{width:20px;height:20px;accent-color:#F0C040}
#trModal .tr-go{min-height:48px;padding:0 22px;border:0;border-radius:12px;background:#F0C040;color:#0B1530;font:800 16px/1 Inter,system-ui,sans-serif;cursor:pointer}
@media (max-width:600px){ #trModal{top:auto;bottom:0;left:0;right:0;width:auto;max-height:88vh;border-radius:20px 20px 0 0;transform:translateY(30px);padding:16px 14px calc(16px + env(safe-area-inset-bottom,0px))}
  #trModal.on{transform:none} #trModal .tr-t{font-size:17px} #trModal .tr-go{width:100%}
  #trModal .tr-foot{bottom:calc(-16px - env(safe-area-inset-bottom,0px));margin:4px -14px calc(-16px - env(safe-area-inset-bottom,0px));padding:12px 14px calc(16px + env(safe-area-inset-bottom,0px))} }
@media (prefers-reduced-motion:reduce){#trModal,#trBack{transition:none}}
</style>
<div id="trBack" onclick="otsTold(false)"></div>
<div id="trModal" role="dialog" aria-modal="true" aria-labelledby="trTtl" aria-hidden="true">
  <div class="tr-top"><div class="tr-ttl" id="trTtl"></div><button class="tr-x" type="button" onclick="otsTold(false)" aria-label="Close">✕</button></div>
  <div class="tr-box tr-told"><div class="tr-h"><span class="dot"></span><span>What they told you</span></div><div class="tr-t" id="trTold"></div></div>
  <div class="tr-box tr-rec"><div class="tr-h"><span class="dot"></span><span>What the record shows</span></div><div class="tr-t" id="trRec"></div></div>
  <div class="tr-foot">
    <label><input type="checkbox" id="trAuto" checked> <span>Show this when each scene opens</span></label>
    <button class="tr-go" type="button" onclick="otsTold(false)">Explore this scene</button>
  </div>
</div>
<script>
(function(){
  function $(id){ return document.getElementById(id); }
  function tr(k){ try{ var d = (I18N[LANG] || {}).ui || {}; return d[k] || k; }catch(e){ return k; } }
  var AUTO = 'ots_tr_auto';
  function auto(){ try{ return localStorage.getItem(AUTO) !== '0'; }catch(e){ return true; } }

  /* ---------- card stepper text: "4 cards" before starting, then "Card 2 of 4" ---------- */
  var origUpdate = window.updateWalkControls;
  window.updateWalkControls = function(){
    origUpdate.apply(this, arguments);
    var n = (S[cur] && S[cur].ents || []).length, i = walkIndex;
    var wb = document.querySelector('footer .walkbar'); if(wb) wb.classList.toggle('idle', i < 0 && n > 0);
    var pl = $('walkPlay'); if(pl) pl.setAttribute('aria-label', tr('Play scene') + ' · ' + tr('{t} cards').replace('{t}', n));
    $('walkTxt').textContent = i < 0 ? tr('{t} cards').replace('{t}', n) : tr('Card {n} of {t}').replace('{n}', i + 1).replace('{t}', n);
    var mp = $('mwPos'); if(mp) mp.textContent = i < 0 ? '' : (i + 1) + ' / ' + n;
    var pv = $('mwPrev'), nx = $('mwNext');
    if(pv) pv.disabled = i <= 0;
    if(nx){ var last = i >= n - 1; nx.textContent = last ? (cur < S.length - 1 ? tr('Next scene ▸') : tr('Next card ▸')) : tr('Next card ▸'); nx.disabled = last && cur >= S.length - 1; }
  };
  /* from an open card: next card, or the next scene after the last card */
  window.otsCardNext = function(){
    var n = (S[cur] && S[cur].ents || []).length;
    if(walkIndex >= n - 1){ if(cur < S.length - 1){ closeModal(); go(1); } return; }
    walkStep(1);
  };

  /* ---------- told vs. record ---------- */
  var box = $('trModal'), back = $('trBack'), chk = $('trAuto');
  chk.checked = auto();
  chk.addEventListener('change', function(){ try{ localStorage.setItem(AUTO, chk.checked ? '1' : '0'); }catch(e){} });
  function shown(el){ return el && el.isConnected && !el.hidden && getComputedStyle(el).display !== 'none' && !el.classList.contains('fade-out'); }
  function busy(){
    var b = document.body.classList; if(b.contains('book-open')) return true;
    if(shown($('welcomeOverlay'))) return true;
    var x = $('xpChooser'); if(x && x.classList.contains('on')) return true;
    var e = $('elevenOverlay'); if(e && !e.hidden) return true;
    var t = $('tourOverlay'); if(t && t.classList.contains('active')) return true;
    var c = $('otsCoach'); if(c && c.classList.contains('on')) return true;
    var m = $('otsMenu'); if(m && m.classList.contains('on')) return true;
    return ['modalBack','ddBack','guideBack','rsrcBack','srcPanel','legendPanel','rpPanel','uxCh','langModal','dashPage','mapPage'].some(function(id){ var el = $(id); return el && el.classList.contains('on'); });
  }
  window.otsTold = function(open){
    if(open){
      var told = ($('told').textContent || '').trim(), rec = ($('rec').textContent || '').trim();
      if(!told && !rec) return;
      $('trTtl').textContent = ($('title').textContent || '').trim();
      $('trTold').textContent = told; $('trRec').textContent = rec;
      chk.checked = auto();
      try{ if(window.localizeUI) window.localizeUI(box); }catch(e){}
    }
    box.classList.toggle('on', !!open); back.classList.toggle('on', !!open);
    box.setAttribute('aria-hidden', open ? 'false' : 'true');
    if(open) setTimeout(function(){ try{ box.querySelector('.tr-go').focus({preventScroll:true}); }catch(e){} }, 60);
  };
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && box.classList.contains('on')) otsTold(false); });

  /* each scene opens with it (unless switched off, or something else is on screen) */
  var timer = null, shownFor = null;
  function sceneChanged(){
    clearTimeout(timer); window.__trPending = false;
    if(box.classList.contains('on')) otsTold(false);
    if(!auto()) return;
    var at = cur, tries = 0; window.__trPending = true;   /* the first-visit card waits for this */
    timer = setTimeout(function wait(){
      if(cur !== at){ window.__trPending = false; return; }   /* moved on already */
      if(busy()){ if(++tries < 120) timer = setTimeout(wait, 700); else window.__trPending = false; return; }
      window.__trPending = false;
      if(shownFor === S[at].id) return;
      shownFor = S[at].id; otsTold(true);
    }, 550);
  }
  var origRender = window.renderScene;
  window.renderScene = function(){ var r = origRender.apply(this, arguments); try{ shownFor = null; sceneChanged(); }catch(e){} return r; };
  try{ if(typeof S !== 'undefined' && S.length) sceneChanged(); }catch(e){}
  try{ updateWalkControls(); }catch(e){}
})();
</script>
<!--SCENECTL-END-->
'''
assert s.count('</body>') == 1
s = s.replace('</body>', BLOCK + '</body>')

ES = {
 'Play scene': 'Reproducir escena', '◂ Previous scene': '◂ Escena anterior', 'Next scene ▸': 'Escena siguiente ▸', 'Cards': 'Tarjetas',
 '{t} cards': '{t} tarjetas', 'Card {n} of {t}': 'Tarjeta {n} de {t}', '◂ Previous card': '◂ Tarjeta anterior', 'Next card ▸': 'Tarjeta siguiente ▸',
 'Previous card': 'Tarjeta anterior', 'Next card': 'Tarjeta siguiente', 'Cards in this scene': 'Tarjetas de esta escena',
 'What they told you': 'Lo que te dijeron', 'What the record shows': 'Lo que muestra el registro',
 'Show this when each scene opens': 'Mostrar esto al abrir cada escena', 'Explore this scene': 'Explorar esta escena',
}
AR = {
 'Play scene': 'شغّل المشهد', '◂ Previous scene': 'المشهد السابق ▸', 'Next scene ▸': '◂ المشهد التالي', 'Cards': 'البطاقات',
 '{t} cards': '{t} بطاقات', 'Card {n} of {t}': 'البطاقة {n} من {t}', '◂ Previous card': 'البطاقة السابقة ▸', 'Next card ▸': '◂ البطاقة التالية',
 'Previous card': 'البطاقة السابقة', 'Next card': 'البطاقة التالية', 'Cards in this scene': 'بطاقات هذا المشهد',
 'What they told you': 'ما قيل لك', 'What the record shows': 'ما يُظهره السجل',
 'Show this when each scene opens': 'اعرض هذا عند فتح كل مشهد', 'Explore this scene': 'استكشف هذا المشهد',
}
for lang, add in (('es', ES), ('ar', AR)):
    m = re.search(r'(<script type="application/json" id="i18n-%s">)(.*?)(</script>)' % lang, s, re.S)
    d = json.loads(m.group(2))
    for k, v in add.items(): d['ui'][k] = v
    txt = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + txt + s[m.end(2):]

open(P, 'w', encoding='utf-8').write(s)
print('scene controls applied; %d Spanish and %d Arabic strings added' % (len(ES), len(AR)))
