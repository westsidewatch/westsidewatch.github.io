#!/usr/bin/env python3
"""Assemble AW-011 traversal order and enforce exact canonical-source relock."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Mapping


class TraversalError(ValueError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assemble(build_manifest: Mapping[str, Any], frames_report: Mapping[str, Any], out_dir: Path) -> dict[str, Any]:
    source = build_manifest.get("source")
    camera = build_manifest.get("camera")
    if not isinstance(source, dict) or not isinstance(camera, dict):
        raise TraversalError("build manifest missing source/camera")
    source_path = Path(str(source.get("path", "")))
    expected_sha = str(source.get("sha256", ""))
    canonical = str(source.get("canonical_pose_id", "P000"))
    if not source_path.is_file():
        raise TraversalError(f"canonical source missing: {source_path}")
    if _sha256(source_path) != expected_sha:
        raise TraversalError("canonical source fingerprint changed after preflight")

    ordered = camera.get("ordered_pose_ids")
    if not isinstance(ordered, list) or len(ordered) < 3:
        raise TraversalError("invalid Camera Spine ordering")
    pose_ids = [str(value) for value in ordered]
    if pose_ids[0] != canonical or pose_ids[-1] != canonical:
        raise TraversalError("Camera Spine must begin and return at canonical pose")

    raw_frames = frames_report.get("frames")
    if not isinstance(raw_frames, list):
        raise TraversalError("frames report missing accepted frames")
    accepted: dict[str, Path] = {}
    for raw in raw_frames:
        if not isinstance(raw, dict):
            raise TraversalError("invalid accepted frame record")
        pose_id = str(raw.get("id", "")).strip()
        path = Path(str(raw.get("output", "")))
        if not pose_id or pose_id in accepted or not path.is_file():
            raise TraversalError(f"invalid accepted frame for {pose_id}")
        accepted[pose_id] = path

    travel = [pose_id for pose_id in pose_ids[1:-1] if pose_id != canonical]
    missing = [pose_id for pose_id in travel if pose_id not in accepted]
    extra = [pose_id for pose_id in accepted if pose_id not in travel]
    if missing:
        raise TraversalError("accepted frames missing Camera Spine poses: " + ", ".join(missing))
    if extra:
        raise TraversalError("accepted frames contain poses outside Camera Spine: " + ", ".join(extra))

    relock_dir = out_dir / "frames"
    relock_dir.mkdir(parents=True, exist_ok=True)
    suffix = source_path.suffix or ".bin"
    return_path = relock_dir / f"{canonical}-return{suffix}"
    shutil.copyfile(source_path, return_path)
    if return_path.read_bytes() != source_path.read_bytes():
        raise TraversalError("exact source relock failed")

    sequence = [{"id": canonical, "role": "source_start", "path": str(source_path), "sha256": expected_sha}]
    for pose_id in travel:
        frame_path = accepted[pose_id]
        sequence.append({"id": pose_id, "role": "travel", "path": str(frame_path), "sha256": _sha256(frame_path)})
    sequence.append({"id": canonical, "role": "exact_source_relock", "path": str(return_path), "sha256": _sha256(return_path)})

    if sequence[-1]["sha256"] != expected_sha:
        raise TraversalError("return frame fingerprint is not canonical source")

    return {
        "aw_id": "AW-011",
        "stage": "traversal-assembly-v1",
        "canonical_pose_id": canonical,
        "sequence": sequence,
        "exact_source_relock": True,
        "status": "TRAVERSAL_READY",
    }
