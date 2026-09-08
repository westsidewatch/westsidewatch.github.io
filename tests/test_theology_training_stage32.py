import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "local" / "dore-local" / "theology-training-stage32.py"
spec = importlib.util.spec_from_file_location("theology_training_stage32", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TheologyTrainingStage32Test(unittest.TestCase):
    def test_seed_sizes_are_bounded(self):
        self.assertEqual(len(mod.PAIRS), 32)
        self.assertEqual(len(mod.VALID), 4)
        self.assertEqual(len(mod.TEST), 4)

    def test_jsonl_writer_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.jsonl"
            b = Path(tmp) / "b.jsonl"
            hash_a = mod.write_jsonl(a, mod.PAIRS)
            hash_b = mod.write_jsonl(b, mod.PAIRS)
            self.assertEqual(hash_a, hash_b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(len(a.read_text(encoding="utf-8").splitlines()), 32)

    def test_seed_is_positive_ministry_data_not_canonical_runtime_data(self):
        all_text = " ".join(user + " " + answer for user, answer in mod.PAIRS)
        self.assertIn("耶穌基督", all_text)
        self.assertIn("Jesus Christ", all_text)
        self.assertNotIn("Library/Application Support/Dore", str(mod.ROOT))
        self.assertNotIn("/.dore", str(mod.ROOT))


if __name__ == "__main__":
    unittest.main()
