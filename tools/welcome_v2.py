#!/usr/bin/env python3
"""Welcome screen v2 for the Israel simulation (index.html), plus the first-visit experience chooser.

- The welcome summary stays until the visitor chooses (no more 15-second auto-continue).
- A short "what the record shows" brief, larger type on a darker backing for legibility over the rain.
- A bigger red pill; bolder social buttons (TikTok @awakenwithsophia, Instagram @chosen.ron13).
- First visit: after the red pill, a chooser (Simulation or Library) in the Israel flag's blue and white.
  Full screen on phones, a modal on larger screens. Returning visitors go straight in.
- Every new string has Spanish and Arabic entries in the simulation's UI dictionaries.
Usage: python3 tools/welcome_v2.py [index.html]"""
import json, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if 'id="xpChooser"' in s:
    print('welcome v2 already applied'); sys.exit(0)

def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('not found exactly %d time(s): ' % count) + old[:90]
    s = s.replace(old, new)

# ---------------------------------------------------------------- welcome markup
swap('''    <div class="welcome-cta">
    <button id="enterSimBtn" onclick="dismissWelcome()">💊 Enter Simulation</button>
    <div class="redpill-caption">Red Pill Only</div>
    <div class="welcome-skip">Auto-continuing in <span class="wtimer" id="wCountdown">15</span>s — or click above</div>
    </div>
    <div class="welcome-divider"></div>''',
'''    <div class="welcome-cta">
    <button id="enterSimBtn" onclick="openXpChooser()"><span class="rp-ico" aria-hidden="true">💊</span><span class="rp-lab">Enter Simulation</span></button>
    <div class="redpill-caption"><span class="rp-mini" aria-hidden="true">💊</span><span>Red Pill Only</span><span class="rp-mini" aria-hidden="true">💊</span></div>
    </div>
    <div class="welcome-divider"></div>
    <div class="welcome-brief">
      <div class="wb-h">What the record shows</div>
      <ul>
        <li><b class="wb-k">51 years</b><span>Recognition took eleven minutes on May 14, 1948. The structure behind it took 51 years to build.</span></li>
        <li><b class="wb-k">37 years</b><span>Herzl's program, the Balfour Declaration and the League of Nations Mandate all came before Hitler took power.</span></li>
        <li><b class="wb-k">757,182</b><span>People counted by Britain's own 1922 census of Palestine — about 11% Jewish.</span></li>
        <li><b class="wb-k">Overruled</b><span>The Secretary of State, the Pentagon and the new CIA opposed recognition in writing.</span></li>
      </ul>
    </div>''')

s, n = re.subn(r'<div class="welcome-highlights">.*?</div>\n',
    '<div class="welcome-highlights"><b>NEW: The Library.</b> <span>Read the record as books. Volumes I–III are ready.</span><br>'
    '<span class="wh-sub">Also: Eleven Minutes · Español · العربية · 📊 dashboards · 🗺️ architecture maps · 💻 the machine in code — tap ➕</span></div>\n', s, count=1, flags=re.S)
assert n == 1, 'highlights'

swap('''    <div class="welcome-follow">
      <div class="welcome-follow-label">Follow Me @chosen.ron13</div>
      <div class="welcome-follow-row">
        <a class="follow-btn" href="https://www.tiktok.com/@chosen.ron13" target="_blank" rel="noopener noreferrer"><span class="follow-icon">♫</span> TikTok</a>
        <a class="follow-btn" href="https://www.instagram.com/chosen.ron13" target="_blank" rel="noopener noreferrer"><span class="follow-icon">📷</span> Instagram</a>
      </div>
    </div>''',
'''    <div class="welcome-follow">
      <div class="welcome-follow-label">Follow the work</div>
      <div class="welcome-follow-row">
        <a class="sbtn sbtn-tt" href="https://www.tiktok.com/@awakenwithsophia" target="_blank" rel="noopener noreferrer"><span class="sb-ico" aria-hidden="true">♪</span><span class="sb-txt"><small>TikTok</small><b>@awakenwithsophia</b></span></a>
        <a class="sbtn sbtn-ig" href="https://www.instagram.com/chosen.ron13" target="_blank" rel="noopener noreferrer"><span class="sb-ico" aria-hidden="true">◎</span><span class="sb-txt"><small>Instagram</small><b>@chosen.ron13</b></span></a>
      </div>
    </div>''')

