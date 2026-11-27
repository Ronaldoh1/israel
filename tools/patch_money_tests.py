#!/usr/bin/env python3
"""Adds "Whose money?" to the Road to 1948 network map's Tests: removes the documented money by source
(or keeps only one source) while the people and their other ties stay, and says plainly that removing all
money gives 0% by construction. Figures computed on the restored model, 26 Nov 2026. Idempotent.

Usage: python3 tools/patch_money_tests.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if 'const VMONEY=' in s:
    print('money tests already applied'); sys.exit(0)

T = r"""const VM_ROTH=['edmond_r','james_armand'];
const VM_WEALTH=['edmond_r','james_armand','schiff','warburg_f','sieff','marks_s','mond','straus_n','wissotzky','feinberg','kaufmann_e','hecht'];
const VM_US=['upa','uja','jdc','meir','zoa','americans_haganah','sonneborn_inst','ajrc','straus_n','schiff','warburg_f','feinberg','kaufmann_e','hecht','mickey_cohen','siegel','state_dept'];
const VM_OWN=['shekel','jct','jnf','blue_box','keren_hayesod','kofer','jewish_agency','herzl','sacher'];
const vmShare=ids=>{ const m=VB.edges.filter(e=>e[2]===0); const t=m.reduce((a,e)=>a+e[4],0)||1; return Math.round(m.filter(e=>ids.includes(e[0])).reduce((a,e)=>a+e[4],0)/t*100); };
const VMONEY=[
 {id:'m_all', q:'What if there had been no money at all?', drop:()=>vMoneyDrop(()=>true),
  what:'Every documented money tie on the map, about $404 million in 1948 dollars from 1882 to 1948: the Rothschild colonies, the fund drives, the transfer agreement, the 1948 tour, the movement\'s dues and tins. The people, the land, the arms, the diplomacy and the organisation all stay.',
  read:'0%, at any date: not possible. This result is built into the map. It counts six things a state needs (money, land, arms, diplomacy, organisation and recognition) and multiplies them, so any one at zero makes the whole zero; taking out all the arms gives 0% too. It shows that money was required, which no one disputes. The tests below ask the question that tells you more: whose money mattered, and when.'},
 {id:'m_roth', q:'What if Edmond de Rothschild\'s money had never come?', drop:()=>vMoneyDrop(e=>VM_ROTH.includes(e[0])),
  what:'The money of Edmond de Rothschild and his son James Armand: the colonies from 1882, the land company PICA, "over sixty million dollars" by 1934 at 1913 prices. About 36% of all documented money. The family\'s other ties stay.',
  read:'About 36% on time and 44% at any later date, with about 38 years of work lost: unlikely. A third of the money, but more than half of the chance, because it came first: from 1882, when almost no one else was paying, it bought the land and built the colonies everything later stood on. Removing the Rothschilds entirely, ties and all, gives about 34%, close to this figure: their weight was mostly their money.'},
 {id:'m_wealthy', q:'What if the wealthy donors had kept their money: the Rothschilds, Schiff, Warburg, Sieff, Marks, Mond and the rest?', drop:()=>vMoneyDrop(e=>VM_WEALTH.includes(e[0])),
  what:'Every individual donor of wealth on the map, among them Edmond and James de Rothschild, Jacob Schiff, Felix Warburg, Israel Sieff, Simon Marks, Alfred Mond and Nathan Straus. About 38% of all documented money.',
  read:'About 35% on time and 43% at any later date: unlikely. Almost all of the effect is the Rothschild money; the other wealthy donors together move the figure by about one point.'},
 {id:'m_us', q:'What if no American money had come?', drop:()=>vMoneyDrop(e=>VM_US.includes(e[0])),
  what:'The American fund drives (the United Palestine Appeal, the United Jewish Appeal, the Joint Distribution Committee), Golda Meyerson\'s 1948 tour, the arms buyers and the American donors. About 37% of all documented money, as much as the Rothschilds\'.',
  read:'About 84%: still likely, but delayed by about a year. As much money as the Rothschilds gave, but it weighs far less, because most of it came late, in the 1940s, after the ground was built; the map treats late money as easier to replace. Meyerson\'s $50 million in 1948 was raised for arms when the state was months away.'},
 {id:'m_haavara', q:'What if there had been no transfer agreement with Nazi Germany?', drop:()=>vMoneyDrop(e=>e[0]==='haavara'),
  what:'The Haavara agreement of 1933 between Zionist bodies and the German economics ministry, which let German Jews move about 105 million Reichsmarks, about $35 million, as German goods through the Anglo-Palestine Bank. About 15% of all documented money.',
  read:'About 89%, almost no change. The transfer brought a large sum in the 1930s, but the state did not depend on it.'},
 {id:'m_own', q:'What if the movement had raised nothing of its own: no dues, no donation tins, no Keren Hayesod, no defence levy?', drop:()=>vMoneyDrop(e=>VM_OWN.includes(e[0])),
  what:'The shekel membership dues, the Jewish Colonial Trust, the Jewish National Fund and its Blue Box tins, Keren Hayesod, the Kofer HaYishuv defence levy and the Jewish Agency\'s own funds. About 10% of all documented money.',
  read:'About 92%, almost no change. The movement\'s own small-donor money was real and widely given, but on the record it was a tenth of the money, too little to carry the founding or to be missed. Unrecorded giving is not counted, so this most likely understates it.'},
 {id:'m_only_roth', q:'What if the Rothschilds\' money had been the only money?', drop:()=>vMoneyDrop(e=>!VM_ROTH.includes(e[0])),
  what:'Every documented money tie except Edmond and James de Rothschild\'s.',
  read:'About 60% on time and 62% ever: possible, with great difficulty. One family\'s money, alone, carries the founding most of the way.'},
 {id:'m_only_us', q:'What if American money had been the only money?', drop:()=>vMoneyDrop(e=>!VM_US.includes(e[0])),
  what:'Every documented money tie except the American ones.',
  read:'About 13% on time and 31% ever: unlikely. The same amount of money as the Rothschilds\', arriving later, carries less than a quarter as far.'},
 {id:'m_only_own', q:'What if the movement\'s own funds had been the only money?', drop:()=>vMoneyDrop(e=>!VM_OWN.includes(e[0])),
  what:'Every documented money tie except the movement\'s dues, tins, funds and levy.',
  read:'About 4% on time and 13% ever: not possible on this record. The movement could not have paid for its state itself.'}
];
let vMoneyCache=null;
function vMoneyResults(){ if(vMoneyCache) return vMoneyCache; vMoneyCache=VMONEY.map(t=>vRunScenario(t,()=>({t, rd:vRead(vScore(removed))}))); return vMoneyCache; }
function vMoneyList(){ return `<h3 class="vsec">Whose money?</h3><p class="vtxt">The map records about $404 million in 1948 dollars flowing into the founding from 1882 to 1948. These tests take money out by its source, or keep only one source, while the people and their other ties stay. Taking out all of it gives 0% by the map's own design, since a state needs money as it needs arms; the tests after it show which money mattered, and why timing counts as much as size.</p><div class="vtlist">${vMoneyResults().map((x,i)=>`<button class="vtrow" type="button" data-money="${i}">${vRing(x.rd.on,x.rd.verdict)}<span class="vtq"><span class="vfeat">Whose money?</span><b>${esc(x.t.q)}</b><small><span class="vtl" style="background:${vLight(x.rd.verdict)[0]}"></span>${esc(x.rd.verdict)} · ${Math.round(x.rd.on)}% on time · ${Math.round(x.rd.ever)}% ever</small></span><span class="vtgo" aria-hidden="true">›</span></button>`).join('')}</div>`; }
vCard.addEventListener('click', e=>{ const b=e.target.closest('[data-money]'); if(!b) return; e.stopPropagation(); vClose(); vRunTest(VMONEY[+b.dataset.money]); }, true);
"""
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
rep('const BRK_KIND=', T + 'const BRK_KIND=')
rep('  ${vCaseList()}\n', '  ${vMoneyList()}\n  ${vCaseList()}\n')
a = "   ...vCaseResults().map((x,i)=>({a:`data-case=\"${i}\"`,q:x.t.q,on:x.rd.on,ever:x.rd.ever,v:x.rd.verdict,k:'Test of the case'})),"
rep(a, a + "\n   ...vMoneyResults().map((x,i)=>({a:`data-money=\"${i}\"`,q:x.t.q,on:x.rd.on,ever:x.rd.ever,v:x.rd.verdict,k:'Whose money?'})),")
open(P, 'w', encoding='utf-8').write(s)
print('money tests applied:', s.count("{id:'m_"))
