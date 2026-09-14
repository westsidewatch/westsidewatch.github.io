#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "data/system-atlas.v0.json"
MAINLINE = ROOT / "docs/CURRENT_MAINLINE.md"

ALIASES = {
    "浮現": "capability:emergence",
    "emergence": "capability:emergence",
    "doré emergence": "capability:emergence",
    "dore emergence": "capability:emergence",
    "多寫": "tool:dore-folio",
    "doré folio": "tool:dore-folio",
    "dore folio": "tool:dore-folio",
    "one": "tool:one",
    "天堂電影院": "system:paradise-cinema",
    "paradise cinema": "system:paradise-cinema",
    "黎明書局": "system:dawn-library",
    "dawn library": "system:dawn-library",
}

AUTHORITY_RANK = {
    "github-current-canon": 500,
    "accepted-recent-decision": 400,
    "durable-history": 300,
    "memory-summary": 200,
    "model-inference": 100,
}


def load_atlas():
    return json.loads(ATLAS.read_text(encoding="utf-8"))


def resolve_entity(term, atlas):
    normalized = term.strip().casefold()
    entity_id = ALIASES.get(normalized)
    if entity_id:
        return next((e for e in atlas["entities"] if e["id"] == entity_id), None)
    for entity in atlas["entities"]:
        if normalized in {entity["id"].casefold(), entity.get("name", "").casefold()}:
            return entity
    return None


def existing_authority_files(entity):
    candidates = []
    for rel in entity.get("docs", []):
        path = ROOT / rel
        if path.is_file():
            candidates.append(rel)
    if MAINLINE.is_file() and "docs/CURRENT_MAINLINE.md" not in candidates:
        candidates.append("docs/CURRENT_MAINLINE.md")
    return candidates


def admit(term):
    atlas = load_atlas()
    entity = resolve_entity(term, atlas)
    if not entity:
        return {"schema":"dore.context-admission.v1","state":"unregistered","term":term,"mayAnswerEngineeringFacts":False,"reason":"UNKNOWN — registered engineering entity not resolved"}

    authority = existing_authority_files(entity)
    if not authority:
        return {"schema":"dore.context-admission.v1","state":"blocked","entity":entity["id"],"mayAnswerEngineeringFacts":False,"reason":"UNKNOWN — authoritative record not retrieved"}

    return {
        "schema":"dore.context-admission.v1",
        "state":"admitted",
        "entity":entity["id"],
        "name":entity.get("name"),
        "status":entity.get("status"),
        "authorityRank":"github-current-canon",
        "authorityFiles":authority,
        "relations":entity.get("relations", []),
        "mayAnswerEngineeringFacts":True,
        "policy":"Lower-ranked memory or inference may aid discovery but cannot override admitted GitHub authority.",
    }


if __name__ == "__main__":
    import sys
    term = " ".join(sys.argv[1:]).strip()
    print(json.dumps(admit(term), ensure_ascii=False, indent=2))
