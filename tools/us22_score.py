"""Part 22 scorecard engine. Goalpost scoring (HDI-style): score = 10*(v-floor)/(goal-floor), clipped 0..10.
Each indicator: (domain, id, label, unit, US, IL_citizens, IL_governed or None(=same), floor, goal, part, cites)
None value -> unscored for that side (row shown, excluded)."""
import json, sys
P = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
def g(k, d=None): return P.get(k, d)

I = []
def add(dom, iid, label, us, il, ilg, floor, goal, part, cites, note=''):
    I.append(dict(dom=dom, id=iid, label=label, us=us, il=il, ilg=il if ilg == 'same' else ilg, floor=floor, goal=goal, part=part, cites=cites, note=note))

S = 'same'
# --- Citizen services ---
add('Health', 'uninsured', 'People without health coverage, % of residents (2025)', 7.9, 0.0, S, 20, 0, 'us16_systems', ['us16_census_2025', 'us16_wiki_ilhealth'], 'Israel: universal for citizens and permanent residents; asylum seekers and foreign workers excluded')
add('Health', 'life', 'Life expectancy at birth, years (2024)', 78.9, 83.2, S, 75, 85, 'us16_outcomes', ['us16_wb_le'])
add('Health', 'infant', 'Infant deaths per 1,000 births (2024)', 5.5, 2.7, S, 8, 1.5, 'us16_outcomes', ['us16_wb_imr'])
add('Health', 'hale', 'Healthy life expectancy at birth, years (WHO, 2021)', 63.2, 70.9, S, 60, 75, 'us16_outcomes', ['us22_who_hale21'])
#add('Health', 'hcost', 'Health spending, % of GDP (2023); lower is cheaper', 16.7, 7.1, S, 18, 6, 'us16_cost', ['us16_wb_chegdp'])
add('Work and wages', 'wage', 'Average annual wage, 2024 USD PPP', 82933, 54736, S, 25000, 85000, 'us14_wages', ['us14_oecd_avwage'])
add('Work and wages', 'wagegrowth', 'Real average-wage growth 2000–2024, %', 27.7, 10.9, S, 0, 40, 'us14_wages', ['us14_oecd_avwage'])
add('Work and wages', 'hours', 'Hours worked a year per worker (2025); fewer is better', 1800, 1870, S, 2200, 1350, 'us13_wages', ['us13_wiki_hours'])
add('Work and wages', 'vacation', 'Paid vacation days guaranteed by national law', 0, 12, S, 0, 25, 'us13_wages', ['us13_dol_vacation', 'us13_toi_vacation'])
#add('Work and wages', 'minwage', 'National minimum wage as share of median full-time wage', g('mw_us'), g('mw_il'), S, 0.2, 0.6, 'us13_wages', g('mw_cites', []))
add('Work and wages', 'union', 'Collective-agreement coverage, % of employees', 11.2, 25, S, 0, 80, 'us13_unions', ['us13_bls_union2025', 'us13_oecd_cb_israel'], 'Israel: midpoint of the OECD range of 20–30%')
add('Household debt and prices', 'hhdebt', 'Household debt, % of GDP (2024)', 69.2, 42.3, S, 100, 20, 'us14_basket', ['us14_globes_mortgagegdp'])
add('Household debt and prices', 'infl', 'Inflation, distance from a 2% target, points (year to Sept 2026)', 1.7, 0.4, S, 6, 0, 'us14_basket', ['us14_bls_cpi_sep26', 'us14_te_cpi_sep26'])
add('Household debt and prices', 'tuition', 'Published public-university tuition, USD a year (2025–26)', 11950, 3300, S, 15000, 0, 'us17_higher', ['us14_cb_trends2025', 'us14_huji_tuition'], 'Israel: NIS 12,017 at about NIS 3.65 to the dollar; US net price after aid about $2,300')
add('Housing', 'homeless', 'Homelessness per 100,000 (US one-night count 2025; Israel 2020 service counts plus untreated street dwellers)', 218, 46, S, 300, 0, 'us15_housing', ['us15_hud_pit2025', 'us15_ynet_homeless2022'], 'Not strictly comparable; Israel scored on its highest available count')
add('Education', 'pisa', 'PISA reading score, 15-year-olds (2025)', 490, 436, S, 400, 550, 'us17_schools', ['us17_edweek_pisa2025', 'us17_ih_pisa2025'])
add('Family and safety net', 'leave', 'Weeks of paid leave after a birth, by national law', 0, 15, S, 0, 26, 'us18_family', ['us18_crs_leave', 'us18_nii_maternity2018'])
add('Family and safety net', 'famspend', 'Public spending on families, % of GDP (2023)', 0.60, 1.89, S, 0, 3.5, 'us18_family', ['us18_socx_usa', 'us18_socx_isr'])
add('Family and safety net', 'unemp', 'Unemployment benefit, share of previous net income replaced in the first months (OECD, 2025; single person on 67% of the average wage)', 55, 65, S, 20, 90, 'us13_wages', ['us22_oecd_nrr_usa67', 'us22_oecd_nrr_isr67'])
add('Family and safety net', 'oldpov', 'Old-age poverty, people 66 and over below half the median, % (OECD; US 2023, Israel 2022)', 22.9, 15.3, S, 35, 3, 'us18_safetynet', ['us22_oecd_idd_usa66', 'us22_oecd_idd_isr66'])
add('Family and safety net', 'poverty', 'Relative poverty, % below half the median (OECD)', 18.0, 19.5, S, 25, 5, 'us18_poverty', ['us22_statista_oecdpov', 'us18_nii_pov2023'])
add('Family and safety net', 'childpov', 'Child poverty, % below half the median (OECD)', None, 23.4, S, 30, 5, 'us18_poverty', ['us18_nii_pov2023'])
add('Public safety', 'homicide', 'Homicide victims per 100,000 (US 2025; Israel 2023)', 4.1, 3.04, S, 10, 0.5, 'us5_homicide', ['us5_fox_fbi2025', 'us5_taub_homicide'])
add('Public safety', 'gundeaths', 'Firearm deaths per 100,000, all intents (US 2024)', 12.8, None, S, 15, 0, 'us5_guns', ['us5_pew_gundeaths'])
add('Wellbeing', 'happy', 'World Happiness Report life evaluation, 0–10 (2026)', 6.816, 7.187, S, 4, 8, 'us22_method', ['us22_whr26_hli', 'us22_fox5_whr26'])
add('Family budget and security', 'oop', 'Out-of-pocket health spending per person, USD PPP (2023; book arithmetic: out-of-pocket share × spending per person)', 1469, 827, S, 2000, 0, 'us16_cost', ['us16_wb_oop', 'us16_wb_chepc'])
add('Family budget and security', 'food', 'Food as a share of household spending, % (US 2024; Israel 2023); lower leaves more', 12.9, 17.9, S, 25, 5, 'us14_basket', ['us22_bls_ce24_food', 'us22_cbs_hes23_food'])
add('Family budget and security', 'housingshare', 'Housing as a share of household spending, % (OECD, latest)', 16.5, 21.1, S, 30, 10, 'us14_housing', ['us22_oecd_hpt_usa', 'us22_oecd_hpt_isr'])
add('Family budget and security', 'rentburden', 'Low-income renters spending over 40% of income on rent, % (OECD, latest)', 48.3, 54.1, S, 70, 10, 'us14_housing', ['us22_oecd_hpt_usa', 'us22_oecd_hpt_isr', 'us22_oecd_hc12'], 'US measured on gross income')
add('Family budget and security', 'taxwedge', 'Taxes on a low-wage worker: income tax and social contributions, % of labour costs (OECD tax wedge, single worker on 67% of the average wage, 2025)', 27.5, 19.4, S, 45, 10, 'us11_fiscal', ['us22_oecd_tw26_ch3'], 'Excludes consumption taxes: Israel VAT 18%, US average state and local sales tax 7.53%')
add('Family budget and security', 'sick', 'Paid sick days a year guaranteed by national law', 0, 18, S, 0, 20, 'us13_wages', ['us22_dol_sick', 'us22_kolzchut_sick'], 'US: 81% of private workers get paid sick leave from employers (2026)')
add('Family budget and security', 'pension', 'Retirement contribution required by law, % of wages (employer + employee, including severance)', 0, 18.5, S, 0, 20, 'us18_safetynet', ['us22_bls_ebs26', 'us22_boi_dp202508'], 'US: 52% of private workers participate in an employer plan (2026)')
# --- Liberty and coercion ---
add('Liberty and coercion', 'fh', 'Freedom House total score, 0–100 (2026)', 81, 73, 53.1, 0, 100, 'us3_elections', ['us3_fh_us2026', 'us3_fh_il2026'] + ['us1_fh_israel2026', 'us9_pcbs_2025'], 'Everyone-governed Israel: population-weighted with the West Bank and Gaza scores')
add('Liberty and coercion', 'rsf', 'Press-freedom rank of 180 (RSF 2026)', 64, 116, S, 180, 1, 'us3_speech', ['us3_wboc_rsf', 'us3_rsf_il'])
add('Liberty and coercion', 'cpi', 'Corruption Perceptions Index, 0–100 (2025)', 64, 62, S, 20, 90, 'us2_integrity', ['us2_wiki_cpi'])
add('Liberty and coercion', 'prison', 'People imprisoned per 100,000 (2023; everyone-governed Israel: its 19,756 prisoners over the 15.5m people it governs)', 542, 217, 127, 600, 50, 'us4_prisons', ['us4_wpb_us', 'us4_wpb_il'], 'Israel includes Palestinian security prisoners')
add('Liberty and coercion', 'nocharge', 'Held without criminal charge per 100,000 governed (US: ICE civil detention + Guantanamo; Israel: administrative and "unlawful combatant" detainees)', 20.0, None, 29.2, 50, 0, 'us4_detention', ['us4_trac_ice', 'us4_amnesty_gtmo', 'us4_hamoked_charts'], 'Israel\'s detainees are almost all Palestinians from the territories, so scored only in the everyone-governed view')
add('Liberty and coercion', 'exec', 'Executions per 10 million (2025)', 1.37, 0.0, S, 3, 0, 'us4_prisons', ['us4_dpic_2025'])
add('Liberty and coercion', 'religion', 'Government restrictions on religion, Pew index 0–10 (2022)', 2.7, 6.7, S, 10, 0, 'us7_us', ['us7_pew_gri2022'])
add('Liberty and coercion', 'novote', 'Share of people governed who cannot vote for the governing state, %', 1.1, None, 35.9, 50, 0, 'us9_us', ['us9_crs_territories', 'us9_pcbs_2025'], 'US: territory residents; Israel: Palestinians of the West Bank and Gaza, scored only in the everyone-governed view')
# --- Economy and public finances ---
add('Economy and public finances', 'gdppc', 'GDP per person, constant 2015 USD (2025)', 67946, 42596, S, 20000, 80000, 'us11_growth', ['us11_wb_gdppc_const'])
add('Economy and public finances', 'growth', 'Growth of GDP per person, % a year since 1980', 1.75, 1.86, S, 0, 3, 'us11_growth', ['us11_wb_gdppc_const'])
add('Economy and public finances', 'pubdebt', 'Public debt, % of GDP (2025; US federal debt held by the public, Israel general government gross)', 99, 67.9, S, 150, 30, 'us11_fiscal', ['us11_cbo_outlook2026', 'us11_imf_debt'], 'Definitions differ; the US measure is the narrower one, so a like-for-like gross figure would score the US lower still')
#add('Economy and public finances', 'rd', 'Research and development, % of GDP (2023)', 3.45, 6.35, S, 0, 6, 'us12_tech', ['us12_im_rd_usa', 'us12_im_rd_isr'])
add('Equity inside each system', 'gender', 'WEF Global Gender Gap Index, 0–1 (2025)', 0.756, 0.709, S, 0.6, 0.9, 'us8_gender', ['us8_wiki_ggg'])
add('Equity inside each system', 'infratio', 'Infant-mortality ratio, most-affected group to majority (US Black:white 2023; Israel Arab:Jewish 2022)', 2.44, 2.43, S, 3, 1, 'us16_outcomes', ['us16_cdc_imr2023', 'us16_toi_moh_gaps'])

