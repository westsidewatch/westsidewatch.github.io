#!/usr/bin/env python3
import json, os, sqlite3, hashlib, uuid, urllib.request, re
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path
from design_memory import DesignEvidence, classify_scope, consolidate, TRUTH_STATES
from penpot_agent import status as penpot_status, run_task as run_penpot_task
from legacy_memory import ensure_schema as ensure_legacy_schema, import_items as import_legacy_items, recall as legacy_recall, context as legacy_context
from self_memory import ensure_schema as ensure_self_schema, upsert_self, add_learning, status as self_status, context as self_context
from learning_planner import plan as learning_plan, validate_gate
from autonomous_learner import status as autonomous_learning_status
ROOT=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore'))
DB=ROOT/'data'/'dore.sqlite3'; HOST=os.environ.get('DORE_LOCAL_HOST','127.0.0.1'); PORT=int(os.environ.get('DORE_LOCAL_PORT','8788'))
MODEL=os.environ.get('DORE_LOCAL_MODEL','gemma4:e4b'); OLLAMA=os.environ.get('OLLAMA_BASE_URL','http://127.0.0.1:11434')
ALLOWED_ORIGINS={'https://westsidewatch.github.io','https://westsidewatch-github-io.pages.dev'}
SYSTEM='''I am Doré, a persistent local research and knowledge agent. The foundation model is a replaceable inference engine, not my identity. Never claim that I am Gemma, Qwen, or another foundation model. If technically relevant, describe the current engine as a component, for example: "我是 Doré。Gemma 4 E4B 是我目前使用的一個本地推理引擎。" Use supplied memory as evidence. Do not invent memories. If memory is insufficient, say so. Keep continuity across conversations through Doré Memory Core.
When design working memory is supplied, distinguish confirmed/current rules from exploration, references, rejected/corrected history and unresolved questions. Never treat a proposal, attempted tool action, created layer/object, or unfinished reference as a verified design. For Westside Watch design work, preserve project context across related design and technical turns.'''
DESIGN_HINTS=('設計','设计','penpot','figma','template','模板','layout','排版','typography','字體','字体','visual','視覺','视觉','ui','ux','design')
PENPOT_ACTION_PATTERNS=(r'在\s*penpot.*(?:設計|设计|做|建立|創建|创建|修改|改)',r'(?:用|使用)\s*penpot',r'penpot.*(?:設計|设计|template|模板|create|build|modify|update)')
def now(): return datetime.now(timezone.utc).isoformat()
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def ensure_design_schema():
 ROOT.joinpath('archive','design-evidence').mkdir(parents=True,exist_ok=True)
 with db() as c:
  ensure_legacy_schema(c)
  ensure_self_schema(c)
  c.execute("CREATE TABLE IF NOT EXISTS dore_context_state (conversation_id TEXT PRIMARY KEY,project_id TEXT NOT NULL,scope TEXT NOT NULL DEFAULT 'candidate',brand_project_status TEXT NOT NULL DEFAULT 'candidate',design_mode INTEGER NOT NULL DEFAULT 0,updated_at TEXT NOT NULL)")
  c.execute("CREATE TABLE IF NOT EXISTS dore_design_evidence (id TEXT PRIMARY KEY,conversation_id TEXT NOT NULL,message_id TEXT,project_id TEXT NOT NULL,scope TEXT NOT NULL,truth_state TEXT NOT NULL,content TEXT NOT NULL,source_ref TEXT,supersedes TEXT,created_at TEXT NOT NULL)")
  c.execute('CREATE INDEX IF NOT EXISTS idx_design_project_time ON dore_design_evidence(project_id,created_at DESC)')
  c.execute('CREATE INDEX IF NOT EXISTS idx_design_truth ON dore_design_evidence(truth_state,created_at DESC)')
