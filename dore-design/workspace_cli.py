#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import app_multi as m
def out(v): print(json.dumps(v,ensure_ascii=False,indent=2))
p=argparse.ArgumentParser();sub=p.add_subparsers(dest='cmd',required=True)
sub.add_parser('get');sub.add_parser('verify')
a=sub.add_parser('add-page');a.add_argument('name',nargs='?',default=None)
r=sub.add_parser('rename-page');r.add_argument('page_id');r.add_argument('name')
t=sub.add_parser('add-text');t.add_argument('page_id');t.add_argument('text')
s=sub.add_parser('set-node');s.add_argument('page_id');s.add_argument('node_id');s.add_argument('patch_json')
x=p.parse_args();w=m.workspace()
if x.cmd=='get': out(w)
elif x.cmd=='verify':
 ids=[p['id'] for p in w.get('pages',[])];nodes=[n['id'] for p in w.get('pages',[]) for n in p.get('nodes',[])];checks={'schema':w.get('schema')=='dore.design.workspace.v1','pages':len(ids)>=1,'unique_pages':len(ids)==len(set(ids)),'unique_nodes':len(nodes)==len(set(nodes))};out({'ok':all(checks.values()),'checks':checks,'revision':w.get('revision'),'page_count':len(ids),'node_count':len(nodes)});raise SystemExit(0 if all(checks.values()) else 2)
elif x.cmd=='add-page': out(m.mutate(w,{'op':'add_page','name':x.name}))
elif x.cmd=='rename-page': out(m.mutate(w,{'op':'rename_page','page_id':x.page_id,'name':x.name}))
elif x.cmd=='add-text': out(m.mutate(w,{'op':'add_text','page_id':x.page_id,'text':x.text}))
elif x.cmd=='set-node': out(m.mutate(w,{'op':'set_node','page_id':x.page_id,'id':x.node_id,'patch':json.loads(x.patch_json)}))
