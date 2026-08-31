#!/usr/bin/env python3
import json,os,subprocess,tempfile
from pathlib import Path

def run(cwd,*a): return subprocess.run(list(a),cwd=cwd,text=True,capture_output=True,check=True)
with tempfile.TemporaryDirectory() as td:
 td=Path(td);remote=td/'remote.git';seed=td/'seed';local=td/'local'
 run(td,'git','init','--bare',str(remote));run(td,'git','clone',str(remote),str(seed))
 run(seed,'git','config','user.email','test@example.com');run(seed,'git','config','user.name','test')
 (seed/'base.txt').write_text('base\n');run(seed,'git','add','.');run(seed,'git','commit','-m','base');run(seed,'git','branch','-M','main');run(seed,'git','push','-u','origin','main')
 run(td,'git','clone','-b','main',str(remote),str(local));run(local,'git','config','user.email','test@example.com');run(local,'git','config','user.name','test')
 (local/'local.txt').write_text('local\n');run(local,'git','add','.');run(local,'git','commit','-m','local work');local_before=run(local,'git','rev-parse','HEAD').stdout.strip()
 (seed/'remote.txt').write_text('remote\n');run(seed,'git','add','.');run(seed,'git','commit','-m','remote work');run(seed,'git','push')
 env=os.environ.copy();env['DORE_REPO_ROOT']=str(local);env['DORE_RESCUE_SKIP_INSTALL']='1'
 cp=subprocess.run(['python3',str(Path(__file__).with_name('rescue-coordination.py'))],env=env,text=True,capture_output=True)
 assert cp.returncode==0,(cp.stdout,cp.stderr);out=json.loads(cp.stdout.strip().splitlines()[-1]);assert out['ok'] and out['code']=='DORE_COORDINATION_RESCUE_PASS';assert out['backup_branch']
 backup=run(local,'git','rev-parse',out['backup_branch']).stdout.strip();assert backup==local_before
 assert (local/'local.txt').read_text()=='local\n' and (local/'remote.txt').read_text()=='remote\n'
 ahead,behind=map(int,run(local,'git','rev-list','--left-right','--count','HEAD...origin/main').stdout.split());assert behind==0
 print(json.dumps({'ok':True,'code':'RESCUE_DIVERGENCE_TEST_PASS','backup_preserved':backup==local_before,'behind':behind,'ahead':ahead}))
