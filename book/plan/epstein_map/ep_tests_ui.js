/* ---------- Tests: preset what-if questions on the Epstein map (mirrors the 1948 map's Tests) ---------- */
function vReach(rem){ const live=vAlive(rem), adj=new Map(); for(const [f,t] of VB.edges){ if(rem.has(f)||rem.has(t)) continue; if((VENT.has(f)&&!live.has(f))||(VENT.has(t)&&!live.has(t))) continue; (adj.get(f)||adj.set(f,[]).get(f)).push(t); (adj.get(t)||adj.set(t,[]).get(t)).push(f); }
  const seen=new Set(VB.hubs.filter(h=>!rem.has(h))), q=[...seen]; while(q.length){ const u=q.pop(); for(const v of adj.get(u)||[]) if(!seen.has(v)){ seen.add(v); q.push(v); } } return seen; }
function vCollapsed(){ const seen=vReach(removed), seen0=vReach(new Set()); return [...seen0].filter(x=>!seen.has(x)&&!removed.has(x)); }
const G=k=>VB.groups[k].filter(x=>N.get(x));
const VTESTS=[
 {q:'What if Jeffrey Epstein had never been in the picture?', ids:()=>['epstein'],
  what:'Jeffrey Epstein, and with him everything he owned: his companies and trusts (Southern Trust, Financial Trust, JEGE, Plan D and the others), the houses, the island and the aircraft.',
  read:'Nothing runs. Every documented payer paid him, every account was his or his companies\', and the properties and aircraft were his. Maxwell\'s own ties remain, but on this record none of them carried money, banking or property. The record does not show an operation that existed apart from him.'},
 {q:'What if Ghislaine Maxwell had never been in the picture?', ids:()=>['gmax'],
  what:'Ghislaine Maxwell and her documented ties: her conviction as his co-conspirator (December 2021), the more than $30 million he transferred to her (1999–2007), the travel schedules she gave his pilot, the staff manual she issued at the Palm Beach house, and her social ties.',
  read:'On the documented ties the operation still runs: the money, the accounts, the properties and most of the staff ties were his, not hers. This is where a model that counts ties reaches its limit. Her conviction covers years of conduct and counts here as one tie. The map does not say who would have done what she did, and it names no one as her successor; it shows only that the rest of the documented network, most of it his staff, his office and his houses, is still there.'},
 {q:'What if neither Epstein nor Maxwell had been in the picture?', ids:()=>['epstein','gmax'],
  what:'Both, with everything they owned.',
  read:'With both gone no one is left to run it: the companies, trusts, properties and aircraft fall with their owners, and every channel is empty.'},
 {q:'What if Les Wexner had never trusted him with his money?', ids:()=>['wexner'],
  what:'Les Wexner and his ties: the 1991 power of attorney, the Manhattan house transferred to an Epstein entity, and the assets worth roughly $100 million that the New York Times counted as reaching Epstein through the relationship.',
  read:'Wexner\'s money came first. Read year by year, from 1991 to 2011 almost all the money the record quantifies is his; without it those twenty years run on a few million dollars, and Black\'s money arrives only in 2012. The houses, the island and the staff are still on the map, but the record shows no other way they were paid for. Wexner has said Epstein misappropriated vast sums from him, and that Epstein returned $46 million in 2008.'},
 {q:'What if Leon Black had never paid him?', ids:()=>['black','bv70'],
  what:'Leon Black\'s payments ($158 million plus $12 million in fees, 2012–17; about $170 million by the Senate Finance Committee\'s count) and his company BV70\'s loans to Plan D.',
  read:'Black was the largest single payer in the record, but his money came late. By 2012 the houses, the island, the aircraft and the staff had long been in place, so on a year-by-year reading the first two decades are untouched. Black denies any misconduct and says the payments were for tax advice.'},
 {q:'What if neither Wexner nor Black had paid him?', ids:()=>G('The big payers (Wexner and Black)'),
  what:'Wexner and Black together: almost all the money the record puts a number on.',
  read:'What is left of the documented money is a 1987–93 consultancy from Steven Hoffenberg, the Edmond de Rothschild group\'s 2015 fee and a few paying clients with no stated sums. On this record the operation could not have been paid for.'},
 {q:'What if JPMorgan had never taken him as a client?', ids:()=>['jpm'],
  what:'JPMorgan Chase: his bank from 1998 to 2013, kept through his 2006 arrest and his 2008 plea.',
  read:'One bank alone is replaceable on this record: Deutsche Bank took him on in 2013, and other banks held accounts too (FirstBank in Puerto Rico from 2002, HSBC, Goldman Sachs until 2010, Wells Fargo later). JPMorgan paid $290 million to settle the victims\' class action in 2023 and $75 million to the Virgin Islands, without admitting liability.'},
 {q:'What if no bank had kept him as a client?', ids:()=>G('The banks'),
  what:'Every bank on the map: JPMorgan, Deutsche Bank, Bank of America, Goldman Sachs, HSBC, Wells Fargo, FirstBank, TD Bank, Citi, UBS, Bank Leumi and the others.',
  read:'Banking is the channel nothing else in the record could supply. Without a bank to hold his accounts, the money, the payroll, the property costs and the wires have no route. It is the clearest structural finding of the model: the operation depended on banks keeping him after the red flags, a point regulators later made (Deutsche Bank\'s $150 million New York penalty, 2020).'},
 {q:'What if there had been no 2008 deal?', ids:()=>['npa'],
  what:'The 2008 non-prosecution agreement, and with it the immunity it gave him and the four people it named.',
  read:'Without the deal the case goes federal in 2008: Marie Villafaña had drafted a 60-count indictment. The model takes that to end the operation\'s later years, so everything documented after 2008 drops out: Black\'s money, the Deutsche Bank years, the Great St. James purchase, the later aircraft. What is left is the operation as it stood in 2008. The model cannot say what a federal jury would have decided.'},
 {q:'What if Alexander Acosta had not been the US Attorney?', ids:()=>['acosta'],
  what:'Alexander Acosta, the US Attorney in Miami who approved the deal.',
  read:'Removing Acosta alone barely changes the deal. On the record the push for it came from a large defence team, from the supervisor who negotiated the plea route and from the state attorney\'s lesser charge; the resistance came from the line prosecutor, the police chief and the FBI agents. An unnamed successor faces the same push, minus Jay Lefkowitz\'s personal approaches to Acosta. The Justice Department\'s own review (2020) found "poor judgment", not misconduct.'},
 {q:'What if he had not had his 2005–08 defence team?', ids:()=>G('The defence lawyers (2005-08)'),
  what:'Jay Lefkowitz, Kenneth Starr, Alan Dershowitz, Lilly Ann Sanchez, Roy Black and Jack Goldberger.',
  read:'The lawyers were the deal\'s main push on this record. Without them its chance falls by about a third, and in the branch where there is no deal the operation\'s later years do not happen.'},
 {q:'What if the Miami Herald had not published "Perversion of Justice"?', ids:()=>G('The Miami Herald and its series'),
  what:'Julie K. Brown, the Miami Herald and its November 2018 series.',
  read:'The model keeps most of the chance of the 2019 arrest, because other pushes remain: Virginia Giuffre\'s litigation and Judge Marra\'s February 2019 ruling that the deal broke the victims\' rights law. The record itself credits the arrest largely to the series, which a count of pushes cannot fully weigh; read this as the most the arrest could have kept.'},
 {q:'What if Virginia Giuffre had not gone to court?', ids:()=>['giuffre','boies'],
  what:'Virginia Giuffre and her lawyer David Boies: her 2009 settlement with Epstein, her 2015 defamation suit against Maxwell and her other litigation.',
  read:'Her litigation is one push among several toward the 2019 case, so removing it alone lowers the arrest\'s chance only a little. Her sworn allegations bear more on other parts of the map than on this model\'s two decisions.'},
 {q:'What if the Virgin Islands had not given him tax breaks?', ids:()=>['usvi_edc','usvi'],
  what:'The Virgin Islands government and its Economic Development Commission: tax benefits to Financial Trust ($219.8 million, 1999–2012) and Southern Trust ($80.6 million, 2013–18).',
  read:'The tax breaks were a large public benefit, but on this record they protected his wealth rather than ran the operation, so they count as cover, and removing them changes little. The territory later sued JPMorgan ($75 million settlement) and Leon Black ($62 million).'},
 {q:'What if he had owned none of the houses or the island?', ids:()=>G('The properties'),
  what:'9 East 71st Street, El Brillo Way in Palm Beach, Little and Great St. James, Zorro Ranch, the Paris apartment and the East 66th Street apartments.',
  read:'The places are where the documented conduct happened; the criminal and civil records tie it to them. They were his, and the model reads their loss as a heavy blow but not the end, because the money that bought them is still there.'},
 {q:'What if he had had no private aircraft?', ids:()=>G('The aircraft and pilots'),
  what:'The Boeing 727 and the two Gulfstreams, the companies that held them, Shmitka Air, and the pilots Larry Visoski and David Rodgers.',
  read:'The planes moved people between the houses. Removing them weakens places and staff, but the houses and the money remain.'},
 {q:'What if no one had managed his reputation?', ids:()=>G('The reputation managers'),
  what:'Al Seckel, the Philippines search-engine team, Osborne & Partners, Peggy Siegal and R. Couri Hay.',
  read:'The reputation work after 2008 (search-result clean-up, a reputation memo, society introductions) counts as access. It served his standing, not the running of the operation, so on this model removing it changes almost nothing.'},
];
let vTestCache=null;
function vRunScenario(t, fn){ const r0=new Set(removed); removed.clear(); t.ids().forEach(x=>{ if(N.get(x)) removed.add(x); }); const out=fn(); removed.clear(); r0.forEach(x=>removed.add(x)); return out; }
function vTestResults(){ if(vTestCache) return vTestCache; vTestCache=VTESTS.map(t=>vRunScenario(t,()=>{ const R=vScore(removed); return {t, R, v:vVerdict(R.P)}; })); return vTestCache; }
function vRing(v, label){ const [lc]=vLight(label), r=15, c=2*Math.PI*r, f=Math.max(0,Math.min(1,v/100));
  return `<svg width="44" height="44" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="${r}" fill="none" stroke="var(--line)" stroke-width="5"/><circle cx="22" cy="22" r="${r}" fill="none" stroke="${lc}" stroke-width="5" stroke-linecap="round" stroke-dasharray="${(c*f).toFixed(1)} ${c.toFixed(1)}" transform="rotate(-90 22 22)"/><text x="22" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="currentColor">${Math.round(v)}</text></svg>`; }
