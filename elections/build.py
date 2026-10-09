import json,sys
src=open('/home/claude/el26/app.html',encoding='utf-8').read()
data=json.load(open(sys.argv[1] if len(sys.argv)>1 else '/home/claude/el26/data.json'))
blob=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
out=src.replace('/*__DATA__*/',blob)
open(sys.argv[2] if len(sys.argv)>2 else '/home/claude/el26/elections-2026.html','w',encoding='utf-8').write(out)
print(len(out))
