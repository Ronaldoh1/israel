#!/usr/bin/env python3
"""Back-button guard for the network map pages (road-network.html, epstein-network.html). Each map is its own URL and
opens in the same window from the library. When the reader presses the browser's Back button on a map, a small dialog
asks whether to leave the map and go back to the library; "Stay" keeps them on the map. Idempotent.
Usage: python3 tools/patch_map_back_guard.py [page.html ...]"""
import sys
PAGES = sys.argv[1:] or ['road-network.html', 'epstein-network.html']
BLOCK = r'''<!-- back-button guard: ask before leaving the map for the library -->
<style>
.mbg{position:fixed;inset:0;z-index:9999;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(6,11,23,.62)}
.mbg.on{display:flex}
.mbg-box{width:min(380px,100%);border-radius:16px;padding:20px 20px 16px;background:#0E182C;color:#EAEEF7;border:1px solid #C9912B;box-shadow:0 24px 60px rgba(0,0,0,.55);font:15px/1.5 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
.mbg-box h2{font:600 21px/1.25 "Fraunces",Georgia,serif;margin:0 0 6px}
.mbg-box p{margin:0 0 16px;color:#B6C0D2}
.mbg-row{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}
.mbg-row button{min-height:44px;padding:10px 16px;border-radius:999px;font:600 15px/1 inherit;cursor:pointer}
.mbg-stay{background:transparent;color:#EAEEF7;border:1px solid #3B5075}
.mbg-go{background:#F0C040;color:#1A1204;border:0}
.mbg-row button:focus-visible{outline:2px solid #F0C040;outline-offset:2px}
</style>
<div class="mbg" id="mbg" role="dialog" aria-modal="true" aria-labelledby="mbgT" aria-describedby="mbgB">
  <div class="mbg-box"><h2 id="mbgT">Leave the map?</h2><p id="mbgB">You'll go back to the Library of Truth. Your place on the map isn't kept.</p>
  <div class="mbg-row"><button class="mbg-stay" type="button" id="mbgStay">Stay on the map</button><button class="mbg-go" type="button" id="mbgGo">Go to the library</button></div></div>
</div>
<script>
(function(){
  var box = document.getElementById('mbg'), leaving = false, last = null;
  var LIB = 'index.html#library';
  function fromLibrary(){ try{ var r = document.referrer ? new URL(document.referrer) : null; return !!(r && r.origin === location.origin && /(^|\/)(index\.html)?$/.test(r.pathname)); }catch(e){ return false; } }
  try{ if(!history.state || !history.state.mapGuard) history.pushState({mapGuard: 1}, '', location.href); }catch(e){}
  function open(){ last = document.activeElement; box.classList.add('on'); setTimeout(function(){ document.getElementById('mbgGo').focus(); }, 30); }
  function close(){ box.classList.remove('on'); try{ history.pushState({mapGuard: 1}, '', location.href); }catch(e){} if(last && last.focus) try{ last.focus(); }catch(e){} }
  window.addEventListener('popstate', function(){ if(leaving) return; open(); });
  document.getElementById('mbgStay').addEventListener('click', close);
  document.getElementById('mbgGo').addEventListener('click', function(){ leaving = true; box.classList.remove('on'); if(fromLibrary()) history.back(); else location.href = LIB; });
  box.addEventListener('click', function(e){ if(e.target === box) close(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && box.classList.contains('on')) close(); });
})();
</script>
'''
for P in PAGES:
    s = open(P, encoding='utf-8').read()
    if 'id="mbg"' in s: print(P, 'already patched'); continue
    i = s.rindex('</body>') if '</body>' in s else s.rindex('</html>')
    s = s[:i] + BLOCK + s[i:]
    open(P, 'w', encoding='utf-8').write(s)
    print(P, 'back guard added')
