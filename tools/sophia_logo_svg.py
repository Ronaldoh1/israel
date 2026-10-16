"""The Sophia wordmark as inline SVG (replaces the 2.3 MB PNG). Crisp at any size; gold is a gradient, not pixels."""
import math

def logo():
    cx, cy, R = 200, 200, 148          # medallion
    r = 44                             # flower-of-life petal radius
    pts = set()
    for q in range(-8, 9):
        for s in range(-8, 9):
            x = r * (q + s / 2); y = r * s * math.sqrt(3) / 2
            if math.hypot(x, y) <= R + r * 0.2: pts.add((round(cx + x, 2), round(cy + y, 2)))
    flower = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y in sorted(pts))
    studs = ''
    for ang in (0, 90, 180, 270):
        a = math.radians(ang); ox, oy = math.cos(a), math.sin(a)
        x1, y1 = cx + ox * (R + 4), cy + oy * (R + 4); x2, y2 = cx + ox * (R + 30), cy + oy * (R + 30)
        studs += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="url(#sgV)" stroke-width="7" stroke-linecap="round"/>'
                  f'<circle cx="{cx + ox * (R + 16):.1f}" cy="{cy + oy * (R + 16):.1f}" r="8.5" fill="url(#sgR)"/>'
                  f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="11" fill="url(#sgR)"/>')
    return f'''<svg class="hero-logo reveal" viewBox="0 0 1240 410" role="img" aria-label="Sophia — Observe. Collapse. Reignite." xmlns="http://www.w3.org/2000/svg">
<defs>
 <linearGradient id="sgV" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFF1BF"/><stop offset=".28" stop-color="#FFD25E"/><stop offset=".55" stop-color="#E9A72A"/>
  <stop offset=".78" stop-color="#B9771A"/><stop offset="1" stop-color="#F6C35A"/></linearGradient>
 <linearGradient id="sgT" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FFE9A0"/><stop offset=".2" stop-color="#F9C548"/><stop offset=".48" stop-color="#E39C25"/>
  <stop offset=".5" stop-color="#BF7A16"/><stop offset=".78" stop-color="#D99325"/><stop offset="1" stop-color="#F7CE6A"/></linearGradient>
 <radialGradient id="sgR" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#FFF6D6"/><stop offset=".45" stop-color="#F2B640"/><stop offset="1" stop-color="#8E5A12"/></radialGradient>
 <linearGradient id="sgS" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE9A8"/><stop offset=".5" stop-color="#D9952A"/><stop offset="1" stop-color="#FFD873"/></linearGradient>
 <clipPath id="sgClip"><circle cx="{cx}" cy="{cy}" r="{R - 14}"/></clipPath>
 <filter id="sgBevel" x="-5%" y="-5%" width="110%" height="115%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="1.6" result="b"/>
  <feSpecularLighting in="b" surfaceScale="3" specularConstant=".85" specularExponent="22" lighting-color="#FFF6DA" result="s">
   <feDistantLight azimuth="235" elevation="48"/></feSpecularLighting>
  <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
  <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".38" k4="0"/>
 </filter>
 <filter id="sgDrop" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000" flood-opacity=".55"/></filter>
</defs>
<g filter="url(#sgDrop)">
 <g filter="url(#sgBevel)">
  {studs}
  <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="url(#sgV)" stroke-width="9"/>
  <circle cx="{cx}" cy="{cy}" r="{R - 12}" fill="none" stroke="url(#sgV)" stroke-width="3"/>
  <g clip-path="url(#sgClip)" fill="none" stroke="url(#sgS)" stroke-width="3.6">{flower}</g>
  <circle cx="{cx}" cy="{cy}" r="{R - 12}" fill="none" stroke="url(#sgV)" stroke-width="3"/>
  <text x="{cx}" y="{cy + 66}" text-anchor="middle" font-family="'Playfair Display','EB Garamond',Georgia,serif" font-weight="800" font-size="196" fill="#4A2C06" transform="translate(0 5)">&#931;</text>
  <text x="{cx}" y="{cy + 66}" text-anchor="middle" font-family="'Playfair Display','EB Garamond',Georgia,serif" font-weight="800" font-size="196"
        fill="url(#sgT)" stroke="#6E430C" stroke-width="3" paint-order="stroke">&#931;</text>
  <text x="400" y="262" transform="translate(0 6)" fill="#4A2C06" font-family="'Playfair Display','EB Garamond',Georgia,serif" font-weight="800" font-size="236" letter-spacing="-2">Sophia</text>
  <text x="400" y="262" font-family="'Playfair Display','EB Garamond',Georgia,serif" font-weight="800" font-size="236" letter-spacing="-2"
        fill="url(#sgT)" stroke="#6E430C" stroke-width="3" paint-order="stroke">Sophia</text>
 </g>
 <g fill="url(#sgV)">
  <rect x="404" y="337" width="64" height="5" rx="2.5"/><rect x="1132" y="337" width="64" height="5" rx="2.5"/>
  <text x="800" y="352" text-anchor="middle" textLength="640" lengthAdjust="spacingAndGlyphs" font-family="'EB Garamond',Georgia,serif" font-weight="700" font-size="40">OBSERVE  ·  COLLAPSE  ·  REIGNITE</text>
 </g>
</g>
</svg>'''

if __name__ == '__main__':
    print(logo())
