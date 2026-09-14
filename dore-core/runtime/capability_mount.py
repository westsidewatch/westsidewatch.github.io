"""Truthful Doré Arsenal mount / execute bridge.

A capability is never credited merely because its id appears in a loadout or a
prompt.  Lifecycle evidence is explicit:

selected -> mounted -> executed -> consumed

Capabilities without an executable bridge remain selected-not-mounted.  The
currently executing root capability is never recursively invoked.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

from dore_core.context.compiler import build_index
from dore_core.context.retrieve import retrieve_westside_context


def _digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _query(request: dict[str, Any]) -> str:
    parts = [
        str(request.get("task_context") or "").strip(),
        str(request.get("surface_family") or request.get("consumer") or "").strip(),
        str(request.get("primary_axis") or "").strip(),
    ]
    return " ".join(part for part in parts if part)[:1200] or "Westside identity context"


def _westside_context(request: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    source = repo_root / "docs" / "MASTER_SITE_ARCHITECTURE.md"
    if not source.exists():
        raise FileNotFoundError("westside_context_source_missing")
    markdown = source.read_text(encoding="utf-8")
    with sqlite3.connect(":memory:") as db:
        source_sha = build_index(markdown, db, str(source.relative_to(repo_root)))
        packets = retrieve_westside_context(_query(request), db, limit=4)
    return {
        "ok": True,
        "status": "completed",
        "capability": "westside.context",
        "authority": False,
        "source_authority": True,
        "source_sha256": source_sha,
        "packets": packets,
    }


def _bus_call(capability_id: str, request: dict[str, Any], caller_product: str | None) -> dict[str, Any]:
    # capability_bus is intentionally imported lazily.  On real Doré runtimes
    # local/dore-local is already on sys.path; tests may inject an executor map.
    import capability_bus

    query = _query(request)
    if capability_id == "knowledge.recall":
        args = {"query": query, "mode": "strict", "project": "dore"}
    elif capability_id == "image.generate":
        args = {
            "prompt": (
                "Create one text-free visual material study for a web design exploration. "
                "Treat authored identity and content as immutable authority. "
                f"Design context: {query}. Avoid logos, invented people, invented ministries, "
                "religious stock cliches, quotations, and readable text."
            ),
            "purpose": "design-material-study",
            "consumer": caller_product or "dore-core",
        }
    else:
        args = {"query": query}
    return capability_bus.call(capability_id, args, None, caller_product=caller_product)


def execute_loadout(
    plan: dict[str, Any],
    request: dict[str, Any],
    *,
    repo_root: Path,
    current_capability: str,
    caller_product: str | None = None,
    executors: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Mount and execute the selected Arsenal loadout with auditable lifecycle.

    `executors` is a narrow test/host injection surface.  Production execution
    otherwise uses canonical local adapters.  Outputs are request-scoped only.
    """
    executors = dict(executors or {})
    weapons = list(((plan.get("loadout") or {}).get("weapons") or []))
    lifecycle: list[dict[str, Any]] = []
    outputs: dict[str, Any] = {}

    for weapon in weapons:
        capability_id = str(weapon.get("id") or "")
        roles = list(weapon.get("roles") or [])
        record: dict[str, Any] = {
            "capability": capability_id,
            "roles": roles,
            "selected": True,
            "mounted": False,
            "executed": False,
            "consumed": False,
            "state": "selected",
        }
        if capability_id == current_capability:
            record.update({
                "mounted": True,
                "executed": True,
                "state": "root-executing",
                "mount_adapter": "current-capability",
                "reason": "self-recursion-forbidden",
            })
            lifecycle.append(record)
            continue

        executor = executors.get(capability_id)
        mount_adapter = "injected-executor" if executor else None
        if executor is None and capability_id == "westside.context":
            executor = lambda req: _westside_context(req, repo_root)
            mount_adapter = "dore_core.context.retrieve"
        elif executor is None and capability_id in {"knowledge.recall", "image.generate"}:
            executor = lambda req, cid=capability_id: _bus_call(cid, req, caller_product)
            mount_adapter = "local.capability_bus"

        if executor is None:
            record.update({"state": "selected-not-mounted", "reason": "no-execution-bridge"})
            lifecycle.append(record)
            continue

        record.update({"mounted": True, "state": "mounted", "mount_adapter": mount_adapter})
        try:
            result = executor(request)
            if not isinstance(result, dict):
                raise TypeError("capability_result_must_be_object")
            if result.get("ok") is False or str(result.get("status") or "").lower() in {"failed", "not_ready"}:
                record.update({
                    "executed": True,
                    "state": "executed-no-output",
                    "reason": str(((result.get("error") or {}).get("code") if isinstance(result.get("error"), dict) else result.get("error")) or result.get("status") or "capability-returned-no-output"),
                    "output_sha256": _digest(result),
                })
            else:
                digest = _digest(result)
                outputs[capability_id] = result
                record.update({"executed": True, "state": "executed", "output_sha256": digest})
        except Exception as exc:
            record.update({
                "executed": True,
                "state": "execution-failed",
                "reason": f"{type(exc).__name__}:{exc}",
            })
        lifecycle.append(record)

    return {
        "schema": "dore.capability-mount-evidence.v0",
        "current_capability": current_capability,
        "caller_product": caller_product,
        "no_self_recursion": not any(
            row["capability"] == current_capability and row.get("mount_adapter") != "current-capability"
            for row in lifecycle
        ),
        "lifecycle": lifecycle,
        "outputs": outputs,
    }


def mark_consumed(evidence: dict[str, Any], capability_ids: list[str], consumer: str) -> dict[str, Any]:
    """Mark only already-executed outputs as consumed by a named downstream stage."""
    ids = set(capability_ids)
    out = json.loads(json.dumps(evidence, ensure_ascii=False))
    available = set((out.get("outputs") or {}).keys())
    for row in out.get("lifecycle") or []:
        cid = str(row.get("capability") or "")
        if cid in ids and cid in available and row.get("executed"):
            row["consumed"] = True
            row["state"] = "consumed"
            row["consumed_by"] = consumer
    return out