SERV = ['Health', 'Work and wages', 'Household debt and prices', 'Housing', 'Education', 'Family and safety net', 'Public safety', 'Wellbeing', 'Family budget and security']
DOMS = SERV + ['Liberty and coercion', 'Economy and public finances', 'Equity inside each system']

def sc(v, f, gl):
    if v is None: return None
    s = 10 * (v - f) / (gl - f)
    return round(max(0, min(10, s)), 2)
for x in I:
    x['s_us'] = sc(x['us'], x['floor'], x['goal']); x['s_il'] = sc(x['il'], x['floor'], x['goal']); x['s_ilg'] = sc(x['ilg'], x['floor'], x['goal'])
    if x['s_us'] is None or (x['s_il'] is None and x['s_ilg'] is None): x['scored'] = False
    else: x['scored'] = True
def dom(d, key):
    v = [x[key] for x in I if x['dom'] == d and x['scored'] and x[key] is not None and x['s_us'] is not None]
    if key != 's_us':
        v = [x[key] for x in I if x['dom'] == d and x[key] is not None and x['s_us'] is not None]
    else:
        pass
    return round(sum(v) / len(v), 2) if v else None
def domscore(d, key):
    # pair-consistent: for country-side key use rows where both US and that side scored
    rows = [x for x in I if x['dom'] == d and x['s_us'] is not None and x[key] is not None]
    return round(sum(x[key] for x in rows) / len(rows), 2) if rows else None
