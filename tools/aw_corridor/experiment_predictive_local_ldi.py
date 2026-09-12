#!/usr/bin/env python3
"""AW-011 V8: predictive, region-local persistent LDI.

The camera spine is known before rendering.  V8 therefore predicts where depth
occlusion boundaries can expose unseen world, builds a canonical World Demand
Map, and spends extra hidden-world layers only inside those regions.

This is intentionally global as an algorithm and local as a workload:
  whole image + whole camera path -> demand regions -> local hidden world.
Known Doré RGB remains authoritative on the front layer and the final canonical
pose is relocked exactly to the source.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_world_cache import build_hidden_layer, raster_layer


def camera_demand_radius(poses, ppu: float) -> tuple[int, float]:
    """Predict the maximum image-plane exposure budget from the known spine."""
    if not poses:
        return 9, 0.0
    p0 = np.asarray(poses[0]["position"], np.float32)
    max_shift = 0.0
    for pose in poses:
        p = np.asarray(pose["position"], np.float32)
        d = p - p0
        # x/y translation dominates local disocclusion; z adds a smaller
        # expansion allowance because it changes apparent scale.
        shift = float(np.hypot(d[0], d[1]) * ppu + abs(d[2]) * ppu * 0.35)
        max_shift = max(max_shift, shift)
    # Keep the local band bounded; V8 must not silently become a global layer.
    radius = int(np.clip(np.ceil(max_shift) + 7, 9, 96))
    return radius, max_shift


def build_world_demand_map(dep: np.ndarray, poses, ppu: float, edge_q: float = 0.90):
    """Find depth discontinuities and expand only by the camera's future demand."""
    gx = cv2.Sobel(dep, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(dep, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.magnitude(gx, gy)
    nz = grad[grad > 0]
    thr = float(np.quantile(nz, edge_q)) if nz.size else 0.0
    # Retain an absolute floor so shallow texture noise does not purchase world.
    edge = (grad >= max(0.025, thr)).astype(np.uint8) * 255

    radius, predicted_shift = camera_demand_radius(poses, ppu)
    k = 2 * radius + 1
    demand = cv2.dilate(edge, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))

    # Remove tiny isolated regions; keep the rule semantic-free and reusable.
    n, labels, stats, _ = cv2.connectedComponentsWithStats((demand > 0).astype(np.uint8), 8)
    cleaned = np.zeros_like(demand)
    min_area = max(32, int(dep.size * 0.00008))
    components = []
    for i in range(1, n):
        area = int(stats[i, cv2.CC_STAT_AREA])
        if area < min_area:
            continue
        cleaned[labels == i] = 255
        components.append({
            "area": area,
            "x": int(stats[i, cv2.CC_STAT_LEFT]),
            "y": int(stats[i, cv2.CC_STAT_TOP]),
            "w": int(stats[i, cv2.CC_STAT_WIDTH]),
            "h": int(stats[i, cv2.CC_STAT_HEIGHT]),
        })
    return cleaned, edge, radius, predicted_shift, components, thr


def build_local_layers(src, dep, demand, count=3):
    """One global foundation + extra layers generated only for demand regions."""
    base_rgb, base_depth, base_mask = build_hidden_layer(src, dep)
    layers = []
    seed_rgb = base_rgb
    seed_depth = base_depth

    # Local layers recede behind occluders.  Their support masks are canonical,
    # persistent, and reused at every frame.
    for i in range(count):
        grow_px = 5 + 6 * i
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (grow_px * 2 + 1, grow_px * 2 + 1))
        support = cv2.dilate(demand, kernel)
        # Inpaint only the predicted world-demand support rather than the canvas.
        rgb = cv2.inpaint(seed_rgb, support, 5.0 + 3.0 * i, cv2.INPAINT_TELEA)
        smooth = cv2.GaussianBlur(seed_depth, (0, 0), 4.0 + 1.5 * i)
        depth = np.clip(smooth - (0.10 + 0.055 * i), 0.0, 1.0).astype(np.float32)
        layers.append((rgb, depth, support))
        seed_rgb, seed_depth = rgb, depth
    return (base_rgb, base_depth), layers, base_mask


def raster_support(mask, depth, p, ppu, step):
    rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    warped, known = raster_layer(rgb, depth, p, ppu, step, None)
    visible = (known > 0) & (warped[:, :, 0] > 96)
    return visible


