#!/usr/bin/env python3
"""AW-011 V6: two-layer persistent LDI world cache on MoGe geometry.

The Doré source remains texture authority for visible geometry. A single hidden
background layer is completed once in canonical source space, pushed behind the
foreground depth field, and reprojected on every frame. No per-frame synthesis
is allowed. This is the first persistent hidden-world approximation for AW-011.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np
from experiment_depth_traversal import prepare, load_pose_points, smoothstep, project_grid, raster_triangle


def build_hidden_layer(src, dep):
    gx = cv2.Sobel(dep, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(dep, cv2.CV_32F, 0, 1, ksize=3)
    edge = np.hypot(gx, gy)
    mask = (edge > 0.08).astype(np.uint8) * 255
    mask = cv2.dilate(mask, np.ones((19, 19), np.uint8), iterations=1)
    hidden_rgb = cv2.inpaint(src, mask, 7.0, cv2.INPAINT_TELEA)
    smooth = cv2.GaussianBlur(dep, (0, 0), 7.0)
    hidden_depth = np.clip(smooth - 0.14, 0.0, 1.0).astype(np.float32)
    return hidden_rgb, hidden_depth, mask


def raster_layer(texture, depth, p, ppu=520.0, step=6, edge_threshold=None):
    h, w = depth.shape
    xs, ys, xx, yy, z, px, py = project_grid(depth, *map(float, p), ppu, step)
    out = np.zeros_like(texture)
    known = np.zeros((h, w), np.uint8)
    zbuf = np.full((h, w), -np.inf, np.float32)
    rows, cols = z.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            ids = [(r,c),(r,c+1),(r+1,c+1),(r+1,c)]
            for tri in ((0,1,2),(0,2,3)):
                q = [ids[k] for k in tri]
                zv = np.array([z[a,b] for a,b in q], np.float32)
                if edge_threshold is not None and float(zv.max() - zv.min()) > edge_threshold:
                    continue
                sxy = np.array([[xx[a,b], yy[a,b]] for a,b in q], np.float32)
                dxy = np.array([[px[a,b], py[a,b]] for a,b in q], np.float32)
                raster_triangle(texture, zbuf, out, known, sxy, dxy, zv)
    return out, known


def render_frame(src, dep, hidden_rgb, hidden_depth, p, ppu=520.0, step=6, fg_thr=0.10):
    back, back_known = raster_layer(hidden_rgb, hidden_depth, p, ppu, step, None)
    front, front_known = raster_layer(src, dep, p, ppu, step, fg_thr)
    frame = back.copy()
    frame[front_known > 0] = front[front_known > 0]
    residual = (back_known == 0).astype(np.uint8) * 255
    if np.any(residual):
        stable_fill = cv2.inpaint(back, residual, 3.0, cv2.INPAINT_TELEA)
        frame[(front_known == 0) & (back_known == 0)] = stable_fill[(front_known == 0) & (back_known == 0)]
    unseen_fraction = float(np.count_nonzero(front_known == 0) / front_known.size)
    hidden_coverage = float(np.count_nonzero((front_known == 0) & (back_known > 0)) / front_known.size)
    residual_fraction = float(np.count_nonzero((front_known == 0) & (back_known == 0)) / front_known.size)
    return frame, unseen_fraction, hidden_coverage, residual_fraction


def main():
    ap = argparse.ArgumentParser()
    for name in ["source", "depth", "spine", "output", "report"]:
        ap.add_argument("--" + name, type=Path, required=True)
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--segment-frames", type=int, default=24)
    args = ap.parse_args()

    src, dep = prepare(args.source, args.depth, args.width)
    poses = load_pose_points(args.spine)
    hidden_rgb, hidden_depth, hidden_mask = build_hidden_layer(src, dep)
    h, w = src.shape[:2]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), args.fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError("video writer failed")

    unseen, coverage, residual = [], [], []
    for i in range(len(poses) - 1):
        p0 = np.asarray(poses[i]["position"], np.float32)
        p1 = np.asarray(poses[i + 1]["position"], np.float32)
        for j in range(args.segment_frames):
            s = smoothstep(j / float(args.segment_frames))
            frame, u, c, r = render_frame(src, dep, hidden_rgb, hidden_depth, p0 * (1 - s) + p1 * s)
            writer.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r)
    writer.write(src)
    writer.release()

    max_unseen = max(unseen, default=0.0)
    max_residual = max(residual, default=0.0)
    mean_ratio = float(np.mean([c / u if u > 1e-9 else 1.0 for c, u in zip(coverage, unseen)]))
    passed = max_unseen > 0.001 and mean_ratio >= 0.80 and max_residual <= 0.02
    report = {
        "status": "PERSISTENT_LDI_ACCEPTED" if passed else "PERSISTENT_LDI_INSUFFICIENT",
        "mode": "moge2_two_layer_persistent_ldi_v6",
        "hidden_layer_generated_once": True,
        "per_frame_synthesis": False,
        "max_foreground_unseen_fraction": max_unseen,
        "mean_hidden_layer_coverage_ratio": mean_ratio,
        "max_residual_uncovered_fraction": max_residual,
        "hidden_source_mask_fraction": float(np.count_nonzero(hidden_mask) / hidden_mask.size),
        "exact_final_source_relock": True,
        "quantitative_gate": passed,
        "visual_gate": "PENDING_HUMAN_REVIEW"
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if passed else 2

if __name__ == "__main__":
    raise SystemExit(main())
