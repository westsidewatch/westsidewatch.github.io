#!/usr/bin/env python3
"""Resolve a Doré generation prompt from canonical Italian Editorial Atlas authority.

Formal generation must use this resolver (or an equivalent consumer adapter) rather
than reconstructing editorial grammar from chat memory.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "static" / "dore-design"
GRAMMARS = D / "italian-editorial-grammars.v1.json"
EVIDENCE = D / "italian-editorial-evidence.v1.json"
CANDIDATES = D / "italian-editorial-grammar-candidates.v1.json"
MODULES = ("layout", "image", "typography", "material", "density", "sequence", "irony", "emergence")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(era_id, modules=None, subject=None, artifact_type="image", consumer="dore", exploration=False):
    gdb = load(GRAMMARS)
    edb = load(EVIDENCE)
    cdb = load(CANDIDATES) if CANDIDATES.exists() else {"items": []}
    selected_family = selected_era = None
    for family in gdb.get("families", []):
        for era in family.get("eras", []):
            if era.get("id") == era_id:
                selected_family, selected_era = family, era
                break
        if selected_era:
            break
    if not selected_era:
        raise ValueError(f"unknown canonical grammar era: {era_id}")

    wanted = set(modules or MODULES)
    unknown = wanted.difference(MODULES)
    if unknown:
        raise ValueError(f"unknown grammar modules: {', '.join(sorted(unknown))}")

    grammar_lines = []
    selected_tokens = []
    for module, values in selected_era.get("grammar", {}).items():
        if module not in wanted:
            continue
        for value in values:
            grammar_lines.append(f"{module}: {value}")
            selected_tokens.append(value)

    # Only admitted evidence-derived candidates may enter generation.
    admitted = []
    for item in cdb.get("items", []):
        if item.get("family") == selected_family.get("id") and item.get("era") == era_id and item.get("state") == "admitted" and item.get("module") in wanted:
            admitted.append(item)
            grammar_lines.append(f"{item['module']}: {item['value']}")
            selected_tokens.append(item["value"])

    evidence = []
    for item in edb.get("items", []):
        if item.get("family") != selected_family.get("id") or item.get("era") != era_id:
            continue
        if set(item.get("tokens", [])).intersection(selected_tokens):
            evidence.append(item)

    evidence_ids = sorted({x["id"] for x in evidence})
    missing = [t for t in selected_tokens if not any(t in x.get("tokens", []) for x in evidence)]
    if missing and not exploration:
        raise ValueError("formal generation blocked: canonical tokens missing visual evidence: " + "; ".join(missing))

    prompt_spec = selected_era.get("prompt") or {}
    base = prompt_spec.get("cover") or (
        f"Preserve the supplied source image and subject identity. Recompose it using the selected "
        f"{selected_family['publication']} / {selected_era['label']} editorial grammar without copying logos, mastheads or a historical cover."
    )
    temporal = prompt_spec.get("emergence")
    parts = [base]
    if subject:
        parts.append(f"Subject / task: {subject}")
    parts.append("Selected canonical grammar:\n- " + "\n- ".join(grammar_lines))
    if temporal:
        parts.append("Temporal / Emergence translation: " + temporal)
    parts.append("Visual evidence authority: " + (", ".join(evidence_ids) if evidence_ids else "none"))
    parts.append("Generated images remain evaluation-only and are never historical authority.")
    if exploration:
        parts.append("Truth state: exploration / evaluation-only.")

    return {
        "schema": "dore.design-generation-resolution.v1",
        "consumer": consumer,
        "artifact_type": artifact_type,
        "family_id": selected_family["id"],
        "publication": selected_family["publication"],
        "grammar_id": era_id,
        "grammar_version": gdb.get("schema"),
        "truth_state": "exploration" if exploration else "canonical-resolved",
        "canonical_prompt": "\n\n".join(parts),
        "visual_evidence": evidence_ids,
        "admitted_candidates": [x["id"] for x in admitted],
        "authority_sources": [
            str(GRAMMARS.relative_to(ROOT)),
            str(EVIDENCE.relative_to(ROOT)),
            str(CANDIDATES.relative_to(ROOT)) if CANDIDATES.exists() else None,
        ],
        "missing_evidence": missing,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--era", required=True)
    p.add_argument("--module", action="append", dest="modules")
    p.add_argument("--subject")
    p.add_argument("--artifact-type", default="image")
    p.add_argument("--consumer", default="dore")
    p.add_argument("--exploration", action="store_true")
    p.add_argument("--prompt-only", action="store_true")
    a = p.parse_args()
    try:
        out = resolve(a.era, a.modules, a.subject, a.artifact_type, a.consumer, a.exploration)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"BLOCKED: {e}", file=sys.stderr)
        return 2
    print(out["canonical_prompt"] if a.prompt_only else json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
