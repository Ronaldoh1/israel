/* ---------- Tests: preset what-if questions, run on the whole map (road map only) ---------- */
function vCollapsed(){ const lost=vLost(removed), seen=vReach(lost), seen0=vReach(new Set()); return [...seen0].filter(x=>!seen.has(x)&&!lost.has(x)); }
function vMoneyDrop(pred){ return VB.edges.filter(e=>e[2]===0&&pred(e)).map(e=>e[0]+'>'+e[1]); }
const ROTH=()=>new Set(VB.groups['Rothschild family and houses']);
const USSET=()=>new Set(VB.groups['Without the United States']);
const VTESTS=[
 {id:'herzl', q:'What if Theodor Herzl had never been in the picture?', ids:()=>['herzl'],
  what:'Theodor Herzl and every documented tie he made: the Congresses he led, his diplomacy with the Sultan, the Kaiser, the Pope and the British, and the newspaper he paid for.',
  read:'The movement Herzl founded is still in the record without him: the Zionist Organization, the Jewish Colonial Trust and the Jewish National Fund carried on under Wolffsohn, Nordau and Weizmann, and the documents he never touched (the Balfour Declaration, the Mandate, the UN vote) do not depend on him. The map cannot remove what he started together with the man; for that, run "What if Zionism had never become an organized movement?".'},
 {id:'movement', q:'What if Zionism had never become an organized movement?', ids:()=>[...[...N.values()].filter(n=>n.cluster==='zionist movement').map(n=>n.id), 'wzo','jewish_agency','jnf','keren_hayesod','jct','apc_bank','congress1897','shekel','die_welt'].filter(x=>N.get(x)),
  what:'The whole organized movement: its leaders, the Zionist Organization and its Congresses, the Jewish Agency, and the funds it built (the Jewish National Fund, Keren Hayesod, the Jewish Colonial Trust and its bank, the shekel dues).',
  read:'Without an organized movement there is no one to pursue the state: the money, the land purchases, the diplomacy and the organization all had the movement as their carrier. Outside support remains on the map (governments, the UN, donors, armed groups), but on this record none of it set out to build the state on its own. Compare "What if Theodor Herzl had never been in the picture?": the founder alone is not the movement.'},
 {id:'rothmoney', q:'What if the Rothschilds had not provided the funding?', drop:()=>vMoneyDrop(e=>ROTH().has(e[0])||ROTH().has(e[1])),
  what:'Every documented money tie to or from the Rothschild family and houses, including Edmond de Rothschild\'s investment (over $60 million in Palestine, reported in 1934 (≈ $1.5 billion today)) and the colonies and companies he funded. The family\'s other ties (letters, meetings, the Balfour Declaration) stay.',
  read:'Edmond\'s money is the single largest sum in the record, and for its first two decades almost the only money in it: from 1882 he carried the colonies when no one else documented could. Later money (Keren Hayesod from 1921, the American appeals, the 1948 tour) still reaches the movement, but it cannot give back the years before it existed.'},
 {id:'roth', q:'What if the Rothschild family had played no part at all?', ids:()=>VB.groups['Rothschild family and houses'],
  what:'Every member and house of the Rothschild family in the map, with all their ties: the money, the colonies, the letters and meetings, and Walter Rothschild\'s role as addressee and drafter of the Balfour Declaration.',
  read:'By default the Balfour Declaration still stands, because the bodies that issued it (the War Cabinet, Balfour, the British government) remain; it would have needed another addressee. The loss is then mostly Edmond\'s money and the years before anyone else could fund the colonies. Run "What if the Declaration needed Walter Rothschild?" to see the stricter reading.'},
 {id:'walter', q:'What if the Declaration needed Walter Rothschild?', ids:()=>['walter_r'], strict:true,
  what:'Walter Rothschild, the Declaration\'s addressee and one of its drafters, under the stricter reading: a document could not have been issued without its named addressee. With him goes the Balfour Declaration, and with it the Mandate that wrote it into its text.',
  read:'This test takes an argument some make, that Britain would not have issued the Declaration to anyone else. The record documents that it was addressed to him and that he worked on its draft with Weizmann; it does not document that it would have been withheld otherwise. Under the default reading, removing Walter alone changes little, because Weizmann was doing the same work at the same time.'},
 {id:'edmond', q:'What if Edmond de Rothschild had not bought land and funded colonies in Palestine?', drop:()=>VB.edges.filter(e=>(e[0]==='edmond_r'||e[1]==='edmond_r')&&(e[2]===0||e[2]===1)).map(e=>e[0]+'>'+e[1]),
  what:'Edmond de Rothschild\'s money and land ties: the colonies he funded from 1882 (Rishon LeZion, Zikhron Ya\'akov, Rosh Pinna, Metulla and others), his transfer to the Jewish Colonization Association, and PICA. He stays on the map for his other ties.',
  read:'Edmond carried the first colonies from 1882, when they were failing, and for two decades his money was almost the only money in the record. With the work placed in the years it was done, no documented actor could have done it in those years: the Zionist Organization\'s funds were small, the Keren Hayesod began only in 1921, and the large American appeals came in 1946-48. And what he built stayed built, so the shortfall keeps counting until later money outgrows it, which on this record happens only after the war. Later land buyers (the Jewish National Fund, Hankin, the Palestine Land Development Company) still bought land, which limits the loss on land.'},
 {id:'balfour', q:'What if there had been no Balfour Declaration?', ids:()=>['balfour_decl'],
  what:'The Balfour Declaration of 2 November 1917 and every tie to it: its drafting, its approval by the War Cabinet, its American endorsements, and its incorporation into the Mandate.',
  read:'The Mandate wrote the Declaration into its text, so without the Declaration there is no Jewish national home in the Mandate. Under the Mandate the Jewish population grew about ten times faster than under Ottoman rule; without it, immigration and settlement from 1920 to 1948 go at the Ottoman pace, and most of those years\' work is lost. The UN vote of 1947 still happens on its own terms.'},
 {id:'britain', q:'What if Britain had not backed the project?', ids:()=>VB.groups['British government'],
  what:'The British government, its cabinets and officials, Parliament and the Mandate administration, with every tie.',
  read:'Without the British state the Balfour Declaration loses every body that issued it, except its later American endorsements, and the Mandate loses its Mandatory power.'},
 {id:'us', q:'What if the United States had stayed out?', ids:()=>VB.groups['Without the United States'], drop:()=>VB.drop['Without the United States']||[],
  what:'The American government, Congress and parties, the American Zionist organizations, and American funders and arms buyers, plus the money raised in America by others (Golda Meyerson\'s 1948 tour).',
  read:'This removes the largest share of money after Edmond\'s, the American votes and pressure at the UN, the first recognition of the state, and the American arms network at once.'},
 {id:'moscow', q:'What if only Moscow had backed partition, and Washington had stayed out?', ids:()=>['us_gov'],
  what:'The American government as a state: its vote for partition, its recognition, its diplomacy. American Zionist organizations, donors and Congress stay; the Soviet Union and its side still back partition.',
  read:'In 1947-48 most governments moved with the bloc they depended on. In the partition vote two-thirds of the Rio Pact states and nearly three-quarters of the Marshall Plan states voted with the United States; without its lead, each of them keeps its vote and its recognition only at that bloc\'s measured independence. Moscow\'s side alone could not carry two-thirds of the Assembly. The same rule applies to the Soviet side: run "What if the Soviet bloc had not supplied arms and votes?" for the other half of the comparison.'},
 {id:'truman', q:'What if Truman had never become vice president?', ids:()=>['truman'],
  what:'Harry Truman and every documented tie he made as president: the recognition decision of 14 May 1948, the White House meeting of 12 May, the pressure on Attlee, and the access that Eddie Jacobson, Clark Clifford, David Niles and the 1948 donors (Abraham Feinberg and Ed Kaufmann) had through him. In this case Henry Wallace, the vice president the party leaders replaced in July 1944, becomes president when Roosevelt dies.',
  read:'Removing Truman takes out the man who made the decisions, not the American state: Congress, the State Department, the American Zionist organizations and the money stay. The record also shows who would have been in his place. Henry Wallace was described as a supporter of Zionism; he met Ben-Gurion and Begin in Palestine in October 1947, and in 1948 he attacked Truman from the pro-Israel side, promising to end the arms embargo. But Wallace would not have inherited the push that moved Truman: Clark Clifford\'s electoral memo, David Niles, Eddie Jacobson\'s friendship and Weizmann\'s letters were aimed at Truman, while the resistance (Marshall, the State Department, its planners, Henderson) would have stayed. The map reads the two American decisions again around Wallace; see "Key decisions" above.'},
 {id:'fdr', q:'What if Roosevelt had been healthy and kept his April 1945 pledge to Ibn Saud?', ids:()=>['truman'], decider:{us_partition:'fdr', us_recognition:'fdr'},
  what:'Roosevelt lives and serves out his term to January 1949, so there is no Truman presidency. On 5 April 1945 Roosevelt assured Ibn Saud he would take no action "which might prove hostile to the Arab people" and would consult both sides before any basic change; here Roosevelt, not Truman, decides the American vote and pressure for partition and American recognition. The push that reached Truman personally (Clifford, Niles, Jacobson, Weizmann\'s letters) reaches Roosevelt only where he had his own documented tie; his pledge counts against. If the American pressure fails, the three states reported as pressured (the Philippines, whose delegate had argued against partition, Haiti and Liberia) vote against partition. The rest of the American record stays.',
  read:'This is an assumption about what Roosevelt would have done, taken from his own last written words on the subject; he also approved a State Department plan to keep the Palestine question out of public debate during the war, and weakened a statement Stephen Wise had drafted for him. He had also, at other times, said things the Zionist leaders welcomed, so the test is one reading, not a certainty. His illness was concealed: a Navy cardiologist found heart failure in March 1944, and he died on 12 April 1945. The one earlier president whose incapacity was hidden in the same way was Woodrow Wilson, after his stroke of October 1919.'},
 {id:'un', q:'What if the UN vote had never happened?', ids:()=>VB.groups['The United Nations'],
  what:'The United Nations, its General Assembly and Security Council, and its Special Committee on Palestine. Without them there is no Resolution 181.',
  read:'The state loses the legal basis its Declaration of Independence cited, but individual states could still recognize it: the United States did so in May 1948, a year before Israel joined the UN.'},
 {id:'votes', q:'What if the three pressured votes had gone the other way?', ids:()=>['philippines','haiti','liberia'], mode:'against',
  what:'The Philippines, Haiti and Liberia, the three states reported as pressured into voting for partition, counted here as voting against it.',
  read:'Partition needed two-thirds of the votes cast. With these three against, the count is 30 to 16 and Resolution 181 fails: the margin was that narrow.'},
 {id:'soviet', q:'What if the Soviet bloc had not supplied arms and votes?', ids:()=>VB.groups['Soviet bloc'],
  what:'The Soviet Union and its bloc: their votes for partition, the Czechoslovak arms and aircraft, and their early recognitions.',
  read:'The vote still passes without the bloc\'s five votes; the larger loss is the Czechoslovak arms supply of 1948.'},
 {id:'stalin', q:'What if Stalin had not backed partition?', ids:()=>['stalin'],
  what:'Joseph Stalin and his documented ties: the Soviet decision to back partition in 1947, and his consent to the Czechoslovak arms sales of 1948. The Soviet state stays; an unnamed successor decides in his place, with no documented position of his own, so the support is an even chance at best.',
  read:'Before 1947 Soviet policy had opposed Zionism; the switch is reported as Stalin\'s own decision, made to get Britain out of Palestine. If the Soviet Union votes against, its side follows it at the bloc\'s measured loyalty, and the Czechoslovak arms lose the consent they went ahead with. The vote is close, but the American side alone still clears two-thirds in most outcomes.'},
 {id:'czech', q:'What if the Czechoslovak arms had never come?', ids:()=>['czechoslovakia','masaryk','avriel','balak'].filter(x=>N.get(x)),
  what:'Czechoslovakia as a supplier and voter, Jan Masaryk who signed the first sale on 14 January 1948, Ehud Avriel who bought for the Haganah in Prague, and the Balak airlift from Žatec.',
  read:'Through October 1948 the sales brought 34,500 rifles, over 6,000 machine guns and the first fighter aircraft; Ben-Gurion said that without them "we would have not survived". The map counts this loss modestly, and that is a limit of the map, not a finding: arms ties are weighed by their connections, not by the number of rifles and aircraft they carried, and the map measures the founding of the state on 14 May 1948, not the war that followed it.'},
 {id:'usmoney', q:'What if American money had not reached the movement?', drop:()=>[...vMoneyDrop(e=>USSET().has(e[0])||USSET().has(e[1])), ...(VB.drop['Without the United States']||[])],
  what:'Every money tie from American donors, appeals and funds (the UJA and UPA, Nathan Straus, Jacob Schiff, the arms buyers\' money, the 1948 tour). American politics and votes stay.',
  read:'This isolates the money from the rest of the American role, to compare with the Rothschild funding test.'},
 {id:'armed', q:'What if there had been no armed groups or arms network?', ids:()=>VB.groups['Armed groups and arms network'],
  what:'The Haganah, the Irgun and Lehi, their commanders, and the arms network that supplied them.',
  read:'Every other channel survives, but the arms and force channel is emptied, and on this record nothing outside it could take its place.'},
 {id:'roth_london', q:'What if the London Rothschilds had stayed out?', ids:()=>['nathan_r','lionel_r','natty','walter_r','charles_r','rozsika_r','leopold_r','evelyn_r','anthony_r','alfred_r','lionel_1882','anthony_g','nm_rothschild','victor_r','miriam_r'].filter(x=>N.get(x)),
  what:'The London branch: Nathan Mayer and his descendants (Lionel, Natty, Walter, Charles and Rózsika, Leopold, Lionel Nathan, Anthony Gustav, Victor) and N M Rothschild & Sons, with every tie.',
  read:'The London house gave the project its most famous moment, Walter as addressee of the Balfour Declaration, and Rózsika and Dorothy\'s introductions for Weizmann, but very little money, and Natty, its head in Herzl\'s day, opposed a Jewish state. Under the default reading the Declaration survives with another addressee, so the loss is small. The weight of the family on this record sits in Paris, not London.'},
 {id:'roth_paris', q:'What if the Paris Rothschilds had stayed out?', ids:()=>['james_mayer','rothschild_freres','alphonse_r','gustave_r','edmond_r','adelheid_r','james_armand','dorothy','maurice_r','edouard_r','guy_r','edmond_adolphe','batsheva_r','albert_cohn','scheid','ossowetzky','nathaniel_paris','pica','yad_hanadiv','erf','rothschild_hospital','evelina_school'].filter(x=>N.get(x)),
  what:'The Paris branch: James Mayer and his sons, Edmond and his administration in Palestine (Scheid, Ossowetzky), Edmond\'s son James and his wife Dorothy, PICA and the family\'s later foundations.',
  read:'Almost the whole of the family\'s weight on this record is the Paris line, and within it Edmond: his money carried the colonies from 1882, and his son\'s PICA held about 500,000 dunams in 1934. Take the Paris house out and the result is close to removing the whole family.'},
 {id:'roth_heirs', q:'What if Edmond\'s heirs had not carried on after he died in 1934?', ids:()=>['james_armand','dorothy','pica'].filter(x=>N.get(x)),
  what:'Edmond\'s son James Armand, James\'s wife Dorothy, and PICA, the land company James ran from 1924 and the family\'s main vehicle in Palestine after Edmond.',
  read:'Without the heirs, what Edmond built still stands, and the land PICA held is the larger loss: it was the biggest Jewish landholder in 1934. But by the 1930s the Jewish National Fund, Keren Hayesod and the American appeals were all raising money, so the founding is delayed rather than stopped.'},
 {id:'roth_barons', q:'What if neither of the two philanthropic barons had funded settlement?', ids:()=>['edmond_r','hirsch'].filter(x=>N.get(x)),
  what:'Baron Edmond de Rothschild, who funded the colonies in Palestine from 1882, and Baron Maurice de Hirsch, whose Jewish Colonization Association (1891) funded colonies in Argentina and later took over Edmond\'s colonies.',
  read:'Hirsch adds little on top of Edmond, because his money went mostly to Argentina; the loss is Edmond\'s. That is the point of the test: of the two great Jewish philanthropists of the 1880s and 1890s, only one put his fortune into Palestine.'},
 {id:'roth_conn', q:'What if the Rothschilds had given their money but none of their connections?', drop:()=>VB.edges.filter(e=>(ROTH().has(e[0])||ROTH().has(e[1]))&&e[2]!==0&&e[2]!==1).map(e=>e[0]+'>'+e[1]),
  what:'Every Rothschild tie that is not money or land: the letters, meetings and introductions (Rózsika and Dorothy for Weizmann), Walter\'s and James\'s work on the Balfour Declaration, seats in Parliament, and the family\'s roles in its own banks. The money and land stay.',
  read:'Connections matter far less than money on this record. Weizmann had other routes to the British government (C. P. Scott, Herbert Samuel, Lloyd George), and the Declaration had other advocates. What the family gave that no one else could was early money.'},
 {id:'roth_intro', q:'What if no Rothschild had opened doors for Weizmann?', ids:()=>['rozsika_r','dorothy','walter_r'].filter(x=>N.get(x)),
  what:'Rózsika Rothschild, who brought Weizmann to Charles and Walter; Dorothy de Rothschild, his correspondent and ally from 1914; and Walter, the Declaration\'s addressee and one of its drafters.',
  read:'Under the default reading the founding barely moves: Weizmann reached the cabinet through C. P. Scott and others as well. Under the strict reading, where the Declaration could only have gone to Walter, it falls with him, and the result drops to about the level of "no Balfour Declaration".'},
 {id:'rothus', q:'What if neither the Rothschilds nor the United States had been involved?', ids:()=>[...VB.groups['Rothschild family and houses'], ...VB.groups['Without the United States']], drop:()=>VB.drop['Without the United States']||[],
  what:'Both of the two largest sources of money and support in the record, removed together.',
  read:'Together they hold most of the documented money, so the money channel, which counts twice, collapses far more than either removal alone.'},
];
const VRECORD={id:'veto', q:'After 1948: what has protected Israel\'s standing at the UN?', hi:['us_vetoes','syria82','res3379','res4686','africa_aid','africa_break73','elnet','iaf','concert'],
  read:`<p class="vtxt">This one is a reading of the record, not a computed test: the 1948 model ends with the founding. Expelling or suspending a UN member needs a recommendation from the Security Council, where the United States has a veto; by 2023 it had vetoed Israel-related resolutions 46 times. When Syria moved in 1982 to "review Israel's status", the State Department warned that suspension or expulsion "would have serious consequences for continued U.S. participation in and support for the United Nations", and no majority for expulsion formed.</p>
  <p class="vtxt">The other operations on the map (aid to Africa aimed at UN votes, ELNET in Europe, the Israel Allies Foundation's caucuses, the state-funded campaigns) build and hold allies, but they have not held majorities: African states broke ties in 1973, the General Assembly passed "Zionism is racism" in 1975 by 72 to 35, and the ministry that ran the campaigns called them "a failure by every conceivable parameter". On this record, without the American veto Israel's membership would have rested on General Assembly majorities it has not had.</p>`};
