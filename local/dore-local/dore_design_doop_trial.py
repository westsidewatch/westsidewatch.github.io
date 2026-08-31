#!/usr/bin/env python3
from __future__ import annotations
import json,os,subprocess
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); P=HOME/'runtime/design-providers/doop'
def run(a,t=900):
 c=subprocess.run(a,cwd=P,text=True,capture_output=True,timeout=t);return {'ok':c.returncode==0,'returncode':c.returncode,'stdout':(c.stdout or '')[-8000:],'stderr':(c.stderr or '')[-8000:]}
def main():
 if not P.exists(): print(json.dumps({'ok':False,'cause':'provider_not_installed'}));return 1
 pkg=P/'package.json'
 meta=json.loads(pkg.read_text()) if pkg.exists() else {}; scripts=meta.get('scripts') or {}
 install=run(['npm','install'])
 if not install['ok']: print(json.dumps({'ok':False,'cause':'npm_install_failed','install':install}));return 1
 build=run(['npm','run','build'],900) if 'build' in scripts else {'ok':True,'skipped':True}
 if not build['ok']: print(json.dumps({'ok':False,'cause':'build_failed','build':build}));return 1
 # Do not fabricate a design pass: auth/server/MCP must expose a bounded autonomous creation path.
 out={'ok':False,'cause':'local_collaboration_server_requires_live_protocol_or_auth_adapter','install':install,'build':build,'scripts':scripts,'learning':'A runnable collaboration app is not yet an autonomous Doré design capability; MCP/auth/session bootstrap must be proven without user mediation.'}
 print(json.dumps(out,ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