# the summary stays until the visitor chooses
swap("    if(seconds <= 0){ dismiss(); }", "    if(seconds <= 0){ clearInterval(countdownTimer); }")

# ---------------------------------------------------------------- the chooser
SIM_ICON = ('<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">'
            '<path d="M14 18 L32 30 L50 16 M32 30 L22 48 M32 30 L46 46"/></g><g fill="currentColor">'
            '<circle cx="14" cy="18" r="5.5"/><circle cx="50" cy="16" r="5.5"/><circle cx="22" cy="48" r="5.5"/><circle cx="46" cy="46" r="5.5"/></g>'
            '<circle cx="32" cy="30" r="8" fill="#fff" stroke="currentColor" stroke-width="3"/></svg>')
LIB_ICON = ('<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round">'
            '<path d="M32 16 C24 11 14 11 8 13 V50 C14 48 24 48 32 53 C40 48 50 48 56 50 V13 C50 11 40 11 32 16 Z"/><path d="M32 16 V53"/></g>'
            '<g stroke="currentColor" stroke-width="1.8" stroke-linecap="round" opacity=".7"><path d="M14 22 H26 M14 28 H26 M14 34 H24 M38 22 H50 M38 28 H50 M38 34 H48"/></g></svg>')
CHOOSER = '''
<div id="xpChooser" hidden role="dialog" aria-modal="true" aria-labelledby="xpTitle">
  <div class="xp-card">
    <div class="xp-band" aria-hidden="true"></div>
    <div class="xp-head">
      <div class="xp-k">The Israel Architecture</div>
      <h2 id="xpTitle">Choose how to explore</h2>
      <p>Both hold the same documented record, with every claim tied to its source.</p>
    </div>
    <div class="xp-opts">
      <section class="xp-opt xp-sim">
        <div class="xp-ico">%s</div>
        <div class="xp-tag">The Simulation</div>
        <h3>Walk it scene by scene</h3>
        <p>Every chapter as interactive scenes. Tap any person, document or event to see who they are, how they connect, and the source behind it.</p>
        <p class="xp-note">Opens with a short introduction and a guided tour.</p>
        <button class="xp-cta" type="button" onclick="chooseXp('sim')"><span>Enter the Simulation</span><span aria-hidden="true"> ▸</span></button>
      </section>
      <section class="xp-opt xp-lib">
        <div class="xp-ico">%s</div>
        <div class="xp-tag">The Library</div>
        <h3>Read it as books</h3>
        <p>The same record, told in order as volumes, with every claim footnoted. Each chapter becomes its own volume.</p>
        <p class="xp-note">Ready now: The Baseline · The Road to 1948 · The Cold War Architecture</p>
        <button class="xp-cta" type="button" onclick="chooseXp('lib')"><span>Open the Library</span><span aria-hidden="true"> ▸</span></button>
      </section>
    </div>
    <div class="xp-foot">You can switch between the two at any time from the ＋ button.</div>
    <div class="xp-band" aria-hidden="true"></div>
  </div>
</div>
''' % (SIM_ICON, LIB_ICON)
swap('<div id="glossTip"></div>', CHOOSER + '<div id="glossTip"></div>')

