#!/usr/bin/env python3
import tempfile,os,sys,json
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 os.environ['DORE_DESIGN_DATA']=td
 sys.path.insert(0,str(Path(__file__).resolve().parent))
 import app_multi as m
 w=m.workspace();assert len(w['pages'])==3
 w=m.mutate(w,{'op':'add_text','page_id':'contents','id':'probe','text':'PROBE'});assert any(n['id']=='probe' for n in m.page(w,'contents')['nodes'])
 w=m.mutate(w,{'op':'set_node','page_id':'contents','id':'probe','patch':{'x':123,'text':'EDITED'}});assert next(n for n in m.page(w,'contents')['nodes'] if n['id']=='probe')['x']==123
 w=m.mutate(w,{'op':'duplicate_node','page_id':'contents','id':'probe'});assert len(m.page(w,'contents')['nodes'])==2
 w=m.mutate(w,{'op':'delete_node','page_id':'contents','id':'probe'});assert not any(n['id']=='probe' for n in m.page(w,'contents')['nodes'])
 w=m.mutate(w,{'op':'add_text','page_id':'contents','id':'old','text':'安提阿 ANTIOCH'});assert not any('安提阿' in json.dumps(n,ensure_ascii=False) for n in m.page(w,'contents')['nodes'])
 w=m.mutate(w,{'op':'duplicate_page','page_id':'contents'});copyid=w['pages'][-1]['id'];w=m.mutate(w,{'op':'delete_page','page_id':copyid});assert not m.page(w,copyid)
 print(json.dumps({'ok':True,'page_count':len(w['pages']),'revision':w['revision'],'verified':['multi-page','node-create','node-edit','node-duplicate','node-delete','page-duplicate','page-delete','obsolete-content-guard']}))
