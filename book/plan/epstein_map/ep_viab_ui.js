/* ---------- what-if model (Epstein map); mirrors ep_viability.py ---------- */
const VB = DATA.viab;
const VKEY = 'ep_removed_v1', VINTRO = 'ep_model_intro_v1';
const VENT = new Set(VB.ent), VK = -Math.log(1-VB.cal);
function vLS(k, v){ try{ if(v === undefined) return JSON.parse(localStorage.getItem(k) || 'null'); if(v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v)); }catch(e){ return null; } }
function vAlive(rem){ const out=new Set(); for(const x of VB.ent){ if(rem.has(x)) continue; let o=VB.owner[x], ok=true; const seen=new Set(); while(o&&!seen.has(o)){ seen.add(o); if(rem.has(o)){ ok=false; break; } o=VB.owner[o]; } if(ok) out.add(x); } return out; }
function vDecisionChance(D, rem){ let dec=D.decider;
  if(rem.has(dec)) dec=(D.successor&&!rem.has(D.successor))?D.successor:null;
  if(!dec) return [0, null];
  const W=D.weights||{}; let S=0, O=0;
  for(const l of D.levers){ if(rem.has(l)) continue; if(dec!==D.decider&&(VB.tied[D.decider]||[]).includes(l)) continue; S+=W[l]||1; }
  for(const o of D.oppose) if(!rem.has(o)) O+=W[o]||1;
  if(dec!==D.decider){ S+=VB.unknown_successor; O+=VB.unknown_successor; }
  return [S+O?S/(S+O):0, dec]; }
function vBase(rem, after){ const live=vAlive(rem), cap=VB.channels.map(()=>0);
  const ok=(f,t)=>!(rem.has(f)||rem.has(t))&&(live.has(f)||live.has(t))&&!(VENT.has(f)&&!live.has(f))&&!(VENT.has(t)&&!live.has(t));
  for(const [f,t,c,w,y] of VB.edges){ if(!ok(f,t)) continue; if(after&&y&&y>after) continue; cap[c]+=w; }
  const gone=VB.hubs.every(h=>rem.has(h)); if(gone) cap.fill(0);
  const pc=cap.map((x,i)=>VB.cap0[i]?1-Math.exp(-VK*x/VB.cap0[i]):1);
  const yrs=[]; for(let Y=VB.y0;Y<=VB.y1;Y++){ if(gone||(after&&Y>after)){ yrs.push(0); continue; } let s=0, s0=0;
    for(const [f,t,c,w,y] of VB.edges){ if(c!==0||(y&&y>Y)) continue; s0+=w; if(ok(f,t)) s+=w; } yrs.push(s0?1-Math.exp(-VK*s/s0):1); }
  pc[0]=yrs.reduce((a,b)=>a+b,0)/yrs.length;
  const eff=pc.map((p,i)=>VB.cover.includes(i)?0.5+0.5*p:p);
  return {P:100*eff.reduce((a,b)=>a*b,1), pc, cap, gone}; }
function vScore(rem0){ const rem=new Set(rem0);
  if(rem.has('epstein')){ const R=vBase(rem); return Object.assign(R,{deal:null, arrest:null, account:null, decisions:[]}); }
  const [D1,D2]=VB.decisions, c=(D,r)=>vDecisionChance(D,r);
  const p10=c(D1,new Set())[0], [p1,d1]=c(D1,rem); let r1=p10?Math.min(1,p1/p10):1; if(rem.has('npa')) r1=0;
  const p20=c(D2,new Set())[0], [p2,d2]=c(D2,rem), r2=p20?Math.min(1,p2/p20):1;
  const A=vBase(rem), B=vBase(new Set([...rem,'npa']), 2008);
  return {P:r1*A.P+(1-r1)*B.P, pc:A.pc.map((a,i)=>r1*a+(1-r1)*B.pc[i]), cap:A.cap, gone:false, deal:r1, arrest:r2, account:(1-r1)+r1*r2,
    decisions:[{id:D1.id,name:D1.name,chance:r1,decider:d1},{id:D2.id,name:D2.name,chance:r2,decider:d2}]}; }
