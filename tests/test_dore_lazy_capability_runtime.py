from pathlib import Path

import pytest

from dore_core.capabilities.model import TaskState
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.capabilities.visual import require_visual_inputs, visual_artifact


def test_unrelated_task_loads_no_visual_body(tmp_path: Path):
    state = TaskState("non-visual")
    runtime = LazyCapabilityRuntime(default_registry(), root=tmp_path)
    assert state.telemetry["lazy_loads"] == 0
    assert state.telemetry["provider_activations"] == 0
    assert state.active_capabilities == []
    assert runtime._instruction_cache == {}
    assert runtime._provider_cache == {}


def test_instruction_is_loaded_only_after_activation(tmp_path: Path):
    skill = tmp_path / "dore-image" / "SKILL.md"
    skill.parent.mkdir()
    skill.write_text("Dore image instructions", encoding="utf-8")
    state = TaskState("critic")
    runtime = LazyCapabilityRuntime(default_registry(), root=tmp_path)
    loaded = runtime.activate("image.critic", state)
    assert loaded.instruction == "Dore image instructions"
    assert state.active_capabilities == ["image.critic"]
    assert state.telemetry["lazy_loads"] == 1
    runtime.activate("image.critic", state)
    assert state.telemetry["lazy_loads"] == 1
    assert state.telemetry["instruction_cache_hits"] == 1


def test_provider_is_lazy_and_cached(tmp_path: Path):
    skill = tmp_path / "dore-image" / "SKILL.md"
    skill.parent.mkdir()
    skill.write_text("Dore image instructions", encoding="utf-8")
    calls = []

    def provider_loader(ref: str):
        calls.append(ref)
        return {"provider": ref}

    state = TaskState("generate")
    runtime = LazyCapabilityRuntime(default_registry(), root=tmp_path, provider_loader=provider_loader)
    runtime.activate("image.generate", state)
    runtime.activate("image.generate", state)
    assert calls == ["local-image-renderer"]
    assert state.telemetry["provider_activations"] == 1
    assert state.telemetry["provider_cache_hits"] == 1


def test_visual_capabilities_share_typed_state():
    state = TaskState("visual-shared")
    brief = visual_artifact(state, "visual_brief", {"need": "Matthew 3 hero"}, provenance=("user",))
    recipe = visual_artifact(state, "style_recipe", {"family": "Dore Original"}, provenance=(brief.content_hash,))
    inputs = require_visual_inputs(state, ("visual_brief", "style_recipe"))
    assert inputs["visual_brief"] is brief
    assert inputs["style_recipe"] is recipe
    assert recipe.provenance == (brief.content_hash,)


def test_missing_visual_input_fails_closed():
    state = TaskState("missing")
    visual_artifact(state, "visual_brief", {"need": "hero"})
    with pytest.raises(ValueError, match="style_recipe"):
        require_visual_inputs(state, ("visual_brief", "style_recipe"))
