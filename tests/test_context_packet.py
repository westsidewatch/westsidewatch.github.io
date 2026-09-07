from __future__ import annotations

import sqlite3
import unittest

from dore_core.context.compiler import build_index, search_context
from dore_core.context.packet import packet_dict


class ContextPacketTests(unittest.TestCase):
    def test_packet_preserves_ancestry_and_provenance(self) -> None:
        markdown = """# Main Site\n## Journal\n### WALK\n#### 以馬忤斯 Emmaus\nONE is the Bible study reconnaissance station.\n"""
        db = sqlite3.connect(":memory:")
        source_sha = build_index(markdown, db, "docs/MASTER_SITE_ARCHITECTURE.md")
        packets = search_context(db, "ONE 查經前哨站")
        self.assertTrue(packets)
        packet = next(p for p in packets if p.match.title == "以馬忤斯 Emmaus")
        data = packet_dict(packet)
        self.assertEqual([n["title"] for n in data["ancestors"]], ["Main Site", "Journal", "WALK"])
        self.assertEqual(data["match"]["title"], "以馬忤斯 Emmaus")
        self.assertEqual(data["match"]["source_sha256"], source_sha)
        self.assertEqual(data["path"], [n.node_id for n in packet.ancestors] + [packet.match.node_id])

    def test_packet_is_not_a_write_path(self) -> None:
        markdown = "# Main Site\n## Journal\n"
        db = sqlite3.connect(":memory:")
        build_index(markdown, db)
        packet = search_context(db, "Journal")[0]
        data = packet_dict(packet)
        self.assertNotIn("update", data)
        self.assertNotIn("write", data)


if __name__ == "__main__":
    unittest.main()
