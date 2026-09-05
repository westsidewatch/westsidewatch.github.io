from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ResidentImageConfig:
    schema: str
    endpoint: str
    model: str
    template: str
    output_dir: str
    vision_provider: str | None = None

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


def load_resident_image_config(path: Path) -> ResidentImageConfig:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("resident image config must be an object")
    if value.get("schema") != "dore.image.resident.v1":
        raise ValueError("unsupported resident image config schema")
    endpoint = str(value.get("endpoint", ""))
    if not endpoint.startswith("http://127.0.0.1:") and not endpoint.startswith("http://localhost:"):
        raise ValueError("resident image endpoint must be loopback-local")
    model = str(value.get("model", "")).strip()
    template = str(value.get("template", "")).strip()
    output_dir = str(value.get("output_dir", "dore-image/generated")).strip()
    if not model or not template:
        raise ValueError("resident image config requires model and template")
    return ResidentImageConfig(
        schema="dore.image.resident.v1", endpoint=endpoint, model=model,
        template=template, output_dir=output_dir,
        vision_provider=str(value["vision_provider"]) if value.get("vision_provider") else None,
    )
