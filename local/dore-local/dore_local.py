#!/usr/bin/env python3
import json, os, sqlite3, hashlib, uuid, urllib.request, re
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore'))
DB=ROOT/'data'/'dore.sqlite3'; HOST=os.environ.get('DORE_LOCAL_HOST','127.0.0.1'); PORT=int(os.environ.get('DORE_LOCAL_PORT','8788'))
MODEL=os.environ.get('DORE_LOCAL_MODEL','qwen3:8b'); OLLAMA=os.environ.get('OLLAMA_BASE_URL','http://127.0.0.1:11434')
ALLOWED_ORIGINS={'https://westsidewatch.github.io','https://westsidewatch-github-io.pages.dev'}
SYSTEM='''You are Doré, a persistent local research and knowledge agent. Your identity is independent of the language model serving this response. Use supplied memory as evidence. Do not invent memories. If memory is insufficient, say so. Keep continuity across conversations through Doré Memory Core.'''
def now(): return datetime.now(timezone.utc).isoformat()
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def save(cid,role,content,project='dore-global'):
 mid=str(uuid.uuid4()); ts=now(); h=hashlib.sha256(content.encode()).hexdigest(); key=f'conversations/{project}/{cid}/{mid}.json'; p=ROOT/'archive'/key; p.parent.mkdir(parents=True,exist_ok=True)
 payload={'schema':'dore.local-message.v1','id':mid,'conversation_id':cid,'project_id':project,'role':role,'content':content,'created_at':ts,'workers_ai_required':False}; p.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
 with db() as c:
  c.execute('INSERT OR IGNORE INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(cid,project,'local','LOCAL',None,ts,ts)); c.execute('UPDATE dore_conversations SET updated_at=? WHERE id=?',(ts,cid)); c.execute('INSERT OR IGNORE INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(mid,cid,project,'local',role,content,h,key,ts))
 return mid
def query_terms(q):
 # Keep Chinese runs as overlapping 2-4 character terms and Latin words as tokens.
 s=str(q).lower(); terms=set(re.findall(r'[a-z0-9_:-]{2,}',s))
 for run in re.findall(r'[\u3400-\u9fff]+',s):
  if len(run)<=4: terms.add(run)
  for n in (2,3,4):
   for i in range(max(0,len(run)-n+1)): terms.add(run[i:i+n])
 return terms
def recall(project,cid,q,limit=18):
 terms=query_terms(q)
 with db() as c:
  # Search the complete project history: old but relevant memory must not disappear merely because new chat was added.
  rows=[dict(x) for x in c.execute('SELECT * FROM dore_messages WHERE project_id=? ORDER BY created_at DESC',(project,))]
 scored=[]
 for r in rows:
  content=r['content'].lower(); hits=sum(1 for t in terms if t in content)
  same=(r['conversation_id']==cid)
  # Current conversation gets continuity priority, while cross-conversation memories remain retrievable by relevance.
  r['_score']=hits*10+(5 if same else 0)
  if hits or same: scored.append(r)
 ranked=sorted(scored,key=lambda x:(x['_score'],x['created_at']),reverse=True)
 # Preserve chronological order in the prompt after relevance selection so the model sees coherent history.
 return sorted(ranked[:limit],key=lambda x:x['created_at'])
def ollama(messages):
 data=json.dumps({'model':MODEL,'messages':messages,'stream':False}).encode(); req=urllib.request.Request(OLLAMA+'/api/chat',data=data,headers={'Content-Type':'application/json'}); return json.loads(urllib.request.urlopen(req,timeout=300).read())['message']['content']
class H(BaseHTTPRequestHandler):
 def cors(self):
  origin=self.headers.get('Origin','')
  if origin in ALLOWED_ORIGINS:
   self.send_header('Access-Control-Allow-Origin',origin)
   self.send_header('Vary','Origin')
  self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
  self.send_header('Access-Control-Allow-Headers','Content-Type, Accept')
  self.send_header('Access-Control-Allow-Private-Network','true')
 def sendj(self,x,s=200):
  b=json.dumps(x,ensure_ascii=False).encode(); self.send_response(s); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.cors(); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
 def do_OPTIONS(self):
  self.send_response(204); self.cors(); self.send_header('Content-Length','0'); self.end_headers()
 def do_GET(self):
  if self.path=='/health': return self.sendj({'ok':True,'node':'dore-local','model':MODEL,'memory_core':'sqlite+filesystem','workers_ai_required':False,'search_loopback':True,'recall':'project-wide-v2'})
  self.sendj({'ok':False,'error':'not_found'},404)
 def do_POST(self):
  try: n=int(self.headers.get('Content-Length','0')); b=json.loads(self.rfile.read(n) or b'{}')
  except: return self.sendj({'ok':False,'error':'invalid_json'},400)
  if self.path!='/chat': return self.sendj({'ok':False,'error':'not_found'},404)
  text=str(b.get('message','')).strip(); cid=str(b.get('conversation_id') or uuid.uuid4()); project=str(b.get('project_id') or 'dore-global')
  if not text:return self.sendj({'ok':False,'error':'empty_message'},400)
  save(cid,'user',text,project); memories=recall(project,cid,text); context='\n'.join(f"[{m['created_at']}] {m['role']}: {m['content']}" for m in memories)
  try: answer=ollama([{'role':'system','content':SYSTEM+'\n\nDoré memory:\n'+context},{'role':'user','content':text}])
  except Exception as e:return self.sendj({'ok':False,'error':'local_model_failed','detail':str(e),'workers_ai_used':False},502)
  save(cid,'assistant',answer,project); return self.sendj({'ok':True,'conversation_id':cid,'project_id':project,'answer':answer,'memory_hits':len(memories),'model':MODEL,'provider':{'name':'dore-local','model':MODEL},'workers_ai_used':False,'recall':'project-wide-v2'})
 def log_message(self,*a): pass
if __name__=='__main__':
 print(f'Doré Local API http://{HOST}:{PORT} model={MODEL} workers_ai_required=false recall=project-wide-v2',flush=True); ThreadingHTTPServer((HOST,PORT),H).serve_forever()
