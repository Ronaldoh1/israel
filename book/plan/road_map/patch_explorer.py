"""Write the current network, viability model, other-homelands layer and the breakers search into road-network.html's
DATA line (the rest of the page is left as it is). Run after build_road.py, alt_homeland.py and breakers.py."""
import json, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import viability

GL = {'Rothschild family and houses': 'the Rothschild family', 'Without the United States': 'the United States (government, organizations and money)',
      'British government': 'the British government', 'US government': 'the US government', 'American Zionist organizations': 'the American Zionist organizations',
      'Soviet bloc': 'the Soviet bloc', 'Finance and banks': 'the banks and land and finance companies',
      'The Zionist movement (organizations and leaders)': 'the organized Zionist movement', 'Armed groups and arms network': 'the armed groups and the arms network',
      'Countries that voted for partition': 'the states that voted for partition', 'The United Nations': 'the United Nations', 'France': 'France',
      'Christian Zionism': 'Christian Zionism', 'Religious institutions': 'the religious institutions', 'The Vatican': 'the Vatican'}

def compact_breakers(B, d):
    N = {n['id']: n['name'] for n in d['nodes']}
    def row(kind, label, x, **k):
        dec = [D for D in x['decisions'] if D['chance'] < 50]
        return dict(kind=kind, label=label, V=x['read']['on'], verdict=x['read']['verdict'], ever=x['read']['ever'],
                    weakest=x['weakest'], lost=x['lost_years'], dec=[[D['name'], D['chance']] for D in dec], **k)
    items = []
    for x in B['singles']: items.append(row('single', 'Without ' + x['names'][0], x, ids=x['ids']))
    for x in B['groups']:
        if x['V'] < B['cut']: items.append(row('group', 'Without ' + GL.get(x['group'], x['group']), x, groups=[x['group']]))
    for x in B['group_pairs']:
        items.append(row('groups', 'Without ' + ' and '.join(GL.get(g, g) for g in x['groups']), x, groups=x['groups'], alone=x['alone']))
    for x in B['pairs']: items.append(row('pair', 'Without both ' + ' and '.join(x['names']), x, ids=x['ids'], alone=x['alone']))
    # triples that differ only by one member of the same chain (same result) are shown once, with the alternatives named
    merged = []
    for x in B['triples']:
        hit = None
        for m in merged:
            common = set(m['ids']) & set(x['ids'])
            if len(common) == 2 and abs(m['V'] - x['V']) <= 0.5 and (not m.get('fixed') or set(m['fixed']) == common): hit = m; break
        if hit:
            if not hit.get('fixed'):
                hit['fixed'] = [i for i in hit['ids'] if i in common]; hit['alts'] = [i for i in hit['ids'] if i not in common]
            hit['alts'] += [i for i in x['ids'] if i not in common]; hit['V'] = max(hit['V'], x['V'])
        else: merged.append(dict(x))
    for x in merged:
        if x.get('alts'):
            label = 'Without ' + ' and '.join(N.get(i, i) for i in x['fixed']) + ', plus any one of: ' + ', '.join(N.get(i, i) for i in x['alts'])
            items.append(row('triple', label, x, ids=x['ids'], alts=x['alts'], fixed=x['fixed']))
        else:
            items.append(row('triple', 'Without ' + ', '.join(x['names'][:-1]) + ' and ' + x['names'][-1], x, ids=x['ids'], alone=x['alone']))
    return {'built': B['built'], 'cut': B['cut'], 'baseline': B['baseline'], 'searched': B['searched'], 'pool': B['pool'], 'pool3': B['pool3'], 'items': items}

def main():
    d, M = viability.run()
    M['alt'] = json.load(open(os.path.join(HERE, 'alt_layer.json')))
    bp = os.path.join(HERE, 'breakers.json')
    if os.path.exists(bp): M['breakers'] = compact_breakers(json.load(open(bp)), d)
    p = os.path.join(ROOT, 'road-network.html'); t = open(p).read()
    m = re.search(r'^const DATA = (.*);$', t, re.M)
    new = {'built': time.strftime('%Y-%m-%d'), 'qop_meta': d['qop_meta'], 'viab': M, 'viability_meta': d['viability_meta'], 'nodes': d['nodes'], 'edges': d['edges']}
    t = t[:m.start()] + 'const DATA = ' + json.dumps(new, ensure_ascii=False) + ';' + t[m.end():]
    open(p, 'w').write(t)
    return M.get('breakers')

if __name__ == '__main__':
    b = main()
    if b:
        for x in b['items']: print(x['kind'], round(x['V'], 1), x['label'][:150])
