#!/usr/bin/env python3
"""The tally of US government aid to Israel, year by year, in the dollars of each year and in today's dollars.

Inputs (this folder):
  federal_by_year.csv   CRS year table as published by the Jewish Virtual Library, FY1949-FY2025, $ millions
  additions.csv         federal money outside that table: cooperative programs, the April 2024 supplemental's
                        stock replenishment and ammunition, and FY2026 (enacted 3 Feb 2026)
  loans_crs2006.csv     the loans inside the totals, by year (CRS 2006 table); CRS reports none outstanding by Sept 2024
  cpi_u.csv             BLS CPI-U annual averages; cpi_u_monthly_2025_2026.csv for FY2026 and today's index

Method: each fiscal year's dollars are converted with that fiscal year's average CPI-U (a fiscal year runs October
to September, so one quarter of the previous calendar year and three quarters of its own), to October 2026 prices
(CPI-U 337.511, the latest month BLS has published). Writes tally.json and tally.xlsx."""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: list(csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8')))
num = lambda v: float(v) if v not in (None, '') else 0.0

TODAY_LABEL, TODAY = 'October 2026', 337.511
CPI = {int(r['year']): float(r['annual_avg']) for r in rd('cpi_u.csv')}
mon = [float(r['cpi_u_nsa']) for r in rd('cpi_u_monthly_2025_2026.csv') if r['month'] <= '2026-09']
CPI_FY = {y: 0.25 * CPI[y - 1] + 0.75 * CPI[y] for y in range(1949, 2026)}
CPI_FY[2026] = sum(mon) / len(mon)          # Nov 2025-Sep 2026 (BLS collected no October 2025 data)
factor = lambda y: TODAY / CPI_FY[y]

CATS = [('military', 'Military financing (grants and loans)'),
        ('missile_defense_coop', 'Missile defence and defence cooperation'),
        ('war_supplemental', 'Weapons replaced and ammunition (2024 supplemental)'),
        ('economic', 'Economic aid (grants and loans)'),
        ('refugee', 'Refugee and immigrant resettlement'),
        ('asha', 'Schools and hospitals abroad'),
        ('other', 'Other (Export-Import Bank loans, food aid and other programmes)')]
years = {y: {c: 0.0 for c, _ in CATS} for y in range(1949, 2027)}
for r in rd('federal_by_year.csv'):
    y = int(r['year']); Y = years[y]
    Y['military'] += num(r['military']); Y['missile_defense_coop'] += num(r['other_defense'])
    Y['economic'] += num(r['economic']); Y['refugee'] += num(r['refugee']); Y['asha'] += num(r['asha']); Y['other'] += num(r['all_other'])
for r in rd('additions.csv'):
    years[int(r['year'])][r['category']] += float(r['amount_musd'])
loans = {int(r['year']): num(r['mil_loan']) + num(r['econ_loan']) + num(r['other_loans_identified']) for r in rd('loans_crs2006.csv')}

rows, tot = [], {'nominal': 0, 'today': 0, 'loans_nominal': 0, 'loans_today': 0, 'cats_nominal': {c: 0 for c, _ in CATS}, 'cats_today': {c: 0 for c, _ in CATS}}
for y in sorted(years):
    Y = years[y]; n = sum(Y.values()); f = factor(y); L = loans.get(y, 0.0)
    rows.append({'fy': y, 'cpi_fy': round(CPI_FY[y], 3), 'factor': round(f, 4), 'nominal': round(n, 2), 'today': round(n * f, 1),
                 'loans_nominal': L, 'grants_nominal': round(n - L, 2), 'grants_today': round((n - L) * f, 1),
                 'cats': {c: round(Y[c], 2) for c, _ in CATS}, 'cats_today': {c: round(Y[c] * f, 1) for c, _ in CATS}})
    tot['nominal'] += n; tot['today'] += n * f; tot['loans_nominal'] += L; tot['loans_today'] += L * f
    for c, _ in CATS: tot['cats_nominal'][c] += Y[c]; tot['cats_today'][c] += Y[c] * f
tot['grants_nominal'] = tot['nominal'] - tot['loans_nominal']; tot['grants_today'] = tot['today'] - tot['loans_today']

# check against CRS's own inflation-adjusted figure: about $298 billion, 1946-2024, in constant 2024 dollars
crs_check = sum(sum(years[y].values()) * CPI[2024] / CPI_FY[y] for y in range(1949, 2025))
# the table itself, before additions, against its published column totals
# the same total with the GDP price index instead of consumer prices (2025 dollars, the latest annual value)
GD = {int(r['year']): float(r['gdp_deflator_2017_100']) for r in rd('gdp_deflator.csv')}
gd_fy = lambda y: 0.25 * GD[y - 1] + 0.75 * GD[y] if y <= 2025 else GD[2025]
gdp_alt = sum(sum(years[y].values()) * GD[2025] / gd_fy(y) for y in years)
tbl = rd('federal_by_year.csv')
tbl_tot = sum(num(r[c]) for r in tbl for c in ('military', 'other_defense', 'economic', 'refugee', 'asha', 'all_other'))

def today(amount, year):     # a dated figure in calendar-year dollars -> today's
    return amount * TODAY / CPI[year]
SEP = [  # shown beside the total, never added to it
 {'k': 'guarantees', 't': 'Loan guarantees: 1992 programme (available after settlement deductions)', 'nominal': 9226.2, 'year': 1993, 'today': today(9226.2, 1993),
  'note': 'Israel borrowed from private lenders with a US guarantee and paid the fees; no cost to the US unless Israel defaults, which it never has', 'src': 'us20_jvl_loans'},
 {'k': 'guarantees', 't': 'Loan guarantees: 2003 programme (bonds issued)', 'nominal': 4100.0, 'year': 2003, 'today': today(4100.0, 2003),
  'note': 'Authorized $9 billion; about $3.8 billion still available; extended to 2030', 'src': 'us20_jvl_loans'},
 {'k': 'bonds', 't': 'Israel Bonds bought by US states, counties and cities, Oct 2023-Jul 2024', 'nominal': 1700.0, 'year': 2024, 'today': today(1700.0, 2024),
  'note': 'Investments that Israel repays with interest; "more than" $1.7 billion', 'src': 'pm_icij_bonds'},
 {'k': 'ops', 't': 'US military operations in the region, Oct 2023-Sep 2025 (low estimate)', 'nominal': 9650.0, 'year': 2025, 'today': today(9650.0, 2025),
  'note': 'Red Sea and Yemen, defence of Israel against Iran, the June 2025 strikes on Iran; not all of it for Israel; high estimate $12.07 billion', 'src': 'tally_bilmes_2025'},
 {'k': 'ops', 't': 'US interceptors fired defending Israel, Feb-Jun 2026 (estimate)', 'nominal': 5255.0, 'year': 2026, 'today': 5255.0 * TODAY / CPI_FY[2026],
  'note': 'One analyst\'s estimate from Pentagon budget documents and reporting; covers the 2026 war with Iran', 'src': 'tally_semler_interceptors'},
 {'k': 'private', 't': 'American private giving to Israeli organisations, 2007 (one year)', 'nominal': 2059.0, 'year': 2007, 'today': today(2059.0, 2007),
  'note': 'Raised by 774 US charities; tax-deductible; not government money', 'src': 'us20_brandeis_philanthropy'},
 {'k': 'private', 't': 'American private giving to Israel\'s nonprofit sector, 2021 (one year)', 'nominal': 2650.0, 'year': 2021, 'today': today(2650.0, 2021),
  'note': 'More than $2.65 billion from about 1,200 US organisations', 'src': 'us20_ejp_giving2021'},
 {'k': 'pre48', 't': 'Before the state: United Palestine Appeal spending in Palestine, 1946', 'nominal': 52.0, 'year': 1946, 'today': 52.0 * TODAY / 19.5,
  'note': 'Private American money through the United Jewish Appeal; no US government money to the Yishuv has been found', 'src': 'tally_jta_uja1946'},
 {'k': 'pre48', 't': 'United Palestine Appeal share of the 1948 United Jewish Appeal', 'nominal': 74.7, 'year': 1948, 'today': today(74.7, 1948),
  'note': 'Of $150 million raised in 1948', 'src': 'tally_jta_uja1948'},
]
out = {'today_label': TODAY_LABEL, 'today_cpi': TODAY, 'cats': CATS, 'rows': rows,
       'total': {k: (round(v, 1) if not isinstance(v, dict) else {c: round(x, 1) for c, x in v.items()}) for k, v in tot.items()},
       'check': {'crs_2024_dollars_1949_2024': round(crs_check, 1), 'crs_published_2024_dollars': 298000, 'table_total_nominal': round(tbl_tot, 2),
                 'crs_published_nominal_1946_2025': 174965.11, 'gdp_index_2025_dollars': round(gdp_alt, 1),
                 'crs_check_gdp_index_2024': round(sum(sum(years[y].values()) * GD[2024] / gd_fy(y) for y in range(1949, 2025)), 1)},
       'separate': [dict(s, today=round(s['today'], 1)) for s in SEP]}
json.dump(out, open(os.path.join(HERE, 'tally.json'), 'w'), indent=1)

if __name__ == '__main__':
    T = out['total']
    print('FY1949-FY2026: $%.1fB at the time; $%.1fB in %s dollars' % (T['nominal'] / 1e3, T['today'] / 1e3, TODAY_LABEL))
    print('  of which loans (repaid): $%.1fB then, $%.1fB today; grants $%.1fB then, $%.1fB today' % (T['loans_nominal'] / 1e3, T['loans_today'] / 1e3, T['grants_nominal'] / 1e3, T['grants_today'] / 1e3))
    for c, lab in CATS: print('  %-70s %8.1f  %8.1f' % (lab, T['cats_nominal'][c] / 1e3, T['cats_today'][c] / 1e3))
    print('check: 1949-2024 in 2024 dollars = $%.1fB (CRS: about $298B, 1946-2024); table total %.2f (published 176,871.65)' % (crs_check / 1e3, tbl_tot))
    print('GDP price index instead of CPI: $%.1fB in 2025 dollars; 1949-2024 in 2024 dollars $%.1fB' % (gdp_alt / 1e3, out['check']['crs_check_gdp_index_2024'] / 1e3))
    big = sorted(rows, key=lambda r: -r['today'])[:6]
    print('largest years today:', [(r['fy'], round(r['today'] / 1e3, 1)) for r in big])
    for s in out['separate']: print('  sep %-75s %8.0f -> %8.0f' % (s['t'][:75], s['nominal'], s['today']))

# ---------- the dashboard the book's figures draw from, and the download ----------
def fmtB(m): return '$%.1fB' % (m / 1e3)
def build_outputs():
    T = out['total']; R = out['rows']
    peak = max(R, key=lambda r: r['today'])
    cat_lab = dict(CATS)
    dash = {'title': 'US Aid to Israel, Year by Year', 'sub': 'Every fiscal year from 1949 to 2026, in the dollars of the time and in ' + TODAY_LABEL + ' dollars, by kind of aid.',
     'tabs': [
      {'name': 'Totals', 'sections': [
        {'type': 'kpis', 'items': [[fmtB(T['today']), 'All US government aid, FY1949–FY2026, in ' + TODAY_LABEL + ' dollars'],
                                   [fmtB(T['nominal']), 'The same aid in the dollars of each year'],
                                   [fmtB(T['grants_today']), 'Grants only, today\'s dollars (the loans were repaid)'],
                                   [fmtB(T['loans_nominal']), 'Loans inside the total, at the time; none outstanding since 2024'],
                                   ['$' + format(round(peak['today'] / 1e3, 1)) + 'B', 'Largest single year in today\'s dollars: FY%d' % peak['fy']],
                                   [fmtB(sum(r['today'] for r in R if r['fy'] >= 2024)), 'FY2024–FY2026, today\'s dollars']]},
        {'type': 'hbar', 'title': 'By kind of aid, in today\'s dollars', 'cap': 'Billions of ' + TODAY_LABEL + ' dollars, FY1949–FY2026.', 'unit': '$B', 'highlight': 0,
         'data': [[cat_lab[c], round(T['cats_today'][c] / 1e3, 1)] for c, _ in sorted(CATS, key=lambda x: -T['cats_today'][x[0]])]}]},
      {'name': 'By year', 'sections': [
        {'type': 'line', 'title': 'Each year\'s aid, in today\'s dollars', 'cap': 'Billions of ' + TODAY_LABEL + ' dollars, by fiscal year.', 'unit': '$B',
         'data': [[r['fy'], round(r['today'] / 1e3, 1)] for r in R]},
        {'type': 'line', 'title': 'Each year\'s aid, in the dollars of the time', 'cap': 'Billions of dollars as appropriated, by fiscal year.', 'unit': '$B',
         'data': [[r['fy'], round(r['nominal'] / 1e3, 1)] for r in R]},
        {'type': 'table', 'title': 'Every year, converted', 'cap': 'Millions of dollars. "Multiplier" is October 2026 prices divided by the fiscal year\'s average prices (CPI-U).',
         'cols': ['Fiscal year', 'At the time', 'Multiplier', 'Today\'s dollars', 'Of which loans (then)'], 'num': True, 'highlight': 0,
         'rows': [[str(r['fy']), format(round(r['nominal'], 1), ',.1f'), '×%.2f' % r['factor'], format(round(r['today']), ','), format(r['loans_nominal'], ',.1f') if r['loans_nominal'] else '–'] for r in R]
                 + [['Total', format(round(T['nominal'], 1), ',.1f'), '', format(round(T['today']), ','), format(T['loans_nominal'], ',.1f')]]}]},
      {'name': 'By kind', 'sections': [
        {'type': 'stacked', 'title': 'Military and economic aid by decade, today\'s dollars', 'cap': 'Billions of ' + TODAY_LABEL + ' dollars.', 'unit': '$B',
         'series': ['Military financing', 'Missile defence and cooperation', 'Economic aid', 'Everything else'],
         'data': [[('%ds' % d) if 1940 < d < 2020 else ('1949' if d == 1940 else '2020–26'), [round(sum(r['cats_today']['military'] for r in R if d <= r['fy'] < d + 10) / 1e3, 1),
                                    round(sum(r['cats_today']['missile_defense_coop'] + r['cats_today']['war_supplemental'] for r in R if d <= r['fy'] < d + 10) / 1e3, 1),
                                    round(sum(r['cats_today']['economic'] for r in R if d <= r['fy'] < d + 10) / 1e3, 1),
                                    round(sum(r['cats_today']['refugee'] + r['cats_today']['asha'] + r['cats_today']['other'] for r in R if d <= r['fy'] < d + 10) / 1e3, 1)]]
                  for d in range(1940, 2030, 10) if any(d <= r['fy'] < d + 10 for r in R)]}]},
      {'name': 'Beside the total', 'sections': [
        {'type': 'table', 'title': 'Money shown beside the total, not added to it', 'cap': 'Millions of dollars; today\'s dollars use the same CPI-U conversion from the year shown.',
         'cols': ['What', 'Year', 'At the time', 'Today\'s dollars'], 'num': True, 'highlight': 0,
         'rows': [[s['t'], str(s['year']), format(round(s['nominal'], 1), ',.1f'), format(round(s['today']), ',')] for s in out['separate']]},
        {'type': 'note', 'html': 'Loan guarantees and Israel Bonds are borrowing that Israel repays. The costs of US operations are American spending in the region, estimated by independent researchers, and not all of it was for Israel. Private giving is not government money. None is added to the government total.'}]}],
     'sources': [['Congressional Research Service, RL33222, U.S. Foreign Aid to Israel (28 May 2025)', 'https://www.everycrsreport.com/files/2025-05-28_RL33222_5306b5d4e077538d2db80d05cd10ca8c08501669.htm'],
                 ['Jewish Virtual Library, Total U.S. Foreign Aid to Israel (1949–present), from CRS data', 'https://www.jewishvirtuallibrary.org/total-u-s-foreign-aid-to-israel-1949-present'],
                 ['Congressional Research Service, RL33222 (5 January 2006), loans and grants by year', 'https://www.everycrsreport.com/files/20060105_RL33222_da0d42e940692039bff20562bd3c8ab972fc388e.html'],
                 ['W. Hartung, Costs of War and Quincy Institute, U.S. Military Aid and Arms Transfers to Israel (Oct 2025)', 'https://costsofwar.watson.brown.edu/sites/default/files/2025-10/Hartung_US_Military_Aid_to_Israel_Oct.20.pdf'],
                 ['House Appropriations, FY26 National Security, Department of State minibus summary', 'https://appropriations.house.gov/sites/evo-subsites/republicans-appropriations.house.gov/files/evo-media-document/final-fy26-nsrp-minibus-summary.pdf'],
                 ['Senate Appropriations, Congress approves FY2026 defense appropriations bill', 'https://appropriations.senate.gov/news/majority/congress-approves-fy-2026-defense-appropriations-bill'],
                 ['BLS, Consumer Price Index, October 2026 (released 10 Nov 2026)', 'https://www.bls.gov/news.release/archives/cpi_11102026.htm'],
                 ['Federal Reserve Bank of Minneapolis, Consumer Price Index 1913– (BLS annual averages)', 'https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-'],
                 ['FRED, CPI-U not seasonally adjusted (CPIAUCNS)', 'https://fred.stlouisfed.org/data/cpiaucns']]}
    root = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
    json.dump(dash, open(os.path.join(root, 'book', 'src', 'aid_tally_dashboard.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # the download: one CSV and one spreadsheet
    head = ['fiscal_year', 'cpi_u_fy_avg', 'multiplier_to_oct2026'] + [c for c, _ in CATS] + ['total_at_the_time', 'total_oct2026_dollars', 'loans_at_the_time', 'grants_oct2026_dollars']
    with open(os.path.join(HERE, 'aid-tally.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(head)
        for r in R: w.writerow([r['fy'], r['cpi_fy'], r['factor']] + [r['cats'][c] for c, _ in CATS] + [r['nominal'], r['today'], r['loans_nominal'], r['grants_today']])
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    wb = Workbook(); ws = wb.active; ws.title = 'By year'
    ws.append(['US government aid to Israel, FY1949–FY2026, $ millions. Today\'s dollars = ' + TODAY_LABEL + ' prices (CPI-U ' + str(TODAY) + ').'])
    ws.append(['Fiscal year', 'CPI-U (FY average)', 'Multiplier'] + [l for _, l in CATS] + ['Total, at the time', 'Total, today\'s dollars', 'Loans (at the time)', 'Grants, today\'s dollars'])
    for i, r in enumerate(R, start=3):
        ws.append([r['fy'], r['cpi_fy'], None] + [r['cats'][c] for c, _ in CATS] + [None, None, r['loans_nominal'] or None, None])
        ws.cell(i, 3).value = '=%s/B%d' % (TODAY, i)                       # live formulas, so a reader can change the base month
        ws.cell(i, 11).value = '=SUM(D%d:J%d)' % (i, i); ws.cell(i, 12).value = '=K%d*C%d' % (i, i)
        ws.cell(i, 14).value = '=(K%d-IF(M%d="",0,M%d))*C%d' % (i, i, i, i)
    n = len(R) + 2
    ws.append(['Total', None, None] + ['=SUM(%s3:%s%d)' % (col, col, n) for col in 'DEFGHIJKL'] + ['=SUM(M3:M%d)' % n, '=SUM(N3:N%d)' % n])
    for c in ws[2]: c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical='top')
    for c in ws[n + 1]: c.font = Font(bold=True)
    ws.column_dimensions['A'].width = 11
    for col in 'BCDEFGHIJKLMN': ws.column_dimensions[col].width = 15
    for row in ws.iter_rows(min_row=3, max_row=n + 1, min_col=2, max_col=14):
        for c in row: c.number_format = '#,##0.0'
    ws.freeze_panes = 'B3'
    w2 = wb.create_sheet('Beside the total')
    w2.append(['Shown beside the total, never added to it. $ millions.'])
    w2.append(['What', 'Year', 'At the time', 'Today\'s dollars', 'Why it is separate', 'Source key'])
    for s in out['separate']: w2.append([s['t'], s['year'], s['nominal'], round(s['today'], 1), s['note'], s['src']])
    for c in w2[2]: c.font = Font(bold=True)
    w2.column_dimensions['A'].width = 70; w2.column_dimensions['E'].width = 90
    w3 = wb.create_sheet('Method and sources')
    for line in ['Method',
                 'Each fiscal year (October to September) is converted with its own average consumer prices (CPI-U): one quarter of the previous calendar year\'s average and three quarters of its own. FY2026 uses November 2025 to September 2026 (BLS collected no October 2025 data).',
                 'Today\'s dollars are ' + TODAY_LABEL + ' prices: CPI-U ' + str(TODAY) + ' (BLS, released 10 November 2026).',
                 'FY1949–FY2025: the Congressional Research Service year table as published by the Jewish Virtual Library. Its column totals match the published totals to the cent.',
                 'Added: anti-tunnel and counter-drone cooperation FY2020–FY2025 (not in that table\'s defence column); the April 2024 supplemental\'s $4.4 billion to replace US weapons sent to Israel and $801.4 million for ammunition; FY2026 as enacted on 3 February 2026.',
                 'Loans: the loans inside the totals by year come from the CRS table of January 2006. CRS reported in 2025 that Israel no longer owed any sovereign debt to the US government as of September 2024.',
                 'With the GDP price index instead of consumer prices the total is about $%.0f billion in 2025 dollars. CRS gives about $298 billion for 1946–2024 in 2024 dollars; that figure leaves out missile defence funded by the Defense Department and does not state its price index.' % (out['check']['gdp_index_2025_dollars'] / 1e3),
                 '', 'Sources'] + ['%s: %s' % (a, b) for a, b in dash['sources']]:
        w3.append([line])
    w3.column_dimensions['A'].width = 160
    wb.save(os.path.join(HERE, 'aid-tally.xlsx'))
    return dash
if __name__ == '__main__':
    build_outputs(); print('wrote book/src/aid_tally_dashboard.json, aid-tally.csv, aid-tally.xlsx')
