#!/usr/bin/env python3
"""Builds book/src/dream_dashboard.json from scratchpad/ad_series/*.json."""
import json, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SER = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(ROOT, 'book', 'plan', 'dream_series', '*.json'))}
OUT = os.path.join(ROOT, 'book', 'src', 'dream_dashboard.json')

def fmtv(v, how):
    if how == 'T': return '$%.1fT' % v
    if how == 'Tb': return '$%.2fT' % (v / 1000)        # billions -> trillions
    if how == 'B': return '$%dB' % round(v)
    if how == 'Bd': return '$%.2fB' % v
    if how == '$': return '$' + format(round(v), ',')
    if how == '$c': return '$%.2f' % v
    if how == '%': return ('%g' % v) + '%'
    if how == 'x': return ('%g' % v) + '×'
    if how == 'n': return format(round(v), ',')
    return '%g' % v

def clean(c):
    import re
    c = re.sub(r'\s*\((?:keys?|cite)[^)]*\)', '', c)
    c = re.sub(r'\s*Sources?: [a-z0-9_, ]+\.?$', '', c)
    return c.strip()

def line(key, how, title=None, unit=''):
    d = SER[key]
    return {'type': 'line', 'title': title or d['title'], 'unit': unit,
            'cap': clean(d.get('cap', '')), 'data': [[str(x), y, fmtv(y, how)] for x, y in d['data']]}

def pairs(ka, kb, A, B, title, cap, how='', only=None):
    a = dict((x, y) for x, y in SER[ka]['data']); b = dict((x, y) for x, y in SER[kb]['data'])
    yrs = [y for y in a if y in b and (only is None or y in only)]
    mx = max(max(a.values()), max(b.values()))
    return {'type': 'pair', 'a': A, 'b': B, 'max': mx * 1.05, 'title': title, 'cap': cap,
            'data': [[str(y), a[y], b[y], fmtv(a[y], how), fmtv(b[y], how), ''] for y in yrs]}

def has(*k): return all(x in SER for x in k)

def last(key): return SER[key]['data'][-1]
def first(key): return SER[key]['data'][0]

tabs = []
kp = []
if has('ad3_absolute_mobility'):
    f, l = first('ad3_absolute_mobility'), last('ad3_absolute_mobility')
    kp.append(['%g%% → %g%%' % (f[1], l[1]), 'Children earning more than their parents: born %s vs born %s' % (f[0], l[0])])
if has('ad4_productivity_index', 'ad4_pay_index'):
    p, w = last('ad4_productivity_index'), last('ad4_pay_index')
    kp.append(['%d vs %d' % (round(p[1]), round(w[1])), 'Productivity vs typical pay, index 1948 = 100 (%s)' % p[0]])
if has('ad6_price_to_income'):
    f, l = first('ad6_price_to_income'), last('ad6_price_to_income')
    kp.append(['%.1f× → %.1f×' % (f[1], l[1]), 'Typical house price as a multiple of income, %s to %s' % (f[0], l[0])])
if has('ad5_real_minwage'):
    l = last('ad5_real_minwage'); kp.append(['$7.25', 'Federal minimum wage, unchanged since 2009'])
if has('ad8_family_premium'):
    l = last('ad8_family_premium'); kp.append([fmtv(l[1], '$'), 'Average employer family health premium, %s' % l[0]])
if has('ad16_gallup_get_ahead'):
    f, l = first('ad16_gallup_get_ahead'), last('ad16_gallup_get_ahead')
    kp.append(['%g%% → %g%%' % (f[1], l[1]), 'Satisfied with the chance to get ahead by working hard, %s to %s' % (f[0], l[0])])
tabs.append({'name': 'The promise', 'sections': [
    {'type': 'kpis', 'items': kp},
    {'type': 'explain', 'title': 'How to read this dashboard', 'paras': [
        'Each panel is one documented series used in the book. Dollar figures are in the source\'s own real (inflation-adjusted) dollars where it publishes them; where the book adjusts for inflation itself it uses the Census Bureau\'s convention, and the caption says which.',
        'A rising or falling line is a record, not a verdict. The parts of the book linked from each chart explain what drives it, who gains and who pays, and where the record is disputed.']}]})

def tab(name, secs):
    secs = [s for s in secs if s]
    if secs: tabs.append({'name': name, 'sections': secs})

def L(key, how, **kw): return line(key, how, **kw) if key in SER else None

