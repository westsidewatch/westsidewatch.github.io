#!/usr/bin/env python3
from pathlib import Path
p=Path(__file__).with_name('dore_local.py'); s=p.read_text(encoding='utf-8')
pen="from penpot_agent import status as penpot_status, run_task as run_penpot_task\n"; imp="from legacy_memory import ensure_schema as ensure_legacy_schema, import_items as import_legacy_items, recall as legacy_recall, context as legacy_context\n"
while s.count(imp)>1: s=s.replace(imp+imp,imp)
if imp not in s: s=s.replace(pen,pen+imp,1)
# Legacy wiring is migration-only and must never duplicate active runtime wiring.
if 'def bootstrap_legacy_memory():' not in s: raise SystemExit('legacy bootstrap missing; regenerate from canonical runtime instead of blind patching')
if "memories=recall(project,cid,text); inherited=legacy_view(text);" not in s: raise SystemExit('legacy recall wiring missing')
if "self.path=='/legacy-memory/status'" not in s: raise SystemExit('legacy status route missing')
while "'legacy_memory_hits':len(inherited),'legacy_memory_hits':len(inherited)" in s: s=s.replace("'legacy_memory_hits':len(inherited),'legacy_memory_hits':len(inherited)","'legacy_memory_hits':len(inherited)")
p.write_text(s,encoding='utf-8'); print('DORE_LEGACY_TRANSPLANT_IDEMPOTENT_PASS')
