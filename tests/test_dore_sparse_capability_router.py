from dore_core.capabilities import SparseCapabilityRouter, TaskState
from dore_core.capabilities.registry import default_registry


def test_non_visual_task_does_not_activate_visual_capabilities():
    state = TaskState("t-non-visual")
    router = SparseCapabilityRouter(default_registry())
    decision = router.route("查馬太福音六章希臘原文", state=state)
    assert decision.capability_ids == ()
    assert state.active_capabilities == []
    assert decision.level == "L2_REQUIRED"


def test_visual_route_is_sparse_and_shared_state():
    state = TaskState("t-visual")
    router = SparseCapabilityRouter(default_registry(), max_active=3)
    decision = router.route("create image illustration for website hero", state=state)
    assert 1 <= len(decision.capability_ids) <= 3
    assert len(state.active_capabilities) <= 3
    assert state.route_history[-1] == decision


def test_dormant_registry_growth_does_not_expand_working_set():
    registry = default_registry()
    manifest_type = type(registry.get("visual.direct"))
    for i in range(1000):
        registry.register(manifest_type(
            id=f"dormant.{i}",
            faculty="future",
            description=f"Unrelated dormant capability {i}",
            triggers=(f"never-trigger-{i}",),
        ))
    router = SparseCapabilityRouter(registry, max_active=3)
    decision = router.route("generate image hero art")
    assert len(decision.capability_ids) <= 3
    assert all(not cid.startswith("dormant.") for cid in decision.capability_ids)


def test_registry_contains_only_manifest_refs_not_loaded_provider_objects():
    registry = default_registry()
    image = registry.get("image.generate")
    assert image.provider_refs == ("local-image-renderer",)
    assert image.instruction_ref == "dore-image/SKILL.md"
