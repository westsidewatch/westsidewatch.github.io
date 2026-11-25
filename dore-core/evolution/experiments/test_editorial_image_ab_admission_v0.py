from __future__ import annotations

import hashlib
import json

import pytest

from editorial_image_ab_admission_v0 import admit_blind_result, freeze_artifact


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _fixture():
    mapping = {"X": "arm-2", "Y": "arm-1"}
    commitment = _sha256_json(mapping)
    manifest = {
        "status": "READY_FOR_TWO_INDEPENDENT_GENERATION_CALLS",
        "anonymous_mapping_commitment": commitment,
    }
    sealed = {
        "mapping": mapping,
        "mapping_commitment": commitment,
        "arm_provenance": {
            "arm-1": "baseline-no-evidence-retrieval",
            "arm-2": "campo-grafico-evidence-backed-compiler",
        },
    }
    judge = {
        "schema": "dore.blind-aesthetic-judge-record.v0",
        "provenance_visible": False,
        "winner": "X",
        "evaluations": [
            {
                "candidate": "X",
                "beauty": 9,
                "editorial_intentionality": 9,
                "semantic_content_form_relation": 9,
                "hierarchy": 8,
                "material_justification": 9,
                "non_template_behavior": 9,
                "restraint": 8,
                "decision": "ACCEPT",
                "reasoning_summary": "Strong content-form relation without surface imitation.",
            },
            {
                "candidate": "Y",
                "beauty": 7,
                "editorial_intentionality": 6,
                "semantic_content_form_relation": 6,
                "hierarchy": 7,
                "material_justification": 5,
                "non_template_behavior": 5,
                "restraint": 7,
                "decision": "REJECT",
                "reasoning_summary": "Polished but generic and weakly tied to the semantic brief.",
            },
        ],
    }
    return manifest, sealed, judge


def test_admission_verifies_commitment_and_unblinds_after_judgement():
    manifest, sealed, judge = _fixture()
    result = admit_blind_result(
        manifest=manifest,
        sealed_provenance=sealed,
        artifact_x=freeze_artifact("X", b"image-x"),
        artifact_y=freeze_artifact("Y", b"image-y"),
        judge_record=judge,
    )
    assert result["status"] == "BLIND_JUDGEMENT_ADMITTED"
    assert result["mapping_commitment_verified"] is True
    assert result["resolved"][0]["provenance"] == "campo-grafico-evidence-backed-compiler"
    assert result["capability_effect"] == "EVIDENCE_ONLY_NO_PROMOTION"


def test_tampered_mapping_is_rejected():
    manifest, sealed, judge = _fixture()
    sealed["mapping"] = {"X": "arm-1", "Y": "arm-2"}
    with pytest.raises(ValueError, match="commitment"):
        admit_blind_result(
            manifest=manifest,
            sealed_provenance=sealed,
            artifact_x=freeze_artifact("X", b"image-x"),
            artifact_y=freeze_artifact("Y", b"image-y"),
            judge_record=judge,
        )


def test_nonblind_judge_is_rejected():
    manifest, sealed, judge = _fixture()
    judge["provenance_visible"] = True
    with pytest.raises(ValueError, match="not blind"):
        admit_blind_result(
            manifest=manifest,
            sealed_provenance=sealed,
            artifact_x=freeze_artifact("X", b"image-x"),
            artifact_y=freeze_artifact("Y", b"image-y"),
            judge_record=judge,
        )


def test_identical_artifacts_are_rejected():
    manifest, sealed, judge = _fixture()
    with pytest.raises(ValueError, match="identical"):
        admit_blind_result(
            manifest=manifest,
            sealed_provenance=sealed,
            artifact_x=freeze_artifact("X", b"same"),
            artifact_y=freeze_artifact("Y", b"same"),
            judge_record=judge,
        )
