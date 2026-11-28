// Recomputes every node's "if removed" reading on the Road to 1948 map with the page's own model (27 Nov 2026), so the
// readings on each node's card match the tests. Run after any change to the model. Usage: node tools/node_readings.js [road-network.html]
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const P=path.resolve(process.argv[2]||path.join(__dirname,'..','road-network.html'));
(async()=>{ const b=await chromium.launch(); const p=await b.newPage();
  await p.goto('file://'+P); await p.waitForTimeout(3000);
  const R=await p.evaluate(()=>{ const out={}; const base=vRead(vScore(new Set())).on;
    for(const n of N.values()){ if(!(n.qop&&n.qop.viability)) continue;
      const r=vRunScenario({id:'n',ids:()=>[n.id]},()=>{ const y=vScore(removed); const rd=vRead(y); return [y,rd]; }); const [y,rd]=r;
      const mi=y.pc.indexOf(Math.min(...y.pc)), rnd=(x,k=1)=>x==null?null:Math.round(x*Math.pow(10,k))/Math.pow(10,k);
      out[n.id]={V:rnd(rd.on), rating:vRating(rd.on), weakest:VB.channels[mi], channels:y.pc.map(x=>rnd(x,3)), delay:rnd(rd.delay), drop:rnd(base-rd.on),
        read:{on:rnd(rd.on), delay:rnd(rd.delay), survive:rnd(rd.survive), lost:rnd(rd.lost), by1958:rnd(rd.by1958), by1978:rnd(rd.by1978), ever:rnd(rd.ever), retry:rd.retry, verdict:rd.verdict},
        weight:y.share.map(x=>rnd(Math.max(0,1-x),3))}; }
    return out; });
  await b.close();
  let s=fs.readFileSync(P,'utf8'); const k=s.indexOf('const DATA = ')+13; let depth=0,i=k,inStr=false,esc=false;
  for(;i<s.length;i++){ const c=s[i]; if(inStr){ if(esc) esc=false; else if(c==='\\') esc=true; else if(c==='"') inStr=false; continue; } if(c==='"') inStr=true; else if(c==='{') depth++; else if(c==='}'){ depth--; if(!depth){ i++; break; } } }
  const D=JSON.parse(s.slice(k,i)); let n=0; for(const x of D.nodes){ if(R[x.id]){ x.qop.viability=R[x.id]; n++; } }
  fs.writeFileSync(P, s.slice(0,k)+JSON.stringify(D)+s.slice(i)); console.log('node readings recomputed:',n);
})();