let vTestCache=null;
function vRunScenario(t, fn){ const r0=new Set(removed), d0=new Set(vDrop), m0=vMode; removed.clear(); vDrop.clear(); vMode=t.mode||VB.vote_mode; const s0=vStrict; vStrict=!!t.strict; const dc0=Object.assign({},vDecider); for(const k in vDecider) delete vDecider[k]; Object.assign(vDecider,t.decider||{}); const nv0=new Set(vNoVote), fl0=new Set(vFlip); vNoVote.clear(); vFlip.clear(); (t.novote||[]).forEach(x=>vNoVote.add(x)); (t.flip||[]).forEach(x=>vFlip.add(x));
  (t.ids?t.ids():[]).forEach(x=>removed.add(x)); (t.drop?t.drop():[]).forEach(x=>vDrop.add(x)); const out=fn();
  removed.clear(); r0.forEach(x=>removed.add(x)); vDrop.clear(); d0.forEach(x=>vDrop.add(x)); vMode=m0; vStrict=s0; for(const k in vDecider) delete vDecider[k]; Object.assign(vDecider,dc0); vNoVote.clear(); nv0.forEach(x=>vNoVote.add(x)); vFlip.clear(); fl0.forEach(x=>vFlip.add(x)); return out; }
function vTestResults(){ if(vTestCache) return vTestCache;
  vTestCache=VTESTS.map(t=>vRunScenario(t,()=>{ const R=vScore(removed); return {t, R, rd:vRead(R), vote:vVote(vLost(removed)), n:removed.size, col:vCollapsed().length}; })); return vTestCache; }
