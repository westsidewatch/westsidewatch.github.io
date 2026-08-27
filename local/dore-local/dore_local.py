#!/usr/bin/env python3
import json, os, sqlite3, hashlib, uuid, urllib.request, re
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path
from design_memory import DesignEvidence, classify_scope, consolidate, TRUTH_STATES
from penpot_agent import status as penpot_status, run_task as run_penpot_task
ROOT=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore'))
DB=ROOT/'data'/'dore.sqlite3'; HOST=os.environ.get('DORE_LOCAL_HOST','127.0.0.1'); PORT=int(os.environ.get('DORE_LOCAL_PORT','8788'))
MODEL=os.environ.get('DORE_LOCAL_MODEL','qwen3:8b'); OLLAMA=os.environ.get('OLLAMA_BASE_URL','http://127.0.0.1:11434')
ALLOWED_ORIGINS={'https://westsidewatch.github.io','https://westsidewatch-github-io.pages.dev'}
SYSTEM='''You are Doré, a persistent local research and knowledge agent. Your identity is independent of the language model serving this response. Use supplied memory as evidence. Do not invent memories. If memory is insufficient, say so. Keep continuity across conversations through Doré Memory Core.
When design working memory is supplied, distinguish confirmed/current rules from exploration, references, rejected/corrected history and unresolved questions. Never treat a proposal, attempted tool action, created layer/object, or unfinished reference as a verified design. For Westside Watch design work, preserve project context across related design and technical turns.'''
DESIGN_HINTS=('設計','设计','penpot','figma','template','模板','layout','排版','typography','字體','字体','visual','視覺','视觉','ui','ux','design')
PENPOT_ACTION_PATTERNS=(r'在\s*penpot.*(?:設計|设计|做|建立|創建|创建|修改|改)',r'(?:用|使用)\s*penpot',r'penpot.*(?:設計|设计|template|模板|create|build|modify|update)')
def now(): return datetime.now(timezone.utc).isoformat()
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def ensure_design_schema():
 ROOT.joinpath('archive','design-evidence').mkdir(parents=True,exist_ok=True)
 with db() as c:
  c.execute("CREATE TABLE IF NOT EXISTS dore_context_state (conversation_id TEXT PRIMARY KEY,project_id TEXT NOT NULL,scope TEXT NOT NULL DEFAULT 'candidate',brand_project_status TEXT NOT NULL DEFAULT 'candidate',design_mode INTEGER NOT NULL DEFAULT 0,updated_at TEXT NOT NULL)")
  c.execute("CREATE TABLE IF NOT EXISTS dore_design_evidence (id TEXT PRIMARY KEY,conversation_id TEXT NOT NULL,message_id TEXT,project_id TEXT NOT NULL,scope TEXT NOT NULL,truth_state TEXT NOT NULL,content TEXT NOT NULL,source_ref TEXT,supersedes TEXT,created_at TEXT NOT NULL)")
  c.execute('CREATE INDEX IF NOT EXISTS idx_design_project_time ON dore_design_evidence(project_id,created_at DESC)')
  c.execute('CREATE INDEX IF NOT EXISTS idx_design_truth ON dore_design_evidence(truth_state,created_at DESC)')
def save(cid,role,content,project='dore-global'):
 mid=str(uuid.uuid4()); ts=now(); h=hashlib.sha256(content.encode()).hexdigest(); key=f'conversations/{project}/{cid}/{mid}.json'; p=ROOT/'archive'/key; p.parent.mkdir(parents=True,exist_ok=True)
 payload={'schema':'dore.local-message.v1','id':mid,'conversation_id':cid,'project_id':project,'role':role,'content':content,'created_at':ts,'workers_ai_required':False}; p.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
 with db() as c:
  c.execute('INSERT OR IGNORE INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(cid,project,'local','LOCAL',None,ts,ts)); c.execute('UPDATE dore_conversations SET updated_at=? WHERE id=?',(ts,cid)); c.execute('INSERT OR IGNORE INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(mid,cid,project,'local',role,content,h,key,ts))
 return mid
def context_state(cid,project,text):
 with db() as c:
  row=c.execute('SELECT * FROM dore_context_state WHERE conversation_id=?',(cid,)).fetchone()
  inherited=row['scope'] if row else None; scope=classify_scope(text,inherited)
  design=bool(row['design_mode']) if row else False
  if any(h in text.lower() for h in DESIGN_HINTS): design=True
  status='confirmed' if scope in {'westside_brand','scripture_church_theology'} else 'candidate'
  ts=now(); c.execute('INSERT INTO dore_context_state(conversation_id,project_id,scope,brand_project_status,design_mode,updated_at) VALUES(?,?,?,?,?,?) ON CONFLICT(conversation_id) DO UPDATE SET project_id=excluded.project_id,scope=excluded.scope,brand_project_status=excluded.brand_project_status,design_mode=excluded.design_mode,updated_at=excluded.updated_at',(cid,project,scope,status,1 if design else 0,ts))
 return {'scope':scope,'brand_project_status':status,'design_mode':design}
