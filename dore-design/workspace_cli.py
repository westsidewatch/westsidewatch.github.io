#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import app_multi as m
def out(v): print(json.dumps(v,ensure_ascii=False,indent=2))
p=argparse.ArgumentParser();sub=p.add_subparsers(dest='cmd',required=True)
sub.add_parser('get');sub.add_parser('verify')
a=sub.add_parser('add-page');a.add_argument('name',nargs='?',default=None)
r=sub.add_parser('rename-page');r.add_argument('page_id');r.add_argument('name')
d=sub.add_parser('delete-page');d.add_argument('page_id')
dp=sub.add_parser('duplicate-page');dp.add_argument('page_id')
t=sub.add_parser('add-text');t.add_argument('page_id');t.add_argument('text')
s=sub.add_parser('set-node');s.add_argument('page_id');s.add_argument('node_id');s.add_argument('patch_json')
dn=sub.add_parser('delete-node');dn.add_argument('page_id');dn.add_argument('node_id')
du=sub.add_parser('duplicate-node');du.add_argument('page_id');du.add_argument('node_id')
x=p.parse_args();w=m.workspace()
if x.cmd=='get': out(w)
elif x.cmd=='verify':
 pids=[q['id'] for q in w.get('pages',[])];allnodes=[(q['id'],n['id']) for q in w.get('pages',[]) for n in q.get('nodes',[])];obsolete=[(q['id'],n['id']) for q in w.get('pages',[]) for n in q.get('nodes',[]) if '安提阿' in json.dumps(n,ensure_ascii=False) or 'antioch' in json.dumps(n,ensure_ascii=False).lower()];checks={'schema':w.get('schema')=='dore.design.workspace.v1','pages':len(pids)>=1,'unique_pages':len(pids)==len(set(pids)),'unique_nodes_per_page':all(len([n['id'] for n in q['nodes']])==len(set(n['id'] for n in q['nodes'])) for q in w['pages']),'obsolete_removed':not obsolete};out({'ok':all(checks.values()),'checks':checks,'revision':w.get('revision'),'page_count':len(pids),'node_count':len(allnodes),'obsolete':obsolete});raise SystemExit(0 if all(checks.values()) else 2)
elif x.cmd=='add-page': out(m.mutate(w,{'op':'add_page','name':x.name}))
elif x.cmd=='rename-page': out(m.mutate(w,{'op':'rename_page','page_id':x.page_id,'name':x.name}))
elif x.cmd=='delete-page': out(m.mutate(w,{'op':'delete_page','page_id':x.page_id}))
elif x.cmd=='duplicate-page': out(m.mutate(w,{'op':'duplicate_page','page_id':x.page_id}))
elif x.cmd=='add-text': out(m.mutate(w,{'op':'add_text','page_id':x.page_id,'text':x.text}))
elif x.cmd=='set-node': out(m.mutate(w,{'op':'set_node','page_id':x.page_id,'id':x.node_id,'patch':json.loads(x.patch_json)}))
elif x.cmd=='delete-node': out(m.mutate(w,{'op':'delete_node','page_id':x.page_id,'id':x.node_id}))
elif x.cmd=='duplicate-node': out(m.mutate(w,{'op':'duplicate_node','page_id':x.page_id,'id':x.node_id}))
