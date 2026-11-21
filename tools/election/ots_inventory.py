#!/usr/bin/env python3
"""Inventory of the VoteAmericaFirst data folder: what was collected, for how many candidates, and what is missing.
Reads only; changes nothing. Writes inventory.md next to this script and prints it.
Usage:  python3 ots_inventory.py [folder]      (default: the folder this script is in)"""
import os, sys, csv, json, collections, datetime

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '__pycache__', 'node_modules'}
out = []
def p(s=''): out.append(s)
def mb(n): return f'{n / 1e6:,.1f} MB' if n < 1e9 else f'{n / 1e9:,.2f} GB'

# 1. sizes by top-level folder and by second level under data/
def walk_size(d):
    t = n = 0
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x not in SKIP_DIRS]
        for f in fs:
            try: t += os.path.getsize(os.path.join(r, f)); n += 1
            except OSError: pass
    return t, n

p(f'# VoteAmericaFirst inventory, {datetime.datetime.now():%Y-%m-%d %H:%M}')
p(f'Folder: {ROOT}\n')
p('## Size by folder')
total = 0
for name in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, name)
    if os.path.isdir(full) and name not in SKIP_DIRS:
        s, n = walk_size(full); total += s
        p(f'- {name}/  {mb(s)}, {n:,} files')
        if name in ('data', '_downloads'):
            for sub in sorted(os.listdir(full)):
                sf = os.path.join(full, sub)
                if os.path.isdir(sf):
                    s2, n2 = walk_size(sf); p(f'    - {sub}/  {mb(s2)}, {n2:,} files')
                else:
                    p(f'    - {sub}  {mb(os.path.getsize(sf))}')
    elif os.path.isfile(full):
        total += os.path.getsize(full)
p(f'Total: {mb(total)}\n')

# 2. candidate folders: data/<dataset>/<STATE>/<candidate>/ ; count which files each candidate has
p('## Per-candidate coverage (which files exist, by dataset)')
data = os.path.join(ROOT, 'data')
if os.path.isdir(data):
    for ds in sorted(os.listdir(data)):
        dsp = os.path.join(data, ds)
        if not os.path.isdir(dsp): continue
        states = [s for s in sorted(os.listdir(dsp)) if os.path.isdir(os.path.join(dsp, s)) and len(s) == 2 and s.isupper()]
        if not states: continue
        cands = []
        for s in states:
            for c in sorted(os.listdir(os.path.join(dsp, s))):
                cp = os.path.join(dsp, s, c)
                if os.path.isdir(cp): cands.append((s, c, set(os.listdir(cp))))
        files = collections.Counter(f for _, _, fs in cands for f in fs)
        p(f'\n### data/{ds}: {len(cands):,} candidates in {len(states)} states')
        for f, n in files.most_common(40):
            p(f'- {f}: {n:,} of {len(cands):,} ({100 * n / max(1, len(cands)):.0f}%)')
        empty = [f'{s}/{c}' for s, c, fs in cands if not fs]
        if empty: p(f'- empty candidate folders: {len(empty)} (e.g. {", ".join(empty[:5])})')
        by_state = collections.Counter(s for s, _, _ in cands)
        p('- candidates by state: ' + ', '.join(f'{s} {n}' for s, n in sorted(by_state.items())))
        # step status recorded inside money_deep.json, if present
        steps = collections.Counter(); seen = 0
        for s, c, fs in cands:
            if 'money_deep.json' in fs:
                try: d = json.load(open(os.path.join(dsp, s, c, 'money_deep.json')))
                except Exception: continue
                seen += 1
                for k, v in (d.items() if isinstance(d, dict) else []):
                    if v not in (None, {}, [], '', 0): steps[k] += 1
        if seen:
            p(f'- money_deep.json filled sections ({seen:,} files): ' + ', '.join(f'{k} {n:,}' for k, n in steps.most_common()))
else:
    p('(no data/ folder)')

# 3. summary CSVs: row counts and columns
p('\n## Summary files')
for r, ds, fs in os.walk(ROOT):
    ds[:] = [x for x in ds if x not in SKIP_DIRS and x != '_downloads']
    depth = os.path.relpath(r, ROOT).count(os.sep)
    if depth > 2: ds[:] = []; continue
    for f in sorted(fs):
        if f.endswith('.csv') and ('summary' in f or 'index' in f or 'candidates' in f or 'ballot' in f):
            fp = os.path.join(r, f)
            try:
                with open(fp, newline='', encoding='utf-8', errors='replace') as h:
                    rd = csv.reader(h); head = next(rd, []); rows = sum(1 for _ in rd)
                p(f'- {os.path.relpath(fp, ROOT)}: {rows:,} rows; columns: {", ".join(head[:18])}{" …" if len(head) > 18 else ""}')
            except Exception as e: p(f'- {os.path.relpath(fp, ROOT)}: unreadable ({e})')
        if f.endswith('.md') and f.lower().startswith('summary'):
            p(f'- {os.path.relpath(os.path.join(r, f), ROOT)} (markdown summary)')

# 4. last lines of every log
p('\n## Logs (last 4 lines each)')
logs = os.path.join(ROOT, 'logs')
if os.path.isdir(logs):
    for f in sorted(os.listdir(logs)):
        fp = os.path.join(logs, f)
        if os.path.isfile(fp):
            try: lines = open(fp, errors='replace').read().strip().splitlines()[-4:]
            except Exception: lines = []
            p(f'\n{f}  ({datetime.datetime.fromtimestamp(os.path.getmtime(fp)):%m-%d %H:%M})')
            for l in lines: p('    ' + l[:200])

txt = '\n'.join(out)
open(os.path.join(ROOT, 'inventory.md'), 'w').write(txt + '\n')
print(txt)
