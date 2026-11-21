"""Build an Obsidian vault from network.json. Usage: python3 make_vault.py OUTDIR"""
import json, os, sys, math, re, shutil
from collections import defaultdict, deque
D=json.load(open(os.path.join(os.path.dirname(__file__),'network.json')))
OUT=sys.argv[1]; V=os.path.join(OUT,'Epstein Network Map')
shutil.rmtree(V,ignore_errors=True)
N={x['id']:x for x in D['nodes']}; E=D['edges']
FOLD={'person':'People','institution':'Institutions','company':'Institutions','government':'Institutions','document':'Documents','place':'Places'}
EMO={'person':'👤','company':'💼','institution':'🎓','government':'🏛️','document':'📜','place':'📍'}
ST={'probable':'🟡 probable (inference, labelled)','verified':'✅ verified','to-verify':'🔎 to verify','not-established':'⛔ not established'}
TIER={'adjudicated':'Adjudicated (verdict, ruling or settlement)','sworn-allegation':'Sworn allegation','association':'Documented association (no conduct alleged)','charged':'Charged (died before trial)','withdrawn-allegation':'Allegation withdrawn','allegation-to-congress':'Allegation made to Congress (unadjudicated; denied)','':'—'}
CL={'centre':'The centre','finance':'Finance','money':'Money vehicles','tech':'Tech','politics':'Politics','state':'State','royals':'Royals','culture':'Culture and science','justice':'Justice system','release':'The files fight','intelligence':'Intelligence','reporters':'Those who reported it','places':'Places','abroad':'Accountability abroad','witnesses':'Deaths and lost testimony','operations':'Running the operation','evidence':'The evidence trail','vendors':'Vendors and service providers'}
safe=lambda s: re.sub(r'[\\/:*?"<>|#^\[\]]','',s)
fn=lambda i: safe(N[i]['name'])
# degree from Epstein over verified edges
NOTIE={'custody','instruction','knowledge of spouse\'s connection','allegation to Congress','claim','investigation','testimony','litigation','oversight','complaint','court ruling','reporting','document','forensic review'}
adj=defaultdict(set)
for x in E:
    if x['status']=='verified' and x['type'] not in NOTIE: adj[x['f']].add(x['t']); adj[x['t']].add(x['f'])
deg={'epstein':0}; q=deque(['epstein'])
while q:
    u=q.popleft()
    for w in adj[u]:
        if w not in deg: deg[w]=deg[u]+1; q.append(w)
DL=lambda i: {0:'centre',1:'1° direct',2:'2° operational',3:'3° strategic'}.get(deg.get(i),'not connected by verified edges') + (' · apex' if N[i]['apex'] else '')
# notes
byn=defaultdict(list)
for x in E: byn[x['f']].append((x,x['t'])); byn[x['t']].append((x,x['f']))
for i,x in N.items():
    d=os.path.join(V,FOLD[x['kind']]); os.makedirs(d,exist_ok=True)
    tags=[x['cluster'],x['kind']]+(['apex'] if x['apex'] else [])
    fm=['---',f"type: {x['kind']}",f"cluster: {CL[x['cluster']]}",f"tier: {TIER[x['tier']]}",f"distance: {DL(i)}",f"scenes: [{', '.join(x['scenes'])}]",f"tags: [{', '.join(tags)}]",'---']
    b=[f"# {EMO[x['kind']]} {x['name']}",'',x['note'],'',f"**Tier:** {TIER[x['tier']]}  ",f"**Distance from Epstein:** {DL(i)}  "]
    if x['scenes']: b.append(f"**Simulation scenes:** {', '.join('`'+s+'`' for s in x['scenes'])}")
    b+=['','## Connections','']
    for ed,o in sorted(byn[i],key=lambda z:(z[0]['status']!='verified',N[z[1]]['name'])):
        arrow='→' if ed['f']==i else '←'
        b.append(f"- {arrow} [[{fn(o)}]] — {ed['label']} · *{ed['type']}* · {ST[ed['status']]} · source: {ed['src']}")
    open(os.path.join(d,fn(i)+'.md'),'w').write('\n'.join(fm+b)+'\n')
