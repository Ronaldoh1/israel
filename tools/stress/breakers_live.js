const {chromium}=require('playwright');const fs=require('fs');
const SP='/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/';
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route('**/d3*.min.js',r=>r.fulfill({body:fs.readFileSync('/home/claude/israel/tools/vendor/d3-7.8.5.min.js'),contentType:'application/javascript'}));
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{try{localStorage.setItem('road_model_intro_v1','1')}catch(e){}});
await p.goto('file:///home/claude/israel/road-network.html');await p.waitForTimeout(4000);
const out=await p.evaluate(()=>{
 const CUT=35, OUTCOME=new Set(['decl_indep','provisional','israel_gov','recognition48']), POOL=60, POOL3=26;
 const G=VB.groups, DR=VB.drop||{};
 const ev=(ids,drop)=>vRunScenario({ids:()=>ids,drop:()=>drop||[]},()=>{const R=vScore(removed), rd=vRead(R); const pc=R.pc||(R.mix?R.mix[0][1].pc:[]); 
   let wi=0; pc.forEach((x,i)=>{ if(x<pc[wi]) wi=i; });
   return {V:Math.round(rd.on*10)/10, verdict:rd.verdict, ever:Math.round(rd.ever*10)/10, lost:Math.round((rd.lost||0)*10)/10, weakest:VB.channels[wi],
     dec:(R.decisions||[]).filter(D=>D.chance<0.5).map(D=>[D.name,Math.round(100*D.chance)])};});
 const nm=i=>N.get(i)?N.get(i).name:i;
 const single={}; for(const n of DATA.nodes){ if(OUTCOME.has(n.id)) continue; single[n.id]=ev([n.id]).V; }
 const items=[];
 for(const [i,v] of Object.entries(single).sort((a,b)=>a[1]-b[1])) if(v<CUT+0.0001||(v<CUT+5&&N.get(i).kind==='person')) items.push(Object.assign({kind:'single',label:'Without '+nm(i),ids:[i]},ev([i])));
 const GL={'Rothschild family and houses':'the Rothschild family','Without the United States':'the United States (government, organizations and money)','British government':'the British government','US government':'the US government','American Zionist organizations':'the American Zionist organizations','Soviet bloc':'the Soviet bloc','Finance and banks':'the banks and land and finance companies','The Zionist movement (organizations and leaders)':'the organized Zionist movement','Armed groups and arms network':'the armed groups and the arms network','Countries that voted for partition':'the states that voted for partition','The United Nations':'the United Nations','France':'France','Christian Zionism':'Christian Zionism','Religious institutions':'the religious institutions','The Vatican':'the Vatican'};
 const gl=g=>GL[g]||g;
 const gv={}; const gnames=Object.keys(G);
 for(const g of gnames){ const r=ev(G[g],DR[g]); gv[g]=r.V; if(r.V<CUT) items.push(Object.assign({kind:'group',label:'Without '+gl(g),groups:[g]},r)); }
 let gp=0;
 for(let a=0;a<gnames.length;a++) for(let c=a+1;c<gnames.length;c++){ gp++; const A=gnames[a],B=gnames[c]; if(gv[A]<CUT||gv[B]<CUT) continue;
   const r=ev([...new Set([...G[A],...G[B]])],[...(DR[A]||[]),...(DR[B]||[])]); if(r.V<CUT) items.push(Object.assign({kind:'groups',label:'Without '+gl(A)+' and '+gl(B),groups:[A,B],alone:[gv[A],gv[B]]},r)); }
 const base=ev([]).V;
 let pool=Object.entries(single).sort((a,b)=>a[1]-b[1]).filter(([i,v])=>(v<base-0.05&&N.get(i).kind!=='document')||['balfour_decl','mandate','res181'].includes(i)).map(x=>x[0]).slice(0,POOL);
 pool=pool.filter(i=>single[i]>=CUT+5);
 const broken=new Set(); const pairs=[];
 for(let a=0;a<pool.length;a++) for(let c=a+1;c<pool.length;c++){ const r=ev([pool[a],pool[c]]); if(r.V<CUT){ pairs.push(Object.assign({kind:'pair',label:'Without both '+nm(pool[a])+' and '+nm(pool[c]),ids:[pool[a],pool[c]],alone:[single[pool[a]],single[pool[c]]]},r)); broken.add(pool[a]+'|'+pool[c]); } }
 const P3=pool.slice(0,POOL3), tri=[]; let nt=0;
 const bk=(x,y)=>broken.has(x+'|'+y)||broken.has(y+'|'+x);
 for(let a=0;a<P3.length;a++) for(let c=a+1;c<P3.length;c++) for(let e=c+1;e<P3.length;e++){ nt++; const [x,y,z]=[P3[a],P3[c],P3[e]]; if(bk(x,y)||bk(x,z)||bk(y,z)) continue; const r=ev([x,y,z]); if(r.V<CUT) tri.push(Object.assign({ids:[x,y,z]},r)); }
 tri.sort((a,b)=>a.V-b.V); pairs.sort((a,b)=>a.V-b.V);
 const merged=[]; for(const x of tri){ let hit=null; for(const m of merged){ const common=m.ids.filter(i=>x.ids.includes(i)); if(common.length===2&&Math.abs(m.V-x.V)<=0.5&&(!m.fixed||m.fixed.every(i=>common.includes(i)))){hit=m;break;} }
   if(hit){ const common=hit.ids.filter(i=>x.ids.includes(i)); if(!hit.fixed){ hit.fixed=hit.ids.filter(i=>common.includes(i)); hit.alts=hit.ids.filter(i=>!common.includes(i)); } hit.alts.push(...x.ids.filter(i=>!common.includes(i))); hit.V=Math.max(hit.V,x.V); } else merged.push(Object.assign({},x)); }
 for(const x of merged){ if(x.alts) items.push(Object.assign({},x,{kind:'triple',label:'Without '+x.fixed.map(nm).join(' and ')+', plus any one of: '+x.alts.map(nm).join(', ')}));
   else items.push(Object.assign({},x,{kind:'triple',label:'Without '+x.ids.slice(0,-1).map(nm).join(', ')+' and '+nm(x.ids[2]),alone:x.ids.map(i=>single[i])})); }
 items.splice(items.length,0); const all=items.filter(x=>x.kind!=='pair').concat([]); // keep order: singles, groups, group pairs, then pairs, then triples
 const ordered=[...items.filter(x=>x.kind==='single'),...items.filter(x=>x.kind==='group').sort((a,b)=>a.V-b.V),...items.filter(x=>x.kind==='groups').sort((a,b)=>a.V-b.V),...pairs,...items.filter(x=>x.kind==='triple')];
 return {built:'2026-11-19',cut:CUT,baseline:base,searched:{singles:Object.keys(single).length,groups:gnames.length,group_pairs:gp,pairs:pool.length*(pool.length-1)/2,triples:nt},pool:pool.length,pool3:P3.length,items:ordered};
});
console.log(JSON.stringify(errs).slice(0,300)); fs.writeFileSync(SP+'breakers_live.json',JSON.stringify(out,null,1)); console.log(out.items.length, JSON.stringify(out.searched)); await b.close();})();
