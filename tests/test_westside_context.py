from __future__ import annotations

import sqlite3
import unittest

from dore_core.context.compiler import build_index, compile_markdown, search, search_context


ARCHITECTURE_FIXTURE = """# MASTER SITE ARCHITECTURE

## 1. Main Site

Living Water Westside Watch

## 2. Journal

Journal is the publication core.

### WALK

#### 以馬忤斯 Emmaus

同行入口、查經與共同學習工作台。

##### ONE

查經前哨站。

##### 多寫

寫作研究工作台。

## 3. News Broadcast

Cross-column function.
"""


class WestsideContextTests(unittest.TestCase):
    def test_compiler_preserves_hierarchy(self) -> None:
        nodes = compile_markdown(ARCHITECTURE_FIXTURE, "docs/MASTER_SITE_ARCHITECTURE.md")
        emmaus = next(n for n in nodes if "Emmaus" in n.title)
        one = next(n for n in nodes if n.title == "ONE")
        self.assertEqual(one.parent_id, emmaus.node_id)
        self.assertEqual(emmaus.level, 4)
        self.assertEqual(emmaus.source_path, "docs/MASTER_SITE_ARCHITECTURE.md")
        self.assertEqual(len(emmaus.source_sha256), 64)

    def test_fts_retrieves_relevant_context(self) -> None:
        db = sqlite3.connect(":memory:")
        build_index(ARCHITECTURE_FIXTURE, db, "docs/MASTER_SITE_ARCHITECTURE.md")
        results = search(db, "查經前哨站", limit=3)
        self.assertTrue(results)
        self.assertEqual(results[0].title, "ONE")

    def test_cjk_substring_fallback_retrieves_context(self) -> None:
        db = sqlite3.connect(":memory:")
        build_index(ARCHITECTURE_FIXTURE, db, "docs/MASTER_SITE_ARCHITECTURE.md")
        results = search(db, "查經與共同學習", limit=3)
        self.assertTrue(results)
        self.assertEqual(results[0].title, "以馬忤斯 Emmaus")

    def test_context_packet_recovers_canonical_ancestors(self) -> None:
        db = sqlite3.connect(":memory:")
        build_index(ARCHITECTURE_FIXTURE, db, "docs/MASTER_SITE_ARCHITECTURE.md")
        packets = search_context(db, "查經前哨站", limit=1)
        self.assertEqual(len(packets), 1)
        self.assertEqual(packets[0].match.title, "ONE")
        self.assertEqual([node.title for node in packets[0].ancestors], [
            "MASTER SITE ARCHITECTURE",
            "2. Journal",
            "WALK",
            "以馬忤斯 Emmaus",
        ])

    def test_empty_query_does_not_touch_search(self) -> None:
        db = sqlite3.connect(":memory:")
        build_index(ARCHITECTURE_FIXTURE, db)
        self.assertEqual(search(db, ""), [])
        self.assertEqual(search(db, "   "), [])
        self.assertEqual(search_context(db, ""), [])


if __name__ == "__main__":
    unittest.main()
