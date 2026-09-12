import unittest
from unittest.mock import patch

import browser_capability_transport as transport


class BrowserCapabilityTransportTests(unittest.TestCase):
    def test_rejects_non_publishing_capability(self):
        body, status = transport.call_browser_capability({
            "capability": "production.deploy",
            "args": {},
        })
        self.assertEqual(status, 403)
        self.assertEqual(body["error"], "capability_not_allowed")

    def test_rejects_invalid_args(self):
        body, status = transport.call_browser_capability({
            "capability": "publishing.book-intelligence",
            "args": "not-an-object",
        })
        self.assertEqual(status, 400)
        self.assertEqual(body["error"], "invalid_args")

    @patch.object(transport.capability_bus, "call")
    def test_forces_multiwrite_caller_and_calls_only_reviewed_capability(self, call):
        call.return_value = {"ok": True, "report": {"schema": "dore.book-intelligence-report.v2"}}
        body, status = transport.call_browser_capability({
            "capability": "publishing.book-intelligence",
            "args": {"source": {}, "sections": []},
            "caller_product": "production-console",
        })

        self.assertEqual(status, 200)
        self.assertTrue(body["ok"])
        call.assert_called_once_with(
            "publishing.book-intelligence",
            {"source": {}, "sections": []},
            transport.production_actions,
            caller_product="multiwrite",
        )


if __name__ == "__main__":
    unittest.main()
