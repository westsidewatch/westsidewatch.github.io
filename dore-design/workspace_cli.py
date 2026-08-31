#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import app_workspace as m
def out(v):print(json.dumps(v,ensure_ascii=False,indent=2))
p=argparse.ArgumentParser();sub=p.add_subparsers(dest='cmd',required=True)
for c in ('get','verify','history','undo'):sub.add_parser(c)
a=sub.add_parser('add-page');a.add_argument('name',nargs='?',default=None)
r=sub.add_parser('rename-page');r.add_argument('page_id');r.add_argument('name')
for c in ('delete-page','duplicate-page'):
 q=sub.add_parser(c);q.add_argument('page_id')
t=sub.add_parser('add-text');t.add_argument('page_id');t.add_argument('text')
ar=sub.add_parser('add-rule');ar.add_argument('page_id')
s=sub.add_parser('set-node');s.add_argument('page_id');s.add_argument('node_id');s.add_argument('patch_json')
for c in ('delete-node','duplicate-node'):
 q=sub.add_parser(c);q.add_argument('page_id');q.add_argument('node_id')
tok=sub.add_parser('token');tok.add_argument('key');tok.add_argument('value')
cv=sub.add_parser('canvas');cv.add_argument('page_id');cv.add_argument('width',type=float);cv.add_argument('height',type=float)
ex=sub.add_parser('export-svg');ex.add_argument('page_id')
x=p.parse_args();w=m.workspace()
if x.cmd=='get':out(w)
elif x.cmd=='verify':
 v=m.verify(w);out(v);raise SystemExit(0 if v['ok'] else 2)
elif x.cmd=='history':out(m.history())
elif x.cmd=='undo':out(m.undo())
elif x.cmd=='add-page':out(m.mutate(w,{'op':'add_page','name':x.name}))
elif x.cmd=='rename-page':out(m.mutate(w,{'op':'rename_page','page_id':x.page_id,'name':x.name}))
elif x.cmd=='delete-page':out(m.mutate(w,{'op':'delete_page','page_id':x.page_id}))
elif x.cmd=='duplicate-page':out(m.mutate(w,{'op':'duplicate_page','page_id':x.page_id}))
elif x.cmd=='add-text':out(m.mutate(w,{'op':'add_text','page_id':x.page_id,'text':x.text}))
elif x.cmd=='add-rule':out(m.mutate(w,{'op':'add_rule','page_id':x.page_id}))
elif x.cmd=='set-node':out(m.mutate(w,{'op':'set_node','page_id':x.page_id,'id':x.node_id,'patch':json.loads(x.patch_json)}))
elif x.cmd=='delete-node':out(m.mutate(w,{'op':'delete_node','page_id':x.page_id,'id':x.node_id}))
elif x.cmd=='duplicate-node':out(m.mutate(w,{'op':'duplicate_node','page_id':x.page_id,'id':x.node_id}))
elif x.cmd=='token':out(m.mutate(w,{'op':'token','key':x.key,'value':x.value}))
elif x.cmd=='canvas':out(m.mutate(w,{'op':'set_canvas','page_id':x.page_id,'patch':{'w':x.width,'h':x.height}}))
elif x.cmd=='export-svg':
 s=m.page_svg(w,x.page_id);dest=m.EXPORTS/f'westside-watch.{x.page_id}.svg';m.atomic_text(dest,s);out({'ok':True,'path':str(dest),'bytes':len(s)})
