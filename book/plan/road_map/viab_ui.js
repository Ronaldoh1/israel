/* ---------- survival model (road map only); mirrors viability.py ---------- */
const VB = DATA.viab;
const vDrop = new Set();          // ties dropped by a scenario (money raised in the US but carried by a non-American)
const VKEY = 'road_removed_v1', VINTRO = 'road_model_intro_v1';
function vLS(k, v){ try{ if(v === undefined) return JSON.parse(localStorage.getItem(k) || 'null'); if(v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v)); }catch(e){ return null; } }
function vLost(rem){ const out=new Set(rem); let ch=true; while(ch){ ch=false; for(const [doc,iss] of Object.entries(VB.issuers)){ if(!out.has(doc) && iss.length && iss.every(i=>out.has(i))){ out.add(doc); ch=true; } } } return out; }
function vReach(rem){ const adj=new Map(); for(const [f,t] of VB.edges){ if(rem.has(f)||rem.has(t)||vDrop.has(f+'>'+t)) continue; (adj.get(f)||adj.set(f,[]).get(f)).push(t); (adj.get(t)||adj.set(t,[]).get(t)).push(f); }
  const seen=new Set(VB.core.filter(x=>!rem.has(x))), q=[...seen]; while(q.length){ const u=q.pop(); for(const v of adj.get(u)||[]) if(!seen.has(v)){ seen.add(v); q.push(v); } } return seen; }
function vScore(rem0){ const rem=vLost(rem0), seen=vReach(rem), cap=[0,0,0,0,0], ties=[0,0,0,0,0], ties0=[0,0,0,0,0], funders=new Set(), funders0=new Set();
  for(const [f,t,c,w,v] of VB.edges){ ties0[c]++; if(c===0&&v>0) funders0.add(f);
    if(rem.has(f)||rem.has(t)||vDrop.has(f+'>'+t)) continue; if(seen.has(f)||seen.has(t)){ cap[c]+=v; ties[c]++; if(c===0&&v>0) funders.add(f); } }
  const k=-Math.log(1-VB.cal), pc=cap.map((x,i)=>VB.cap0[i]?1-Math.exp(-k*x/VB.cap0[i]):1), share=cap.map((x,i)=>VB.cap0[i]?x/VB.cap0[i]:1);
  const P=pc.reduce((a,b,i)=>a*Math.pow(b,VB.exp[i]),100), delay=share.map((r,i)=>VB.tbuild[i]*(1-r));
  const lostDocs=[...rem].filter(x=>!rem0.has(x));
  return {P,pc,share,delay,cap,ties,ties0,funders:funders.size,funders0:funders0.size,lostDocs}; }
const V0 = vScore(new Set());

/* five readings of one removal (mirrors viability.readings) */
function vRead(R){ const k=-Math.log(1-VB.cal), P0=R.P/100, D=Math.max(...R.delay);
  const Pat=sh=>sh.reduce((p,x,i)=>p*Math.pow(1-Math.exp(-k*x),VB.exp[i]),1);
  const out={on:100*P0, delay:D, survive:100*Math.pow(R.pc[0],2)*R.pc[4]}; let best=0, tb=0;
  for(let t=1;t<=100;t++){ const sh=R.share.map((s,i)=>s>0.001?Math.min(1,s+t/VB.tbuild[i]):0), p=Pat(sh)*Math.exp(-VB.hazard*t); if(p>best){ best=p; tb=t; } if(VB.horizons.includes(t)) out['by'+(1948+t)]=100*Math.max(P0,best); }
  out.ever=100*Math.max(P0,best); out.retry=best>P0?1948+tb:null;
  for(const [cut,key,txt] of VB.verdict) if(out[key]>=cut){ out.verdict=txt; break; }
  return out; }