const V0 = vScore(new Set());
function vVerdict(P){ for(const [cut,txt] of VB.verdict) if(P>=cut) return txt; return VB.verdict[VB.verdict.length-1][1]; }
function vColor(V){ return V>=75?'var(--ver)':V>=35?'var(--tov)':'var(--nest)'; }
function vLight(v){ return v===VB.verdict[0][1]?['#2E9E5B','Green']:(v===VB.verdict[1][1]||v===VB.verdict[2][1])?['#E0A800','Yellow']:['#D64545','Red']; }
function vMoney(m){ return m>=1?'$'+(Math.round(m*10)/10)+' million':'$'+Math.round(m*1000)+',000'; }
function vName(x){ return x==='*'?'an unnamed successor':(N.get(x)?N.get(x).name:x); }
function vPct(x){ return x==null?'—':Math.round(100*x)+'%'; }

/* ---------- reading blocks ---------- */
function vReadTable(R){ const row=(l,v,sub)=>`<tr><td>${l}${sub?`<small style="display:block;color:var(--muted)">${sub}</small>`:''}</td><td style="color:${v==null?'inherit':vColor(100*v)}">${vPct(v)}</td></tr>`;
  if(R.deal==null) return `<table class="vread">${row('The operation runs as documented, 1991–2019',R.P/100)}<tr><td colspan="2" style="text-align:left;font-family:inherit;font-weight:400">With Epstein removed there is no operation of his to shield or to bring to account.</td></tr></table>`;
  return `<table class="vread">${row('The operation runs as documented, 1991–2019',R.P/100)}${row('The 2008 deal is still made',R.deal,'against the record, where it was made')}${row('The 2019 arrest still comes',R.arrest,'against the record, where it came')}${row('He is brought to account (2008 or 2019)',R.account,'no deal means a federal case in 2008')}</table>`; }
function vHead(R){ const v=vVerdict(R.P); return `<div class="vbig"><b style="color:${vColor(R.P)}">${Math.round(R.P)}%</b><span style="font-weight:600">${esc(v)}</span></div>${vReadTable(R)}`; }
function vBars(R){ return VB.channels.map((c,i)=>`<div class="vrow"><span>${esc(VB.labels[c])}${VB.cover.includes(i)?' <em>half weight</em>':''}</span><span class="vbar"><i style="width:${Math.round(R.pc[i]*100)}%;background:${vColor(R.pc[i]*100)}"></i></span><span class="vnum">${Math.round(R.pc[i]*100)}%</span></div>`).join(''); }
function vDecText(R){ if(!R.decisions||!R.decisions.length) return '';
  return `<ul class="vul">${R.decisions.map(x=>{ const D=VB.decisions.find(d=>d.id===x.id); return `<li><b>${esc(x.name)}</b>: ${x.decider?`decided by ${esc(vName(x.decider))}${x.decider!==D.decider?` instead of ${esc(vName(D.decider))}`:''}`:'no one left to decide'}; chance it still happens, against the record: <b>${Math.round(x.chance*100)}%</b>.</li>`; }).join('')}</ul>`; }
function vNeed(R){ if(R.gone) return `<p class="vtxt"><b>No one is left to run it.</b> Epstein and Maxwell are both removed; the companies, trusts, properties and aircraft fall with them, so every channel counts as empty.</p>`;
  if(R.deal==null) return `<p class="vtxt"><b>The operation was his.</b> The money came to him, the accounts were his, and the companies, trusts, properties and aircraft were his or his companies'. Without him they fall too; what remains is Maxwell's own documented ties, which on this record carried none of the money, banking or property.</p>`;
  const weak=R.pc.map((x,i)=>[x,i]).filter(([x])=>x<0.9).sort((a,b)=>a[0]-b[0]);
  return weak.length?`<p class="vtxt">Weakest after this removal: ${weak.slice(0,3).map(([x,i])=>`${esc(VB.labels[VB.channels[i]].toLowerCase())} (${Math.round(x*100)}%)`).join(', ')}.</p>`:'<p class="vtxt">The rest of the documented network covers what was taken away.</p>'; }