function vTestsTable(){
  const rows=vTestResults().map((x,i)=>`<button class="vtrow" type="button" data-test="${i}">${vRing(x.R.P, x.v)}<span class="vtq"><b>${esc(x.t.q)}</b><small><span class="vtl" style="background:${vLight(x.v)[0]}"></span>${esc(x.v)} · ${Math.round(x.R.P)}% runs${x.R.deal!=null&&x.R.deal<0.995?` · deal ${vPct(x.R.deal)}`:''}${x.R.account!=null&&x.R.account<0.995?` · brought to account ${vPct(x.R.account)}`:''}</small></span><span class="vtgo" aria-hidden="true">›</span></button>`).join('');
  vOpen(`<div class="kind">Tests</div><h3 id="vmH">What would have happened if…</h3>
  <p class="vtxt">Each test removes part of the documented network and recalculates the whole map. The ring shows the chance the operation still runs as the record documents it, 1991–2019; its colour is the verdict (green runs, yellow weakened or crippled, red very unlikely or not at all). Where a test moves the 2008 deal or the 2019 arrest, that is shown too. Tap a test to run it on the map.</p>
  <div class="vtlist">${rows}</div>
  <div class="vbtns"><button class="vbtn" type="button" data-v="how">How the chances are computed</button><button class="vbtn" type="button" data-v="close">Close</button></div>`); }
