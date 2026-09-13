#!/usr/bin/env python3
"""Acceptance for 1C/3: canonical capability execution is durably verified."""
from __future__ import annotations

import importlib.util
import json
import os
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
HOME=Path(tempfile.mkdtemp(prefix="dore-a2a-exec-"))
os.environ["DORE_LOCAL_HOME"]=str(HOME)
os.environ["DORE_A2A_WORKER_ID"]="acceptance-worker"

def load(name):
    path=HERE/f"{name}.py"
    spec=importlib.util.spec_from_file_location(f"dore_exec_test_{name}",path)
    assert spec and spec.loader
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

native=load("native_host")
plane=load("a2a_execution_plane")

raw={
    "capability":"bible.query-plan",
    "args":{"query":"約翰福音 7:38"},
    "caller_product":"execution-acceptance",
    "request_id":"durable-execution-1",
    "conversation_id":"conv-durable",
    "session_id":"session-durable",
    "transport":"unix-domain-socket",
}
first=native.route_payload(raw)
second=native.route_payload(raw)
execution=first.get("execution") or {}
task_id=execution.get("task_id")
status=plane.status(task_id) if task_id else {}
task=status.get("task") or {}

# Same request identity with different payload must fail closed rather than reuse work.
conflict=dict(raw);conflict["args"]={"query":"創世記 1:1"}
conflict_result=native.route_payload(conflict)

checks={
    "typed_core_result":first.get("protocol")=="dore.a2a/1" and first.get("status")=="succeeded",
    "execution_authority":((first.get("core_route") or {}).get("execution_authority")=="a2a_execution_plane"),
    "durable_pass":execution.get("execution_status")=="PASS",
    "completion_evidence":execution.get("completion_evidence") is True and status.get("completion_evidence") is True,
    "artifact_recorded":task.get("status")=="PASS" and isinstance(task.get("artifact"),dict) and bool(task["artifact"].get("sha256")),
    "verification_recorded":bool((task.get("verification") or {}).get("ok")),
    "replay_is_idempotent":((second.get("execution") or {}).get("replayed") is True and (second.get("execution") or {}).get("task_id")==task_id),
    "replay_keeps_completion":((second.get("execution") or {}).get("completion_evidence") is True),
    "identity_conflict_fails_closed":conflict_result.get("status")=="failed" and "identity_conflict" in str((conflict_result.get("error") or {}).get("message") or conflict_result).lower(),
}
ok=all(checks.values())
print(json.dumps({"ok":ok,"code":"DORE_A2A_DURABLE_EXECUTION_PASS" if ok else "DORE_A2A_DURABLE_EXECUTION_FAIL","checks":checks,"task_id":task_id,"task_status":task.get("status"),"artifact_sha256":(task.get("artifact") or {}).get("sha256"),"verification":task.get("verification"),"replay":(second.get("execution") or {}).get("replayed"),"conflict_status":conflict_result.get("status")},ensure_ascii=False,indent=2))
raise SystemExit(0 if ok else 1)