def is_penpot_action(text):
 s=str(text).lower(); return any(re.search(p,s,re.I) for p in PENPOT_ACTION_PATTERNS)
def save_design_evidence(cid,mid,project,scope,content,state='observation',source_ref=None,supersedes=None):
 if state not in TRUTH_STATES: raise ValueError('invalid truth state')
 eid=str(uuid.uuid4()); ts=now(); item=DesignEvidence(eid,content,state,project,scope,source_ref,ts,supersedes).validate(); key=f'{project}/{cid}/{eid}.json'; p=ROOT/'archive'/'design-evidence'/key; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(item.json(),ensure_ascii=False),encoding='utf-8')
 with db() as c: c.execute('INSERT INTO dore_design_evidence(id,conversation_id,message_id,project_id,scope,truth_state,content,source_ref,supersedes,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(eid,cid,mid,project,scope,state,content,source_ref,supersedes,ts))
 return eid
def design_view(project,limit=120):
 with db() as c: rows=[dict(x) for x in c.execute('SELECT * FROM dore_design_evidence WHERE project_id=? ORDER BY created_at ASC LIMIT ?',(project,limit))]
 items=[DesignEvidence(r['id'],r['content'],r['truth_state'],r['project_id'],r['scope'],r['source_ref'],r['created_at'],r['supersedes']) for r in rows]
 return consolidate(items)
def design_context(view):
 def lines(key): return '\n'.join(f"- [{x['truth_state']}] {x['content']}" for x in view[key][-20:]) or '- none'
 return 'CURRENT / CONFIRMED:\n'+lines('current')+'\n\nACTIVE EXPLORATION:\n'+lines('exploration')+'\n\nREFERENCES / EVIDENCE:\n'+lines('references')+'\n\nREJECTED / CORRECTED HISTORY:\n'+lines('historical')+'\n\nUNRESOLVED:\n'+lines('unresolved')
def query_terms(q):
 s=str(q).lower(); terms=set(re.findall(r'[a-z0-9_:-]{2,}',s))
 for run in re.findall(r'[\u3400-\u9fff]+',s):
  if len(run)<=4: terms.add(run)
  for n in (2,3,4):
   for i in range(max(0,len(run)-n+1)): terms.add(run[i:i+n])
 return terms
def recall(project,cid,q,limit=18):
 terms=query_terms(q)
 with db() as c: rows=[dict(x) for x in c.execute('SELECT * FROM dore_messages WHERE project_id=? ORDER BY created_at DESC',(project,))]
 scored=[]
 for r in rows:
  content=r['content'].lower(); hits=sum(1 for t in terms if t in content); same=(r['conversation_id']==cid); r['_score']=hits*10+(5 if same else 0)
  if hits or same: scored.append(r)
 ranked=sorted(scored,key=lambda x:(x['_score'],x['created_at']),reverse=True); return sorted(ranked[:limit],key=lambda x:x['created_at'])
def ollama(messages):
 data=json.dumps({'model':MODEL,'messages':messages,'stream':False}).encode(); req=urllib.request.Request(OLLAMA+'/api/chat',data=data,headers={'Content-Type':'application/json'}); return json.loads(urllib.request.urlopen(req,timeout=300).read())['message']['content']
class H(BaseHTTPRequestHandler):
 def cors(self):
  origin=self.headers.get('Origin','')
  if origin in ALLOWED_ORIGINS: self.send_header('Access-Control-Allow-Origin',origin); self.send_header('Vary','Origin')
  self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS'); self.send_header('Access-Control-Allow-Headers','Content-Type, Accept'); self.send_header('Access-Control-Allow-Private-Network','true')
 def sendj(self,x,s=200):
  b=json.dumps(x,ensure_ascii=False).encode(); self.send_response(s); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.cors(); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def do_OPTIONS(self): self.send_response(204); self.cors(); self.send_header('Content-Length','0'); self.end_headers()
 def do_GET(self):
  if self.path=='/health': return self.sendj({'ok':True,'node':'dore-local','model':MODEL,'memory_core':'sqlite+filesystem','workers_ai_required':False,'search_loopback':True,'recall':'project-wide-v2','design_working_memory':'d1-d4-bridge-v1','penpot_agent':'mcp+local-vlm'})
  self.sendj({'ok':False,'error':'not_found'},404)
 def do_POST(self):
  try: n=int(self.headers.get('Content-Length','0')); b=json.loads(self.rfile.read(n) or b'{}')
  except: return self.sendj({'ok':False,'error':'invalid_json'},400)
  if self.path=='/design/evidence':
   cid=str(b.get('conversation_id') or uuid.uuid4()); project=str(b.get('project_id') or 'dore-global'); text=str(b.get('content','')).strip(); state=str(b.get('truth_state') or 'observation'); scope=str(b.get('scope') or classify_scope(text))
   if not text:return self.sendj({'ok':False,'error':'empty_content'},400)
   try:eid=save_design_evidence(cid,None,project,scope,text,state,b.get('source_ref'),b.get('supersedes'))
   except ValueError as e:return self.sendj({'ok':False,'error':str(e)},400)
   return self.sendj({'ok':True,'evidence_id':eid,'design_view':design_view(project)})
  if self.path=='/design/view':
   project=str(b.get('project_id') or 'dore-global'); return self.sendj({'ok':True,'project_id':project,'design_view':design_view(project)})
  if self.path=='/design/penpot/status': return self.sendj(penpot_status())
  if self.path=='/design/penpot/run':
   project=str(b.get('project_id') or 'dore-search'); cid=str(b.get('conversation_id') or uuid.uuid4()); task=str(b.get('task') or '').strip()
   if not task:return self.sendj({'ok':False,'error':'empty_task'},400)
   scope=classify_scope(task); brief=design_context(design_view(project))
   try: result=run_penpot_task(task,brief)
   except Exception as e: result={'ok':False,'verified':False,'error':str(e)}
   evstate='verified' if result.get('verified') else 'attempt'; save_design_evidence(cid,None,project,scope,json.dumps({'task':task,'result':result},ensure_ascii=False),evstate,'penpot-mcp')
   return self.sendj({'ok':True,'penpot_run':result,'truth_state':evstate})
  if self.path!='/chat': return self.sendj({'ok':False,'error':'not_found'},404)
  text=str(b.get('message','')).strip(); cid=str(b.get('conversation_id') or uuid.uuid4()); project=str(b.get('project_id') or 'dore-global')
  if not text:return self.sendj({'ok':False,'error':'empty_message'},400)
  state=context_state(cid,project,text); mid=save(cid,'user',text,project)
  if state['design_mode']: save_design_evidence(cid,mid,project,state['scope'],text,'observation','dore-search')
  memories=recall(project,cid,text); context='\n'.join(f"[{m['created_at']}] {m['role']}: {m['content']}" for m in memories); dv=design_view(project) if state['design_mode'] else None
  if state['design_mode'] and is_penpot_action(text):
   brief=design_context(dv)
   try: result=run_penpot_task(text,brief)
   except Exception as e: result={'ok':False,'verified':False,'error':str(e)}
   evstate='verified' if result.get('verified') else 'attempt'; save_design_evidence(cid,mid,project,state['scope'],json.dumps({'task':text,'result':result},ensure_ascii=False),evstate,'penpot-mcp')
   if result.get('verified'): answer=result.get('answer') or 'Penpot 設計已完成並通過實際畫面驗證。'
   else: answer='Penpot 設計尚未通過視覺驗證。'+((' 阻塞：'+str(result.get('error'))) if result.get('error') else ' 我沒有把工具執行或圖層建立當作完成。')
   save(cid,'assistant',answer,project); return self.sendj({'ok':True,'conversation_id':cid,'project_id':project,'answer':answer,'provider':{'name':'dore-local','model':MODEL},'workers_ai_used':False,'context_state':state,'design_working_memory':'d1-d4-bridge-v1','penpot_run':result,'truth_state':evstate})
  sys=SYSTEM+'\n\nDoré memory:\n'+context
  if dv is not None: sys+='\n\nDoré Design Working Memory:\n'+design_context(dv)
  try: answer=ollama([{'role':'system','content':sys},{'role':'user','content':text}])
  except Exception as e:return self.sendj({'ok':False,'error':'local_model_failed','detail':str(e),'workers_ai_used':False},502)
  save(cid,'assistant',answer,project); return self.sendj({'ok':True,'conversation_id':cid,'project_id':project,'answer':answer,'memory_hits':len(memories),'model':MODEL,'provider':{'name':'dore-local','model':MODEL},'workers_ai_used':False,'recall':'project-wide-v2','context_state':state,'design_working_memory':'d1-d4-bridge-v1'})
 def log_message(self,*a): pass
if __name__=='__main__':
 ensure_design_schema(); print(f'Doré Local API http://{HOST}:{PORT} model={MODEL} workers_ai_required=false recall=project-wide-v2 design=d1-d4-bridge-v1',flush=True); ThreadingHTTPServer((HOST,PORT),H).serve_forever()