function vReadTable(rd){ const row=(l,v,sub)=>`<tr><td>${l}${sub?`<small style="display:block;color:var(--muted)">${sub}</small>`:''}</td><td style="color:${vColor(v)}">${Math.round(v)}%</td></tr>`;
  return `<table class="vread">${row('Founded on time, in 1948',rd.on)}${row('Founded by 1958',rd.by1958, rd.retry&&rd.retry<=1958?'best year to try again: '+rd.retry:'')}${row('Ever becomes a state',rd.ever,'later attempts lose 2% a year as the 1947-48 window closes')}${row('The movement itself survives',rd.survive,'keeps its money and organization, whatever happens to the state')}
  <tr><td>Time to rebuild what was lost</td><td>${rd.delay<1?'none':'about '+Math.round(rd.delay)+' yrs'}</td></tr></table>`; }
function vHead(R){ const rd=vRead(R); return `<div class="vbig"><b style="color:${vColor(rd.on)}">${Math.round(rd.on)}%</b><span style="font-weight:600">${esc(rd.verdict)}${rd.verdict.indexOf('delayed')>=0?` (about ${Math.round(rd.delay)} years)`:''}</span></div>${vReadTable(rd)}`; }
function vRating(V){ return V>=90?'Still possible':V>=75?'Still possible, with more work':V>=55?'Possible only with major outside help':V>=35?'Doubtful':V>=15?'Very unlikely':'Not possible on this record'; }
function vColor(V){ return V>=75?'var(--ver)':V>=35?'var(--tov)':'var(--nest)'; }
function vMoney(m){ return m>=1?'$'+(Math.round(m*10)/10)+' million':'$'+Math.round(m*1000)+',000'; }
function vName(x){ const n=N.get(x); return n?n.name:x; }
function vSave(){ vLS(VKEY, removed.size||vDrop.size ? {removed:[...removed], drop:[...vDrop]} : null); vPill(); }
function vBars(R){ return VB.channels.map((c,i)=>`<div class="vrow"><span>${esc(VB.labels[c])}${VB.exp[i]>1?' <em>×2</em>':''}</span><span class="vbar"><i style="width:${Math.round(R.pc[i]*100)}%;background:${vColor(R.pc[i]*100)}"></i></span><span class="vnum">${Math.round(R.pc[i]*100)}%</span></div>`).join(''); }
function vDelayText(R){ const md=Math.max(...R.delay), mi=R.delay.indexOf(md);
  if(R.pc.some(p=>p<0.005)) return `<p class="vtxt"><b>On this record the state is not founded.</b> ${esc(VB.labels[VB.channels[R.pc.indexOf(Math.min(...R.pc))]])} is gone entirely. Rebuilding it at the pace it was first built (from ${esc(VB.tfrom[mi])}) would take about ${Math.round(md)} years.</p>`;
  if(md>=1){ const rd=vRead(R); return `<p class="vtxt">Rebuilding the lost ${esc(VB.labels[VB.channels[mi]].toLowerCase())} fully, at the pace it was first built (from ${esc(VB.tfrom[mi])}), would take about <b>${Math.round(md)} years</b>.${rd.retry?` Because the 1947-48 window was closing, the best chance of a later founding comes sooner, around <b>${rd.retry}</b>, with what has been rebuilt by then.`:' Waiting would not raise the chance: the window was closing faster than the loss could be rebuilt.'}</p>`; }
  return '<p class="vtxt">No meaningful delay: the rest of the documented network covers what was taken away.</p>'; }
function vNeed(R){ const weak=R.pc.map((x,i)=>[x,i]).filter(([x])=>x<0.95).sort((a,b)=>a[0]-b[0]);
  return weak.length?`<p class="vtxt">To make up the loss the movement would need ${weak.slice(0,2).map(([x,i])=>esc(VB.need[VB.channels[i]])).join(', and ')}.</p>`:''; }