function vRing(v, label){ const [lc]=vLight(label), r=15, c=2*Math.PI*r, f=Math.max(0,Math.min(1,v/100));
  return `<svg width="44" height="44" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="${r}" fill="none" stroke="var(--line)" stroke-width="5"/><circle cx="22" cy="22" r="${r}" fill="none" stroke="${lc}" stroke-width="5" stroke-linecap="round" stroke-dasharray="${(c*f).toFixed(1)} ${c.toFixed(1)}" transform="rotate(-90 22 22)"/><text x="22" y="26" text-anchor="middle" font-size="11" font-weight="700" fill="currentColor">${Math.round(v)}</text></svg>`; }
function vTestsTable(){
  const rows=vTestResults().map((x,i)=>`<button class="vtrow" type="button" data-test="${i}">${vRing(x.rd.on, x.rd.verdict)}<span class="vtq"><b>${esc(x.t.q)}</b><small><span class="vtl" style="background:${vLight(x.rd.verdict)[0]}"></span>${esc(x.rd.verdict)}${x.t.strict?' · stricter reading':''} · ${Math.round(x.rd.on)}% on time · ${Math.round(x.rd.ever)}% ever${x.vote.passes?'':' · UN vote fails'}</small></span><span class="vtgo" aria-hidden="true">›</span></button>`).join('');
  vOpen(`<div class="kind">Tests</div><h3 id="vmH">What would have happened if…</h3>
  <p class="vtxt">Each test removes part of the documented network and recalculates the whole map. The ring shows the chance the state is still founded in 1948; its colour is the verdict (green on time, yellow likely or possible with difficulty, red unlikely or not possible). Tap a test to run it on the map.</p>
  <div class="vtlist">${rows}<button class="vtrow" type="button" data-test="record"><svg width="44" height="44" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="15" fill="none" stroke="var(--line)" stroke-width="5" stroke-dasharray="3 3"/><text x="22" y="26" text-anchor="middle" font-size="10" font-weight="700" fill="currentColor">1948+</text></svg><span class="vtq"><b>${esc(VRECORD.q)}</b><small>A reading of the record after the founding, not a computed test</small></span><span class="vtgo" aria-hidden="true">›</span></button></div>
  <h3 class="vsec">Other homelands</h3><p class="vtxt">Not removals from this map but the other lands that were proposed, offered or studied, measured on the same six channels against what the Palestine record had, in the order they were raised.</p>
  <div class="vtlist">${(VB.alt?VB.alt.alts:[]).map((a,i)=>`<button class="vtrow" type="button" data-alt="${i}">${vRing(a.chance,a.verdict)}<span class="vtq"><b>${esc(a.name)}</b><small><span class="vtl" style="background:${vLight(a.verdict)[0]}"></span>${esc(a.verdict)} · ${a.chance<1?'under 1':Math.round(a.chance)}% chance of a state</small></span><span class="vtgo" aria-hidden="true">›</span></button>`).join('')}</div>
  <div class="vbtns"><button class="vbtn" type="button" data-v="how">How the chances are computed</button><button class="vbtn" type="button" data-v="close">Close</button></div>`);
}
function vAltSrc(k){ const s=VB.alt.sources; return k.split(';').map(x=>x.trim()).filter(x=>s[x]).map(x=>`<a href="${esc(s[x][1])}" target="_blank" rel="noopener">${esc(s[x][0])}</a>`).join('; '); }
function vAlt(i){ const a=VB.alt.alts[i], P=VB.alt.palestine;
  $('side').innerHTML=`<div class="kind">Other homelands</div><h2>${esc(a.name)}</h2>
  <div class="viab"><div class="vbig"><b style="color:${vColor(a.chance)}">${a.chance<1?'&lt;1':Math.round(a.chance)}%</b><span style="font-weight:600">${esc(a.verdict)}</span></div><p class="vtxt">The chance of a Jewish state there by 1948, on the same formula as the map, from the shares below.</p></div>
  <h3 class="vsec">What the record shows</h3><ul class="vul">${a.facts.map(([f,k])=>`<li>${esc(f)} <small style="color:var(--muted)">(${vAltSrc(k)})</small></li>`).join('')}</ul>
  <h3 class="vsec">The six channels, against the Palestine record</h3>${VB.channels.map(c=>{ const [s,why]=a.share[c]; return `<div class="vrow"><span>${esc(VB.labels[c])}</span><span class="vbar"><i style="width:${Math.round(s*100)}%;background:${vColor(s*100)}"></i></span><span class="vnum">${Math.round(s*100)}%</span></div><p class="vtxt" style="margin:0 0 6px">${esc(why)}</p>`; }).join('')}
  <p class="vtxt">These shares are judgments read from the record, not counts from the map; they are shown so you can disagree with any of them.</p>
  <p class="vtxt"><b>Jewish settlers at the peak:</b> ${esc(a.peak)} (Palestine: ${esc(P.peak)}).</p>
  <h3 class="vsec">The likely path</h3><p class="vtxt">${esc(a.path)}</p>
  <h3 class="vsec">The cost</h3><p class="vtxt">${esc(a.cost)}</p>
  <h3 class="vsec">Palestine, for comparison</h3><ul class="vul">${P.facts.map(([f,k])=>`<li>${esc(f)} <small style="color:var(--muted)">(${vAltSrc(k)})</small></li>`).join('')}<li>${esc(P.path)} ${esc(P.cost)}</li></ul>
  <div class="vbtns"><button class="vbtn pri" type="button" id="vtBack">All tests</button></div>`; vWire(); setSheet('mid'); }
