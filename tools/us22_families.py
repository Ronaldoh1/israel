"""Three families: arithmetic from BLS CE 2024 (Table 1101) and CBS HES 2021 (Table 2). Prints all derived figures."""
import json
# --- Israel 2021, quintile = mean of two deciles (each decile holds 10% of households) ---
D = {  # decile: gross, compulsory, net, money exp, mortgage, persons, food, fruitveg, health, edu, transcomm
 1:(4320,223,4097,8108,268,3.79,1738,481,528,670,1113), 2:(7070,350,6720,8049,347,3.26,1909,520,656,464,1037),
 5:(14908,1310,13599,10564,774,3.25,2151,570,784,687,1708), 6:(18046,1992,16054,12024,1005,3.21,2266,588,948,941,2104),
 7:(21618,2813,18805,13229,1180,3.18,2378,591,954,928,2881), 8:(26740,4394,22347,14816,1256,3.20,2405,635,1246,1045,3150)}
def q(a, b): return [ (x + y) / 2 for x, y in zip(D[a], D[b]) ]
IL = {'lower': q(1, 2), 'middle': q(5, 6), 'upper': q(7, 8)}
PPP = 4.28  # NIS per international $, household consumption, World Bank 2020 (latest found)
# --- US 2024 ---
US = {'lower': dict(g=16658, p=1.6, wages=5172, se=299, exp=35046, pip=711, food=5498, health=3445, ins=2153, edu=828, trans=5105, taxratio=None),
      'middle': dict(g=74474, p=2.5, wages=55348, se=3349, exp=66900, pip=6248, food=9097, health=5676, ins=3842, edu=749, trans=11657, taxratio=66606 / 71057),
      'upper': dict(g=121548, p=2.9, wages=100178, se=5867, exp=89972, pip=11934, food=11845, health=7247, ins=4913, edu=1353, trans=15952, taxratio=104559 / 116717)}
out = {}
for k in ['lower', 'middle', 'upper']:
    g, c, n, mx, mort, p, food, fv, hl, ed, tc = IL[k]
    il = dict(gross=g, comp=c, net=n, spend=mx, mort=mort, persons=p,
              comp_pct=100 * c / g, spend_pct=100 * mx / g, mort_pct=100 * mort / g, left_pct=100 * (g - c - mx - mort) / g,
              left_net_pct=100 * (n - mx) / n, left_net_pct_mort=100 * (n - mx - mort) / n,
              food_pct=100 * (food + fv) / g, health_pct=100 * hl / g, edu_pct=100 * ed / g, tc_pct=100 * tc / g,
              net_pp_ppp=n * 12 / p / PPP, left_pp_ppp=(n - mx - mort) * 12 / p / PPP)
    u = US[k]
    itax = (1 - u['taxratio']) * u['g'] if u['taxratio'] else None
    fica = 0.0765 * u['wages'] + 0.153 * u['se']
    sp = u['exp'] - u['pip']
    us = dict(gross=u['g'], persons=u['p'], itax=itax, fica=fica, spend=sp, food_pct=100 * u['food'] / u['g'], health_pct=100 * u['health'] / u['g'],
              ins=u['ins'], edu_pct=100 * u['edu'] / u['g'], trans_pct=100 * u['trans'] / u['g'], spend_pct=100 * sp / u['g'])
    if itax is not None:
        th = u['g'] - itax - fica
        us.update(comp=itax + fica, comp_pct=100 * (itax + fica) / u['g'], takehome=th, left=th - sp, left_pct=100 * (th - sp) / u['g'],
                  left_net_pct=100 * (th - sp) / th, takehome_pp=th / u['p'], left_pp=(th - sp) / u['p'])
    out[k] = dict(il=il, us=us)
json.dump(out, open('/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/us22/families.json', 'w'), indent=1)
for k, v in out.items():
    print('==', k)
    for side in ['il', 'us']:
        print(side, {a: (round(b, 1) if isinstance(b, float) else b) for a, b in v[side].items()})
