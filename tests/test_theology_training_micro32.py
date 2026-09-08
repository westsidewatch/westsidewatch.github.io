import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "local" / "dore-local" / "theology-training-micro32.py"
spec = importlib.util.spec_from_file_location("theology_training_micro32", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TheologyTrainingMicro32Test(unittest.TestCase):
    def test_micro32_command_is_fixed_and_non_shell(self):
        repo = Path("/tmp/repo")
        quarantine = Path("/tmp/quarantine")
        command = mod.build_command(repo, quarantine)
        self.assertEqual(command[0], mod.sys.executable)
        self.assertEqual(command[1], "/tmp/repo/local/dore-local/theology-training-poc.py")
        self.assertEqual(command[2:], [
            "--quarantine", "/tmp/quarantine",
            "--size", "32",
            "--execute",
        ])
        self.assertNotIn("shell", " ".join(command).lower())
        self.assertNotIn("64", command)
        self.assertNotIn("128", command)
        self.assertNotIn("256", command)


if __name__ == "__main__":
    unittest.main()
