from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "local" / "dore-local" / "install-knowledge-substrates-macos.sh"
POC = ROOT / "local" / "dore-local" / "knowledge-substrate-poc.py"


class KnowledgeSubstrateInstallContract(unittest.TestCase):
    def test_installer_is_dore_scoped_and_non_privileged(self):
        text = INSTALL.read_text(encoding="utf-8")
        self.assertIn("Library/Application Support/Dore/local-ai", text)
        self.assertIn("@tobilu/qmd longmemory", text)
        self.assertIn("--prefix", text)
        self.assertNotIn("sudo ", text)
        self.assertNotIn("npm install -g", text)

    def test_poc_keeps_qmd_passive_lane_model_free(self):
        text = POC.read_text(encoding="utf-8")
        self.assertIn('"search", "嗎哪 曠野"', text)
        self.assertNotIn('"embed"', text)
        self.assertIn('"large_model_invoked": False', text)

    def test_poc_does_not_ingest_canonical_dore_memory(self):
        text = POC.read_text(encoding="utf-8")
        self.assertIn('"canonical_ingest": False', text)
        self.assertIn('"canonical_knowledge_untouched": True', text)
        self.assertNotIn('"ingest",', text)


if __name__ == "__main__":
    unittest.main()
