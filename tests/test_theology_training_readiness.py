import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "local" / "dore-local" / "theology-training-readiness.py"
spec = importlib.util.spec_from_file_location("theology_training_readiness", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_command_output_handles_missing_command():
    assert mod.command_output(["/definitely/not/a/real/command"]) is None
