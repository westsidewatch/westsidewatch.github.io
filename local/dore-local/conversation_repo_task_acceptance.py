#!/usr/bin/env python3
"""End-to-end acceptance for conversation -> A2A -> repo-task execution."""
from __future__ import annotations
import json,os,subprocess,tempfile
from pathlib import Path
import conversation_gateway as gateway
CAPABILITY="engineering.repo-task"
def git(repo:Path,*args:str)->str:return subprocess.run(["git","-C",str(repo),*args],check=True,text=True,capture_output=True).stdout.strip()
def call(args:dict,request_id:str):return gateway.call(CAPABILITY,args,conversation_id="repo-task-e2e",session_id="repo-task-e2e",request_id=request_id)
def main()->int:
 with tempfile.TemporaryDirectory(prefix="dore-conversation-repo-") as tmp:
  repo=Path(tmp)/"westsidewatch.github.io";repo.mkdir();git(repo,"init","-q");git(repo,"config","user.email","dore@example.invalid");git(repo,"config","user.name","DoreConversationAcceptance")
  specimen=repo/"specimen.txt";specimen.write_text("before\n",encoding="utf-8");git(repo,"add","specimen.txt");git(repo,"commit","-qm","init");initial_head=git(repo,"rev-parse","HEAD")
  old=os.environ.get("DORE_WORKTREE");os.environ["DORE_WORKTREE"]=str(repo)
  try:
   discovered=gateway.discover();caps=discovered.get("capabilities") or [];found=any(x.get("id")==CAPABILITY and x.get("callable") is True for x in caps)
   described=gateway.describe(CAPABILITY);descriptor=described.get("descriptor") or {};callable_descriptor=described.get("ok") is True and descriptor.get("callable") is True
   inspected=call({"operation":"inspect"},"repo-task-e2e-inspect");read=call({"operation":"read","path":"specimen.txt"},"repo-task-e2e-read");escape=call({"operation":"read","path":"../outside.txt"},"repo-task-e2e-escape");write=call({"operation":"write","path":"specimen.txt","content":"after\n"},"repo-task-e2e-write");verify=call({"operation":"verify","verb":"diff-check"},"repo-task-e2e-verify");commit=call({"operation":"commit","paths":["specimen.txt"],"message":"test: Doré repo task acceptance"},"repo-task-e2e-commit")
   final_head=git(repo,"rev-parse","HEAD");committed_content=git(repo,"show","HEAD:specimen.txt")
   checks={"discover_callable":found,"describe_callable":callable_descriptor,"inspect":inspected.get("ok") is True,"read":read.get("ok") is True,"path_escape_rejected":escape.get("ok") is False,"write":write.get("ok") is True,"diff_check":verify.get("ok") is True,"commit":commit.get("ok") is True,"commit_created":final_head!=initial_head,"committed_content":committed_content=="after"}
   ok=all(checks.values());print(json.dumps({"ok":ok,"capability":CAPABILITY,"path":"conversation-gateway->native-host->a2a->capability-bus->repo-task-runtime","checks":checks,"head":final_head},separators=(",",":")));return 0 if ok else 1
  finally:
   if old is None:os.environ.pop("DORE_WORKTREE",None)
   else:os.environ["DORE_WORKTREE"]=old
if __name__=="__main__":raise SystemExit(main())
