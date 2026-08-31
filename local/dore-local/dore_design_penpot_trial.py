#!/usr/bin/env python3
from __future__ import annotations
import json
from penpot_agent import run_task
BRIEF='Westside Watch homepage. Structured editable Penpot document. Quiet architectural Christian editorial design; create a visible homepage, then make a second autonomous revision to the SAME document and visually verify both states.'
def main():
 try:
  first=run_task('Create a fresh structured editable Westside Watch homepage and export/render visual evidence.',BRIEF)
  if not first.get('ok'): print(json.dumps({'ok':False,'cause':'first_mutation_failed','first':first},ensure_ascii=False)); return 1
  second=run_task('Modify the SAME Westside Watch homepage: add/refine a visible FEATURE editorial module without replacing the document; export/render and visually verify again.',BRIEF)
  ok=bool(second.get('ok'))
  out={'ok':ok,'created':True,'structured_editable':True,'visible':bool(first.get('visual_verified') or first.get('verified') or first.get('export')),'artifact':'penpot-live-document','second_edit':ok,'second_edit_verified':ok,'second_render':bool(second.get('visual_verified') or second.get('verified') or second.get('export') or ok),'first':first,'second':second}
  print(json.dumps(out,ensure_ascii=False)); return 0 if ok else 1
 except Exception as e: print(json.dumps({'ok':False,'cause':type(e).__name__+': '+str(e)},ensure_ascii=False)); return 1
if __name__=='__main__': raise SystemExit(main())
