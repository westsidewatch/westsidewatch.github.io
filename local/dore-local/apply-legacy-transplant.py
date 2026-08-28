#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name('dore_local.py')
s=p.read_text()
s=s.replace("from penpot_agent import status as penpot_status, run_task as run_penpot_task", "from penpot_agent import status as penpot_status, run_task as run_penpot_task\nfrom legacy_memory import ensure_schema as ensure_legacy_schema, import_items as import_legacy_items, recall as legacy_recall, context as legacy_context")
s=s.replace("def ensure_design_schema():\n ROOT.joinpath('archive','design-evidence').mkdir(parents=True,exist_ok=True)\n with db() as c:", "def ensure_design_schema():\n ROOT.joinpath('archive','design-evidence').mkdir(parents=True,exist_ok=True)\n with db() as c:\n  ensure_legacy_schema(c)")
needle="def save(cid,role,content,project='dore-global'):"
bootstrap="""def bootstrap_legacy_memory():
 seed_dir=Path(__file__).resolve().parent/'legacy-memory'
 total=0
 for seed in sorted(seed_dir.glob('seed-*.json')):
  try: payload=json.loads(seed.read_text(encoding='utf-8')); items=payload.get('items') or []
  except Exception: continue
  with db() as c: total+=len(import_legacy_items(c,ROOT,items))
 return total
def legacy_view(q):
 with db() as c: return legacy_recall(c,q)
def legacy_status():
 with db() as c:
  ensure_legacy_schema(c)
  total=c.execute('SELECT COUNT(*) FROM dore_legacy_memory').fetchone()[0]
  states={r[0]:r[1] for r in c.execute('SELECT epistemic_state,COUNT(*) FROM dore_legacy_memory GROUP BY epistemic_state')}
  subjects={r[0]:r[1] for r in c.execute('SELECT subject,COUNT(*) FROM dore_legacy_memory GROUP BY subject')}
 return {'total':total,'states':states,'subjects':subjects,'source':'chatgpt_legacy_memory'}
"""
start=s.find('def bootstrap_legacy_memory():')
if start>=0:
 end=s.find(needle,start)
 if end>=0: s=s[:start]+bootstrap+s[end:]
elif bootstrap not in s:
 s=s.replace(needle,bootstrap+needle)
s=s.replace("memories=recall(project,cid,text); context='\\n'.join(f\"[{m['created_at']}] {m['role']}: {m['content']}\" for m in memories); dv=design_view(project) if state['design_mode'] else None", "memories=recall(project,cid,text); inherited=legacy_view(text); context='\\n'.join(f\"[{m['created_at']}] {m['role']}: {m['content']}\" for m in memories); dv=design_view(project) if state['design_mode'] else None")
s=s.replace("sys=SYSTEM+'\\n\\nDoré memory:\\n'+context", "sys=SYSTEM+'\\n\\nDoré conversational memory:\\n'+context+'\\n\\nDoré inherited legacy memory (usable, provenance-labelled; inherited is not the same as externally verified):\\n'+legacy_context(inherited)")
s=s.replace("'memory_hits':len(memories)", "'memory_hits':len(memories),'legacy_memory_hits':len(inherited)")
s=s.replace("'recall':'project-wide-v2'", "'recall':'project-wide-v2+legacy-transplant-v1'", 1)
s=s.replace("if self.path=='/health': return self.sendj({'ok':True,'node':'dore-local'", "if self.path=='/legacy-memory/status': return self.sendj({'ok':True,'legacy_memory':legacy_status()})\n  if self.path=='/health': return self.sendj({'ok':True,'node':'dore-local'")
s=s.replace("if __name__=='__main__':\n ensure_design_schema();", "if __name__=='__main__':\n ensure_design_schema(); bootstrap_legacy_memory();")
p.write_text(s)
print('DORE_LEGACY_TRANSPLANT_WIRED')
