from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "local" / "dore-companion-extension"


class CompanionNativeContractTest(unittest.TestCase):
    def test_native_manifest_contract_matches_native_host(self) -> None:
        manifest = json.loads((EXT / "manifest.native-messaging.json").read_text(encoding="utf-8"))
        self.assertIn("nativeMessaging", manifest["permissions"])
        self.assertEqual(manifest["browser_specific_settings"]["gecko"]["id"], "dore-companion@westsidewatch.ca")
        self.assertEqual(manifest["dore_native_messaging"]["host"], "ca.dore.companion")
        self.assertEqual(manifest["dore_native_messaging"]["fallback_role"], "compatibility-debug-only")

    def test_companion_1_manifest_is_installable_firefox_extension(self) -> None:
        manifest = json.loads((EXT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["manifest_version"], 2)
        self.assertEqual(manifest["version"], "1.1.0")
        self.assertIn("nativeMessaging", manifest["permissions"])
        self.assertEqual(manifest["browser_specific_settings"]["gecko"]["id"], "dore-companion@westsidewatch.ca")
        self.assertIn("background.js", manifest["background"]["scripts"])
        script = manifest["content_scripts"][0]
        self.assertIn("https://chatgpt.com/*", script["matches"])
        self.assertIn("content_script.js", script["js"])

    def test_transport_prefers_native_and_keeps_4312_only_as_fallback(self) -> None:
        source = (EXT / "native_transport.js").read_text(encoding="utf-8")
        self.assertIn('browser.runtime.connectNative(DORE_NATIVE_HOST)', source)
        self.assertIn('const DORE_NATIVE_HOST = "ca.dore.companion"', source)
        self.assertIn('const DORE_FALLBACK_URL = "http://127.0.0.1:4312/a2a"', source)
        self.assertLess(source.index("sendViaNative(payload)"), source.index("sendVia4312(payload)"))
        self.assertIn("__dore_transport_id", source)

    def test_background_routes_dore_commands_through_transport_module(self) -> None:
        source = (EXT / "background.js").read_text(encoding="utf-8")
        self.assertIn('import(browser.runtime.getURL("native_transport.js"))', source)
        self.assertIn('message.type === "dore.command"', source)
        self.assertIn('protocol: "dore.a2a/1"', source)
        self.assertIn("transport.sendDorePayload", source)
        self.assertIn("transport.nativeHealth", source)

    def test_content_script_captures_command_and_surfaces_status(self) -> None:
        source = (EXT / "content_script.js").read_text(encoding="utf-8")
        self.assertIn('startsWith("/dore")', source)
        self.assertIn('type: "dore.command"', source)
        self.assertIn('type: "dore.health"', source)
        self.assertIn("DORÉ A2A ·", source)
        self.assertIn('"dore:a2a-result"', source)

    def test_command_capture_survives_chatgpt_dom_and_locale_changes(self) -> None:
        source = (EXT / "content_script.js").read_text(encoding="utf-8")
        self.assertIn("#prompt-textarea", source)
        self.assertIn('document.addEventListener("input", rememberComposer, true)', source)
        self.assertIn('document.addEventListener("keydown"', source)
        self.assertIn('document.addEventListener("submit"', source)
        self.assertIn('document.addEventListener("click"', source)
        self.assertIn("pendingComposerCommand", source)
        self.assertNotIn('label.includes("send")', source)
        self.assertNotIn('label.includes("submit")', source)

    def test_installer_prepares_native_host_and_exact_extension_manifest(self) -> None:
        source = (EXT / "install_companion_1.command").read_text(encoding="utf-8")
        self.assertIn('install_native_messaging.sh', source)
        self.assertIn('companion-1.0', source)
        self.assertIn('dore-companion@westsidewatch.ca', source)
        self.assertIn('about:debugging#/runtime/this-firefox', source)
        self.assertIn('Load Temporary Add-on', source)
        self.assertNotIn('openai.com/v1', source.lower())
        self.assertNotIn('api.openai.com', source.lower())


if __name__ == "__main__":
    unittest.main()
