#!/usr/bin/env python3
"""Series-level selection for Olive Mountain; use existing Doré candidate engine."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "scripts/generate_magazine_candidates.py"
SCORE = ROOT / "scripts/score_magazine_candidates.py"
SPEAKERS = ROOT / "data/westside-core/entities/sermon-speakers.v1.json"
OUT = ROOT / "static/dore-design/runtime/olive-series-diversity.v1.json"

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def select():
    gen = load_module(GEN, "olive_series_gen")
    scorer = load_module(SCORE, "olive_series_score")
    rows = json.loads(SPEAKERS.read_text(encoding="utf-8"))["records"]
    used = {}
    result = []
    for row in rows:
        slug = row["id"].split(":", 1)[1]
        # This is a layout study, not evidence that a verified portrait exists.
        candidates = scorer.rank(gen.generate(slug, "verified"))["candidates"]
        viable = [c for c in candidates if c["score"]["hardPass"] and c["family"] != "typographic-no-portrait"]
        if not viable:
            raise ValueError("No valid portrait-bearing composition for " + slug)
        # Penalize repetition across the entire series, not only per-person quality.
        chosen = max(viable, key=lambda c: (
            c["score"]["reward"] - 12 * used.get(c["family"], 0),
            -used.get(c["family"], 0),
            c["family"],
        ))
        used[chosen["family"]] = used.get(chosen["family"], 0) + 1
        result.append({
            "speaker": slug, "family": chosen["family"],
            "candidateId": chosen["id"], "geometry": chosen["geometry"],
            "originalReward": chosen["score"]["reward"],
            "repeatCountBeforeSelection": used[chosen["family"]] - 1,
            "portraitVerification": "required-before-publication",
            "assetBinding": "none",
        })
    return {
        "schema": "dore.olive-series-diversity.v1",
        "authority": "Doré Magazine Engine / series-level selection",
        "status": "proposal-not-live",
        "familyCounts": used, "records": result,
    }

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(select(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
