#!/usr/bin/env python3
"""First-time visitors, and returning library readers, land straight in the library, with no flash of anything else (index.html).

Before: a reader whose last view was the library saw the welcome screen animate in, then fade out
over the simulation, and only then the library (the library opened on window load + 1.1 s).
After: a tiny script at the top of <head> covers the page in the library's own page color (paper,
sepia or night, from the reader's settings) before anything paints; the library opens as soon as
the document is parsed, the welcome screen is skipped without its fade, and the cover lifts once the
library is showing. Links to a scene, dashboard, map or #11minutes still win, as before.
Idempotent. Usage: python3 tools/library_boot.py [index.html]"""
import re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '<!--LIBBOOT-START-->' in s:
    print('library boot already applied'); sys.exit(0)

def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('not found exactly %d time(s): ' % count) + old[:100]
    s = s.replace(old, new)

HEAD = ('<!--LIBBOOT-START--><script>(function(){try{'
        "var v=JSON.parse(localStorage.getItem('ots_view')||'null');"
        "var h=location.hash||'',deep=/^#(book|library)/.test(h);if(window.parent!==window||(!deep&&((v!=='library'&&v!==null)||h.replace('#',''))))return;"
        "var p=JSON.parse(localStorage.getItem('ots_book_prefs')||'null')||{};"
        "var bg={sepia:'#F5EBD7',night:'#121212'}[p.theme]||'#FBF9F4',ink=p.theme==='night'?'#E6E2DA':'#1C1B19',mu=p.theme==='night'?'#A39E94':'#6B655B';"
        "var d=document.documentElement;d.classList.add('ots-lib-boot');d.style.setProperty('--ots-boot-bg',bg);d.style.setProperty('--ots-boot-ink',ink);d.style.setProperty('--ots-boot-mu',mu);"
        # the loading screen: what is on the shelves, and a moving bar so it never looks stuck
        "var L=['The Israel \\u{1F1EE}\\u{1F1F1} Architecture','The USA \\u{1F1FA}\\u{1F1F8} vs Israel \\u{1F1EE}\\u{1F1F1} System','The American Dream Architecture','The Vatican \\u{1F1FB}\\u{1F1E6} Architecture','The Dark Enlightenment Architecture'];"
        "function add(){if(!document.body||document.getElementById('otsBoot'))return !!document.body;var x=document.createElement('div');x.id='otsBoot';x.setAttribute('role','status');x.setAttribute('aria-live','polite');"
        "x.innerHTML='<div class=\"ob-in\"><div class=\"ob-k\">Observe The System</div><div class=\"ob-h\">Opening the library</div><div class=\"ob-bar\"><i></i></div><div class=\"ob-l\">On the shelves</div><ul>'+L.map(function(s){return '<li>'+s+'</li>';}).join('')+'</ul></div>';"
        "document.body.insertBefore(x,document.body.firstChild);return true;}"
        "if(!add()){var mo=new MutationObserver(function(){if(add())mo.disconnect();});mo.observe(d,{childList:true,subtree:true});}"
        "window.__otsBootOff=function(){d.classList.remove('ots-lib-boot');var x=document.getElementById('otsBoot');if(x){x.classList.add('out');setTimeout(function(){if(x.parentNode)x.parentNode.removeChild(x);},380);}};"
        "setTimeout(window.__otsBootOff,12000);"   # never leave a reader stuck behind the cover
        '}catch(e){}})();</script>'
        '<style>html.ots-lib-boot,html.ots-lib-boot body{background:var(--ots-boot-bg,#FBF9F4) !important}'
        "html.ots-lib-boot body::before{content:'';position:fixed;inset:0;z-index:2147483646;background:var(--ots-boot-bg,#FBF9F4)}"
        "#otsBoot{position:fixed;inset:0;z-index:2147483647;background:var(--ots-boot-bg,#FBF9F4);color:var(--ots-boot-ink,#1C1B19);display:flex;align-items:center;justify-content:center;padding:24px 16px;font-family:Georgia,'Times New Roman',serif;transition:opacity .35s}"
        "#otsBoot.out{opacity:0;pointer-events:none}"
        "#otsBoot .ob-in{max-width:340px;width:100%;text-align:center}"
        "#otsBoot .ob-k{font-size:12px;letter-spacing:.2em;font-variant:small-caps;color:var(--ots-boot-mu,#6B655B)}"
        "#otsBoot .ob-h{font-size:26px;line-height:1.25;margin:6px 0 18px;font-weight:600}"
        "#otsBoot .ob-bar{height:3px;border-radius:3px;background:rgba(138,45,31,.15);overflow:hidden;margin:0 auto 26px;width:72%}"
        "#otsBoot .ob-bar i{display:block;height:100%;width:38%;border-radius:3px;background:#B8862B;animation:obslide 1.3s ease-in-out infinite}"
        "@keyframes obslide{0%{transform:translateX(-105%)}100%{transform:translateX(270%)}}"
        "@media (prefers-reduced-motion:reduce){#otsBoot .ob-bar i{animation-duration:3s}}"
        "#otsBoot .ob-l{font-size:12px;letter-spacing:.16em;font-variant:small-caps;color:var(--ots-boot-mu,#6B655B);margin:0 0 10px}"
        "#otsBoot ul{list-style:none;margin:0;padding:0}"
        "#otsBoot li{font-size:17px;line-height:1.35;padding:7px 0;border-top:1px solid rgba(127,120,108,.22)}"
        "#otsBoot li:last-child{border-bottom:1px solid rgba(127,120,108,.22)}"
        "#otsBoot li{opacity:0;animation:obin .45s ease forwards}"
        "#otsBoot li:nth-child(2){animation-delay:.12s}#otsBoot li:nth-child(3){animation-delay:.24s}#otsBoot li:nth-child(4){animation-delay:.36s}#otsBoot li:nth-child(5){animation-delay:.48s}"
        "@keyframes obin{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}</style>"
        '<!--LIBBOOT-END-->')
