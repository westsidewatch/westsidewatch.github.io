#!/usr/bin/env python3
"""Doré Local Agent Runtime v0: bounded repo execution substrate."""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
from typing import Any

CAPABILITY="engineering.repo-task";DEFAULT_REPO_NAME="westsidewatch.github.io";MAX_READ_BYTES=1_000_000;MAX_OUTPUT=12_000

def _repo()->Path:
 root=Path(os.environ.get("DORE_WORKTREE") or os.environ.get("DORE_REPO_ROOT") or Path.home()/DEFAULT_REPO_NAME).expanduser().resolve()
 if root.name!=DEFAULT_REPO_NAME or not (root/".git").exists():raise RuntimeError("repo_not_allowlisted")
 return root

def _inside(repo:Path,relative:str)->Path:
 if not relative or relative.startswith("/"):raise ValueError("relative_path_required")
 target=(repo/relative).resolve()
 if target!=repo and repo not in target.parents:raise ValueError("path_outside_repo")
 return target

def _run(repo:Path,argv:list[str],timeout:int=120)->dict[str,Any]:
 proc=subprocess.run(argv,cwd=repo,text=True,capture_output=True,timeout=timeout)
 return {"argv":argv,"returncode":proc.returncode,"stdout":proc.stdout[-MAX_OUTPUT:],"stderr":proc.stderr[-MAX_OUTPUT:]}

def _command(repo:Path,verb:str)->dict[str,Any]:
 commands={"status":["git","status","--short"],"diff":["git","diff","--"],"diff-check":["git","diff","--check"],"head":["git","rev-parse","HEAD"]};argv=commands.get(verb)
 if argv is None:return {"ok":False,"error":"command_not_allowlisted","verb":verb}
 result=_run(repo,argv);return {"ok":result["returncode"]==0,"result":result}

def _commit(repo:Path,args:dict[str,Any])->dict[str,Any]:
 message=str(args.get("message") or "").strip();raw_paths=args.get("paths")
 if not message or len(message)>200:raise ValueError("commit_message_required_or_too_long")
 if not isinstance(raw_paths,list) or not raw_paths or len(raw_paths)>20:raise ValueError("commit_paths_required")
 paths=[]
 for raw in raw_paths:
  target=_inside(repo,str(raw));rel=str(target.relative_to(repo))
  if not target.exists():raise ValueError("commit_path_missing:"+rel)
  paths.append(rel)
 check=_run(repo,["git","diff","--check","--",*paths])
 if check["returncode"]!=0:return {"ok":False,"status":"failed","capability":CAPABILITY,"error":"git_diff_check_failed","check":check}
 changed=_run(repo,["git","diff","--name-only","--",*paths])
 changed_paths=[x for x in changed["stdout"].splitlines() if x.strip()]
 if not changed_paths:return {"ok":False,"status":"failed","capability":CAPABILITY,"error":"no_tracked_changes_to_commit"}
 before=_command(repo,"head")
 commit=_run(repo,["git","commit","--only","-m",message,"--",*paths])
 after=_command(repo,"head")
 ok=commit["returncode"]==0 and after.get("ok") and before.get("ok") and after["result"]["stdout"].strip()!=before["result"]["stdout"].strip()
 return {"ok":ok,"status":"completed" if ok else "failed","capability":CAPABILITY,"paths":paths,"commit":commit,"head_before":before,"head_after":after}

def execute(args:dict[str,Any]|None=None)->dict[str,Any]:
 args=args or {}
 try:repo=_repo()
 except Exception as exc:return {"ok":False,"status":"failed","capability":CAPABILITY,"error":str(exc)}
 op=str(args.get("operation") or "inspect")
 try:
  if op=="inspect":
   status=_command(repo,"status");head=_command(repo,"head");return {"ok":status["ok"] and head["ok"],"status":"completed","capability":CAPABILITY,"repo":str(repo),"git_status":status,"head":head}
  if op=="read":
   path=_inside(repo,str(args.get("path") or ""))
   if not path.is_file():raise FileNotFoundError(str(path))
   if path.stat().st_size>MAX_READ_BYTES:raise ValueError("file_too_large")
   return {"ok":True,"status":"completed","capability":CAPABILITY,"path":str(path.relative_to(repo)),"content":path.read_text(encoding="utf-8")}
  if op=="write":
   path=_inside(repo,str(args.get("path") or ""));content=args.get("content")
   if not isinstance(content,str):raise ValueError("content_must_be_string")
   if len(content.encode("utf-8"))>MAX_READ_BYTES:raise ValueError("content_too_large")
   if not path.exists():raise ValueError("v0_refuses_new_file_write")
   before=path.read_text(encoding="utf-8");path.write_text(content,encoding="utf-8");check=_command(repo,"diff-check");diff=_command(repo,"diff")
   if not check["ok"]:
    path.write_text(before,encoding="utf-8");return {"ok":False,"status":"failed","capability":CAPABILITY,"error":"git_diff_check_failed","rolled_back":True,"check":check}
   return {"ok":True,"status":"completed","capability":CAPABILITY,"path":str(path.relative_to(repo)),"diff":diff,"check":check}
  if op=="verify":
   verb=str(args.get("verb") or "diff-check");result=_command(repo,verb);return {"ok":result["ok"],"status":"completed" if result["ok"] else "failed","capability":CAPABILITY,"verification":result}
  if op=="commit":return _commit(repo,args)
  return {"ok":False,"status":"failed","capability":CAPABILITY,"error":"operation_not_allowlisted","operation":op}
 except Exception as exc:return {"ok":False,"status":"failed","capability":CAPABILITY,"error":f"{type(exc).__name__}:{exc}"}

def main()->int:
 try:payload=json.loads(sys.stdin.read() or "{}")
 except json.JSONDecodeError as exc:print(json.dumps({"ok":False,"error":f"invalid_json:{exc}"}));return 2
 result=execute(payload);print(json.dumps(result,ensure_ascii=False,separators=(",",":")));return 0 if result.get("ok") else 1
if __name__=="__main__":raise SystemExit(main())
