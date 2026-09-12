from __future__ import annotations

import unittest
from unittest.mock import patch

from dore_core.capabilities import resident_design


GOOD = {
    "ok": True,
    "service": "dore-design",
    "version": "2.0",
    "entrypoint": "dore-design/app_design2.py",
    "branch": "dore/candidate01-visual-graph-experiment",
    "commit": "abc123",
    "workspace_id": "westside-watch",
    "workspace_revision": 42,
    "port": 4310,
}


class RuntimeIdentityCapabilityTest(unittest.TestCase):
    def test_accepts_design2_identity(self):
        with patch.object(resident_design, "_json_get", return_value=dict(GOOD)):
            identity = resident_design._runtime_identity({"workspace_id": "westside-watch"})
        self.assertEqual(identity["version"], "2.0")

    def test_rejects_design1(self):
        with patch.object(resident_design, "_json_get", return_value=dict(GOOD, version="1.0")):
            with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
                resident_design._runtime_identity()

    def test_rejects_wrong_entrypoint(self):
        with patch.object(resident_design, "_json_get", return_value=dict(GOOD, entrypoint="dore-design/app_design.py")):
            with self.assertRaisesRegex(RuntimeError, "entrypoint"):
                resident_design._runtime_identity()

    def test_rejects_stale_expected_commit(self):
        with patch.object(resident_design, "_json_get", return_value=dict(GOOD)):
            with self.assertRaisesRegex(RuntimeError, "precondition failed"):
                resident_design._runtime_identity({"commit": "newer456"})

    def test_rejects_wrong_workspace(self):
        with patch.object(resident_design, "_json_get", return_value=dict(GOOD)):
            with self.assertRaisesRegex(RuntimeError, "workspace_id"):
                resident_design._runtime_identity({"workspace_id": "candidate-other"})

    def test_filters_unknown_preconditions(self):
        asset = {"runtime_precondition": {"commit": "abc123", "workspace_id": "westside-watch", "ignored": True}}
        self.assertEqual(
            resident_design._runtime_precondition(asset),
            {"commit": "abc123", "workspace_id": "westside-watch"},
        )


if __name__ == "__main__":
    unittest.main()