# loops: short cycles (3–4) over verified edges, excluding pure kinship/office triangles
SKIP=NOTIE
und=defaultdict(dict)
for x in E:
    if x['status']=='verified' and x['type'] not in SKIP: und[x['f']][x['t']]=x; und[x['t']][x['f']]=x
cyc=set()
def dfs(path):
    if len(path)>4: return
    for w in und[path[-1]]:
        if w==path[0] and len(path)>=3: cyc.add(tuple(path))
        elif w not in path and w>path[0]: dfs(path+[w])
for s in list(und): dfs([s])
seen=set(); loops=[]
for c in cyc:
    k=frozenset(c)
    if k in seen: continue
    seen.add(k); loops.append(c)
def ok(c):
    ts=[und[c[j]][c[(j+1)%len(c)]]['type'] for j in range(len(c))]
    return sum(t in ('kinship','office','ownership') for t in ts) < len(ts)-1
loops=[c for c in loops if ok(c)]
lp=['# 🔄 Loops','','Closed circles found automatically in the **verified** edges (3–4 steps). Investigation, testimony and litigation edges are left out, because a probe looking at two people is not a tie between them. A loop is a lead to examine, not a finding: each one is tested in the book (Part 4, "The loops chapter").','']
for c in sorted(loops,key=len):
    seq=list(c)+[c[0]]
    lp.append('- '+' → '.join(f'[[{fn(a)}]]' for a in seq))
    for j in range(len(c)):
        ed=und[c[j]][c[(j+1)%len(c)]]; lp.append(f"    - {N[c[j]]['name']} – {N[c[(j+1)%len(c)]]['name']}: {ed['label']} ({ed['type']})")
os.makedirs(os.path.join(V,'Maps'),exist_ok=True)
open(os.path.join(V,'Maps','Loops.md'),'w').write('\n'.join(lp)+'\n')
# to-verify list
tv=['# 🔎 To verify','','Every edge still marked as a lead. Each needs a primary document (an EFTA file, a filing or named reporting) before it can be used in the book. Change `status` to `verified` in `network.json` once it is sourced, then rebuild.','']
for x in E:
    if x['status']=='to-verify': tv.append(f"- [ ] [[{fn(x['f'])}]] → [[{fn(x['t'])}]]: {x['label']} — *{x['src']}*")
tv+=['','## Not established (kept so readers see where the record stops)','']
for x in E:
    if x['status']=='not-established': tv.append(f"- [[{fn(x['f'])}]] → [[{fn(x['t'])}]]: {x['label']}")
open(os.path.join(V,'Maps','To Verify.md'),'w').write('\n'.join(tv)+'\n')
# clusters
for c,label in CL.items():
    mem=[i for i in N if N[i]['cluster']==c]
    if not mem: continue
    open(os.path.join(V,'Maps',f'Cluster - {safe(label)}.md'),'w').write(f"# {label}\n\n"+'\n'.join(f"- [[{fn(i)}]] · {TIER[N[i]['tier']]} · {DL(i)}" for i in sorted(mem,key=lambda i:N[i]['name']))+'\n')