def bootstrap_legacy_memory():
 seed_dir=Path(__file__).resolve().parent/'legacy-memory'; total=0
 for seed in sorted(seed_dir.glob('seed-*.json')):
  try: payload=json.loads(seed.read_text(encoding='utf-8')); items=payload.get('items') or []
  except Exception: continue
  with db() as c: total+=len(import_legacy_items(c,ROOT,items))
 return total
def bootstrap_self_memory():
 seed=Path(__file__).resolve().parent/'self-memory'/'seed-v1.json'
 if not seed.is_file(): return 0
 try: payload=json.loads(seed.read_text(encoding='utf-8'))
 except Exception: return 0
 n=0
 with db() as c:
  ensure_self_schema(c)
  for x in payload.get('self') or []: upsert_self(c,x['key'],x['content'],x.get('source_type','legacy_transplant'),x.get('source_ref'),x.get('epistemic_state','inherited')); n+=1
  for x in payload.get('learning') or []: add_learning(c,x['domain'],x['claim'],x.get('stage'),x.get('assessment'),x.get('status','recorded'),x.get('evidence_ref'),x.get('source_type','chatgpt_legacy_memory'),x.get('epistemic_state','inherited')); n+=1
 return n
def self_view():
 with db() as c: return self_status(c)
def self_prompt():
 with db() as c: return self_context(c)
def learning_plan_view():
 path=Path(__file__).resolve().parent/'learning-gates'/'core-v1.json'
 try: payload=json.loads(path.read_text(encoding='utf-8'))
 except Exception as e: return {'ok':False,'error':'learning_gate_load_failed','detail':str(e)}
 try: gates=[validate_gate(x) for x in (payload.get('gates') or [])]
 except ValueError as e: return {'ok':False,'error':'invalid_learning_gate','detail':str(e)}
 with db() as c: state=self_status(c)
 out=learning_plan(state,gates); out['ok']=True; return out
def autonomous_learning_view():
 with db() as c: return autonomous_learning_status(c)
def legacy_view(q):
 with db() as c: return legacy_recall(c,q)
def legacy_status():
 with db() as c:
  ensure_legacy_schema(c); total=c.execute('SELECT COUNT(*) FROM dore_legacy_memory').fetchone()[0]; states={r[0]:r[1] for r in c.execute('SELECT epistemic_state,COUNT(*) FROM dore_legacy_memory GROUP BY epistemic_state')}; subjects={r[0]:r[1] for r in c.execute('SELECT subject,COUNT(*) FROM dore_legacy_memory GROUP BY subject')}
 return {'total':total,'states':states,'subjects':subjects,'source':'chatgpt_legacy_memory'}
def save(cid,role,content,project='dore-global'):
 mid=str(uuid.uuid4()); ts=now(); h=hashlib.sha256(content.encode()).hexdigest(); key=f'conversations/{project}/{cid}/{mid}.json'; p=ROOT/'archive'/key; p.parent.mkdir(parents=True,exist_ok=True)
 payload={'schema':'dore.local-message.v1','id':mid,'conversation_id':cid,'project_id':project,'role':role,'content':content,'created_at':ts,'workers_ai_required':False}; p.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
 with db() as c:
  c.execute('INSERT OR IGNORE INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(cid,project,'local','LOCAL',None,ts,ts)); c.execute('UPDATE dore_conversations SET updated_at=? WHERE id=?',(ts,cid)); c.execute('INSERT OR IGNORE INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(mid,cid,project,'local',role,content,h,key,ts))
 return mid
def context_state(cid,project,text):
 with db() as c:
  row=c.execute('SELECT * FROM dore_context_state WHERE conversation_id=?',(cid,)).fetchone(); inherited=row['scope'] if row else None; scope=classify_scope(text,inherited); design=bool(row['design_mode']) if row else False
  if any(h in text.lower() for h in DESIGN_HINTS): design=True
  status='confirmed' if scope in {'westside_brand','scripture_church_theology'} else 'candidate'; ts=now(); c.execute('INSERT INTO dore_context_state(conversation_id,project_id,scope,brand_project_status,design_mode,updated_at) VALUES(?,?,?,?,?,?) ON CONFLICT(conversation_id) DO UPDATE SET project_id=excluded.project_id,scope=excluded.scope,brand_project_status=excluded.brand_project_status,design_mode=excluded.design_mode,updated_at=excluded.updated_at',(cid,project,scope,status,1 if design else 0,ts)); return {'scope':scope,'brand_project_status':status,'design_mode':design}