def domscore_us(d, side):
    rows = [x for x in I if x['dom'] == d and x['s_us'] is not None and x[side] is not None]
    return round(sum(x['s_us'] for x in rows) / len(rows), 2) if rows else None
out = {'rows': I, 'domains': {}}
for d in DOMS:
    out['domains'][d] = dict(us_c=domscore_us(d, 's_il'), il=domscore(d, 's_il'), us_g=domscore_us(d, 's_ilg'), ilg=domscore(d, 's_ilg'))
def comp(ds, us_key, il_key, w=None):
    w = w or {d: 1 for d in ds}
    a = [(out['domains'][d][us_key], out['domains'][d][il_key], w[d]) for d in ds if out['domains'][d][il_key] is not None]
    W = sum(z[2] for z in a)
    return round(sum(z[0] * z[2] for z in a) / W, 2), round(sum(z[1] * z[2] for z in a) / W, 2)
C = {}
C['services'] = comp(SERV, 'us_c', 'il')
C['liberty_cit'] = comp(['Liberty and coercion'], 'us_c', 'il')
C['liberty_gov'] = comp(['Liberty and coercion'], 'us_g', 'ilg')
C['economy'] = comp(['Economy and public finances'], 'us_c', 'il')
C['equity'] = comp(['Equity inside each system'], 'us_c', 'il')
C['overall_cit'] = comp(DOMS, 'us_c', 'il')
C['overall_gov'] = comp(DOMS, 'us_g', 'ilg')
# sensitivity
C['overall_gov_lib2'] = comp(DOMS, 'us_g', 'ilg', {d: (2 if d == 'Liberty and coercion' else 1) for d in DOMS})
C['overall_cit_lib2'] = comp(DOMS, 'us_c', 'il', {d: (2 if d == 'Liberty and coercion' else 1) for d in DOMS})
# three-pillar: services, liberty, economy equally
def mean(*p): return round(sum(p) / len(p), 2)
C['pillars_cit'] = (mean(C['services'][0], C['liberty_cit'][0], C['economy'][0]), mean(C['services'][1], C['liberty_cit'][1], C['economy'][1]))
C['pillars_gov'] = (mean(C['services'][0], C['liberty_gov'][0], C['economy'][0]), mean(C['services'][1], C['liberty_gov'][1], C['economy'][1]))
# equal indicator weights
def eqind(side):
    rows = [x for x in I if x['s_us'] is not None and x[side] is not None]
    return round(sum(x['s_us'] for x in rows) / len(rows), 2), round(sum(x[side] for x in rows) / len(rows), 2), len(rows)
