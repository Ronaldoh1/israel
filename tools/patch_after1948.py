#!/usr/bin/env python3
"""Adds the after-1948 layer to the Road to 1948 network map (book/plan/road_map/after1948_layer.json):
nodes and ties from the founding to 2026, drawn in red; a Years switch (Up to 1948 / Both / After 1948);
and "What followed", the downstream tests for the seventh link of the case. The founding model (the chances
of a state in 1948) is not touched: the layer adds no weighted ties. Idempotent; run after restore_model.py.

Usage: python3 tools/patch_after1948.py [road-network.html]"""
import json, os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
L = json.load(open(os.path.join(ROOT, 'book', 'plan', 'road_map', 'after1948_layer.json'), encoding='utf-8'))

# source index: research files, then the simulation's citation data
IDX = {}
def walk(x):
    if isinstance(x, dict):
        if 'key' in x and 'url' in x: IDX.setdefault(x['key'], (x['url'], x.get('label', '')))
        for v in x.values(): walk(v)
    elif isinstance(x, list):
        for v in x: walk(v)
rd = os.path.join(ROOT, 'book', 'research')
for f in sorted(os.listdir(rd)):
    if f.endswith('.json'):
        try: walk(json.load(open(os.path.join(rd, f), encoding='utf-8')))
        except Exception: pass
ix = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
m = re.search(r'<script id="citationdata" type="application/json">(.*?)</script>', ix, re.S)
CI = json.loads(m.group(1))
m = re.search(r'window\.CITE_LABELS = (\{.*?\});\n', ix, re.S)
CL = json.loads(m.group(1)) if m else {}
for k, u in CI.items(): IDX.setdefault(k, (u, CL.get(k, k)))
def refs(keys):
    out = []
    for k in keys:
        assert k in IDX, 'unknown source key ' + k
        u, t = IDX[k]; out.append({'t': t or k, 'u': u})
    return out

s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if D.get('after1948'):
    print('after-1948 layer already applied'); sys.exit(0)

byid = {n['id']: n for n in D['nodes']}
year = {}
for (i, name, kind, cl, y, note, cites) in L['nodes']:
    n = {'id': i, 'name': name, 'kind': kind, 'cluster': cl, 'note': note, 'year': y, 'era': 'after' if y > 1948 else 'before', 'refs': refs(cites)}
    if i in byid: byid[i].update({k2: v for k2, v in n.items() if k2 not in ('name',)})
    else: D['nodes'].append(n); byid[i] = n
    year[i] = y
for i, y in L['existing_after'].items():
    byid[i]['era'] = 'after'; byid[i]['year'] = y; year[i] = y
TYPE = {'cause': 'led to'}
fol = []
for (f, t, kind, label, cites, need) in L['ties']:
    assert f in byid and t in byid, (f, t)
    D['edges'].append({'f': f, 't': t, 'label': label, 'type': TYPE.get(kind, kind), 'status': 'verified', 'src': cites[0] if cites else '',
                       'refs': refs(cites), 'n': 1, 'sec': '', 'era': 'after'})
    yf, yt = year.get(f, 1948), year.get(t, 1948)
    if byid[t]['kind'] != 'person' and yf <= yt: fol.append([f, t, 1 if need else 0])
after = [i for i in byid if byid[i].get('era') == 'after']
D['follow'] = {'edges': fol, 'after': after}
D['after1948'] = True
s = s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]

def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)

if 'const FOL=' in s:   # the page code is already in place (a rebuild replaced only the data)
    open(P, 'w', encoding='utf-8').write(s)
    print('after-1948 data restored on a rebuilt page'); sys.exit(0)

# colours: one red for everything after the founding, in both themes
rep('--k-event:#e6c25a;', '--k-event:#e6c25a; --after:#ff6b5e;')
s = re.sub(r'--k-event:#8a6a0a;(?! --after)', '--k-event:#8a6a0a; --after:#c62828;', s)
rep("panel:css('--panel'),gold:css('--gold')}); }", "panel:css('--panel'),gold:css('--gold'),after:css('--after')}); }")
rep("const kc = id => C[KINDS.includes(N.get(id).kind)?N.get(id).kind:'place'];",
    "const kc = id => N.get(id).era==='after'?C.after:C[KINDS.includes(N.get(id).kind)?N.get(id).kind:'place'];")
rep("return hiEdges.has(d.i)?C.hi: rem(d)?C.nest: s==='verified'?C.line:",
    "return hiEdges.has(d.i)?C.hi: rem(d)?C.nest: E[d.i].era==='after'?C.after: s==='verified'?C.line:")

