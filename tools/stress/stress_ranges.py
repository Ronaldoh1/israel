import json,sys
SP='/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad/'
d=json.load(open(SP+'stress.json'))
out={}
for k,pub in d['base'].items():
    vals=[v[k] for n,v in d['all'].items() if (n.startswith('exp_') or n.startswith('reported_') or n=='training_x10')]
    vals.append(pub)
    out[k]=[round(pub),round(min(vals)),round(max(vals)),round(d['all']['people_linear'][k]),round(d['all']['cal_0.95'][k]),round(d['all']['cal_0.999'][k])]
for k,v in out.items(): print(k,v)
json.dump(out,open(SP+'stress_ranges.json','w'))
l=json.load(open(SP+'stress_loso.json'))
print(json.dumps(l)[:200])