C['eqind_cit'] = eqind('s_il'); C['eqind_gov'] = eqind('s_ilg')
# head-to-head wins (no goalposts)
def wins(side, doms=DOMS):
    u = i = t = 0
    for x in I:
        if x['dom'] in doms and x['us'] is not None and x[side.replace('s_', '')] is not None:
            a, b = x['s_us'], x[side]
            if abs(a - b) < 0.25: t += 1
            elif a > b: u += 1
            else: i += 1
    return u, i, t
C['wins_cit'] = wins('s_il'); C['wins_gov'] = wins('s_ilg'); C['wins_serv'] = wins('s_il', SERV)
# goalpost sensitivity: widen every goalpost range by 25% each side
def rescore(mod):
    """mod(x)->(floor,goal); returns area-weighted overall for both views"""
    res = {}
    for side, base in [('s_il','il'), ('s_ilg','ilg')]:
        ds_u, ds_i = [], []
        for d in DOMS:
            rows = [x for x in I if x['dom'] == d and x['us'] is not None and x[base] is not None]
            if not rows: continue
            ds_u.append(sum(sc(x['us'], *mod(x)) for x in rows) / len(rows))
            ds_i.append(sum(sc(x[base], *mod(x)) for x in rows) / len(rows))
        res[side] = (round(sum(ds_u)/len(ds_u), 2), round(sum(ds_i)/len(ds_i), 2))
    return res
