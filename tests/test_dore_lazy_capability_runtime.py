import tempfile
import unittest
from pathlib import Path

from dore_core.capabilities.model import TaskState
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.capabilities.visual import require_visual_inputs, visual_artifact


class LazyCapabilityRuntimeTests(unittest.TestCase):
    def test_unrelated_task_loads_no_visual_body(self):
        with tempfile.TemporaryDirectory() as td:
            state = TaskState("non-visual")
            runtime = LazyCapabilityRuntime(default_registry(), root=Path(td))
            self.assertEqual(state.telemetry["lazy_loads"], 0)
            self.assertEqual(state.telemetry["provider_activations"], 0)
            self.assertEqual(state.active_capabilities, [])
            self.assertEqual(runtime._instruction_cache, {})
            self.assertEqual(runtime._provider_cache, {})

    def test_instruction_is_loaded_only_after_activation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / "dore-image" / "SKILL.md"
            skill.parent.mkdir()
            skill.write_text("Dore image instructions", encoding="utf-8")
            state = TaskState("critic")
            runtime = LazyCapabilityRuntime(default_registry(), root=root)
            loaded = runtime.activate("image.critic", state)
            self.assertEqual(loaded.instruction, "Dore image instructions")
            self.assertEqual(state.active_capabilities, ["image.critic"])
            self.assertEqual(state.telemetry["lazy_loads"], 1)
            runtime.activate("image.critic", state)
            self.assertEqual(state.telemetry["lazy_loads"], 1)
            self.assertEqual(state.telemetry["instruction_cache_hits"], 1)

    def test_provider_is_lazy_and_cached(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / "dore-image" / "SKILL.md"
            skill.parent.mkdir()
            skill.write_text("Dore image instructions", encoding="utf-8")
            calls = []

            def provider_loader(ref: str):
                calls.append(ref)
                return {"provider": ref}

            state = TaskState("generate")
            runtime = LazyCapabilityRuntime(default_registry(), root=root, provider_loader=provider_loader)
            runtime.activate("image.generate", state)
            runtime.activate("image.generate", state)
            self.assertEqual(calls, ["local-image-renderer"])
            self.assertEqual(state.telemetry["provider_activations"], 1)
            self.assertEqual(state.telemetry["provider_cache_hits"], 1)

    def test_visual_capabilities_share_typed_state(self):
        state = TaskState("visual-shared")
        brief = visual_artifact(state, "visual_brief", {"need": "Matthew 3 hero"}, provenance=("user",))
        recipe = visual_artifact(state, "style_recipe", {"family": "Dore Original"}, provenance=(brief.content_hash,))
        inputs = require_visual_inputs(state, ("visual_brief", "style_recipe"))
        self.assertIs(inputs["visual_brief"], brief)
        self.assertIs(inputs["style_recipe"], recipe)
        self.assertEqual(recipe.provenance, (brief.content_hash,))

    def test_missing_visual_input_fails_closed(self):
        state = TaskState("missing")
        visual_artifact(state, "visual_brief", {"need": "hero"})
        with self.assertRaisesRegex(ValueError, "style_recipe"):
            require_visual_inputs(state, ("visual_brief", "style_recipe"))


if __name__ == "__main__":
    unittest.main()
