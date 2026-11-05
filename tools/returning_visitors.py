#!/usr/bin/env python3
"""Returning visitors skip the welcome screen; anyone can reopen it from the + menu (index.html).

- The welcome screen shows on a first visit only. Once a visitor has gone past it (or picked
  Simulation/Library in the chooser), later visits open straight into their view; a style in <head>
  hides the welcome screen before it can paint, so it never flashes.
- + > Help and more > "The welcome briefing" brings it back, rain and all; its red pill closes it again.
Run after tools/simplify_ux.py. Idempotent. Usage: python3 tools/returning_visitors.py [index.html]"""
import re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '<!--RETURN-START-->' in s:
    print('returning-visitor welcome already applied'); sys.exit(0)

def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('not found exactly %d time(s): ' % count) + old[:100]
    s = s.replace(old, new)

HEAD = ('<!--RETURN-START--><script>try{if(localStorage.getItem("ots_welcome_seen")||localStorage.getItem("ots_xp_chosen"))'
        'document.documentElement.classList.add("ots-skip-welcome");}catch(e){}</script>'
        '<style>html.ots-skip-welcome #welcomeOverlay{display:none !important}</style><!--RETURN-END-->')
m = re.search(r'<head[^>]*>', s)
s = s[:m.end()] + HEAD + s[m.end():]

swap('''  var dismissed = false;
  function dismiss(){
    if(dismissed) return;
    dismissed = true;''',
'''  var dismissed = false;
  function dismiss(){
    if(dismissed) return;
    dismissed = true;
    try{ localStorage.setItem('ots_welcome_seen', '1'); }catch(e){}''')

swap('''  window.dismissWelcome = dismiss;
})();''',
'''  window.dismissWelcome = dismiss;

  /* returning visitors: the welcome screen is hidden from the first paint (<!--RETURN--> in <head>);
     go past it as if the red pill had been pressed, once every script has wrapped dismissWelcome */
  if(document.documentElement.classList.contains('ots-skip-welcome')){
    document.addEventListener('DOMContentLoaded', function(){ try{ window.dismissWelcome(); }catch(e){} });
  }
  /* + > The welcome briefing: bring the screen back; its red pill closes it as before */
  var welcomeNode = document.getElementById('welcomeOverlay'), welcomeHome = welcomeNode && welcomeNode.parentNode;
  window.__welcomeReopen = function(){
    if(!welcomeNode || (document.getElementById('welcomeOverlay') && !dismissed)) return;
    document.documentElement.classList.remove('ots-skip-welcome');
    welcomeNode.classList.remove('fade-out'); welcomeNode.style.display = '';
    if(!welcomeNode.parentNode) (welcomeHome || document.body).appendChild(welcomeNode);
    welcomeNode.scrollTop = 0; dismissed = false;
    clearInterval(matrixTimer); matrixTimer = setInterval(drawMatrix, 45);
    try{ var b = document.getElementById('enterSimBtn'); if(b) b.focus({preventScroll:true}); }catch(e){}
  };
})();''')

open(P, 'w', encoding='utf-8').write(s)
print('returning-visitor welcome applied')
