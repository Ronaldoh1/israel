#!/usr/bin/env python3
"""Adds "Tests of the case" to the Road to 1948 network map: one or more tests for each link of the case
argued in The Case (Volume XXVI) that the map can measure, each stating what the case says, removing the part
of the record the link rests on, and reporting the result, including results that limit the case.
Figures in the readings were computed on the restored nine-channel model (26 Nov 2026). Idempotent.

Usage: python3 tools/patch_case_tests.py [road-network.html]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
if 'const VCASE=' in s:
    print('case tests already applied'); sys.exit(0)

T = r"""const VCASE_PEOPLE=()=>({ids:['imm_ottoman','imm_1924_29','imm_1933_39'], drop:['mandate_admin>imm_1919_23','mandate_admin>imm_1924_29','mandate_admin>imm_1930_32','mandate_admin>imm_1933_39','mandate_admin>imm_1940_41','mandate_admin>imm_1942_48','mossad_aliyah>imm_1942_48']});
const vCaseOf=(id,k)=>{ const t=VTESTS.find(x=>x.id===id); return t&&t[k]?t[k]():[]; };
const VCASE_SHIELD=()=>['acpc','blackstone','blackstone_1891','darby','scofield','apc','ccp','hechler','holocaust','die_welt','jta_news','palestine_post'].concat(vCaseOf('legit_christian_us','ids'),vCaseOf('media_campaign','ids'));
const VCASE=[
 {id:'case_secular', link:1, q:'What if the movement\'s political leaders had been absent, and its religious bodies had stayed?',
  claim:'A secular political movement chose the Holy Land; the state was led into being by its political leaders, not by religious authority.',
  ids:()=>['herzl','wolffsohn','sokolow','weizmann','jabotinsky','bengurion','sharett','meir'].filter(x=>N.get(x)),
  what:'Eight political leaders of the movement and of the Jewish community in Palestine: Herzl, Wolffsohn, Sokolow, Weizmann, Jabotinsky, Ben-Gurion, Sharett and Golda Meyerson (Meir). Their organizations stay, and so do Mizrachi, Rabbi Mohilever, Rav Kook, the Chief Rabbinate and every other religious body.',
  read:'About 83%, three years late: still likely, but delayed, with 20 more parts of the map left with no route to the core. Removing the religious Zionist bodies instead leaves the chance at about 93%, unchanged, and the Orthodox bodies that opposed the movement, Agudat Israel and Neturei Karta, carry no weight either way. On this map the founding ran through the movement\'s political leadership, not through its religious bodies. The test measures who did the work, not what anyone believed.'},
 {id:'case_empire_bank', link:2, q:'What if neither the British Empire nor the Rothschilds had been involved?',
  claim:'An empire and a bank carried the movement to its state.',
  ids:()=>[...new Set([...VB.groups['British government'],...VB.groups['Rothschild family and houses']])].filter(x=>N.get(x)),
  what:'The British government (the War Cabinet that issued the Balfour Declaration, the Mandate government and every tie) and the Rothschild family and houses, together.',
  read:'About 12% on time and 32% at any later date, with about 51 years of work lost: unlikely. Britain alone leaves about 36%, the Rothschilds alone about 34%. Each is a large dependence on its own; together they come close to deciding the founding.'},
 {id:'case_three', link:2, q:'What if the empire, the bank and the superpower had all stayed out: Britain, the Rothschilds and the United States?',
  claim:'An empire, a bank and a superpower carried it.',
  ids:()=>[...new Set([...VB.groups['British government'],...VB.groups['Rothschild family and houses'],...VB.groups['Without the United States']])].filter(x=>N.get(x)),
  drop:()=>VB.drop['Without the United States']||[],
  what:'The British government, the Rothschild family and houses, and everything American on the map (the government, Congress and parties, the American Zionist organizations, American funders and arms buyers).',
  read:'About 1% on time and 14% at any later date: not possible on this record. With the three removed, what remains of the documented network, the movement, its own funds and the Soviet bloc among them, does not reach a state by 1948.'},
 {id:'case_powers', link:2, q:'What if no great power had backed the movement: no Britain, no United States, no Soviet bloc?',
  claim:'The state was carried by powers as well as by its own people.',
  ids:()=>[...new Set([...VB.groups['British government'],...VB.groups['Without the United States'],...VB.groups['Soviet bloc']])].filter(x=>N.get(x)),
  drop:()=>VB.drop['Without the United States']||[],
  what:'Every great power the map holds as a backer: the British government, everything American, and the Soviet bloc with the Czechoslovak arms. The movement, its funds, its institutions in Palestine and its people stay.',
  read:'About 1% on time and 16% at any later date: not possible on this record. The movement had money, institutions and people of its own, but on this map none of it reaches a state without a great power behind it. The British certificates that let most immigrants in fall with Britain, so the people channel falls too.'},
 {id:'case_people', link:2, q:'What if the powers had backed it, but the immigrants had not come: no waves before 1914, no Mandate certificates, no Fourth or Fifth Aliyah, no clandestine voyages?',
  claim:'Tests the other side of the same link: whether the powers could have carried the founding without the people who came.',
  ids:()=>VCASE_PEOPLE().ids, drop:()=>VCASE_PEOPLE().drop,
  what:'The immigration of 1881 to 1914, every legal immigration certificate issued under the Mandate, the Fourth and Fifth Aliyah, and the clandestine voyages after 1942. Britain, the United States, the Soviet bloc, the Rothschilds and the movement\'s bodies all stay.',
  read:'About 17%, and no later date recovers it: not possible on this record. This result limits the case: the powers could not have founded the state without the people who came. It also shows how most of them came. The Mandate\'s certificates alone account for a fall to about 78%, because Article 6 of the Mandate obliged Britain to facilitate Jewish immigration. The people were needed, and most of them came through a door the empire held open.'},
 {id:'case_shared', link:3, q:'What if the camp that proposed one country for both peoples had been absent: Brit Shalom, Judah Magnes and Martin Buber?',
  claim:'A shared country was proposed and refused.',
  ids:()=>['brit_shalom','magnes','buber'].filter(x=>N.get(x)),
  what:'Brit Shalom (1925) and the two best-known advocates of one country shared by Jews and Arabs, Judah Magnes and Martin Buber.',
  read:'About 92%, almost no change. On this map the shared-country camp was marginal to what built the state: the movement\'s bodies did not act on its proposals, so removing it moves nothing. Magnes\'s one weighted tie is his opposition to American recognition in May 1948, which Truman overrode. The map cannot test the road not taken, a shared state; it shows only that those who proposed it did not carry the founding.'},
 {id:'case_force', link:4, q:'What if the Haganah, the Palmach and the Haganah\'s intelligence service had never existed, and the Irgun and Lehi had?',
  claim:'The state was founded and held by force.',
  ids:()=>['haganah','palmach','shai'].filter(x=>N.get(x)),
  what:'The Haganah, the main Jewish armed force under the Mandate, its strike force the Palmach, and its intelligence service, Shai. The Irgun, Lehi and the arms network stay.',
  read:'About 73%, two years late. Removing the Irgun and Lehi instead leaves about 92%, and removing every armed group and arms channel leaves no chance at all. The founding rested on force, and the main force was the Haganah, the force the movement\'s own leadership commanded, not the two groups Britain classed as terrorist. On the population the map does not measure, see "What if there had been no Plan Dalet and no expulsions?" below.'},
 {id:'case_legitimacy', link:5, q:'What if the founding had drawn no legitimacy from faith or from persecution: no Holy Land to Christians, no survivors\' case, no American Christian and public support, no public campaign and no movement press?',
  claim:'Scripture and persecution served as a shield for the political project.',
  ids:()=>[...new Set(VCASE_SHIELD())].filter(x=>N.get(x)),
  drop:()=>[...vCaseOf('media_campaign','drop'), ...vCaseOf('legit_christian_us','drop')],
  what:'Every part of the legitimacy the map holds: the Christian side of the theology (Darby, Scofield, Blackstone and his memorials, Hechler, the Christian Palestine committees), the survivors\' case (the displaced persons, the Harrison Report and the inquiries that followed), American Christian and public support and the congressional endorsements, the 1947 public campaign, and the movement\'s own press.',
  read:'About 48% on time: unlikely. Each part alone barely moves the figure (88 to 93%); together they halve it. The survivors\' case and American Christian and public support together already bring it to about 68%. The map counts legitimacy only where the record ties it to a decision (the Harrison Report to Truman, the committees to the 1945 congressional resolution, the camps to the UN committee), so this is a floor. It measures what that legitimacy did, not whether it was deserved: the survivors\' suffering was real, and what the case examines is the political use made of faith and of persecution.'},
 {id:'case_us_orgs', link:6, q:'What if the American Zionist organizations had been absent: the Zionist Organization of America, Hadassah, the Emergency Council, the committee that became AIPAC, and the rest?',
  claim:'American money, arms and votes sustain it, and organized lobbying turned them into policy.',
  ids:()=>VB.groups['American Zionist organizations'].filter(x=>N.get(x)),
  what:'The 37 American Zionist organizations on the map, among them the Zionist Organization of America, Hadassah, the American Zionist Emergency Council and the American Zionist Committee for Public Affairs (later AIPAC). The American government stays.',
  read:'About 77% on time, three years late. The organizations mattered, but the American state mattered more: without the American government, with American money and arms still flowing, the chance falls to about 32% (54% ever), and without everything American to about 25%.'},
 {id:'case_us_gov', link:6, q:'What if the American government had stayed out, but Americans had still given money and bought arms?',
  claim:'The American state, not only American donors, carried the founding.',
  ids:()=>VB.groups['US government'].filter(x=>N.get(x)),
  what:'The American government as the map holds it: the presidents, the State and Defense departments, Congress, the parties, the vote and pressure at the UN and the recognition of 14 May 1948. American donors, organizations and arms buyers stay.',
  read:'About 32% on time and 54% at any later date: unlikely. American money and arms without the American state leave a state possible only later; the vote of November 1947 and the recognition in May 1948 were the American state\'s, not its citizens\'.'}
];
let vCaseCache=null;
function vCaseResults(){ if(vCaseCache) return vCaseCache; vCaseCache=VCASE.map(t=>vRunScenario(t,()=>{ const R=vScore(removed); return {t, rd:vRead(R)}; })); return vCaseCache; }
const VCASE_LINK=['','A secular movement chose the Holy Land','An empire, a bank and a superpower carried it','A shared country was proposed and refused','Founded and held by force','Faith and persecution as legitimacy','American money, arms and votes'];
function vCaseList(){ return `<h3 class="vsec">Tests of the case</h3><p class="vtxt">The Case, the last volume of the Israel shelf, argues that the state came from seven links. Each test below takes a link, states what the case says, and removes the part of the record it rests on. Where a result limits the case, it is shown as plainly as where it supports it. The seventh link, that the wars and accords followed from the founding, cannot be tested here: this map stops in 1948.</p><div class="vtlist">${vCaseResults().map((x,i)=>`<button class="vtrow" type="button" data-case="${i}">${vRing(x.rd.on,x.rd.verdict)}<span class="vtq"><span class="vfeat">Link ${x.t.link} · ${esc(VCASE_LINK[x.t.link])}</span><b>${esc(x.t.q)}</b><span style="display:block;font-size:12.5px;line-height:1.35;margin:3px 0 4px;font-style:italic">The case: ${esc(x.t.claim)}</span><small><span class="vtl" style="background:${vLight(x.rd.verdict)[0]}"></span>${esc(x.rd.verdict)} · ${Math.round(x.rd.on)}% on time · ${Math.round(x.rd.ever)}% ever</small></span><span class="vtgo" aria-hidden="true">›</span></button>`).join('')}</div>`; }
vCard.addEventListener('click', e=>{ const b=e.target.closest('[data-case]'); if(!b) return; e.stopPropagation(); vClose(); const t=VCASE[+b.dataset.case]; vRunTest(Object.assign({},t,{what:'The case: '+t.claim+' Removed: '+t.what})); }, true);
"""
anchor = 'const BRK_KIND='
assert s.count(anchor) == 1
s = s.replace(anchor, T + anchor)
a = '  ${vDispList()}\n'
assert s.count(a) == 1, 'tests list anchor'
s = s.replace(a, '  ${vCaseList()}\n' + a)
a = "   ...vDispResults().map((x,i)=>({a:`data-disp=\"${i}\"`,q:x.t.q,on:x.rd.on,ever:x.rd.ever,v:x.rd.verdict,k:'Often denied'})),"
assert s.count(a) == 1, 'rank anchor'
s = s.replace(a, a + "\n   ...vCaseResults().map((x,i)=>({a:`data-case=\"${i}\"`,q:x.t.q,on:x.rd.on,ever:x.rd.ever,v:x.rd.verdict,k:'Test of the case'})),")
# readings moved by a point when the model was restored with the 23-24 Nov verified ties
for a, b in [("read:'About 66%, possible only with great difficulty. The arms came", "read:'About 67%, possible only with great difficulty. The arms came"),
             ("read:'About 13% for 1948 and about 35% ever: unlikely.", "read:'About 14% for 1948 and about 36% ever: unlikely.")]:
    if a in s: s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s)
print('case tests applied:', s.count("{id:'case_"))