# start here
cnt=defaultdict(int)
for x in E: cnt[x['status']]+=1
sh=f"""# Start here

**The Epstein Network Map** · data as of {D['built']} · {len(N)} nodes · {len(E)} connections ({cnt['verified']} verified, {cnt['to-verify']} to verify, {cnt['not-established']} not established, {cnt['probable']} probable)

This vault is generated from `book/plan/epstein_map/network.json`. Edit the data and rebuild; don't edit notes by hand, or the next build overwrites them. The same data will drive the clickable map in the library.

## How to read it
- **Open the graph view** (Ctrl/Cmd+G). Colours: centre = gold, finance = green, tech = blue, politics/state = purple, royals = magenta, justice/release = slate, intelligence = grey, places = brown, reporters = teal.
- **Open `Network.canvas`** for the ring layout: Epstein at the centre, then 1° direct, 2° operational and 3° strategic connections. Distance counts only real ties (money, employment, office, kinship, correspondence), never an investigator or committee looking at two people.
- **Every connection line** in a note carries: direction · label · *type* · status · source.

## Status
- ✅ **verified**: in a sourced simulation scene or checked live on the build date.
- 🔎 **to verify**: a lead (mostly from the documentaries). Not usable in the book until sourced. See [[To Verify]].
- 🟡 **probable**: a labelled inference from documented facts, never a finding (used for spouse knowledge-of-connection).
- ⛔ **not established**: kept on purpose, so the map shows where the record stops (the intelligence claims).

## Tiers (for people)
Adjudicated → Sworn allegation → Documented association (no conduct alleged) → Not carried (not on the map at all).
Being on this map is **not** an accusation. Most people here are *documented association*, and that tier says nothing about conduct.

## Rules built into the data
- Family members are separate notes with a kinship edge (for example [[Hillary Clinton]] and [[Bill Clinton]]). One person's record never transfers to another.
- [[State of Israel (government)]] carries documented state acts only (offices, a state funeral, a SIGINT unit), never a people or a faith.
- Intelligence claims appear only as ⛔ edges, labelled.

## Maps
- [[Loops]]: circles found automatically in verified edges.
- [[To Verify]]: the research queue.
- Clusters: {', '.join(f'[[Cluster - {safe(l)}]]' for c,l in CL.items() if any(N[i]['cluster']==c for i in N))}
"""
open(os.path.join(V,'00 Start Here.md'),'w').write(sh)
# canvas: rings by degree, sectors by cluster
order=list(CL)
ring=defaultdict(list)
for i in N: ring[min(deg.get(i,4),4)].append(i)
cn=[]; pos={}
R={0:0,1:1100,2:2100,3:2900,4:3600}
for r,ids in ring.items():
    ids.sort(key=lambda i:(order.index(N[i]['cluster']),N[i]['name']))
    for k,i in enumerate(ids):
        a=2*math.pi*k/max(len(ids),1)-math.pi/2
        x,y=(0,0) if r==0 else (R[r]*math.cos(a),R[r]*math.sin(a))
        pos[i]=(x,y)
COL={'centre':'3','finance':'4','money':'4','tech':'5','politics':'6','state':'6','royals':'6','culture':'2','justice':'1','release':'1','intelligence':'0','reporters':'5','places':'2','abroad':'1','witnesses':'1','operations':'4','evidence':'2','vendors':'5'}
for i,(x,y) in pos.items():
    item={'id':i,'type':'file','file':f"{FOLD[N[i]['kind']]}/{fn(i)}.md",'x':int(x-170),'y':int(y-90),'width':340,'height':180}
    if COL.get(N[i]['cluster'],'0')!='0': item['color']=COL[N[i]['cluster']]
    cn.append(item)
ce=[]
for k,x in enumerate(E):
    ed={'id':f'e{k}','fromNode':x['f'],'toNode':x['t'],'label':x['label'][:60]}
    if x['status']=='to-verify': ed['color']='3'
    if x['status']=='not-established': ed['color']='1'
    ce.append(ed)
json.dump({'nodes':cn,'edges':ce},open(os.path.join(V,'Network.canvas'),'w'),indent=1)
# graph colours
os.makedirs(os.path.join(V,'.obsidian'),exist_ok=True)
rgb=lambda h:int(h.lstrip('#'),16)
groups=[('tag:#centre','#D4A62A'),('tag:#finance OR tag:#money','#2E8B57'),('tag:#tech','#3A6FD8'),('tag:#politics OR tag:#state','#7B4FB8'),('tag:#royals','#B0408A'),('tag:#justice OR tag:#release','#5B6B7F'),('tag:#intelligence','#8A8A8A'),('tag:#places','#8B5A2B'),('tag:#reporters','#2A9D9D'),('tag:#abroad','#5B6B7F'),('tag:#culture','#C07A2C'),('tag:#witnesses','#A33A3A'),('tag:#operations','#4E7D3A'),('tag:#evidence','#B08A2E'),('tag:#vendors','#3A8FA0')]
json.dump({'colorGroups':[{'query':q,'color':{'a':1,'rgb':rgb(c)}} for q,c in groups],'showTags':False,'showAttachments':False,'hideUnresolved':True},open(os.path.join(V,'.obsidian','graph.json'),'w'),indent=1)
print('vault',V,'| notes',len(N),'| loops',len(loops),'| degrees',dict(sorted(((v,sum(1 for d in deg.values() if d==v)) for v in set(deg.values())))),'| unreached',[N[i]['name'] for i in N if i not in deg])
