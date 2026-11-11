/* ---------- survival model (road map only); mirrors viability.py ---------- */
const VB = DATA.viab;
const vDrop = new Set();          // ties dropped by a scenario (money raised in the US but carried by a non-American)
const VKEY = 'road_removed_v1', VINTRO = 'road_model_intro_v1';
function vLS(k, v){ try{ if(v === undefined) return JSON.parse(localStorage.getItem(k) || 'null'); if(v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v)); }catch(e){ return null; } }
let vMode = vLS('road_vote_mode') || VB.vote_mode;
let vStrict = !!vLS('road_strict_v1');
const vNoVote = new Set();   /* states that keep their record but do not cast their partition vote (a test scenario) */
const vFlip = new Set();     /* yes-voters that vote against instead (a test scenario) */   /* the stricter reading: a document cannot be issued without its named addressee */
/* Resolution 181 needs two-thirds of the votes cast: at least twice as many for as against */
function vVote(out){ const yes=VB.vote.yes, no=VB.vote.no;
  const fl=yes.filter(x=>vFlip.has(x)&&!out.has(x)).length, yr=yes.filter(x=>(out.has(x)||vNoVote.has(x))&&!vFlip.has(x)).length, nr=no.filter(x=>out.has(x)).length;
  const y=yes.length-yr-fl, n=no.length-nr+fl+(vMode==='against'?yr:0), unGone=out.has('un')||out.has('unga');
  return {yes:y, no:n, abstain:VB.vote.abstain.length+nr+(vMode==='against'?0:yr), passes:y>=2*n&&!unGone, need:2*n, unGone, yr, fl}; }
/* blocs: without its leader, a member that followed it keeps its yes (and its 1948 recognition) only at the bloc's independence */
function vLeaderOut(B, rem){ const L=B.leader; return rem.has(L)||vNoVote.has(L)||vFlip.has(L); }
function vPassProb(rem){ const v=vVote(rem); if(!v.passes) return 0; const yes=new Set(VB.vote.yes), unsure=[];
  for(const B of VB.blocs){ if(!vLeaderOut(B,rem)) continue; for(const m of B.members) if(yes.has(m)&&!rem.has(m)&&!vNoVote.has(m)&&!vFlip.has(m)) unsure.push(1-B.follow); }
  if(!unsure.length) return 1; const sure=v.yes-unsure.length, n=v.no; let dist=[1];
  for(const p of unsure){ const nd=Array(dist.length+1).fill(0); dist.forEach((q,k)=>{ nd[k]+=q*(1-p); nd[k+1]+=q*p; }); dist=nd; }
  let ok=0; dist.forEach((q,k)=>{ const y=sure+k, nn=n+(vMode==='against'?unsure.length-k:0); if(y>=2*nn) ok+=q; }); return ok; }
function vLost(rem){ const out=new Set(rem); let ch=true; while(ch){ ch=false; for(const [doc,iss] of Object.entries(VB.issuers)){ if(!out.has(doc) && iss.length && iss.every(i=>out.has(i))){ out.add(doc); ch=true; } }
  if(!out.has('res181') && !vVote(out).passes){ out.add('res181'); ch=true; }
  for(const [dep,src] of VB.incorp) if(out.has(src)&&!out.has(dep)&&!VB.core.includes(dep)){ out.add(dep); ch=true; }
  for(const [doc,fw] of Object.entries(VB.framework)) if(!out.has(doc)&&fw.needs.some(x=>out.has(x))){ out.add(doc); ch=true; }
  if(vStrict) for(const [doc,who] of Object.entries(VB.addressee)) if(!out.has(doc)&&who.length&&who.every(x=>out.has(x))){ out.add(doc); ch=true; } } return out; }
function vVoteLine(rem0){ const v=vVote(vLost(rem0));
  if(v.unGone) return `<b>The UN partition vote cannot happen</b>: without the United Nations there is no General Assembly to hold it.`;
  return `UN partition vote: <b>${v.yes} for, ${v.no} against</b>, ${v.abstain} abstaining. ${v.passes?`<b>Passes</b> (two-thirds needed: at least ${v.need} for).`:`<b>Fails</b>: two-thirds of the votes cast were needed, at least ${v.need} for.`}${v.yr?` ${v.yr} removed yes-vote${v.yr===1?'':'s'} counted as ${vMode==='against'?'votes against':'abstentions'}.`:''}${v.fl?` ${v.fl} yes-vote${v.fl===1?'':'s'} turned into vote${v.fl===1?'':'s'} against.`:''}`; }
function vReach(rem){ const adj=new Map(); for(const [f,t] of VB.edges){ if(rem.has(f)||rem.has(t)||vDrop.has(f+'>'+t)) continue; (adj.get(f)||adj.set(f,[]).get(f)).push(t); (adj.get(t)||adj.set(t,[]).get(t)).push(f); }
  const seen=new Set(VB.core.filter(x=>!rem.has(x))), q=[...seen]; while(q.length){ const u=q.pop(); for(const v of adj.get(u)||[]) if(!seen.has(v)){ seen.add(v); q.push(v); } } return seen; }
const vDecider = {};   /* a test can name who decides instead (for example Roosevelt in place of Truman) */
function vDecisionChance(D, rem, dec0){ let dec=dec0||D.decider; const tied=VB.tied, orig=D.decider;
  if(rem.has(dec)) dec=(D.successor&&!rem.has(D.successor))?D.successor:null;
  if(!dec) return [0, null];
  let S=0, O=0;
  for(const l of D.levers){ if(rem.has(l)||l===dec) continue; const personal=(tied[orig]||[]).includes(l);
    if(personal&&dec!==orig&&!(dec&&(tied[dec]||[]).includes(l))) continue; S++; }
  for(const o of D.oppose) if(!rem.has(o)) O++;
  const st=dec!==orig?(VB.stance[dec]||0):0; S+=Math.max(0,st); O+=Math.max(0,-st);
  if(dec&&dec!==orig&&!(dec in VB.stance)){ const u=VB.unknown_successor==null?1:VB.unknown_successor; S+=u; O+=u; }
  return [S+O?S/(S+O):0, dec]; }
/* holistic reading: the base reading averaged over whether each key decision still happens */
function vScore(rem0){ const rel=[];
  for(const D of VB.decisions){ const p0=vDecisionChance(D,new Set())[0], [p,dec]=vDecisionChance(D,rem0,vDecider[D.id]), r=p0?Math.min(1,p/p0):1;
    if(r<0.999&&!rem0.has(D.act)) rel.push([D,Math.round(r*1e4)/1e4,dec]); }
  const lf=vLost(rem0), pv=lf.has('res181')?1:vPassProb(lf);
  if(pv<0.999) rel.push([{id:'un_vote',name:'The UN partition vote, with blocs following their leaders',act:'res181',effects:{remove:['res181']}},Math.round(pv*1e4)/1e4,null]);
  if(!rel.length){ const R=vScoreBase(rem0); R.decisions=[]; return R; }
  const mix=[], sd=new Set(vDrop), sn=new Set(vNoVote), sf=new Set(vFlip);
  for(let m=0;m<(1<<rel.length);m++){ let w=1; const rem2=new Set(rem0);
    rel.forEach(([D,r],i)=>{ if(m>>i&1){ w*=1-r; const E=D.effects; (E.remove||[]).forEach(x=>rem2.add(x)); (E.drop||[]).forEach(x=>vDrop.add(x)); (E.novote||[]).forEach(x=>vNoVote.add(x)); (E.flip||[]).forEach(x=>vFlip.add(x)); } else w*=r; });
    if(w>1e-6) mix.push([w, vScoreBase(rem2)]);
    vDrop.clear(); sd.forEach(x=>vDrop.add(x)); vNoVote.clear(); sn.forEach(x=>vNoVote.add(x)); vFlip.clear(); sf.forEach(x=>vFlip.add(x)); }
  const top=mix.reduce((a,b)=>b[0]>a[0]?b:a)[1];
  return Object.assign({}, top, {P:mix.reduce((a,[w,x])=>a+w*x.P,0), mix, decisions:rel.map(([D,r,dec])=>({id:D.id,name:D.name,chance:r,decider:dec}))}); }
