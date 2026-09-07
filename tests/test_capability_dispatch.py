"""End-to-end proof that Doré Runtime can invoke Westside Context."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from dore_core.context.compiler import build_index_from_file
from dore_core.runtime.capability import discover_capability, invoke_capability

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs/MASTER_SITE_ARCHITECTURE.md"


def test_westside_context_is_discoverable() -> None:
    capability = discover_capability("westside.context")
    assert capability["entrypoint"] == "dore_core.context.retrieve:retrieve_westside_context"
    assert capability["network"] is False
    assert capability["write_access"] is False


def test_runtime_can_answer_where_dore_exploration_is_defined(tmp_path: Path) -> None:
    database = tmp_path / "westside-context.sqlite3"
    build_index_from_file(MASTER, database)

    with sqlite3.connect(database) as db:
        packets = invoke_capability("westside.context", "多雷探索是什么意思？", db=db, limit=4)

    assert packets
    match = packets[0]["match"]
    assert match["title"] == "9. 多雷探索 / Doré Exploration"
    assert [node["title"] for node in packets[0]["ancestors"]] == ["MASTER SITE ARCHITECTURE"]
    assert match["source_path"].endswith("docs/MASTER_SITE_ARCHITECTURE.md")
    assert len(match["source_sha256"]) == 64
