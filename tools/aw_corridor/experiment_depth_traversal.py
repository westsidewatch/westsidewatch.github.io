#!/usr/bin/env python3
"""Render a depth-aware AW-011 traversal from the accepted monocular scaffold.

This extends the already-passing Camera Corridor rather than changing its goal.
V2 fixes the visual failure found in human review of V1: backward remapping could
make displaced Doré structures read like a transparent moving layer. V2 projects
canonical source pixels forward into the new camera pose, resolves competing
surfaces with a z-buffer, and synthesizes only destination pixels with no visible
source evidence.
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


def forward_project_zbuffer(
    source: np.ndarray,
    depth: np.ndarray,
    cam_x: float,
    cam_y: float,
    cam_z: float,
    pixels_per_unit: float,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """Project canonical Doré RGB once, then resolve visibility in destination space.

    Depth is geometry evidence only. RGB always comes from canonical source pixels.
    A destination pixel receives at most one visible source surface: the nearest
    (largest normalized depth in the current experimental convention) wins.
    """
    h, w = depth.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

    base_x = np.float32(cam_x * pixels_per_unit)
    base_y = np.float32(cam_y * pixels_per_unit)
    near_x = np.float32(0.35) + np.float32(1.30) * depth
    near_y = np.float32(0.45) + np.float32(0.90) * depth
    forward_gain = np.float32(1.0 + max(-0.35, min(0.35, -cam_z * 0.9)))

    shift_x = (base_x * near_x).astype(np.float32)
    shift_y = (base_y * near_y).astype(np.float32)
    cx = np.float32((w - 1) * 0.5)
    cy = np.float32((h - 1) * 0.5)

    # Forward projection: canonical pixel -> camera-space destination.
    dst_x_f = (cx + (xx - cx) * forward_gain + shift_x).astype(np.float32)
    dst_y_f = (cy + (yy - cy) * forward_gain + shift_y).astype(np.float32)
    dst_x = np.rint(dst_x_f).astype(np.int32)
    dst_y = np.rint(dst_y_f).astype(np.int32)

    in_bounds = (dst_x >= 0) & (dst_x < w) & (dst_y >= 0) & (dst_y < h)
    src_flat = source.reshape(-1, 3)
    depth_flat = depth.reshape(-1)
    in_flat = in_bounds.reshape(-1)
    dx_flat = dst_x.reshape(-1)
    dy_flat = dst_y.reshape(-1)

    src_ids = np.flatnonzero(in_flat)
    dst_ids = dy_flat[src_ids].astype(np.int64) * w + dx_flat[src_ids].astype(np.int64)
    src_depth = depth_flat[src_ids]

    # Z-buffer in destination space. np.maximum.at makes visibility deterministic
    # and avoids retaining the old source position beneath a displaced foreground.
    zbuf = np.full(h * w, -1.0, dtype=np.float32)
    np.maximum.at(zbuf, dst_ids, src_depth)
    winner = src_depth >= (zbuf[dst_ids] - np.float32(1e-6))
    winner_src = src_ids[winner]
    winner_dst = dst_ids[winner]

    # If equal-depth pixels collide, deterministic later assignment is harmless:
    # they represent the same local depth surface, not two alpha-composited layers.
    projected = np.zeros((h * w, 3), dtype=np.uint8)
    projected[winner_dst] = src_flat[winner_src]
    projected = projected.reshape(h, w, 3)

    known = (zbuf.reshape(h, w) >= 0.0).astype(np.uint8) * 255
    unseen = cv2.bitwise_not(known)

    # Only genuinely unobserved destination pixels are synthesized. Telea remains
    # a temporary corridor filler, not world geometry and not source evidence.
    if np.count_nonzero(unseen):
        filled = cv2.inpaint(projected, unseen, 3.0, cv2.INPAINT_TELEA)
        out = np.where(known[..., None] > 0, projected, filled)
    else:
        out = projected

    q1, q2 = np.quantile(depth, [1 / 3, 2 / 3])
    bands = [depth <= q1, (depth > q1) & (depth <= q2), depth > q2]
    band_shift = [float(np.mean(np.abs(shift_x[m]))) if np.any(m) else 0.0 for m in bands]

    in_count = int(src_ids.size)
    unique_visible = int(np.count_nonzero(known))
    collision_count = max(0, in_count - unique_visible)
    metrics = {
        "camera": [float(cam_x), float(cam_y), float(cam_z)],
        "known_fraction": float(unique_visible / known.size),
        "unseen_fraction": float(np.count_nonzero(unseen) / unseen.size),
        "source_projected_in_bounds_fraction": float(in_count / depth.size),
        "zbuffer_collision_fraction": float(collision_count / max(1, in_count)),
        "depth_band_mean_abs_x_shift_px": band_shift,
        "depth_band_shift_span_px": float(max(band_shift) - min(band_shift)),
        "depth_band_shift_variance": float(np.var(band_shift)),
        "projected_x_displacement_std_px": float(np.std(dst_x_f - xx)),
        "projected_y_displacement_std_px": float(np.std(dst_y_f - yy)),
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
            frame, _, m = forward_project_zbuffer(
                source, depth, float(p[0]), float(p[1]), float(p[2]), args.pixels_per_unit
            )
            writer.write(frame)
            m["segment"] = si
            m["frame"] = frame_count
            all_metrics.append(m)
            frame_count += 1

    # Canonical authority is never reconstructed at relock: it is the source.
    writer.write(source)
    writer.release()
    frame_count += 1

    travel = [m for m in all_metrics if sum(abs(v) for v in m["camera"]) > 1e-6]
    max_span = max((m["depth_band_shift_span_px"] for m in travel), default=0.0)
    max_var = max((m["depth_band_shift_variance"] for m in travel), default=0.0)
    max_unseen = max((m["unseen_fraction"] for m in travel), default=0.0)
    max_proj_std = max((m["projected_x_displacement_std_px"] for m in travel), default=0.0)
    max_collision = max((m["zbuffer_collision_fraction"] for m in travel), default=0.0)

    # Geometric gate remains cumulative: depth-dependent motion + actual visibility
    # events + disocclusion + exact authority relock. Human visual review is a
    # separate mandatory gate and can still reject this quantitative PASS.
    passed = (
        max_span >= 3.0
        and max_var >= 1.0
        and max_proj_std >= 2.0
        and max_unseen > 0.001
        and max_collision > 0.0001
    )
    report = {
        "status": "GEOMETRIC_TRAVERSAL_ACCEPTED" if passed else "GEOMETRIC_TRAVERSAL_TOO_PLANAR",
        "mode": "depth_aware_camera_corridor_v2_zbuffer",
        "source_authority": "canonical_dore_011_rgb_forward_projected_once",
        "visibility_model": "forward_projection_zbuffer_no_alpha_layering",
        "depth_role": "geometry_evidence_only",
        "unseen_fill_role": "temporary_non_evidence_fill_only",
        "resolution": [w, h],
        "fps": args.fps,
        "frame_count": frame_count,
        "duration_seconds": frame_count / args.fps,
        "max_depth_band_shift_span_px": max_span,
        "max_depth_band_shift_variance": max_var,
        "max_map_x_displacement_std_px": max_proj_std,
        "max_unseen_fraction": max_unseen,
        "max_zbuffer_collision_fraction": max_collision,
        "exact_final_source_relock": True,
        "quantitative_gate": passed,
        "visual_gate": "PENDING_HUMAN_REVIEW",
        "gate": passed,
        "samples": all_metrics[::max(1, len(all_metrics) // 12)],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