function nodeWeights(id){ const q=(N.get(id)||{}).qop||{}, v=q.whatif; if(!v) return '';
  return `<p class="vtxt">Taken out alone: <b>${esc(v.verdict)}</b>, ${v.P}%${v.drop>=0.5?` (down ${v.drop} points)`:''}; weakest channel: ${esc(VB.labels[VB.channels[v.weakest]].toLowerCase())}${v.deal!=null&&v.deal<100?`; the 2008 deal ${v.deal}% as likely`:''}${v.account!=null&&v.account<100?`; brought to account ${v.account}% as likely`:''}.</p>`; }

/* ---------- styles and the dialog ---------- */
document.head.insertAdjacentHTML('beforeend', `<style>
.viab{border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:0 0 14px;background:color-mix(in srgb,var(--panel-2) 60%,transparent)}
.vlabel{font:500 11px/1.3 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 4px}
.vrow{display:grid;grid-template-columns:140px 1fr 46px;gap:8px;align-items:center;font-size:12.5px;margin:3px 0}
.vrow em{font-style:normal;color:var(--gold);font-size:10.5px}
.vbar{height:7px;border-radius:4px;background:var(--line);overflow:hidden}.vbar i{display:block;height:100%}
.vnum{text-align:right;font-family:var(--f-mono)}
.vtxt{margin:7px 0 0;font-size:13px;line-height:1.5}
.vbig{display:flex;align-items:baseline;gap:10px;margin:6px 0 4px;flex-wrap:wrap}.vbig b{font:700 2.2rem/1 var(--f-display)}
.vbtn{border:1px solid var(--gold-2);background:transparent;color:var(--gold);border-radius:999px;padding:8px 14px;font:600 13px/1 inherit;cursor:pointer}
.vbtn.pri{background:var(--gold);color:var(--panel);border-color:var(--gold)}
.vbtns{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.vmodal{position:fixed;inset:0;z-index:60;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(0,0,0,.55);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
.vmodal.on{display:flex}
.vcard{width:min(540px,100%);max-height:calc(100dvh - 32px);overflow:auto;-webkit-overflow-scrolling:touch;background:var(--panel);border:1px solid var(--gold-2);border-radius:20px;padding:18px 18px calc(16px + env(safe-area-inset-bottom,0px));box-shadow:0 30px 80px rgba(0,0,0,.5)}
.vcard h3{font:700 1.25rem/1.25 var(--f-display);margin:2px 0 6px}.vcard h4{font:600 .95rem/1.3 var(--f-display);margin:14px 0 2px}
.vcard .kind{margin:0}.vcard ul{margin:6px 0 0;padding-left:18px;font-size:13px;line-height:1.5}
.vread{width:100%;border-collapse:collapse;font-size:12.8px;margin:6px 0 4px}.vread td{padding:5px 4px;border-top:1px solid var(--line);vertical-align:top}.vread td:last-child{text-align:right;font-family:var(--f-mono);white-space:nowrap;font-weight:600}
.vcard table{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:6px}.vcard td{padding:4px 6px;border-top:1px solid var(--line);vertical-align:top}.vcard td:last-child{text-align:right;font-family:var(--f-mono);white-space:nowrap}
.vpill{position:absolute;left:10px;top:64px;z-index:3;display:none;align-items:center;gap:8px;padding:6px 8px 6px 12px;border-radius:999px;border:1px solid var(--gold-2);background:color-mix(in srgb,var(--panel) 92%,transparent);font-size:12.5px;max-width:calc(100% - 70px)}
.vpill.on{display:flex}.vpill button{border:0;background:transparent;color:var(--gold);font:600 12.5px/1 inherit;cursor:pointer;padding:4px 6px}
.c-rm{margin-top:8px;width:100%}
@media (max-width:820px){.vpill{top:auto;bottom:calc(96px + env(safe-area-inset-bottom,0px));left:10px}}
.vsig{position:fixed;left:50%;top:calc(10px + env(safe-area-inset-top,0px));z-index:70;width:min(440px,calc(100% - 20px));transform:translate(-50%,-140%);transition:transform .32s cubic-bezier(.2,.85,.25,1),opacity .32s;opacity:0;display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:start;padding:11px 10px 11px 12px;border-radius:16px;border:1px solid var(--line);background:color-mix(in srgb,var(--panel) 96%,transparent);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);box-shadow:0 14px 40px rgba(0,0,0,.35);cursor:pointer}
.vsig.on{transform:translate(-50%,0);opacity:1}
.vsig .lamp{width:16px;height:16px;border-radius:50%;margin-top:3px;box-shadow:0 0 0 3px color-mix(in srgb,var(--lc) 25%,transparent),0 0 14px var(--lc);background:var(--lc)}
.vsig .t1{font-weight:700;font-size:14px;line-height:1.3}.vsig .t2{font-size:12.5px;line-height:1.45;color:var(--muted);margin-top:2px}.vsig .t2 b{color:inherit}
.vsig .x{border:0;background:transparent;color:var(--muted);font-size:20px;line-height:1;padding:2px 6px;cursor:pointer}
.vsig .bar{grid-column:1/-1;height:2px;border-radius:2px;background:var(--lc);transform-origin:left;opacity:.6}
@media (prefers-reduced-motion:reduce){.vsig{transition:none}}
</style>`);
document.body.insertAdjacentHTML('beforeend', '<div class="vmodal" id="vModal" role="dialog" aria-modal="true" aria-labelledby="vmH"><div class="vcard" id="vCard"></div></div><div class="vsig" id="vSig" role="status" aria-live="polite"></div>');
const vModal=document.getElementById('vModal'), vCard=document.getElementById('vCard');
vModal.addEventListener('click', e=>{ if(e.target===vModal) vClose(); });
document.addEventListener('keydown', e=>{ if(e.key==='Escape' && vModal.classList.contains('on')) vClose(); });
function vOpen(h){ vCard.innerHTML=h; vModal.classList.add('on'); vCard.scrollTop=0; const b=vCard.querySelector('button'); if(b) try{ b.focus({preventScroll:true}); }catch(e){} }
function vClose(){ vModal.classList.remove('on'); }

