#!/usr/bin/env python3
"""Deterministic Doré Design engine verification."""
import json,tempfile,os,sys
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 os.environ['DORE_DESIGN_DATA']=td
 import app
 d=app.load('westside-watch');r0=d['revision'];hero=next(n for n in d['nodes'] if n['id']=='hero');old=hero['size']
 d=app.mutate(d,{'op':'set','id':'hero','patch':{'size':old-4}});assert d['revision']==r0+1;assert next(n for n in d['nodes'] if n['id']=='hero')['size']==old-4
 d=app.mutate(d,{'op':'token','key':'gold','value':'#B79838'});assert d['tokens']['gold']=='#B79838'
 d=app.mutate(d,{'op':'add','node':{'id':'probe','type':'text','text':'PROBE','x':10,'y':10,'w':100,'size':12}});assert any(n['id']=='probe' for n in d['nodes'])
 d=app.mutate(d,{'op':'delete','id':'probe'});assert not any(n['id']=='probe' for n in d['nodes'])
 before_batch=d['revision'];d=app.batch(d,[{'op':'set','id':'hero','patch':{'x':84,'size':82}},{'op':'token','key':'night','value':'#16324A'}]);assert d['revision']==before_batch+1;assert next(n for n in d['nodes'] if n['id']=='hero')['x']==84
 target_revision=r0+1;d=app.restore('westside-watch',target_revision);assert d['revision']>before_batch;assert next(n for n in d['nodes'] if n['id']=='hero')['size']==old-4
 s=app.svg(d);assert s.startswith('<svg') and 'WATCH FOR' in s
 v=app.verify(d);assert v['ok'] and v['checks']['schema_valid'] and v['checks']['render_nonempty']
 snaps=list((Path(td)/'history').glob('westside-watch.r*.json'));assert len(snaps)>=5
 print(json.dumps({'ok':True,'schema':d['schema'],'revision':d['revision'],'history_snapshots':len(snaps),'svg_bytes':len(s),'render_sha256':v['render_sha256'],'verified':['stable-document-identity','node-crud','token-edit','atomic-batch','revision-history','restore-undo','svg-export','machine-verifier']}))
