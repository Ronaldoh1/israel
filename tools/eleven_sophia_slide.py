"""Add the "Eleven Minutes" slide to Sophia's landing carousel (#showcaseSpotlight). Idempotent.
The slide opens the Israel simulation with parent.__elevenRoute set, so the intro opens immediately.
Usage: python3 tools/eleven_sophia_slide.py [sophia.html]"""
import re, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'sophia.html'
s = open(P, encoding='utf-8').read()
s = re.sub(r'\s*<!--ELEVEN-SLIDE-->.*?<!--/ELEVEN-SLIDE-->', '', s, flags=re.S)
SLIDE = '''
  <!--ELEVEN-SLIDE--><div class="spot-slide" data-target="eleven" style="--spot-color:#FFE14D;--spot-glow:rgba(255,225,77,0.38)">
    <div class="spot-top"><span class="spot-flag">🕕</span><span class="spot-title">Eleven Minutes</span></div>
    <div class="spot-desc">A state at 6:00 p.m., U.S. recognition at 6:11. Eighteen documents show the machine behind it.</div>
    <div class="spot-record"><b>Start here</b> — a four-minute intro to the Israel simulation. Double-tap each document to reveal the record.</div>
  </div><!--/ELEVEN-SLIDE-->'''
anchor = '<div class="spot-slide" data-target="volumes"'
i = s.index(anchor); i = s.rfind('\n', 0, i)
s = s[:i] + SLIDE + s[i:]
# dots: rebuild from slide count
box_start = s.index('id="showcaseSpotlight"')
d0 = s.index('<div class="spot-dots">', box_start); d1 = s.index('</div>', d0)
n = s[box_start:d0].count('class="spot-slide')
dots = ''.join('\n    <span class="spot-dot%s" data-i="%d"></span>' % (' active' if k == 0 else '', k) for k in range(n))
s = s[:d0] + '<div class="spot-dots">' + dots + '\n  ' + s[d1:]
# click handler
a = "    if(target === 'volumes'){"
b = "    if(target === 'eleven'){ window.__elevenRoute = true; if(typeof window.openSimOverlay === 'function') window.openSimOverlay('israel'); return; }\n"
if b not in s:
    assert a in s; s = s.replace(a, b + a, 1)
open(P, 'w', encoding='utf-8').write(s)
print('slides:', n)
