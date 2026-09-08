import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "local" / "dore-local" / "theology-training-poc.py"
spec = importlib.util.spec_from_file_location("theology_training_poc", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def write_jsonl(path: Path, count: int) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for i in range(count):
            fh.write(json.dumps({"messages": [{"role": "user", "content": f"case {i}"}, {"role": "assistant", "content": "safe"}]}) + "\n")


class TheologyTrainingPOCTest(unittest.TestCase):
    def test_verify_dataset_and_stage_split(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "quarantine"
            root.mkdir()
            write_jsonl(root / "train-32.jsonl", 32)
            write_jsonl(root / "valid.jsonl", 4)
            write_jsonl(root / "test.jsonl", 4)
            dataset = mod.verify_dataset(root, 32)
            self.assertEqual(dataset["train_rows"], 32)
            self.assertEqual(dataset["valid_rows"], 4)
            self.assertEqual(dataset["test_rows"], 4)

            work = Path(tmp) / "work"
            stage = mod.stage_split(dataset, work)
            self.assertEqual(mod.count_jsonl(stage / "train.jsonl"), 32)
            self.assertEqual(mod.count_jsonl(stage / "valid.jsonl"), 4)
            self.assertEqual(mod.count_jsonl(stage / "test.jsonl"), 4)

    def test_build_command_uses_isolated_mlx_vlm_and_keeps_adapter_separate(self):
        command = mod.build_command(
            "local-model",
            Path("/tmp/dataset"),
            Path("/tmp/adapter/adapter.safetensors"),
            80,
        )
        joined = " ".join(command)
        self.assertEqual(command[0], str(mod.PY))
        self.assertIn("mlx_vlm.lora", joined)
        self.assertIn("--model-path local-model", joined)
        self.assertIn("--dataset /tmp/dataset", joined)
        self.assertIn("--output-path /tmp/adapter/adapter.safetensors", joined)
        self.assertIn("--train-on-completions", joined)
        self.assertNotIn("mlx_lm.lora", joined)
        self.assertNotIn("fuse", joined.lower())


if __name__ == "__main__":
    unittest.main()