/* ---------- the explainer ---------- */
function vIntro(){
  const heavy=[...N.values()].filter(n=>n.qop&&n.qop.whatif&&!['epstein','gmax'].includes(n.id)).sort((a,b)=>b.qop.whatif.drop-a.qop.whatif.drop).slice(0,10);
  const amts=Object.entries(VB.amounts).sort((a,b)=>b[1][0]-a[1][0]), D1=VB.decisions[0], D2=VB.decisions[1], p1=vDecisionChance(D1,new Set())[0], p2=vDecisionChance(D2,new Set())[0];
  vOpen(`<div class="kind">How the chances are computed</div><h3 id="vmH">A model of what the operation needed, built only from this map</h3>
  <p class="vtxt">Take any node out and the map works out the chance that the operation still runs as the record documents it, from 1991 to 2019, and whether the 2008 deal and the 2019 arrest still happen. It is a model of the documented ties, not a measured probability, and it is the same arithmetic as the Road to 1948 map. Here is everything it does.</p>
  <h4>1. What counts as the operation</h4>
  <p class="vtxt">Epstein, Maxwell, the office and companies that carried his business (Indyke, Kahn, HBRK, Southern Trust, Financial Trust, the trusts, JEGE, Plan D, Hyperion and others), and the properties and aircraft they owned: ${VB.ent.length} nodes. An owned company, trust or property falls with whoever owned it.</p>
  <h4>2. Six channels</h4>
  <p class="vtxt">Every documented tie between the operation and an outside node is sorted into one: <b>money in</b> (people documented as paying him); <b>banking</b>; <b>places and aircraft</b>; <b>staff and operations</b>; <b>legal and official cover</b> (his lawyers, the deals, the Virgin Islands tax break); <b>access and reputation</b> (correspondence, introductions, the people and causes his money reached). Investigations, testimony, lawsuits, reporting, flight-log entries and records are not support and are left out. ${VB.edges.length} ties count.</p>
  <h4>3. Money is a stock, built year by year</h4>
  <p class="vtxt">Each money tie carries the sum the record states, in millions of dollars; a tie with no stated sum counts ${vMoney(VB.default_m)}, an assumption. Each year from ${VB.y0} to ${VB.y1} is read against the money that had come in by then, so money that arrived early (Wexner's, from 1991) carries more years than money that came late (Black's, from 2012).</p>
  <table>${amts.map(([k,a])=>`<tr><td>${esc(a[1])}</td><td>${vMoney(a[0])}</td></tr>`).join('')}</table>
  <h4>4. The other channels</h4>
  <p class="vtxt">A verified tie counts 1, a reported one 0.6; leads still to verify count nothing. A bank tie counts the years the account ran (${VB.default_bank_years} if unstated). Each channel's strength is 1 &minus; e<sup>&minus;k&middot;C/C₀</sup>, where C is what still connects, C₀ the full record and k is set so the full record gives 99%: spare capacity protects a channel, and losses bite harder as it empties.</p>
  <h4>5. Running and cover</h4>
  <p class="vtxt">Money, banking, places and staff ran the operation: all four were needed, so the chance is their product. Legal cover and access protected it rather than ran it, so each enters as half plus half its strength: losing all of either halves the chance instead of ending it. On the full record: ${Math.round(V0.P)}%.</p>
  <h4>6. Two decisions</h4>
  <p class="vtxt"><b>${esc(D1.name)}</b>, decided by Alexander Acosta. ${esc(D1.why)} On the record its chance is the push over push plus resistance: ${Math.round(p1*100)}%; the readings show it relative to that. If Acosta is removed an unnamed successor decides, with one unit added to each side, and Lefkowitz's personal approaches to Acosta do not pass to him. Without the deal, the case is taken to go federal in 2008, so the operation's ties that begin after 2008 never happen.</p>
  <p class="vtxt"><b>${esc(D2.name)}</b>, decided by Geoffrey Berman's office. ${esc(D2.why)} On the record: ${Math.round(p2*100)}%. "Brought to account" is the chance of either: a federal case in 2008, or, with the deal, the 2019 arrest.</p>
  <h4>7. The verdict</h4>
  <p class="vtxt">${VB.verdict.map(([c,t],i)=>`<b>${esc(t)}</b>${i<VB.verdict.length-1?` from ${c}%`:''}`).join('; ')}.</p>
  <h4>The heaviest nodes, each removed alone</h4>
  <table>${heavy.map(n=>`<tr><td>${esc(n.name)}<small style="display:block;color:var(--muted)">${esc(n.qop.whatif.verdict)}</small></td><td>${n.qop.whatif.P}%</td></tr>`).join('')}</table>
  <h4>What it cannot know, and what it does not do</h4>
  <p class="vtxt">It counts documented ties, not their gravity: a criminal conviction covering ten years of conduct counts as one tie. It cannot know whether someone undocumented would have stepped in. And it names no one as a successor to Epstein or Maxwell: where the readings show work still covered, that means other documented ties remain, not that anyone would have taken their place. Group removals are in the Remove a node panel.</p>
  <div class="vbtns"><button class="vbtn pri" type="button" data-v="close">Start exploring</button></div>`);
  vLS(VINTRO, 1);
}

