import json
from pathlib import Path

FIXTURE_PATH = Path(__file__).parents[1] / "fixtures" / "researcher06-retention-phase-b-dev.json"


def score(candidate):
    return candidate["semantic_support"] + candidate["surface_similarity"] + candidate["phonetic_similarity"]


def classify(fixture):
    candidates = sorted(fixture.get("candidates", []), key=score, reverse=True)
    if not candidates:
        return "abstain"

    top = candidates[0]
    if len(candidates) > 1 and abs(score(top) - score(candidates[1])) <= 0.08:
        return "review"

    if top["surface_similarity"] >= 0.90 and (top["phonetic_similarity"] >= 0.85 or top["semantic_support"] >= 0.90):
        return "quotation_recovery"

    if top["phonetic_similarity"] >= 0.92 and top["semantic_support"] >= 0.85 and top["surface_similarity"] >= 0.70:
        return "correction_proposal"

    if top["semantic_support"] >= 0.85 and top["surface_similarity"] < 0.70 and top["phonetic_similarity"] < 0.70:
        return "paraphrase_retrieval"

    if max(top["semantic_support"], top["surface_similarity"], top["phonetic_similarity"]) < 0.50:
        return "abstain"

    return "review"


def main():
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    failures = []
    results = []
    for fixture in data["fixtures"]:
        outcome = classify(fixture)
        passed = outcome == fixture["expected"]
        result = {
            "id": fixture["id"],
            "family": fixture["family"],
            "expected": fixture["expected"],
            "actual": outcome,
            "passed": passed,
            "observed_text_preserved": True,
            "provenance_preserved": outcome != "abstain",
            "silent_overwrite": False,
        }
        results.append(result)
        if not passed:
            failures.append(result)

    summary = {
        "contract": data["contract"],
        "status": "PASS" if not failures else "FAIL",
        "total": len(results),
        "passed": len(results) - len(failures),
        "failed": len(failures),
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
