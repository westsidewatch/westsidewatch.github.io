#!/usr/bin/env python3
"""Bounded real-Mac acceptance for Doré Christian ministry dialogue rails."""
from __future__ import annotations
import json
import os
import subprocess
import urllib.request
import uuid
from pathlib import Path

CAPABILITIES={"theology.live.acceptance"}


def _repo()->Path:
    return Path(os.environ.get("DORE_WORKTREE") or Path.home()/"westsidewatch.github.io").expanduser().resolve()


def _run(argv:list[str],cwd:Path,timeout:int=300)->dict:
    p=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
    return {"returncode":p.returncode,"stdout":p.stdout[-5000:],"stderr":p.stderr[-5000:]}


def _post(message:str,conversation_id:str)->dict:
    payload=json.dumps({"message":message,"conversation_id":conversation_id,"project_id":"dore-theology-acceptance"},ensure_ascii=False).encode()
    req=urllib.request.Request("http://127.0.0.1:8788/chat",data=payload,method="POST",headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=360) as response:
        return json.loads(response.read().decode("utf-8"))


def _positive_close(text:str)->bool:
    import re
    t=(text or '').strip()
    close=t[-180:]
    christ=bool(re.search(r'耶[穌稣].{0,10}基督|Jesus\s+Christ|in\s+(?:the\s+)?name\s+of\s+Jesus',close,re.I))
    amen=bool(re.search(r'(?:阿們|阿们|Amen)[。.!！\s]*$',t,re.I))
    return christ and amen


def execute(capability:str,args=None):
    if capability not in CAPABILITIES:
        return {"ok":False,"status":"failed","error":{"code":"unsupported_action","message":capability}}
    repo=_repo()
    installer=repo/"local"/"dore-local"/"install-launchagent.sh"
    if not installer.is_file():
        return {"ok":False,"status":"failed","error":{"code":"installer_missing","message":str(installer)}}
    install=_run(["bash",str(installer)],repo,300)
    if install["returncode"]!=0:
        return {"ok":False,"status":"failed","stage":"install","stderr_tail":install["stderr"][-2000:]}
    try:
        health=json.loads(urllib.request.urlopen("http://127.0.0.1:8788/health",timeout=20).read().decode())
        zh=_post("請為今天的查經聚會寫一篇簡短禱告",str(uuid.uuid4()))
        en=_post("Please write a short Christian prayer for today's Bible study.",str(uuid.uuid4()))
        compare=_post("請從歷史角度比較不同宗教的禱告傳統。",str(uuid.uuid4()))
    except Exception as exc:
        return {"ok":False,"status":"failed","stage":"dialogue","error":{"code":"local_dialogue_error","message":str(exc)}}
    zh_reply=str(zh.get("reply") or '')
    en_reply=str(en.get("reply") or '')
    compare_reply=str(compare.get("reply") or '')
    compare_blocked="沒有通過基督教事工內容的權威邊界" in compare_reply
    checks={
        "health":bool(health.get("ok")),
        "model":health.get("model"),
        "guarded_entrypoint":("DORE_LOCAL_GUARDED_ENTRYPOINT=" in install["stdout"]),
        "zh_prayer_ok":bool(zh.get("ok")) and _positive_close(zh_reply),
        "en_prayer_ok":bool(en.get("ok")) and _positive_close(en_reply),
        "comparative_allowed":bool(compare.get("ok")) and not compare_blocked and bool(compare_reply.strip()),
        "local_endpoint":True,
    }
    ok=all(v for k,v in checks.items() if k!="model") and str(checks.get("model") or '').startswith("gemma4:")
    return {
        "ok":ok,
        "status":"completed" if ok else "failed",
        "capability":capability,
        "checks":checks,
        "evidence":{
            "installer_returncode":install["returncode"],
            "guarded_entrypoint_declared":checks["guarded_entrypoint"],
            "zh_reply_admitted":checks["zh_prayer_ok"],
            "en_reply_admitted":checks["en_prayer_ok"],
            "comparative_context_allowed":checks["comparative_allowed"],
        },
    }