function vScoreBase(rem0){ const rem=vLost(rem0), keep={}; for(const B of VB.blocs){ if(rem.has(B.leader)||vDrop.has(B.leader+'>decl_indep')) for(const m of B.members) keep[m]=Math.min(keep[m]??1,1-B.follow); } const _k=keep, seen=vReach(rem), cap=VB.channels.map(()=>0), ties=VB.channels.map(()=>0), ties0=VB.channels.map(()=>0), funders=new Set(), funders0=new Set();
  for(const [f,t,c,w,v] of VB.edges){ ties0[c]++; if(c===0&&v>0) funders0.add(f);
    if(rem.has(f)||rem.has(t)||vDrop.has(f+'>'+t)) continue; if(seen.has(f)||seen.has(t)){ cap[c]+=v*(c===5?(_k[f]??1):1); ties[c]++; if(c===0&&v>0) funders.add(f); } }
  const nocarrier=VB.carriers.length>0&&VB.carriers.every(c=>rem.has(c)); if(nocarrier){ cap.fill(0); funders.clear(); }
  const k=-Math.log(1-VB.cal), pc=cap.map((x,i)=>VB.cap0[i]?1-Math.exp(-k*x/VB.cap0[i]):1), share=cap.map((x,i)=>VB.cap0[i]?x/VB.cap0[i]:1);
  const years=(vDrop.size||[...rem].some(x=>VB.actors[x]||VB.framework[x]))?vYears(rem,vDrop):{L:0,per:{},who:{}}, tau=Math.max(0,1-years.L/(VB.y1-VB.y0));
  const P=pc.reduce((a,b,i)=>a*Math.pow(b,VB.exp[i]),100)*tau, delay=share.map((r,i)=>r>0.001?Math.min(200,VB.tbuild[i]*(1-r)/r):200);
  const lostDocs=[...rem].filter(x=>!rem0.has(x));
  return {P,pc,share,delay,cap,ties,ties0,funders:funders.size,funders0:funders0.size,lostDocs,nocarrier,years,tau}; }
const V0 = vScore(new Set());

/* five readings of one removal (mirrors viability.readings) */

/* lost years and substitutes (mirrors viability.lost_years) */
function vYears(rem, drop){ const A=VB.actors, ids=Object.keys(A), NCh=VB.channels.length, y0=VB.y0, Ys=VB.y1-VB.y0+1;
  const Z=()=>Array.from({length:NCh},()=>new Float64Array(Ys)), cap={}, live={}, avail={};
  for(const i of ids){ cap[i]=Z(); live[i]=Z(); avail[i]=Z(); }
  VB.edges.forEach(([f,t,c,w,v],n)=>{ if(!VB.year_ch.includes(c)||!v) return; const [ea,eb]=VB.eyear[n], dropped=drop.has(f+'>'+t);
    for(const [x,o] of [[f,t],[t,f]]){ if(!cap[x]) continue; const s0=A[x][0], s1=A[x][1]; let a,b;
      if(ea){ a=ea; b=eb; } else if(A[o]&&Math.max(s0,A[o][0])<=Math.min(s1,A[o][1])){ a=Math.max(s0,A[o][0]); b=Math.min(s1,A[o][1]); } else { a=s0; b=s1; }
      let rate=v/(b-a+1), lo=Math.max(a,s0), hi=Math.min(b,s1); if(lo>hi){ lo=hi=Math.min(Math.max(a,s0),s1); rate=v; }
      for(let y=lo;y<=hi;y++){ cap[x][c][y-y0]+=rate; if(!(rem.has(x)||dropped)) live[x][c][y-y0]+=rate; if(!(rem.has(f)||rem.has(t)||dropped)) avail[x][c][y-y0]+=rate; } } });
  let total=0; const per={}, who={}, S=Array(NCh).fill(0), D=Array(NCh).fill(0), Da={}, cum={};
  for(const i of ids) cum[i]=Array(NCh).fill(0);
  const Sfin=[]; for(let k=0;k<NCh;k++){ let s=0; for(const i of ids) for(let j=0;j<Ys;j++) s+=cap[i][k][j]; Sfin.push(s); }
  const lostAt={}; for(const a of ids){ lostAt[a]=[]; for(let k=0;k<NCh;k++){ let q=false; for(let j=0;j<Ys;j++) if(cap[a][k][j]-live[a][k][j]>1e-9){ q=true; break; } lostAt[a].push(q); } }
  const material=VB.material==null?0.05:VB.material;
  for(let y=VB.y0;y<=VB.y1;y++){ const j=y-y0, F=Array(NCh).fill(0);
    for(const k of VB.year_ch){ for(const i of ids) cum[i][k]+=avail[i][k][j]; let tot=0; for(const i of ids) tot+=cap[i][k][j];
      for(const a of ids){ if(!lostAt[a][k]) continue; const l=cap[a][k][j]-live[a][k][j]; if(l<=1e-9) continue;
        let best=null, bc=0; for(const b of ids){ if(b===a||rem.has(b)||A[b][2]!==A[a][2]||A[b][0]>y) continue; const rb=cum[b][k]/(y-A[b][0]+1); if(rb>bc){ best=b; bc=rb; } }
        const cov=best?Math.min(1,bc/l):0, u=l*(1-cov); D[k]+=u; (Da[a]||(Da[a]=Array(NCh).fill(0)))[k]+=u;
        const r=who[a]||(who[a]={s:A[a][0],e:A[a][1],years:0,ch:null,subs:{},w:0,yk:{}}); if(tot&&l/tot>r.w){ r.ch=k; r.w=l/tot; }
        if(best){ const q=r.subs[k]; if(!q||cov>q[1]) r.subs[k]=[best,Math.round(cov*100)/100,A[best][0]]; } }
      S[k]+=tot;
      if(S[k]>0&&S[k]>=material*Sfin[k]){ F[k]=VB.stock===false?0:Math.min(1,D[k]/S[k]); for(const a in Da) if(Da[a][k]>0) who[a].yk[k]=(who[a].yk[k]||0)+Da[a][k]/S[k]; } }
    for(const [doc,fw] of Object.entries(VB.framework)) if(rem.has(doc)&&fw.y[0]<=y&&y<=fw.y[1]){ F[fw.ch]=Math.max(F[fw.ch],fw.loss);
      const r=who[doc]||(who[doc]={s:fw.y[0],e:fw.y[1],years:0,ch:fw.ch,subs:{},w:fw.loss,yk:{},framework:true}); r.yk[fw.ch]=(r.yk[fw.ch]||0)+fw.loss; }
    const f=Math.max(...F); per[y]=Math.round(f*1000)/1000; total+=f; }
  for(const a in who){ const r=who[a]; if(r.ch!=null) r.years=r.yk[r.ch]||0; }
  return {L:total, per, who}; }
