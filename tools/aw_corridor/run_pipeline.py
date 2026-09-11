#!/usr/bin/env python3
"""Continuous AW-011 production pipeline entrypoint.

Runs production preflight, optional scaffold ingestion, then optional unseen-only
frame admission. The runner stops at the first missing/invalid boundary and never
fabricates production artifacts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from frame_gate import FrameGateError, RasterError, compose
from run_aw011 import InputError, build
from scaffold_gate import MaskError, ScaffoldError, validate


def _load_json(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise InputError(f"missing JSON input: {path}")
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise InputError(f"JSON root must be an object: {path}")
    return obj


def _resolve(root: Path, value: Any, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{field} must be a non-empty path")
    path = Path(value)
    return path if path.is_absolute() else (root / path).resolve()


def _admit_frames(scaffold_manifest: Path, render_manifest: Path, out_dir: Path) -> dict[str, Any]:
    scaffold = _load_json(scaffold_manifest)
    render = _load_json(render_manifest)
    if render.get("aw_id") != "AW-011":
        raise InputError("render manifest aw_id must be AW-011")

    scaffold_root = scaffold_manifest.parent.resolve()
    render_root = render_manifest.parent.resolve()
    scaffold_poses_raw = scaffold.get("poses")
    render_poses_raw = render.get("poses")
    if not isinstance(scaffold_poses_raw, list) or not isinstance(render_poses_raw, list):
        raise InputError("scaffold/render poses must be lists")

    scaffold_by_id = {
        str(pose.get("id")): pose
        for pose in scaffold_poses_raw
        if isinstance(pose, dict) and str(pose.get("id", "")).strip()
    }
    render_by_id: dict[str, Mapping[str, Any]] = {}
    for raw in render_poses_raw:
        if not isinstance(raw, dict):
            raise InputError("each render pose must be an object")
        pose_id = str(raw.get("id", "")).strip()
        if not pose_id or pose_id in render_by_id:
            raise InputError(f"invalid or duplicate render pose id: {pose_id}")
        render_by_id[pose_id] = raw

    missing = [pose_id for pose_id in scaffold_by_id if pose_id not in render_by_id]
    extra = [pose_id for pose_id in render_by_id if pose_id not in scaffold_by_id]
    if missing:
        raise InputError("render manifest missing scaffold poses: " + ", ".join(missing))
    if extra:
        raise InputError("render manifest contains unknown poses: " + ", ".join(extra))

    frame_reports = []
    frames_dir = out_dir / "frames"
    for pose_id in scaffold_by_id:
        scaffold_pose = scaffold_by_id[pose_id]
        render_pose = render_by_id[pose_id]
        known = _resolve(scaffold_root, scaffold_pose.get("known"), f"scaffold[{pose_id}].known")
        unseen_mask = _resolve(
            scaffold_root,
            scaffold_pose.get("unseen_mask"),
            f"scaffold[{pose_id}].unseen_mask",
        )
        generated = _resolve(
            render_root,
            render_pose.get("generated"),
            f"render[{pose_id}].generated",
        )
        output = frames_dir / f"{pose_id}.png"
        report = compose(known, generated, unseen_mask, output)
        report["id"] = pose_id
        frame_reports.append(report)

    return {
        "status": "FRAMES_ACCEPTED",
        "pose_count": len(frame_reports),
        "frames": frame_reports,
    }


def run(
    production_manifest: Path,
    out_dir: Path,
    scaffold_manifest: Path | None = None,
    render_manifest: Path | None = None,
) -> dict:
    preflight = build(production_manifest, out_dir)
    result = {
        "aw_id": "AW-011",
        "stage": "camera-corridor-pipeline-v2",
        "preflight": preflight,
        "scaffold": None,
        "frames": None,
    }

    if preflight["status"] != "READY_FOR_SCAFFOLD":
        result["status"] = preflight["status"]
        return result
    if scaffold_manifest is None:
        result["status"] = "AWAITING_SCAFFOLD"
        return result

    scaffold_report = validate(out_dir / "build-manifest.json", scaffold_manifest)
    result["scaffold"] = scaffold_report
    if render_manifest is None:
        result["status"] = "SCAFFOLD_ACCEPTED"
        return result

    frame_report = _admit_frames(scaffold_manifest, render_manifest, out_dir)
    result["frames"] = frame_report
    result["status"] = "FRAMES_ACCEPTED"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("production_manifest", type=Path)
    parser.add_argument("--scaffold-manifest", type=Path)
    parser.add_argument("--render-manifest", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("build/aw-011"))
    args = parser.parse_args()

    try:
        report = run(
            args.production_manifest,
            args.out_dir,
            args.scaffold_manifest,
            args.render_manifest,
        )
    except (
        InputError,
        ScaffoldError,
        MaskError,
        FrameGateError,
        RasterError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        print(json.dumps({"aw_id": "AW-011", "status": "BLOCKED_PIPELINE", "error": str(exc)}))
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "pipeline-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] in (
        "AWAITING_SCAFFOLD",
        "SCAFFOLD_ACCEPTED",
        "FRAMES_ACCEPTED",
    ) else 3


if __name__ == "__main__":
    raise SystemExit(main())
