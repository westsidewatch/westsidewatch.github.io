import hashlib
import sqlite3
import unittest
from pathlib import Path

from dore_core.context.compiler import build_index
from dore_core.context.retrieve import retrieve_westside_context


class WestsideContextRetrieveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = Path("docs/MASTER_SITE_ARCHITECTURE.md")
        self.markdown = self.source.read_text(encoding="utf-8")
        self.db = sqlite3.connect(":memory:")
        build_index(self.markdown, self.db, str(self.source))

    def tearDown(self) -> None:
        self.db.close()

    def test_adapter_returns_bounded_provenance_preserving_packet(self) -> None:
        packets = retrieve_westside_context("ONE 查經前哨站", self.db, limit=1)
        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(packet["match"]["title"], "以馬忤斯 Emmaus")
        self.assertEqual(
            [node["title"] for node in packet["ancestors"]],
            ["Living Water Westside Watch", "2. Journal", "WALK"],
        )
        self.assertEqual(
            packet["match"]["source_sha256"],
            hashlib.sha256(self.markdown.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(
            packet["path"],
            [node["node_id"] for node in packet["ancestors"]] + [packet["match"]["node_id"]],
        )

    def test_adapter_is_read_only_data_boundary(self) -> None:
        packet = retrieve_westside_context("多雷探索", self.db, limit=1)[0]
        serialized = repr(packet)
        self.assertNotIn("update_file", serialized)
        self.assertNotIn("write_architecture", serialized)
        self.assertNotIn("supabase", serialized.lower())

    def test_limit_is_enforced(self) -> None:
        packets = retrieve_westside_context("Journal", self.db, limit=2)
        self.assertLessEqual(len(packets), 2)


if __name__ == "__main__":
    unittest.main()
