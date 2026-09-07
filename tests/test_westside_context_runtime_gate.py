from __future__ import annotations

import sqlite3
from pathlib import Path

from dore_core.context.compiler import build_index
from dore_core.runtime.capability import discover_capability, invoke_capability


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "dore-core" / "runtime" / "capability-registry.v1.json"
ARCHITECTURE = ROOT / "docs" / "MASTER_SITE_ARCHITECTURE.md"


def test_dore_can_find_dore_exploration_through_runtime_capability():
    capability = discover_capability("westside.context", REGISTRY)

    assert capability["network"] is False
    assert capability["write_access"] is False
    assert capability["entrypoint"] == "dore_core.context.retrieve:retrieve_westside_context"

    db = sqlite3.connect(":memory:")
    build_index(db, ARCHITECTURE)

    packets = invoke_capability(
        "westside.context",
        "多雷探索是什么意思？",
        db=db,
        limit=1,
        registry_path=REGISTRY,
    )

    assert packets
    packet = packets[0]
    assert packet["match"]["title"] == "9. 多雷探索 / Doré Exploration"
    assert packet["path"][-1] == packet["match"]["node_id"]
    assert packet["match"]["source_path"] == "docs/MASTER_SITE_ARCHITECTURE.md"
    assert len(packet["match"]["source_sha256"]) == 64
    assert [node["title"] for node in packet["ancestors"]] == ["MASTER SITE ARCHITECTURE"]
