#!/usr/bin/env python3
"""Doré Design 0.6.1 live workspace migration.
Removes the obsolete Antioch placeholder and turns empty pages into real Westside Watch editorial boards.
Safe to run repeatedly.
"""
from pathlib import Path
import json, os, datetime
HOME=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design')).expanduser()
WS=HOME/'westside-watch.workspace.json'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def text(i,t,x,y,w,size,role=None):
 n={'id':i,'type':'text','text':t,'x':x,'y':y,'w':w,'size':size}
 if role:n['role']=role
 return n
def rule(i,x,y,w): return {'id':i,'type':'rule','x':x,'y':y,'w':w,'h':1}
def block(i,eye,title,body,x,y,w,h=420): return {'id':i,'type':'block','eyebrow':eye,'title':title,'body':body,'x':x,'y':y,'w':w,'h':h}
def clean_nodes(nodes):
 out=[]
 for n in nodes:
  hay=' '.join(str(n.get(k,'')) for k in ('id','text','title','body','eyebrow')).lower()
  if '安提阿' in hay or 'antioch' in hay: continue
  out.append(n)
 return out
def main():
 if not WS.exists(): raise SystemExit('workspace_not_found')
 w=json.loads(WS.read_text(encoding='utf-8'))
 for p in w.get('pages',[]): p['nodes']=clean_nodes(p.get('nodes',[]))
 pages=w.setdefault('pages',[])
 by={p['id']:p for p in pages}
 if 'page-02' in by and not by['page-02'].get('nodes'):
  p=by['page-02'];p['name']='Contents / Editorial Wall';p['nodes']=[
   text('contents-kicker','WESTSIDE WATCH · CONTENTS',72,58,900,18),
   text('contents-title','守望，\n一座光明的城',72,112,650,68,'hero'),rule('contents-rule',72,278,1056),
   block('editor-note','米斯巴 · EDITOR’S NOTE','卷首','從黑夜到黎明：本期守望的起點。',72,330,310),
   block('feature-story','FEATURE','本月專題','信息為磚，輕重成垛，時間成流。',445,330,310),
   block('praise','何烈山 · PRAISE','頌讚','在曠野與山上重新聽見呼召。',818,330,310),
   text('contents-footer','01  米斯巴     02  FEATURE     03  何烈山     04  看見     05  以琳     06  感動',72,835,1056,15)]
 if 'page-03' in by and not by['page-03'].get('nodes'):
  p=by['page-03'];p['name']='Feature / Story';p['nodes']=[
   text('story-section','FEATURE · 01',72,60,420,16),rule('story-rule',72,100,1056),
   text('story-title','一座光明的城',72,150,690,78,'hero'),
   text('story-deck','守望不是等待事情發生，而是在黎明以前辨認光。',76,350,620,25),
   block('story-body','本月專題','WATCH FOR THE DAWN','「黑夜已深，白晝將近。」\n\n版面以 5:8 的編輯重量、細線、留白與城牆節奏組織內容。',790,150,338,560),
   text('story-footer','WESTSIDE WATCH · JOURNAL',72,855,600,14)]
 w['workspace_version']='0.6.1';w['revision']=int(w.get('revision',0))+1;w['updated_at']=now()
 tmp=WS.with_suffix('.json.tmp');tmp.write_text(json.dumps(w,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(WS)
 print(json.dumps({'ok':True,'code':'DORE_DESIGN_061_UPGRADE_PASS','revision':w['revision'],'pages':[(p['id'],p['name'],len(p.get('nodes',[]))) for p in pages],'antioch_remaining':any('安提阿' in json.dumps(p,ensure_ascii=False) or 'antioch' in json.dumps(p,ensure_ascii=False).lower() for p in pages)},ensure_ascii=False))
if __name__=='__main__': main()