# the Years switch
rep('<div class="hud"><div class="legend" id="legend"></div>',
    '<div class="hud"><div class="eraSeg" id="eraSeg" role="group" aria-label="Years shown"><button type="button" data-era="before">Up to 1948</button><button type="button" data-era="both" class="on">Both</button><button type="button" data-era="after">After 1948</button></div><div class="brk"></div><div class="legend" id="legend"></div>')
rep('.legend i{', '.hud{flex-wrap:wrap}\n.hud .brk{flex-basis:100%;height:0}\n.eraSeg{pointer-events:auto;display:inline-flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;background:color-mix(in srgb,var(--panel) 88%,transparent);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);margin-bottom:4px;width:max-content;max-width:100%}\n.eraSeg button{font:inherit;font-size:12px;font-weight:600;padding:6px 11px;border:0;background:transparent;color:var(--muted);cursor:pointer;min-height:32px}\n.eraSeg button.on{background:var(--after);color:#fff}\n.eraSeg button[data-era="before"].on{background:var(--gold);color:#1b1b1b}\n.eraSeg button[data-era="both"].on{background:var(--ink,#1B2A4A);color:var(--panel)}\n.eraSeg button:focus-visible{outline:2px solid var(--hi);outline-offset:-2px}\n.legend i{')
rep("function walkable(e,show){ if(e.status==='co-mention') return false;",
    "let ERA='both', AFTER_NB=new Set();\nfunction eraOk(id){ if(ERA==='both') return true; const n=N.get(id); if(!n) return false; return ERA==='before'?n.era!=='after':(n.era==='after'||AFTER_NB.has(id)); }\nfunction walkable(e,show){ if(e.status==='co-mention') return false; if(!eraOk(e.f)||!eraOk(e.t)) return false;")
rep("  const depth=visibleSet(), ids=[...depth.keys()];",
    "  const depth=visibleSet(); [...depth.keys()].forEach(x=>{ if(!eraOk(x)) depth.delete(x); }); const ids=[...depth.keys()];")
rep("$('legend').innerHTML=KINDS.map(k=>`<span><i style=\"background:var(--k-${k})\"></i>${k}</span>`).join('');",
    "$('legend').innerHTML=KINDS.map(k=>`<span><i style=\"background:var(--k-${k})\"></i>${k}</span>`).join('')+`<span><i style=\"background:var(--after)\"></i>after 1948</span>`;\n"
    "E.forEach(e=>{ if(e.era!=='after') return; [e.f,e.t].forEach(x=>{ if(N.get(x)&&N.get(x).era!=='after') AFTER_NB.add(x); }); });\n"
    "function setEra(v){ ERA=v; $('eraSeg').querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.era===v)); if(!eraOk($('root').value)){ $('root').value=v==='after'?'israel_gov':'herzl'; } if(v==='after'){ $('depth').value=5; $('dval').textContent='All'; } expanded.clear(); posCache.clear(); needFit=true; hideCallout(); draw(); }\n"
    "$('eraSeg').addEventListener('click',ev=>{ const b=ev.target.closest('[data-era]'); if(b) setEra(b.dataset.era); });")
# the lede says what the red layer is
rep('from the Bank of England in 1694 to the eve of the June 1967 war.',
    'from the Bank of England in 1694 to the eve of the June 1967 war, and, in red, what followed the founding to 2026: the refugees, the wars, the occupation, the armed movements, the peace plans, the patron and the courts. The switch on the map shows the years up to 1948, after it, or both.')

