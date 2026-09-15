#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "data/system-atlas.v0.json"
IDENTITIES = ROOT / "data/context-authority-entities.v1.json"

AUTHORITY_RANK = {
    "github-current-canon": 500,
    "accepted-recent-decision": 400,
    "durable-event-decision-history": 300,
    "memory-summary": 200,
    "model-inference": 100,
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_identity(term):
    normalized = term.strip().casefold()
    registry = load_json(IDENTITIES)
    for entity in registry["entities"]:
        keys = [entity["id"], *entity.get("aliases", [])]
        if normalized in {k.casefold() for k in keys}:
            return entity
    return None


def atlas_entity(entity_id):
    atlas = load_json(ATLAS)
    return next((e for e in atlas["entities"] if e["id"] == entity_id), None)


def admit(term):
    identity = resolve_identity(term)
    if not identity:
        return {"schema":"dore.context-admission.v1","state":"unregistered","term":term,"mayAnswerEngineeringFacts":False,"reason":"UNKNOWN — registered engineering entity not resolved"}

    required = identity.get("canonicalAuthority", [])
    missing = [rel for rel in required if not (ROOT / rel).is_file()]
    if missing:
        return {"schema":"dore.context-admission.v1","state":"blocked","entity":identity["id"],"missingAuthority":missing,"mayAnswerEngineeringFacts":False,"reason":identity.get("fallback", "UNKNOWN — authoritative record not retrieved")}

    atlas = atlas_entity(identity.get("atlasEntity"))
    if not atlas:
        return {"schema":"dore.context-admission.v1","state":"blocked","entity":identity["id"],"mayAnswerEngineeringFacts":False,"reason":"UNKNOWN — System Atlas entity not retrieved"}

    return {
        "schema":"dore.context-admission.v1",
        "state":"admitted",
        "entity":identity["id"],
        "atlasEntity":atlas["id"],
        "name":atlas.get("name"),
        "status":identity.get("status"),
        "authorityRank":"github-current-canon",
        "authorityFiles":required,
        "currentCheckpoint":identity.get("currentCheckpoint"),
        "canonicalPath":identity.get("canonicalPath"),
        "dependencies":identity.get("dependencies", []),
        "relations":atlas.get("relations", []),
        "mayAnswerEngineeringFacts":True,
        "policy":"Lower-ranked memory or inference may aid discovery but cannot override admitted GitHub authority.",
    }


if __name__ == "__main__":
    import sys
    print(json.dumps(admit(" ".join(sys.argv[1:]).strip()), ensure_ascii=False, indent=2))
