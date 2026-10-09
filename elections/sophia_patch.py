"""Idempotent Sophia patcher for the 2026 Elections module.
- refreshes el26_sim_b64 (elections module) and il_sim_b64 (Israel simulation) blobs
- MODULES hash keys, deep link #elections2026-card, window.goElections2026(), pulse CSS
Run: python3 sophia_patch.py [sophia.html] [elections.html] [israel-sim.html]"""
import base64, re, sys
P = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/sophia.html'
EL = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/el26/elections-2026.html'
IL = sys.argv[3] if len(sys.argv) > 3 else '/mnt/user-data/outputs/Israel-simulationv1.0.html'
s = open(P, encoding='utf-8').read()

def set_blob(s, bid, path):
    b64 = base64.b64encode(open(path, 'rb').read()).decode()
    m = re.search(r'(<script type="text/plain" id="%s">)(.*?)(</script>)' % bid, s, re.S)
    assert m, bid
    return s[:m.start(2)] + b64 + s[m.end(2):]
s = set_blob(s, 'el26_sim_b64', EL)
s = set_blob(s, 'il_sim_b64', IL)

def once(s, marker, old, new):
    if marker in s: return s
    assert s.count(old) == 1, (old[:70], s.count(old))
    return s.replace(old, new)

# 1. hash keys
s = once(s, "elections2026:'goToCollapseView'",
  "hamas:'goToHamasSim', iran:'goToIranSim', icc:'goToIccSim' };",
  "hamas:'goToHamasSim', iran:'goToIranSim', icc:'goToIccSim',\n                    elections2026:'goToCollapseView', 'elections2026-card':'goToCollapseView' };")

# 2. openModule branch for the card deep link (lands on Collapse, card pulses)
s = once(s, "key === 'elections2026-card'",
  "    if(key === 'elections2026'){",
  """    if(key === 'elections2026-card'){
      landingView.classList.remove('active');
      rainCanvasEl.style.opacity = '0';
      goToCollapseView();
      setTimeout(()=>{ if(window.pulseElectionsCard) window.pulseElectionsCard(); }, 320);
      setHash('elections2026-card');
      return true;
    }
    if(key === 'elections2026'){""")

# 3. cards carry their id; the elections card glows permanently
s = once(s, "card.dataset.instId = inst.id;",
  "  card.className = 'inst-card' + (inst.disabled ? ' disabled' : '');\n",
  "  card.className = 'inst-card' + (inst.disabled ? ' disabled' : '') + (inst.id === 'elections2026' ? ' el-live' : '');\n  card.dataset.instId = inst.id;\n")

# 4. pulse + cross-module entry point (called from inside the Israel simulation)
s = once(s, "window.goElections2026",
  "  function closeSim(){",
  """  window.pulseElectionsCard = function(){
    const c = document.querySelector('.inst-card[data-inst-id="elections2026"]');
    if(!c) return;
    c.scrollIntoView({block:'center', behavior:'smooth'});
    c.classList.remove('el-pulse'); void c.offsetWidth; c.classList.add('el-pulse');
    setTimeout(()=>c.classList.remove('el-pulse'), 5200);
  };
  window.goElections2026 = function(openModule){
    setTimeout(()=>{
      if(overlay.classList.contains('open')) closeSim();
      try{ landingView.classList.remove('active'); }catch(e){}
      goToCollapseView();
      try{ history.replaceState(null, '', '#elections2026-card'); }catch(e){}
      setTimeout(()=>{ window.pulseElectionsCard(); if(openModule) setTimeout(()=>window.openSimOverlay('elections2026'), 1600); }, 360);
    }, 0);
    return true;
  };
  function closeSim(){""")

# 5. CSS
s = once(s, ".inst-card.el-live",
  ".inst-card{\n",
  """@keyframes elGlow{0%,100%{box-shadow:0 0 0 1px rgba(240,185,62,.55),0 0 18px rgba(240,185,62,.18)}50%{box-shadow:0 0 0 1px rgba(255,216,115,.9),0 0 30px rgba(240,185,62,.38)}}
@keyframes elPulse{0%{box-shadow:0 0 0 0 rgba(255,216,115,.85)}70%{box-shadow:0 0 0 22px rgba(255,216,115,0)}100%{box-shadow:0 0 0 0 rgba(255,216,115,0)}}
.inst-card.el-live{animation:elGlow 3.2s ease-in-out infinite;border-color:rgba(240,185,62,.7)}
.inst-card.el-live:after{content:'LIVE \\00B7  NOV 3';position:absolute;top:14px;left:50%;transform:translateX(-50%);font:800 10px/1 'JetBrains Mono',monospace;letter-spacing:.14em;color:#0a1220;background:#F0B93E;padding:5px 9px;border-radius:999px;z-index:3}
.inst-card.el-pulse{animation:elPulse 1.3s ease-out 4,elGlow 3.2s ease-in-out infinite;transform:scale(1.02)}
@media (prefers-reduced-motion:reduce){.inst-card.el-live,.inst-card.el-pulse{animation:none}}
.inst-card{
""")