vCard.addEventListener('click', e=>{ const a=e.target.closest('[data-alt]'); if(a){ vClose(); vAlt(+a.dataset.alt); return; } const b=e.target.closest('[data-test]'); if(!b) return; vClose(); const k=b.dataset.test; if(k==='record') vRecord(); else vRunTest(+k); });
function vAssess(x){
  const col=vCollapsed(), R=vScore(removed), lostM=V0.cap[0]-R.cap[0], nv=[...vNoVote];
  return `<div class="kind">Test</div><h2>${esc(x.t.q)}</h2>
  <div class="viab">${vHead(R)}</div>
  <h3 class="vsec">What was taken out</h3><p class="vtxt">${esc(x.t.what)}</p>
  <h3 class="vsec">What collapsed</h3><ul class="vul">
   <li>${removed.size?removed.size+' node'+(removed.size===1?'':'s')+' removed':'No nodes removed'}${vDrop.size?`, ${vDrop.size} tie${vDrop.size===1?'':'s'} cut`:''}.</li>
   <li>${col.length} more node${col.length===1?'':'s'} cut off from the state-building core, shown on the map with red dashed rings${col.length?`: ${col.slice(0,30).map(x=>esc(vName(x))).join(', ')}${col.length>30?` and ${col.length-30} more`:''}`:''}.</li>
   ${nv.length?`<li>Not voting for partition: ${nv.map(x=>esc(vName(x))).join(', ')}.</li>`:''}${vFlip.size?`<li>Voting against instead of for: ${[...vFlip].map(x=>esc(vName(x))).join(', ')}.</li>`:''}<li>${vVoteLine(removed)}</li>
   <li>Money still reaching the movement: ${vMoney(R.cap[0])} of ${vMoney(VB.cap0[0])}${lostM>0.05?` (${vMoney(lostM)} gone)`:''}, from ${R.funders} of ${R.funders0} funders.</li></ul>
  <h3 class="vsec">The six channels</h3>${vBars(R)}
  ${R.decisions&&R.decisions.length?'<h3 class="vsec">Key decisions</h3>'+vDecText(R):''}
  <h3 class="vsec">Lost years, and who could have taken over</h3>${vYearsText(R)||'<p class="vtxt">No years of work lost.</p>'}
  ${vDelayText(R)}${vNeed(R)}
  <h3 class="vsec">Reading the result</h3><p class="vtxt">${esc(x.t.read)}</p>
  <div class="vbtns"><button class="vbtn pri" type="button" id="vtBack">All tests</button><button class="vbtn" type="button" id="vtReset">Reset the graph</button><button class="vbtn" type="button" id="vtHow">How this is computed</button></div>`;
}
function vWire(){ const b=$('vtBack'); if(b) b.onclick=vTestsTable; const r=$('vtReset'); if(r) r.onclick=()=>$('reset').click(); const h=$('vtHow'); if(h) h.onclick=vIntro; }
function vShowWhole(){ if(+$('depth').value<5){ $('depth').value=5; $('dval').textContent=dlab(5); } needFit=true; }
function vRunTest(i){
  const x=vTestResults()[i], before=vScore(removed).P;
  if(mode!=='del') setMode('del');
  vShowWhole(); removed.clear(); vDrop.clear(); vNoVote.clear(); vFlip.clear(); for(const k in vDecider) delete vDecider[k]; Object.assign(vDecider,x.t.decider||{}); (x.t.novote||[]).forEach(v=>vNoVote.add(v)); (x.t.flip||[]).forEach(v=>vFlip.add(v)); vMode=x.t.mode||VB.vote_mode; vStrict=!!x.t.strict; vLS('road_strict_v1', vStrict?1:null);
  draw(); fit(true);
  const ids=x.t.ids?x.t.ids():[], drop=x.t.drop?x.t.drop():[];
  setTimeout(()=>{
    ids.forEach(id=>removed.add(id)); drop.forEach(k=>vDrop.add(k)); vSave();
    const r=reconnect(); hiNodes=r.nodes; hiEdges=r.edges; draw(); vAnimate(new Set(ids), drop);
    $('side').innerHTML=vAssess(x); vWire(); setSheet('mid');
    vSignal('Test: '+x.t.q, before);
  }, 650);
}
function vRecord(){
  if(mode!=='expand') setMode('expand'); vShowWhole(); hiNodes=new Set(VRECORD.hi.filter(x=>N.get(x))); hiEdges=new Set(E.map((e,i)=>[e,i]).filter(([e])=>hiNodes.has(e.f)||hiNodes.has(e.t)).map(([,i])=>i)); draw(); fit(true);
  $('side').innerHTML=`<div class="kind">Reading of the record</div><h2>${esc(VRECORD.q)}</h2>${VRECORD.read}<p class="vtxt">Highlighted on the map: ${VRECORD.hi.filter(x=>N.get(x)).map(x=>esc(vName(x))).join(', ')}. Tap any of them for its sources.</p>
  <div class="vbtns"><button class="vbtn pri" type="button" id="vtBack">All tests</button></div>`; vWire(); setSheet('mid');
}
/* the removed nodes pulse out; ties cut by a test flash; everything cut off from the core gets a red dashed ring */
function vAnimate(ids, drop){
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches; let k=0;
  gn.selectAll('g.n').filter(d=>ids.has(d.id)).each(function(d){ const g=d3.select(this), delay=reduce?0:Math.min(k++,60)*25;
    if(reduce) return; g.append('circle').attr('class','vpulse').attr('r',8).attr('fill','none').attr('stroke','#D64545').attr('stroke-width',3).attr('opacity',.9)
      .transition().delay(delay).duration(900).attr('r',34).attr('opacity',0).remove();
    g.select('circle.dot').transition().delay(delay).duration(500).attr('r',3); });
  if(drop.length && !reduce){ const ks=new Set(drop); gl.selectAll('line').filter(d=>ks.has(E[d.i].f+'>'+E[d.i].t)).attr('stroke','#D64545').attr('stroke-width',3).attr('stroke-opacity',1)
      .transition().duration(1400).attr('stroke-opacity',.15).attr('stroke-width',1.1); }
  setTimeout(vDecorate, reduce?0:700);
}
function vDecorate(){ if(!removed.size&&!vDrop.size){ gn.selectAll('g.n circle.dot').attr('stroke-dasharray',null); return; }
  const col=new Set(vCollapsed()); gn.selectAll('g.n').each(function(d){ const c=d3.select(this).select('circle.dot');
    if(col.has(d.id)) c.attr('stroke','#D64545').attr('stroke-width',2.2).attr('stroke-dasharray','3 2'); else c.attr('stroke-dasharray',null); }); }