vCard.addEventListener('click', e=>{ const b=e.target.closest('[data-test]'); if(!b) return; vClose(); vRunTest(+b.dataset.test); });
function vAssess(x){ const col=vCollapsed(), R=vScore(removed);
  return `<div class="kind">Test</div><h2>${esc(x.t.q)}</h2><div class="viab">${vHead(R)}</div>
  <h3 class="vsec">What was taken out</h3><p class="vtxt">${esc(x.t.what)}</p>
  <h3 class="vsec">What collapsed</h3><ul class="vul"><li>${removed.size} node${removed.size===1?'':'s'} removed.</li>
   <li>${col.length} more node${col.length===1?'':'s'} cut off from the operation, shown on the map with red dashed rings${col.length?`: ${col.slice(0,30).map(x=>esc(vName(x))).join(', ')}${col.length>30?` and ${col.length-30} more`:''}`:''}.</li>
   <li>Money in still reaching him: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])}.</li></ul>
  <h3 class="vsec">The six channels</h3>${vBars(R)}
  ${R.decisions&&R.decisions.length?'<h3 class="vsec">Key decisions</h3>'+vDecText(R):''}${vNeed(R)}
  <h3 class="vsec">Reading the result</h3><p class="vtxt">${esc(x.t.read)}</p>
  <div class="vbtns"><button class="vbtn pri" type="button" id="vtBack">All tests</button><button class="vbtn" type="button" id="vtReset">Reset the graph</button><button class="vbtn" type="button" id="vtHow">How this is computed</button></div>`; }
