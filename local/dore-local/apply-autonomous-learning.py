#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name('dore_local.py'); s=p.read_text(encoding='utf-8')
imp="from autonomous_learner import status as autonomous_learning_status\n"
if imp not in s:
    anchor="from learning_planner import plan as learning_plan, validate_gate\n"
    s=s.replace(anchor,anchor+imp,1)
if 'def autonomous_learning_view():' not in s:
    anchor="def learning_plan_view():\n"
    pos=s.find(anchor)
    if pos>=0:
        end=s.find('def legacy_view(q):',pos)
        block="""def autonomous_learning_view():
 with db() as c: return autonomous_learning_status(c)
"""
        if end>=0: s=s[:end]+block+s[end:]
route="  if self.path=='/learning/autonomous/status': return self.sendj(autonomous_learning_view())\n"
while s.count(route)>1: s=s.replace(route+route,route)
if route not in s:
    marker="  if self.path=='/learning/plan': return self.sendj(learning_plan_view())\n"
    s=s.replace(marker,marker+route,1)
for old in ('project-wide-v4+self-memory+learning-ledger+capability-planner','project-wide-v5+self-memory+learning-ledger+autonomous-learning'):
    s=s.replace(old,'project-wide-v5+self-memory+learning-ledger+autonomous-learning')
p.write_text(s,encoding='utf-8'); print('DORE_AUTONOMOUS_LEARNING_WIRE_PASS')
