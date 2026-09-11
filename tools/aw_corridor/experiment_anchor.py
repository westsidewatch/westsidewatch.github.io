#!/usr/bin/env python3
"""Build the first end-to-end AW-011 experimental anchor/scaffold package.

This is an EXPERIMENT provider. It uses planar reprojection for known pixels and
OpenCV Telea inpainting only inside the measured unseen mask. The inferred pixels
are explicitly D_INFERRED_UNSEEN; they are not promoted to canonical Doré data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_mask(path: Path) -> np.ndarray:
    mask = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise ValueError(f"cannot read mask: {path}")
    return np.where(mask > 0, 255, 0).astype(np.uint8)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--spine", type=Path, required=True)
    ap.add_argument("--work-root", type=Path, required=True)
    ap.add_argument("--mask-manifest", type=Path, required=True)
    ap.add_argument("--scaffold-out", type=Path, required=True)
    ap.add_argument("--render-out", type=Path, required=True)
    ap.add_argument("--anchor-manifest-out", type=Path, required=True)
    ap.add_argument("--pixels-per-world-unit", type=float, default=420.0)
    args = ap.parse_args()

    source = cv2.imread(str(args.source), cv2.IMREAD_COLOR)
    if source is None:
        raise ValueError(f"cannot read source: {args.source}")
    height, width = source.shape[:2]

    spine = json.loads(args.spine.read_text(encoding="utf-8"))
    poses = spine["poses"]
    cpos = poses[0]["position"]
    travel = poses[1:-1]

    mask_manifest = json.loads(args.mask_manifest.read_text(encoding="utf-8"))
    mask_by_id = {p["id"]: p for p in mask_manifest["poses"]}

    scaffold = {
        "aw_id": "AW-011",
        "canonical_source_sha256": sha256(args.source),
        "provider": "planar-opencv-telea-experiment-v1",
        "poses": [],
    }
    render = {"aw_id": "AW-011", "poses": []}
    anchor_manifest = {
        "max_residual_unseen_fraction": 0.01,
        "poses": [],
        "candidates": [{
            "id": "A001-telea-inferred",
            "provenance": "D_INFERRED_UNSEEN",
            "coverage_masks": {},
            "redundancy_penalty": 0.0,
            "weak_overlap_penalty": 0.0,
        }],
    }
    report = {"provider": scaffold["provider"], "poses": []}

    for pose in travel:
        pose_id = pose["id"]
        pos = pose["position"]
        dx = int(round((float(pos[0]) - float(cpos[0])) * args.pixels_per_world_unit))
        dy = int(round((float(pos[1]) - float(cpos[1])) * args.pixels_per_world_unit))

        matrix = np.float32([[1, 0, dx], [0, 1, dy]])
        known = cv2.warpAffine(
            source, matrix, (width, height), flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0)
        )

        mask_entry = mask_by_id[pose_id]
        unseen_path = (args.mask_manifest.parent / mask_entry["unseen_mask"]).resolve()
        unseen = read_mask(unseen_path)
        if unseen.shape != (height, width):
            raise ValueError(f"mask dimensions differ for {pose_id}")
        known_mask = cv2.bitwise_not(unseen)

        generated = cv2.inpaint(known, unseen, 7.0, cv2.INPAINT_TELEA)
        # Preserve the measured known reprojection byte-for-byte. Only unseen pixels
        # are admitted from the inferred candidate.
        generated[known_mask > 0] = known[known_mask > 0]

        pose_dir = args.work_root / "poses" / pose_id
        pose_dir.mkdir(parents=True, exist_ok=True)
        known_path = pose_dir / "known.png"
        known_mask_path = pose_dir / "known-mask.png"
        unseen_copy = pose_dir / "unseen-mask.png"
        generated_path = args.work_root / "generated" / f"{pose_id}.png"
        generated_path.parent.mkdir(parents=True, exist_ok=True)
        coverage_path = args.work_root / "anchors" / "A001-telea-inferred" / f"{pose_id}-coverage.png"
        coverage_path.parent.mkdir(parents=True, exist_ok=True)

        if not cv2.imwrite(str(known_path), known):
            raise ValueError(f"failed to write {known_path}")
        if not cv2.imwrite(str(known_mask_path), known_mask):
            raise ValueError(f"failed to write {known_mask_path}")
        if not cv2.imwrite(str(unseen_copy), unseen):
            raise ValueError(f"failed to write {unseen_copy}")
        if not cv2.imwrite(str(generated_path), generated):
            raise ValueError(f"failed to write {generated_path}")
        if not cv2.imwrite(str(coverage_path), unseen):
            raise ValueError(f"failed to write {coverage_path}")

        def rel(path: Path, root: Path) -> str:
            return path.resolve().relative_to(root.resolve()).as_posix()

        scaffold["poses"].append({
            "id": pose_id,
            "known": rel(known_path, args.scaffold_out.parent),
            "known_mask": rel(known_mask_path, args.scaffold_out.parent),
            "unseen_mask": rel(unseen_copy, args.scaffold_out.parent),
        })
        render["poses"].append({
            "id": pose_id,
            "generated": rel(generated_path, args.render_out.parent),
        })
        anchor_manifest["poses"].append({
            "id": pose_id,
            "weight": 1.0,
            "unseen_mask": rel(unseen_copy, args.anchor_manifest_out.parent),
        })
        anchor_manifest["candidates"][0]["coverage_masks"][pose_id] = rel(
            coverage_path, args.anchor_manifest_out.parent
        )
        report["poses"].append({
            "id": pose_id,
            "dx_pixels": dx,
            "dy_pixels": dy,
            "unseen_pixels": int(np.count_nonzero(unseen)),
            "known_pixels": int(np.count_nonzero(known_mask)),
            "provenance": "D_INFERRED_UNSEEN",
            "generated": str(generated_path),
        })

    args.scaffold_out.write_text(json.dumps(scaffold, indent=2) + "\n", encoding="utf-8")
    args.render_out.write_text(json.dumps(render, indent=2) + "\n", encoding="utf-8")
    args.anchor_manifest_out.write_text(json.dumps(anchor_manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
