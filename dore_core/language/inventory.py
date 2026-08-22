"""Canonical reference inventory sidecars for Doré textual witnesses."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable
from .base import LanguageUnit, TextWitness


def canonical_refs(units: Iterable[LanguageUnit]) -> list[str]:
    """Return only refs already mapped into Doré's shared bible.ref namespace."""
    return sorted({u.canonical_ref_id for u in units if u.canonical_ref_id and u.canonical_ref_id.startswith("bible.ref.")})


def write_inventory(path: str | Path, witness: TextWitness, units: Iterable[LanguageUnit]) -> dict:
    units = tuple(units)
    refs = canonical_refs(units)
    books = sorted({ref.split(".")[2] for ref in refs})
    source_specific_refs = sorted({u.canonical_ref_id for u in units if u.canonical_ref_id and not u.canonical_ref_id.startswith("bible.ref.")})
    payload = {
        "schema": "dore.canonical-inventory.v0.1",
        "witness_id": witness.witness_id,
        "language": witness.language,
        "edition": witness.edition,
        "source_id": witness.source_id,
        "snapshot": witness.snapshot,
        "book_count": len(books),
        "book_ids": books,
        "canonical_ref_count": len(refs),
        "canonical_refs": refs,
        "source_specific_ref_count": len(source_specific_refs),
        "source_specific_ref_sample": source_specific_refs[:100],
    }
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def read_inventory(path: str | Path) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema") != "dore.canonical-inventory.v0.1":
        raise ValueError(f"unsupported inventory schema: {payload.get('schema')}")
    if not payload.get("witness_id") or not isinstance(payload.get("canonical_refs"), list):
        raise ValueError("invalid canonical inventory")
    return payload
