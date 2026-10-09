const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 let fails=0;
 const p=await b.newPage({viewport:{width:412,height:860}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 // 1. deep link to the card
 await p.goto('file:///mnt/user-data/outputs/sophia.html#elections2026-card',{timeout:120000}); await p.waitForTimeout(3000);
 const st=await p.evaluate(()=>{const c=document.querySelector('.inst-card[data-inst-id="elections2026"]'); return c?c.className:null});
 console.log('card class after deep link:',st); if(!st||!/el-live/.test(st)) fails++;
 await p.screenshot({path:'/tmp/claude-0/shots/sophia_card.png'});
 // 2. from inside the Israel simulation
 await p.evaluate(()=>window.openSimOverlay('israel')); await p.waitForTimeout(6000);
 const fr=p.frames().find(f=>f!==p.mainFrame()&&f.url()!=='about:blank');
 await fr.evaluate(()=>{ try{dismissWelcome()}catch(e){}; renderScene(S.findIndex(x=>x.id==='el26_s01')); });
 await p.waitForTimeout(1200);
 await fr.evaluate(()=>showEntity(S[cur].ents.find(e=>e.id==='el26_portal'))); await p.waitForTimeout(300);
 await fr.click('#mBody .el26-btn'); await p.waitForTimeout(1500);
 const r=await p.evaluate(()=>({open:document.getElementById('simOverlay').classList.contains('open'), hash:location.hash, pulse:!!document.querySelector('.inst-card.el-pulse')}));
 console.log('after portal click:',r); if(r.open||!r.pulse) fails++;
 await p.screenshot({path:'/tmp/claude-0/shots/sophia_pulse.png'});
 // 3. module still opens from card
 await p.click('.inst-card[data-inst-id="elections2026"]'); await p.waitForTimeout(2500);
 const fr2=p.frames().find(f=>f!==p.mainFrame()&&f.url()!=='about:blank');
 console.log('module h1:', await fr2.textContent('h1'));
 await fr2.click('.methodcard'); console.log('method h1:', await fr2.textContent('h1'));
 if(errs.length){console.log(errs.slice(0,5)); fails+=errs.length;}
 await b.close(); console.log('fails:',fails);
})();