function nodeWeights(id){ const q=(N.get(id)||{}).qop||{}, v=q.viability; if(!v) return '';
  const parts=VB.channels.map((c,i)=>[c,v.weight[i]]).filter(([c,w])=>w>=0.005).sort((a,b)=>b[1]-a[1]).map(([c,w])=>`${esc(VB.labels[c].toLowerCase())} ${Math.round(w*100)}%`);
  return `<p class="vtxt">Its own share of the network: ${parts.length?parts.join(', '):'under 1% of every channel'}. Taken out alone: <b>${esc(v.read.verdict)}</b>; ${v.V}% on time${v.drop>=0.5?` (down ${v.drop} points)`:''}, ${v.read.ever}% ever, and the movement survives at ${v.read.survive}%.</p>`; }

/* ---------- styles ---------- */
document.head.insertAdjacentHTML('beforeend', `<style>
.viab{border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:0 0 14px;background:color-mix(in srgb,var(--panel-2) 60%,transparent)}
.vlabel{font:500 11px/1.3 var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin:0 0 4px}
.vrow{display:grid;grid-template-columns:128px 1fr 46px;gap:8px;align-items:center;font-size:12.5px;margin:3px 0}
.vrow em{font-style:normal;color:var(--gold);font-size:11px}
.vbar{height:7px;border-radius:4px;background:var(--line);overflow:hidden}.vbar i{display:block;height:100%}
.vnum{text-align:right;font-family:var(--f-mono)}
.vtxt{margin:7px 0 0;font-size:13px;line-height:1.5;color:var(--ink,inherit)}
.vbig{display:flex;align-items:baseline;gap:10px;margin:6px 0 4px;flex-wrap:wrap}
.vbig b{font:700 2.2rem/1 var(--f-display)}
.vbtn{border:1px solid var(--gold-2);background:transparent;color:var(--gold);border-radius:999px;padding:8px 14px;font:600 13px/1 inherit;cursor:pointer}
.vbtn.pri{background:var(--gold);color:var(--panel);border-color:var(--gold)}
.vbtns{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.vmodal{position:fixed;inset:0;z-index:60;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(0,0,0,.55);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
.vmodal.on{display:flex}
.vcard{width:min(540px,100%);max-height:calc(100dvh - 32px);overflow:auto;-webkit-overflow-scrolling:touch;background:var(--panel);border:1px solid var(--gold-2);border-radius:20px;padding:18px 18px calc(16px + env(safe-area-inset-bottom,0px));box-shadow:0 30px 80px rgba(0,0,0,.5)}
.vcard h3{font:700 1.25rem/1.25 var(--f-display);margin:2px 0 6px}
.vcard h4{font:600 .95rem/1.3 var(--f-display);margin:14px 0 2px}
.vcard .kind{margin:0}
.vcard ul{margin:6px 0 0;padding-left:18px;font-size:13px;line-height:1.5}
.vread{width:100%;border-collapse:collapse;font-size:12.8px;margin:6px 0 4px}.vread td{padding:5px 4px;border-top:1px solid var(--line);vertical-align:top}.vread td:last-child{text-align:right;font-family:var(--f-mono);white-space:nowrap;font-weight:600}
.vcard table{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:6px}.vcard td{padding:4px 6px;border-top:1px solid var(--line);vertical-align:top}.vcard td:last-child{text-align:right;font-family:var(--f-mono);white-space:nowrap}
.vpill{position:absolute;left:10px;top:64px;z-index:3;display:none;align-items:center;gap:8px;padding:6px 8px 6px 12px;border-radius:999px;border:1px solid var(--gold-2);background:color-mix(in srgb,var(--panel) 92%,transparent);font-size:12.5px;max-width:calc(100% - 70px)}
.vpill.on{display:flex}.vpill button{border:0;background:transparent;color:var(--gold);font:600 12.5px/1 inherit;cursor:pointer;padding:4px 6px}
.c-rm{margin-top:8px;width:100%}
@media (max-width:820px){.vpill{top:auto;bottom:calc(96px + env(safe-area-inset-bottom,0px));left:10px}.vcard{border-radius:20px}}
</style>`);
document.body.insertAdjacentHTML('beforeend', '<div class="vmodal" id="vModal" role="dialog" aria-modal="true" aria-labelledby="vmH"><div class="vcard" id="vCard"></div></div>');
const vModal=document.getElementById('vModal'), vCard=document.getElementById('vCard');
vModal.addEventListener('click', e=>{ if(e.target===vModal) vClose(); });
document.addEventListener('keydown', e=>{ if(e.key==='Escape' && vModal.classList.contains('on')) vClose(); });
function vOpen(h){ vCard.innerHTML=h; vModal.classList.add('on'); vCard.scrollTop=0; const b=vCard.querySelector('button'); if(b) try{ b.focus({preventScroll:true}); }catch(e){} }
function vClose(){ vModal.classList.remove('on'); }