/* ---------- the result of a removal ---------- */
function vResult(what, before, ids){
  const R=vScore(removed), cutSet=ids||[...removed], cut=E.filter(e=>cutSet.some(x=>e.f===x||e.t===x)&&e.status!=='not-established').length;
  vOpen(`<div class="kind">Removed from the network</div><h3 id="vmH">${esc(what)}</h3>${vHead(R)}
  <p class="vtxt">${ids?`Before this removal ${Math.round(before)}%, now ${Math.round(R.P)}% (${Math.round(V0.P)}% on the full record).`:`Everything removed is read together: ${Math.round(R.P)}% against ${Math.round(V0.P)}% on the full record.`}</p>
  <h4>The six channels</h4>${vBars(R)}
  <h4>What happened in the graph</h4><ul><li>${cut} documented tie${cut===1?'':'s'} cut.</li><li>Money in still reaching him: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])}.</li><li>${removed.size} node${removed.size===1?'':'s'} removed in total, read together.</li></ul>
  ${R.decisions&&R.decisions.length?'<h4>Key decisions</h4>'+vDecText(R):''}${vNeed(R)}
  <div class="vbtns"><button class="vbtn pri" type="button" data-v="close">Keep exploring</button>${ids&&ids.length?'<button class="vbtn" type="button" data-v="undo">Undo this removal</button>':''}<button class="vbtn" type="button" data-v="reset">Reset the graph</button><button class="vbtn" type="button" data-v="how">How this is computed</button></div>`);
  vCard.dataset.ids=JSON.stringify(ids||[]);
}
vCard.addEventListener('click', e=>{ const b=e.target.closest('[data-v]'); if(!b) return; const a=b.dataset.v;
  if(a==='close') vClose(); else if(a==='how') vIntro(); else if(a==='reset'){ vClose(); $('reset').click(); }
  else if(a==='undo'){ JSON.parse(vCard.dataset.ids||'[]').forEach(x=>removed.delete(x)); vClose(); vRefresh(); } });
