#!/usr/bin/env python3
"""End-to-end HTTP verification for Doré Design."""
import json,os,socket,subprocess,sys,tempfile,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def req(url,data=None):
 headers={};body=None
 if data is not None:body=json.dumps(data).encode();headers['Content-Type']='application/json'
 r=urllib.request.Request(url,data=body,headers=headers,method='POST' if data is not None else 'GET')
 with urllib.request.urlopen(r,timeout=3) as x:return x.status,x.headers.get_content_type(),x.read()
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
with tempfile.TemporaryDirectory() as td:
 env=os.environ.copy();env['DORE_DESIGN_DATA']=td;env['DORE_DESIGN_PORT']=str(port)
 p=subprocess.Popen([sys.executable,str(ROOT/'app.py')],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try:
  base=f'http://127.0.0.1:{port}'
  for _ in range(30):
   try:code,_,raw=req(base+'/api/health');break
   except Exception:time.sleep(.1)
  else:raise RuntimeError('service_not_ready')
  health=json.loads(raw);assert code==200 and health['ok']
  code,typ,html=req(base+'/');assert code==200 and typ=='text/html' and b'DORE DESIGN 0.5' in html
  _,_,raw=req(base+'/api/document/westside-watch');d0=json.loads(raw);r0=d0['revision']
  _,_,raw=req(base+'/api/document/westside-watch/mutate',{'op':'set','id':'hero','patch':{'x':91}});d1=json.loads(raw)['document'];assert d1['revision']==r0+1 and next(n for n in d1['nodes'] if n['id']=='hero')['x']==91
  _,_,raw=req(base+'/api/document/westside-watch/batch',{'ops':[{'op':'set','id':'hero','patch':{'size':81}},{'op':'token','key':'gold','value':'#B79838'}]});d2=json.loads(raw)['document'];assert d2['revision']==r0+2
  _,typ,svg=req(base+'/api/document/westside-watch/export.svg');assert typ=='image/svg+xml' and b'<svg' in svg and b'WATCH FOR' in svg
  _,_,raw=req(base+'/api/document/westside-watch/verify');v=json.loads(raw);assert v['ok']
  _,_,raw=req(base+'/api/document/westside-watch/history');h=json.loads(raw);assert len(h)>=3
  print(json.dumps({'ok':True,'service':'dore-design','version':'0.5','http_workbench':True,'revision_before':r0,'revision_after':d2['revision'],'history_entries':len(h),'svg_bytes':len(svg),'verification':v},ensure_ascii=False))
 finally:
  p.terminate()
  try:p.wait(timeout=3)
  except subprocess.TimeoutExpired:p.kill()
