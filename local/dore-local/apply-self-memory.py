#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name('dore_local.py')
s=p.read_text(encoding='utf-8')
imp="from self_memory import ensure_schema as ensure_self_schema, upsert_self, add_learning, status as self_status, context as self_context\n"
if imp not in s:
    marker="from legacy_memory import ensure_schema as ensure_legacy_schema, import_items as import_legacy_items, recall as legacy_recall, context as legacy_context\n"
    # clean accidental duplicate legacy imports while wiring
    while s.count(marker)>1: s=s.replace(marker+marker,marker)
    s=s.replace(marker,marker+imp,1)
s=s.replace("  ensure_legacy_schema(c)\n  ensure_legacy_schema(c)\n  ensure_legacy_schema(c)\n","  ensure_legacy_schema(c)\n  ensure_self_schema(c)\n",1)
if 'def bootstrap_self_memory():' not in s:
    anchor='def legacy_view(q):\n'
    block="""def bootstrap_self_memory():
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
"""
    s=s.replace(anchor,block+anchor,1)
# status routes
needle="  if self.path=='/legacy-memory/status': return self.sendj({'ok':True,'legacy_memory':legacy_status()})\n"
while s.count(needle)>1: s=s.replace(needle+needle,needle)
if "self.path=='/memory/self/status'" not in s:
    s=s.replace(needle,needle+"  if self.path in {'/memory/self/status','/learning/status'}: return self.sendj(self_view())\n",1)
# prompt injection
old="sys=SYSTEM+'\\n\\nDoré conversational memory:\\n'+context+'\\n\\nDoré inherited legacy memory (usable, provenance-labelled; inherited is not the same as externally verified):\\n'+legacy_context(inherited)"
new="sys=SYSTEM+'\\n\\nDoré durable self memory and learning ledger:\\n'+self_prompt()+'\\n\\nDoré conversational memory:\\n'+context+'\\n\\nDoré inherited legacy memory (usable, provenance-labelled; inherited is not the same as externally verified):\\n'+legacy_context(inherited)"
s=s.replace(old,new,1)
# startup
s=s.replace('ensure_design_schema(); bootstrap_legacy_memory();','ensure_design_schema(); bootstrap_legacy_memory(); bootstrap_self_memory();',1)
# health marker
s=s.replace("'recall':'project-wide-v2+legacy-transplant-v1'","'recall':'project-wide-v3+self-memory+learning-ledger'",1)
p.write_text(s,encoding='utf-8')
print('DORE_SELF_MEMORY_WIRE_APPLIED')
