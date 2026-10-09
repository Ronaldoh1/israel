const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 let fails=0;
 for(const w of [412,375,1280]){
 const p=await b.newPage({viewport:{width:w,height:860}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///mnt/user-data/outputs/sophia.html',{timeout:120000}); await p.waitForTimeout(2500);
 await p.evaluate(()=>{const d=document.getElementById('dlDismiss'); if(d) d.click();});
 const bx=await p.evaluate(()=>{const a=document.getElementById('showcaseSpotlight').getBoundingClientRect(),e=document.getElementById('elSpotlight').getBoundingClientRect();return {a:[a.width,a.height,a.bottom],e:[e.width,e.height,e.top],sw:document.documentElement.scrollWidth}});
 console.log(w,'spot',bx); if(Math.abs(bx.a[0]-bx.e[0])>1||Math.abs(bx.a[1]-bx.e[1])>1||bx.e[2]<bx.a[2]||bx.sw>w) {fails++;console.log('size/order/overflow FAIL')}
 await p.evaluate(()=>document.getElementById('elSpotlight').scrollIntoView({block:'center'})); await p.waitForTimeout(400);
 if(w===412){ for(let i=0;i<4;i++){ await p.evaluate(i=>document.querySelectorAll('.el-dot')[i].click(),i); await p.waitForTimeout(700); await p.locator('#elSpotlight').screenshot({path:'/tmp/claude-0/shots/elspot'+i+'.png'}); } await p.screenshot({path:'/tmp/claude-0/shots/landing412.png'}); }
 // click each slide
 const exp=[['home','Who is paying'],['chamber','U.S. House'],['chamber','U.S. Senate'],['method','How every page']];
 for(let i=0;i<4;i++){
   await p.evaluate(()=>{const o=document.getElementById('simOverlay'); if(o.classList.contains('open')){const c=o.querySelector('[class*=close],#simClose'); if(c) c.click();}});
   await p.waitForTimeout(500);
   await p.evaluate(i=>{document.querySelectorAll('.el-dot')[i].click();},i); await p.waitForTimeout(700);
   await p.evaluate(()=>document.getElementById('elSpotlight').click()); await p.waitForTimeout(3000);
   const fr=p.frames().find(f=>f!==p.mainFrame()&&f.url()!=='about:blank'&&f.url()!=='');
   const h=fr?await fr.textContent('h1').catch(()=>null):null;
   const ok=h&&h.indexOf(exp[i][1])>-1; console.log(w,'slide',i,'->',h,ok?'ok':'FAIL'); if(!ok) fails++;
   if(i===1&&w===412){ await p.screenshot({path:'/tmp/claude-0/shots/al_state412.png'}); const bad=await fr.evaluate(()=>document.querySelectorAll('.badge .sdot.live').length); console.log('green dots',bad); if(!bad) fails++; }
 }
 if(errs.length){console.log(errs.slice(0,5)); fails+=errs.length;}
 await p.close(); }
 await b.close(); console.log('fails:',fails);
})();
