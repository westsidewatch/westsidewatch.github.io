from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


REQUIRED_JUDGE_FIELDS = {
    "candidate",
    "beauty",
    "editorial_intentionality",
    "semantic_content_form_relation",
    "hierarchy",
    "material_justification",
    "non_template_behavior",
    "restraint",
    "decision",
    "reasoning_summary",
}


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


@dataclass(frozen=True)
class FrozenArtifact:
    anonymous_id: str
    sha256: str
    byte_size: int


def freeze_artifact(anonymous_id: str, artifact_bytes: bytes) -> FrozenArtifact:
    if anonymous_id not in {"X", "Y"}:
        raise ValueError("anonymous_id must be X or Y")
    if not artifact_bytes:
        raise ValueError("artifact must not be empty")
    return FrozenArtifact(
        anonymous_id=anonymous_id,
        sha256=_sha256_bytes(artifact_bytes),
        byte_size=len(artifact_bytes),
    )


def validate_blind_judge_record(record: dict) -> None:
    if record.get("schema") != "dore.blind-aesthetic-judge-record.v0":
        raise ValueError("unexpected judge schema")
    if record.get("provenance_visible") is not False:
        raise ValueError("judge record is not blind")

    evaluations = record.get("evaluations")
    if not isinstance(evaluations, list) or len(evaluations) != 2:
        raise ValueError("judge record must contain exactly two evaluations")

    candidates = set()
    for evaluation in evaluations:
        missing = REQUIRED_JUDGE_FIELDS - set(evaluation)
        if missing:
            raise ValueError(f"judge evaluation missing fields: {sorted(missing)}")
        candidate = evaluation["candidate"]
        if candidate not in {"X", "Y"}:
            raise ValueError("judge may evaluate only X and Y")
        candidates.add(candidate)
        for key in (
            "beauty",
            "editorial_intentionality",
            "semantic_content_form_relation",
            "hierarchy",
            "material_justification",
            "non_template_behavior",
            "restraint",
        ):
            value = evaluation[key]
            if not isinstance(value, (int, float)) or not 0 <= value <= 10:
                raise ValueError(f"{key} must be a score from 0 to 10")
    if candidates != {"X", "Y"}:
        raise ValueError("judge record must evaluate both X and Y exactly once")


def admit_blind_result(
    *,
    manifest: dict,
    sealed_provenance: dict,
    artifact_x: FrozenArtifact,
    artifact_y: FrozenArtifact,
    judge_record: dict,
) -> dict:
    if manifest.get("status") != "READY_FOR_TWO_INDEPENDENT_GENERATION_CALLS":
        raise ValueError("run manifest is not ready for admission")

    commitment = manifest.get("anonymous_mapping_commitment")
    if not commitment:
        raise ValueError("anonymous mapping commitment missing")
    if sealed_provenance.get("mapping_commitment") != commitment:
        raise ValueError("sealed provenance does not match manifest commitment")
    if _sha256_json(sealed_provenance.get("mapping")) != commitment:
        raise ValueError("anonymous mapping commitment verification failed")

    if artifact_x.anonymous_id != "X" or artifact_y.anonymous_id != "Y":
        raise ValueError("artifact identities must remain anonymous X/Y before unblind")
    if artifact_x.sha256 == artifact_y.sha256:
        raise ValueError("X and Y resolve to identical artifact bytes")

    validate_blind_judge_record(judge_record)

    mapping = sealed_provenance["mapping"]
    arm_provenance = sealed_provenance["arm_provenance"]
    judge_by_candidate = {row["candidate"]: row for row in judge_record["evaluations"]}

    def resolved(candidate: str, frozen: FrozenArtifact) -> dict:
        arm = mapping[candidate]
        return {
            "candidate": candidate,
            "artifact_sha256": frozen.sha256,
            "artifact_byte_size": frozen.byte_size,
            "arm": arm,
            "provenance": arm_provenance[arm],
            "judge": judge_by_candidate[candidate],
        }

    rows = [resolved("X", artifact_x), resolved("Y", artifact_y)]
    winner = judge_record.get("winner")
    if winner not in {"X", "Y", "TIE"}:
        raise ValueError("winner must be X, Y, or TIE")

    result = {
        "schema": "dore.editorial-image-ab-admission.v0",
        "status": "BLIND_JUDGEMENT_ADMITTED",
        "mapping_commitment_verified": True,
        "artifacts_frozen_before_unblind": True,
        "provenance_attached_after_judgement": True,
        "winner": winner,
        "resolved": rows,
        "capability_effect": "EVIDENCE_ONLY_NO_PROMOTION",
    }
    result["record_sha256"] = _sha256_json(result)
    return result


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