# 8. American-flag skin for the elections card
s = once(s, "/*el26-flag*/",
  ".inst-card{\n",
  """/*el26-flag*/.inst-card.el-live>svg{display:none}
.inst-card.el-live{padding-top:calc(52.632% + 22px);background:url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 1900 1000%22%3E%3Crect width=%221900%22 height=%221000%22 fill=%22%23FFFFFF%22/%3E%3Crect y=%220.00%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22153.85%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22307.69%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22461.54%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22615.38%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22769.23%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22923.08%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect width=%22760%22 height=%22538.46%22 fill=%22%233C3B6E%22/%3E%3Cpath fill=%22%23FFFFFF%22 d=%22M63.0,23.2 L69.9,44.5 L92.3,44.5 L74.2,57.6 L81.1,78.9 L63.0,65.8 L44.9,78.9 L51.8,57.6 L33.7,44.5 L56.1,44.5Z M189.0,23.2 L195.9,44.5 L218.3,44.5 L200.2,57.6 L207.1,78.9 L189.0,65.8 L170.9,78.9 L177.8,57.6 L159.7,44.5 L182.1,44.5Z M315.0,23.2 L321.9,44.5 L344.3,44.5 L326.2,57.6 L333.1,78.9 L315.0,65.8 L296.9,78.9 L303.8,57.6 L285.7,44.5 L308.1,44.5Z M441.0,23.2 L447.9,44.5 L470.3,44.5 L452.2,57.6 L459.1,78.9 L441.0,65.8 L422.9,78.9 L429.8,57.6 L411.7,44.5 L434.1,44.5Z M567.0,23.2 L573.9,44.5 L596.3,44.5 L578.2,57.6 L585.1,78.9 L567.0,65.8 L548.9,78.9 L555.8,57.6 L537.7,44.5 L560.1,44.5Z M693.0,23.2 L699.9,44.5 L722.3,44.5 L704.2,57.6 L711.1,78.9 L693.0,65.8 L674.9,78.9 L681.8,57.6 L663.7,44.5 L686.1,44.5Z M126.0,77.2 L132.9,98.5 L155.3,98.5 L137.2,111.6 L144.1,132.9 L126.0,119.8 L107.9,132.9 L114.8,111.6 L96.7,98.5 L119.1,98.5Z M252.0,77.2 L258.9,98.5 L281.3,98.5 L263.2,111.6 L270.1,132.9 L252.0,119.8 L233.9,132.9 L240.8,111.6 L222.7,98.5 L245.1,98.5Z M378.0,77.2 L384.9,98.5 L407.3,98.5 L389.2,111.6 L396.1,132.9 L378.0,119.8 L359.9,132.9 L366.8,111.6 L348.7,98.5 L371.1,98.5Z M504.0,77.2 L510.9,98.5 L533.3,98.5 L515.2,111.6 L522.1,132.9 L504.0,119.8 L485.9,132.9 L492.8,111.6 L474.7,98.5 L497.1,98.5Z M630.0,77.2 L636.9,98.5 L659.3,98.5 L641.2,111.6 L648.1,132.9 L630.0,119.8 L611.9,132.9 L618.8,111.6 L600.7,98.5 L623.1,98.5Z M63.0,131.2 L69.9,152.5 L92.3,152.5 L74.2,165.6 L81.1,186.9 L63.0,173.8 L44.9,186.9 L51.8,165.6 L33.7,152.5 L56.1,152.5Z M189.0,131.2 L195.9,152.5 L218.3,152.5 L200.2,165.6 L207.1,186.9 L189.0,173.8 L170.9,186.9 L177.8,165.6 L159.7,152.5 L182.1,152.5Z M315.0,131.2 L321.9,152.5 L344.3,152.5 L326.2,165.6 L333.1,186.9 L315.0,173.8 L296.9,186.9 L303.8,165.6 L285.7,152.5 L308.1,152.5Z M441.0,131.2 L447.9,152.5 L470.3,152.5 L452.2,165.6 L459.1,186.9 L441.0,173.8 L422.9,186.9 L429.8,165.6 L411.7,152.5 L434.1,152.5Z M567.0,131.2 L573.9,152.5 L596.3,152.5 L578.2,165.6 L585.1,186.9 L567.0,173.8 L548.9,186.9 L555.8,165.6 L537.7,152.5 L560.1,152.5Z M693.0,131.2 L699.9,152.5 L722.3,152.5 L704.2,165.6 L711.1,186.9 L693.0,173.8 L674.9,186.9 L681.8,165.6 L663.7,152.5 L686.1,152.5Z M126.0,185.2 L132.9,206.5 L155.3,206.5 L137.2,219.6 L144.1,240.9 L126.0,227.8 L107.9,240.9 L114.8,219.6 L96.7,206.5 L119.1,206.5Z M252.0,185.2 L258.9,206.5 L281.3,206.5 L263.2,219.6 L270.1,240.9 L252.0,227.8 L233.9,240.9 L240.8,219.6 L222.7,206.5 L245.1,206.5Z M378.0,185.2 L384.9,206.5 L407.3,206.5 L389.2,219.6 L396.1,240.9 L378.0,227.8 L359.9,240.9 L366.8,219.6 L348.7,206.5 L371.1,206.5Z M504.0,185.2 L510.9,206.5 L533.3,206.5 L515.2,219.6 L522.1,240.9 L504.0,227.8 L485.9,240.9 L492.8,219.6 L474.7,206.5 L497.1,206.5Z M630.0,185.2 L636.9,206.5 L659.3,206.5 L641.2,219.6 L648.1,240.9 L630.0,227.8 L611.9,240.9 L618.8,219.6 L600.7,206.5 L623.1,206.5Z M63.0,239.2 L69.9,260.5 L92.3,260.5 L74.2,273.6 L81.1,294.9 L63.0,281.8 L44.9,294.9 L51.8,273.6 L33.7,260.5 L56.1,260.5Z M189.0,239.2 L195.9,260.5 L218.3,260.5 L200.2,273.6 L207.1,294.9 L189.0,281.8 L170.9,294.9 L177.8,273.6 L159.7,260.5 L182.1,260.5Z M315.0,239.2 L321.9,260.5 L344.3,260.5 L326.2,273.6 L333.1,294.9 L315.0,281.8 L296.9,294.9 L303.8,273.6 L285.7,260.5 L308.1,260.5Z M441.0,239.2 L447.9,260.5 L470.3,260.5 L452.2,273.6 L459.1,294.9 L441.0,281.8 L422.9,294.9 L429.8,273.6 L411.7,260.5 L434.1,260.5Z M567.0,239.2 L573.9,260.5 L596.3,260.5 L578.2,273.6 L585.1,294.9 L567.0,281.8 L548.9,294.9 L555.8,273.6 L537.7,260.5 L560.1,260.5Z M693.0,239.2 L699.9,260.5 L722.3,260.5 L704.2,273.6 L711.1,294.9 L693.0,281.8 L674.9,294.9 L681.8,273.6 L663.7,260.5 L686.1,260.5Z M126.0,293.2 L132.9,314.5 L155.3,314.5 L137.2,327.6 L144.1,348.9 L126.0,335.8 L107.9,348.9 L114.8,327.6 L96.7,314.5 L119.1,314.5Z M252.0,293.2 L258.9,314.5 L281.3,314.5 L263.2,327.6 L270.1,348.9 L252.0,335.8 L233.9,348.9 L240.8,327.6 L222.7,314.5 L245.1,314.5Z M378.0,293.2 L384.9,314.5 L407.3,314.5 L389.2,327.6 L396.1,348.9 L378.0,335.8 L359.9,348.9 L366.8,327.6 L348.7,314.5 L371.1,314.5Z M504.0,293.2 L510.9,314.5 L533.3,314.5 L515.2,327.6 L522.1,348.9 L504.0,335.8 L485.9,348.9 L492.8,327.6 L474.7,314.5 L497.1,314.5Z M630.0,293.2 L636.9,314.5 L659.3,314.5 L641.2,327.6 L648.1,348.9 L630.0,335.8 L611.9,348.9 L618.8,327.6 L600.7,314.5 L623.1,314.5Z M63.0,347.2 L69.9,368.5 L92.3,368.5 L74.2,381.6 L81.1,402.9 L63.0,389.8 L44.9,402.9 L51.8,381.6 L33.7,368.5 L56.1,368.5Z M189.0,347.2 L195.9,368.5 L218.3,368.5 L200.2,381.6 L207.1,402.9 L189.0,389.8 L170.9,402.9 L177.8,381.6 L159.7,368.5 L182.1,368.5Z M315.0,347.2 L321.9,368.5 L344.3,368.5 L326.2,381.6 L333.1,402.9 L315.0,389.8 L296.9,402.9 L303.8,381.6 L285.7,368.5 L308.1,368.5Z M441.0,347.2 L447.9,368.5 L470.3,368.5 L452.2,381.6 L459.1,402.9 L441.0,389.8 L422.9,402.9 L429.8,381.6 L411.7,368.5 L434.1,368.5Z M567.0,347.2 L573.9,368.5 L596.3,368.5 L578.2,381.6 L585.1,402.9 L567.0,389.8 L548.9,402.9 L555.8,381.6 L537.7,368.5 L560.1,368.5Z M693.0,347.2 L699.9,368.5 L722.3,368.5 L704.2,381.6 L711.1,402.9 L693.0,389.8 L674.9,402.9 L681.8,381.6 L663.7,368.5 L686.1,368.5Z M126.0,401.2 L132.9,422.5 L155.3,422.5 L137.2,435.6 L144.1,456.9 L126.0,443.8 L107.9,456.9 L114.8,435.6 L96.7,422.5 L119.1,422.5Z M252.0,401.2 L258.9,422.5 L281.3,422.5 L263.2,435.6 L270.1,456.9 L252.0,443.8 L233.9,456.9 L240.8,435.6 L222.7,422.5 L245.1,422.5Z M378.0,401.2 L384.9,422.5 L407.3,422.5 L389.2,435.6 L396.1,456.9 L378.0,443.8 L359.9,456.9 L366.8,435.6 L348.7,422.5 L371.1,422.5Z M504.0,401.2 L510.9,422.5 L533.3,422.5 L515.2,435.6 L522.1,456.9 L504.0,443.8 L485.9,456.9 L492.8,435.6 L474.7,422.5 L497.1,422.5Z M630.0,401.2 L636.9,422.5 L659.3,422.5 L641.2,435.6 L648.1,456.9 L630.0,443.8 L611.9,456.9 L618.8,435.6 L600.7,422.5 L623.1,422.5Z M63.0,455.2 L69.9,476.5 L92.3,476.5 L74.2,489.6 L81.1,510.9 L63.0,497.8 L44.9,510.9 L51.8,489.6 L33.7,476.5 L56.1,476.5Z M189.0,455.2 L195.9,476.5 L218.3,476.5 L200.2,489.6 L207.1,510.9 L189.0,497.8 L170.9,510.9 L177.8,489.6 L159.7,476.5 L182.1,476.5Z M315.0,455.2 L321.9,476.5 L344.3,476.5 L326.2,489.6 L333.1,510.9 L315.0,497.8 L296.9,510.9 L303.8,489.6 L285.7,476.5 L308.1,476.5Z M441.0,455.2 L447.9,476.5 L470.3,476.5 L452.2,489.6 L459.1,510.9 L441.0,497.8 L422.9,510.9 L429.8,489.6 L411.7,476.5 L434.1,476.5Z M567.0,455.2 L573.9,476.5 L596.3,476.5 L578.2,489.6 L585.1,510.9 L567.0,497.8 L548.9,510.9 L555.8,489.6 L537.7,476.5 L560.1,476.5Z M693.0,455.2 L699.9,476.5 L722.3,476.5 L704.2,489.6 L711.1,510.9 L693.0,497.8 L674.9,510.9 L681.8,489.6 L663.7,476.5 L686.1,476.5Z%22/%3E%3C/svg%3E") top left/100% auto no-repeat,linear-gradient(160deg,#16294a,#0d1728)}
.inst-card.el-live:after{top:10px!important;left:auto!important;right:10px;transform:none!important}
.inst-card.el-live>.card-top,.inst-card.el-live>.card-hook,.inst-card.el-live>.card-name,.inst-card.el-live>.card-desc,.inst-card.el-live>.card-foot{position:relative;z-index:1}
.inst-card{\n""")

