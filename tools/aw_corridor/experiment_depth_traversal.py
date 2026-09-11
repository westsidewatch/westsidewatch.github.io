#!/usr/bin/env python3
"""Render a depth-aware AW-011 traversal from the accepted monocular scaffold.

This is the next Camera Corridor engineering translation after the planar baseline.
It does not redefine the project as an 'enter the image' experiment. It asks one
narrow question: does the accepted world scaffold turn Camera Spine motion into
measurably non-planar parallax/disocclusion while canonical RGB remains the source
of all known pixels?
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def smoothstep(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def load_pose_points(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    poses = data.get("poses")
    if not isinstance(poses, list) or len(poses) < 4:
        raise ValueError("Camera Spine needs canonical, travel, and return poses")
    return poses


def prepare(source_path: Path, depth_path: Path, width: int) -> tuple[np.ndarray, np.ndarray]:
    src = cv2.imread(str(source_path), cv2.IMREAD_COLOR)
    if src is None:
        raise ValueError(f"cannot read source: {source_path}")
    depth = cv2.imread(str(depth_path), cv2.IMREAD_GRAYSCALE)
    if depth is None:
        raise ValueError(f"cannot read depth: {depth_path}")
    if width > 0 and src.shape[1] != width:
        h = int(round(src.shape[0] * width / src.shape[1]))
        src = cv2.resize(src, (width, h), interpolation=cv2.INTER_AREA)
        depth = cv2.resize(depth, (width, h), interpolation=cv2.INTER_CUBIC)
    elif depth.shape[:2] != src.shape[:2]:
        depth = cv2.resize(depth, (src.shape[1], src.shape[0]), interpolation=cv2.INTER_CUBIC)
    d = depth.astype(np.float32) / np.float32(255.0)
    lo, hi = np.quantile(d, [0.05, 0.95])
    dn = np.clip((d - lo) / max(1e-6, hi - lo), 0.0, 1.0).astype(np.float32)
    return src, dn


def render_depth_view(source: np.ndarray, depth: np.ndarray, cam_x: float, cam_y: float,
                      cam_z: float, pixels_per_unit: float) -> tuple[np.ndarray, np.ndarray, dict]:
    h, w = depth.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    base_x = np.float32(cam_x * pixels_per_unit)
    base_y = np.float32(cam_y * pixels_per_unit)
    near_weight = np.float32(0.35) + np.float32(1.30) * depth
    forward_gain = np.float32(1.0 + max(-0.35, min(0.35, -cam_z * 0.9)))

    shift_x = (base_x * near_weight).astype(np.float32)
    shift_y = (base_y * (np.float32(0.45) + np.float32(0.90) * depth)).astype(np.float32)

    cx = np.float32((w - 1) * 0.5)
    cy = np.float32((h - 1) * 0.5)
    map_x = (cx + (xx - cx) / forward_gain - shift_x).astype(np.float32)
    map_y = (cy + (yy - cy) / forward_gain - shift_y).astype(np.float32)

    known = ((map_x >= 0) & (map_x <= w - 1) & (map_y >= 0) & (map_y <= h - 1)).astype(np.uint8) * 255
    warped = cv2.remap(source, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    unseen = cv2.bitwise_not(known)
    if np.count_nonzero(unseen):
        filled = cv2.inpaint(warped, unseen, 3.0, cv2.INPAINT_TELEA)
        out = np.where(known[..., None] > 0, warped, filled)
    else:
        out = warped

    q1, q2 = np.quantile(depth, [1 / 3, 2 / 3])
    bands = [depth <= q1, (depth > q1) & (depth <= q2), depth > q2]
    band_shift = [float(np.mean(np.abs(shift_x[m]))) if np.any(m) else 0.0 for m in bands]
    metrics = {
        "camera": [float(cam_x), float(cam_y), float(cam_z)],
        "known_fraction": float(np.count_nonzero(known) / known.size),
        "unseen_fraction": float(np.count_nonzero(unseen) / unseen.size),
        "depth_band_mean_abs_x_shift_px": band_shift,
        "depth_band_shift_span_px": float(max(band_shift) - min(band_shift)),
        "depth_band_shift_variance": float(np.var(band_shift)),
        "map_x_std": float(np.std(map_x - xx)),
        "map_y_std": float(np.std(map_y - yy)),
    }
    return out, unseen, metrics


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--depth", type=Path, required=True)
    ap.add_argument("--spine", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--segment-frames", type=int, default=24)
    ap.add_argument("--pixels-per-unit", type=float, default=520.0)
    args = ap.parse_args()

    source, depth = prepare(args.source, args.depth, args.width)
    poses = load_pose_points(args.spine)
    h, w = source.shape[:2]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), args.fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError("video writer failed")

    all_metrics: list[dict] = []
    frame_count = 0
    for si in range(len(poses) - 1):
        a, b = poses[si], poses[si + 1]
        pa = np.asarray(a["position"], dtype=np.float32)
        pb = np.asarray(b["position"], dtype=np.float32)
        for j in range(args.segment_frames):
            t = j / float(args.segment_frames)
            s = smoothstep(t)
            p = pa * (1.0 - s) + pb * s
            frame, _, m = render_depth_view(source, depth, float(p[0]), float(p[1]), float(p[2]), args.pixels_per_unit)
            writer.write(frame)
            m["segment"] = si
            m["frame"] = frame_count
            all_metrics.append(m)
            frame_count += 1

    writer.write(source)
    writer.release()
    frame_count += 1

    travel = [m for m in all_metrics if abs(m["camera"][0]) + abs(m["camera"][1]) + abs(m["camera"][2]) > 1e-6]
    max_span = max((m["depth_band_shift_span_px"] for m in travel), default=0.0)
    max_var = max((m["depth_band_shift_variance"] for m in travel), default=0.0)
    max_unseen = max((m["unseen_fraction"] for m in travel), default=0.0)
    max_map_std = max((m["map_x_std"] for m in travel), default=0.0)

    passed = max_span >= 3.0 and max_var >= 1.0 and max_map_std >= 2.0 and max_unseen > 0.001
    report = {
        "status": "GEOMETRIC_TRAVERSAL_ACCEPTED" if passed else "GEOMETRIC_TRAVERSAL_TOO_PLANAR",
        "mode": "depth_aware_camera_corridor_v1",
        "source_authority": "known_rgb_reprojected_from_dore_011",
        "depth_role": "geometry_evidence_only",
        "resolution": [w, h],
        "fps": args.fps,
        "frame_count": frame_count,
        "duration_seconds": frame_count / args.fps,
        "max_depth_band_shift_span_px": max_span,
        "max_depth_band_shift_variance": max_var,
        "max_map_x_displacement_std_px": max_map_std,
        "max_unseen_fraction": max_unseen,
        "exact_final_source_relock": True,
        "gate": passed,
        "samples": all_metrics[::max(1, len(all_metrics)//12)],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