function vSave(){ vLS(VKEY, removed.size?{removed:[...removed]}:null); vPill(); }
function vRefresh(){ vSave(); if(mode==='del'){ const r=reconnect(); hiNodes=r.nodes; hiEdges=r.edges; delPanel(r); } else if(sel) side(sel); draw(); if(calloutId) showCallout(calloutId); }
function vRemove(ids, what){ const before=vScore(removed).P; ids.forEach(x=>{ if(N.get(x)) removed.add(x); }); vRefresh(); vSignal('Removed: '+what, before); }

/* ---------- the signal ---------- */
const vSig=document.getElementById('vSig'); let vSigT=null, vSigY=null;
function vSignal(label, before){
  const R=vScore(removed), v=vVerdict(R.P), [lc]=vLight(v), d=Math.round(R.P)-Math.round(before), n=removed.size;
  vSig.style.setProperty('--lc', lc);
  vSig.innerHTML=`<span class="lamp" aria-hidden="true"></span><div><div class="t1">${esc(v)}</div><div class="t2">${esc(label)} · ${n?n+' removed':'Nothing removed'}<br><b>${Math.round(R.P)}%</b> runs${d?` (${d>0?'+':''}${d})`:''}${R.deal!=null?` · deal <b>${vPct(R.deal)}</b> · brought to account <b>${vPct(R.account)}</b>`:''} · tap for details</div></div><button class="x" type="button" aria-label="Dismiss">×</button><span class="bar" id="vSigBar"></span>`;
  vSig.classList.add('on'); clearTimeout(vSigT);
  document.getElementById('vSigBar').animate([{transform:'scaleX(1)'},{transform:'scaleX(0)'}],{duration:6500,easing:'linear'}); vSigT=setTimeout(vSigOff, 6500); }
function vSigOff(){ clearTimeout(vSigT); vSig.classList.remove('on'); vSig.style.transform=''; }
vSig.addEventListener('click', e=>{ if(e.target.closest('.x')){ e.stopPropagation(); vSigOff(); return; } vSigOff(); vResult('The network as it stands', V0.P, null); });
vSig.addEventListener('pointerenter', ()=>{ clearTimeout(vSigT); vSig.getAnimations({subtree:true}).forEach(a=>a.pause()); });
vSig.addEventListener('pointerleave', e=>{ if(e.pointerType==='mouse' && vSig.classList.contains('on')){ vSig.getAnimations({subtree:true}).forEach(a=>a.play()); vSigT=setTimeout(vSigOff, 2500); } });
vSig.addEventListener('touchstart', e=>{ vSigY=e.touches[0].clientY; clearTimeout(vSigT); }, {passive:true});
vSig.addEventListener('touchend', e=>{ if(vSigY==null) return; const dy=e.changedTouches[0].clientY-vSigY; vSigY=null; if(dy<-30){ vSigOff(); e.preventDefault(); } else vSigT=setTimeout(vSigOff, 3000); });