const vDraw0 = draw;
draw = function(){ vDraw0(); try{ vDecorate(); }catch(e){} };
document.head.insertAdjacentHTML('beforeend', `<style>
.vtlist{display:flex;flex-direction:column;gap:6px;margin-top:10px}
.vtrow{display:grid;grid-template-columns:44px 1fr 14px;gap:10px;align-items:center;text-align:left;width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:14px;background:transparent;color:inherit;cursor:pointer;font:inherit}
.vtrow:hover,.vtrow:focus-visible{border-color:var(--gold-2)}
.vtq b{display:block;font-size:13.5px;line-height:1.3;font-weight:600}.vtq small{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted);margin-top:3px;line-height:1.35}
.vtl{flex:none;width:9px;height:9px;border-radius:50%}
.vtgo{font-size:22px;color:var(--muted)}
.vsec{font:600 1rem/1.3 var(--f-display);margin:16px 0 4px}
.vul{margin:4px 0 0;padding-left:18px;font-size:13px;line-height:1.5}
</style>`);
/* the Tests button: first in the mode row, and in Tools */
$('mExpand').insertAdjacentHTML('beforebegin','<button id="mTests" type="button" title="Preset what-if tests">Tests</button>');
$('mTests').onclick=vTestsTable;
$('whole').insertAdjacentHTML('afterend','<button id="toolTests" class="ghost" type="button">Run a test</button>');
$('toolTests').onclick=vTestsTable;
