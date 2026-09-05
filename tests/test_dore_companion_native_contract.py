from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "local" / "dore-companion-extension"


class CompanionNativeContractTest(unittest.TestCase):
    def test_manifest_contract_matches_native_host(self) -> None:
        manifest = json.loads((EXT / "manifest.native-messaging.json").read_text(encoding="utf-8"))
        self.assertIn("nativeMessaging", manifest["permissions"])
        self.assertEqual(
            manifest["browser_specific_settings"]["gecko"]["id"],
            "dore-companion@westsidewatch.ca",
        )
        self.assertEqual(manifest["dore_native_messaging"]["host"], "ca.dore.companion")
        self.assertEqual(manifest["dore_native_messaging"]["fallback_role"], "compatibility-debug-only")

    def test_transport_prefers_native_and_keeps_4312_only_as_fallback(self) -> None:
        source = (EXT / "native_transport.js").read_text(encoding="utf-8")
        self.assertIn('browser.runtime.connectNative(DORE_NATIVE_HOST)', source)
        self.assertIn('const DORE_NATIVE_HOST = "ca.dore.companion"', source)
        self.assertIn('const DORE_FALLBACK_URL = "http://127.0.0.1:4312/a2a"', source)
        self.assertLess(source.index("sendViaNative(payload)"), source.index("sendVia4312(payload)"))
        self.assertIn("__dore_transport_id", source)


if __name__ == "__main__":
    unittest.main()
