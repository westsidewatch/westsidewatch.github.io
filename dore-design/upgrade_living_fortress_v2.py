#!/usr/bin/env python3
"""Promote A · Living Fortress into the durable Doré Design workspace.

The migration snapshots the current workspace and replaces only the homepage.
Journal section pages and later human edits remain untouched on repeat runs.
"""
from pathlib import Path
import datetime
import json
import os
import shutil

DATA=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design')).expanduser()
WS=DATA/'westside-watch.workspace.json'
HIST=DATA/'workspace-history'
SURFACE='homepage-v2-living-fortress'


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def text(node_id,value,x,y,w,size,role=None):
    node={'id':node_id,'type':'text','text':value,'x':x,'y':y,'w':w,'size':size}
    if role:
        node['role']=role
    return node


def rule(node_id,x,y,w,h=1):
    return {'id':node_id,'type':'rule','x':x,'y':y,'w':w,'h':h}


def block(node_id,eyebrow,title,body,x,y,w,h):
    return {
        'id':node_id,'type':'block','eyebrow':eyebrow,'title':title,'body':body,
        'x':x,'y':y,'w':w,'h':h,
    }


def homepage():
    nodes=[
        text('brand','WESTSIDE WATCH',54,38,460,18),
        text('brand-zh','西望',1050,38,100,18),
        rule('h-rule',54,78,1092),
        text('watch-kicker','A · LIVING FORTRESS / HOMEPAGE V2',54,112,620,14),
        text('home-title','A CITY\nSTILL AWAKE.',54,148,670,70,'hero'),
        text('home-deck','信息為磚，輕重成垛，時間成流。',58,305,600,21),
        block('journal-tower','JOURNAL PORTAL · CURRENT VOLUME','守望，\n一座光明的城','5:8 · Highest Editorial Gravity · Enter the independent issue',54,360,390,624),
        block('one-territory','ONE · SCRIPTURE','路上，祂向我們\n打開聖經','Open ONE',462,425,255,240),
        block('signal-territory','NOW · FIRST WATCH','城牆之上，\n黎明之前','Current editorial signal',735,480,200,220),
        block('church-territory','LIVING WATER WEST','一座城，\n也是一個家','Worship · Bible Study · Prayer',952,370,194,330),
        block('witness-territory','WITNESS','在日常中\n看見神','Life and testimony',462,750,185,234),
        block('prayer-territory','PRAYER','主啊，\n願你來','Maranatha',818,710,126,118),
        block('archive-territory','ARCHIVE · TIME','留下來','Old content recedes without disappearing.',808,838,138,146),
        block('library-territory','DAWN LIBRARY','被保存的光','Maps · essays · history · research',960,720,186,264),
        text('gate-mark','THE GATE',680,930,150,14),
        rule('gate-left',660,986,48),
        rule('gate-right',812,986,48),
        text('footer','WESTSIDE WATCH · BRICK / BATTLEMENT / FLOW',462,1025,620,13),
    ]
    return {
        'id':'homepage',
        'name':'Homepage V2 / A · Living Fortress',
        'canvas':{'w':1200,'h':1080},
        'nodes':nodes,
    }


def main():
    if not WS.exists():
        raise SystemExit('workspace_not_found')
    workspace=json.loads(WS.read_text(encoding='utf-8'))
    current=next((p for p in workspace.get('pages',[]) if p.get('id')=='homepage'),None)
    if workspace.get('active_surface')==SURFACE and current and any(n.get('id')=='one-territory' for n in current.get('nodes',[])):
        print(json.dumps({'ok':True,'code':'LIVING_FORTRESS_ALREADY_CURRENT','revision':workspace.get('revision'),'surface':SURFACE},ensure_ascii=False))
        return
    HIST.mkdir(parents=True,exist_ok=True)
    stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    shutil.copy2(WS,HIST/f'westside-watch.before-living-fortress-{stamp}.json')
    pages=workspace.setdefault('pages',[])
    replacement=homepage()
    index=next((i for i,p in enumerate(pages) if p.get('id')=='homepage'),None)
    if index is None:
        pages.insert(0,replacement)
    else:
        pages[index]=replacement
    workspace['name']='New Westside — A · Living Fortress'
    workspace['active_surface']=SURFACE
    workspace['design_direction']='A-living-fortress'
    workspace['revision']=int(workspace.get('revision',0))+1
    workspace['updated_at']=now()
    tmp=WS.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(workspace,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(WS)
    print(json.dumps({
        'ok':True,
        'code':'LIVING_FORTRESS_WORKSPACE_PASS',
        'revision':workspace['revision'],
        'surface':SURFACE,
        'homepage_nodes':len(replacement['nodes']),
        'preserved_pages':[p.get('id') for p in pages if p.get('id')!='homepage'],
    },ensure_ascii=False))


if __name__=='__main__':
    main()
