#!/usr/bin/env python3
import tempfile,os,sys,json
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 os.environ['DORE_DESIGN_DATA']=td
 sys.path.insert(0,str(Path(__file__).resolve().parent));import app_workspace as m
 w=m.workspace();assert len(w['pages'])==3 and m.verify(w)['ok'];r0=w['revision']
 w=m.mutate(w,{'op':'add_text','page_id':'contents','id':'probe','text':'PROBE'});assert any(n['id']=='probe' for n in m.page(w,'contents')['nodes'])
 w=m.mutate(w,{'op':'set_node','page_id':'contents','id':'probe','patch':{'x':123,'text':'EDITED'}});assert next(n for n in m.page(w,'contents')['nodes'] if n['id']=='probe')['x']==123
 w=m.mutate(w,{'op':'duplicate_node','page_id':'contents','id':'probe'});assert len([n for n in m.page(w,'contents')['nodes'] if n['id'].startswith('probe')])==2
 w=m.mutate(w,{'op':'delete_node','page_id':'contents','id':'probe'});assert not any(n['id']=='probe' for n in m.page(w,'contents')['nodes'])
 w=m.mutate(w,{'op':'add_text','page_id':'contents','id':'section-10','text':'10 · 安提阿'});assert not any(n['id']=='section-10' for n in m.page(w,'contents')['nodes'])
 w=m.mutate(w,{'op':'add_text','page_id':'contents','id':'history-word','text':'Antioch may still appear in legitimate article text'});assert any(n['id']=='history-word' for n in m.page(w,'contents')['nodes'])
 w=m.mutate(w,{'op':'duplicate_page','page_id':'contents'});copyid=w['pages'][-1]['id'];w=m.mutate(w,{'op':'delete_page','page_id':copyid});assert not m.page(w,copyid)
 w=m.mutate(w,{'op':'token','key':'gold','value':'#B79838'});assert w['tokens']['gold']=='#B79838'
 w=m.mutate(w,{'op':'set_canvas','page_id':'contents','patch':{'w':1180,'h':900}});assert m.page(w,'contents')['canvas']['w']==1180
 svg=m.page_svg(w,'cover');assert svg.startswith('<svg') and 'WATCH FOR' in svg
 assert len(m.history())>1;before=w['revision'];w=m.undo();assert w['revision']==before+1
 v=m.verify(w);assert v['ok'] and v['page_count']>=2
 print(json.dumps({'ok':True,'revision_start':r0,'revision_end':w['revision'],'page_count':v['page_count'],'verified':['multi-page','node-crud','page-crud','human-delete','tokens','canvas','history','undo','svg-export','machine-verify','legacy-structure-migration']}))
