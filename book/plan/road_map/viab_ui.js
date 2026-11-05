/* ---------- viability reading (road map only); mirrors viability.py ---------- */
const VB = DATA.viab;
const vDrop = new Set();          // ties dropped by a scenario (money raised in the US but carried by a non-American)
function vReach(rem){ const adj=new Map(); for(const [f,t] of VB.edges){ if(rem.has(f)||rem.has(t)||vDrop.has(f+'>'+t)) continue; (adj.get(f)||adj.set(f,[]).get(f)).push(t); (adj.get(t)||adj.set(t,[]).get(t)).push(f); }
  const seen=new Set(VB.core.filter(x=>!rem.has(x))), q=[...seen]; while(q.length){ const u=q.pop(); for(const v of adj.get(u)||[]) if(!seen.has(v)){ seen.add(v); q.push(v); } } return seen; }
function vScore(rem){ const seen=vReach(rem), cap=[0,0,0,0,0], ties=[0,0,0,0,0], ties0=[0,0,0,0,0], funders=new Set(), funders0=new Set();
  for(const [f,t,c,w,v] of VB.edges){ ties0[c]++; if(c===0) funders0.add(f);
    if(rem.has(f)||rem.has(t)||vDrop.has(f+'>'+t)) continue; if(seen.has(f)||seen.has(t)){ cap[c]+=v; ties[c]++; if(c===0) funders.add(f); } }
  const k=-Math.log(1-VB.cal), pc=cap.map((x,i)=>VB.cap0[i]?1-Math.exp(-k*x/VB.cap0[i]):1), share=cap.map((x,i)=>VB.cap0[i]?x/VB.cap0[i]:1);
  const P=pc.reduce((a,b)=>a*b,100), delay=share.map((r,i)=>VB.tbuild[i]*(1-r));
  return {P,pc,share,delay,cap,ties,ties0,funders:funders.size,funders0:funders0.size}; }
