#!/usr/bin/env python3
"""Bounded local production actions exposed to the DORÉ local control plane."""
from __future__ import annotations
import json, os, subprocess, time
from pathlib import Path
from urllib import request
CAPABILITIES={"design.production.rollout","search.local.repair","image.local.repair","wake.runtime.install","core.substrate.acceptance","knowledge.substrates.install","search.production.index"}
def _run(argv:list[str],cwd:Path|None=None,timeout:int=120,env:dict|None=None)->dict:
 child_env=os.environ.copy();child_env.update(env or {})
 try:
  p=subprocess.run(argv,cwd=str(cwd) if cwd else None,text=True,capture_output=True,timeout=timeout,env=child_env);return {"argv":argv,"returncode":p.returncode,"stdout":p.stdout[-8000:],"stderr":p.stderr[-8000:]}
 except subprocess.TimeoutExpired as exc:
  out=exc.stdout.decode() if isinstance(exc.stdout,bytes) else (exc.stdout or "");err=exc.stderr.decode() if isinstance(exc.stderr,bytes) else (exc.stderr or "");return {"argv":argv,"returncode":124,"stdout":out[-8000:],"stderr":(err+f"\ntimeout_after={timeout}s")[-8000:]}
def _repo():return Path(os.environ.get("DORE_WORKTREE") or os.environ.get("DORE_REPO_ROOT") or Path.home()/"westsidewatch.github.io").expanduser().resolve()
def _json(url,timeout=5):
 with request.urlopen(url,timeout=timeout) as r:return json.loads(r.read().decode())
def _post_json(url,payload,headers=None,timeout=240):
 data=json.dumps(payload,ensure_ascii=False).encode();h={"Content-Type":"application/json","Accept":"application/json"};h.update(headers or {});req=request.Request(url,data=data,method="POST",headers=h)
 with request.urlopen(req,timeout=timeout) as r:return json.loads(r.read().decode())
def _health():return _json("http://127.0.0.1:4310/api/health")
def _sync(repo):
 if not (repo/".git").exists():return {"ok":False,"status":"failed","error":{"code":"worktree_missing","message":str(repo)}}
 fetch=_run(["git","fetch","origin","main"],repo)
 if fetch["returncode"]:return {"ok":False,"status":"failed","step":"fetch","result":fetch}
 ff=_run(["git","merge","--ff-only","origin/main"],repo)
 if ff["returncode"]:return {"ok":False,"status":"failed","step":"fast_forward","result":ff}
