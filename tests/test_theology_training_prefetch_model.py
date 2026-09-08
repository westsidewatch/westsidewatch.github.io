import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "local" / "dore-local" / "theology-training-prefetch-model.py"
spec = importlib.util.spec_from_file_location("theology_training_prefetch_model", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class TheologyTrainingPrefetchModelTest(unittest.TestCase):
    def test_model_and_cache_are_fixed(self):
        self.assertEqual(mod.MODEL_ID, "mlx-community/gemma-4-e4b-it-4bit")
        self.assertEqual(mod.REVISION, "main")
        self.assertIn("Library/Caches/Dore/theology-training", str(mod.CACHE_ROOT))

    def test_prefetch_has_no_caller_parameters(self):
        import inspect
        self.assertEqual(list(inspect.signature(mod.main).parameters), [])


if __name__ == "__main__":
    unittest.main()
