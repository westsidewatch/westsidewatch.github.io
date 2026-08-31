#!/usr/bin/env python3
from pathlib import Path
import json
p=Path.home()/'.dore/design/westside-watch.json'
d=json.loads(p.read_text(encoding='utf-8'))
d['canvas']['h']=1540
ids={x['id'] for x in d['nodes']}
labels=['EDITOR’S NOTE / 米斯巴','FEATURE / 迦密','頌讚 / 何烈山','看見 / 西區的夜晚','以琳','感動 / 別是巴','查經 / 伯特利','見證人 / 以斯帖','對話 / 守望者','安提阿','禱告 / 瑪拉拿','刊頭']
for i,label in enumerate(labels,1):
 nid='section-%02d'%i
 if nid in ids: continue
 col=0 if i<=6 else 1; row=(i-1)%6
 d['nodes'].append({'id':nid,'type':'text','role':'subtitle','text':'%02d · %s'%(i,label),'x':72+col*578,'y':980+row*80,'w':500,'size':24})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'ok':True,'canvas':d['canvas'],'node_count':len(d['nodes'])},ensure_ascii=False))
