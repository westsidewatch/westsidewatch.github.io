#!/usr/bin/env python3
from __future__ import annotations
import os, subprocess, json
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
OUT=ROOT/'dore-design'/'prep'; OUT.mkdir(parents=True,exist_ok=True)
MODEL=os.environ.get('DORE_LOCAL_MODEL','gemma4:e4b')
BASE='''You are Doré working on Westside Watch visual preparation in the background. Do NOT redesign from zero. Preserve accepted visual DNA: editorial gravity; information-as-brick, weight-as-battlement, time-as-flow; 5:8 editorial weight; Light + Line/Engraving + Architecture; quiet architectural Christian editorial dawn character; Cormorant Garamond/Noto Serif TC intent; First Light Gold #A2872A, Warm Gold #B79838, Morning Gold #D2BC69, Watch Night #102A43, Living Paper #FAF9F5, Ink Black #252525, Olive Branch #738A5A, Living Water #5B8FA8, Harvest #B8944A, Crimson Robe #A14D57. Output concise production-ready design guidance, not abstract philosophy.'''
TASKS={
'COLOR.md':BASE+'\nFocus only on colour roles, hierarchy, contrast, combinations to avoid, and a compact token/usage proposal for homepage production.',
'STRUCTURE.md':BASE+'\nFocus only on page architecture, hierarchy, section rhythm, 5:8 editorial modules, navigation/hero/feature/content/footer relationships, and reusable structural rules.',
'CONTENT.md':BASE+'\nFocus only on editorial content preparation: masthead, hero message hierarchy, Chinese/English balance, feature labels, short module copy requirements, and what content should be ready before layout.',
'OBSERVATION.md':BASE+'\nAct as an apprentice watching the Doré Design mainline. Record what must be learned from the working pipeline: evidence-first tool use, create-render-edit-rerender verification, preserving same artifact, and how prepared visual decisions should become machine-operable inputs after merge.'}
def ask(prompt):
 cp=subprocess.run(['ollama','run',MODEL,prompt],cwd=ROOT,text=True,capture_output=True,timeout=600)
 if cp.returncode!=0: raise RuntimeError(cp.stderr[-3000:])
 return cp.stdout.strip()
results={}
for name,prompt in TASKS.items():
 try:
  text=ask(prompt); (OUT/name).write_text(text+'\n',encoding='utf-8'); results[name]={'ok':True,'chars':len(text)}
 except Exception as e: results[name]={'ok':False,'error':str(e)[:1000]}
manifest={'generated_at':datetime.now(timezone.utc).isoformat(),'model':MODEL,'results':results,'mainline_blocking':False,'visual_restart_forbidden':True}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'ok':all(v['ok'] for v in results.values()),'output_dir':str(OUT),'results':results},ensure_ascii=False))
