"""Make a ballot-only copy of the 2026 election data.

Reads ballot_2026.csv (from export_ballot.py) and your data folder (one folder per state, each with a
candidates.csv and one sub-folder per candidate), and writes a NEW folder holding only the candidates
on the November 3 ballot. Your original folder is never changed or deleted.

Usage: python3 filter_to_ballot.py ballot_2026.csv /path/to/2026elections-data /path/to/2026elections-ballot"""
import csv, os, shutil, sys
ballot_csv, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
if os.path.abspath(src) == os.path.abspath(dst): raise SystemExit('the output folder must be different from the data folder')
ballot = list(csv.DictReader(open(ballot_csv, encoding='utf-8')))
keep = {r['data_id'] for r in ballot if r['data_id']}
kept = dropped = 0; found = set()
for st in sorted(os.listdir(src)):
    sdir = os.path.join(src, st)
    if not os.path.isdir(sdir) or not os.path.exists(os.path.join(sdir, 'candidates.csv')): continue
    os.makedirs(os.path.join(dst, st), exist_ok=True)
    with open(os.path.join(sdir, 'candidates.csv'), encoding='utf-8') as f:
        rd = csv.DictReader(f); fields = rd.fieldnames; rows = list(rd)
    with open(os.path.join(dst, st, 'candidates.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in rows:
            if r['id'] in keep:
                w.writerow(r); kept += 1; found.add(r['id'])
                if os.path.isdir(os.path.join(sdir, r['id'])):
                    shutil.copytree(os.path.join(sdir, r['id']), os.path.join(dst, st, r['id']), dirs_exist_ok=True)
            else: dropped += 1
    for name in os.listdir(sdir):          # state-level files (anything that is not a candidate folder)
        p = os.path.join(sdir, name)
        if os.path.isfile(p) and name != 'candidates.csv': shutil.copy2(p, os.path.join(dst, st, name))
shutil.copy2(ballot_csv, os.path.join(dst, 'ballot_2026.csv'))
missing = sorted(keep - found)
print('kept %d ballot candidates, left out %d filers who are not on the ballot -> %s' % (kept, dropped, dst))
if missing: print('ballot ids not found in the data folder:', len(missing), missing[:10])