function vWire(){ const b=$('vtBack'); if(b) b.onclick=vTestsTable; const r=$('vtReset'); if(r) r.onclick=()=>$('reset').click(); const h=$('vtHow'); if(h) h.onclick=vIntro; }
function vShowWhole(){ if(+$('depth').value<5){ $('depth').value=5; $('dval').textContent=dlab(5); } needFit=true; }
function vRunTest(i){ const x=vTestResults()[i], before=vScore(removed).P;
  if(mode!=='del') setMode('del'); vShowWhole(); removed.clear(); draw(); fit(true);
  const ids=x.t.ids().filter(id=>N.get(id));
  setTimeout(()=>{ ids.forEach(id=>removed.add(id)); vSave(); const r=reconnect(); hiNodes=r.nodes; hiEdges=r.edges; draw(); vAnimate(new Set(ids));
    $('side').innerHTML=vAssess(x); vWire(); setSheet('mid'); vSignal('Test: '+x.t.q, before); }, 650); }
function vAnimate(ids){ const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches; let k=0;
  if(!reduce) gn.selectAll('g.n').filter(d=>ids.has(d.id)).each(function(d){ const g=d3.select(this), delay=Math.min(k++,60)*25;
    g.append('circle').attr('class','vpulse').attr('r',8).attr('fill','none').attr('stroke','#D64545').attr('stroke-width',3).attr('opacity',.9).transition().delay(delay).duration(900).attr('r',34).attr('opacity',0).remove();
    g.select('circle.dot').transition().delay(delay).duration(500).attr('r',3); });
  setTimeout(vDecorate, reduce?0:700); }
function vDecorate(){ if(!removed.size){ gn.selectAll('g.n circle.dot').attr('stroke-dasharray',null); return; }
  const col=new Set(vCollapsed()); gn.selectAll('g.n').each(function(d){ const c=d3.select(this).select('circle.dot');
    if(col.has(d.id)) c.attr('stroke','#D64545').attr('stroke-width',2.2).attr('stroke-dasharray','3 2'); else c.attr('stroke-dasharray',null); }); }
const vDraw0 = draw;
draw = function(){ vDraw0(); try{ vDecorate(); }catch(e){} };
document.head.insertAdjacentHTML('beforeend', `<style>
.vtlist{display:flex;flex-direction:column;gap:6px;margin-top:10px}
.vtrow{display:grid;grid-template-columns:44px 1fr 14px;gap:10px;align-items:center;text-align:left;width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:14px;background:transparent;color:inherit;cursor:pointer;font:inherit}
.vtrow:hover,.vtrow:focus-visible{border-color:var(--gold-2)}
.vtq b{display:block;font-size:13.5px;line-height:1.3;font-weight:600}.vtq small{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);margin-top:3px;line-height:1.35;flex-wrap:wrap}
.vtl{flex:none;width:9px;height:9px;border-radius:50%}.vtgo{font-size:22px;color:var(--muted)}
.vsec{font:600 1rem/1.3 var(--f-display);margin:16px 0 4px}.vul{margin:4px 0 0;padding-left:18px;font-size:13px;line-height:1.5}
</style>`);
$('mExpand').insertAdjacentHTML('beforebegin','<button id="mTests" type="button" title="Preset what-if tests">Tests</button>');
$('mTests').onclick=vTestsTable;
$('whole').insertAdjacentHTML('afterend','<button id="toolTests" class="ghost" type="button">Run a test</button>');
$('toolTests').onclick=vTestsTable;
