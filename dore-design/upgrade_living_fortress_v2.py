#!/usr/bin/env python3
"""Restore the approved #262 Watch for the Dawn front door into the workspace."""
from pathlib import Path
import datetime
import json
import os
import shutil

DATA=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design')).expanduser()
WS=DATA/'westside-watch.workspace.json'
HIST=DATA/'workspace-history'
SURFACE='homepage-watch-for-the-dawn-wysiwyg-v4'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def text(node_id,value,x,y,w,size,role=None):
    node={'id':node_id,'type':'text','text':value,'x':x,'y':y,'w':w,'size':size}
    if role: node['role']=role
    return node


def rule(node_id,x,y,w,h=1):
    return {'id':node_id,'type':'rule','x':x,'y':y,'w':w,'h':h}


def block(node_id,eyebrow,title,body,x,y,w,h):
    return {'id':node_id,'type':'block','eyebrow':eyebrow,'title':title,'body':body,'x':x,'y':y,'w':w,'h':h}


def homepage():
    # Coordinates remain available for the Structure maintenance view. The real
    # homepage/editor layout is responsive and comes from the approved #262 DOM.
    nodes=[
        text('brand','WESTSIDE WATCH',64,38,460,18),
        text('brand-zh','西望',1035,38,110,18),
        rule('h-rule',64,82,1072),
        text('watch-kicker','Westside Watch / 西望',64,145,500,14),
        text('home-title','WATCH\nFOR THE\nDAWN.',64,185,650,88,'hero'),
        text('home-deck','在黑夜仍然守望，在清晨尚未來到以前保存光。文章、聖經、教會生活與研究，在同一座城中彼此照亮。',68,500,505,24),
        text('verse','The night is far spent,\nthe day is at hand.\nRomans 13:12',820,545,300,14),
        rule('hero-rule',64,695,1072),
        text('threshold-title','一個入口，四條路。',64,735,420,25),
        text('threshold-meta','Read · Study · Gather · Remember',735,742,400,13),
        block('journal-tower','Journal · Current volume','守望，\n一座光明的城','進入本期 Journal。圖像、文字、見證與禱告在一個獨立的閱讀世界中展開。',64,825,470,760),
        block('one-territory','ONE · Bible study','路上，祂向我們打開聖經。','從一章、一卷書、一條路線開始，把經文、歷史、地圖與串珠重新連起來。',552,825,584,270),
        block('church-territory','Living Water West','一座城，\n也是一個家。','Sunday Worship · Bible Study · Prayer · Life Together',552,1113,282,472),
        block('library-territory','Dawn Library · 黎明書局','被保存的光。','地圖、文章、史料與研究資源逐步沉澱，成為可以再次被調用的知識。',852,1113,284,226),
        block('join-territory','The Gate','Come\nand see.','',852,1357,284,228),
        text('gate-copy-left','從閱讀走向相遇。',64,1678,360,30),
        text('gate-mark','THE GATE',526,1765,150,14),
        text('gate-copy-right','從守望走向黎明。',820,1655,316,30),
        rule('gate-left',64,1828,445),
        rule('gate-right',691,1828,445),
        text('watch-number','12',64,1935,250,128,'hero'),
        text('watch-quote','黑夜已深，\n白晝將近。',420,1930,620,54,'hero'),
        text('watch-cite','Romans 13:12 · Watch for the Dawn',424,2080,360,14),
        rule('footer-rule',64,2175,1072),
        text('footer','WESTSIDE WATCH · WATCH FOR THE DAWN',64,2210,650,13),
    ]
    return {'id':'homepage','name':'Homepage / Watch for the Dawn','canvas':{'w':1200,'h':2280},'nodes':nodes}


def main():
    if not WS.exists(): raise SystemExit('workspace_not_found')
    workspace=json.loads(WS.read_text(encoding='utf-8'))
    current=next((p for p in workspace.get('pages',[]) if p.get('id')=='homepage'),None)
    if workspace.get('active_surface')==SURFACE and current and any(n.get('id')=='join-territory' for n in current.get('nodes',[])):
        print(json.dumps({'ok':True,'code':'WATCH_FOR_DAWN_WYSIWYG_ALREADY_CURRENT','revision':workspace.get('revision'),'surface':SURFACE},ensure_ascii=False));return
    HIST.mkdir(parents=True,exist_ok=True)
    stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    shutil.copy2(WS,HIST/f'westside-watch.before-wysiwyg-front-door-{stamp}.json')
    pages=workspace.setdefault('pages',[]);replacement=homepage()
    index=next((i for i,p in enumerate(pages) if p.get('id')=='homepage'),None)
    if index is None: pages.insert(0,replacement)
    else: pages[index]=replacement
    workspace['name']='New Westside — Watch for the Dawn'
    workspace['active_surface']=SURFACE
    workspace['design_direction']='watch-for-the-dawn'
    workspace['layout_source']='approved-front-door-262'
    workspace['revision']=int(workspace.get('revision',0))+1
    workspace['updated_at']=now()
    tmp=WS.with_suffix('.json.tmp');tmp.write_text(json.dumps(workspace,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(WS)
    print(json.dumps({'ok':True,'code':'WATCH_FOR_DAWN_WYSIWYG_WORKSPACE_PASS','revision':workspace['revision'],'surface':SURFACE,'homepage_nodes':len(replacement['nodes']),'preserved_pages':[p.get('id') for p in pages if p.get('id')!='homepage']},ensure_ascii=False))


if __name__=='__main__': main()