m = re.search(r'<head[^>]*>', s)
s = s[:m.end()] + HEAD + s[m.end():]

swap('''  window.addEventListener('load', function(){ setTimeout(function(){
    if(ls('ots_view') !== 'library' || view.classList.contains('on')) return;
    if((location.hash || '').replace('#', '')) return;
    var ev = $('elevenOverlay'); if(ev && !ev.hidden) return;
    try{ if(window.parent !== window && (window.parent.__bookRoute || window.parent.__elevenRoute)) return; }catch(e){}
    window.__bookOpening = true; try{ if(shown($('welcomeOverlay')) && window.dismissWelcome) window.dismissWelcome(); }catch(e){}
    setTimeout(function(){ window.__bookOpening = false; openBook(null); }, 450);
  }, 650); });''',
'''  /* opens as soon as the page is parsed; the cover from <!--LIBBOOT--> hides everything until the library shows */
  function libBootDone(){ requestAnimationFrame(function(){ requestAnimationFrame(function(){ if(window.__otsBootOff) window.__otsBootOff(); else document.documentElement.classList.remove('ots-lib-boot'); }); }); }
  function libBoot(){
    if(/^#(book|library)/.test(location.hash || '')){ try{ deepEntry(); }catch(e){} return libBootDone(); }   /* a link into the library or a book opens it under the cover */
    var v0 = ls('ots_view'); if((v0 !== 'library' && v0 != null) || view.classList.contains('on')) return libBootDone();   /* first visit (no view yet) lands in the library too */
    if((location.hash || '').replace('#', '')) return libBootDone();
    var ev = $('elevenOverlay'); if(ev && !ev.hidden) return libBootDone();
    try{ if(window.parent !== window && (window.parent.__bookRoute || window.parent.__elevenRoute)) return libBootDone(); }catch(e){}
    window.__bookOpening = true;
    try{ var w = $('welcomeOverlay'); if(shown(w) && window.dismissWelcome){ window.dismissWelcome(); w.style.display = 'none'; } }catch(e){}
    window.__bookOpening = false;
    bootOpen = true; try{ openBook(null); }catch(e){} bootOpen = false;
    libBootDone();
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(libBoot, 0); });
  else setTimeout(libBoot, 0);''')

open(P, 'w', encoding='utf-8').write(s)
print('library boot applied')
