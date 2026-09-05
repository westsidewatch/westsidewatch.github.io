from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "local" / "dore-local" / "bootstrap_companion_1.command"


class CompanionBootstrapContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = BOOTSTRAP.read_text(encoding="utf-8")

    def test_bootstrap_does_not_touch_local_git_checkout(self) -> None:
        lowered = self.source.lower()
        forbidden = (
            "git pull",
            "git reset",
            "git rebase",
            "git merge",
            "git checkout",
            "git cherry-pick",
            "~/westsidewatch.github.io",
        )
        for token in forbidden:
            self.assertNotIn(token, lowered)
        self.assertIn("Local Git checkout: untouched", self.source)

    def test_bootstrap_installs_native_messaging_contract(self) -> None:
        self.assertIn('HOST_NAME="ca.dore.companion"', self.source)
        self.assertIn('EXTENSION_ID="dore-companion@westsidewatch.ca"', self.source)
        self.assertIn("NativeMessagingHosts", self.source)
        self.assertIn("native_host.py", self.source)
        self.assertIn("test_native_host.py", self.source)

    def test_bootstrap_stages_complete_companion_1_extension(self) -> None:
        self.assertIn('EXT_DIR="$APP_ROOT/companion-1.0"', self.source)
        for name in ("manifest.json", "background.js", "content_script.js", "native_transport.js"):
            self.assertIn(name, self.source)
        self.assertIn("about:debugging#/runtime/this-firefox", self.source)

    def test_zero_cost_boundary_is_explicit(self) -> None:
        self.assertIn("zero-cost", self.source.lower())
        self.assertNotIn("api.openai.com", self.source)
        self.assertNotIn("OPENAI_API_KEY", self.source)


if __name__ == "__main__":
    unittest.main()