def render(src, dep, base, locals_, p, ppu=520.0, step=6, fg_thr=0.10):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)
    contributions = [0] * (1 + len(locals_))

    # Global foundation remains a single layer; it prevents border holes but
    # does not receive additional world complexity.
    base_rgb, base_depth = base
    bimg, bknown = raster_layer(base_rgb, base_depth, p, ppu, step, None)
    take = bknown > 0
    frame[take] = bimg[take]
    occupied[take] = 255
    contributions[0] = int(np.count_nonzero(take))

    # Draw local hidden world farthest -> nearest, only inside projected support.
    for idx, (rgb, depth, support) in reversed(list(enumerate(locals_))):
        img, known = raster_layer(rgb, depth, p, ppu, step, None)
        local_visible = raster_support(support, depth, p, ppu, step)
        take = (known > 0) & local_visible
        # Local evidence is allowed to replace the coarse hidden foundation,
        # but never the authoritative front Doré layer.
        frame[take] = img[take]
        occupied[take] = 255
        contributions[1 + idx] += int(np.count_nonzero(take))

    front, front_known = raster_layer(src, dep, p, ppu, step, fg_thr)
    front_take = front_known > 0
    frame[front_take] = front[front_take]

    residual = (front_known == 0) & (occupied == 0)
    if np.any(residual):
        # Diagnostic border fallback only.  It is excluded from world coverage.
        stable = cv2.inpaint(frame, residual.astype(np.uint8) * 255, 3.0, cv2.INPAINT_TELEA)
        frame[residual] = stable[residual]

    u = float(np.count_nonzero(front_known == 0) / front_known.size)
    r = float(np.count_nonzero(residual) / front_known.size)
    return frame, u, max(0.0, u - r), r, contributions


def main():
    ap = argparse.ArgumentParser()
    for n in ("source", "depth", "spine", "output", "report"):
        ap.add_argument("--" + n, type=Path, required=True)
    ap.add_argument("--demand-map", type=Path)
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--segment-frames", type=int, default=24)
    ap.add_argument("--local-layers", type=int, default=3)
    ap.add_argument("--ppu", type=float, default=520.0)
    a = ap.parse_args()

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    demand, edge, radius, predicted_shift, components, edge_thr = build_world_demand_map(dep, poses, a.ppu)
    base, locals_, base_mask = build_local_layers(src, dep, demand, max(1, a.local_layers))

    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.demand_map:
        a.demand_map.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.demand_map), demand)

    h, w = src.shape[:2]
    wr = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*"mp4v"), a.fps, (w, h))
    if not wr.isOpened():
        raise RuntimeError("video writer failed")

    unseen, coverage, residual = [], [], []
    contributions = np.zeros(1 + len(locals_), np.int64)
    worst = {"fraction": -1.0, "frame": -1, "pose": None}
    frame_no = 0
    for i in range(len(poses) - 1):
        p0 = np.asarray(poses[i]["position"], np.float32)
        p1 = np.asarray(poses[i + 1]["position"], np.float32)
        for j in range(a.segment_frames):
            s = smoothstep(j / float(a.segment_frames))
            p = p0 * (1 - s) + p1 * s
            frame, u, c, r, contrib = render(src, dep, base, locals_, p, a.ppu)
            wr.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r)
            contributions += np.asarray(contrib, np.int64)
            if r > worst["fraction"]:
                worst = {"fraction": r, "frame": frame_no, "pose": [float(x) for x in p]}
            frame_no += 1

    wr.write(src)
    wr.release()

    max_u = max(unseen, default=0.0)
    max_r = max(residual, default=0.0)
    ratios = [c / u if u > 1e-9 else 1.0 for c, u in zip(coverage, unseen)]
    mean_ratio = float(np.mean(ratios))
    demand_fraction = float(np.count_nonzero(demand) / demand.size)

    # V8 is aimed at the final production zone: <0.2% raw residual while local
    # extra-world demand stays bounded.  Visual review remains authoritative.
    passed = max_u > 0.001 and mean_ratio >= 0.985 and max_r <= 0.002 and demand_fraction <= 0.45
    report = {
        "status": "PREDICTIVE_LOCAL_LDI_ACCEPTED" if passed else "PREDICTIVE_LOCAL_LDI_INSUFFICIENT",
        "mode": "moge2_predictive_local_world_demand_ldi_v8",
        "algorithm_scope": "global_detection_local_world_generation",
        "local_layer_count": len(locals_),
        "hidden_layers_generated_once": True,
        "per_frame_synthesis": False,
        "predicted_camera_shift_pixels": predicted_shift,
        "demand_radius_pixels": radius,
        "depth_edge_threshold": edge_thr,
        "world_demand_fraction": demand_fraction,
        "world_demand_component_count": len(components),
        "world_demand_components": components[:32],
        "max_foreground_unseen_fraction": max_u,
        "mean_hidden_layer_coverage_ratio": mean_ratio,
        "max_residual_uncovered_fraction": max_r,
        "worst_residual": worst,
        "base_hidden_source_mask_fraction": float(np.count_nonzero(base_mask) / base_mask.size),
        "layer_contributed_pixels_total": [int(x) for x in contributions],
        "exact_final_source_relock": True,
        "quantitative_gate": passed,
        "visual_gate": "PENDING_HUMAN_REVIEW"
    }
    a.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
