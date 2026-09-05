from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
from urllib.request import Request, urlopen

from .image_artifacts import ImageArtifactRecord
from .image_handoff import build_design_image_patch


def design_payload(artifact: ImageArtifactRecord, *, page_id: str = "cover",
                   placement: Mapping[str, float] | None = None,
                   asset_url: str | None = None, fit: str = "cover") -> dict[str, Any]:
    placement = placement or {"x": 0, "y": 0, "w": 1200, "h": 930}
    patch = build_design_image_patch(artifact, page_id=page_id, placement=placement, fit=fit)
    asset, shape = patch.to_asset_and_shape()
    a=asset.to_payload();s=shape.to_payload()
    if asset_url:a["uri"]=asset_url
    # Design node ids use the workspace's conservative id grammar.
    s["id"]="image-"+artifact.sha256[:16]
    return {"op":"place_image","page_id":page_id,"asset":a,"shape":s}


def place_in_design(artifact: ImageArtifactRecord, *, design_endpoint: str = "http://127.0.0.1:4310/api/workspace",
                    page_id: str = "cover", placement: Mapping[str, float] | None = None,
                    asset_url: str | None = None, fit: str = "cover", timeout: float = 3.0) -> dict[str, Any]:
    payload=design_payload(artifact,page_id=page_id,placement=placement,asset_url=asset_url,fit=fit)
    req=Request(design_endpoint,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urlopen(req,timeout=timeout) as r:
        out=json.loads(r.read().decode())
    if not isinstance(out,dict):raise RuntimeError("invalid Doré Design response")
    return out


def local_asset_url(artifact: ImageArtifactRecord, base: str = "http://127.0.0.1:8790/asset") -> str:
    from urllib.parse import quote
    return base+"?name="+quote(Path(artifact.uri).name)
