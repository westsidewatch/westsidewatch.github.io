#!/usr/bin/env python3
"""Runtime admission acceptance for writing.westside-dimensional-journalism."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

CAPABILITY = "writing.westside-dimensional-journalism"


def load(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"westside_runtime_acceptance_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


registry = load("capability_registry")
bindings = load("capability_bindings")
bus = load("capability_bus")
a2a = load("a2a_adapter")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class NoProduction:
    def execute(self, capability, args):
        raise AssertionError(f"writing capability must not route to production action: {capability}")


def main() -> None:
    descriptor = registry.get(CAPABILITY, include_planned=True)
    check(isinstance(descriptor, dict), "capability missing from canonical registry")
    check(descriptor.get("entrypoint") == "local/dore-local/westside_writing_capability.py", "wrong canonical entrypoint")
    check(descriptor.get("author_thesis_authority") is True, "author thesis authority missing")
    check(descriptor.get("may_rewrite_thesis") is False, "thesis rewrite boundary missing")

    binding = bindings.get(CAPABILITY)
    check(binding == {"kind": "native", "handler": CAPABILITY}, "native binding missing or wrong")
    authority = bindings.validate_authority(registry.discover(include_planned=True))
    check(authority.get("ok") is True, f"binding authority failed: {authority}")

    resolved = bus.resolve(CAPABILITY)
    check(resolved is not None and resolved.get("callable") is True, "capability bus does not expose callable skill")

    payload = {
        "text": "七天，沒有一個人開口。靜默和約伯的痛苦哪個更大似乎都不能被明辨。七天又過了一天，約伯發出了聲音。",
        "authorThesis": "約伯的沉默與聲音讓人的有限逐漸顯現。",
        "mode": "evaluate",
    }
    direct = bus.call(CAPABILITY, payload, NoProduction(), caller_product="journal")
    check(direct.get("ok") is True and direct.get("status") == "completed", f"direct bus call failed: {direct}")
    report = direct.get("report") or {}
    check(report.get("authorThesis") == payload["authorThesis"], "direct route lost author thesis")
    check((report.get("authority") or {}).get("mayRewriteThesis") is False, "direct route weakened thesis authority")
    check((direct.get("core_route") or {}).get("identity_source") == "dore-core/runtime/capability-registry.v1.json", "direct route lost canonical identity")

    envelope = {
        "protocol": "dore.a2a/1",
        "action": "dispatch",
        "request_id": "westside-writing-runtime-acceptance",
        "conversation_id": "westside-writing-runtime-acceptance",
        "session_id": "westside-writing-runtime-acceptance",
        "consumer_id": "journal",
        "capability_id": CAPABILITY,
        "payload": payload,
    }
    routed = a2a.handle_universal_envelope(envelope)
    check(isinstance(routed, dict), "A2A returned no response")
    check(routed.get("capability_id") == CAPABILITY, "A2A changed capability identity")
    check((routed.get("core_route") or {}).get("identity_authority") == "dore-core/runtime/capability-registry.v1.json", "A2A did not preserve canonical registry authority")
    check((routed.get("core_route") or {}).get("execution_binding") == "native", "A2A did not use native binding")
    check(routed.get("status") == "succeeded", f"A2A execution did not pass: {json.dumps(routed, ensure_ascii=False)}")
    a2a_report = ((routed.get("result") or {}).get("report") or {})
    check(a2a_report.get("authorThesis") == payload["authorThesis"], "A2A route lost author thesis")
    check((a2a_report.get("authority") or {}).get("mayRewriteThesis") is False, "A2A route weakened thesis authority")

    print(json.dumps({
        "schema": "dore.westside-writing-runtime-acceptance.v0",
        "status": "PASS",
        "capability": CAPABILITY,
        "registry": True,
        "binding": "native",
        "bus": "callable",
        "a2a": "succeeded",
        "provider_required_for_route_proof": False,
        "author_thesis_preserved": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