/* ---------- the explainer: shown on the first visit, and from every reading ---------- */
function vIntro(){
  const heavy=[...N.values()].filter(n=>n.qop&&n.qop.viability).sort((a,b)=>b.qop.viability.drop-a.qop.viability.drop).slice(0,10);
  const amts=Object.entries(VB.amounts).sort((a,b)=>b[1][0]-a[1][0]);
  vOpen(`<div class="kind">How the chances are computed</div><h3 id="vmH">A model of what the state needed, built only from this map</h3>
  <p class="vtxt">Take any node out and the map works out the chance that the state is still founded in 1948, how much money still reaches the movement, and how long the loss would delay it. It is a model built on the documented record, not a measured historical probability. Here is everything it does.</p>
  <h4>1. Five things the state needed</h4>
  <p class="vtxt">Every supportive tie dated before 1949 is sorted into one channel: <b>money</b>; <b>land and settlers</b>; <b>arms and force</b>; <b>diplomacy and law</b>; <b>organization</b>. Opposition, violence, ties on the Arab or Nazi side, and money that did not go to the project (Rothschild loans to the British treasury, the Suez purchase) are left out.</p>
  <h4>2. Money counts most</h4>
  <p class="vtxt">Without money nothing else could be bought, built or defended, so the money channel counts twice in the overall chance. Each money tie is weighted by the sum the record states, in 1948 dollars (francs at 5.18 to the dollar, sterling at $4.86, older sums brought to 1948 prices). Where the record states no sum the tie is assumed to carry ${vMoney(VB.default_m)}; that is an assumption, not a finding. Money passed along (the UJA to the UPA) or already inside a total (Edmond's colonies, inside his lifetime figure) is counted once.</p>
  <table>${amts.map(([k,a])=>`<tr><td>${esc(a[1])}</td><td>${vMoney(a[0])}</td></tr>`).join('')}<tr><td>Total money in the record, 1948 dollars</td><td>${vMoney(VB.cap0[0])}</td></tr></table>
  <h4>3. Connections count</h4>
  <p class="vtxt">For the other four channels, a tie counts 1 if verified and 0.6 if only reported, multiplied by how connected its two ends are: from 1× for someone with a single tie to 2× for the best-connected node. A tie between two well-connected people (Herzl, Weizmann, Edmond or Walter Rothschild, Balfour) opens more doors than one between two minor figures.</p>
  <h4>4. A document needs someone to give it force</h4>
  <p class="vtxt">A declaration, mandate or resolution counts only while at least one of the bodies that issued or signed it remains. The Balfour Declaration rested on the War Cabinet, Balfour and the British government, and was endorsed by Wilson and Congress; the Mandate rested on San Remo and the League. Remove all of a document's issuers and the document falls too, with everything that leaned on it.</p>
  <h4>5. Every removal is recalculated</h4>
  <p class="vtxt">After each removal the whole network is walked again from the core (the Declaration, the provisional government, the Jewish Agency, the Zionist Organization, the Haganah, Resolution 181). A tie counts only if neither end is gone and it still connects to the core, so a funder cut off from the core no longer counts even if it is still on the map.</p>
  <h4>6. From capacity to a chance</h4>
  <p class="vtxt">Each channel's chance is 1 &minus; e<sup>&minus;k&middot;C/C₀</sup>: C is what still connects, C₀ the full record, and k is set so the full record gives 99%. Spare capacity protects a channel; losses bite harder as it empties. All five were needed, so the overall chance is their product, with money squared: ${Math.round(V0.P)}% on the full record.</p>
  <h4>7. Delay</h4>
  <p class="vtxt">The lost share of each channel is rebuilt at the pace it was first built: money and organization over 51 years from 1897, land over 66 from 1882, arms over 28 from 1920, diplomacy over 31 from 1917. The longest is the delay shown.</p>
  <h4>8. Five readings of every removal</h4>
  <ul><li><b>Founded on time, in 1948</b>: the chance computed above.</li>
  <li><b>Founded by 1958</b> and <b>ever becomes a state</b>: the movement can wait while it rebuilds, but each year waited costs 2% of the chance, because the window of 1947-48 (the end of the Mandate, the UN vote, post-war sympathy, American and Soviet support at the same moment) was closing. The best year to try is chosen; the reading never falls below 1948's. A channel with nothing left cannot regrow from inside the record.</li>
  <li><b>The movement itself survives</b>: money (counted twice) and organization only. A movement can survive while its state is blocked.</li>
  <li><b>Time to rebuild</b>: the delay described in step 7.</li></ul>
  <p class="vtxt">The verdict: <b>Happens on time</b> if the 1948 chance is 85% or more; <b>Still likely, but delayed</b> if it is 70% or more, or the ever chance is 75% or more; <b>Possible, with great difficulty</b> from 55%; <b>Unlikely</b> from 30%; below that, <b>Not possible on this record</b>.</p>
  <h4>The heaviest nodes, each removed alone</h4>
  <table>${heavy.map(n=>`<tr><td>${esc(n.name)}<small style="display:block;color:var(--muted)">${esc(n.qop.viability.read.verdict)}</small></td><td>${n.qop.viability.V}%</td></tr>`).join('')}</table>
  <h4>What it cannot know</h4>
  <p class="vtxt">That someone else might have stepped in; the size of ties with no stated sum; anything the record does not document. Group removals ("Without the United States", "Rothschild family and houses") are in the Remove a node panel.</p>
  <div class="vbtns"><button class="vbtn pri" type="button" data-v="close">Start exploring</button></div>`);
  vLS(VINTRO, 1);
}