# What followed: the downstream tests (link 7)
T = r"""const FOL=DATA.follow||{edges:[],after:[]};
function vFollow(rem){ const inc=new Map(), all=new Set();
  FOL.edges.forEach(([f,t,nd])=>{ all.add(f); all.add(t); if(!inc.has(t)) inc.set(t,[]); inc.get(t).push([f,nd]); });
  const alive=new Map([...all].map(x=>[x,!rem.has(x)])); let ch=true;
  while(ch){ ch=false; for(const x of all){ if(!alive.get(x)) continue; const c=inc.get(x); if(!c) continue; if(!c.every(([f,nd])=>!nd||alive.get(f))||!c.some(([f])=>alive.get(f))){ alive.set(x,false); ch=true; } } }
  const later=FOL.after.filter(x=>all.has(x)&&!rem.has(x));
  const lost=later.filter(x=>!alive.get(x)), weak=later.filter(x=>alive.get(x)&&(inc.get(x)||[]).some(([f])=>!alive.get(f)));
  const byY=(a,b)=>(N.get(a).year||0)-(N.get(b).year||0);
  return {lost:lost.sort(byY), weak:weak.sort(byY), n:later.length, keep:later.length-lost.length-weak.length}; }
const VFOLLOW=[
 {id:'f_state', q:'What if no state had been declared in 1948?', rem:['decl_indep'],
  read:'Nearly everything after 1948 on the map loses every documented cause: the refugee question, the occupation and its wars, the peace plans, the American aid and vetoes, the war in Gaza and the cases in court. What keeps a cause is what the record shows growing from roots of its own: the Iranian revolution, rooted in the coup of 1953; the Islamist movement in Gaza, rooted in the Muslim Brotherhood of 1928; and the Shia movement in Lebanon that predates 1982. Hamas and Hezbollah are weakened, not erased: the forms they took, an armed movement against an occupation, do not exist without it.'},
 {id:'f_nakba', q:'What if the state had been founded without the displacement of 1948?', rem:['nakba'],
  read:'The refugee question goes: Resolution 194, UNRWA, the Absentees\' Property Law and Gaza\'s refugee population all lose their documented cause, and with them the documented route to Fatah and the PLO. The occupation and what grew from it stay, because they run through the war of 1967 rather than the displacement. The map cannot say whether a Palestinian national movement would have formed anyway; it shows only that the one on the record formed from the refugees.'},
 {id:'f_occupation', q:'What if there had been no occupation after 1967?', rem:['occupation'],
  read:'The settlements, both uprisings, the Oslo process and the summits that followed it, the 1973 war\'s documented cause, the Egyptian peace and the court rulings on the occupation all lose their documented cause. So do Hamas\'s takeover of Gaza, which came through the Palestinian Authority that Oslo created, the attack of 7 October and the war and rulings that followed. Hamas itself keeps one cause, the Islamist network rooted in the Brotherhood, so it is weakened rather than erased.'},
 {id:'f_lebanon', q:'What if Israel had not invaded Lebanon in 1982?', rem:['lebanon_1982'],
  read:'Sabra and Shatila lose their cause. Hezbollah keeps two: Iran\'s Revolutionary Guards in the Bekaa and the Shia movement that predates 1982. This is the record\'s own split on the question, and the map keeps it.'},
 {id:'f_coup', q:'What if there had been no coup in Iran in 1953?', rem:['ajax'],
  read:'A chain that does not run through the founding: the revolution of 1979 loses its documented root, and with it the Revolutionary Guards in Lebanon and the war of June 2025. Hezbollah and the Abraham Accords are weakened. This is the limit of the case: part of the region\'s conflict began with a coup that had nothing to do with Israel.'},
 {id:'f_patron', q:'What if the American government had withdrawn its support after 1948?', rem:['us_gov'],
  read:'The aid, the memorandum, the vetoes and the executive order lose their documented cause; the Abraham Accords and the war with Iran are weakened. The wars and the occupation themselves keep their causes: the map records what the patron paid for and shielded, not that it started them.'}
];
let vFolCache=null;
function vFolResults(){ if(vFolCache) return vFolCache; vFolCache=VFOLLOW.map(t=>({t, r:vFollow(new Set(t.rem))})); return vFolCache; }
function vFolRing(x){ const f=x.r.n?x.r.lost.length/x.r.n:0, r=15, c=2*Math.PI*r; return `<svg width="44" height="44" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="${r}" fill="none" stroke="var(--line)" stroke-width="5"/><circle cx="22" cy="22" r="${r}" fill="none" stroke="var(--after)" stroke-width="5" stroke-linecap="round" stroke-dasharray="${(c*f).toFixed(1)} ${c.toFixed(1)}" transform="rotate(-90 22 22)"/><text x="22" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="currentColor">${x.r.lost.length}</text></svg>`; }
function vFollowList(){ return `<h3 class="vsec">What followed: tests after 1948</h3><p class="vtxt">The seventh link of the case: which of the wars, uprisings, plans and rulings since 1948 would exist without the founding. These tests use the red layer of the map, where each later event carries the documented causes the library's volumes give it. Remove a cause, and an event that loses every documented cause is counted as lost; one that keeps another cause is weakened. A few causes are treated as necessary because the event cannot exist without them by definition: the parties to a war, the territory of an occupation, the state an aid programme pays. This is a reading of the record's own chains, not a chance; the number in each ring is how many later events lose every cause.</p><div class="vtlist">${vFolResults().map((x,i)=>`<button class="vtrow" type="button" data-fol="${i}">${vFolRing(x)}<span class="vtq"><span class="vfeat">Link 7 · What followed</span><b>${esc(x.t.q)}</b><small><span class="vtl" style="background:var(--after)"></span>${x.r.lost.length} of ${x.r.n} later events lose every documented cause · ${x.r.weak.length} weakened</small></span><span class="vtgo" aria-hidden="true">›</span></button>`).join('')}</div>`; }
function vFollowOpen(i){ const x=vFolResults()[i], li=a=>a.length?'<ul class="pl">'+a.map(id=>`<li>${esc(N.get(id).name)}</li>`).join('')+'</ul>':'<p class="vtxt">None.</p>';
  vOpen(`<div class="kind">What followed · link 7</div><h3 id="vmH">${esc(x.t.q)}</h3><p class="vtxt">Removed: ${x.t.rem.map(id=>esc(N.get(id).name)).join(', ')}.</p><p class="vtxt">${esc(x.t.read)}</p>
  <h3 class="vsec">Lose every documented cause (${x.r.lost.length})</h3>${li(x.r.lost)}<h3 class="vsec">Weakened: keep another cause (${x.r.weak.length})</h3>${li(x.r.weak)}<p class="vtxt">Unaffected: ${x.r.keep} of ${x.r.n} later events.</p>
  <div class="vbtns"><button class="vbtn pri" type="button" data-folmap="${i}">Show on the map</button><button class="vbtn" type="button" data-v="tests">Back to the tests</button><button class="vbtn" type="button" data-v="close">Close</button></div>`); }
vCard.addEventListener('click', e=>{ const b=e.target.closest('[data-fol]'); if(b){ e.stopPropagation(); vFollowOpen(+b.dataset.fol); return; }
  const m=e.target.closest('[data-folmap]'); if(!m) return; e.stopPropagation(); const x=vFolResults()[+m.dataset.folmap]; vClose();
  ERA='both'; $('eraSeg').querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.era==='both')); $('root').value='israel_gov'; $('depth').value=5; $('dval').textContent='All';
  hiNodes=new Set([...x.t.rem,...x.r.lost,...x.r.weak]); hiEdges=new Set(); E.forEach((ed,i)=>{ if(ed.era==='after'&&hiNodes.has(ed.f)&&hiNodes.has(ed.t)) hiEdges.add(i); }); posCache.clear(); needFit=true; draw(); }, true);
/* nodes after 1948: the founding chance does not apply; show what followed from them instead */
const vSide1=side; side=function(id,msg){ vSide1(id,msg); const n=N.get(id); if(!n||n.era!=='after') return; const box=$('side').querySelector('.viab'); if(!box) return; const r=vFollow(new Set([id])), li=a=>a.length?'<ul class="pl">'+a.map(x=>`<li>${esc(N.get(x).name)}</li>`).join('')+'</ul>':'';
  box.innerHTML=`<div class="vlabel">After 1948 · what followed from it</div><p class="vtxt">${n.year?esc(String(n.year))+'. ':''}The chance of a state in 1948 does not apply to what came after the founding. On the red layer, without this ${r.lost.length?r.lost.length+' later '+(r.lost.length===1?'event loses':'events lose')+' every documented cause'+(r.weak.length?' and '+r.weak.length+' '+(r.weak.length===1?'is':'are')+' weakened':''):r.weak.length?r.weak.length+' later '+(r.weak.length===1?'event is':'events are')+' weakened, keeping another cause':'no later event loses a documented cause'}.</p>${li(r.lost)}${r.weak.length?'<p class="vtxt">Weakened:</p>'+li(r.weak):''}`; };
const vCallout1=showCallout; showCallout=function(id){ vCallout1(id); const n=N.get(id); if(!n||n.era!=='after') return; const b=callout.querySelector('.c-rm'); if(b) b.remove(); placeCallout(); };
"""
rep('const BRK_KIND=', T + 'const BRK_KIND=')
rep('  ${vCaseList()}\n', '  ${vCaseList()}\n  ${vFollowList()}\n')
rep('The seventh link, that the wars and accords followed from the founding, cannot be tested here: this map stops in 1948.</p>',
    'The seventh link, that the wars and accords followed from the founding, is tested in the next section, on the red layer after 1948.</p>')
open(P, 'w', encoding='utf-8').write(s)
print('after-1948 layer applied:', len(L['nodes']), 'nodes,', len(L['ties']), 'ties,', len(fol), 'causal links,', len(after), 'nodes after 1948')
