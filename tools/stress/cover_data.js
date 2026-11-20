const {chromium}=require('playwright');const fs=require('fs');
const SP='/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/';
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.route('**/d3.min.js',r=>r.fulfill({body:fs.readFileSync(SP+'graph/node_modules/d3/dist/d3.min.js'),contentType:'application/javascript'}));
await p.addInitScript(()=>{try{localStorage.setItem('road_model_intro_v1','1')}catch(e){}});
await p.goto('file:///home/claude/israel/road-network.html');await p.waitForTimeout(4000);
const ids=['soviet','roth','us','britain','balfour','czech','un','herzl','truman','movement','legit_holocaust','people_mandate','soviet'];
const out=await p.evaluate((ids)=>{const res={};const base=vScore(new Set());res.base={pc:base.pc,on:vRead(base).on};
 for(const x of vTestResults()){ if(!ids.includes(x.t.id)) continue; const R=x.R; const pc=R.pc|| (R.mix?R.mix[0][1].pc:null);
   res[x.t.id]={q:x.t.q,pc,on:x.rd.on,ever:x.rd.ever,lost:x.rd.lost,verdict:x.rd.verdict,by1958:x.rd.by1958,by1978:x.rd.by1978,survive:x.rd.survive,retry:x.rd.retry,weak:R.weakest||null}; }
 return res;},ids);
fs.writeFileSync('/home/claude/israel/tools/stress/cover_data.json',JSON.stringify(out,null,1));console.log(JSON.stringify(out).slice(0,3000));await b.close();})();