def design_production_rollout(args=None):
 repo=_repo();err=_sync(repo)
 if err:return err
 install=_run(["bash",str(repo/"dore-design"/"install-macos.sh")],repo,env={"DORE_SKIP_CONTROL_PLANE_REFRESH":"1"})
 if install["returncode"]:return {"ok":False,"status":"failed","step":"install","result":install}
 health=_health()
 try:specimen=_json("http://127.0.0.1:4310/api/design2/specimen")
 except Exception as exc:specimen={"ok":False,"error":str(exc)}
 ok=bool(health.get("ok") and health.get("resident_entrypoint")=="app_design2.py" and health.get("immutable_publication") is True and specimen.get("ok"));return {"ok":ok,"status":"completed" if ok else "failed","capability":"design.production.rollout","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"health":health,"specimen":specimen,"install_tail":install["stdout"][-2000:]}
def search_local_repair(args=None):
 repo=_repo();err=_sync(repo)
 if err:return err
 install=_run(["bash",str(repo/"local"/"dore-local"/"install-launchagent.sh")],repo,env={"DORE_REPO_ROOT":str(repo)},timeout=180)
 if install["returncode"]:return {"ok":False,"status":"failed","step":"install","result":install}
 try:health=_json("http://127.0.0.1:8788/health")
 except Exception as exc:return {"ok":False,"status":"failed","step":"health","error":str(exc),"install_tail":install["stdout"][-2000:]}
 ok=bool(health.get("ok") and health.get("search_loopback") is True);return {"ok":ok,"status":"completed" if ok else "failed","capability":"search.local.repair","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"health":health,"install_tail":install["stdout"][-2000:]}
def image_local_repair(args=None):
 repo=_repo();err=_sync(repo)
 if err:return err
 install=_run(["bash",str(repo/"local"/"dore-local"/"install-image-local-macos.sh")],repo,timeout=3600)
 if install["returncode"]:return {"ok":False,"status":"failed","capability":"image.local.repair","step":"install","result":install}
 try:health=_json("http://127.0.0.1:8790/health",15)
 except Exception as exc:return {"ok":False,"status":"failed","capability":"image.local.repair","step":"health","error":str(exc),"install_tail":install["stdout"][-3000:]}
 allowed={"comfyui","stable-diffusion.cpp"}
 if not (health.get("ok") and health.get("renderer") is True and health.get("model_backed") is True and health.get("renderer_mode") in allowed and health.get("config") is True):return {"ok":False,"status":"failed","capability":"image.local.repair","step":"model_backed_renderer_ready","health":health,"install_tail":install["stdout"][-3000:]}
 try:generated=_post_json("http://127.0.0.1:8790/generate",{"message":"生成一張自然晨光中的古典石門圖片，真實攝影質感，大量留白"},{"X-Dore-Origin":"dore-search"},1500)
 except Exception as exc:return {"ok":False,"status":"failed","capability":"image.local.repair","step":"generate","health":health,"error":str(exc),"install_tail":install["stdout"][-3000:]}
 art=generated.get("artifact") or {};raster=art.get("mime_type") in {"image/png","image/jpeg","image/webp"};ok=bool(generated.get("ok") and generated.get("capability")=="image.generate" and generated.get("model_backed") is True and generated.get("renderer") in allowed and art.get("sha256") and raster and int(art.get("bytes") or 0)>1024);return {"ok":ok,"status":"completed" if ok else "failed","capability":"image.local.repair","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"health":health,"generation":generated,"install_tail":install["stdout"][-3000:]}
def wake_runtime_install(args=None):
 repo=_repo();err=_sync(repo)
 if err:return err
 runtime=repo/"dore-core"/"runtime"/"wake_runtime.py";installer=repo/"dore-core"/"runtime"/"install_wake_launchd.py";db=Path.home()/"Library"/"Application Support"/"Dore"/"wake-state.sqlite3";plist=Path.home()/"Library"/"LaunchAgents"/"org.westsidewatch.dore.wake.plist";log_dir=Path.home()/"Library"/"Application Support"/"Dore"/"logs";init=_run(["python3",str(runtime),"--db",str(db),"init"],repo,timeout=15)
 if init["returncode"]:return {"ok":False,"status":"failed","capability":"wake.runtime.install","step":"db_init","result":init}
 smoke=_run(["python3",str(runtime),"--db",str(db),"enqueue","--kind","probe","--payload-json",json.dumps({"argv":["/usr/bin/true"]}),"--idempotency-key","wake-local-install-smoke-v3","--max-attempts","1"],repo,timeout=15)
 if smoke["returncode"]:return {"ok":False,"status":"failed","capability":"wake.runtime.install","step":"smoke_enqueue","result":smoke}
 try:smoke_task_id=str(json.loads(smoke["stdout"])["task_id"])
 except Exception:return {"ok":False,"status":"failed","capability":"wake.runtime.install","step":"smoke_id","result":smoke}
 install=_run(["python3",str(installer),"--repo",str(repo)],repo,timeout=120)
 if install["returncode"]:return {"ok":False,"status":"failed","capability":"wake.runtime.install","step":"install","result":install,"smoke_task_id":smoke_task_id}
 uid=os.getuid();label=f"gui/{uid}/org.westsidewatch.dore.wake";launch=_run(["/bin/launchctl","print",label],repo,timeout=15);kick=_run(["/bin/launchctl","kickstart","-k",label],repo,timeout=45);state={"stdout":"","returncode":1,"stderr":"not_polled","argv":[]};smoke_row={};smoke_pass=False
 for _ in range(30):
  state=_run(["python3",str(runtime),"--db",str(db),"status"],repo,timeout=15)
  if state["returncode"]==0:
   try:
    rows=json.loads(state["stdout"]);smoke_row=next((r for r in rows if str(r.get("id"))==smoke_task_id),{})
    if smoke_row.get("state")=="passed":smoke_pass=True;break
    if smoke_row.get("state")=="failed":break
   except Exception:pass
  time.sleep(.5)
 out_log=(log_dir/"wake.out.log").read_text(errors="replace")[-3000:] if (log_dir/"wake.out.log").is_file() else "";err_log=(log_dir/"wake.err.log").read_text(errors="replace")[-3000:] if (log_dir/"wake.err.log").is_file() else "";ok=bool(launch["returncode"]==0 and db.is_file() and plist.is_file() and smoke_pass);return {"ok":ok,"status":"completed" if ok else "failed","capability":"wake.runtime.install","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"label":label,"plist":str(plist),"db":str(db),"launchctl_loaded":launch["returncode"]==0,"smoke_task_id":smoke_task_id,"smoke_state":smoke_row.get("state"),"smoke_passed":smoke_pass,"kickstart_returncode":kick["returncode"],"install_tail":install["stdout"][-2000:],"launchctl_tail":launch["stdout"][-2500:],"state_tail":state["stdout"][-4000:],"wake_out_tail":out_log,"wake_err_tail":err_log}
def _acceptance_script(repo,name):
 run=_run(["python3",str(repo/"dore-core"/"runtime"/name)],repo,timeout=60)
 try:evidence=json.loads(run["stdout"])
 except Exception:evidence={"ok":False,"error":"invalid_acceptance_output","stdout":run["stdout"]}
 return {"ok":bool(run["returncode"]==0 and evidence.get("ok") is True),"evidence":evidence,"stderr_tail":run["stderr"][-2000:]}
def core_substrate_acceptance(args=None):
 repo=_repo();err=_sync(repo)
 if err:return err
 common=_acceptance_script(repo,"common_substrate_acceptance.py");conversation=_acceptance_script(repo,"conversation_substrate_acceptance.py");ok=bool(common["ok"] and conversation["ok"]);return {"ok":ok,"status":"completed" if ok else "failed","capability":"core.substrate.acceptance","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"acceptance":{"common":common["evidence"],"conversation":conversation["evidence"]},"stderr_tail":{"common":common["stderr_tail"],"conversation":conversation["stderr_tail"]}}
def knowledge_substrates_install(args=None):
 repo=_repo();err=_sync(repo)
 if err:return err
 script=repo/"local"/"dore-local"/"install-knowledge-substrates-macos.sh"
 if not script.is_file():return {"ok":False,"status":"failed","capability":"knowledge.substrates.install","error":{"code":"installer_missing","message":str(script)}}
 run=_run(["bash",str(script)],repo,timeout=1800,env={"DORE_REPO_ROOT":str(repo)})
 evidence={}
 if run["stdout"].strip():
  try:evidence=json.loads(run["stdout"].splitlines()[-1])
  except Exception:evidence={"ok":False,"error":"invalid_poc_output","stdout_tail":run["stdout"][-4000:]}
 ok=bool(run["returncode"]==0 and evidence.get("ok") is True and evidence.get("authority") is False and evidence.get("offline_core") is True)
 return {"ok":ok,"status":"completed" if ok else "failed","capability":"knowledge.substrates.install","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"evidence":evidence,"install_tail":run["stdout"][-4000:],"stderr_tail":run["stderr"][-4000:]}
def search_production_index(args=None):
 repo=_repo();err=_sync(repo)
 if err:return err
 base=Path.home()/"Library"/"Application Support"/"Dore"/"local-ai";qmd=base/"bin"/"qmd";script=repo/"local"/"dore-local"/"search-production-index.py"
 if not qmd.is_file():return {"ok":False,"status":"failed","capability":"search.production.index","error":{"code":"qmd_missing","message":str(qmd)}}
 run=_run(["python3",str(script),"--repo",str(repo),"--qmd",str(qmd),"--data",str(base/"data")],repo,timeout=600)
 try:evidence=json.loads(run["stdout"].splitlines()[-1])
 except Exception:evidence={"ok":False,"error":"invalid_index_output","stdout_tail":run["stdout"][-4000:]}
 ok=bool(run["returncode"]==0 and evidence.get("ok") is True and evidence.get("authority") is False)
 return {"ok":ok,"status":"completed" if ok else "failed","capability":"search.production.index","repo":str(repo),"head":_run(["git","rev-parse","HEAD"],repo)["stdout"].strip(),"evidence":evidence,"stderr_tail":run["stderr"][-3000:]}
def execute(capability,args=None):
 if capability=="design.production.rollout":return design_production_rollout(args)
 if capability=="search.local.repair":return search_local_repair(args)
 if capability=="image.local.repair":return image_local_repair(args)
 if capability=="wake.runtime.install":return wake_runtime_install(args)
 if capability=="core.substrate.acceptance":return core_substrate_acceptance(args)
 if capability=="knowledge.substrates.install":return knowledge_substrates_install(args)
 if capability=="search.production.index":return search_production_index(args)
 return {"ok":False,"status":"failed","error":{"code":"unsupported_production_action","message":capability}}