CSS = r'''
<style>
/* ===== welcome v2: legibility, red pill, social buttons (tools/welcome_v2.py) ===== */
#welcomeOverlay .welcome-content{background:radial-gradient(120% 90% at 50% 40%,rgba(0,8,3,.88),rgba(0,6,2,.74));border:1px solid rgba(0,255,65,.16);border-radius:22px;box-shadow:0 0 0 1px rgba(0,0,0,.4),0 30px 80px rgba(0,0,0,.6)}
@media(max-width:600px){#welcomeOverlay .welcome-content{border-radius:0;border-left:0;border-right:0}}
#welcomeOverlay .welcome-tagline{font-size:21px;line-height:1.55;color:#7DFFA0;text-shadow:0 1px 2px #000}
#welcomeOverlay .welcome-body{font-size:19px;line-height:1.7;color:#F4FFF6;text-shadow:0 1px 2px #000}
#welcomeOverlay .welcome-stat{font-size:15px;color:#9CFFB6}
#welcomeOverlay .welcome-stat b{font-size:30px}
#welcomeOverlay .welcome-highlights{font-size:14px;line-height:1.6;color:#C9FFD6;letter-spacing:.2px}
#welcomeOverlay .welcome-highlights b{color:#FFC700}
#welcomeOverlay .wh-sub{color:#9CFFB6;font-size:13px}
#welcomeOverlay .welcome-skip{display:none}
/* the brief */
.welcome-brief{text-align:left;margin:4px auto 22px;padding:18px 20px;border-radius:16px;background:rgba(0,0,0,.55);border:1px solid rgba(255,199,0,.28);opacity:0;animation:wFadeUp .9s ease forwards;animation-delay:1.4s}
.welcome-brief .wb-h{font-family:'Courier New',monospace;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:#FFC700;margin-bottom:12px;text-align:center}
.welcome-brief ul{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.welcome-brief li{display:grid;grid-template-columns:118px 1fr;gap:14px;align-items:baseline}
.welcome-brief .wb-k{font-family:'Courier New',monospace;font-size:21px;font-weight:700;color:#FFC700;text-align:right;white-space:nowrap}
.welcome-brief li span{font-family:'EB Garamond',Georgia,serif;font-size:18.5px;line-height:1.45;color:#F4FFF6}
@media(max-width:600px){.welcome-brief{padding:16px 14px}.welcome-brief li{grid-template-columns:1fr;gap:2px}.welcome-brief .wb-k{text-align:left;font-size:20px}}
body.lang-ar .welcome-brief,html[dir="rtl"] .welcome-brief{text-align:right}
html[dir="rtl"] .welcome-brief .wb-k{text-align:left}
/* the red pill */
#welcomeOverlay #enterSimBtn{display:inline-flex;align-items:center;gap:14px;font-size:21px;letter-spacing:2.5px;padding:18px 40px 18px 26px;border-width:2px;
  background:radial-gradient(120% 160% at 30% 20%,#FF4D4D 0%,#C8102E 45%,#7A0010 100%);color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.5);
  box-shadow:0 0 0 4px rgba(255,59,59,.18),0 10px 40px rgba(255,30,30,.55),inset 0 2px 0 rgba(255,255,255,.35)}
#welcomeOverlay #enterSimBtn .rp-ico{font-size:40px;line-height:1;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5));display:inline-block;transform:rotate(-24deg)}
#welcomeOverlay #enterSimBtn:hover{transform:translateY(-2px) scale(1.03)}
#welcomeOverlay .redpill-caption{font-size:15px;letter-spacing:5px;color:#FF7A7A;display:flex;gap:10px;align-items:center;justify-content:center;font-weight:700}
#welcomeOverlay .redpill-caption .rp-mini{font-size:20px;letter-spacing:0}
@keyframes rpGlow{0%,100%{box-shadow:0 0 0 4px rgba(255,59,59,.18),0 10px 40px rgba(255,30,30,.5),inset 0 2px 0 rgba(255,255,255,.35)}50%{box-shadow:0 0 0 10px rgba(255,59,59,.08),0 12px 60px rgba(255,30,30,.85),inset 0 2px 0 rgba(255,255,255,.35)}}
@media(prefers-reduced-motion:no-preference){#welcomeOverlay #enterSimBtn{animation:wFadeUp .9s ease forwards 2.15s,rpGlow 2.4s ease-in-out 3.2s infinite}}
@media(max-width:600px){#welcomeOverlay #enterSimBtn{font-size:18px;padding:16px 30px 16px 20px;gap:12px}#welcomeOverlay #enterSimBtn .rp-ico{font-size:34px}}
/* social buttons */
#welcomeOverlay .welcome-follow-label{font-size:13px;letter-spacing:3px;color:#C9FFD6}
#welcomeOverlay .welcome-follow-row{gap:12px}
.sbtn{display:inline-flex;align-items:center;gap:12px;min-width:220px;padding:11px 20px 11px 14px;border-radius:16px;color:#fff;text-decoration:none;font-family:Inter,system-ui,sans-serif;
  transition:transform .15s ease,box-shadow .15s ease;box-shadow:0 8px 26px rgba(0,0,0,.45)}
.sbtn:hover,.sbtn:focus-visible{transform:translateY(-2px)}
.sbtn:focus-visible{outline:3px solid #fff;outline-offset:3px}
.sbtn .sb-ico{width:38px;height:38px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;background:rgba(255,255,255,.14)}
.sbtn .sb-txt{display:flex;flex-direction:column;text-align:left;line-height:1.15}
.sbtn small{font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;opacity:.9}
.sbtn b{font-size:16.5px;font-weight:800}
.sbtn-tt{background:#0B0B0F;border:1.5px solid #25F4EE;box-shadow:-3px -2px 0 #25F4EE,3px 2px 0 #FE2C55,0 10px 30px rgba(254,44,85,.35)}
.sbtn-tt .sb-ico{color:#fff;text-shadow:-2px -1px 0 #25F4EE,2px 1px 0 #FE2C55}
.sbtn-ig{background:linear-gradient(135deg,#F58529 0%,#DD2A7B 45%,#8134AF 75%,#515BD4 100%);border:1.5px solid rgba(255,255,255,.55);box-shadow:0 10px 30px rgba(221,42,123,.45)}
html[dir="rtl"] .sbtn .sb-txt{text-align:right}

/* ===== first-visit experience chooser — Israel flag blue and white ===== */
#xpChooser{position:fixed;inset:0;z-index:100000;display:flex;align-items:center;justify-content:center;padding:28px;background:rgba(2,8,28,.72);
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);opacity:0;transition:opacity .35s ease}
#xpChooser[hidden]{display:none}
#xpChooser.on{opacity:1}
#xpChooser .xp-card{--b:#0038B8;--ink:#0A1A4A;position:relative;width:min(1000px,100%);max-height:calc(100dvh - 56px);overflow:auto;background:#FFFFFF;color:var(--ink);border-radius:22px;
  box-shadow:0 40px 120px rgba(0,0,0,.6);transform:translateY(14px) scale(.98);transition:transform .4s cubic-bezier(.2,.8,.2,1);font-family:Inter,system-ui,sans-serif}
#xpChooser.on .xp-card{transform:none}
#xpChooser .xp-band{height:14px;margin:18px 0;background:var(--b)}
#xpChooser .xp-head,#xpChooser .xp-foot{display:block;position:static;background:none;border:0;box-shadow:none;height:auto}
#xpChooser .xp-head{text-align:center;padding:6px 28px 4px}
#xpChooser .xp-k{font-size:12px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:var(--b)}
#xpChooser h2{font-family:'EB Garamond',Georgia,serif;font-size:42px;line-height:1.05;margin:8px 0 8px;color:var(--ink);font-weight:700}
#xpChooser .xp-head p{font-size:16px;line-height:1.5;margin:0 auto;max-width:560px;color:#3A4A75}
#xpChooser .xp-opts{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:22px 28px 6px;border:2px solid var(--b);border-radius:18px;overflow:hidden}
#xpChooser .xp-opt{display:flex;flex-direction:column;align-items:flex-start;padding:26px 28px 28px;text-align:left}
#xpChooser .xp-sim{background:linear-gradient(180deg,#F3F7FF,#FFFFFF)}
#xpChooser .xp-lib{background:linear-gradient(180deg,#FFFFFF,#F3F7FF);border-left:2px solid var(--b)}
#xpChooser .xp-ico{width:62px;height:62px;color:var(--b);margin-bottom:12px}
#xpChooser .xp-ico svg{width:100%;height:100%}
#xpChooser .xp-tag{font-size:12px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:var(--b)}
#xpChooser h3{font-family:'EB Garamond',Georgia,serif;font-size:30px;line-height:1.1;margin:6px 0 10px;color:var(--ink)}
#xpChooser .xp-opt p{font-size:16px;line-height:1.55;margin:0 0 10px;color:#22305A}
#xpChooser .xp-opt .xp-note{font-size:14px;color:#4A5A86;font-style:italic;margin-bottom:20px}
#xpChooser .xp-cta{margin-top:auto;align-self:stretch;border:0;border-radius:14px;padding:16px 22px;font-size:17px;font-weight:800;letter-spacing:.3px;cursor:pointer;color:#fff;
  background:linear-gradient(180deg,#0B4AD6,#0038B8);box-shadow:0 10px 24px rgba(0,56,184,.35),inset 0 1px 0 rgba(255,255,255,.3);transition:transform .15s ease,box-shadow .15s ease}
#xpChooser .xp-cta:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,56,184,.45),inset 0 1px 0 rgba(255,255,255,.3)}
#xpChooser .xp-cta:focus-visible{outline:3px solid #FFC700;outline-offset:3px}
#xpChooser .xp-foot{text-align:center;font-size:14.5px;color:#3A4A75;padding:14px 24px 0}
html[dir="rtl"] #xpChooser .xp-opt{text-align:right;align-items:flex-end}
html[dir="rtl"] #xpChooser .xp-lib{border-left:0;border-right:2px solid var(--b)}
@media(max-width:760px){
  #xpChooser{padding:0;align-items:stretch}
  #xpChooser .xp-card{width:100%;max-height:none;height:100dvh;border-radius:0;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
  #xpChooser .xp-band{height:10px;margin:calc(10px + env(safe-area-inset-top,0px)) 0 8px;flex-shrink:0}
  #xpChooser .xp-band:last-child{margin:10px 0 calc(10px + env(safe-area-inset-bottom,0px))}
  #xpChooser .xp-head{padding:4px 20px 0}
  #xpChooser h2{font-size:32px}
  #xpChooser .xp-head p{font-size:15px}
  #xpChooser .xp-opts{grid-template-columns:1fr;margin:14px 14px 4px}
  #xpChooser .xp-opt{padding:20px 20px 22px;min-height:calc(50dvh - 60px)}
  #xpChooser .xp-lib{border-left:0;border-top:2px solid var(--b)}
  html[dir="rtl"] #xpChooser .xp-lib{border-right:0}
  #xpChooser h3{font-size:27px}
  #xpChooser .xp-ico{width:52px;height:52px}
}
@media(prefers-reduced-motion:reduce){#xpChooser,#xpChooser .xp-card{transition:none}}
</style>
<script>
(function(){
  var KEY = 'ots_xp_chosen';
  function get(){ try{ return localStorage.getItem(KEY); }catch(e){ return null; } }
  function set(v){ try{ localStorage.setItem(KEY, v); }catch(e){} }
  var box = function(){ return document.getElementById('xpChooser'); };
  window.openXpChooser = function(){
    try{ if(window.pauseWelcomeCountdown) window.pauseWelcomeCountdown(); }catch(e){}
    if(get()){ window.dismissWelcome(); return; }          /* returning visitor: straight in */
    var c = box(); if(!c){ window.dismissWelcome(); return; }
    c.hidden = false; requestAnimationFrame(function(){ c.classList.add('on'); });
    setTimeout(function(){ var b = c.querySelector('.xp-cta'); if(b) try{ b.focus({preventScroll:true}); }catch(e){} }, 380);
  };
  window.chooseXp = function(which){
    set(which); var c = box();
    if(c){ c.classList.remove('on'); setTimeout(function(){ c.hidden = true; }, 360); }
    if(which === 'lib'){
      window.__bookOpening = true;                          /* the opener and the tour stay closed for the library */
      window.dismissWelcome();
      setTimeout(function(){ try{ window.openBook(null); }catch(e){} window.__bookOpening = false; }, 380);
    } else window.dismissWelcome();
  };
  document.addEventListener('keydown', function(e){ var c = box(); if(e.key === 'Escape' && c && !c.hidden) window.chooseXp('sim'); });
})();
</script>
'''
swap('<div id="glossTip"></div>', CSS + '<div id="glossTip"></div>')