def is_penpot_action(text): return any(re.search(p,str(text).lower(),re.I) for p in PENPOT_ACTION_PATTERNS)
def save_design_evidence(cid,mid,project,scope,content,state='observation',source_ref=None,supersedes=None):
 if state not in TRUTH_STATES: raise ValueError('invalid truth state')
 eid=str(uuid.uuid4()); ts=now(); item=DesignEvidence(eid,content,state,project,scope,source_ref,ts,supersedes).validate(); key=f'{project}/{cid}/{eid}.json'; p=ROOT/'archive'/'design-evidence'/key; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(item.json(),ensure_ascii=False),encoding='utf-8')
 with db() as c: c.execute('INSERT INTO dore_design_evidence(id,conversation_id,message_id,project_id,scope,truth_state,content,source_ref,supersedes,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(eid,cid,mid,project,scope,state,content,source_ref,supersedes,ts))
 return eid
def design_view(project,limit=120):
 with db() as c: rows=[dict(x) for x in c.execute('SELECT * FROM dore_design_evidence WHERE project_id=? ORDER BY created_at ASC LIMIT ?',(project,limit))]
 return consolidate([DesignEvidence(r['id'],r['content'],r['truth_state'],r['project_id'],r['scope'],r['source_ref'],r['created_at'],r['supersedes']) for r in rows])
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
  hits=sum(1 for t in terms if t in r['content'].lower()); same=(r['conversation_id']==cid); r['_score']=hits*10+(5 if same else 0)
  if hits or same: scored.append(r)
 return sorted(sorted(scored,key=lambda x:(x['_score'],x['created_at']),reverse=True)[:limit],key=lambda x:x['created_at'])
def ollama(messages):
 data=json.dumps({'model':MODEL,'messages':messages,'stream':False}).encode(); req=urllib.request.Request(OLLAMA+'/api/chat',data=data,headers={'Content-Type':'application/json'}); return json.loads(urllib.request.urlopen(req,timeout=300).read())['message']['content']
def execute_penpot(b, compatibility=False):
 project=str(b.get('project_id') or 'dore-search'); cid=str(b.get('conversation_id') or uuid.uuid4()); action=str(b.get('action') or '').strip(); task=str(b.get('task') or '').strip()
 if compatibility and action=='read_page' and not task: task='Read the currently open Penpot page. Return the actual current page structure and visible composition evidence without modifying anything.'
 if not task:return {'http':400,'body':{'ok':False,'error':'empty_task'}}
 scope=classify_scope(task); brief=design_context(design_view(project))
 try: result=run_penpot_task(task,brief)
 except Exception as e: result={'ok':False,'verified':False,'error':str(e)}
 evstate='verified' if result.get('verified') else ('evidence' if action=='read_page' and result.get('ok') else 'attempt'); save_design_evidence(cid,None,project,scope,json.dumps({'action':action or 'run','task':task,'result':result},ensure_ascii=False),evstate,'penpot-mcp')
 return {'http':200,'body':{'ok':bool(result.get('ok')),'penpot_run':result,'truth_state':evstate,'compatibility_route':compatibility}}
class H(BaseHTTPRequestHandler):
 def cors(self):
  origin=self.headers.get('Origin','')
  if origin in ALLOWED_ORIGINS: self.send_header('Access-Control-Allow-Origin',origin); self.send_header('Vary','Origin')
  self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS'); self.send_header('Access-Control-Allow-Headers','Content-Type, Accept'); self.send_header('Access-Control-Allow-Private-Network','true')
 def sendj(self,x,s=200):
  b=json.dumps(x,ensure_ascii=False).encode(); self.send_response(s); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.cors(); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def do_OPTIONS(self): self.send_response(204); self.cors(); self.send_header('Content-Length','0'); self.end_headers()
 def do_GET(self):
  if self.path=='/legacy-memory/status': return self.sendj({'ok':True,'legacy_memory':legacy_status()})
  if self.path in {'/memory/self/status','/learning/status'}: return self.sendj(self_view())
  if self.path=='/learning/plan': return self.sendj(learning_plan_view())
  if self.path=='/learning/autonomous/status': return self.sendj(autonomous_learning_view())
  if self.path=='/health': return self.sendj({'ok':True,'node':'dore-local','model':MODEL,'memory_core':'sqlite+filesystem','workers_ai_required':False,'search_loopback':True,'recall':'project-wide-v5+self-memory+learning-ledger+autonomous-learning','design_working_memory':'d1-d4-bridge-v2','penpot_agent':'mcp+local-vlm','penpot_routes':['/penpot','/design/penpot/status','/design/penpot/run']})
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
  if self.path=='/design/view': return self.sendj({'ok':True,'project_id':str(b.get('project_id') or 'dore-global'),'design_view':design_view(str(b.get('project_id') or 'dore-global'))})
  if self.path=='/design/penpot/status': return self.sendj(penpot_status())
  if self.path in {'/design/penpot/run','/penpot'}:
   out=execute_penpot(b,self.path=='/penpot'); return self.sendj(out['body'],out['http'])
  if self.path!='/chat': return self.sendj({'ok':False,'error':'not_found'},404)
  text=str(b.get('message','')).strip(); cid=str(b.get('conversation_id') or uuid.uuid4()); project=str(b.get('project_id') or 'dore-global')
  if not text:return self.sendj({'ok':False,'error':'empty_message'},400)
  state=context_state(cid,project,text); mid=save(cid,'user',text,project)
  if state['design_mode'] and is_penpot_action(text):
   out=execute_penpot({'project_id':project,'conversation_id':cid,'task':text}); reply=json.dumps(out['body'],ensure_ascii=False); save(cid,'assistant',reply,project); return self.sendj({'ok':bool(out['body'].get('ok')),'conversation_id':cid,'reply':reply,'mode':'design+penpot','penpot':out['body']})
  memories=recall(project,cid,text); legacy=legacy_context(legacy_view(text)); selfmem=self_prompt(); design=design_context(design_view(project)) if state['design_mode'] else 'Design mode inactive.'
  hist='\n'.join(f"{x['role']}: {x['content']}" for x in memories[-14:]); prompt=f"{SYSTEM}\n\nDORÉ SELF / LEARNING MEMORY:\n{selfmem}\n\nLEGACY CHATGPT MEMORY (inherited; not independently learned):\n{legacy}\n\nDESIGN WORKING MEMORY:\n{design}\n\nRECALLED DORÉ MEMORY:\n{hist}\n\nCurrent user message:\n{text}"
  try: reply=ollama([{'role':'system','content':SYSTEM},{'role':'user','content':prompt}])
  except Exception as e:return self.sendj({'ok':False,'error':'ollama_failed','detail':str(e)},502)
  save(cid,'assistant',reply,project); return self.sendj({'ok':True,'conversation_id':cid,'reply':reply,'memory_hits':len(memories),'legacy_memory':True,'self_memory':True,'design_mode':state['design_mode'],'scope':state['scope']})
 def log_message(self,*args): pass
def main():
 ROOT.joinpath('data').mkdir(parents=True,exist_ok=True); ROOT.joinpath('archive','conversations').mkdir(parents=True,exist_ok=True); ensure_design_schema(); legacy_count=bootstrap_legacy_memory(); self_count=bootstrap_self_memory(); print(f'Doré Local http://{HOST}:{PORT} model={MODEL} legacy_seeded={legacy_count} self_seeded={self_count}',flush=True); ThreadingHTTPServer((HOST,PORT),H).serve_forever()
if __name__=='__main__': main()