function vDecText(R){ if(!R.decisions||!R.decisions.length) return '';
  return `<ul class="vul">${R.decisions.map(x=>{ if(x.id==='un_vote') return `<li><b>${esc(x.name)}</b>: chance it still reaches two-thirds: <b>${Math.round(x.chance*100)}%</b>. A bloc whose leader is out keeps only its members' independent votes.</li>`; const D=VB.decisions.find(d=>d.id===x.id); return `<li><b>${esc(x.name)}</b>: ${x.decider?`decided by ${x.decider==='*'?'an unnamed successor':esc(vName(x.decider))}${x.decider!==D.decider?` instead of ${esc(vName(D.decider))}`:''}`:'no one documented left to decide'}; chance it still happens, against the record: <b>${Math.round(x.chance*100)}%</b>.</li>`; }).join('')}</ul>
  <p class="vtxt">A decision's chance is the documented push over push plus resistance, around whoever decides. Push aimed at the man himself (his staff, friends and correspondents) does not pass to a successor without his own documented tie; resistance stays.</p>`; }
function vYearsText(R){ if(!R.years||R.years.L<0.5) return R.years&&Object.keys(R.years.who).length?`<p class="vtxt">No years of work lost: documented actors already active at the time could carry what was taken out.</p>`:'';
  const Y=R.years, rows=Object.entries(Y.who).filter(([a,r])=>r.years>=0.5).sort((a,b)=>b[1].years-a[1].years).slice(0,5);
  const lostY=Object.entries(Y.per).filter(([y,f])=>f>=0.5).map(([y])=>+y), span=lostY.length?` (hardest hit: ${lostY[0]}${lostY.length>1?'–'+lostY[lostY.length-1]:''})`:'';
  return `<p class="vtxt"><b>About ${Math.round(Y.L)} years of the movement's work lost</b>${span}. That slows the founding in proportion: the on-time chance is multiplied by ${Math.round(R.tau*100)}%, the share of the 66 build-up years (1882–1948) still delivered.</p>
  <ul class="vul">${rows.map(([a,r])=>{ const ch=r.ch, q=r.subs[ch];
    if(r.framework) return `<li><b>${esc(vName(a))}</b> falls, so from ${r.s} to ${r.e} immigration and settlement go at the Ottoman-era pace: about 2,200 people a year instead of about 21,900. About ${Math.round(r.years)} years of land and settlement work lost.</li>`;
    return `<li><b>${esc(vName(a))}</b>, active ${r.s}${r.e>r.s?'–'+r.e:''}, carried ${Math.round(r.w*100)}% of the ${esc(VB.labels[VB.channels[ch]].toLowerCase())} work at its height. ${q?`Closest documented substitute: <b>${esc(vName(q[0]))}</b>, active from ${q[2]}, able to carry about ${Math.round(q[1]*100)}% of that role${q[2]>r.s?`; before ${q[2]} no one documented could`:''}.`:'No documented substitute in that role.'} About ${Math.round(r.years)} years of that role lost.</li>`; }).join('')}</ul>`; }
function vRead(R){ if(R.mix){ const parts=R.mix.map(([w,x])=>[w,vRead1(x)]), out={};
    for(const k of ['on','delay','survive','lost','by1958','by1978','ever']) out[k]=parts.reduce((a,[w,p])=>a+w*p[k],0);
    out.retry=parts.reduce((a,b)=>b[0]>a[0]?b:a)[1].retry; out.nocarrier=parts.every(([w,p])=>p.nocarrier);
    for(const [cut,key,txt] of VB.verdict) if(out[key]>=cut){ out.verdict=txt; break; } return out; }
  return vRead1(R); }
function vRead1(R){ const k=-Math.log(1-VB.cal), P0=R.P/100, Ly=R.years?R.years.L:0, D=Math.max(Math.max(...R.delay),Ly), Lmin=Math.ceil(Ly);
  const Pat=sh=>sh.reduce((p,x,i)=>p*Math.pow(1-Math.exp(-k*x),VB.exp[i]),1);
  const out={on:100*P0, delay:D, lost:Ly, survive:100*Math.pow(R.pc[0],2)*R.pc[4]}; let best=0, tb=0;
  for(let t=1;t<=100;t++){ const sh=R.share.map((s,i)=>s>0.001?Math.min(1,s*(1+t/VB.tbuild[i])):0), p=t>=Lmin?Pat(sh)*Math.exp(-VB.hazard*t):0; if(p>best){ best=p; tb=t; } if(VB.horizons.includes(t)) out['by'+(1948+t)]=100*Math.max(P0,best); }
  out.ever=100*Math.max(P0,best); out.retry=best>P0?1948+tb:null; out.nocarrier=!!R.nocarrier;
  for(const [cut,key,txt] of VB.verdict) if(out[key]>=cut){ out.verdict=txt; break; }
  return out; }
function vReadTable(rd){ const row=(l,v,sub)=>`<tr><td>${l}${sub?`<small style="display:block;color:var(--muted)">${sub}</small>`:''}</td><td style="color:${vColor(v)}">${Math.round(v)}%</td></tr>`;
  return `<table class="vread">${row('Founded on time, in 1948',rd.on)}${row('Founded by 1958',rd.by1958, rd.retry&&rd.retry<=1958?'best year to try again: '+rd.retry:'')}${row('Ever becomes a state',rd.ever,'later attempts lose 2% a year as the 1947-48 window closes')}${row('The movement itself survives',rd.survive,'keeps its money and organization, whatever happens to the state')}
  <tr><td>Years of the movement's work lost</td><td>${rd.lost<0.5?'none':'about '+Math.round(rd.lost)}</td></tr><tr><td>Time to rebuild what was lost</td><td>${rd.nocarrier?'no one left':rd.delay<1?'none':rd.delay>100?'over a century':'about '+Math.round(rd.delay)+' yrs'}</td></tr></table>`; }
function vHead(R){ const rd=vRead(R); return `<div class="vbig"><b style="color:${vColor(rd.on)}">${Math.round(rd.on)}%</b><span style="font-weight:600">${esc(rd.verdict)}${rd.verdict.indexOf('delayed')>=0?` (about ${Math.round(rd.delay)} years)`:''}</span></div>${vReadTable(rd)}`; }
function vRating(V){ return V>=90?'Still possible':V>=75?'Still possible, with more work':V>=55?'Possible only with major outside help':V>=35?'Doubtful':V>=15?'Very unlikely':'Not possible on this record'; }
function vColor(V){ return V>=75?'var(--ver)':V>=35?'var(--tov)':'var(--nest)'; }
const TDY48=1001.3/72.2;
function vToday(m){ const x=m*TDY48; return x>=1000?'$'+(Math.round(x/100)/10)+' billion':x>=10?'$'+Math.round(x)+' million':x>=1?'$'+(Math.round(x*10)/10)+' million':'$'+(Math.round(x*1000)*1000).toLocaleString('en-US'); }
function vMoney(m){ const b=m>=1?'$'+(Math.round(m*10)/10)+' million':'$'+Math.round(m*1000)+',000'; return b+' (≈ '+vToday(m)+' today)'; }
function vName(x){ const n=N.get(x); return n?n.name:x; }
function vSave(){ vLS(VKEY, removed.size||vDrop.size||vNoVote.size||vFlip.size ? {removed:[...removed], drop:[...vDrop], novote:[...vNoVote], flip:[...vFlip]} : null); vPill(); }
function vBars(R){ return VB.channels.map((c,i)=>`<div class="vrow"><span>${esc(VB.labels[c])}${VB.exp[i]>1?' <em>×2</em>':''}</span><span class="vbar"><i style="width:${Math.round(R.pc[i]*100)}%;background:${vColor(R.pc[i]*100)}"></i></span><span class="vnum">${Math.round(R.pc[i]*100)}%</span></div>`).join(''); }
function vDelayText(R){ const md=Math.max(...R.delay), mi=R.delay.indexOf(md);
  if(R.nocarrier) return `<p class="vtxt"><b>No one is left to pursue the state.</b> The Zionist Organization, the Jewish Agency and the Jewish National Council (Va'ad Leumi) are all removed; on this record nothing else carried the goal, so every channel counts as empty.</p>`;
  if(R.pc.some(p=>p<0.005)) return `<p class="vtxt"><b>On this record the state is not founded.</b> ${esc(VB.labels[VB.channels[R.pc.indexOf(Math.min(...R.pc))]])} is gone entirely. Rebuilding it at the pace it was first built (from ${esc(VB.tfrom[mi])}) would take about ${Math.round(md)} years.</p>`;
  if(md>=1){ const rd=vRead(R); return `<p class="vtxt">Rebuilding the lost ${esc(VB.labels[VB.channels[mi]].toLowerCase())} fully would take ${md>100?'<b>over a century</b>':`about <b>${Math.round(md)} years</b>`}: the network that is left rebuilds it, at the pace the channel was first built (from ${esc(VB.tfrom[mi])}) scaled down to the share that remains.${rd.retry?` Because the 1947-48 window was closing, the best chance of a later founding comes sooner, around <b>${rd.retry}</b>, with what has been rebuilt by then.`:' Waiting would not raise the chance: the window was closing faster than the loss could be rebuilt.'}</p>`; }
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

.vmodal.ipm{background:radial-gradient(90% 70% at 50% 8%,rgba(40,30,70,.42),rgba(3,6,14,.86));-webkit-backdrop-filter:blur(7px);backdrop-filter:blur(7px)}
.vcard.ivc{--ia:var(--gold);position:relative;width:min(660px,100%);max-height:min(780px,calc(100dvh - 32px));padding:0;display:flex;flex-direction:column;overflow:hidden;border-radius:26px;border:1px solid color-mix(in srgb,var(--ia) 42%,var(--line));background:radial-gradient(120% 65% at 0% 0%,color-mix(in srgb,var(--ia) 22%,transparent),transparent 62%),radial-gradient(80% 55% at 100% 100%,color-mix(in srgb,var(--ia) 13%,transparent),transparent 66%),linear-gradient(180deg,color-mix(in srgb,var(--panel-2) 78%,var(--panel)),var(--panel));box-shadow:0 44px 110px rgba(0,0,0,.6),0 0 60px -20px color-mix(in srgb,var(--ia) 55%,transparent),inset 0 1px 0 color-mix(in srgb,var(--ia) 40%,transparent);transition:border-color .4s,box-shadow .4s}
.vcard.ivc::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,transparent,var(--ia) 30%,var(--ia) 70%,transparent);z-index:3}
.ip-wm{position:absolute;right:20px;top:46px;font:900 150px/1 var(--f-display);color:var(--ia);opacity:.07;pointer-events:none;user-select:none;letter-spacing:-.04em;z-index:0;transition:color .4s}
.ip-top{position:relative;z-index:2;display:flex;align-items:center;gap:14px;padding:18px 18px 4px 22px}
.ip-prog{flex:1;display:flex;gap:5px}
.ip-prog i{position:relative;flex:1;height:4px;border-radius:4px;background:color-mix(in srgb,var(--ink) 13%,transparent);overflow:hidden}
.ip-prog i::after{content:"";position:absolute;inset:0;border-radius:4px;background:var(--seg);transform:scaleX(0);transform-origin:left;transition:transform .45s cubic-bezier(.2,.8,.2,1)}
.ip-prog i.done::after,.ip-prog i.on::after{transform:scaleX(1)}
.ip-prog i.on::after{box-shadow:0 0 12px var(--seg)}
.ip-x{flex:none;width:34px;height:34px;border-radius:50%;border:1px solid color-mix(in srgb,var(--ink) 18%,transparent);background:color-mix(in srgb,var(--ink) 6%,transparent);color:var(--muted);font:400 20px/1 var(--f-body);cursor:pointer;display:grid;place-items:center;transition:background .2s,color .2s}
.ip-x:hover,.ip-x:focus-visible{background:color-mix(in srgb,var(--ia) 22%,transparent);color:var(--ink);outline:none}
.ip-body{position:relative;z-index:1;flex:1;min-height:0;overflow:auto;-webkit-overflow-scrolling:touch;padding:16px 24px 20px;scrollbar-width:thin;scrollbar-color:color-mix(in srgb,var(--ia) 55%,transparent) transparent;-webkit-mask-image:linear-gradient(transparent 0,#000 14px,#000 calc(100% - 26px),transparent 100%);mask-image:linear-gradient(transparent 0,#000 14px,#000 calc(100% - 26px),transparent 100%)}
.ip-page.inr{animation:ipR .38s cubic-bezier(.2,.8,.2,1) both}.ip-page.inl{animation:ipL .38s cubic-bezier(.2,.8,.2,1) both}
@keyframes ipR{from{opacity:0;transform:translateX(30px)}to{opacity:1;transform:none}}
@keyframes ipL{from{opacity:0;transform:translateX(-30px)}to{opacity:1;transform:none}}
.ip-k{font:600 11px/1 var(--f-mono);letter-spacing:.18em;text-transform:uppercase;color:var(--ia);display:flex;align-items:center;gap:10px}
.ip-k::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,color-mix(in srgb,var(--ia) 55%,transparent),transparent)}
.vcard.ivc .ip-t{font:700 1.8rem/1.14 var(--f-display);letter-spacing:-.012em;margin:14px 0 6px;max-width:90%;color:var(--ink)}
.ip-sub{font-size:13.5px;line-height:1.5;color:var(--muted);margin:0 0 6px;max-width:92%}
.ip-s{margin-top:14px;padding:14px 16px 8px;border-radius:16px;border:1px solid color-mix(in srgb,var(--ia) 20%,var(--line));border-left:3px solid var(--ia);background:linear-gradient(180deg,color-mix(in srgb,var(--ia) 7%,transparent),color-mix(in srgb,var(--ink) 3%,transparent))}
.ip-s h4{display:flex;gap:9px;align-items:flex-start;margin:0 0 7px;font:600 .98rem/1.3 var(--f-display);color:var(--ink)}
.ip-s h4::before{content:"";flex:none;width:8px;height:8px;margin-top:6px;border-radius:2px;transform:rotate(45deg);background:var(--ia);box-shadow:0 0 10px color-mix(in srgb,var(--ia) 70%,transparent)}
.ip-s .vtxt,.ip-s p,.ip-s li{font-size:13.8px;line-height:1.68;color:color-mix(in srgb,var(--ink) 90%,transparent)}
.ip-s p{margin:0 0 9px}.ip-s ul{margin:2px 0 8px;padding-left:18px}.ip-s b{color:var(--ink);font-weight:600}
.ip-s table{width:100%;border-collapse:collapse;font-size:12.6px;margin:6px 0 8px}
.ip-s td{padding:6px 4px;border-top:1px solid color-mix(in srgb,var(--ia) 16%,var(--line));vertical-align:top}
.ip-s td:last-child{text-align:right;white-space:nowrap;font-family:var(--f-mono);font-weight:600;color:var(--ia)}
.vcard.ivc .ip-cover .ip-t{font-size:2.1rem;line-height:1.1;margin-top:16px}
.ip-lede{font-size:14.2px;line-height:1.68;color:color-mix(in srgb,var(--ink) 88%,transparent);margin:10px 0 18px;max-width:94%}
.ip-toc{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.ip-toc button{--ia:var(--gold);position:relative;display:flex;align-items:center;gap:11px;text-align:left;padding:11px 12px;border-radius:14px;cursor:pointer;color:var(--ink);font:600 13px/1.25 var(--f-body);border:1px solid color-mix(in srgb,var(--ia) 28%,var(--line));background:linear-gradient(135deg,color-mix(in srgb,var(--ia) 12%,transparent),color-mix(in srgb,var(--ink) 3%,transparent));transition:transform .18s,border-color .18s,background .18s}
.ip-toc button:hover,.ip-toc button:focus-visible{transform:translateY(-2px);border-color:var(--ia);outline:none}
.ip-toc b{flex:none;width:28px;height:28px;border-radius:9px;display:grid;place-items:center;font:700 12px/1 var(--f-mono);background:var(--ia);color:var(--on-accent)}
.ip-toc span small{display:block;margin-top:2px;font:500 11px/1.2 var(--f-body);color:var(--muted)}
.ip-foot{position:relative;z-index:2;display:flex;align-items:center;gap:12px;padding:12px 18px calc(14px + env(safe-area-inset-bottom,0px)) 22px;border-top:1px solid color-mix(in srgb,var(--ia) 24%,var(--line));background:color-mix(in srgb,var(--panel) 78%,transparent);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.ip-dots{display:flex;align-items:center;gap:6px;flex:1;min-width:0}
.ip-dots button{width:8px;height:8px;padding:0;border:0;border-radius:50%;background:color-mix(in srgb,var(--ink) 24%,transparent);cursor:pointer;transition:width .25s,background .25s}
.ip-dots button[aria-current="true"]{width:24px;border-radius:6px;background:var(--ia)}
.ip-cnt{font:600 11px/1 var(--f-mono);letter-spacing:.1em;color:var(--muted);margin-left:6px;white-space:nowrap}
.ip-btns{display:flex;gap:8px;flex:none}
.ip-btn{min-height:40px;padding:0 18px;border-radius:999px;cursor:pointer;font:600 13px/1 var(--f-body);border:1px solid color-mix(in srgb,var(--ink) 20%,transparent);background:transparent;color:var(--ink);transition:transform .15s,opacity .2s,background .2s}
.ip-btn:hover{background:color-mix(in srgb,var(--ink) 7%,transparent)}.ip-btn[disabled]{opacity:.3;cursor:default;pointer-events:none}
.ip-btn.ip-next{border:0;padding:0 22px;color:var(--on-accent);background:linear-gradient(135deg,var(--ia),color-mix(in srgb,var(--ia) 62%,var(--ink)));box-shadow:0 8px 22px -8px var(--ia)}
.ip-btn.ip-next:hover{transform:translateY(-1px);background:linear-gradient(135deg,var(--ia),color-mix(in srgb,var(--ia) 62%,var(--ink)))}
.ip-btn:focus-visible,.ip-dots button:focus-visible{outline:2px solid var(--ia);outline-offset:2px}
@media (max-width:820px){.vmodal.ipm{align-items:flex-end;padding:0}.vcard.ivc{width:100%;max-height:93dvh;border-radius:26px 26px 0 0}.vcard.ivc .ip-t{font-size:1.5rem}.vcard.ivc .ip-cover .ip-t{font-size:1.75rem}.ip-toc{grid-template-columns:1fr}.ip-wm{font-size:120px}.ip-body{padding:14px 18px 18px}.ip-cnt{display:none}.ip-btn{min-height:44px}}
@media (prefers-reduced-motion:reduce){.ip-page.inr,.ip-page.inl{animation:none}.ip-prog i::after,.vcard.ivc{transition:none}}
</style>`);
document.body.insertAdjacentHTML('beforeend', '<div class="vmodal" id="vModal" role="dialog" aria-modal="true" aria-labelledby="vmH"><div class="vcard" id="vCard"></div></div>');
const vModal=document.getElementById('vModal'), vCard=document.getElementById('vCard');
vModal.addEventListener('click', e=>{ if(e.target===vModal) vClose(); });
document.addEventListener('keydown', e=>{ if(e.key==='Escape' && vModal.classList.contains('on')) vClose(); });
function vOpen(h){ vModal.classList.remove('ipm'); vCard.classList.remove('ivc'); vCard.style.removeProperty('--ia'); vCard.innerHTML=h; vModal.classList.add('on'); vCard.scrollTop=0; const b=vCard.querySelector('button'); if(b) try{ b.focus({preventScroll:true}); }catch(e){} }
function vClose(){ vModal.classList.remove('on'); vModal.classList.remove('ipm'); }

/* ---------- the explainer as a paged, colour-keyed walkthrough (the text itself is unchanged) ---------- */
const VPAGES = [{k:"The inputs",t:"What the model counts, and what counts most",s:"Six things the state needed, and why money counts twice.",c:"var(--k-government)",m:/^1\.|^2\./i},{k:"The weights",t:"How a tie is weighed",s:"Connections, documents that need an issuer, and the power of states.",c:"var(--k-institution)",m:/^3\.|^4\.|power of states/i},{k:"The arithmetic",t:"Recalculating after every removal",s:"From capacity to a chance, and from lost years to delay.",c:"var(--k-company)",m:/^5\.|^6\.|^7\./i},{k:"The decisions",t:"Decisions, blocs and recognition",s:"Seven decisions read as decisions, and how governments moved with their blocs.",c:"var(--k-document)",m:/key decisions|blocs|recognition and the un/i},{k:"The framework",t:"The Mandate, lost years and the movement",s:"What changes when the Mandate or a funder falls, and who could have stepped in.",c:"var(--nest)",m:/mandate|stricter|lost years|pursue the goal/i},{k:"The readings",t:"Reading the result",s:"Five readings, the verdict thresholds, the heaviest nodes, and what the model cannot know.",c:"var(--ver)",m:/^8\.|heaviest|cannot know/i}];
let ipI = 0, ipList = [];
function vOpenIntro(h){
  const box = document.createElement('div'); box.innerHTML = h;
  const cover = [], secs = []; let cur = null;
  for(const el of [...box.children]){
    if(el.classList.contains('vbtns')) continue;
    if(el.tagName === 'H4'){ cur = {h: el.textContent, nodes: [el]}; secs.push(cur); }
    else if(cur) cur.nodes.push(el); else cover.push(el);
  }
  const defs = VPAGES.map(d => Object.assign({secs: []}, d));
  for(const s of secs){ const d = defs.find(d => d.m.test(s.h)) || defs[defs.length - 1]; d.secs.push(s); }
  const kicker = (cover.find(e => e.classList.contains('kind')) || {}).textContent || '';
  const title = (cover.find(e => e.tagName === 'H3') || {}).textContent || '';
  const lede = cover.filter(e => e.tagName === 'P').map(e => e.outerHTML).join('');
  ipList = defs.filter(d => d.secs.length);
  const total = ipList.length + 1;
  ipList.forEach((d, i) => { d.n = i + 1; });
  ipList.unshift({c: 'var(--gold)', t: title, cover: true, n: 0, kicker});
  ipList[0].lede = lede;
  vModal.classList.add('ipm');
  vCard.className = 'vcard ivc';
  vCard.innerHTML = `<div class="ip-wm" id="ipWm" aria-hidden="true"></div>
    <div class="ip-top"><div class="ip-prog" aria-hidden="true">${ipList.map(d => `<i style="--seg:${d.c}"></i>`).join('')}</div><button class="ip-x" type="button" data-v="close" aria-label="Close">&times;</button></div>
    <div class="ip-body" id="ipBody"><div class="ip-page" id="ipPage"></div></div>
    <div class="ip-foot"><div class="ip-dots" role="tablist" aria-label="Pages">${ipList.map((d, i) => `<button type="button" role="tab" data-ip-go="${i}" aria-label="Page ${i + 1}: ${esc(d.cover ? 'Overview' : d.t)}"></button>`).join('')}<span class="ip-cnt" id="ipCnt"></span></div>
      <div class="ip-btns"><button class="ip-btn" type="button" data-ip="back" id="ipBack">Back</button><button class="ip-btn ip-next" type="button" data-ip="next" id="ipNext">Next</button></div></div>`;
  ipShow(0, 1);
  vModal.classList.add('on');
}
function ipShow(i, dir){
  i = Math.max(0, Math.min(ipList.length - 1, i));
  const d = ipList[i], last = i === ipList.length - 1, pg = document.getElementById('ipPage');
  vCard.style.setProperty('--ia', d.c);
  let body;
  if(d.cover){
    body = `<div class="ip-cover"><div class="ip-k">${esc(d.kicker)}</div><h3 class="ip-t" id="vmH">${esc(d.t)}</h3><div class="ip-lede">${d.lede}</div>
      <div class="ip-toc">${ipList.slice(1).map((p, k) => `<button type="button" data-ip-go="${k + 1}" style="--ia:${p.c}"><b>${String(k + 1).padStart(2, '0')}</b><span>${esc(p.t)}<small>${p.secs.length} ${p.secs.length === 1 ? 'section' : 'sections'}</small></span></button>`).join('')}</div></div>`;
  } else {
    body = `<div class="ip-k">Step ${i} of ${ipList.length - 1} &middot; ${esc(d.k)}</div><h3 class="ip-t" id="vmH">${esc(d.t)}</h3>${d.s ? `<p class="ip-sub">${esc(d.s)}</p>` : ''}` +
      d.secs.map(s => `<section class="ip-s">${s.nodes.map(n => n.outerHTML).join('')}</section>`).join('');
  }
  pg.className = 'ip-page ' + (dir < 0 ? 'inl' : 'inr'); pg.innerHTML = body; void pg.offsetWidth;
  document.getElementById('ipBody').scrollTop = 0;
  document.getElementById('ipWm').textContent = i ? String(i).padStart(2, '0') : '';
  vCard.querySelectorAll('.ip-prog i').forEach((e, k) => { e.className = k < i ? 'done' : k === i ? 'on' : ''; });
  vCard.querySelectorAll('.ip-dots button').forEach((e, k) => e.setAttribute('aria-current', k === i ? 'true' : 'false'));
  document.getElementById('ipCnt').textContent = i === 0 ? 'OVERVIEW' : String(i).padStart(2, '0') + ' / ' + String(ipList.length - 1).padStart(2, '0');
  const b = document.getElementById('ipBack'), n = document.getElementById('ipNext');
  b.disabled = i === 0;
  n.textContent = last ? 'Start exploring' : i === 0 ? 'Begin' : 'Next';
  n.dataset.ip = last ? 'done' : 'next';
  ipI = i;
  try{ n.focus({preventScroll: true}); }catch(e){}
}
function ipOn(){ return vModal.classList.contains('on') && vCard.classList.contains('ivc'); }
vCard.addEventListener('click', e => { const b = e.target.closest('[data-ip],[data-ip-go]'); if(!b || !ipOn()) return;
  if(b.dataset.ipGo != null) ipShow(+b.dataset.ipGo, +b.dataset.ipGo < ipI ? -1 : 1);
  else if(b.dataset.ip === 'next') ipShow(ipI + 1, 1);
  else if(b.dataset.ip === 'back') ipShow(ipI - 1, -1);
  else if(b.dataset.ip === 'done') vClose(); });
document.addEventListener('keydown', e => { if(!ipOn() || e.metaKey || e.ctrlKey || e.altKey) return;
  if(e.key === 'ArrowRight' || e.key === 'PageDown'){ e.preventDefault(); ipShow(ipI + 1, 1); }
  else if(e.key === 'ArrowLeft' || e.key === 'PageUp'){ e.preventDefault(); ipShow(ipI - 1, -1); }
  else if(e.key === 'Home'){ e.preventDefault(); ipShow(0, -1); }
  else if(e.key === 'End'){ e.preventDefault(); ipShow(ipList.length - 1, 1); } });
(function(){ let x0 = null, y0 = 0; vCard.addEventListener('touchstart', e => { if(!ipOn()) return; x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, {passive: true});
  vCard.addEventListener('touchend', e => { if(x0 == null || !ipOn()) return; const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
    if(Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.6) ipShow(ipI + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1); }, {passive: true}); })();


/* ---------- the explainer: shown on the first visit, and from every reading ---------- */
function vIntro(){
  const heavy=[...N.values()].filter(n=>n.qop&&n.qop.viability).sort((a,b)=>b.qop.viability.drop-a.qop.viability.drop).slice(0,10);
  const amts=Object.entries(VB.amounts).sort((a,b)=>b[1][0]-a[1][0]);
  vOpenIntro(`<div class="kind">How the chances are computed</div><h3 id="vmH">A model of what the state needed, built only from this map</h3>
  <p class="vtxt">Take any node out and the map works out the chance that the state is still founded in 1948, how much money still reaches the movement, and how long the loss would delay it. It is a model built on the documented record, not a measured historical probability. Here is everything it does.</p>
  <h4>1. Six things the state needed</h4>
  <p class="vtxt">Every supportive tie dated before 1949 is sorted into one channel: <b>money</b>; <b>land and settlers</b>; <b>arms and force</b>; <b>diplomacy and law</b>; <b>organization</b>; <b>recognition</b> as a state. Opposition, violence, ties on the Arab or Nazi side, and money that did not go to the project (Rothschild loans to the British treasury, the Suez purchase) are left out.</p>
  <h4>2. Money counts most</h4>
  <p class="vtxt">Without money nothing else could be bought, built or defended, so the money channel counts twice in the overall chance. Each money tie is weighted by the sum the record states, in 1948 dollars (francs at 5.18 to the dollar, sterling at $4.86, older sums brought to 1948 prices; each 1948 figure also shown in today's dollars, ×13.9 on US consumer prices). Where the record states no sum the tie is assumed to carry ${vMoney(VB.default_m)}; that is an assumption, not a finding. Money passed along (the UJA to the UPA) or already inside a total (Edmond's colonies, inside his lifetime figure) is counted once.</p>
  <table>${amts.map(([k,a])=>`<tr><td>${esc(a[1])}</td><td>${vMoney(a[0])}</td></tr>`).join('')}<tr><td>Total money in the record, 1948 dollars</td><td>${vMoney(VB.cap0[0])}</td></tr></table>
  <h4>3. Connections count</h4>
  <p class="vtxt">For the other four channels, a tie counts 1 if verified and 0.6 if only reported, multiplied by how connected its two ends are: from 1× for someone with a single tie to 2× for the best-connected node. A tie between two well-connected people (Herzl, Weizmann, Edmond or Walter Rothschild, Balfour) opens more doors than one between two minor figures.</p>
  <h4>4. A document needs someone to give it force</h4>
  <p class="vtxt">A declaration, mandate or resolution counts only while at least one of the bodies that issued or signed it remains. The Balfour Declaration rested on the War Cabinet, Balfour and the British government, and was endorsed by Wilson and Congress; the Mandate rested on San Remo and the League. Remove all of a document's issuers and the document falls too, with everything that leaned on it.</p>
  <h4>5. Every removal is recalculated</h4>
  <p class="vtxt">After each removal the whole network is walked again from the core (the Declaration, the provisional government, the Jewish Agency, the Zionist Organization, the Haganah, Resolution 181). A tie counts only if neither end is gone and it still connects to the core, so a funder cut off from the core no longer counts even if it is still on the map.</p>
  <h4>6. From capacity to a chance</h4>
  <p class="vtxt">Each channel's chance is 1 &minus; e<sup>&minus;k&middot;C/C₀</sup>: C is what still connects, C₀ the full record, and k is set so the full record gives 99%. Spare capacity protects a channel; losses bite harder as it empties. All six were needed, so the overall chance is their product, with money squared: ${Math.round(V0.P)}% on the full record.</p>
  <h4>7. Delay</h4>
  <p class="vtxt">What is lost is rebuilt by the network that is left, so the pace scales with what remains. Each channel was first built over 51 years for money and organization (from 1897), 66 for land (from 1882), 28 for arms (from 1920) and 31 for diplomacy (from 1917); with half of a channel left it rebuilds at half that pace, with a quarter left at a quarter. The longest is the delay shown. The same scaled pace governs the "by 1958" and "ever" readings.</p>
  <h4>Key decisions, read as a whole</h4>
  <p class="vtxt">Seven decisions are read as decisions, not just as ties: the Balfour Declaration (decided by the War Cabinet), the League of Nations' approval of the Mandate (24 July 1922), Britain's referral of Palestine to the UN (decided by Bevin's cabinet, February 1947), Soviet support for partition (decided by Stalin, 1947), the American vote and pressure for partition in November 1947 and American recognition on 14 May 1948 (both decided by Truman), and the Czechoslovak arms sales (January to October 1948). For each, the map lists who pushed and who resisted, from ties on the map dated before the decision. Its chance of still happening is the push over push plus resistance, relative to the full record, where it happened. If the decider is removed, his documented successor decides (Henry Wallace in Truman's place, Attlee in Bevin's, an unnamed successor in Stalin's); if there is none, the decision is not taken. Push aimed at the man himself (his staff, friends and correspondents) does not pass to the successor unless the successor has his own documented tie to that person; the resistance stays; the successor's own documented position counts for or against, and a successor with no documented position adds one unit to each side (an even chance). The overall chance is then averaged over whether each decision still happens. Each push or resistance counts one; that is an assumption, disclosed here.</p>
  <h4>Blocs follow their leaders</h4>
  <p class="vtxt">In 1947-48 most governments moved with the bloc they depended on. Blocs are taken from the treaties of the time: the Americas (the Rio Pact, signed 2 September 1947), Western Europe (the Marshall Plan accord, April 1948) and the Soviet side (the Soviet republics and Moscow's allies). The partition vote itself measures how closely each followed its leader: ${VB.blocs.map(B=>`${esc(B.name)}, ${Math.round(B.follow*100)}%`).join('; ')}. If a leader is out (removed, or not voting for partition), each member that followed it keeps its vote for partition, and its 1948 recognition, only at the bloc's independence (100% minus that share). The vote then passes with a computed probability rather than for certain. The same rule applies to both sides; the Soviet side moved fewer votes, so losing its lead costs less.</p>
  <h4>The power of states</h4>
  <p class="vtxt">A tie with a great power counts for more than a tie with a small state. The five great powers named in the UN Charter are weighed by their economic output in 1950 (Angus Maddison's estimates), relative to France, the smallest of the five: the United States 6.6, the Soviet Union 2.3, Britain 1.6, China 1.1, France 1. Every other state weighs 1. The weight applies to diplomatic ties and to recognitions; in the UN vote every country still has one vote. In 1944 William Fox, who coined the word "superpower", named three: the United States, the Soviet Union and Britain.</p>
  <h4>The Mandate as a framework</h4>
  <p class="vtxt">The Mandate (in force 1923) wrote the Balfour Declaration into its preamble and made Britain responsible for "the establishment of the Jewish national home". Under it the Jewish population grew about 21,900 a year (83,794 in 1922 to 630,000 in 1947); under Ottoman rule it grew about 2,200 a year (24,000 in 1882 to 94,000 in 1914). So if the Mandate falls (with the Balfour Declaration, or with Britain, its Mandatory power), immigration and settlement from 1920 to 1948 go at the Ottoman pace, and about 90% of that period's land-and-settlers work counts as lost years. Part of the faster growth came from persecution in Europe in the 1930s, which would have driven emigration anyway; this credits all of it to the Mandate.</p>
  <h4>A stricter reading you can switch on</h4>
  <p class="vtxt">By default a document stands while any body that issued it remains. The Balfour Declaration was issued by the War Cabinet and signed by Balfour; it was addressed to Walter Rothschild, who also helped draft it. Some argue it could not have been issued without him. The record documents his role but not that Britain would have withheld it otherwise, so this is offered as a switch in the Remove a node panel, off by default: with it on, a document falls when its named addressee is removed.</p>
  <h4>Lost years, and who could have taken over</h4>
  <p class="vtxt">Removing a funder or a leader also removes years of work. Each tie's work is placed in the years it was done: its own dates where the record gives them (Edmond de Rothschild's money from 1882 to 1934, the American appeals' from 1946 to 1948), otherwise spread over the years its actor was active. Actors run from their first to their last dated tie, except where the founding and end are documented (the Jewish Agency from 1929, not earlier; the Palestine Office from 1908; Herzl from 1895 to 1904). For each year from 1882 to 1948 the map asks, channel by channel, what work the removed actors did that year, and whether the strongest documented actor on the same side, already founded, could have done it: a substitute covers only up to the yearly work it had actually shown by then, not money it raised decades later.</p>
  <p class="vtxt">Work built stays built, so a loss carries forward. What no one covered is a shortfall against everything built so far, and it keeps counting each year until later work outgrows it: losing the first colonies matters for decades, losing one year's donation in 1947 matters for a year. A channel starts counting once its record reaches 5% of its 1948 total, because before that the record is too thin to say a year was lost. A year counts as lost in proportion to the worst-hit channel's shortfall.</p>
  <p class="vtxt">The lost years then lower the on-time chance in proportion to the 66 build-up years (losing 22 years leaves two-thirds), and a later founding cannot come before those years are made up. Each reading names the removed actors, the years they were active, the closest documented substitute, from when, and how much of the role it could carry. The map cannot know whether someone undocumented would have stepped in, or whether a substitute would have chosen to.</p>
  <h4>Someone has to pursue the goal</h4>
  <p class="vtxt">The state was the goal of an organized movement. If its three carrying bodies are all removed (the Zionist Organization, the Jewish Agency and the Jewish National Council of the Yishuv), there is no one left to pursue it, and every channel counts as empty however much support remains elsewhere.</p>
  <h4>Recognition and the UN vote</h4>
  <p class="vtxt">The UN was founded on 24 October 1945. On 29 November 1947 its General Assembly adopted partition, Resolution 181, by 33 votes to 13 with 10 abstentions; two-thirds of the votes cast were needed, so it needed at least twice as many votes for as against. The map holds that vote: remove countries that voted for it and they count as abstaining (or, if you choose the harsher reading, as voting against); remove countries that voted against and they do not vote. If the count falls below two-thirds, or the UN itself is removed, Resolution 181 loses its force.</p>
  <p class="vtxt">The recognition channel weighs Resolution 181 in force as 10 (the UN's legal basis, which the Declaration of Independence cited), each great power's recognition in 1948 (the United States and the Soviet Union) as 3, and each other state's 1948 recognition as 1. A state could still be recognized without the UN vote, as the United States recognized Israel a year before its UN admission in May 1949, so losing the vote weakens recognition but does not end it. Lost recognition is rebuilt over three years, the time from the UN's founding to the vote.</p>
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
  <h4>The six channels</h4>${vBars(R)}
  <h4>What happened in the graph</h4>
  <ul><li>${vVoteLine(removed)}</li><li>${cut} documented tie${cut===1?'':'s'} cut.</li>
  ${R.lostDocs.filter(x=>x!=='res181').length?`<li>Lost their force: ${R.lostDocs.filter(x=>x!=='res181').map(x=>esc(vName(x))).join(', ')} (every body that issued them is gone).</li>`:''}${R.lostDocs.includes('res181')&&!removed.has('res181')?`<li>Resolution 181 never passes, so the Declaration loses its UN legal basis; recognition rests on individual states alone.</li>`:''}
  <li>Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])}${lostM>0.05?` (${vMoney(lostM)} gone or cut off)`:''}, from ${R.funders} of ${R.funders0} funders.</li>
  <li>${removed.size} node${removed.size===1?'':'s'} removed in total, read together; they stay removed until you reset the graph${removed.size?`: ${[...removed].slice(0,40).map(x=>esc(vName(x))).join(', ')}${removed.size>40?` and ${removed.size-40} more`:''}`:''}.</li></ul>
  ${R.decisions&&R.decisions.length?'<h4>Key decisions</h4>'+vDecText(R):''}${vYearsText(R)}${vDelayText(R)}${vNeed(R)}
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
   <div class="t2">${esc(label)} · ${what}${vVote(vLost(removed)).passes?'':' · <b>the UN vote fails</b>'}<br><b>${Math.round(rd.on)}%</b> on time${d?` (${d>0?'+':''}${d})`:''} · <b>${Math.round(rd.ever)}%</b> ever · movement <b>${Math.round(rd.survive)}%</b> · tap for details</div></div>
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
function vPill(){ const p=$('vPill'); if(!p) return; const n=removed.size; if(!n&&!vDrop.size&&!vNoVote.size){ p.classList.remove('on'); return; }
  const R=vScore(removed); $('vPillT').innerHTML=`${n} removed · <b style="color:${vColor(R.P)}">${Math.round(R.P)}%</b> on time`; p.classList.add('on'); }
$('vPillV').onclick=()=>{ const R=vScore(removed); vOpen(`<div class="kind">The network as it stands</div><h3 id="vmH">${[...removed].map(vName).map(esc).join(', ')||'Scenario'}</h3>
  ${vHead(R)}<h4>The six channels</h4>${vBars(R)}
  <p class="vtxt">${vVoteLine(removed)}</p><p class="vtxt">Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])}, from ${R.funders} of ${R.funders0} funders.</p>${vYearsText(R)}${vDelayText(R)}${vNeed(R)}
  <div class="vbtns"><button class="vbtn pri" type="button" data-v="close">Keep exploring</button><button class="vbtn" type="button" data-v="reset">Reset the graph</button><button class="vbtn" type="button" data-v="how">How this is computed</button></div>`); };
$('vPillR').onclick=()=>$('reset').click();

/* ---------- the reading at the top of the Remove a node panel ---------- */
function viabBlock(){
  const R=vScore(removed), any=removed.size||vDrop.size||vNoVote.size||vFlip.size;
  const opts=Object.keys(VB.groups).map(g=>`<option value="${esc(g)}">${esc(g)} (${VB.groups[g].length})</option>`).join('');
  let h=`<div class="viab"><div class="vlabel">The state&rsquo;s chances, on this record</div>
  ${vHead(R)}${any?`<p class="vtxt">On time: down ${Math.round(V0.P-R.P)} from ${Math.round(V0.P)}%.</p>`:''}${vBars(R)}
  <p class="vtxt">Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])} (1948 dollars), from ${R.funders} of ${R.funders0} funders.</p><p class="vtxt">${vVoteLine(removed)}</p>
  <label class="vtxt" style="display:flex;gap:8px;align-items:flex-start"><input type="checkbox" id="vstrict"${vStrict?' checked':''} style="margin-top:3px"><span>Stricter reading: a document could not have been issued without its named addressee (for example, no Balfour Declaration without Walter Rothschild). An assumption, not a finding; off by default.</span></label>
  <label class="vtxt" style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">Removed yes-votes count as <select id="vmode" class="sel" style="padding:5px 26px 5px 8px"><option value="abstain"${vMode==='abstain'?' selected':''}>abstentions</option><option value="against"${vMode==='against'?' selected':''}>votes against</option></select></label>`;
  if(any) h+=vDecText(R)+vYearsText(R)+vDelayText(R)+vNeed(R); else h+=`<p class="vtxt">Tap any node to remove it, or remove a whole group below.</p>`;
  h+=`<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px"><select id="vgrp" class="sel" style="flex:1 1 180px;padding:7px 30px 7px 10px">${opts}</select><button id="vgo" class="ghost" type="button">Remove group</button>${any?'<button id="vclr" class="ghost" type="button">Restore all</button>':''}</div>
  <div class="vbtns" style="margin-top:8px"><button class="vbtn" type="button" id="vhow">How this is computed</button></div></div>`;
  return h;
}
function delPanel(r){ delPanel0(r); $('side').insertAdjacentHTML('afterbegin', viabBlock());
  const go=$('vgo'); if(go) go.onclick=()=>{ const g=$('vgrp').value; vRemove(VB.groups[g], g==='Without the United States'?'the United States':g, VB.drop[g]); };
  const cl=$('vclr'); if(cl) cl.onclick=()=>$('reset').click();
  const hw=$('vhow'); if(hw) hw.onclick=vIntro;
  const vs=$('vstrict'); if(vs) vs.onchange=()=>{ const before=vScore(removed).P; vStrict=vs.checked; vLS('road_strict_v1', vStrict?1:null); vTestCache=null; vRefresh(); vSignal('Stricter reading '+(vStrict?'on':'off'), before); };
  const vm=$('vmode'); if(vm) vm.onchange=()=>{ const before=vScore(removed).P; vMode=vm.value; vLS('road_vote_mode', vMode); vRefresh(); vSignal('Removed yes-votes now count as '+(vMode==='against'?'votes against':'abstentions'), before); };
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
(function(){ const s=vLS(VKEY); if(s){ (s.removed||[]).forEach(x=>{ if(N.get(x)) removed.add(x); }); (s.drop||[]).forEach(x=>vDrop.add(x)); (s.novote||[]).forEach(x=>vNoVote.add(x)); (s.flip||[]).forEach(x=>vFlip.add(x)); }
  setTimeout(()=>{ vPill(); if(removed.size) draw(); if(!vLS(VINTRO)) vIntro(); }, 600); })();
