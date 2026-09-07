"""Integration checks for the minimal Context -> Doré boundary."""
from __future__ import annotations

import sqlite3
import unittest

from dore_core.context.compiler import build_index
from dore_core.context.retrieve import retrieve_westside_context


class ContextRetrieveIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = sqlite3.connect(":memory:")
        self.source = """# Main Site\n\n## Journal\n\n### WALK\n\n#### 以馬忤斯 Emmaus\n\nONE is the Bible study reconnaissance station.\n\n## 橄欖山 / Mount of Olives\n\n### 黎明書局 / Dawn Library\n\nResource curation and knowledge context.\n"""
        self.sha = build_index(self.source, self.db, "docs/MASTER_SITE_ARCHITECTURE.md")

    def tearDown(self) -> None:
        self.db.close()

    def test_query_to_context_packet_preserves_structure(self) -> None:
        packets = retrieve_westside_context("ONE 查經前哨站", self.db)
        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(packet["match"]["title"], "以馬忤斯 Emmaus")
        self.assertEqual([n["title"] for n in packet["ancestors"]], ["Main Site", "Journal", "WALK"])
        self.assertEqual(packet["path"], [n["node_id"] for n in packet["ancestors"]] + [packet["match"]["node_id"]])
        self.assertEqual(packet["match"]["source_sha256"], self.sha)

    def test_adapter_is_read_only_and_bounded(self) -> None:
        packets = retrieve_westside_context("Journal", self.db, limit=1)
        self.assertEqual(len(packets), 1)
        self.assertNotIn("update", packets[0])
        self.assertNotIn("write", packets[0])
        self.assertNotIn("delete", packets[0])
        count = self.db.execute("SELECT COUNT(*) FROM context_nodes").fetchone()[0]
        self.assertEqual(count, 7)


if __name__ == "__main__":
    unittest.main()
