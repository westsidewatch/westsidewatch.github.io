from __future__ import annotations

import json
from pathlib import Path

from editorial_image_ab_runner_v0 import prepare_isolated_run


def _fixture() -> dict:
    path = Path(__file__).resolve().parent / "campo-grafico-blind-execution-01.v0.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_generation_arms_are_separate_and_clean() -> None:
    bundle = prepare_isolated_run(_fixture(), seed=76001)
    arm_1 = bundle["requests"]["arm-1"]
    arm_2 = bundle["requests"]["arm-2"]
    assert arm_1 != arm_2
    joined = (json.dumps(arm_1) + json.dumps(arm_2)).lower()
    for forbidden in ("control", "compiled", "campo grafico", "italian style", "winner", "judge", "score"):
        assert forbidden not in joined


def test_judge_contract_is_blind() -> None:
    bundle = prepare_isolated_run(_fixture(), seed=76001)
    contract = bundle["manifest"]["evaluation_contract"]
    assert "artifact-X" in contract["judge_receives"]
    assert "artifact-Y" in contract["judge_receives"]
    assert "generation prompts" in contract["judge_must_not_receive"]
    assert "anonymous mapping" in contract["judge_must_not_receive"]


def test_mapping_is_committed_but_not_exposed_in_manifest() -> None:
    bundle = prepare_isolated_run(_fixture(), seed=76001)
    assert "anonymous_mapping_commitment" in bundle["manifest"]
    assert "mapping" not in bundle["manifest"]
    assert bundle["sealed"]["mapping_commitment"] == bundle["manifest"]["anonymous_mapping_commitment"]


def test_seed_is_reproducible() -> None:
    a = prepare_isolated_run(_fixture(), seed=76001)
    b = prepare_isolated_run(_fixture(), seed=76001)
    assert a["manifest"] == b["manifest"]
    assert a["sealed"] == b["sealed"]
