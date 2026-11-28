#!/usr/bin/env python3
"""Replace the old "~$300B" aid KPI on the aid_arms and us_costs_israel dashboards (English and Arabic) with the
library's own year-by-year tally: about $425 billion, FY1949-FY2026, each year converted to October 2026 dollars
(book/plan/aid_tally; the Aid and Arms volume, Part Two). 28 Nov 2026. Idempotent. Usage: python3 tools/patch_aid_kpis.py"""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(P, encoding='utf-8').read(); s0 = s
R = [('["~$300B", "Total US aid to Israel, inflation-adjusted (Council on Foreign Relations estimate)"]',
      '["~$425B", "Total US aid to Israel, FY1949–2026, each year converted to October 2026 dollars (the library\'s tally; CRS: ~$298B in 2024 dollars)"]'),
     ('["~$300B", "Total US aid to Israel since 1948, inflation-adjusted"]',
      '["~$425B", "Total US aid to Israel, FY1949–2026, each year converted to October 2026 dollars"]'),
     ('["~$300B","إجمالي المساعدات الأمريكية لإسرائيل، معدَّلًا وفق التضخم (تقدير مجلس العلاقات الخارجية)"]',
      '["~$425B","إجمالي المساعدات الأمريكية لإسرائيل، 1949–2026، كل سنة محوَّلة إلى دولارات أكتوبر 2026 (حصيلة المكتبة)"]'),
     ('["~$300B","إجمالي المساعدات الأمريكية لإسرائيل منذ 1948، معدّلًا وفق التضخم"]',
      '["~$425B","إجمالي المساعدات الأمريكية لإسرائيل، 1949–2026، كل سنة محوَّلة إلى دولارات أكتوبر 2026"]')]
for a, b in R:
    if a in s: s = s.replace(a, b)
    else: assert b in s, a[:50]
if s != s0: open(P, 'w', encoding='utf-8').write(s); print('aid KPIs updated')
else: print('aid KPIs already current')
