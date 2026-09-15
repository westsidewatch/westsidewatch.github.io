#!/usr/bin/env python3
"""Contract acceptance for the thin Doré Conversation Capability Gateway."""
from __future__ import annotations
import json
import conversation_gateway as gateway

CAPABILITY = "publishing.dimensional-writing"


def main() -> int:
    discovered = gateway.dispatch({"operation": "discover", "query": "dimensional-writing"})
    described = gateway.dispatch({"operation": "describe", "capability": CAPABILITY})
    descriptor = described.get("descriptor") or {}
    checks = {
        "gateway_schema": discovered.get("schema") == "dore.conversation-gateway/1",
        "discover_ok": discovered.get("ok") is True,
        "discover_finds_writing": CAPABILITY in json.dumps(discovered.get("capabilities") or [], ensure_ascii=False),
        "describe_ok": described.get("ok") is True,
        "canonical_identity": descriptor.get("id") == CAPABILITY,
        "author_thesis_authority": descriptor.get("author_thesis_authority") is True,
        "semantic_admission_required": descriptor.get("semantic_admission_required") is True,
    }
    passed = all(checks.values())
    print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
