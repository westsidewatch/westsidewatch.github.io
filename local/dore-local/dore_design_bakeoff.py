#!/usr/bin/env python3
"""Doré Design provider bake-off: bounded local-first capability discovery/probe."""
from __future__ import annotations
import json,os,shutil,subprocess,time
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
RUNTIME=HOME/'runtime'/'design-providers'; EVIDENCE=HOME/'evolution'/'design-bakeoff'
CANDIDATES={
 'openpencil':{'repo':'https://github.com/open-pencil/open-pencil.git','license':'MIT','priority':'base'},
 'framesmith':{'repo':'https://github.com/vicmaster/framesmith.git','license':'inspect','priority':'component'},
 'doop':{'repo':'https://github.com/kgoedecke/doop.git','license':'AGPL-3.0','priority':'collaboration'},
 'tela':{'repo':'https://github.com/heyimjames/tela.git','license':'inspect','priority':'canvas'},
}
def run(argv,cwd=None,timeout=180):
 try:
  cp=subprocess.run(argv,cwd=str(cwd) if cwd else None,text=True,capture_output=True,timeout=timeout)
  return {'ok':cp.returncode==0,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-6000:],'stderr':(cp.stderr or '')[-6000:]}
 except Exception as e:return {'ok':False,'exception':type(e).__name__+': '+str(e)}
def sync(name,spec):
 target=RUNTIME/name; target.parent.mkdir(parents=True,exist_ok=True)
 if (target/'.git').exists(): r=run(['git','-C',str(target),'pull','--ff-only'],timeout=240)
 else:r=run(['git','clone','--depth','1',spec['repo'],str(target)],timeout=300)
 if not r['ok']:return {'name':name,'ok':False,'stage':'sync','detail':r}
 rev=run(['git','rev-parse','HEAD'],cwd=target); files={}
 for fn in ('LICENSE','LICENSE.md','package.json','README.md'):
  p=target/fn
  if p.exists():files[fn]=p.read_text(errors='replace')[:12000]
 pkg={}
 try:pkg=json.loads((target/'package.json').read_text()) if (target/'package.json').exists() else {}
 except:pass
 return {'name':name,'ok':True,'target':str(target),'revision':rev.get('stdout','').strip(),'declared_license':spec['license'],'priority':spec['priority'],'package_name':pkg.get('name'),'package_version':pkg.get('version'),'scripts':pkg.get('scripts',{}),'has_license':any(k.startswith('LICENSE') for k in files),'license_excerpt':next((v[:2000] for k,v in files.items() if k.startswith('LICENSE')),''),'readme_excerpt':files.get('README.md','')[:4000]}
def environment():
 out={}
 for exe in ('git','node','npm','npx'):
  out[exe]={'path':shutil.which(exe),'version':run([exe,'--version']) if shutil.which(exe) else None}
 out['chrome_candidates']=[p for p in ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','/Applications/Chromium.app/Contents/MacOS/Chromium'] if Path(p).exists()]
 out['penpot_mcp']='configured:localhost:4401'
 return out
def main():
 run_id=time.strftime('%Y%m%d-%H%M%S'); EVIDENCE.mkdir(parents=True,exist_ok=True)
 report={'ok':True,'run_id':run_id,'kind':'DORE_EVOLUTION_RUN_001_DESIGN_EQUIPMENT_DISCOVERY','environment':environment(),'candidates':[],'learning':{'trigger':'Need a stable local-first machine-operable design capability','method':'discover -> provenance -> local probe -> compare -> later real-work acceptance','human_terminal_required':False}}
 for name,spec in CANDIDATES.items():
  item=sync(name,spec);report['candidates'].append(item)
  if not item.get('ok'):report['ok']=False
 p=EVIDENCE/(run_id+'.json');p.write_text(json.dumps(report,ensure_ascii=False,indent=2))
 report['evidence_path']=str(p)
 print(json.dumps(report,ensure_ascii=False))
 return 0
if __name__=='__main__':raise SystemExit(main())
