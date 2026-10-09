/* ===== Rubric v2.1 · STRICT =====
   Same rules for everyone. Unknown is never scored as clean. Every part starts from a neutral 3 (except
   Preparation, which is built from points) and moves only on documented evidence. No caps on deductions. */
var CHECKS = [
  ['money_history', 'Career money history (FEC, pro-Israel trackers, super PAC funders)'],
  ['courts',        'Court records (federal and state dockets)'],
  ['ethics',        'Ethics records (House/Senate Ethics, OCE, state boards)'],
  ['disclosures',   'Personal financial disclosures'],
  ['fara',          'Foreign-agent (FARA) database'],
  ['claims',        'Fixed claim sample checked'],
  ['votes',         'Key-vote roll calls'],
  ['democracy',     'Election-certification votes and statements']
];
function chk(c, k){ return (c.checklist || {})[k] || 'no'; }            // 'done' | 'news' | 'na' | 'no'
function partStatus(c, keys){
  var st = keys.map(function(k){ return chk(c, k); });
  if(st.indexOf('no') > -1) return 'incomplete';
  return st.indexOf('news') > -1 ? 'provisional' : 'final';
}
function sum(a){ return a.reduce(function(t, x){ return t + x; }, 0); }

function scoreFunding(c){
  var f = c.fec; if(!f || !f.receipts || chk(c, 'money_history') === 'no') return null;
  var r = f.receipts, s = f.src || {}, why = [], x = 3, fl = moneyFlags(c), full = chk(c, 'money_history') === 'done';
  if(fl.corp){ x -= 0.75; why.push([-0.75, 'Took or was backed by corporate or industry money (any amount, any cycle): ' + fl.corp.t]); }
  else if(full){ x += 0.75; why.push([0.75, 'No corporate or industry money anywhere in a fully searched career record']); }
  else why.push([0, 'No corporate money found, but the career search is not complete, so no credit is given']);
  if(fl.lobby){ x -= 0.75; why.push([-0.75, 'Took or was backed by foreign-policy lobby money (any amount, any cycle): ' + fl.lobby.t]); }
  else if(full){ x += 0.75; why.push([0.75, 'No foreign-policy lobby money anywhere in a fully searched career record']); }
  else why.push([0, 'No foreign-policy lobby money found, but the career search is not complete, so no credit is given']);
  var org = (s.pac_biz || 0) + (s.pac_ideo || 0) + (s.pac || 0) + (s.earmark || 0) + (s.party || 0), interest = org / r;
  var d1 = Math.floor(interest * 100 / 5) * 0.25;
  if(d1){ x -= d1; } why.push([-d1, 'PAC, party and interest-group-bundled money this cycle: ' + pct(interest) + ' of receipts (−0.25 per 5 points)']);
  var small = (s.small || 0) / r, d2 = small >= 0.5 ? 0.5 : small >= 0.3 ? 0.25 : small < 0.10 ? -0.75 : small < 0.20 ? -0.5 : 0;
  x += d2; why.push([d2, 'Small donors (≤$200): ' + pct(small) + ' of receipts']);
  var sup = 0; ((f.outside || {}).support || []).forEach(function(o){ if(!o[3]) sup += (o[1] || 0); });
  var ratio = sup / r, d3 = ratio >= 1 ? 1 : ratio >= 0.25 ? 0.5 : 0;
  x -= d3; why.push([-d3, 'Outside groups spending to help: ' + money(sup) + ' (' + (Math.round(ratio * 100) / 100) + '× the campaign’s own receipts)']);
  return {s: q4(clamp(x)), why: why, interest: interest, small: small, outside: sup, flags: fl, status: partStatus(c, ['money_history'])};
}

var VERDICT2 = {'true': 0.25, 'partly': -0.25, 'misleading': -0.5, 'false': -1, 'unverifiable': 0, 'opinion': 0};
function scoreHonesty(c){
  if(chk(c, 'claims') === 'no') return null;
  var cl = c.claims || [], x = 3, why = [], pos = 0, rated = 0;
  cl.forEach(function(k){
    var v = k.verdict; if(!(v in VERDICT2)) return;
    if(v !== 'opinion' && v !== 'unverifiable') rated++;
    var d = VERDICT2[v];
    if(v === 'true'){ if(pos >= 2) d = 0; else pos += d; }
    if(v === 'unverifiable' && (k.kind || 'campaign') === 'bio') d = -0.1;          // their own record: the burden of proof is theirs
    if(d){ x += d; why.push([d, (VERDICT[v] ? VERDICT[v].lbl : v) + ': ' + (k.short || k.claim)]); }
    if(k.repeated){ x -= 0.5; why.push([-0.5, 'Said again after being corrected: ' + (k.short || k.claim)]); }
  });
  why.unshift([0, rated + ' checkable claims rated out of ' + cl.length + ' in the fixed sample']);
  if(rated < 5) return {s: null, why: why, rated: rated, status: 'incomplete', nFalse: 0, nMis: 0, nRep: 0, note: 'Fewer than 5 checkable claims — not enough to score'};
  return {s: q4(clamp(x)), why: why, rated: rated, status: partStatus(c, ['claims']),
          nFalse: cl.filter(function(k){ return k.verdict === 'false'; }).length,
          nMis: cl.filter(function(k){ return k.verdict === 'misleading'; }).length,
          nRep: cl.filter(function(k){ return k.repeated; }).length};
}

