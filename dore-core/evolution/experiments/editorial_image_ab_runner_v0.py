from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

FORBIDDEN_GENERATION_LABELS = (
    "control",
    "compiled",
    "campo grafico",
    "italian style",
    "winner",
    "judge",
    "score",
)


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _assert_clean_generation_payload(payload: dict) -> None:
    text = _canonical_json(payload).lower()
    leaked = [term for term in FORBIDDEN_GENERATION_LABELS if term in text]
    if leaked:
        raise ValueError(f"generation payload contains benchmark leakage: {leaked}")


def prepare_isolated_run(execution: dict, seed: int = 76001) -> dict:
    task = execution["task"]
    semantic = task["semantic_intent"]

    # The baseline deliberately does not name a publication, country, benchmark arm or evaluator.
    baseline_prompt = (
        "Create a polished contemporary editorial hero image for this meaning: "
        f"{semantic} "
        "No text inside the image. Build a coherent publication-quality composition."
    )
    evidence_prompt = execution["compiler"]["compiled_prompt"]

    arm_1 = {
        "schema": "dore.image-generation-request.v0",
        "semantic_brief": task,
        "prompt": baseline_prompt,
    }
    arm_2 = {
        "schema": "dore.image-generation-request.v0",
        "semantic_brief": task,
        "prompt": evidence_prompt,
    }
    _assert_clean_generation_payload(arm_1)
    _assert_clean_generation_payload(arm_2)

    rng = random.Random(seed)
    hidden = ["arm-1", "arm-2"]
    rng.shuffle(hidden)
    anonymous = {"X": hidden[0], "Y": hidden[1]}

    requests = {"arm-1": arm_1, "arm-2": arm_2}
    manifest = {
        "schema": "dore.editorial-image-ab-run.v0",
        "status": "READY_FOR_TWO_INDEPENDENT_GENERATION_CALLS",
        "seed": seed,
        "request_hashes": {key: _sha256(value) for key, value in requests.items()},
        "anonymous_mapping_commitment": _sha256(anonymous),
        "evaluation_contract": {
            "judge_receives": [
                "semantic_brief",
                "artifact-X",
                "artifact-Y",
                "rubric",
            ],
            "judge_must_not_receive": [
                "generation prompts",
                "grammar ids",
                "corpus names",
                "arm provenance",
                "anonymous mapping",
            ],
            "rubric": [
                "beauty",
                "editorial intentionality",
                "semantic content-form relation",
                "hierarchy",
                "material justification",
                "non-template behavior",
                "restraint",
            ],
        },
    }

    # Mapping remains sealed until both artifacts are frozen and blind judgement is complete.
    sealed = {
        "schema": "dore.editorial-image-ab-sealed-provenance.v0",
        "mapping": anonymous,
        "mapping_commitment": manifest["anonymous_mapping_commitment"],
        "arm_provenance": {
            "arm-1": "baseline-no-evidence-retrieval",
            "arm-2": "campo-grafico-evidence-backed-compiler",
        },
    }
    return {"requests": requests, "manifest": manifest, "sealed": sealed}


def write_bundle(execution_path: Path, out_dir: Path, seed: int = 76001) -> None:
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    bundle = prepare_isolated_run(execution, seed=seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    for arm, payload in bundle["requests"].items():
        (out_dir / f"{arm}.request.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    (out_dir / "anonymous.manifest.json").write_text(
        json.dumps(bundle["manifest"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "sealed.provenance.json").write_text(
        json.dumps(bundle["sealed"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    write_bundle(
        root / "campo-grafico-blind-execution-01.v0.json",
        root / "runs" / "campo-grafico-blind-01",
    )