# ---------------------------------------------------------------- translations
ES = {
 'Enter Simulation': 'Entrar a la simulación',
 'What the record shows': 'Lo que muestra el registro',
 '51 years': '51 años', '37 years': '37 años', 'Overruled': 'Desautorizados',
 'Recognition took eleven minutes on May 14, 1948. The structure behind it took 51 years to build.':
   'El reconocimiento tomó once minutos el 14 de mayo de 1948. La estructura que lo hizo posible tardó 51 años en construirse.',
 "Herzl's program, the Balfour Declaration and the League of Nations Mandate all came before Hitler took power.":
   'El programa de Herzl, la Declaración Balfour y el Mandato de la Sociedad de Naciones llegaron antes de que Hitler tomara el poder.',
 "People counted by Britain's own 1922 census of Palestine — about 11% Jewish.":
   'Personas contadas por el propio censo británico de Palestina de 1922, cerca del 11 % judías.',
 'The Secretary of State, the Pentagon and the new CIA opposed recognition in writing.':
   'El secretario de Estado, el Pentágono y la recién creada CIA se opusieron por escrito al reconocimiento.',
 'NEW: The Library.': 'NUEVO: La Biblioteca.',
 'Read the record as books. Volumes I–III are ready.': 'Lee el registro como libros. Los volúmenes I–III ya están listos.',
 'Also: Eleven Minutes · Español · العربية · 📊 dashboards · 🗺️ architecture maps · 💻 the machine in code — tap ➕':
   'Además: Once minutos · Español · العربية · 📊 paneles · 🗺️ mapas de la arquitectura · 💻 la máquina en código — toca ➕',
 'Follow the work': 'Sigue el trabajo',
 'The Israel Architecture': 'La Arquitectura de Israel',
 'Choose how to explore': 'Elige cómo explorar',
 'Both hold the same documented record, with every claim tied to its source.':
   'Ambas contienen el mismo registro documentado, con cada afirmación vinculada a su fuente.',
 'The Simulation': 'La simulación', 'Walk it scene by scene': 'Recórrelo escena por escena',
 'Every chapter as interactive scenes. Tap any person, document or event to see who they are, how they connect, and the source behind it.':
   'Cada capítulo en escenas interactivas. Toca cualquier persona, documento o evento para ver quién es, cómo se conecta y la fuente que lo respalda.',
 'Opens with a short introduction and a guided tour.': 'Empieza con una breve introducción y una visita guiada.',
 'Enter the Simulation': 'Entrar a la simulación',
 'The Library': 'La Biblioteca', 'Read it as books': 'Léelo como libros',
 'The same record, told in order as volumes, with every claim footnoted. Each chapter becomes its own volume.':
   'El mismo registro, contado en orden como volúmenes, con cada afirmación anotada. Cada capítulo se convierte en su propio volumen.',
 'Ready now: The Baseline · The Road to 1948 · The Cold War Architecture':
   'Ya disponibles (en inglés): The Baseline · The Road to 1948 · The Cold War Architecture',
 'Open the Library': 'Abrir la Biblioteca',
 'You can switch between the two at any time from the ＋ button.': 'Puedes cambiar entre las dos en cualquier momento desde el botón ＋.',
}
AR = {
 'Enter Simulation': 'ادخل المحاكاة',
 'What the record shows': 'ما يُظهره السجل',
 '51 years': '51 عامًا', '37 years': '37 عامًا', 'Overruled': 'تجاوُز الاعتراضات',
 'Recognition took eleven minutes on May 14, 1948. The structure behind it took 51 years to build.':
   'استغرق الاعتراف إحدى عشرة دقيقة في 14 مايو 1948، أما البنية التي تقف خلفه فقد استغرق بناؤها 51 عامًا.',
 "Herzl's program, the Balfour Declaration and the League of Nations Mandate all came before Hitler took power.":
   'جاء برنامج هرتسل ووعد بلفور وانتداب عصبة الأمم كلها قبل وصول هتلر إلى السلطة.',
 "People counted by Britain's own 1922 census of Palestine — about 11% Jewish.":
   'عدد السكان في إحصاء بريطانيا نفسها لفلسطين عام 1922، نحو 11% منهم يهود.',
 'The Secretary of State, the Pentagon and the new CIA opposed recognition in writing.':
   'عارض وزير الخارجية والبنتاغون ووكالة المخابرات المركزية الناشئة الاعترافَ كتابةً.',
 'NEW: The Library.': 'جديد: المكتبة.',
 'Read the record as books. Volumes I–III are ready.': 'اقرأ السجل في كتب. المجلدات من الأول إلى الثالث جاهزة.',
 'Also: Eleven Minutes · Español · العربية · 📊 dashboards · 🗺️ architecture maps · 💻 the machine in code — tap ➕':
   'أيضًا: إحدى عشرة دقيقة · Español · العربية · 📊 لوحات بيانات · 🗺️ خرائط البنية · 💻 الآلة في شيفرة — اضغط ➕',
 'Follow the work': 'تابع العمل',
 'The Israel Architecture': 'بنية إسرائيل',
 'Choose how to explore': 'اختر طريقة الاستكشاف',
 'Both hold the same documented record, with every claim tied to its source.':
   'كلاهما يحمل السجل الموثّق نفسه، وكل ادعاء فيه مربوط بمصدره.',
 'The Simulation': 'المحاكاة', 'Walk it scene by scene': 'تتبّعه مشهدًا بمشهد',
 'Every chapter as interactive scenes. Tap any person, document or event to see who they are, how they connect, and the source behind it.':
   'كل فصل في مشاهد تفاعلية. اضغط على أي شخص أو وثيقة أو حدث لترى من هو، وكيف يرتبط، والمصدر الذي يستند إليه.',
 'Opens with a short introduction and a guided tour.': 'تبدأ بمقدمة قصيرة وجولة إرشادية.',
 'Enter the Simulation': 'ادخل المحاكاة',
 'The Library': 'المكتبة', 'Read it as books': 'اقرأه في كتب',
 'The same record, told in order as volumes, with every claim footnoted. Each chapter becomes its own volume.':
   'السجل نفسه مرويًّا بالترتيب في مجلدات، وكل ادعاء موثّق بحاشية. يصبح كل فصل مجلدًا قائمًا بذاته.',
 'Ready now: The Baseline · The Road to 1948 · The Cold War Architecture':
   'متاح الآن (بالإنجليزية): The Baseline · The Road to 1948 · The Cold War Architecture',
 'Open the Library': 'افتح المكتبة',
 'You can switch between the two at any time from the ＋ button.': 'يمكنك التبديل بينهما في أي وقت من زر ＋.',
}
for lang, add in (('es', ES), ('ar', AR)):
    m = re.search(r'(<script type="application/json" id="i18n-%s">)(.*?)(</script>)' % lang, s, re.S)
    d = json.loads(m.group(2))
    for k, v in add.items(): d['ui'].setdefault(k, v)
    txt = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + txt + s[m.end(2):]

open(P, 'w', encoding='utf-8').write(s)
print('welcome v2 applied; %d Spanish and %d Arabic strings added' % (len(ES), len(AR)))
