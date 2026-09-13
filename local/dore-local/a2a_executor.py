#!/usr/bin/env python3
"""Universal durable execution wrapper for canonical Doré capabilities.

Every normal canonical capability call must pass through this layer after ingress
normalization and identity/binding resolution. Transport success is never treated as
execution completion.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Callable


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def _task_id(envelope: dict[str, Any]) -> str:
    identity = {
        "request_id": envelope.get("request_id"),
        "conversation_id": envelope.get("conversation_id"),
        "session_id": envelope.get("session_id"),
        "consumer_id": envelope.get("consumer_id"),
    }
    return "cap-" + _digest(identity)[:32]


def _message(envelope: dict[str, Any], task_id: str) -> dict[str, Any]:
    return {
        "message_id": task_id,
        "kind": "capability.call",
        "related_goal": envelope.get("conversation_id"),
        "request_id": envelope.get("request_id"),
        "conversation_id": envelope.get("conversation_id"),
        "session_id": envelope.get("session_id"),
        "consumer_id": envelope.get("consumer_id"),
        "capability_id": envelope.get("capability_id"),
        "payload": envelope.get("payload") or {},
    }


def execute(
    envelope: dict[str, Any],
    descriptor: dict[str, Any],
    binding: dict[str, Any],
    provider_call: Callable[[], dict[str, Any]],
    *,
    plane: Any,
) -> dict[str, Any]:
    """Run one canonical capability with durable claim/artifact/verify/complete truth."""
    task_id = _task_id(envelope)
    message = _message(envelope, task_id)
    task = plane.register(message)

    # Exact replay of a verified completion is idempotent and never re-executes provider work.
    if task.get("status") == "PASS":
        status = plane.status(task_id)
        return {
            "ok": True,
            "task_id": task_id,
            "execution_status": "PASS",
            "completion_evidence": bool(status.get("completion_evidence")),
            "replayed": True,
            "result": task.get("result"),
            "artifact": task.get("artifact"),
            "verification": task.get("verification"),
        }

    owner = f"universal:{envelope.get('consumer_id') or 'dore'}"
    claimed = plane.claim(task_id, consumer=owner)
    if not claimed.get("ok"):
        current = claimed.get("task") or task
        return {
            "ok": False,
            "task_id": task_id,
            "execution_status": current.get("status"),
            "completion_evidence": False,
            "error": {"code": claimed.get("code") or "claim_failed"},
        }

    running = plane.transition(task_id, "RUNNING", consumer=owner)
    if not running.get("ok"):
        return {"ok": False, "task_id": task_id, "execution_status": "UNKNOWN", "completion_evidence": False, "error": {"code": running.get("code") or "running_transition_failed"}}

    # Side-effecting operations may not be generically declared verified. They remain
    # fail-closed until their explicit verification contract is migrated into Core.
    if descriptor.get("requires_verified_execution") is True and not descriptor.get("verification_contract"):
        failed = plane.transition(task_id, "FAIL", consumer=owner, result={"ok": False, "error": {"code": "verification_contract_required"}})
        return {
            "ok": False,
            "task_id": task_id,
            "execution_status": "FAIL",
            "completion_evidence": False,
            "error": {"code": "verification_contract_required", "message": "side-effect capability requires an explicit verification contract before execution"},
            "task": failed.get("task"),
        }

    try:
        result = provider_call()
    except Exception as exc:
        plane.transition(task_id, "FAIL", consumer=owner, result={"ok": False, "error": {"code": "provider_exception", "message": str(exc)}})
        return {"ok": False, "task_id": task_id, "execution_status": "FAIL", "completion_evidence": False, "error": {"code": "provider_exception", "message": str(exc)}}

    semantic_ok = bool(isinstance(result, dict) and result.get("ok") is True and str(result.get("status") or "completed").lower() not in {"failed", "error"})
    if not semantic_ok:
        plane.transition(task_id, "FAIL", consumer=owner, result=result if isinstance(result, dict) else {"value": result})
        return {"ok": False, "task_id": task_id, "execution_status": "FAIL", "completion_evidence": False, "result": result}

    artifact = {
        "schema": "dore.a2a-capability-result-artifact.v1",
        "capability_id": envelope.get("capability_id"),
        "request_id": envelope.get("request_id"),
        "result_sha256": _digest(result),
        "result": result,
    }
    recorded = plane.record_artifact(task_id, artifact, consumer=owner)
    if not recorded.get("ok"):
        return {"ok": False, "task_id": task_id, "execution_status": "UNKNOWN", "completion_evidence": False, "error": {"code": recorded.get("code") or "artifact_record_failed"}, "result": result}

    verification = {
        "ok": True,
        "strategy": "deterministic-handler-result-v1",
        "capability_id": envelope.get("capability_id"),
        "result_sha256": artifact["result_sha256"],
        "binding_kind": binding.get("kind"),
    }
    verified = plane.verify(task_id, verification, consumer=owner)
    if not verified.get("ok"):
        return {"ok": False, "task_id": task_id, "execution_status": "FAIL", "completion_evidence": False, "result": result, "verification": verified.get("task", {}).get("verification")}

    completed = plane.complete(task_id, result=result, consumer=owner)
    status = plane.status(task_id)
    return {
        "ok": bool(completed.get("ok") and status.get("completion_evidence")),
        "task_id": task_id,
        "execution_status": (status.get("task") or {}).get("status"),
        "completion_evidence": bool(status.get("completion_evidence")),
        "replayed": False,
        "result": result,
        "artifact": (status.get("task") or {}).get("artifact"),
        "verification": (status.get("task") or {}).get("verification"),
    }
