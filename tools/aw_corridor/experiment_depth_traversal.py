#!/usr/bin/env python3
"""Render the depth-aware AW-011 Camera Corridor traversal.

V3 preserves the cumulative architecture and fixes the second human-review failure.
V1 read as a transparent moving layer. V2 fixed visibility with a z-buffer, but a
single-pixel forward splat left raster gaps; large Telea fills made moving regions
read as a blurred layer. V3 first rasterizes crisp source-RGB surface footprints
through the same z-buffer. Only residual destination pixels with no visible source
coverage are classified as unseen and sent to the temporary filler.
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


def rasterize_crisp_surface(
    source: np.ndarray,
    depth: np.ndarray,
    dst_x_f: np.ndarray,
    dst_y_f: np.ndarray,
    radius: int,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Forward-rasterize canonical RGB with a small opaque footprint and z-buffer.

    No alpha blending and no RGB averaging are allowed. Every covered destination
    pixel is copied from exactly one canonical Doré source pixel selected by depth.
    The footprint only closes sampling gaps created by forward projection; it does
    not invent RGB evidence.
    """
    h, w = depth.shape
    src_flat = source.reshape(-1, 3)
    depth_flat = depth.reshape(-1)
    x0 = np.rint(dst_x_f).astype(np.int32).reshape(-1)
    y0 = np.rint(dst_y_f).astype(np.int32).reshape(-1)

    zbuf = np.full(h * w, -1.0, dtype=np.float32)
    owner = np.full(h * w, -1, dtype=np.int64)
    projected_attempts = 0

    # Nearer samples win. Iterating offsets keeps the surface opaque while avoiding
    # the huge sparse-hole field that forced V2 to blur with large inpainting areas.
    for oy in range(-radius, radius + 1):
        for ox in range(-radius, radius + 1):
            dx = x0 + ox
            dy = y0 + oy
            valid = (dx >= 0) & (dx < w) & (dy >= 0) & (dy < h)
            src_ids = np.flatnonzero(valid)
            if src_ids.size == 0:
                continue
            dst_ids = dy[src_ids].astype(np.int64) * w + dx[src_ids].astype(np.int64)
            z = depth_flat[src_ids]
            projected_attempts += int(src_ids.size)

            # Sort far-to-near so the last write at a destination is the nearest.
            order = np.lexsort((z, dst_ids))
            d_sorted = dst_ids[order]
            s_sorted = src_ids[order]
            z_sorted = z[order]
            last = np.r_[d_sorted[1:] != d_sorted[:-1], True]
            d = d_sorted[last]
            s = s_sorted[last]
            zz = z_sorted[last]
            take = zz >= zbuf[d]
            d = d[take]
            s = s[take]
            zz = zz[take]
            zbuf[d] = zz
            owner[d] = s

    known_flat = owner >= 0
    projected = np.zeros((h * w, 3), dtype=np.uint8)
    projected[known_flat] = src_flat[owner[known_flat]]
    known = known_flat.reshape(h, w).astype(np.uint8) * 255
    collision_fraction = float(max(0, projected_attempts - int(np.count_nonzero(known_flat))) / max(1, projected_attempts))
    return projected.reshape(h, w, 3), known, collision_fraction


def forward_project_zbuffer(
    source: np.ndarray,
    depth: np.ndarray,
    cam_x: float,
    cam_y: float,
    cam_z: float,
    pixels_per_unit: float,
    splat_radius: int,
) -> tuple[np.ndarray, np.ndarray, dict]:
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
    dst_x_f = (cx + (xx - cx) * forward_gain + shift_x).astype(np.float32)
    dst_y_f = (cy + (yy - cy) * forward_gain + shift_y).astype(np.float32)

    projected, known, collision_fraction = rasterize_crisp_surface(
        source, depth, dst_x_f, dst_y_f, splat_radius
    )
    unseen = cv2.bitwise_not(known)

    # Fill only residual no-evidence pixels. Known RGB is never blurred or blended.
    unseen_fraction = float(np.count_nonzero(unseen) / unseen.size)
    if np.count_nonzero(unseen):
        filled = cv2.inpaint(projected, unseen, 2.0, cv2.INPAINT_TELEA)
        out = projected.copy()
        out[unseen > 0] = filled[unseen > 0]
    else:
        out = projected

    q1, q2 = np.quantile(depth, [1 / 3, 2 / 3])
    bands = [depth <= q1, (depth > q1) & (depth <= q2), depth > q2]
    band_shift = [float(np.mean(np.abs(shift_x[m]))) if np.any(m) else 0.0 for m in bands]
    metrics = {
        "camera": [float(cam_x), float(cam_y), float(cam_z)],
        "known_fraction": float(np.count_nonzero(known) / known.size),
        "unseen_fraction": unseen_fraction,
        "zbuffer_collision_fraction": collision_fraction,
        "splat_radius_px": int(splat_radius),
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
    ap.add_argument("--splat-radius", type=int, default=1)
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
                source, depth, float(p[0]), float(p[1]), float(p[2]),
                args.pixels_per_unit, args.splat_radius
            )
            writer.write(frame)
            m["segment"] = si
            m["frame"] = frame_count
            all_metrics.append(m)
            frame_count += 1

    writer.write(source)
    writer.release()
    frame_count += 1

    travel = [m for m in all_metrics if sum(abs(v) for v in m["camera"]) > 1e-6]
    max_span = max((m["depth_band_shift_span_px"] for m in travel), default=0.0)
    max_var = max((m["depth_band_shift_variance"] for m in travel), default=0.0)
    max_unseen = max((m["unseen_fraction"] for m in travel), default=0.0)
    max_proj_std = max((m["projected_x_displacement_std_px"] for m in travel), default=0.0)
    max_collision = max((m["zbuffer_collision_fraction"] for m in travel), default=0.0)

    passed = (
        max_span >= 3.0
        and max_var >= 1.0
        and max_proj_std >= 2.0
        and max_unseen > 0.001
        and max_collision > 0.0001
    )
    report = {
        "status": "GEOMETRIC_TRAVERSAL_ACCEPTED" if passed else "GEOMETRIC_TRAVERSAL_TOO_PLANAR",
        "mode": "depth_aware_camera_corridor_v3_crisp_surface_splat",
        "source_authority": "canonical_dore_011_rgb_forward_projected_once",
        "visibility_model": "opaque_forward_surface_splat_zbuffer_no_alpha_no_rgb_average",
        "depth_role": "geometry_evidence_only",
        "unseen_fill_role": "residual_no_evidence_pixels_only",
        "splat_radius_px": args.splat_radius,
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