const V0 = vScore(new Set());
function vRating(V){ return V>=90?'Still possible':V>=75?'Still possible, with more work':V>=55?'Possible only with major outside help':V>=35?'Doubtful':V>=15?'Very unlikely':'Not possible on this record'; }
function vColor(V){ return V>=75?'var(--ver)':V>=35?'var(--tov)':'var(--nest)'; }
function vMoney(m){ return m>=1?'$'+(Math.round(m*10)/10)+' million':'$'+Math.round(m*1000)+',000'; }
function viabBlock(){
  const R=vScore(removed), any=removed.size||vDrop.size, md=Math.max(...R.delay), mi=R.delay.indexOf(md);
  const weak=R.pc.map((x,i)=>[x,i]).filter(([x])=>x<0.95).sort((a,b)=>a[0]-b[0]);
  const opts=Object.keys(VB.groups).map(g=>`<option value="${esc(g)}">${esc(g)} (${VB.groups[g].length})</option>`).join('');
  const row=(lab,val,txt)=>`<div style="display:grid;grid-template-columns:118px 1fr 46px;gap:8px;align-items:center;font-size:12.5px;margin:3px 0"><span>${lab}</span><span style="height:7px;border-radius:4px;background:var(--line);overflow:hidden"><i style="display:block;height:100%;width:${Math.round(val*100)}%;background:${vColor(val*100)}"></i></span><span style="text-align:right;font-family:var(--f-mono)">${txt}</span></div>`;
  let h=`<div class="viab" style="border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:0 0 14px;background:color-mix(in srgb,var(--panel-2) 60%,transparent)">
  <div class="kind">Chance the state is founded in 1948, on this record</div>`;
  h+=`<div style="display:flex;align-items:baseline;gap:10px;margin:6px 0 2px;flex-wrap:wrap"><b style="font:700 2rem/1 var(--f-display);color:${vColor(R.P)}">${Math.round(R.P)}%</b><span style="font-weight:600">${vRating(R.P)}</span>${any?`<span class="note" style="margin:0">down ${Math.round(V0.P-R.P)} from ${Math.round(V0.P)}%</span>`:''}</div>`;
  h+=VB.channels.map((c,i)=>row(esc(VB.labels[c]),R.pc[i],Math.round(R.pc[i]*100)+'%')).join('');
  h+=`<p class="note" style="margin:8px 0 0">Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])} (1948 dollars), from ${R.funders} of ${R.funders0} funders.</p>`;
  if(any){
    if(R.pc.some(p=>p<0.005)) h+=`<p class="note" style="margin:6px 0 0"><b>On this record the state is not founded.</b> ${esc(VB.labels[VB.channels[R.pc.indexOf(Math.min(...R.pc))]])} is gone entirely. Rebuilding it at the pace it was first built (from ${esc(VB.tfrom[mi])}) would take about ${Math.round(md)} years.</p>`;
    else if(md>=1) h+=`<p class="note" style="margin:6px 0 0">Likely delay: about <b>${Math.round(md)} years</b> (founding around ${1948+Math.round(md)}), the time to rebuild the lost ${esc(VB.labels[VB.channels[mi]].toLowerCase())} at the pace it was first built, from ${esc(VB.tfrom[mi])}.</p>`;
    if(weak.length) h+=`<p class="note" style="margin:6px 0 0">To make up the loss the movement would need ${weak.slice(0,2).map(([x,i])=>esc(VB.need[VB.channels[i]])).join(', and ')}.</p>`;
    else h+=`<p class="note" style="margin:6px 0 0">The rest of the documented network covers what this removal takes away.</p>`;
  } else h+=`<p class="note" style="margin:6px 0">Tap any node to remove it, or remove a whole group below. Every removal is recalculated against the rest of the network.</p>`;
  h+=`<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px"><select id="vgrp" class="sel" style="flex:1 1 180px;padding:7px 30px 7px 10px">${opts}</select><button id="vgo" class="ghost" type="button">Remove group</button>${any?'<button id="vclr" class="ghost" type="button">Restore all</button>':''}</div>
  <details style="margin-top:10px;font-size:12.5px;color:var(--muted)"><summary style="cursor:pointer">How this is computed</summary>
  <p>This is a model built on the map, not a measured historical probability. It reads only the documented ties dated before 1949 (${VB.edges.length} of them). Each supportive tie goes to one of five channels the state needed: money; land and settlers; arms and force; diplomacy and law; organization. Ties of opposition or violence, ties on the Arab or Nazi side, and money that did not go to the project (such as Rothschild loans to the British treasury) are left out.</p>
  <p><b>Weights.</b> A money tie is weighted by its sum in 1948 dollars where the record states one (${Object.keys(VB.amounts).length} ties: ${Object.values(VB.amounts).map(a=>esc(a[1])).join('; ')}). Francs are converted at the gold parity of 5.18 to the dollar and older sums brought to 1948 prices with the US consumer price index. A money tie with no stated sum is assumed to carry ${vMoney(VB.default_m)}; that is an assumption, not a finding. Other ties weigh 1 if verified and 0.6 if only reported. A node's weight is the share of each channel carried by its own ties.</p>
  <p><b>Recalculation.</b> After any removal the whole network is walked again: a tie still counts only if neither end is gone and it still connects, through supportive ties, to the core (the Declaration, the provisional government, the Jewish Agency, the Zionist Organization, the Haganah, Resolution 181). A funder cut off from the core no longer counts, even if it is still on the map.</p>
  <p><b>Probability.</b> Each channel's chance is 1 &minus; e<sup>&minus;k&middot;C/C₀</sup>, where C is the capacity still connected and C₀ the full record's; k is set so the full record gives 99% per channel. Spare capacity therefore protects a channel, and losses bite harder as it empties. All five were needed, so the overall chance is their product (${Math.round(V0.P)}% on the full record).</p>
  <p><b>Delay.</b> The lost share of a channel is rebuilt at the pace it was first built: money and organization over 51 years from 1897, land over 66 years from 1882, arms over 28 years from 1920, diplomacy over 31 years from 1917. The longest of the five is the delay shown.</p>
  <p><b>The United States scenario</b> removes American government, parties, Zionist organizations and US-based funders and arms buyers, and drops money raised in America but carried by others (Golda Meyerson's 1948 tour).</p>
  <p>What it cannot know: that someone else might have stepped in, the size of ties with no stated sum, or anything the record does not document.</p></details></div>`;
  return h;
}
function delPanel(r){ delPanel0(r); $('side').insertAdjacentHTML('afterbegin', viabBlock());
  const go=$('vgo'); if(go) go.onclick=()=>{ const g=$('vgrp').value; VB.groups[g].forEach(x=>removed.add(x)); (VB.drop[g]||[]).forEach(x=>vDrop.add(x)); const rr=reconnect(); hiNodes=rr.nodes; hiEdges=rr.edges; delPanel(rr); draw(); };
  const cl=$('vclr'); if(cl) cl.onclick=()=>{ removed.clear(); vDrop.clear(); hiNodes=new Set(); hiEdges=new Set(); delPanel(reconnect()); draw(); };
}
