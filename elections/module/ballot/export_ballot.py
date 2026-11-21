"""Export the verified November 3, 2026 ballot from the Elections module data.

Who is on the ballot cannot be worked out from FEC filings: the FEC records who filed, not who won a
primary or qualified for the ballot. The ballot list in the module was checked race by race against
state election offices, Wikipedia/Ballotpedia and AP (sources are listed per race). This script writes
that verified list out as a CSV.

Usage: python3 export_ballot.py data_states.json ballot_2026.csv"""
import csv, json, sys
src = sys.argv[1] if len(sys.argv) > 1 else 'data_states.json'
out = sys.argv[2] if len(sys.argv) > 2 else 'ballot_2026.csv'
d = json.load(open(src, encoding='utf-8')); R, C, CI = d['races'], d['cands'], d.get('cites', {})
PARTY = {'D': 'Democratic', 'R': 'Republican', 'L': 'Libertarian', 'G': 'Green', 'I': 'Independent', 'C': 'Constitution'}
rows = []
for rid in sorted(R, key=lambda k: (R[k].get('state', ''), k)):
    r = R[rid]
    for cid in r.get('candidates') or []:
        c = C[cid]
        rows.append({'race': rid, 'state': r.get('state', rid[:2]), 'office': r.get('chamber') or rid.split('-')[1].lower(),
                     'name': c['name'], 'party': c.get('party_note') or PARTY.get(c['party'], c['party']),
                     'incumbent': 'yes' if c.get('incumbent') else '', 'data_id': c.get('rec', ''),
                     'fec_ids': ';'.join((d.get('rec', {}).get(c.get('rec', ''), {}) or {}).get('fec', []) or ([c['fec_id']] if c.get('fec_id') else [])),
                     'race_status': r.get('status', ''), 'race_note': r.get('note', ''),
                     'sources': ' | '.join(CI[k]['u'] for k in (r.get('src') or []) if k in CI)})
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('%d candidates on the ballot in %d races -> %s' % (len(rows), len({r['race'] for r in rows}), out))
print('without a matching FEC data folder (never filed, mostly independents/minor parties):', sum(1 for r in rows if not r['data_id']))