/* ---------- reminder pill ---------- */
$('board').insertAdjacentHTML('beforeend','<div class="vpill" id="vPill"><span id="vPillT"></span><button type="button" id="vPillV">Details</button><button type="button" id="vPillR">Reset</button></div>');
function vPill(){ const p=$('vPill'); if(!p) return; if(!removed.size){ p.classList.remove('on'); return; } const R=vScore(removed); $('vPillT').innerHTML=`${removed.size} removed · <b style="color:${vColor(R.P)}">${Math.round(R.P)}%</b> runs`; p.classList.add('on'); }
$('vPillV').onclick=()=>vResult([...removed].map(vName).join(', ')||'Scenario', V0.P, null);
$('vPillR').onclick=()=>$('reset').click();

/* ---------- the Remove a node panel ---------- */
function viabBlock(){ const R=vScore(removed), opts=Object.keys(VB.groups).map(g=>`<option value="${esc(g)}">${esc(g)} (${VB.groups[g].filter(x=>N.get(x)).length})</option>`).join('');
  let h=`<div class="viab"><div class="vlabel">The operation&rsquo;s chances, on this record</div>${vHead(R)}${removed.size?`<p class="vtxt">Down ${Math.round(V0.P-R.P)} from ${Math.round(V0.P)}%.</p>`:''}${vBars(R)}`;
  h+=removed.size?vDecText(R)+vNeed(R):`<p class="vtxt">Tap any node to remove it, or remove a whole group below.</p>`;
  h+=`<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px"><select id="vgrp" class="sel" style="flex:1 1 180px;padding:7px 30px 7px 10px">${opts}</select><button id="vgo" class="ghost" type="button">Remove group</button>${removed.size?'<button id="vclr" class="ghost" type="button">Restore all</button>':''}</div><div class="vbtns" style="margin-top:8px"><button class="vbtn" type="button" id="vhow">How this is computed</button></div></div>`;
  return h; }
function delPanel(r){ delPanel0(r); $('side').insertAdjacentHTML('afterbegin', viabBlock());
  const go=$('vgo'); if(go) go.onclick=()=>{ const g=$('vgrp').value; vRemove(VB.groups[g], g); };
  const cl=$('vclr'); if(cl) cl.onclick=()=>$('reset').click(); const hw=$('vhow'); if(hw) hw.onclick=vIntro; }
const vPick0 = pick;
pick = function(id){ if(mode!=='del') return vPick0(id); const had=removed.has(id), before=vScore(removed).P; vPick0(id); vSave(); vSignal((had?'Restored: ':'Removed: ')+vName(id), before); };
const vCallout0 = showCallout;
showCallout = function(id){ vCallout0(id); if(!N.get(id)) return; const on=removed.has(id);
  callout.insertAdjacentHTML('beforeend', `<button class="vbtn c-rm${on?'':' pri'}" type="button">${on?'Restore to the network':'Remove from the network'}</button>`);
  callout.querySelector('.c-rm').onclick=ev=>{ ev.stopPropagation(); if(on){ const before=vScore(removed).P; removed.delete(id); vRefresh(); vSignal('Restored: '+vName(id), before); } else vRemove([id], vName(id)); };
  placeCallout(); };
const vSide0 = side;
side = function(id, msg){ vSide0(id, msg); if(!N.get(id)) return; const on=removed.has(id);
  $('side').insertAdjacentHTML('afterbegin', `<div class="viab"><div class="vlabel">${on?'Removed from the network':'If this were removed'}</div>${nodeWeights(id)}<div class="vbtns"><button class="vbtn${on?'':' pri'}" type="button" id="vSideRm">${on?'Restore to the network':'Remove from the network'}</button><button class="vbtn" type="button" id="vSideHow">How this is computed</button></div></div>`);
  $('vSideRm').onclick=()=>{ if(on){ const before=vScore(removed).P; removed.delete(id); vRefresh(); vSignal('Restored: '+vName(id), before); } else vRemove([id], vName(id)); };
  $('vSideHow').onclick=vIntro; };
(function(){ const s=vLS(VKEY); if(s) (s.removed||[]).forEach(x=>{ if(N.get(x)) removed.add(x); }); setTimeout(()=>{ vPill(); if(removed.size) draw(); if(!vLS(VINTRO)) vIntro(); }, 600); })();