/* ---------- the result of a removal ---------- */
function vResult(what, before, ids){
  const R=vScore(removed), cutSet=ids||[...removed], cut=E.filter(e=>cutSet.some(x=>e.f===x||e.t===x)&&e.status!=='co-mention').length;
  const lostM=V0.cap[0]-R.cap[0];
  vOpen(`<div class="kind">Removed from the network</div><h3 id="vmH">${esc(what)}</h3>
  ${vHead(R)}
  <p class="vtxt">${ids?`On time: ${Math.round(before)}% before this removal, ${Math.round(R.P)}% now (${Math.round(V0.P)}% on the full record).`:`Everything removed is read together: ${Math.round(R.P)}% on time now, against ${Math.round(V0.P)}% on the full record.`}</p>
  <h4>The five channels</h4>${vBars(R)}
  <h4>What happened in the graph</h4>
  <ul><li>${cut} documented tie${cut===1?'':'s'} cut.</li>
  ${R.lostDocs.length?`<li>Lost its force: ${R.lostDocs.map(x=>esc(vName(x))).join(', ')} (every body that issued it is gone).</li>`:''}
  <li>Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])}${lostM>0.05?` (${vMoney(lostM)} gone or cut off)`:''}, from ${R.funders} of ${R.funders0} funders.</li>
  <li>${removed.size} node${removed.size===1?'':'s'} removed in total, read together; they stay removed until you reset the graph${removed.size?`: ${[...removed].slice(0,40).map(x=>esc(vName(x))).join(', ')}${removed.size>40?` and ${removed.size-40} more`:''}`:''}.</li></ul>
  ${vDelayText(R)}${vNeed(R)}
  <div class="vbtns"><button class="vbtn pri" type="button" data-v="close">Keep exploring</button>${ids&&ids.length?'<button class="vbtn" type="button" data-v="undo">Undo this removal</button>':''}<button class="vbtn" type="button" data-v="reset">Reset the graph</button><button class="vbtn" type="button" data-v="how">How this is computed</button></div>`);
  vCard.dataset.ids=JSON.stringify(ids||[]); vCard.dataset.drop=JSON.stringify(what==='the United States'?VB.drop['Without the United States']||[]:[]);
}
vCard.addEventListener('click', e=>{ const b=e.target.closest('[data-v]'); if(!b) return; const a=b.dataset.v;
  if(a==='close') vClose();
  else if(a==='how') vIntro();
  else if(a==='reset'){ vClose(); $('reset').click(); }
  else if(a==='undo'){ JSON.parse(vCard.dataset.ids||'[]').forEach(x=>removed.delete(x)); JSON.parse(vCard.dataset.drop||'[]').forEach(x=>vDrop.delete(x)); vClose(); vRefresh(); }
});
function vRefresh(){ vSave(); if(mode==='del'){ const r=reconnect(); hiNodes=r.nodes; hiEdges=r.edges; delPanel(r); } else if(sel) side(sel); draw(); if(calloutId) showCallout(calloutId); }
function vRemove(ids, what, drop){ const before=vScore(removed).P; ids.forEach(x=>removed.add(x)); (drop||[]).forEach(x=>vDrop.add(x)); vRefresh(); vSignal('Removed: '+what, before); }


