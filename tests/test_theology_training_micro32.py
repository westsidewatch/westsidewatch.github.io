import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "local" / "dore-local" / "theology-training-micro32.py"
spec = importlib.util.spec_from_file_location("theology_training_micro32", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_micro32_command_is_fixed_and_non_shell():
    repo = Path("/tmp/repo")
    quarantine = Path("/tmp/quarantine")
    command = mod.build_command(repo, quarantine)
    assert command[0] == mod.sys.executable
    assert command[1] == "/tmp/repo/local/dore-local/theology-training-poc.py"
    assert command[2:] == [
        "--quarantine", "/tmp/quarantine",
        "--size", "32",
        "--execute",
    ]
    assert "shell" not in " ".join(command).lower()
    assert "64" not in command
    assert "128" not in command
    assert "256" not in command
