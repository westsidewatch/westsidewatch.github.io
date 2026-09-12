#!/usr/bin/env python3
"""Bounded final publication admission: Multiwrite artifacts -> Dawn canonical substrate."""
from __future__ import annotations
import base64,hashlib,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
CAPABILITIES={"dawn.library.publish"};FORBIDDEN=("wikisource","zh.wikisource.org","openlibrary.org");ALLOWED={"cover","web","epub","pdf"};MAX_ASSET_BYTES=48*1024*1024

def _run(argv,cwd,timeout=180):
 p=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout);return {"returncode":p.returncode,"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]}
def _repo():return Path(os.environ.get("DORE_WORKTREE") or os.environ.get("DORE_REPO_ROOT") or Path.home()/"westsidewatch.github.io").expanduser().resolve()
def _safe_name(value):
 name=Path(str(value or "")).name
 if not name or name in {".",".."}:raise ValueError("invalid artifact filename")
 return re.sub(r"[^A-Za-z0-9._-]+","-",name)[:160]
def _validate(admission,assets):
 if not isinstance(admission,dict) or admission.get("schema")!="dore.dawn-publication-admission.v1":raise ValueError("invalid Dawn admission schema")
 raw=json.dumps(admission,ensure_ascii=False).lower()
 if any(token in raw for token in FORBIDDEN):raise ValueError("forbidden runtime dependency")
 work=admission.get("work") or {};edition=admission.get("edition") or {};surface=admission.get("surface") or {};policy=admission.get("policy") or {}
 work_id=str(work.get("workId") or "");edition_id=str(edition.get("editionId") or "")
 if not work_id or not edition_id or edition.get("workId")!=work_id:raise ValueError("invalid Work/Edition identity")
 if not str(work.get("title") or "").strip():raise ValueError("publication title required")
 if policy.get("surfaceOwnsIdentity") is not False or policy.get("wikisource")!="forbidden":raise ValueError("Dawn policy mismatch")
 if (surface.get("ref") or {}).get("workId")!=work_id:raise ValueError("surface Work reference mismatch")
 by_kind={}
 for item in assets or []:
  kind=str(item.get("kind") or "")
  if kind not in ALLOWED or kind in by_kind:raise ValueError("invalid or duplicate artifact kind")
  data=base64.b64decode(str(item.get("base64") or ""),validate=True)
  if not data or len(data)>MAX_ASSET_BYTES:raise ValueError("artifact size rejected")
  if int(item.get("bytes") or len(data))!=len(data):raise ValueError("artifact byte count mismatch")
  if kind=="epub" and not data.startswith(b"PK"):raise ValueError("EPUB signature rejected")
  if kind=="pdf" and not data.startswith(b"%PDF"):raise ValueError("PDF signature rejected")
  if kind=="web" and b"<" not in data[:2048]:raise ValueError("Web artifact rejected")
  by_kind[kind]={"filename":_safe_name(item.get("filename")),"mime":str(item.get("mime") or ""),"data":data,"sha256":hashlib.sha256(data).hexdigest()}
 if set(by_kind)!=ALLOWED:raise ValueError("Cover, Web, EPUB and PDF are all required")
 return work_id,edition_id,by_kind

def _apply(repo,admission,assets):
 work_id,edition_id,by_kind=_validate(admission,assets);key=hashlib.sha256(work_id.encode()).hexdigest()[:20];edition_key=hashlib.sha256(edition_id.encode()).hexdigest()[:16]
 rel_dir=Path("static/dawn-library/publications")/key/edition_key;target=repo/rel_dir;target.mkdir(parents=True,exist_ok=True);pointers={}
 for kind,item in by_kind.items():
  path=target/item["filename"];path.write_bytes(item["data"]);pointers[kind]="/"+str((rel_dir/item["filename"]).as_posix())
 record=json.loads(json.dumps(admission));record["edition"]["artifacts"]=pointers;record["edition"]["checksums"]={k:v["sha256"] for k,v in by_kind.items()}
 admission_dir=repo/"data/dawn-publication-admissions";admission_dir.mkdir(parents=True,exist_ok=True);record_path=admission_dir/f"{key}.json";record_path.write_text(json.dumps(record,ensure_ascii=False,separators=(",",":"))+"\n",encoding="utf-8")
 build=_run(["python3","scripts/build_dawn_canonical_substrate.py"],repo,240)
 if build["returncode"]:raise RuntimeError("canonical rebuild failed: "+build["stderr"])
 index=json.loads((repo/"static/dawn-library/canonical-index.json").read_text());surface=json.loads((repo/"static/dawn-library/surfaces/dawn-storefront.json").read_text())
 canonical=(index.get("works") or {}).get(work_id);refs=[r.get("workId") for s in surface.get("shelves",[]) if s.get("id")=="dore-publications" for r in s.get("items",[])]
 if not canonical or work_id not in refs:raise RuntimeError("publication did not enter canonical Dawn surface")
 return {"workId":work_id,"editionId":edition_id,"record":str(record_path.relative_to(repo)),"artifactDir":"/"+str(rel_dir.as_posix()),"canonical":canonical}

def publish(args=None):
 args=args or {};admission=args.get("admission") or {};assets=args.get("assets") or []
 if args.get("validate_only"):
  work_id,edition_id,by_kind=_validate(admission,assets);return {"ok":True,"status":"validated","capability":"dawn.library.publish","workId":work_id,"editionId":edition_id,"artifacts":{k:v["sha256"] for k,v in by_kind.items()}}
 base=_repo()
 if not (base/".git").exists():return {"ok":False,"status":"failed","error":{"code":"repo_missing","message":str(base)}}
 for attempt in range(1,4):
  fetch=_run(["git","fetch","origin","main"],base,120)
  if fetch["returncode"]:return {"ok":False,"status":"failed","step":"fetch","result":fetch}
  temp=Path(tempfile.mkdtemp(prefix="dore-dawn-publish-"));worktree=temp/"repo"
  try:
   add=_run(["git","worktree","add","--detach",str(worktree),"origin/main"],base,120)
   if add["returncode"]:return {"ok":False,"status":"failed","step":"worktree","result":add}
   evidence=_apply(worktree,admission,assets)
   _run(["git","config","user.name","Doré Publisher"],worktree);_run(["git","config","user.email","westsidewatchca@gmail.com"],worktree)
   paths=[evidence["record"],evidence["artifactDir"].lstrip("/"),"static/dawn-library/canonical-index.json","static/dawn-library/surfaces/dawn-storefront.json","static/dawn-library/surfaces/multiwrite-biblical-world.json"]
   stage=_run(["git","add","--"]+paths,worktree)
   if stage["returncode"]:return {"ok":False,"status":"failed","step":"stage","result":stage}
   quiet=_run(["git","diff","--cached","--quiet"],worktree)
   if quiet["returncode"]==0:return {"ok":True,"status":"completed","capability":"dawn.library.publish","idempotent":True,**evidence}
   commit=_run(["git","commit","-m",f"publish(dawn): {evidence['workId']}"],worktree)
   if commit["returncode"]:return {"ok":False,"status":"failed","step":"commit","result":commit}
   head=_run(["git","rev-parse","HEAD"],worktree)["stdout"].strip();push=_run(["git","push","origin","HEAD:main"],worktree,180)
   if push["returncode"]==0:return {"ok":True,"status":"completed","capability":"dawn.library.publish","idempotent":False,"commit":head,**evidence}
  except Exception as exc:
   return {"ok":False,"status":"failed","step":"publish","error":{"code":"publication_failed","message":str(exc)}}
  finally:
   if worktree.exists():_run(["git","worktree","remove","--force",str(worktree)],base,60)
   shutil.rmtree(temp,ignore_errors=True)
 return {"ok":False,"status":"failed","step":"push","error":{"code":"concurrent_main_updates","message":"publication push did not converge"}}

def execute(capability,args=None):
 if capability!="dawn.library.publish":return {"ok":False,"status":"failed","error":{"code":"unsupported_capability","message":capability}}
 return publish(args)