/* ---------- the signal: a light at the top after every change, gone by itself ---------- */
document.head.insertAdjacentHTML('beforeend', `<style>
.vsig{position:fixed;left:50%;top:calc(10px + env(safe-area-inset-top,0px));z-index:70;width:min(440px,calc(100% - 20px));transform:translate(-50%,-140%);transition:transform .32s cubic-bezier(.2,.85,.25,1),opacity .32s;opacity:0;
  display:grid;grid-template-columns:auto 1fr auto;gap:10px;align-items:start;padding:11px 10px 11px 12px;border-radius:16px;border:1px solid var(--line);background:color-mix(in srgb,var(--panel) 96%,transparent);
  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);box-shadow:0 14px 40px rgba(0,0,0,.35);touch-action:pan-x;cursor:pointer}
.vsig.on{transform:translate(-50%,0);opacity:1}
.vsig .lamp{width:16px;height:16px;border-radius:50%;margin-top:3px;box-shadow:0 0 0 3px color-mix(in srgb,var(--lc) 25%,transparent),0 0 14px var(--lc);background:var(--lc)}
.vsig .t1{font-weight:700;font-size:14px;line-height:1.3}.vsig .t2{font-size:12.5px;line-height:1.45;color:var(--muted);margin-top:2px}
.vsig .t2 b{color:inherit}.vsig .x{border:0;background:transparent;color:var(--muted);font-size:20px;line-height:1;padding:2px 6px;cursor:pointer}
.vsig .bar{grid-column:1/-1;height:2px;border-radius:2px;background:var(--lc);transform-origin:left;opacity:.6}
@media (prefers-reduced-motion:reduce){.vsig{transition:none}}
</style>`);
document.body.insertAdjacentHTML('beforeend','<div class="vsig" id="vSig" role="status" aria-live="polite"></div>');
const vSig=document.getElementById('vSig'); let vSigT=null, vSigY=null;
function vLight(v){ return v==='Happens on time, in 1948'?['#2E9E5B','Green']:(v==='Still likely, but delayed'||v==='Possible, with great difficulty')?['#E0A800','Yellow']:['#D64545','Red']; }
function vSignal(label, before){
  const R=vScore(removed), rd=vRead(R), [lc]=vLight(rd.verdict), d=Math.round(rd.on)-Math.round(before);
  const n=removed.size, what=n?`${n} node${n===1?'':'s'} removed`:'Nothing removed';
  vSig.style.setProperty('--lc', lc);
  vSig.innerHTML=`<span class="lamp" aria-hidden="true"></span><div><div class="t1">${esc(rd.verdict)}${rd.verdict.indexOf('delayed')>=0?` · ~${Math.round(rd.delay)} yrs`:''}</div>
   <div class="t2">${esc(label)} · ${what}<br><b>${Math.round(rd.on)}%</b> on time${d?` (${d>0?'+':''}${d})`:''} · <b>${Math.round(rd.ever)}%</b> ever · movement <b>${Math.round(rd.survive)}%</b> · tap for details</div></div>
   <button class="x" type="button" aria-label="Dismiss">×</button><span class="bar" id="vSigBar"></span>`;
  vSig.classList.add('on'); clearTimeout(vSigT);
  const bar=document.getElementById('vSigBar'); bar.animate([{transform:'scaleX(1)'},{transform:'scaleX(0)'}],{duration:6500,easing:'linear'});
  vSigT=setTimeout(vSigOff, 6500);
}
function vSigOff(){ clearTimeout(vSigT); vSig.classList.remove('on'); vSig.style.transform=''; }
vSig.addEventListener('click', e=>{ if(e.target.closest('.x')){ e.stopPropagation(); vSigOff(); return; } vSigOff(); vResult('The network as it stands', V0.P, null); });
vSig.addEventListener('pointerenter', ()=>{ clearTimeout(vSigT); vSig.getAnimations({subtree:true}).forEach(a=>a.pause()); });
vSig.addEventListener('pointerleave', e=>{ if(e.pointerType==='mouse' && vSig.classList.contains('on')){ vSig.getAnimations({subtree:true}).forEach(a=>a.play()); vSigT=setTimeout(vSigOff, 2500); } });
/* swipe up to dismiss on a phone */
vSig.addEventListener('touchstart', e=>{ vSigY=e.touches[0].clientY; clearTimeout(vSigT); }, {passive:true});
vSig.addEventListener('touchmove', e=>{ if(vSigY==null) return; const dy=Math.min(0,e.touches[0].clientY-vSigY); vSig.style.transition='none'; vSig.style.transform=`translate(-50%,${dy}px)`; }, {passive:true});
vSig.addEventListener('touchend', e=>{ if(vSigY==null) return; const dy=e.changedTouches[0].clientY-vSigY; vSigY=null; vSig.style.transition='';
  if(dy<-30){ vSig.style.transform=''; vSigOff(); e.preventDefault(); } else { vSig.style.transform=''; vSigT=setTimeout(vSigOff, 3000); } });

