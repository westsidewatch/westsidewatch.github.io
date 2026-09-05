from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .image_artifacts import ImageArtifactRecord


@dataclass(frozen=True)
class DesignAsset:
    """Renderer-neutral asset identity owned by Doré, not by the canvas library."""
    id: str
    kind: str
    uri: str
    sha256: str
    provenance: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DesignImageShape:
    """Persistent design state. Konva/SVG are views over this shape, never the source of truth."""
    id: str
    type: str
    asset_id: str
    x: float
    y: float
    w: float
    h: float
    fit: str
    role: str
    rotation: float = 0.0

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DesignImagePatch:
    schema: str
    page_id: str
    asset_id: str
    uri: str
    sha256: str
    placement: dict[str, float]
    fit: str
    role: str
    provenance: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)

    def to_asset_and_shape(self) -> tuple[DesignAsset, DesignImageShape]:
        asset = DesignAsset(
            id=self.asset_id,
            kind="image",
            uri=self.uri,
            sha256=self.sha256,
            provenance=dict(self.provenance),
        )
        p = self.placement
        shape = DesignImageShape(
            id=f"shape:{self.asset_id}",
            type="image",
            asset_id=self.asset_id,
            x=p["x"], y=p["y"], w=p["w"], h=p["h"],
            fit=self.fit,
            role=self.role,
        )
        return asset, shape


def build_design_image_patch(artifact: ImageArtifactRecord, *, page_id: str,
                             placement: Mapping[str, float], fit: str = "cover",
                             role: str = "editorial-image") -> DesignImagePatch:
    required = ("x", "y", "w", "h")
    if any(key not in placement for key in required):
        raise ValueError("placement requires x, y, w, h")
    clean = {key: float(placement[key]) for key in required}
    if clean["w"] <= 0 or clean["h"] <= 0:
        raise ValueError("placement dimensions must be positive")
    if fit not in {"cover", "contain", "fill"}:
        raise ValueError("unsupported image fit")
    return DesignImagePatch(
        schema="dore.design.image-patch.v1",
        page_id=page_id,
        asset_id=artifact.id,
        uri=artifact.uri,
        sha256=artifact.sha256,
        placement=clean,
        fit=fit,
        role=role,
        provenance=dict(artifact.provenance),
    )
