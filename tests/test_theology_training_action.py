import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "local" / "dore-local" / "theology_training_action.py"
spec = importlib.util.spec_from_file_location("theology_training_action", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TheologyTrainingActionTest(unittest.TestCase):
    def test_micro32_is_registered_as_fixed_capability(self):
        self.assertIn("theology.training.micro32", mod.CAPABILITIES)
        self.assertEqual(
            mod.SCRIPTS["theology.training.micro32"],
            ("theology-training-micro32.py", 7200),
        )

    def test_training_action_does_not_use_caller_args_for_command_selection(self):
        self.assertTrue(all(name.startswith("theology-training-") for name, _ in mod.SCRIPTS.values()))
        self.assertEqual(set(mod.SCRIPTS), mod.CAPABILITIES)


if __name__ == "__main__":
    unittest.main()