/* ---------- a small reminder on the graph while anything is removed ---------- */
$('board').insertAdjacentHTML('beforeend','<div class="vpill" id="vPill"><span id="vPillT"></span><button type="button" id="vPillV">Details</button><button type="button" id="vPillR">Reset</button></div>');
function vPill(){ const p=$('vPill'); if(!p) return; const n=removed.size; if(!n&&!vDrop.size){ p.classList.remove('on'); return; }
  const R=vScore(removed); $('vPillT').innerHTML=`${n} removed · <b style="color:${vColor(R.P)}">${Math.round(R.P)}%</b> on time`; p.classList.add('on'); }
$('vPillV').onclick=()=>{ const R=vScore(removed); vOpen(`<div class="kind">The network as it stands</div><h3 id="vmH">${[...removed].map(vName).map(esc).join(', ')||'Scenario'}</h3>
  ${vHead(R)}<h4>The five channels</h4>${vBars(R)}
  <p class="vtxt">Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])}, from ${R.funders} of ${R.funders0} funders.</p>${vDelayText(R)}${vNeed(R)}
  <div class="vbtns"><button class="vbtn pri" type="button" data-v="close">Keep exploring</button><button class="vbtn" type="button" data-v="reset">Reset the graph</button><button class="vbtn" type="button" data-v="how">How this is computed</button></div>`); };
$('vPillR').onclick=()=>$('reset').click();

