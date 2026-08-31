#!/usr/bin/env python3
from __future__ import annotations
import json,os,subprocess
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();P=HOME/'runtime/design-providers/tela'
def run(a,t=900):
 c=subprocess.run(a,cwd=P,text=True,capture_output=True,timeout=t);return {'ok':c.returncode==0,'returncode':c.returncode,'stdout':(c.stdout or '')[-8000:],'stderr':(c.stderr or '')[-8000:]}
def main():
 if not P.exists(): print(json.dumps({'ok':False,'cause':'provider_not_installed'}));return 1
 meta=json.loads((P/'package.json').read_text()) if (P/'package.json').exists() else {};scripts=meta.get('scripts') or {}
 install=run(['npm','install'])
 if not install['ok']: print(json.dumps({'ok':False,'cause':'npm_install_failed','install':install}));return 1
 build=run(['npm','run','build']) if 'build' in scripts else {'ok':True,'skipped':True}
 if not build['ok']: print(json.dumps({'ok':False,'cause':'build_failed','build':build}));return 1
 # Tela's browser dispatch API needs a controllable browser runtime. Do not count static build as real-work evidence.
 out={'ok':False,'cause':'browser_dispatch_runtime_not_available_or_not_proven','install':install,'build':build,'scripts':scripts,'learning':'Tela may supply a useful lightweight canvas/dispatch component, but Doré still needs a browser automation/dispatch bridge for observable create-edit-export work.'}
 print(json.dumps(out,ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
