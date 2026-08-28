#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name('dore_local.py'); s=p.read_text(encoding='utf-8')
imp="from learning_planner import plan as learning_plan, validate_gate\n"
if imp not in s:
    anchor="from self_memory import ensure_schema as ensure_self_schema, upsert_self, add_learning, status as self_status, context as self_context\n"
    s=s.replace(anchor,anchor+imp,1)
if 'def learning_plan_view():' not in s:
    anchor='def self_prompt():\n with db() as c: return self_context(c)\n'
    block="""def learning_plan_view():
 path=Path(__file__).resolve().parent/'learning-gates'/'core-v1.json'
 try: payload=json.loads(path.read_text(encoding='utf-8'))
 except Exception as e: return {'ok':False,'error':'learning_gate_load_failed','detail':str(e)}
 try: gates=[validate_gate(x) for x in (payload.get('gates') or [])]
 except ValueError as e: return {'ok':False,'error':'invalid_learning_gate','detail':str(e)}
 with db() as c: state=self_status(c)
 out=learning_plan(state,gates); out['ok']=True; return out
"""
    s=s.replace(anchor,anchor+block,1)
route="  if self.path=='/learning/plan': return self.sendj(learning_plan_view())\n"
if route not in s:
    marker="  if self.path in {'/memory/self/status','/learning/status'}: return self.sendj(self_view())\n"
    s=s.replace(marker,marker+route,1)
s=s.replace("'recall':'project-wide-v3+self-memory+learning-ledger'","'recall':'project-wide-v4+self-memory+learning-ledger+capability-planner'",1)
p.write_text(s,encoding='utf-8'); print('DORE_LEARNING_PLANNER_WIRE_APPLIED')
