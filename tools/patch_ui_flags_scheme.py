#!/usr/bin/env python3
"""Welcome-screen language flags and colour-scheme protection (index.html). Idempotent.

1. The three language buttons on the welcome screen show the country's flag emoji, large and with no
   circular frame, with the language label underneath: United States (English), El Salvador (Español),
   Palestine (العربية).
2. The page declares its colour scheme (the simulation is dark; the library's paper and sepia pages
   are light), so browsers and in-app web views that auto-darken light pages (Android Chrome's
   auto-dark, TikTok and Instagram web views in dark mode) leave the colours exactly as designed.
Usage: python3 tools/patch_ui_flags_scheme.py [index.html]"""
import re, sys

P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
if '<!--UIFLAGS-->' in s:
    print('flags and colour scheme already applied'); sys.exit(0)

FLAGS = {'en': '\U0001F1FA\U0001F1F8', 'es': '\U0001F1F8\U0001F1FB', 'ar': '\U0001F1F5\U0001F1F8'}
n = 0
for lang, emo in FLAGS.items():
    pat = re.compile(r'(<button class="wl-lang" data-lang="%s"[^>]*>)<span class="wl-flag">.*?</span>(?=\s*<span class="wl-lab")' % lang, re.S)
    s, k = pat.subn(lambda m: m.group(1) + '<span class="wl-flag wl-emoji" aria-hidden="true">' + emo + '</span>', s, count=1)
    n += k
assert n == 3, 'language buttons not found: %d' % n

CSS = ('<style><!--UIFLAGS-->'
       ':root{color-scheme:dark}'
       '.wl-flag.wl-emoji{width:auto !important;height:auto !important;padding:0 !important;border-radius:0 !important;background:none !important;box-shadow:none !important;'
       "font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:62px;line-height:1;letter-spacing:0;filter:drop-shadow(0 4px 10px rgba(0,0,0,.55))}"
       '.wl-flag.wl-emoji::after{display:none !important}'
       '.wl-lang.on .wl-flag.wl-emoji{filter:drop-shadow(0 0 12px rgba(0,255,65,.65)) drop-shadow(0 4px 10px rgba(0,0,0,.55))}'
       '.wl-lang:focus-visible .wl-flag.wl-emoji{outline:3px solid #00FF41;outline-offset:4px}'
       '@media (max-width:420px){.wl-flag.wl-emoji{font-size:54px}}'
       '</style>')
META = '<meta name="color-scheme" content="dark light">'
m = re.search(r'<head[^>]*>', s)
s = s[:m.end()] + META + s[m.end():]
i = s.rfind('</body>')
s = s[:i] + CSS + s[i:]
open(P, 'w', encoding='utf-8').write(s)
print('flags and colour scheme applied')
