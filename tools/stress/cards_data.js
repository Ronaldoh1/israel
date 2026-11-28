const {chromium}=require('playwright');const fs=require('fs');
const SP='/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/';
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route('**/d3.min.js',r=>r.fulfill({body:fs.readFileSync(SP+'graph/node_modules/d3/dist/d3.min.js'),contentType:'application/javascript'}));
await p.addInitScript(()=>{try{localStorage.setItem('road_model_intro_v1','1')}catch(e){}});
await p.goto('file:///home/claude/israel/road-network.html');await p.waitForTimeout(4000);
const r=await p.evaluate(()=>{ vTestCache=null; vDispCache=null;
 const one=(t,k)=>vRunScenario(t,()=>{const R=vScore(removed),rd=vRead(R);const pc=R.pc||(R.mix?R.mix[0][1].pc:[]);return {k,id:t.id,q:t.q,said:t.said,what:t.what,rd,dec:(R.decisions||[]).map(D=>[D.name,Math.round(100*(D.chance||0))]),pc:pc.map(x=>Math.round(x*100)),n:removed.size};});
 const base=vScore(new Set()); 
 const st={}; DATA.edges.forEach(e=>st[e.status]=(st[e.status]||0)+1); return {alts:VB.alt.alts.map(a=>[a.id,a.name,a.chance,a.verdict]),status:st,labels:VB.labels,tbuild:VB.tbuild,verdicts:VB.verdict,hazard:VB.hazard,exp:VB.exp,nodes:DATA.nodes.length, edges:DATA.edges.length, wedges:VB.edges.length, channels:VB.channels, base:vRead(base),
  T:[...VTESTS.map(t=>one(t,'T')),...VDISP.map(t=>one(t,'D')),...VB.breakers.items.map((x,i)=>Object.assign(one(vBreakTest(i),'B'),{label:x.label,kind:x.kind}))]};});
fs.writeFileSync(SP+'cards2.json',JSON.stringify(r));console.log(r.T.length, JSON.stringify(r.base).slice(0,300));await b.close();})();
