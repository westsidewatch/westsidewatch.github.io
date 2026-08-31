#!/usr/bin/env python3
"""Doré Design CLI — stable machine control surface over the structured document engine."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import app

def out(v):print(json.dumps(v,ensure_ascii=False,indent=2))
def main():
 p=argparse.ArgumentParser(prog='dore-design');p.add_argument('--document',default='westside-watch');sub=p.add_subparsers(dest='cmd',required=True)
 sub.add_parser('get');sub.add_parser('verify');sub.add_parser('history');sub.add_parser('export-svg')
 s=sub.add_parser('set');s.add_argument('id');s.add_argument('patch_json')
 t=sub.add_parser('token');t.add_argument('key');t.add_argument('value')
 a=sub.add_parser('add');a.add_argument('node_json')
 d=sub.add_parser('delete');d.add_argument('id')
 b=sub.add_parser('batch');b.add_argument('ops_json')
 r=sub.add_parser('restore');r.add_argument('revision',type=int)
 x=p.parse_args();doc=x.document
 try:
  if x.cmd=='get':out(app.load(doc));return 0
  if x.cmd=='verify':v=app.verify(app.load(doc));out(v);return 0 if v['ok'] else 2
  if x.cmd=='history':out(app.history(doc));return 0
  if x.cmd=='export-svg':
   s=app.svg(app.load(doc));dest=app.EXPORTS/f'{doc}.svg';app.atomic_write(dest,s);out({'ok':True,'path':str(dest),'bytes':len(s)});return 0
  if x.cmd=='set':res=app.mutate(app.load(doc),{'op':'set','id':x.id,'patch':json.loads(x.patch_json)})
  elif x.cmd=='token':res=app.mutate(app.load(doc),{'op':'token','key':x.key,'value':x.value})
  elif x.cmd=='add':res=app.mutate(app.load(doc),{'op':'add','node':json.loads(x.node_json)})
  elif x.cmd=='delete':res=app.mutate(app.load(doc),{'op':'delete','id':x.id})
  elif x.cmd=='batch':res=app.batch(app.load(doc),json.loads(x.ops_json))
  elif x.cmd=='restore':res=app.restore(doc,x.revision)
  out({'ok':True,'document_id':doc,'revision':res['revision']});return 0
 except Exception as e:out({'ok':False,'error':type(e).__name__+': '+str(e)});return 1
if __name__=='__main__':raise SystemExit(main())
