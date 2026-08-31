#!/usr/bin/env python3
from __future__ import annotations
import json,os,subprocess
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); P=HOME/'runtime/design-providers/framesmith'; W=HOME/'evolution/design-bakeoff/framesmith-real-work'; W.mkdir(parents=True,exist_ok=True)
def cmd(a,t=600):
 c=subprocess.run(a,cwd=P,text=True,capture_output=True,timeout=t); return {'ok':c.returncode==0,'returncode':c.returncode,'stdout':(c.stdout or '')[-8000:],'stderr':(c.stderr or '')[-8000:]}
def main():
 if not P.exists(): print(json.dumps({'ok':False,'cause':'provider_not_installed'})); return 1
 install=cmd(['npm','install'],900)
 if not install['ok']: print(json.dumps({'ok':False,'cause':'npm_install_failed','install':install})); return 1
 build=cmd(['npm','run','build'],600)
 if not build['ok']: print(json.dumps({'ok':False,'cause':'build_failed','build':build})); return 1
 # Native package is now executable. Require a documented noninteractive creation surface before claiming a design test.
 helpx=cmd(['node','dist/index.js','--help'],120)
 text=(helpx.get('stdout','')+'\n'+helpx.get('stderr','')).lower()
 has_surface=any(x in text for x in ['create','scene','frame','mcp','stdio'])
 out={'ok':False,'cause':'native_creation_surface_not_proven' if not has_surface else 'native_server_requires_protocol_adapter','install':install,'build':build,'native_probe':helpx,'learning':'Build success is not design success; Framesmith requires a Doré protocol/MCP adapter before real create-render-edit-rerender evidence can be produced.'}
 print(json.dumps(out,ensure_ascii=False)); return 1
if __name__=='__main__': raise SystemExit(main())