# 6. card copy (always set to the current description)
EL_DESC = ("Every Senate and House race on the November 3 ballot, state by state. Each candidate gets a page that opens with a 60-second brief: "
  "who they are, what they claim versus what the record shows, what they said versus how they voted, their documented record on Israel, "
  "and every dollar in the FEC filings \\u2014 small donors, PACs, self-funding, the outside groups spending for and against them and who funds those groups. "
  "Every candidate is scored 1\\u20135 on a published six-part rubric: taking corporate or AIPAC money lowers the score at any amount, and sitting members are scored on how they actually voted. Includes a side-by-side race comparison, a financial dashboard and the Thomas Massie case study. "
  "35 Senate races, 435 House seats and 36 governor races mapped, with sitting members\\u2019 votes checked against a published key-vote list; research fills in state by state.")
s = re.sub(r"(\{id:'elections2026', name:'2026 Elections'.*?desc:')(.*?)(',\n)", lambda m: m.group(1) + EL_DESC + m.group(3), s, count=1, flags=re.S)

# 7. keep the Israel Simulation card's counts in step with the simulation itself
import json as _j
sim = open(IL, encoding='utf-8').read()
def _blk(bid): return _j.loads(re.search(r'<script[^>]*id="%s"[^>]*>(.*?)</script>' % bid, sim, re.S).group(1))
SC = _blk('scenedata'); DDX = _blk('deepdive-en'); CITX = _blk('citationdata')
n_sc = len(SC); n_ent = sum(len(x['ents']) for x in SC); n_dd = sum(len(v) for v in DDX.values()); n_cit = len(CITX)
n_dash = len(re.findall(r'^\s*"?[a-z0-9_]+"?\s*:\s*\{\s*"?title', sim[sim.index('window.DASHBOARDS'):sim.index('window.DASHBOARDS') + 3000000], re.M)) if False else None
m = re.search(r"(id:'simulation', name:'Israel Simulation'.*?desc:')(\d[\d,]*) scenes(.*?)([\d,]+) mapped entities, ([\d,]+) deep-dive analyses, ([\d,]+) independently-verifiable citations(.*?)(entities:)(\d+)", s, re.S)
if m:
    f = lambda n: '{:,}'.format(n)
    new = (m.group(1) + str(n_sc) + ' scenes' + m.group(3) + f(n_ent) + ' mapped entities, ' + f(n_dd) + ' deep-dive analyses, ' + f(n_cit) + ' independently-verifiable citations' + m.group(7) + m.group(8) + str(n_ent))
    s = s[:m.start()] + new + s[m.end():]
    print('sim card:', n_sc, n_ent, n_dd, n_cit)

