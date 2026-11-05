"""Embed "Eleven Minutes" into the Israel simulation (index.html). Idempotent: replaces its own block.
Shown once, right after the landing modal is dismissed (English only; skipped for #scene/#dash/#map deep links).
Also opens on #11minutes. Its "Go deeper" links close the overlay and jump to that scene.
Usage: python3 eleven_patch.py <index.html> <11-minutes.html>"""
import json, re, sys
IDX = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/israel/index.html'
SRC = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/el26/eleven/11-minutes.html'
s = open(IDX, encoding='utf-8').read()
html = open(SRC, encoding='utf-8').read()
payload = json.dumps(html, ensure_ascii=False).replace('</', '<\\/')

BLOCK = '''<!--ELEVEN-START-->
<style>
#elevenOverlay{position:fixed;inset:0;z-index:2147483000;background:#121A2B;opacity:0;transition:opacity .45s}
#elevenOverlay.on{opacity:1}
#elevenOverlay[hidden]{display:none}
#elevenOverlay iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:#121A2B}
</style>
<div id="elevenOverlay" hidden role="dialog" aria-modal="true" aria-label="Eleven Minutes"><iframe title="Eleven Minutes"></iframe></div>
<script type="application/json" id="eleven_html">''' + payload + '''</script>
<script>
(function(){
  var KEY = 'ots_11min_seen', ov = document.getElementById('elevenOverlay'), fr = ov.querySelector('iframe');
  function seen(){ try{ return localStorage.getItem(KEY) === '1'; }catch(e){ return false; } }
  function mark(){ try{ localStorage.setItem(KEY, '1'); }catch(e){} }
  window.__eleven = {
    open: function(){
      if(!ov.hidden) return;
      fr.srcdoc = JSON.parse(document.getElementById('eleven_html').textContent);
      ov.hidden = false; requestAnimationFrame(function(){ ov.classList.add('on'); });
      document.documentElement.style.overflow = 'hidden';
      setTimeout(function(){ try{ fr.focus(); }catch(e){} }, 300);
    },
    close: function(sceneId){
      mark(); ov.classList.remove('on'); document.documentElement.style.overflow = '';
      setTimeout(function(){ ov.hidden = true; fr.removeAttribute('srcdoc'); fr.src = 'about:blank'; }, 450);
      if(location.hash === '#11minutes'){ try{ history.replaceState(null, '', location.pathname + location.search); }catch(e){} }
      if(sceneId){ try{ history.replaceState(null, '', location.pathname + location.search + '#scene=' + sceneId); }catch(e){} if(window.routeFromHash) window.routeFromHash(false); }
    }
  };
  function deepLinked(){ return /^#(scene=|dash=|map=|book)/.test(location.hash || '') || !!window.__bookOpening || !!(window.parent !== window && window.parent.__bookRoute); }
  function english(){ var l = (document.documentElement.lang || 'en').toLowerCase(); return l.indexOf('es') !== 0 && l.indexOf('ar') !== 0 && !/lang=(es|ar)/.test(location.hash || ''); }
  var prev = window.dismissWelcome;
  if(typeof prev === 'function'){
    window.dismissWelcome = function(){
      var r = prev.apply(this, arguments);
      if(!deepLinked() && (location.hash === '#11minutes' || (!seen() && english()))) setTimeout(window.__eleven.open, 420);
      return r;
    };
  }
  function fromHash(){ if(location.hash === '#11minutes'){ try{ if(typeof window.dismissWelcome === 'function' && document.getElementById('welcomeOverlay') && getComputedStyle(document.getElementById('welcomeOverlay')).display !== 'none') window.dismissWelcome(); }catch(e){} window.__eleven.open(); } }
  window.addEventListener('hashchange', fromHash);
  /* Sophia's "Eleven Minutes" slide sets parent.__elevenRoute before opening the simulation. */
  function fromParent(){ try{ if(window.parent !== window && window.parent.__elevenRoute){ window.parent.__elevenRoute = false;
    var w = document.getElementById('welcomeOverlay');
    if(typeof window.dismissWelcome === 'function' && w && getComputedStyle(w).display !== 'none') window.dismissWelcome();
    window.__eleven.open(); } }catch(e){} }
  window.addEventListener('load', function(){ setTimeout(fromHash, 500); setTimeout(fromParent, 600); });
})();
</script>
<!--ELEVEN-END-->
'''
s = re.sub(r'<!--ELEVEN-START-->.*?<!--ELEVEN-END-->\n?', '', s, flags=re.S)
i = s.rfind('</body>')
assert i > 0
s = s[:i] + BLOCK + s[i:]
open(IDX, 'w', encoding='utf-8').write(s)
print('embedded', len(html), 'bytes ->', IDX)
