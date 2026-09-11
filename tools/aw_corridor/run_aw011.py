#!/usr/bin/env python3
"""AW-011 production runner.

Validates the canonical Doré source + fixed Camera Spine, converts real warp masks
into planner evidence when supplied, runs the minimum-evidence planner, and writes
a deterministic build manifest. Missing real inputs are never invented.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from mask_evidence import build_problem
from plan_anchors import parse_problem, plan


class InputError(ValueError):
    pass


def _load_json(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise InputError(f"missing JSON input: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise InputError(f"JSON root must be an object: {path}")
    return data


def _resolve(root: Path, value: object, *, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{field} must be a non-empty path")
    path = Path(value)
    return path if path.is_absolute() else (root / path).resolve()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_camera_spine(
    data: Mapping[str, Any], canonical_pose_id: str
) -> list[Mapping[str, Any]]:
    poses = data.get("poses")
    if not isinstance(poses, list) or len(poses) < 3:
        raise InputError(
            "camera spine must contain at least departure, travel, and return poses"
        )
    for index, pose in enumerate(poses):
        if not isinstance(pose, dict) or not str(pose.get("id", "")).strip():
            raise InputError(f"camera pose #{index} must be an object with id")
    ids = [str(pose["id"]) for pose in poses]
    if ids[0] != canonical_pose_id:
        raise InputError(f"camera spine must start at canonical pose {canonical_pose_id}")
    if ids[-1] != canonical_pose_id:
        raise InputError(f"camera spine must return to canonical pose {canonical_pose_id}")
    if len(set(ids[1:-1])) != len(ids[1:-1]):
        raise InputError("non-canonical camera pose ids must be unique")
    return poses


def _load_evidence(
    root: Path,
    anchors: Mapping[str, Any],
    out_dir: Path,
) -> tuple[Mapping[str, Any], Path, str]:
    direct_value = anchors.get("candidate_coverage_file")
    mask_value = anchors.get("mask_manifest_file")

    if bool(direct_value) == bool(mask_value):
        raise InputError(
            "anchors must provide exactly one of candidate_coverage_file or mask_manifest_file"
        )

    if mask_value:
        mask_manifest_path = _resolve(
            root, mask_value, field="anchors.mask_manifest_file"
        )
        if not mask_manifest_path.is_file():
            raise InputError(f"missing mask manifest: {mask_manifest_path}")
        evidence_data = build_problem(mask_manifest_path)
        out_dir.mkdir(parents=True, exist_ok=True)
        evidence_path = out_dir / "evidence.from-masks.json"
        evidence_path.write_text(
            json.dumps(evidence_data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return evidence_data, evidence_path, "warp_masks"

    evidence_path = _resolve(
        root,
        direct_value,
        field="anchors.candidate_coverage_file",
    )
    return _load_json(evidence_path), evidence_path, "planner_json"


def build(manifest_path: Path, out_dir: Path) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    root = manifest_path.parent.resolve()

    if manifest.get("aw_id") != "AW-011":
        raise InputError("production manifest aw_id must be AW-011")

    source = manifest.get("source")
    if not isinstance(source, dict):
        raise InputError("source must be an object")
    canonical_pose_id = str(source.get("canonical_pose_id", "P000"))
    source_path = _resolve(root, source.get("asset"), field="source.asset")
    if not source_path.is_file():
        raise InputError(f"missing canonical Doré source: {source_path}")

    camera = manifest.get("camera")
    if not isinstance(camera, dict):
        raise InputError("camera must be an object")
    spine_path = _resolve(root, camera.get("spine_file"), field="camera.spine_file")
    spine_data = _load_json(spine_path)
    poses = validate_camera_spine(spine_data, canonical_pose_id)

    anchors = manifest.get("anchors")
    if not isinstance(anchors, dict):
        raise InputError("anchors must be an object")
    evidence_data, evidence_path, evidence_source = _load_evidence(
        root, anchors, out_dir
    )
    parsed_poses, candidates, threshold = parse_problem(evidence_data)

    camera_ids = [str(pose["id"]) for pose in poses]
    evidence_pose_ids = [pose.id for pose in parsed_poses]
    travel_ids = [
        pose_id
        for pose_id in camera_ids[1:-1]
        if pose_id != canonical_pose_id
    ]
    missing_evidence = [
        pose_id for pose_id in travel_ids if pose_id not in evidence_pose_ids
    ]
    extra_evidence = [
        pose_id for pose_id in evidence_pose_ids if pose_id not in travel_ids
    ]
    if missing_evidence:
        raise InputError(
            "evidence problem does not cover camera poses: "
            + ", ".join(missing_evidence)
        )
    if extra_evidence:
        raise InputError(
            "evidence problem contains poses outside Camera Spine: "
            + ", ".join(extra_evidence)
        )

    report = plan(parsed_poses, candidates, threshold)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "anchor-plan.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    scaffold = manifest.get("scaffold")
    provider = scaffold.get("provider") if isinstance(scaffold, dict) else None

    build_report = {
        "aw_id": "AW-011",
        "stage": "production-preflight-v2",
        "source": {
            "path": str(source_path),
            "sha256": _sha256(source_path),
            "canonical_pose_id": canonical_pose_id,
            "authority": "hard_source_lock",
        },
        "camera": {
            "spine_path": str(spine_path),
            "pose_count": len(poses),
            "ordered_pose_ids": camera_ids,
            "returns_to_source": camera_ids[-1] == canonical_pose_id,
        },
        "evidence": {
            "source": evidence_source,
            "problem_path": str(evidence_path),
            "pose_count": len(parsed_poses),
            "candidate_count": len(candidates),
            "selected_anchor_ids": report["selected_anchor_ids"],
            "corridor_passes_planner": report["corridor_passes"],
            "unresolved_pose_ids": report["unresolved_pose_ids"],
        },
        "scaffold": {
            "provider": provider,
            "replaceable": True,
        },
        "next_required_artifacts": [
            "poses/<pose-id>/known.png",
            "poses/<pose-id>/known-mask.png",
            "poses/<pose-id>/unseen-mask.png",
        ],
        "status": (
            "READY_FOR_SCAFFOLD"
            if report["corridor_passes"]
            else "NEEDS_ANCHOR_EVIDENCE"
        ),
    }

    (out_dir / "build-manifest.json").write_text(
        json.dumps(build_report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return build_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("build/aw-011"))
    args = parser.parse_args()

    try:
        report = build(args.manifest, args.out_dir)
    except (InputError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(
            json.dumps(
                {"aw_id": "AW-011", "status": "BLOCKED_INPUT", "error": str(exc)}
            )
        )
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "READY_FOR_SCAFFOLD" else 3


if __name__ == "__main__":
    raise SystemExit(main())
