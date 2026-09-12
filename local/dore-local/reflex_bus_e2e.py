#!/usr/bin/env python3
"""End-to-end boundary gate for Doré Reflex through the canonical capability bus."""
from __future__ import annotations

import base64
from pathlib import Path
import tempfile

import capability_bus
from capability_registry import get


class ProductionStub:
    CAPABILITIES: set[str] = set()

    @staticmethod
    def execute(_capability: str, _args: dict) -> dict:
        raise AssertionError("reflex.project must not fall through to production actions")


SOURCE = {
    "mime": "text/markdown",
    "name": "job-friends.md",
    "canonicalId": "dawn:work:test-job-friends",
    "sourcePointer": "dawn:edition:test-job-friends#body",
}
PAYLOAD = b"# Job and His Friends\n\nEliphaz speaks from received wisdom.\n"


def request(intent: str) -> dict:
    return {
        "intent": intent,
        "source": dict(SOURCE),
        "payloadBase64": base64.b64encode(PAYLOAD).decode("ascii"),
    }


def main() -> None:
    production = ProductionStub()

    registered = get("reflex.project")
    assert registered is not None
    assert registered["status"] == "existing"
    assert registered["execution"] == "core-adapter"
    assert registered["authority"] is False
    assert registered["identity_source"] is False
    assert registered["persistence"] == "request-scoped-none"

    discovered = [item for item in capability_bus.discover(production) if item["id"] == "reflex.project"]
    assert len(discovered) == 1
    descriptor = discovered[0]
    assert descriptor["callable"] is True
    assert descriptor["owner"] == "dore-core"
    assert descriptor["identity_source"] is False

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        before = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
        schemas = set()

        for intent in ("text.search", "publishing.structure", "design.structure"):
            result = capability_bus.call(
                "reflex.project",
                request(intent),
                production,
                caller_product="multiwrite",
            )
            assert result["ok"] is True, result
            assert result["status"] == "completed"
            assert result["capability"] == "reflex.project"
            assert result["source"]["canonicalId"] == SOURCE["canonicalId"]
            assert result["source"]["sourcePointer"] == SOURCE["sourcePointer"]
            assert result["core_route"] == {
                "capability": "reflex.project",
                "caller_product": "multiwrite",
                "provider": "dore-core",
                "transport": "core-adapter",
            }
            assert "events" not in result
            assert "session" not in result
            assert "reflex" not in result
            assert "payloadBase64" not in result
            projection = result["projection"]
            schemas.add(projection["schema"])

        assert len(schemas) == 3
        after = sorted(str(path.relative_to(root)) for path in root.rglob("*"))
        assert before == after, "capability bus must not persist Reflex state"

    invalid = capability_bus.call(
        "reflex.project",
        {"intent": "not.real", "source": SOURCE, "payloadBase64": ""},
        production,
        caller_product="dawn",
    )
    assert invalid["ok"] is False
    assert invalid["error"]["code"] == "unsupported_intent"
    assert invalid["core_route"]["capability"] == "reflex.project"

    unknown = capability_bus.call("reflex.does-not-exist", {}, production)
    assert unknown["ok"] is False
    assert unknown["error"]["code"] == "capability_not_found"

    print("DORE_REFLEX_BUS_E2E=PASS")


if __name__ == "__main__":
    main()
