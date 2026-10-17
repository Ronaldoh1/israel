/* OTSMatrix: a two-way grid shared by the simulation's dashboards and the library's figures.
   Rows are categories down the side, columns are categories across the top; each cell holds labelled chips.
   Panel data: {type:'matrix', cols:[[label, colour], ...], rowHead, colHead,
                rows:[{label, sub, color, cells:[[chip, ...], [chip, ...]]} or {label, sub, color, span:[chip, ...], spanNote}],
                key:{solid, hollow}, note}
   chip: {n: name, l: detail line, g: 1 for solid (e.g. genetic evidence), 0 for hollow (history only)}
   On narrow screens each row becomes a card and every cell names its column. */
(function(){
  'use strict';
  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function chip(c){ return '<li class="mx-chip' + (c.g ? '' : ' mx-h') + '"><b>' + esc(c.n) + '</b>' + (c.l ? '<small>' + esc(c.l) + '</small>' : '') + '</li>'; }
  function cell(list, col){ return '<div class="mx-cell"><span class="mx-cl" style="--mxc:' + esc(col[1]) + '">' + esc(col[0]) + '</span>' + (list && list.length ? '<ul>' + list.map(chip).join('') + '</ul>' : '<p class="mx-none">None in this group</p>') + '</div>'; }
  function render(s){
    var C = s.cols || [], o = '<div class="mx" role="table" aria-label="' + esc(s.title || 'Grid') + '" style="--mxn:' + C.length + '">';
    o += '<div class="mx-head" role="row"><div class="mx-corner">' + (s.rowHead ? '<span>↓ ' + esc(s.rowHead) + '</span>' : '') + (s.colHead ? '<span>' + esc(s.colHead) + ' →</span>' : '') + '</div>' +
      C.map(function(c){ return '<div class="mx-ch" style="--mxc:' + esc(c[1]) + '">' + esc(c[0]) + '</div>'; }).join('') + '</div>';
    (s.rows || []).forEach(function(r){
      o += '<div class="mx-row" role="row" style="--mxr:' + esc(r.color || '#5A6170') + '"><div class="mx-rh"><b>' + esc(r.label) + '</b>' + (r.sub ? '<small>' + esc(r.sub) + '</small>' : '') + '</div>';
      if(r.span) o += '<div class="mx-cell mx-span">' + (r.spanNote ? '<span class="mx-cl mx-cln">' + esc(r.spanNote) + '</span>' : '') + '<ul>' + r.span.map(chip).join('') + '</ul></div>';
      else C.forEach(function(c, i){ o += cell((r.cells || [])[i], c); });
      o += '</div>';
    });
    o += '</div>';
    if(s.key) o += '<p class="mx-key"><span class="mx-chip mx-k"><b>Solid</b></span> ' + esc(s.key.solid) + ' <span class="mx-chip mx-h mx-k"><b>Outlined</b></span> ' + esc(s.key.hollow) + '</p>';
    if(s.note) o += '<p class="mx-note">' + esc(s.note) + '</p>';
    return '<div class="mx-wrap">' + o + '</div>';
  }
  window.OTSMatrix = {render:render};
})();
