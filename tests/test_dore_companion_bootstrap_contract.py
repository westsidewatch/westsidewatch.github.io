from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "local" / "dore-local" / "bootstrap_companion_1.command"


class CompanionBootstrapContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = BOOTSTRAP.read_text(encoding="utf-8")

    def test_bootstrap_does_not_touch_local_git_checkout(self) -> None:
        # Comments/documentation may name forbidden git operations while explaining
        # the safety boundary. Only executable, non-comment lines are governed here.
        executable = "\n".join(
            line for line in self.source.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ).lower()
        forbidden_commands = (
            r"(^|[;&|]\s*)git\s+pull\b",
            r"(^|[;&|]\s*)git\s+reset\b",
            r"(^|[;&|]\s*)git\s+rebase\b",
            r"(^|[;&|]\s*)git\s+merge\b",
            r"(^|[;&|]\s*)git\s+checkout\b",
            r"(^|[;&|]\s*)git\s+cherry-pick\b",
        )
        for pattern in forbidden_commands:
            self.assertIsNone(re.search(pattern, executable, flags=re.MULTILINE), pattern)
        self.assertNotIn("~/westsidewatch.github.io", executable)
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
