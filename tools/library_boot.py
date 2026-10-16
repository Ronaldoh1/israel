#!/usr/bin/env python3
"""Returning library readers land straight in the library, with no flash of anything else (index.html).

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
        "if(v!=='library'||(location.hash||'').replace('#','')||window.parent!==window)return;"
        "var p=JSON.parse(localStorage.getItem('ots_book_prefs')||'null')||{};"
        "var bg={sepia:'#E9DABF',night:'#141519'}[p.theme]||'#F3EDE1';"
        "var d=document.documentElement;d.classList.add('ots-lib-boot');d.style.setProperty('--ots-boot-bg',bg);"
        "setTimeout(function(){d.classList.remove('ots-lib-boot');},8000);"   # never leave a reader stuck behind the cover
        '}catch(e){}})();</script>'
        '<style>html.ots-lib-boot,html.ots-lib-boot body{background:var(--ots-boot-bg,#F3EDE1) !important}'
        "html.ots-lib-boot body::before{content:'';position:fixed;inset:0;z-index:2147483647;background:var(--ots-boot-bg,#F3EDE1)}</style>"
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
  function libBootDone(){ requestAnimationFrame(function(){ requestAnimationFrame(function(){ document.documentElement.classList.remove('ots-lib-boot'); }); }); }
  function libBoot(){
    if(ls('ots_view') !== 'library' || view.classList.contains('on')) return libBootDone();
    if((location.hash || '').replace('#', '')) return libBootDone();
    var ev = $('elevenOverlay'); if(ev && !ev.hidden) return libBootDone();
    try{ if(window.parent !== window && (window.parent.__bookRoute || window.parent.__elevenRoute)) return libBootDone(); }catch(e){}
    window.__bookOpening = true;
    try{ var w = $('welcomeOverlay'); if(shown(w) && window.dismissWelcome){ window.dismissWelcome(); w.style.display = 'none'; } }catch(e){}
    window.__bookOpening = false;
    try{ openBook(null); }catch(e){}
    libBootDone();
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(libBoot, 0); });
  else setTimeout(libBoot, 0);''')

open(P, 'w', encoding='utf-8').write(s)
print('library boot applied')
