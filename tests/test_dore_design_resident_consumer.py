from __future__ import annotations

import io
import json
import unittest
from unittest.mock import patch

from dore_core.capabilities.model import ArtifactRef, TaskState
from dore_core.capabilities.resident_design import design_compose_handler, design_verify_handler


class _Response:
    def __init__(self, payload):
        self.payload = payload
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return json.dumps(self.payload).encode("utf-8")


class ResidentDesignConsumerTest(unittest.TestCase):
    @patch("dore_core.capabilities.resident_design.request.urlopen")
    def test_live_gate_reaches_resident_without_mutating(self, urlopen):
        urlopen.return_value = _Response({"ok": True, "document_id": "westside-watch", "revision": 8})
        inputs = {"asset_candidate": ArtifactRef(id="a", schema="asset_candidate", payload={"asset_id": "gate"})}
        out = design_compose_handler(None, inputs, TaskState("t"))["design_patch"]
        self.assertFalse(out["applied"])
        self.assertTrue(out["verified"])
        self.assertEqual(out["workspace"], "westside-watch")
        self.assertIn("/api/verify", urlopen.call_args.args[0])

    @patch("dore_core.capabilities.resident_design.request.urlopen")
    def test_real_mutation_requires_revision_advance_and_verify(self, urlopen):
        urlopen.side_effect = [
            _Response({"ok": True, "document_id": "westside-watch", "revision": 8}),
            _Response({"schema": "dore.design.workspace.v1", "revision": 9}),
            _Response({"ok": True, "document_id": "westside-watch", "revision": 9, "page_render_sha256": {"cover": "abc"}}),
        ]
        inputs = {"asset_candidate": ArtifactRef(id="a", schema="asset_candidate", payload={
            "asset_id": "real",
            "workspace_mutation": {"op": "add_text", "page_id": "cover", "text": "A2A production"},
        })}
        out = design_compose_handler(None, inputs, TaskState("t"))["design_patch"]
        self.assertTrue(out["applied"])
        self.assertTrue(out["verified"])
        self.assertEqual(out["revision_before"], 8)
        self.assertEqual(out["revision_after"], 9)
        self.assertEqual(out["render_sha256"]["cover"], "abc")

    @patch("dore_core.capabilities.resident_design.request.urlopen")
    def test_verify_reads_real_workspace_verification(self, urlopen):
        urlopen.return_value = _Response({"ok": True, "document_id": "westside-watch", "revision": 9, "checks": {"render_all_pages": True}, "page_render_sha256": {"cover": "abc"}})
        inputs = {"design_patch": ArtifactRef(id="p", schema="design_patch", payload={"operation": "add_text"})}
        out = design_verify_handler(None, inputs, TaskState("t"))["verification_result"]
        self.assertTrue(out["real_render_verified"])
        self.assertEqual(out["resident_workspace"], "westside-watch")
        self.assertTrue(out["checks"]["render_all_pages"])


if __name__ == "__main__":
    unittest.main()
