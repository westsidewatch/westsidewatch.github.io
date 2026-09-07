from dore_core.intelligence.router import choose_route
from dore_core.intelligence.registry import Provider, provider_map, validate


def test_deterministic_lane_wins_before_ai():
    d = choose_route("research", deterministic_available=True, providers={"research": "large"})
    assert d.lane == "deterministic"
    assert d.provider is None


def test_tiny_lane_prevents_large_model_load():
    d = choose_route("language", tiny_sufficient=True, resident={"tiny-reflex": "tiny-local"}, providers={"language": "large-local"})
    assert d.lane == "tiny-hot"
    assert d.provider == "tiny-local"
    assert d.load == "reuse"


def test_resident_specialist_is_reused():
    d = choose_route("coding", resident={"coding": "code-local"}, providers={"coding": "other"})
    assert d.lane == "resident-specialist"
    assert d.provider == "code-local"


def test_cold_specialist_is_on_demand():
    d = choose_route("vision", providers={"vision": "vision-local"})
    assert d.lane == "cold-specialist"
    assert d.load == "on-demand"


def test_free_local_gate_rejects_paid_or_remote_provider():
    for p in (Provider("language", "x", local=False), Provider("language", "x", paid=True)):
        try:
            validate(p)
        except ValueError:
            pass
        else:
            raise AssertionError("provider should be rejected")


def test_provider_map_keeps_physical_names_below_virtual_capability():
    assert provider_map([Provider("language", "local-language")]) == {"language": "local-language"}
