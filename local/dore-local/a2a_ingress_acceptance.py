#!/usr/bin/env python3
"""Acceptance for 1C/2: public dore.call normalization into canonical Core."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load(name):
    path=HERE/f"{name}.py"
    spec=importlib.util.spec_from_file_location(f"dore_ingress_test_{name}",path)
    assert spec and spec.loader
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

ingress=load("a2a_ingress")
native=load("native_host")

raw={
    "capability":"bible.query-plan",
    "args":{"query":"約翰福音 7:38"},
    "caller_product":"acceptance",
    "request_id":"ingress-acceptance-1",
    "conversation_id":"conv-ingress",
    "session_id":"session-ingress",
    "transport":"unix-domain-socket",
}
envelope=ingress.normalize_public_call(raw)
result=native.route_payload(raw)

checks={
    "protocol_normalized":envelope.get("protocol")=="dore.a2a/1",
    "capability_renamed":envelope.get("capability_id")=="bible.query-plan" and "capability" not in envelope,
    "args_renamed":envelope.get("payload")==raw["args"] and "args" not in envelope,
    "identity_preserved":all(envelope.get(k)==raw[k] for k in ("request_id","conversation_id","session_id")),
    "consumer_bound":envelope.get("consumer_id")=="acceptance",
    "normalization_marked":bool((envelope.get("ingress") or {}).get("normalized")),
    "public_call_reaches_core":result.get("protocol")=="dore.a2a/1" and result.get("capability_id")=="bible.query-plan",
    "core_returns_typed_result":result.get("status")=="succeeded" and isinstance(result.get("result"),dict) and result["result"].get("ok") is True,
    "canonical_identity_authority":((result.get("core_route") or {}).get("identity_authority")=="dore-core/runtime/capability-registry.v1.json"),
    "binding_authority":((result.get("core_route") or {}).get("binding_authority")=="capability_bindings"),
}
ok=all(checks.values())
print(json.dumps({"ok":ok,"code":"DORE_A2A_PUBLIC_INGRESS_PASS" if ok else "DORE_A2A_PUBLIC_INGRESS_FAIL","checks":checks,"envelope":envelope,"result_route":result.get("core_route")},ensure_ascii=False,indent=2))
raise SystemExit(0 if ok else 1)
