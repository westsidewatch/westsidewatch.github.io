from __future__ import annotations

import sqlite3
from pathlib import Path

from dore_core.context.compiler import build_index_from_file
from dore_core.context.retrieve import retrieve_westside_context

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs/MASTER_SITE_ARCHITECTURE.md"


def test_question_form_recalls_cjk_heading() -> None:
    database = ROOT / ".tmp-westside-context-test.sqlite3"
    try:
        build_index_from_file(MASTER, database)
        with sqlite3.connect(database) as db:
            packets = retrieve_westside_context("多雷探索是什么意思？", db, limit=1)
        assert packets
        assert packets[0]["match"]["title"] == "9. 多雷探索 / Doré Exploration"
    finally:
        database.unlink(missing_ok=True)
