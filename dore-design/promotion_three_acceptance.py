#!/usr/bin/env python3
import hashlib,json,os,socket,subprocess,sys,tempfile,time,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(HERE));import promotion_pipeline as pp
def req(base,path,data=None):
 body=json.dumps(data).encode() if data else None;r=urllib.request.Request(base+path,data=body,headers={'Content-Type':'application/json'} if body else {},method='POST' if body else 'GET');return json.loads(urllib.request.urlopen(r,timeout=8).read()) if path.startswith('/api/') else urllib.request.urlopen(r,timeout=8).read()
def visual(url):
 cp=subprocess.run(['node','scripts/page-hash.mjs',url],cwd=HERE/'knowledge-lab/storybook',text=True,capture_output=True,timeout=60);assert cp.returncode==0,cp.stderr;return json.loads(cp.stdout)['sha256']
byte_before=hashlib.sha256(pp.BASELINE.read_bytes()).hexdigest();compression=json.loads(subprocess.check_output([sys.executable,str(HERE/'knowledge_compression.py')],text=True))['compression'];assert compression['corpus_source_count']==44
with tempfile.TemporaryDirectory() as d:
 env=os.environ.copy();env['DORE_DESIGN_DATA']=d+'/design';env['DORE_LOCAL_HOME']=d+'/dore';subprocess.run([sys.executable,'-c','import app_workspace;app_workspace.workspace()'],cwd=HERE,env=env,check=True);subprocess.run([sys.executable,str(HERE/'upgrade_living_fortress_v2.py')],cwd=HERE,env=env,check=True);subprocess.run([sys.executable,str(HERE/'install_homepage_candidates.py')],cwd=HERE,env=env,check=True)
 s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close();env['DORE_DESIGN_PORT']=str(port);server=subprocess.Popen([sys.executable,str(HERE/'app_visual_v2.py')],cwd=HERE,env=env)
 try:
  base=f'http://127.0.0.1:{port}'
  for _ in range(50):
   try:req(base,'/api/health');break
   except Exception:time.sleep(.1)
  visual_before=visual(base+'/editor-canvas?page=homepage');promoted=json.loads(subprocess.check_output([sys.executable,str(HERE/'promote_three_candidates.py')],cwd=ROOT,text=True));assert promoted['ok'];visual_after=visual(base+'/editor-canvas?page=homepage');catalog=req(base,'/api/candidates');assert len(catalog['candidates'])==3
  pages={c['page_id']:req(base,'/editor-canvas?page='+c['page_id']) for c in catalog['candidates']};assert all(b'data-node-id="home-title"' in x for x in pages.values());assert all(len((c.get('knowledge') or {}).get('reference_lineage') or [])>=3 and set((c.get('viewport_evidence') or {}).keys())=={'desktop','mobile'} for c in catalog['candidates'])
  j=req(base,'/api/candidates/judgment',{'candidate_id':catalog['candidates'][0]['id'],'decision':'needs_revision','reason':'Strengthen Westside-specific editorial hierarchy.','signals':['human-visual-judgment']});assert j['ok'] and not j['baseline_262_modified'];assert (Path(env['DORE_DESIGN_DATA'])/'candidate-feedback.jsonl').exists();assert (Path(env['DORE_LOCAL_HOME'])/'knowledge-lab/candidate-feedback.jsonl').exists()
 finally:server.terminate();server.wait(timeout=5)
byte_after=hashlib.sha256(pp.BASELINE.read_bytes()).hexdigest();checks={'three_candidates':len(catalog['candidates'])==3,'knowledge_corpus_44':compression['corpus_source_count']==44,'lineage_patterns_viewports':True,'editable_complete_pages':len(pages)==3,'feedback_roundtrip_to_knowledge_lab':True,'baseline_262_byte_invariant':byte_before==byte_after=='e1eb928a030fa9af1924513d34b73c93afa5afc69878fd93494cb6f9cc8fa034','baseline_262_visual_invariant':visual_before==visual_after};out={'ok':all(checks.values()),'code':'DORE_STORYBOOK_TO_DESIGN_THREE_PROMOTION_PASS','checks':checks,'candidates':[c['id'] for c in catalog['candidates']],'baseline_visual_sha256':visual_before};print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out['ok'] else 1)
