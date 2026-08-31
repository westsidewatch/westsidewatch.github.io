#!/usr/bin/env python3
"""Deterministic Build 002 verification without browser or external dependencies."""
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
 s=app.svg(d);assert s.startswith('<svg') and 'WATCH FOR' in s and '#B79838' in s
 snaps=list((Path(td)/'history').glob('westside-watch.r*.json'));assert len(snaps)==4
 print(json.dumps({'ok':True,'schema':d['schema'],'revision':d['revision'],'history_snapshots':len(snaps),'svg_bytes':len(s),'verified':['same-node-mutation','token-mutation','add-delete','revision-history','svg-export']}))
