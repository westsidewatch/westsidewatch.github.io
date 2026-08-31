#!/usr/bin/env python3
"""Rebuild the live Doré Design workspace from the current New Westside visual grammar.
Creates a reversible snapshot, then replaces stale acceptance-demo pages with a real editorial architecture study.
"""
from pathlib import Path
import json, os, datetime, shutil
HOME=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design')).expanduser()
WS=HOME/'westside-watch.workspace.json'; HIST=HOME/'workspace-history'; HIST.mkdir(parents=True,exist_ok=True)
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def text(i,t,x,y,w,size,role=None):
 n={'id':i,'type':'text','text':t,'x':x,'y':y,'w':w,'size':size}
 if role:n['role']=role
 return n
def rule(i,x,y,w,h=1): return {'id':i,'type':'rule','x':x,'y':y,'w':w,'h':h}
def block(i,eye,title,body,x,y,w,h=300): return {'id':i,'type':'block','eyebrow':eye,'title':title,'body':body,'x':x,'y':y,'w':w,'h':h}
def page(pid,name,nodes,h=1000): return {'id':pid,'name':name,'canvas':{'w':1200,'h':h},'nodes':nodes}
def main():
 if not WS.exists(): raise SystemExit('workspace_not_found')
 old=json.loads(WS.read_text(encoding='utf-8'))
 stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
 shutil.copy2(WS,HIST/f'westside-watch.before-new-westside-{stamp}.json')
 tokens=dict(old.get('tokens') or {})
 tokens.update({'paper':'#FAF9F5','ink':'#252525','night':'#102A43','gold':'#A2872A','morning':'#D2BC69'})
 home=[
  text('brand','WESTSIDE WATCH',64,46,470,18),text('brand-zh','西望',1030,45,100,18),rule('h-rule',64,84,1072),
  text('watch-kicker','WATCH FOR THE DAWN',64,122,500,15),text('home-title','守望，\n一座光明的城',64,160,530,66,'hero'),
  text('home-deck','信息為磚，輕重成垛，時間成流。',66,322,500,22),
  block('journal-tower','VOL.00 · JOURNAL','WATCH FOR\nTHE DAWN','本期最高 Editorial Gravity · 5:8 Journal Tower',700,126,360,575),
  rule('wall-horizon',64,424,568),
  block('brick-01','01 · 米斯巴 · 卷首','守望，一座光明的城','Editor’s Note',64,466,258,260),
  block('brick-02','02 · 伯利恆 · 感動','他等候那座有根基的城','Scripture',350,466,282,260),
  block('brick-03','03 · 門 · 看見','誰在建造我們的城？','The Gate · Seeing',64,760,340,190),
  block('brick-04','04 · 迦密 · 特輯','城牆之上，黎明之前','Carmel · Feature',432,760,200,190),
  text('gate-mark','THE GATE',810,770,250,15),rule('gate-left',700,820,142),rule('gate-right',918,820,142),
  text('footer','LIVING WATER WEST  ·  ONE  ·  JOIN',700,910,400,14)
 ]
 watch=[text('m1','I · WATCH / 守望',64,54,600,18),rule('m1r',64,92,1072),text('m1t','We watch because God first watched over us.',64,132,760,40,'hero'),
  block('w01','01 · MIZPAH','米斯巴','卷首 · Editor’s Note',64,300,250),block('w02','02 · BETHLEHEM','伯利恆','感動 · Scripture',342,300,250),block('w03','03 · THE GATE','門','看見 · Seeing',620,300,250),block('w04','04 · CARMEL','迦密','特輯 · Feature',898,300,238),text('selah','FIRST WATCH · SELAH / 細拉',64,720,700,20)]
 witness=[text('m2','II · WITNESS / 見證',64,54,600,18),rule('m2r',64,92,1072),text('m2t','We see how others answered the call of God.',64,132,760,40,'hero'),block('w05','05 · ESTHER','以斯帖','人物 · Witness',64,300,500,430),block('w06','06 · ADULLAM','亞杜蘭洞','對話 · Dialogue',636,300,500,430),text('dove','MIDDLE WATCH · THE SILENT DOVE IN THE DISTANCE / 遠方無聲鴿',64,800,1000,18)]
 walk=[text('m3','III · WALK / 同行',64,54,600,18),rule('m3r',64,92,1072),text('m3t','Grace received becomes a life lived together.',64,132,760,40,'hero'),block('w07','07 · WESTSIDE NIGHT','西區的夜晚','查經 · Bible Study',64,300,244),block('w08','08 · ELIM','以琳','靈修 · Devotion',336,300,244),block('w09','09 · BEERSHEBA','別是巴','默想 · Meditation',608,300,244),block('w10','10 · BETHEL','伯特利','教會生活 · Church Life',880,300,256),text('kinneret','MORNING WATCH · KINNERET / 基尼烈',64,800,700,20)]
 worship=[text('m4','IV · WORSHIP / 敬拜',64,54,600,18),rule('m4r',64,92,1072),text('m4t','Because God is God, we worship and wait for His coming.',64,132,900,40,'hero'),block('w11','11 · HOREB','何烈山','頌讚 · Praise',64,310,500,470),block('w12','12 · MARANATHA','瑪拉拿','禱告 · Prayer',636,310,500,470),text('close','WATCH FOR THE DAWN',64,850,500,22)]
 new={'schema':'dore.design.workspace.v1','id':'westside-watch','name':'New Westside — Living Editorial Grammar','revision':int(old.get('revision',0))+1,'updated_at':now(),'tokens':tokens,'pages':[page('homepage','Homepage / Living Wall',home),page('watch','I · Watch',watch),page('witness','II · Witness',witness),page('walk','III · Walk',walk),page('worship','IV · Worship',worship)]}
 raw=json.dumps(new,ensure_ascii=False,indent=2)
 forbidden='antio' in raw.lower() or '安提阿' in raw
 if forbidden: raise SystemExit('obsolete_structure_detected')
 if not ('10 · BETHEL' in raw and '伯特利' in raw): raise SystemExit('current_item_10_missing')
 tmp=WS.with_suffix('.json.tmp');tmp.write_text(raw,encoding='utf-8');tmp.replace(WS)
 print(json.dumps({'ok':True,'code':'NEW_WESTSIDE_REBUILD_PASS','revision':new['revision'],'pages':[(p['id'],len(p['nodes'])) for p in new['pages']],'item10':'Bethel / 伯特利','obsolete_structure':False},ensure_ascii=False))
if __name__=='__main__': main()
