#!/usr/bin/env python3
"""The "Four Words" dashboard (Hebrew, Jewish, Israeli, Zionist) in the simulation (index.html).

- Adds a "venn" panel type to the simulation's dashboard renderer (the library's renderer, tools/charts.js,
  has its own copy), with its styles.
- Adds the dashboard from book/src/four_words_dashboard.json to window.DASHBOARDS and links it from the
  scenes listed in that file's "scenes", so the scene's dashboard button opens it.
Idempotent. Run after embed_book.py, before simplify_ux.py. Usage: python3 tools/patch_four_words.py [index.html]"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '"four_words":' in s.split('window.DASHBOARDS = ', 1)[1][:200]:
    print('four words dashboard already applied'); sys.exit(0)

def swap(old, new, count=1):
    global s
    assert s.count(old) == count, ('found %d time(s), expected %d: ' % (s.count(old), count)) + old[:110]
    s = s.replace(old, new)

VENN = r'''function venn(s){ var Sx=(s.sets||[]).slice(0,3),G=s.regions||[],r=108,C=[[148,150],[252,150],[200,240]],P={a:[100,118],b:[300,118],c:[200,300],ab:[200,104],ac:[146,214],bc:[254,214],abc:[200,178]},LP=[[96,28],[304,28],[200,376]];
  var o='<svg viewBox="0 0 400 384" role="img" aria-label="'+esc(s.title||'Venn diagram')+'">';
  Sx.forEach(function(x,i){ o+='<circle class="dp-rise" cx="'+C[i][0]+'" cy="'+C[i][1]+'" r="'+r+'" fill="'+x[1]+'" fill-opacity=".16" stroke="'+x[1]+'" stroke-width="3"/>'; });
  Sx.forEach(function(x,i){ o+='<text x="'+LP[i][0]+'" y="'+LP[i][1]+'" text-anchor="middle" font-size="18" font-weight="800" fill="'+x[1]+'">'+esc(x[0])+'</text>'; });
  G.forEach(function(g,k){ var p=P[g.at]; if(!p) return; o+='<circle cx="'+p[0]+'" cy="'+p[1]+'" r="15" fill="'+NAVY+'"/><text x="'+p[0]+'" y="'+(p[1]+6)+'" text-anchor="middle" font-size="16" font-weight="900" fill="#FFC700">'+(k+1)+'</text>'; });
  o+='</svg><ol class="dp-venn">'+G.map(function(g,k){ return '<li><i>'+(k+1)+'</i><span><b>'+esc(g.who)+'</b>'+(g.ex?'<br>'+esc(g.ex):'')+'</span></li>'; }).join('')+'</ol>';
  return o+(s.note?'<p class="dp-cap" style="margin-top:10px">'+esc(s.note)+'</p>':''); }
var R={hbar:hbar,stacked:stacked,donut:donut,line:line,flow:flow,table:table,pair:pair,venn:venn};'''
swap("var R={hbar:hbar,stacked:stacked,donut:donut,line:line,flow:flow,table:table,pair:pair};", VENN)
swap("#dashPage .dp-cap{", "#dashPage .dp-venn{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:10px}#dashPage .dp-venn li{display:flex;gap:10px;align-items:flex-start;font-size:14px;line-height:1.45;color:#2B3A5A}#dashPage .dp-venn i{flex:none;width:26px;height:26px;border-radius:50%;background:#1B2A4A;color:#FFC700;font:900 13px/26px system-ui;text-align:center;font-style:normal}#dashPage .dp-venn b{color:#1B2A4A}#dashPage .dp-card svg{max-width:440px;display:block;margin:0 auto}\n#dashPage .dp-cap{")

D = json.load(open(os.path.join(ROOT, 'book', 'src', 'four_words_dashboard.json'), encoding='utf-8'))
scenes = D.pop('scenes', [])
payload = json.dumps(D, ensure_ascii=False).replace('</', '<\\/')
swap('window.DASHBOARDS = {', 'window.DASHBOARDS = {"four_words": ' + payload + ', ')
for sid in scenes:
    assert ('"id":"%s"' % sid) in s, 'unknown scene ' + sid
swap('window.DASH_SCENES = {', 'window.DASH_SCENES = {' + ''.join('"%s": "four_words", ' % x for x in scenes))

open(P, 'w', encoding='utf-8').write(s)
print('four words dashboard applied (linked from %d scenes)' % len(scenes))
