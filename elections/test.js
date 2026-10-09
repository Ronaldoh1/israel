const {chromium}=require(process.env.NODE_PATH_PW||'/opt/npm-tools/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
 const file=process.argv[2], shots=process.argv[3]||'';
 let fails=0;
 for(const w of [412,375,1280]){
  const p=await b.newPage({viewport:{width:w,height:860}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error'&&!/fonts|ERR_|net::/.test(m.text()))errs.push(m.text())});
  await p.goto('file://'+file); await p.waitForTimeout(300);
  const views=[['home'],['chamber','senate'],['chamber','house'],['state','TX'],['state','CA'],['state','WY'],['race','TX-SEN'],['race','CA-12'],['race','AK-SEN'],['cand','tx-sen-ken-paxton'],['dash','tx-sen-ken-paxton'],['cand','al-sen-barry-moore'],['dash','al-sen-barry-moore'],['method'],['keyvotes'],['stances'],['casestudy','massie'],['chamber','governor'],['race','AL-GOV'],['cand','al-07-terri-sewell'],['compare','TX-SEN'],['compare','MI-SEN'],['cand','tx-sen-james-talarico']];
  for(const [v,a] of views){
   await p.evaluate(([v,a])=>window.__EL26.go(v,a),[v,a]); await p.waitForTimeout(80);
   const ov=await p.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth);
   if(ov>1){console.log(w,v,a,'HSCROLL',ov);fails++;}
   if(shots&&w===412) await p.screenshot({path:`${shots}/${v}_${a||''}.png`,fullPage:true});
  }
  // interaction: click through home->senate->filter->race->candidate->dash->back
  await p.evaluate(()=>window.__EL26.go('home'));
  await p.click('[data-go=chamber][data-arg=senate]'); await p.fill('#ssearch','tex'); await p.click('#slist .row');
  await p.click('.card.tap[data-go=cand]'); await p.click('button[data-go=dash]'); await p.click('#back'); await p.click('#back');
  const t=await p.textContent('h1'); if(!/Texas/.test(t)){console.log('nav fail',t);fails++;}
  await p.evaluate(()=>window.__EL26.go('home')); await p.fill('#gsearch','ossoff'); const n=await p.$$eval('#gres .row',r=>r.length); if(n<1){console.log('search fail');fails++;}
  if(errs.length){console.log(w,errs);fails+=errs.length;}
  await p.close();
 }
 await b.close(); console.log('fails:',fails);
})();