# 9. Landing: 2026 Elections carousel below the featured spotlight (flag theme, 4 deep-linking slides)
FLAG = 'url("data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 1900 1000%22%3E%3Crect width=%221900%22 height=%221000%22 fill=%22%23FFFFFF%22/%3E%3Crect y=%220.00%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22153.85%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22307.69%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22461.54%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22615.38%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22769.23%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect y=%22923.08%22 width=%221900%22 height=%2276.92%22 fill=%22%23B22234%22/%3E%3Crect width=%22760%22 height=%22538.46%22 fill=%22%233C3B6E%22/%3E%3Cpath fill=%22%23FFFFFF%22 d=%22M63.0,23.2 L69.9,44.5 L92.3,44.5 L74.2,57.6 L81.1,78.9 L63.0,65.8 L44.9,78.9 L51.8,57.6 L33.7,44.5 L56.1,44.5Z M189.0,23.2 L195.9,44.5 L218.3,44.5 L200.2,57.6 L207.1,78.9 L189.0,65.8 L170.9,78.9 L177.8,57.6 L159.7,44.5 L182.1,44.5Z M315.0,23.2 L321.9,44.5 L344.3,44.5 L326.2,57.6 L333.1,78.9 L315.0,65.8 L296.9,78.9 L303.8,57.6 L285.7,44.5 L308.1,44.5Z M441.0,23.2 L447.9,44.5 L470.3,44.5 L452.2,57.6 L459.1,78.9 L441.0,65.8 L422.9,78.9 L429.8,57.6 L411.7,44.5 L434.1,44.5Z M567.0,23.2 L573.9,44.5 L596.3,44.5 L578.2,57.6 L585.1,78.9 L567.0,65.8 L548.9,78.9 L555.8,57.6 L537.7,44.5 L560.1,44.5Z M693.0,23.2 L699.9,44.5 L722.3,44.5 L704.2,57.6 L711.1,78.9 L693.0,65.8 L674.9,78.9 L681.8,57.6 L663.7,44.5 L686.1,44.5Z M126.0,77.2 L132.9,98.5 L155.3,98.5 L137.2,111.6 L144.1,132.9 L126.0,119.8 L107.9,132.9 L114.8,111.6 L96.7,98.5 L119.1,98.5Z M252.0,77.2 L258.9,98.5 L281.3,98.5 L263.2,111.6 L270.1,132.9 L252.0,119.8 L233.9,132.9 L240.8,111.6 L222.7,98.5 L245.1,98.5Z M378.0,77.2 L384.9,98.5 L407.3,98.5 L389.2,111.6 L396.1,132.9 L378.0,119.8 L359.9,132.9 L366.8,111.6 L348.7,98.5 L371.1,98.5Z M504.0,77.2 L510.9,98.5 L533.3,98.5 L515.2,111.6 L522.1,132.9 L504.0,119.8 L485.9,132.9 L492.8,111.6 L474.7,98.5 L497.1,98.5Z M630.0,77.2 L636.9,98.5 L659.3,98.5 L641.2,111.6 L648.1,132.9 L630.0,119.8 L611.9,132.9 L618.8,111.6 L600.7,98.5 L623.1,98.5Z M63.0,131.2 L69.9,152.5 L92.3,152.5 L74.2,165.6 L81.1,186.9 L63.0,173.8 L44.9,186.9 L51.8,165.6 L33.7,152.5 L56.1,152.5Z M189.0,131.2 L195.9,152.5 L218.3,152.5 L200.2,165.6 L207.1,186.9 L189.0,173.8 L170.9,186.9 L177.8,165.6 L159.7,152.5 L182.1,152.5Z M315.0,131.2 L321.9,152.5 L344.3,152.5 L326.2,165.6 L333.1,186.9 L315.0,173.8 L296.9,186.9 L303.8,165.6 L285.7,152.5 L308.1,152.5Z M441.0,131.2 L447.9,152.5 L470.3,152.5 L452.2,165.6 L459.1,186.9 L441.0,173.8 L422.9,186.9 L429.8,165.6 L411.7,152.5 L434.1,152.5Z M567.0,131.2 L573.9,152.5 L596.3,152.5 L578.2,165.6 L585.1,186.9 L567.0,173.8 L548.9,186.9 L555.8,165.6 L537.7,152.5 L560.1,152.5Z M693.0,131.2 L699.9,152.5 L722.3,152.5 L704.2,165.6 L711.1,186.9 L693.0,173.8 L674.9,186.9 L681.8,165.6 L663.7,152.5 L686.1,152.5Z M126.0,185.2 L132.9,206.5 L155.3,206.5 L137.2,219.6 L144.1,240.9 L126.0,227.8 L107.9,240.9 L114.8,219.6 L96.7,206.5 L119.1,206.5Z M252.0,185.2 L258.9,206.5 L281.3,206.5 L263.2,219.6 L270.1,240.9 L252.0,227.8 L233.9,240.9 L240.8,219.6 L222.7,206.5 L245.1,206.5Z M378.0,185.2 L384.9,206.5 L407.3,206.5 L389.2,219.6 L396.1,240.9 L378.0,227.8 L359.9,240.9 L366.8,219.6 L348.7,206.5 L371.1,206.5Z M504.0,185.2 L510.9,206.5 L533.3,206.5 L515.2,219.6 L522.1,240.9 L504.0,227.8 L485.9,240.9 L492.8,219.6 L474.7,206.5 L497.1,206.5Z M630.0,185.2 L636.9,206.5 L659.3,206.5 L641.2,219.6 L648.1,240.9 L630.0,227.8 L611.9,240.9 L618.8,219.6 L600.7,206.5 L623.1,206.5Z M63.0,239.2 L69.9,260.5 L92.3,260.5 L74.2,273.6 L81.1,294.9 L63.0,281.8 L44.9,294.9 L51.8,273.6 L33.7,260.5 L56.1,260.5Z M189.0,239.2 L195.9,260.5 L218.3,260.5 L200.2,273.6 L207.1,294.9 L189.0,281.8 L170.9,294.9 L177.8,273.6 L159.7,260.5 L182.1,260.5Z M315.0,239.2 L321.9,260.5 L344.3,260.5 L326.2,273.6 L333.1,294.9 L315.0,281.8 L296.9,294.9 L303.8,273.6 L285.7,260.5 L308.1,260.5Z M441.0,239.2 L447.9,260.5 L470.3,260.5 L452.2,273.6 L459.1,294.9 L441.0,281.8 L422.9,294.9 L429.8,273.6 L411.7,260.5 L434.1,260.5Z M567.0,239.2 L573.9,260.5 L596.3,260.5 L578.2,273.6 L585.1,294.9 L567.0,281.8 L548.9,294.9 L555.8,273.6 L537.7,260.5 L560.1,260.5Z M693.0,239.2 L699.9,260.5 L722.3,260.5 L704.2,273.6 L711.1,294.9 L693.0,281.8 L674.9,294.9 L681.8,273.6 L663.7,260.5 L686.1,260.5Z M126.0,293.2 L132.9,314.5 L155.3,314.5 L137.2,327.6 L144.1,348.9 L126.0,335.8 L107.9,348.9 L114.8,327.6 L96.7,314.5 L119.1,314.5Z M252.0,293.2 L258.9,314.5 L281.3,314.5 L263.2,327.6 L270.1,348.9 L252.0,335.8 L233.9,348.9 L240.8,327.6 L222.7,314.5 L245.1,314.5Z M378.0,293.2 L384.9,314.5 L407.3,314.5 L389.2,327.6 L396.1,348.9 L378.0,335.8 L359.9,348.9 L366.8,327.6 L348.7,314.5 L371.1,314.5Z M504.0,293.2 L510.9,314.5 L533.3,314.5 L515.2,327.6 L522.1,348.9 L504.0,335.8 L485.9,348.9 L492.8,327.6 L474.7,314.5 L497.1,314.5Z M630.0,293.2 L636.9,314.5 L659.3,314.5 L641.2,327.6 L648.1,348.9 L630.0,335.8 L611.9,348.9 L618.8,327.6 L600.7,314.5 L623.1,314.5Z M63.0,347.2 L69.9,368.5 L92.3,368.5 L74.2,381.6 L81.1,402.9 L63.0,389.8 L44.9,402.9 L51.8,381.6 L33.7,368.5 L56.1,368.5Z M189.0,347.2 L195.9,368.5 L218.3,368.5 L200.2,381.6 L207.1,402.9 L189.0,389.8 L170.9,402.9 L177.8,381.6 L159.7,368.5 L182.1,368.5Z M315.0,347.2 L321.9,368.5 L344.3,368.5 L326.2,381.6 L333.1,402.9 L315.0,389.8 L296.9,402.9 L303.8,381.6 L285.7,368.5 L308.1,368.5Z M441.0,347.2 L447.9,368.5 L470.3,368.5 L452.2,381.6 L459.1,402.9 L441.0,389.8 L422.9,402.9 L429.8,381.6 L411.7,368.5 L434.1,368.5Z M567.0,347.2 L573.9,368.5 L596.3,368.5 L578.2,381.6 L585.1,402.9 L567.0,389.8 L548.9,402.9 L555.8,381.6 L537.7,368.5 L560.1,368.5Z M693.0,347.2 L699.9,368.5 L722.3,368.5 L704.2,381.6 L711.1,402.9 L693.0,389.8 L674.9,402.9 L681.8,381.6 L663.7,368.5 L686.1,368.5Z M126.0,401.2 L132.9,422.5 L155.3,422.5 L137.2,435.6 L144.1,456.9 L126.0,443.8 L107.9,456.9 L114.8,435.6 L96.7,422.5 L119.1,422.5Z M252.0,401.2 L258.9,422.5 L281.3,422.5 L263.2,435.6 L270.1,456.9 L252.0,443.8 L233.9,456.9 L240.8,435.6 L222.7,422.5 L245.1,422.5Z M378.0,401.2 L384.9,422.5 L407.3,422.5 L389.2,435.6 L396.1,456.9 L378.0,443.8 L359.9,456.9 L366.8,435.6 L348.7,422.5 L371.1,422.5Z M504.0,401.2 L510.9,422.5 L533.3,422.5 L515.2,435.6 L522.1,456.9 L504.0,443.8 L485.9,456.9 L492.8,435.6 L474.7,422.5 L497.1,422.5Z M630.0,401.2 L636.9,422.5 L659.3,422.5 L641.2,435.6 L648.1,456.9 L630.0,443.8 L611.9,456.9 L618.8,435.6 L600.7,422.5 L623.1,422.5Z M63.0,455.2 L69.9,476.5 L92.3,476.5 L74.2,489.6 L81.1,510.9 L63.0,497.8 L44.9,510.9 L51.8,489.6 L33.7,476.5 L56.1,476.5Z M189.0,455.2 L195.9,476.5 L218.3,476.5 L200.2,489.6 L207.1,510.9 L189.0,497.8 L170.9,510.9 L177.8,489.6 L159.7,476.5 L182.1,476.5Z M315.0,455.2 L321.9,476.5 L344.3,476.5 L326.2,489.6 L333.1,510.9 L315.0,497.8 L296.9,510.9 L303.8,489.6 L285.7,476.5 L308.1,476.5Z M441.0,455.2 L447.9,476.5 L470.3,476.5 L452.2,489.6 L459.1,510.9 L441.0,497.8 L422.9,510.9 L429.8,489.6 L411.7,476.5 L434.1,476.5Z M567.0,455.2 L573.9,476.5 L596.3,476.5 L578.2,489.6 L585.1,510.9 L567.0,497.8 L548.9,510.9 L555.8,489.6 L537.7,476.5 L560.1,476.5Z M693.0,455.2 L699.9,476.5 L722.3,476.5 L704.2,489.6 L711.1,510.9 L693.0,497.8 L674.9,510.9 L681.8,489.6 L663.7,476.5 L686.1,476.5Z%22/%3E%3C/svg%3E")'
EL_SPOT = """<style>
.el-spot{position:relative;width:100%;max-width:480px;margin:6px auto 8px;height:168px;border-radius:16px;overflow:hidden;cursor:pointer;
  background:linear-gradient(160deg,#3C3B6E 0%,#262858 58%,#15173c 100%);border:1.5px solid rgba(255,255,255,.28);
  box-shadow:0 4px 30px -10px rgba(178,34,52,.55);opacity:0;transform:translateY(14px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
.el-spot.reveal{opacity:1;transform:none}
.el-spot::before{content:'';position:absolute;top:0;left:0;right:0;height:5px;z-index:2;
  background:linear-gradient(#B22234 0 3px,#FFFFFF 3px 5px)}
.el-spot::after{content:'';position:absolute;right:-30px;bottom:-26px;width:190px;height:100px;opacity:.10;z-index:0;
  background:"""+FLAG+""" center/contain no-repeat;transform:rotate(-8deg);pointer-events:none}
.el-slide{position:absolute;inset:0;padding:16px 18px 14px;display:flex;flex-direction:column;gap:6px;opacity:0;pointer-events:none;transition:opacity .6s var(--ease);z-index:1}
.el-slide.active{opacity:1;pointer-events:auto}
.el-top{display:flex;align-items:center;gap:9px}
.el-flag{width:34px;height:18px;flex-shrink:0;border-radius:2px;box-shadow:0 0 0 1px rgba(255,255,255,.7);background:"""+FLAG+""" center/100% 100% no-repeat}
.el-title{font-family:var(--serif);font-size:17.7px;font-weight:600;color:#FFFFFF;line-height:1.18}
.el-tag{margin-left:auto;font:800 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.12em;color:#FFFFFF;background:#B22234;padding:4px 7px;border-radius:999px;white-space:nowrap}
.el-tag.ok{background:rgba(51,209,122,.16);color:#7FF0AC;border:1px solid rgba(51,209,122,.5)}
.el-tag .gd{display:inline-block;width:7px;height:7px;border-radius:50%;background:#33D17A;margin-right:5px;vertical-align:0;animation:elGd 1.8s ease-out infinite}
@keyframes elGd{0%{box-shadow:0 0 0 0 rgba(51,209,122,.8)}70%{box-shadow:0 0 0 7px rgba(51,209,122,0)}100%{box-shadow:0 0 0 0 rgba(51,209,122,0)}}
.el-desc{font-family:var(--sans);font-size:12.8px;color:rgba(255,255,255,.86);line-height:1.48;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.el-rec{margin-top:auto;font-family:var(--sans);font-size:11.8px;line-height:1.4;color:#FFFFFF;border-top:1px solid rgba(255,255,255,.22);padding-top:6px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.el-rec b{color:#FF8A96;font-weight:800}
.el-dots{position:absolute;bottom:8px;right:14px;display:flex;gap:5px;z-index:3}
.el-dot{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.45);transition:background .3s,transform .3s}
.el-dot.active{background:#FFFFFF;transform:scale(1.35);box-shadow:0 0 0 1.5px #B22234}
@media (max-width:420px){.el-spot{height:184px}.el-title{font-size:16px}}
@media (prefers-reduced-motion:reduce){.el-tag .gd{animation:none}}
</style>
<div class="el-spot reveal" id="elSpotlight" role="button" tabindex="0" aria-label="2026 Elections — tap to open">
  <div class="el-slide active" data-view="home">
    <div class="el-top"><span class="el-flag"></span><span class="el-title">2026 Elections</span><span class="el-tag" id="elDays">NOV 3</span></div>
    <div class="el-desc">Every Senate, House and governor race on the ballot — who funds each candidate: donors, PACs, outside groups and foreign-nation lobbying groups.</div>
    <div class="el-rec"><b>Who are they running for?</b> Follow the money before you vote — every dollar sourced to the filings.</div>
  </div>
  <div class="el-slide" data-view="state" data-arg="AL">
    <div class="el-top"><span class="el-flag"></span><span class="el-title">Alabama</span><span class="el-tag ok"><i class="gd"></i>COMPLETE</span></div>
    <div class="el-desc">18 candidates across 9 races — Senate, governor and all 7 House seats: money, votes, claims checked, legal record, said vs. did.</div>
    <div class="el-rec"><b>The template.</b> Every state gets this same depth — the rest are in progress.</div>
  </div>
  <div class="el-slide" data-view="chamber" data-arg="senate">
    <div class="el-top"><span class="el-flag"></span><span class="el-title">35 Senate Races</span><span class="el-tag">SENATE</span></div>
    <div class="el-desc">Nominee vs. nominee: who is paying for each campaign, and how sitting members actually voted on the bills that hit your wallet.</div>
    <div class="el-rec"><b>Votes vs. money</b> — key votes checked against official roll calls.</div>
  </div>
  <div class="el-slide" data-view="method">
    <div class="el-top"><span class="el-flag"></span><span class="el-title">Scored 1–5, Both Parties</span><span class="el-tag">RUBRIC</span></div>
    <div class="el-desc">Six published parts — preparation, funding independence, votes for people, honesty, conflicts, record. Same formula for every party.</div>
    <div class="el-rec"><b>Nothing unknown counts as clean.</b> A record not yet searched holds the score back.</div>
  </div>
  <div class="el-dots"><span class="el-dot active" data-i="0"></span><span class="el-dot" data-i="1"></span><span class="el-dot" data-i="2"></span><span class="el-dot" data-i="3"></span></div>
</div>
<script>
(function(){
  window.openElectionsAt = function(view, arg){
    window.__el26Route = [view || 'home', arg];
    if(typeof window.openSimOverlay === 'function') window.openSimOverlay('elections2026');
  };
  const box = document.getElementById('elSpotlight'); if(!box) return;
  const slides = [...box.querySelectorAll('.el-slide')], dots = [...box.querySelectorAll('.el-dot')];
  try{ const d = Math.ceil((new Date('2026-11-03T12:00:00') - new Date()) / 864e5); if(d > 0) document.getElementById('elDays').textContent = d + (d === 1 ? ' DAY' : ' DAYS'); }catch(e){}
  let idx = 0, timer = null, sx = null;
  function show(i){ slides[idx].classList.remove('active'); dots[idx].classList.remove('active'); idx = (i + slides.length) % slides.length; slides[idx].classList.add('active'); dots[idx].classList.add('active'); }
  function start(){ if(!timer) timer = setInterval(()=>show(idx + 1), 5200); }
  function stop(){ if(timer){ clearInterval(timer); timer = null; } }
  box.addEventListener('click', ()=>{ const s = slides[idx]; window.openElectionsAt(s.getAttribute('data-view'), s.getAttribute('data-arg') || undefined); });
  box.addEventListener('keydown', ev=>{ if(ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); box.click(); } });
  dots.forEach(d=>d.addEventListener('click', ev=>{ ev.stopPropagation(); show(parseInt(d.getAttribute('data-i'), 10)); stop(); start(); }));
  box.addEventListener('touchstart', ev=>{ sx = ev.touches[0].clientX; }, {passive:true});
  box.addEventListener('touchend', ev=>{ if(sx == null) return; const dx = ev.changedTouches[0].clientX - sx; sx = null;
    if(Math.abs(dx) > 40){ ev.preventDefault(); show(idx + (dx < 0 ? 1 : -1)); stop(); start(); } });
  box.addEventListener('mouseenter', stop); box.addEventListener('mouseleave', start);
  document.addEventListener('visibilitychange', ()=>{ document.hidden ? stop() : start(); });
  start();
})();
</script>
"""
s = once(s, 'id="elSpotlight"', '    <div class="pillars">', EL_SPOT + '    <div class="pillars">')

# 10. "Complete states" slide — rewritten every run from the current list
DONE_SLIDE = ('<div class="el-slide" data-view="chamber" data-arg="house" data-slot="done">\n'
  '    <div class="el-top"><span class="el-flag"></span><span class="el-title">Alabama &amp; Alaska</span><span class="el-tag ok"><i class="gd"></i>COMPLETE</span></div>\n'
  '    <div class="el-desc">30 candidates across 12 races — Senate, governor and House: money, votes, claims checked, legal record, said vs. did.</div>\n'
  '    <div class="el-rec"><b>The template.</b> Every state gets this same depth — the rest are in progress.</div>\n'
  '  </div>')
i = s.index('class="el-tag ok"'); st = s.rindex('<div class="el-slide"', 0, i); en = s.index('</div>\n  </div>', i) + len('</div>\n  </div>')
s = s[:st] + DONE_SLIDE + s[en:]

open(P, 'w', encoding='utf-8').write(s)
print('ok', len(s))
