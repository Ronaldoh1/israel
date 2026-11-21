const {chromium}=require('playwright');const fs=require('fs');
const SP='/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/';
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route('**/d3.min.js',r=>r.fulfill({body:fs.readFileSync(SP+'graph/node_modules/d3/dist/d3.min.js'),contentType:'application/javascript'}));
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{try{localStorage.setItem('road_model_intro_v1','1')}catch(e){}});
await p.goto('file:///home/claude/israel/road-network.html');await p.waitForTimeout(4000);
const out=await p.evaluate(()=>{
 const HEAD=['britain','us','roth','balfour','d_arms','ottoman_neutral','un','truman','herzl','people_mandate','policy_doors','legit_holocaust','d_all','force_british_training','yishuv_inst','latam_bloc'];
 const snap=()=>{vTestCache=null; vDispCache=null; const r={base:vRead(vScore(new Set())).on}; for(const x of vTestResults()) r[x.t.id]=x.rd.on; for(const x of vDispResults()) r[x.t.id]=x.rd.on; return r;};
 const clone=o=>JSON.parse(JSON.stringify(o));
 const E0=clone(VB.edges), C0=clone(VB.cap0), X0=clone(VB.exp), cal0=VB.cal;
 const restore=()=>{VB.edges.length=0; E0.forEach(e=>VB.edges.push(clone(e))); VB.cap0.splice(0,VB.cap0.length,...C0); VB.exp.splice(0,VB.exp.length,...X0); VB.cal=cal0;};
 const base=snap(); const res={base:Object.fromEntries(HEAD.concat(['base']).map(k=>[k,base[k]]))}; const all={};
 const run=(name,fn)=>{restore(); fn(); const s=snap(); all[name]=s; restore(); };
 // 1. channel importance x0.5 and x2
 VB.channels.forEach((c,i)=>{ run('exp_'+c+'_x0.5',()=>{VB.exp[i]=X0[i]*0.5}); run('exp_'+c+'_x2',()=>{VB.exp[i]=X0[i]*2}); });
 // 2. calibration
 run('cal_0.95',()=>{VB.cal=0.95}); run('cal_0.999',()=>{VB.cal=0.999});
 // 3. reported ties at 0.3 and at 1.0 of a verified tie (cap0 adjusted)
 for(const f of [0.3,1.0]) run('reported_'+f,()=>{ VB.edges.forEach(e=>{ if(e[3]===0.6){ const nv=e[4]/0.6*f; VB.cap0[e[2]]+=nv-e[4]; e[4]=nv; } }); });
 // 4. trained manpower weighted x10
 run('training_x10',()=>{ VB.edges.forEach(e=>{ if(['sns','notrim','jewish_brigade'].includes(e[0])&&e[1]==='haganah'){ VB.cap0[e[2]]+=e[4]*9; e[4]*=10; } }); });
 // 5. linear (non-saturating) curve for the people channel
 const src0=vScoreBase.toString(); const pi=VB.channels.indexOf('people');
 restore(); window.vScoreBase=eval('('+src0.replace("VB.cap0[i]?1-Math.exp(-k*x/VB.cap0[i]):1","VB.cap0[i]?(i==="+pi+"?VB.cal*x/VB.cap0[i]:1-Math.exp(-k*x/VB.cap0[i])):1")+')');
 all['people_linear']=snap(); window.vScoreBase=eval('('+src0+')');
 // 6. leave one source out: group weighted ties by the first ref URL of their display tie
 const ref={}; DATA.edges.forEach(e=>{ if(e.refs&&e.refs.length){ const k=e.f+'>'+e.t; (ref[k]=ref[k]||new Set()); e.refs.forEach(r=>ref[k].add(r.u)); } });
 const bySrc={}; E0.forEach((e,j)=>{ const s=ref[e[0]+'>'+e[1]]; if(s&&s.size===1){ const u=[...s][0]; (bySrc[u]=bySrc[u]||[]).push(j);} });
 const loso={}; const srcs=Object.entries(bySrc).sort((a,b)=>b[1].length-a[1].length);
 for(const [u,js] of srcs){ restore(); js.forEach(j=>{ const e=VB.edges[j]; VB.cap0[e[2]]-=e[4]; e[4]=0; }); const s=snap(); let mx=0,arg=''; for(const k of HEAD){ const d=Math.abs((s[k]??0)-(base[k]??0)); if(d>mx){mx=d;arg=k;} } loso[u]={n:js.length,maxShift:mx,test:arg,base:s.base}; }
 restore();
 return {base:res.base,all,loso,nsrc:srcs.length,assumptions:vTestResults().filter(x=>/Assumption/i.test(x.t.featTag||'')).map(x=>x.t.id)};
});
console.log(JSON.stringify(errs).slice(0,300)); fs.writeFileSync(SP+'stress.json',JSON.stringify(out,null,1)); await b.close();})();
