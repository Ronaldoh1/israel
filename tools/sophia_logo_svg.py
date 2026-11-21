"""The Sophia wordmark as inline SVG: pure vector, no filters.

Bevel, extrusion, sheen and glow are drawn with gradients and stacked copies of the same shapes
(filters such as feSpecularLighting or drop-shadow are rendered as bitmaps by browsers, which made
the earlier version look soft). Sharp at any size and pixel density."""
import math

FONT = "'Playfair Display','EB Garamond',Georgia,serif"

def logo():
    cx, cy, R = 200, 200, 148
    r = 44
    pts = set()
    for q in range(-8, 9):
        for s in range(-8, 9):
            x = r * (q + s / 2); y = r * s * math.sqrt(3) / 2
            if math.hypot(x, y) <= R + r * 0.2: pts.add((round(cx + x, 2), round(cy + y, 2)))
    flower = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y in sorted(pts))

    def studs(fill_bar, fill_ball, dy=0):
        out = ''
        for ang in (0, 90, 180, 270):
            a = math.radians(ang); ox, oy = math.cos(a), math.sin(a)
            x1, y1 = cx + ox * (R + 4), cy + oy * (R + 4) + dy; x2, y2 = cx + ox * (R + 30), cy + oy * (R + 30) + dy
            xm, ym = cx + ox * (R + 16), cy + oy * (R + 16) + dy
            out += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{fill_bar}" stroke-width="7" stroke-linecap="round"/>'
                    f'<circle cx="{xm:.1f}" cy="{ym:.1f}" r="8.5" fill="{fill_ball}"/><circle cx="{x2:.1f}" cy="{y2:.1f}" r="11" fill="{fill_ball}"/>')
        return out

    def word(x, y, size, text, extra=''):
        """the same text in five stacked layers: soft shadow, deep extrusion, rim, gold face, top sheen"""
        base = f'x="{x}" y="{y}" font-family="{FONT}" font-weight="800" font-size="{size}" {extra}'
        return (f'<text {base} fill="#000" fill-opacity=".35" transform="translate(0 12)">{text}</text>'
                f'<text {base} fill="#3B2205" transform="translate(0 6)">{text}</text>'
                f'<text {base} fill="#7A4A0E" transform="translate(0 3)">{text}</text>'
                f'<text {base} fill="url(#sgFace)" stroke="#5A3608" stroke-width="2" paint-order="stroke">{text}</text>'
                f'<text {base} fill="url(#sgSheen)">{text}</text>')

    sigma = word(cx, cy + 66, 196, '&#931;', 'text-anchor="middle"')
    sophia = word(400, 262, 236, 'Sophia', 'letter-spacing="-2"')
    return f'''<svg class="hero-logo reveal" viewBox="0 0 1240 410" role="img" aria-label="Sophia — Observe. Collapse. Reignite." xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision" text-rendering="geometricPrecision">
<defs>
 <linearGradient id="sgFace" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFE7A1"/><stop offset=".18" stop-color="#FFD15A"/><stop offset=".45" stop-color="#F1AE30"/>
  <stop offset=".5" stop-color="#D88E1E"/><stop offset=".78" stop-color="#E9A433"/><stop offset="1" stop-color="#FFD873"/></linearGradient>
 <linearGradient id="sgSheen" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset=".32" stop-color="#FFFFFF" stop-opacity=".12"/><stop offset=".46" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
 <linearGradient id="sgRing" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFF0BC"/><stop offset=".3" stop-color="#FFCF55"/><stop offset=".55" stop-color="#E29A24"/>
  <stop offset=".8" stop-color="#B36F14"/><stop offset="1" stop-color="#F5C35A"/></linearGradient>
 <linearGradient id="sgPetal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE59A"/><stop offset=".5" stop-color="#E3A12E"/><stop offset="1" stop-color="#FFD873"/></linearGradient>
 <radialGradient id="sgBall" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#FFF6D6"/><stop offset=".45" stop-color="#F2B640"/><stop offset="1" stop-color="#8E5A12"/></radialGradient>
 <radialGradient id="sgGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#F0B93E" stop-opacity=".22"/><stop offset=".6" stop-color="#F0B93E" stop-opacity=".07"/><stop offset="1" stop-color="#F0B93E" stop-opacity="0"/></radialGradient>
 <clipPath id="sgClip"><circle cx="{cx}" cy="{cy}" r="{R - 14}"/></clipPath>
</defs>
<ellipse cx="640" cy="205" rx="640" ry="230" fill="url(#sgGlow)"/>
<g>
 {studs('#3B2205', '#3B2205', dy=5)}
 <circle cx="{cx}" cy="{cy + 5}" r="{R}" fill="none" stroke="#3B2205" stroke-width="10"/>
 <circle cx="{cx}" cy="{cy}" r="{R}" fill="#0C1633"/>
 {studs('url(#sgRing)', 'url(#sgBall)')}
 <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="url(#sgRing)" stroke-width="9"/>
 <circle cx="{cx}" cy="{cy}" r="{R - 3.5}" fill="none" stroke="#FFF3C8" stroke-opacity=".55" stroke-width="1.2"/>
 <g clip-path="url(#sgClip)" fill="none">
  <g stroke="#3B2205" stroke-opacity=".55" stroke-width="3.6" transform="translate(0 2)">{flower}</g>
  <g stroke="url(#sgPetal)" stroke-width="3.2">{flower}</g>
 </g>
 <circle cx="{cx}" cy="{cy}" r="{R - 12}" fill="none" stroke="url(#sgRing)" stroke-width="3"/>
 {sigma}
 {sophia}
</g>
<g font-family="'EB Garamond',Georgia,serif" font-weight="700" font-size="40">
 <g fill="#3B2205" transform="translate(0 3)">
  <rect x="404" y="337" width="64" height="5" rx="2.5"/><rect x="1132" y="337" width="64" height="5" rx="2.5"/>
  <text x="800" y="352" text-anchor="middle" textLength="640" lengthAdjust="spacingAndGlyphs">OBSERVE  ·  COLLAPSE  ·  REIGNITE</text>
 </g>
 <g fill="url(#sgRing)">
  <rect x="404" y="337" width="64" height="5" rx="2.5"/><rect x="1132" y="337" width="64" height="5" rx="2.5"/>
  <text x="800" y="352" text-anchor="middle" textLength="640" lengthAdjust="spacingAndGlyphs">OBSERVE  ·  COLLAPSE  ·  REIGNITE</text>
 </g>
</g>
</svg>'''

if __name__ == '__main__':
    print(logo())