def widen(k):
    return rescore(lambda x: (x['floor'] - k*(x['goal']-x['floor']), x['goal'] + k*(x['goal']-x['floor'])))
C['widen25'] = widen(0.25)
def libfloor(f):
    rows=[x for x in I if x['dom']=='Liberty and coercion']
    res={}
    for base in ['il','ilg']:
        rr=[x for x in rows if x['us'] is not None and x[base] is not None]
        m=lambda x: (f, 0) if x['id']=='exec' else (x['floor'], x['goal'])
        res[base]=(round(sum(sc(x['us'],*m(x)) for x in rr)/len(rr),2), round(sum(sc(x[base],*m(x)) for x in rr)/len(rr),2))
    return res
C['execfloor5'] = libfloor(5); C['execfloor10'] = libfloor(10)
# fragility: per area, does dropping any one row flip the leader?
FR = {}
for d in DOMS:
    for base in ['il','ilg']:
        rows=[x for x in I if x['dom']==d and x['us'] is not None and x[base] is not None]
        if len(rows) < 2: FR[(d,base)]='single row'; continue
        full = sum(x['s_us'] for x in rows) - sum(x['s_'+base] for x in rows)
        flips=[]
        for r in rows:
            rr=[x for x in rows if x is not r]
            dd=(sum(x['s_us'] for x in rr)-sum(x['s_'+base] for x in rr))/len(rr)
            if (dd>0)!=(full>0) or abs(dd)<0.25: flips.append((r['id'], round(sum(x['s_us'] for x in rr)/len(rr),2), round(sum(x['s_'+base] for x in rr)/len(rr),2)))
        FR[(d,base)]=flips
C['fragility']={f'{k[0]}|{k[1]}':v for k,v in FR.items()}
out['composites'] = C
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else 'out.json', 'w'), indent=1)
for d in DOMS: print(f"{d:32s}", out['domains'][d])
for k, v in C.items(): print(k, v)
for x in I:
    if not x['scored']: print('UNSCORED', x['id'])
# leave-one-out on liberty
print('LOO liberty')
for side in ['s_il','s_ilg']:
    rows=[x for x in I if x['dom']=='Liberty and coercion' and x['s_us'] is not None and x[side] is not None]
    for r in rows:
        rr=[x for x in rows if x is not r]
        print(side, 'drop', r['id'], round(sum(x['s_us'] for x in rr)/len(rr),2), round(sum(x[side] for x in rr)/len(rr),2))
# LOO on overall: drop each area
print('LOO areas overall')
for d in DOMS:
    ds=[z for z in DOMS if z!=d]
    print(d, comp(ds,'us_c','il'), comp(ds,'us_g','ilg'))