tab('Mobility and income', [L('ad3_absolute_mobility', '%', unit='%'), L('ad2_real_median_household_income', '$', unit='$'),
                            L('ad16_gallup_get_ahead', '%', unit='%')])
tab('Work and wages', [
    pairs('ad4_productivity_index', 'ad4_pay_index', 'Productivity', 'Typical pay', 'Productivity and typical pay, index 1948 = 100', SER['ad4_pay_index'].get('cap', '').replace(' Plot with ad4_productivity_index.', '').rstrip() + ' Productivity is EPI\'s net productivity of the total economy, same base.', 'n') if has('ad4_productivity_index', 'ad4_pay_index') else None,
    L('ad5_real_minwage', '$c', unit='$'), L('ad4_union_private', '%', unit='%'), L('ad4_major_stoppages', 'n'), L('ad4_ceo_ratio', 'x')])
tab('Housing', [L('ad6_price_to_income', 'x'), L('ad6_homeownership', '%', unit='%'),
                pairs('ad13_homeownership_white', 'ad13_homeownership_black', 'White (non-Hispanic)', 'Black', 'Homeownership, white and Black households (%)', SER['ad13_homeownership_black'].get('cap', ''), '%') if has('ad13_homeownership_white', 'ad13_homeownership_black') else None])
tab('Education', [L('ad7_public4yr_tuition', '$', unit='$'), L('ad7_pell_share', '%', unit='%'), L('ad7_student_debt_total', 'Tb')])
tab('Health', [L('ad8_health_spending_per_person', '$', unit='$'), L('ad8_family_premium', '$', unit='$')])
tab('Debt', [L('ad9_household_debt', 'T'), L('ad9_credit_card_balances', 'Tb'), L('ad9_card_apr', '%', unit='%')])
tab('Retirement', [L('ad10_db_share_1975_2004', '%', unit='%'), L('ad10_db_share_2004_2023', '%', unit='%'), L('ad10_poverty_65plus', '%', unit='%')])
tab('Wealth', [pairs('ad12_top1_networth_share', 'ad12_bottom50_networth_share', 'Top 1%', 'Bottom 50%', 'Share of all household net worth: the top 1% and the bottom half (%)', SER['ad12_top1_networth_share'].get('cap', '').split('; vintage')[0] + '. Selected years.', '%', only=[1989, 2000, 2007, 2010, 2019, 2026]) if has('ad12_top1_networth_share', 'ad12_bottom50_networth_share') else None, L('ad12_top1_financial_share', '%', unit='%'), L('ad12_white_black_ratio', 'x')])
if has('ad11_fedrate_lowest', 'ad11_fedrate_middle', 'ad11_fedrate_highest', 'ad11_fedrate_top1'):
    ks = ['ad11_fedrate_lowest', 'ad11_fedrate_middle', 'ad11_fedrate_highest', 'ad11_fedrate_top1']
    yrs = [x for x, _ in SER[ks[0]]['data']]
    fy, ly = yrs[0], yrs[-1]
    hb = {'type': 'pair', 'a': str(fy), 'b': str(ly), 'max': 40, 'title': 'Average federal tax rate by income group, %s and %s (%%)' % (fy, ly),
          'cap': SER[ks[0]].get('cap', ''), 'data': []}
    for k, nm in zip(ks, ['Lowest fifth', 'Middle fifth', 'Highest fifth', 'Top 1%']):
        dd = dict(SER[k]['data']); hb['data'].append([nm, dd[fy], dd[ly], '%g%%' % dd[fy], '%g%%' % dd[ly], ''])
    taxes = hb
else: taxes = None
tab('Taxes and rules', [taxes, L('ad15_lobbying_total', 'Bd'), L('ad15_finance_profit_share', '%', unit='%')])
tab('The trap', [L('ad14_spm_poverty', '%', unit='%'), L('ad14_incarceration_rate', 'n'), L('ad16_overdose_deaths', 'n')])

D = {'title': 'The American Dream in Numbers',
     'sub': 'The documented series behind The American Dream Architecture: mobility, wages, housing, schooling, health, debt, retirement, wealth, taxes and the poverty trap, each with its source in the caption.',
     'scenes': [], 'tabs': tabs}
json.dump(D, open(OUT, 'w'), ensure_ascii=False, indent=1)
print('tabs', [(t['name'], len(t['sections'])) for t in tabs])
