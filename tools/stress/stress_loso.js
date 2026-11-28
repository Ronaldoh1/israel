// Leave one source out (27 Nov 2026, cause-and-effect model): for the 50 sources that carry the most weighted ties alone,
// drop those ties (as if the source did not exist), rerun the headline tests, record the largest shift.
// Writes tools/stress/loso_<date>.json. Usage: node tools/stress/stress_loso.js (needs the local d3 copy in the scratch dir).
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const SP='/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/'; const OUT=path.join(__dirname,'loso_'+new Date().toISOString().slice(0,10)+'.json');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route('**/d3*.min.js',r=>r.fulfill({body:fs.readFileSync(SP+'graph/node_modules/d3/dist/d3.min.js'),contentType:'application/javascript'}));
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{try{localStorage.setItem('road_model_intro_v1','1')}catch(e){}});
await p.goto('file://'+path.join(__dirname,'..','..','road-network.html'));await p.waitForTimeout(4000);
const out=await p.evaluate(()=>{
 const HEAD=['britain','us','roth','balfour','herzl','edmond_all','un','truman','people_mandate','d_all','movement','armed'];
 const snap=()=>{vTestCache=null; vDispCache=null; const r={base:vRead(vScore(new Set())).on}; for(const x of vTestResults()) r[x.t.id]=x.rd.on; for(const x of vDispResults()) r[x.t.id]=x.rd.on; return r;};
 const clone=o=>JSON.parse(JSON.stringify(o)); const E0=clone(VB.edges), C0=clone(VB.cap0);
 const restore=()=>{VB.edges.length=0; E0.forEach(e=>VB.edges.push(clone(e))); VB.cap0.splice(0,VB.cap0.length,...C0);};
 const base=snap();
 const ref={}; DATA.edges.forEach(e=>{ if(e.refs&&e.refs.length){ const k=e.f+'>'+e.t; (ref[k]=ref[k]||new Set()); e.refs.forEach(r=>{ if(r.u) ref[k].add(r.u); }); } });
 const W=E0[0].length-1; // weight is the last numeric field
 const bySrc={}; E0.forEach((e,j)=>{ const s=ref[e[0]+'>'+e[1]]; if(s&&s.size===1){ const u=[...s][0]; (bySrc[u]=bySrc[u]||[]).push(j);} });
 const srcs=Object.entries(bySrc).sort((a,b)=>b[1].length-a[1].length).slice(0,50);
 const loso={};
 for(const [u,js] of srcs){ restore(); js.forEach(j=>{ const e=VB.edges[j]; const wi=e.findIndex((v,i)=>i>2&&typeof v==='number'&&i===4); const w=e[4]; if(typeof w==='number'){ VB.cap0[e[2]]-=w; e[4]=0; } }); const s=snap(); let mx=0,arg=''; for(const k of HEAD){ const d=(s[k]??0)-(base[k]??0); if(Math.abs(d)>Math.abs(mx)){mx=d;arg=k;} } loso[u]={n:js.length,shift:Math.round(mx*10)/10,test:arg,all:Object.fromEntries(HEAD.map(k=>[k,Math.round(((s[k]??0)-(base[k]??0))*10)/10]))}; }
 restore();
 return {base:Object.fromEntries(HEAD.concat(['base']).map(k=>[k,base[k]])),edge0:E0[0],loso,nsrc:Object.keys(bySrc).length};
});
fs.writeFileSync(OUT,JSON.stringify(out,null,1)); console.log(JSON.stringify(errs).slice(0,300), OUT, JSON.stringify(out.edge0));
const L=Object.entries(out.loso).sort((a,b)=>Math.abs(b[1].shift)-Math.abs(a[1].shift)); console.log(L.slice(0,8).map(x=>x[1].shift+' '+x[1].test+' n'+x[1].n+' '+x[0].slice(0,80)).join('\n'));
await b.close();})();
