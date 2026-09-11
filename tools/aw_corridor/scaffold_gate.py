#!/usr/bin/env python3
"""Validate provider-neutral AW-011 scaffold/warp output before planning/rendering.

The gate binds provider output to the canonical source fingerprint and Camera Spine,
then verifies each travel pose has a known frame plus complementary strict binary
known/unseen masks with matching dimensions. Optional depth/confidence artifacts are
accepted but not interpreted here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path
from typing import Any, Mapping

from mask_evidence import MaskError, read_binary_png

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class ScaffoldError(ValueError):
    pass


def _load_json(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise ScaffoldError(f"missing JSON input: {path}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ScaffoldError(f"JSON root must be an object: {path}")
    return obj


def _resolve(root: Path, value: Any, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ScaffoldError(f"{field} must be a non-empty path")
    path = Path(value)
    return path if path.is_absolute() else (root / path).resolve()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or not data.startswith(PNG_SIGNATURE):
        raise ScaffoldError(f"known frame must be PNG: {path}")
    if data[12:16] != b"IHDR":
        raise ScaffoldError(f"PNG missing leading IHDR: {path}")
    width, height = struct.unpack(">II", data[16:24])
    if width <= 0 or height <= 0:
        raise ScaffoldError(f"invalid PNG dimensions: {path}")
    return width, height


def _travel_ids(build_manifest: Mapping[str, Any]) -> tuple[str, list[str]]:
    source = build_manifest.get("source")
    camera = build_manifest.get("camera")
    if not isinstance(source, dict) or not isinstance(camera, dict):
        raise ScaffoldError("build manifest missing source/camera contract")
    canonical = str(source.get("canonical_pose_id", "P000"))
    ordered = camera.get("ordered_pose_ids")
    if not isinstance(ordered, list) or len(ordered) < 3:
        raise ScaffoldError("build manifest camera.ordered_pose_ids is invalid")
    ids = [str(value) for value in ordered]
    if ids[0] != canonical or ids[-1] != canonical:
        raise ScaffoldError("build manifest Camera Spine does not hard-return to source")
    return canonical, [pose_id for pose_id in ids[1:-1] if pose_id != canonical]


def validate(build_manifest_path: Path, scaffold_manifest_path: Path) -> dict[str, Any]:
    build = _load_json(build_manifest_path)
    scaffold = _load_json(scaffold_manifest_path)
    root = scaffold_manifest_path.parent.resolve()

    if build.get("aw_id") != "AW-011" or scaffold.get("aw_id") != "AW-011":
        raise ScaffoldError("both manifests must declare aw_id AW-011")

    source = build.get("source")
    if not isinstance(source, dict):
        raise ScaffoldError("build manifest missing source")
    expected_sha = str(source.get("sha256", "")).strip()
    supplied_sha = str(scaffold.get("canonical_source_sha256", "")).strip()
    if not expected_sha or supplied_sha != expected_sha:
        raise ScaffoldError("scaffold canonical_source_sha256 does not match preflight source")

    canonical, travel_ids = _travel_ids(build)
    poses_raw = scaffold.get("poses")
    if not isinstance(poses_raw, list):
        raise ScaffoldError("scaffold poses must be a list")

    by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw in enumerate(poses_raw):
        if not isinstance(raw, dict):
            raise ScaffoldError(f"scaffold pose #{index} must be an object")
        pose_id = str(raw.get("id", "")).strip()
        if not pose_id or pose_id in by_id:
            raise ScaffoldError(f"invalid or duplicate scaffold pose id: {pose_id}")
        if pose_id == canonical:
            raise ScaffoldError("canonical P000 must not be synthesized by scaffold provider")
        by_id[pose_id] = raw

    missing = [pose_id for pose_id in travel_ids if pose_id not in by_id]
    extra = [pose_id for pose_id in by_id if pose_id not in travel_ids]
    if missing:
        raise ScaffoldError("scaffold missing Camera Spine poses: " + ", ".join(missing))
    if extra:
        raise ScaffoldError("scaffold contains poses outside Camera Spine: " + ", ".join(extra))

    pose_reports: list[dict[str, Any]] = []
    for pose_id in travel_ids:
        raw = by_id[pose_id]
        known_path = _resolve(root, raw.get("known"), f"poses[{pose_id}].known")
        known_mask_path = _resolve(
            root, raw.get("known_mask"), f"poses[{pose_id}].known_mask"
        )
        unseen_mask_path = _resolve(
            root, raw.get("unseen_mask"), f"poses[{pose_id}].unseen_mask"
        )
        for path in (known_path, known_mask_path, unseen_mask_path):
            if not path.is_file():
                raise ScaffoldError(f"missing scaffold artifact: {path}")

        known_dims = png_dimensions(known_path)
        km_w, km_h, known_mask = read_binary_png(known_mask_path)
        um_w, um_h, unseen_mask = read_binary_png(unseen_mask_path)
        if known_dims != (km_w, km_h) or known_dims != (um_w, um_h):
            raise ScaffoldError(
                f"artifact dimensions differ for {pose_id}: known={known_dims}, "
                f"known_mask={(km_w, km_h)}, unseen_mask={(um_w, um_h)}"
            )

        overlap = 0
        holes = 0
        known_count = 0
        unseen_count = 0
        for known_bit, unseen_bit in zip(known_mask, unseen_mask):
            known_count += int(known_bit)
            unseen_count += int(unseen_bit)
            overlap += int(known_bit and unseen_bit)
            holes += int((not known_bit) and (not unseen_bit))
        if overlap:
            raise ScaffoldError(f"known/unseen masks overlap at {overlap} pixels for {pose_id}")
        if holes:
            raise ScaffoldError(f"known/unseen masks leave {holes} unclassified pixels for {pose_id}")

        optional: dict[str, dict[str, Any]] = {}
        for field in ("depth", "confidence"):
            value = raw.get(field)
            if value is None:
                continue
            path = _resolve(root, value, f"poses[{pose_id}].{field}")
            if not path.is_file():
                raise ScaffoldError(f"missing optional scaffold artifact: {path}")
            optional[field] = {"path": str(path), "sha256": _sha256(path)}

        total = known_count + unseen_count
        pose_reports.append(
            {
                "id": pose_id,
                "width": known_dims[0],
                "height": known_dims[1],
                "known_pixels": known_count,
                "unseen_pixels": unseen_count,
                "unseen_fraction": unseen_count / total if total else 0.0,
                "known_sha256": _sha256(known_path),
                "known_mask_sha256": _sha256(known_mask_path),
                "unseen_mask_sha256": _sha256(unseen_mask_path),
                "optional": optional,
            }
        )

    provider = scaffold.get("provider")
    return {
        "aw_id": "AW-011",
        "stage": "scaffold-ingestion-v1",
        "canonical_source_sha256": expected_sha,
        "provider": provider,
        "provider_replaceable": True,
        "pose_count": len(pose_reports),
        "poses": pose_reports,
        "status": "SCAFFOLD_ACCEPTED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_manifest", type=Path)
    parser.add_argument("scaffold_manifest", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        report = validate(args.build_manifest, args.scaffold_manifest)
    except (OSError, json.JSONDecodeError, MaskError, ScaffoldError, ValueError) as exc:
        print(json.dumps({"aw_id": "AW-011", "status": "BLOCKED_SCAFFOLD", "error": str(exc)}))
        return 2
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
