#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name('dore_local.py'); s=p.read_text(encoding='utf-8')
legacy="from legacy_memory import ensure_schema as ensure_legacy_schema, import_items as import_legacy_items, recall as legacy_recall, context as legacy_context\n"
selfimp="from self_memory import ensure_schema as ensure_self_schema, upsert_self, add_learning, status as self_status, context as self_context\n"
while s.count(legacy)>1: s=s.replace(legacy+legacy,legacy)
if selfimp not in s: s=s.replace(legacy,legacy+selfimp,1)
# normalize schema calls
while '  ensure_legacy_schema(c)\n  ensure_legacy_schema(c)\n' in s: s=s.replace('  ensure_legacy_schema(c)\n  ensure_legacy_schema(c)\n','  ensure_legacy_schema(c)\n')
if '  ensure_self_schema(c)\n' not in s.split('def bootstrap_legacy_memory():',1)[0]: s=s.replace('  ensure_legacy_schema(c)\n','  ensure_legacy_schema(c)\n  ensure_self_schema(c)\n',1)
if 'def bootstrap_self_memory():' not in s:
 anchor='def legacy_view(q):\n'; block="""def bootstrap_self_memory():
 seed=Path(__file__).resolve().parent/'self-memory'/'seed-v1.json'
 if not seed.is_file(): return 0
 try: payload=json.loads(seed.read_text(encoding='utf-8'))
 except Exception: return 0
 n=0
 with db() as c:
  ensure_self_schema(c)
  for x in payload.get('self') or []:
   upsert_self(c,x['key'],x['content'],x.get('source_type','legacy_transplant'),x.get('source_ref'),x.get('epistemic_state','inherited')); n+=1
  for x in payload.get('learning') or []:
   add_learning(c,x['domain'],x['claim'],x.get('stage'),x.get('assessment'),x.get('status','recorded'),x.get('evidence_ref'),x.get('source_type','chatgpt_legacy_memory'),x.get('epistemic_state','inherited')); n+=1
 return n
def self_view():
 with db() as c: return self_status(c)
def self_prompt():
 with db() as c: return self_context(c)
"""; s=s.replace(anchor,block+anchor,1)
route="  if self.path=='/legacy-memory/status': return self.sendj({'ok':True,'legacy_memory':legacy_status()})\n"
while s.count(route)>1: s=s.replace(route+route,route)
if "self.path in {'/memory/self/status','/learning/status'}" not in s: s=s.replace(route,route+"  if self.path in {'/memory/self/status','/learning/status'}: return self.sendj(self_view())\n",1)
old="sys=SYSTEM+'\\n\\nDoré conversational memory:\\n'+context+'\\n\\nDoré inherited legacy memory (usable, provenance-labelled; inherited is not the same as externally verified):\\n'+legacy_context(inherited)"
new="sys=SYSTEM+'\\n\\nDoré durable self memory and learning ledger:\\n'+self_prompt()+'\\n\\nDoré conversational memory:\\n'+context+'\\n\\nDoré inherited legacy memory (usable, provenance-labelled; inherited is not the same as externally verified):\\n'+legacy_context(inherited)"
if 'Doré durable self memory and learning ledger:' not in s: s=s.replace(old,new,1)
# normalize startup and stale response markers
if "if __name__=='__main__':" in s:
 head,tail=s.split("if __name__=='__main__':",1)
 lines=tail.splitlines(); lines[1]=" ensure_design_schema(); bootstrap_legacy_memory(); bootstrap_self_memory(); print(f'Doré Local API http://{HOST}:{PORT} model={MODEL} workers_ai_required=false recall=project-wide-v3+self-memory+learning-ledger design=d1-d4-bridge-v2',flush=True); ThreadingHTTPServer((HOST,PORT),H).serve_forever()"
 tail='\n'.join(lines[:2])+('\n' if len(lines)>2 else '')
 s=head+"if __name__=='__main__':"+tail
while "'legacy_memory_hits':len(inherited),'legacy_memory_hits':len(inherited)" in s: s=s.replace("'legacy_memory_hits':len(inherited),'legacy_memory_hits':len(inherited)","'legacy_memory_hits':len(inherited)")
s=s.replace("'recall':'project-wide-v2+legacy-transplant-v1'","'recall':'project-wide-v3+self-memory+learning-ledger'")
p.write_text(s,encoding='utf-8'); print('DORE_SELF_MEMORY_WIRE_IDEMPOTENT_PASS')