/* ---------- the reading at the top of the Remove a node panel ---------- */
function viabBlock(){
  const R=vScore(removed), any=removed.size||vDrop.size;
  const opts=Object.keys(VB.groups).map(g=>`<option value="${esc(g)}">${esc(g)} (${VB.groups[g].length})</option>`).join('');
  let h=`<div class="viab"><div class="vlabel">The state&rsquo;s chances, on this record</div>
  ${vHead(R)}${any?`<p class="vtxt">On time: down ${Math.round(V0.P-R.P)} from ${Math.round(V0.P)}%.</p>`:''}${vBars(R)}
  <p class="vtxt">Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])} (1948 dollars), from ${R.funders} of ${R.funders0} funders.</p>`;
  if(any) h+=vDelayText(R)+vNeed(R); else h+=`<p class="vtxt">Tap any node to remove it, or remove a whole group below.</p>`;
  h+=`<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px"><select id="vgrp" class="sel" style="flex:1 1 180px;padding:7px 30px 7px 10px">${opts}</select><button id="vgo" class="ghost" type="button">Remove group</button>${any?'<button id="vclr" class="ghost" type="button">Restore all</button>':''}</div>
  <div class="vbtns" style="margin-top:8px"><button class="vbtn" type="button" id="vhow">How this is computed</button></div></div>`;
  return h;
}
function delPanel(r){ delPanel0(r); $('side').insertAdjacentHTML('afterbegin', viabBlock());
  const go=$('vgo'); if(go) go.onclick=()=>{ const g=$('vgrp').value; vRemove(VB.groups[g], g==='Without the United States'?'the United States':g, VB.drop[g]); };
  const cl=$('vclr'); if(cl) cl.onclick=()=>$('reset').click();
  const hw=$('vhow'); if(hw) hw.onclick=vIntro;
}
/* tapping a node in Remove mode removes it (or restores it) and shows what happened */
const vPick0 = pick;
pick = function(id){ if(mode!=='del') return vPick0(id); const had=removed.has(id), before=vScore(removed).P; vPick0(id); vSave(); vSignal((had?'Restored: ':'Removed: ')+vName(id), before); };
/* every node's summary and record carry a Remove button and its weights */
const vCallout0 = showCallout;
showCallout = function(id){ vCallout0(id); if(!N.get(id)) return; const on=removed.has(id);
  callout.insertAdjacentHTML('beforeend', `<button class="vbtn c-rm${on?'':' pri'}" type="button">${on?'Restore to the network':'Remove from the network'}</button>`);
  callout.querySelector('.c-rm').onclick=ev=>{ ev.stopPropagation(); if(on){ const before=vScore(removed).P; removed.delete(id); vRefresh(); vSignal('Restored: '+vName(id), before); } else vRemove([id], vName(id)); };
  placeCallout(); };
const vSide0 = side;
side = function(id, msg){ vSide0(id, msg); if(!N.get(id)) return; const on=removed.has(id);
  $('side').insertAdjacentHTML('afterbegin', `<div class="viab"><div class="vlabel">${on?'Removed from the network':'If this were removed'}</div>${nodeWeights(id)}
  <div class="vbtns"><button class="vbtn${on?'':' pri'}" type="button" id="vSideRm">${on?'Restore to the network':'Remove from the network'}</button><button class="vbtn" type="button" id="vSideHow">How this is computed</button></div></div>`);
  $('vSideRm').onclick=()=>{ if(on){ const before=vScore(removed).P; removed.delete(id); vRefresh(); vSignal('Restored: '+vName(id), before); } else vRemove([id], vName(id)); };
  $('vSideHow').onclick=vIntro; };
/* restore what the reader removed last time, and explain the model on the first visit */
(function(){ const s=vLS(VKEY); if(s){ (s.removed||[]).forEach(x=>{ if(N.get(x)) removed.add(x); }); (s.drop||[]).forEach(x=>vDrop.add(x)); }
  setTimeout(()=>{ vPill(); if(removed.size) draw(); if(!vLS(VINTRO)) vIntro(); }, 600); })();
