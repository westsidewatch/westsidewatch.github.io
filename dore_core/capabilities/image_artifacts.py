from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ImageArtifactRecord:
    id: str
    uri: str
    sha256: str
    bytes: int
    provenance: dict[str, Any]
    recipe: dict[str, Any]
    brief: dict[str, Any]


def record_image(path: Path, *, provenance: Mapping[str, Any], recipe: Mapping[str, Any], brief: Mapping[str, Any]) -> ImageArtifactRecord:
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    return ImageArtifactRecord(
        id=f"image:{digest[:16]}", uri=str(path), sha256=digest, bytes=len(data),
        provenance=dict(provenance), recipe=dict(recipe), brief=dict(brief),
    )


def persist_record(record: ImageArtifactRecord, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(asdict(record), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