function scoreConflicts(c){
  var need = ['courts', 'ethics', 'disclosures', 'fara', 'democracy'], st = partStatus(c, need);
  if(st === 'incomplete') return null;
  var items = (c.legal || []).concat(c.foreign || []), x = 5, why = [];
  items.forEach(function(it){ var L = LEGAL[it.kind]; if(!L || !L.d) return; x -= L.d; why.push([-L.d, L.lbl + ': ' + (it.short || it.t)]); });
  var tr = c.finances && c.finances.trades && c.finances.trades.overlap || [];
  tr.forEach(function(t){ x -= 0.25; why.push([-0.25, 'Stock trade in an industry their committee oversees: ' + t.asset + ' (' + t.d + ')']); });
  (c.democracy || []).forEach(function(d){ if(d.kind === 'objected'){ x -= 1; why.push([-1, 'Voted to reject certified election results (' + d.d + ')']); } });
  if(!why.length) why.push([0, 'Nothing found in a completed search of the required records']);
  return {s: q4(clamp(x)), why: why, status: st};
}

function scoreRecord(c){
  var R0 = c.recordx || {}, parts = [], why = [];
  var miss = R0.missed_pct, src = 'official rate';
  if(miss == null && c.votes_kv){ var vs = voteStats(c); if(vs && vs.n){ miss = Math.round(vs.missed / vs.n * 1000) / 10; src = 'key-vote attendance; official rate not yet checked'; } }
  if(miss != null){ var v = miss < 2 ? 5 : miss < 5 ? 4 : miss < 10 ? 3 : miss < 20 ? 2 : 1; parts.push(v); why.push([v, 'Missed votes: ' + miss + '% (' + src + ')']); }
  if(R0.disclosure){ var dv = {'on-time':5, 'extension':5, 'late':3, 'missing':1}[R0.disclosure]; parts.push(dv); why.push([dv, 'Personal financial disclosure: ' + R0.disclosure.replace('-', ' ')]); }
  if(R0.fec){ var fv = {'clean':5, 'notices':4, 'fined':3}[R0.fec]; parts.push(fv); why.push([fv, 'FEC filing record: ' + R0.fec]); }
  if(parts.length < 2) return null;                                       // one item is not a record
  return {s: q4(sum(parts) / parts.length), why: why, status: (R0.missed_pct == null && c.incumbent) ? 'provisional' : 'final'};
}

function scoreVotes(c){
  if(!c.votes_kv) return null;
  var ST = (D.stances && D.stances.stances) || {}, opp = 0, ok = 0, missed = 0, why = [];
  Object.keys(c.votes_kv).forEach(function(id){
    var st = ST[id], k = KVBY[id]; if(!st || !k) return;
    var v = voteNorm(c.votes_kv[id]); opp++;
    if(v === 'yes' || v === 'no'){ var al = v === st.pos; if(al) ok++; why.push([al ? 1 : 0, 1, (al ? 'Sided with households: ' : 'Sided against: ') + k.bill + ' — voted ' + v.toUpperCase() + ' (Sophia position: ' + st.pos.toUpperCase() + ')']); }
    else { missed++; why.push([0, 1, 'Did not vote: ' + k.bill + ' (counted as not standing up)']); }
  });
  if(!opp) return null;
  why.unshift([ok, opp, 'Scored key votes where they sided with Sophia’s published people-first position (missed votes count against)']);
  return {s: q4(clamp(1 + 4 * ok / opp)), why: why, ok: ok, n: opp, status: opp < 8 ? 'provisional' : 'final', note: opp < 8 ? 'Fewer than 8 scored votes' : ''};
}

function scoreCand(c){
  if(c._sc) return c._sc;
  var ax = {prep:scorePrep(c), funding:scoreFunding(c), votes:scoreVotes(c), honesty:scoreHonesty(c), conflicts:scoreConflicts(c), record:scoreRecord(c)};
  Object.keys(ax).forEach(function(k){ if(ax[k] && ax[k].s == null) ax[k] = null; });
  var na = {votes: !votesApplies(c)};
  var used = RUBRIC.axes.filter(function(a){ return !na[a.id]; });
  var done = used.every(function(a){ return ax[a.id]; });
  var W = sum(used.map(function(a){ return a.w; }));
  var overall = done ? q4(sum(used.map(function(a){ return a.w / W * ax[a.id].s; }))) : null;
  var prov = done && used.some(function(a){ return ax[a.id].status && ax[a.id].status !== 'final'; });
  return (c._sc = {ax: ax, overall: overall, done: done, na: na, provisional: prov});
}

function checklistBlock(c){
  var lbl = {done:'Searched directly', news:'Through news reporting only', na:'Does not apply', no:'Not yet searched'};
  return '<div class="recs">' + CHECKS.map(function(k){ var v = chk(c, k[0]);
    return '<div class="rec chk chk-' + v + '"><div class="rec-h"><b>' + esc(k[1]) + '</b><span class="tone ' + ({done:'ok', news:'warn', na:'neutral', no:'bad'}[v]) + '">' + lbl[v] + '</span></div></div>'; }).join('') + '</div>' +
    '<p class="muted" style="margin-top:8px">Every candidate gets this same checklist. A part of the score that depends on a record searched only through news reporting is marked provisional; one that depends on a record not yet searched isn’t scored at all.</p>';
}
