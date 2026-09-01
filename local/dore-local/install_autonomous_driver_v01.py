#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name('coordination_worker.py')
s=p.read_text(encoding='utf-8')
imp="from autonomous_capability_loop import attempt_learning_recovery"
newimp=imp+"\nfrom autonomous_driver import drive as autonomous_drive"
if 'from autonomous_driver import drive as autonomous_drive' not in s:
    if imp not in s: raise SystemExit('expected import anchor missing')
    s=s.replace(imp,newimp,1)
anchor="if kind=='local_exec':return local_exec(msg)"
addition=anchor+"\n if kind in ('autonomous_driver','research_bridge_acceptance','autonomous_capability_loop'):return autonomous_drive(msg)"
if "kind in ('autonomous_driver','research_bridge_acceptance','autonomous_capability_loop')" not in s:
    if anchor not in s: raise SystemExit('expected dispatch anchor missing')
    s=s.replace(anchor,addition,1)
p.write_text(s,encoding='utf-8')
print('AUTONOMOUS_DRIVER_V01_INSTALLED')
