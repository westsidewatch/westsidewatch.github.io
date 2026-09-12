#!/usr/bin/env python3
"""AW-011: depth-banded persistent hidden-world cache.

This experiment follows the geometric-support result but does not collapse the
recovered support back into generic LDI planes.  Each support sample keeps an
estimated canonical depth, is grouped into depth bands, and is rendered from a
persistent cache on every frame.  The Doré source remains authoritative for the
front layer and the final source pose is relocked exactly.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_geometric_support import sample_path, clean_holes
from experiment_world_cache import raster_layer


def collect_depth_conditioned_support(dep, poses, ppu=520.0, n=8, behind=0.08):
    h, w = dep.shape
    cx = np.float32((w - 1) * .5)
    cy = np.float32((h - 1) * .5)
    probe = np.dstack([np.uint8(np.clip(dep, 0, 1) * 255)] * 3)
    zsum = np.zeros((h, w), np.float32)
    weight = np.zeros((h, w), np.float32)
    mapped = 0
    errs = []
    used = 0

    for p in sample_path(poses, n):
        warped, known = raster_layer(probe, dep, p, ppu, 6, .10)
        shift = float(np.hypot(p[0] * ppu, p[1] * ppu))
        hole = clean_holes((known == 0).astype(np.uint8) * 255, shift)
        if not np.any(hole):
            continue

        zview = warped[:, :, 0].astype(np.float32) / 255.0
        missing = (known == 0).astype(np.uint8) * 255
        zfill = cv2.inpaint(zview, missing, 7.0, cv2.INPAINT_TELEA)
        yy, xx = np.nonzero(hole > 0)
        z = zfill[yy, xx]
        gain = np.float32(1.0 + max(-.35, min(.35, -float(p[2]) * .9)))
        sx = np.float32(p[0] * ppu) * (.35 + 1.30 * z)
        sy = np.float32(p[1] * ppu) * (.45 + .90 * z)
        ux = cx + (xx.astype(np.float32) - cx - sx) / gain
        uy = cy + (yy.astype(np.float32) - cy - sy) / gain
        ui = np.rint(ux).astype(np.int32)
        vi = np.rint(uy).astype(np.int32)
        valid = (ui >= 0) & (ui < w) & (vi >= 0) & (vi < h)
        if not np.any(valid):
            continue

        # Hidden support must sit behind the visible surface hypothesis.  Keep
        # the depth attached to each sample instead of replacing it with a
        # generic plane offset later.
        zh = np.clip(z[valid] - behind, 0.0, 1.0)
        np.add.at(zsum, (vi[valid], ui[valid]), zh)
        np.add.at(weight, (vi[valid], ui[valid]), 1.0)
        mapped += int(np.count_nonzero(valid))
        used += 1

        fx = cx + (ui[valid].astype(np.float32) - cx) * gain + np.float32(p[0] * ppu) * (.35 + 1.30 * z[valid])
        fy = cy + (vi[valid].astype(np.float32) - cy) * gain + np.float32(p[1] * ppu) * (.45 + .90 * z[valid])
        errs.append(float(np.mean(np.hypot(fx - xx[valid], fy - yy[valid]))))

    support = weight > 0
    zmap = np.zeros_like(dep, np.float32)
    zmap[support] = zsum[support] / weight[support]
    raw = support.astype(np.uint8) * 255
    raw = cv2.dilate(raw, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

    # Propagate recovered depths only inside the small dilated support band.
    inv = np.where(support, zmap, 0).astype(np.float32)
    miss = ((raw > 0) & (~support)).astype(np.uint8) * 255
    if np.any(miss):
        inv = cv2.inpaint(inv, miss, 3.0, cv2.INPAINT_TELEA)
    return raw, inv, used, mapped, (float(np.mean(errs)) if errs else 0.0)


def build_banded_cache(src, support, zmap, bands=4):
    valid = zmap[support > 0]
    if valid.size == 0:
        return []
    qs = np.quantile(valid, np.linspace(0, 1, bands + 1))
    layers = []
    for i in range(bands):
        lo, hi = float(qs[i]), float(qs[i + 1])
        if i == bands - 1:
            m = ((support > 0) & (zmap >= lo) & (zmap <= hi)).astype(np.uint8) * 255
        else:
            m = ((support > 0) & (zmap >= lo) & (zmap < hi)).astype(np.uint8) * 255
        if np.count_nonzero(m) < 32:
            continue
        # Context expansion is intentionally small. Large dilation is exactly
        # what can turn valid support into a giant false world patch.
        m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        rgb = cv2.inpaint(src, m, 5.0, cv2.INPAINT_TELEA)
        depth = zmap.copy()
        missing = ((m > 0) & (depth <= 0)).astype(np.uint8) * 255
        if np.any(missing):
            depth = cv2.inpaint(depth, missing, 3.0, cv2.INPAINT_TELEA)
        depth = np.clip(depth, 0, 1).astype(np.float32)
        layers.append((rgb, depth, m, (lo, hi)))
    return layers


def raster_support(mask, depth, p, ppu, step=6):
    rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    warped, known = raster_layer(rgb, depth, p, ppu, step, None)
    return (known > 0) & (warped[:, :, 0] > 96)


def render(src, dep, layers, p, ppu=520.0):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    # Render farthest first. Depth values are attached to support samples and
    # rasterized directly; no generic hidden-depth offsets are introduced here.
    order = sorted(range(len(layers)), key=lambda i: layers[i][3][0])
    for i in order:
        rgb, depth, mask, _ = layers[i]
        img, known = raster_layer(rgb, depth, p, ppu, 6, None)
        visible = raster_support(mask, depth, p, ppu, 6)
        take = (known > 0) & visible
        frame[take] = img[take]
        occupied[take] = 255

    front, front_known = raster_layer(src, dep, p, ppu, 6, .10)
    take_front = front_known > 0
    frame[take_front] = front[take_front]

    residual = (front_known == 0) & (occupied == 0)
    # Do not disguise a failed world as successful coverage. Residual pixels are
    # rendered black so visual review and validity metrics can see them.
    frame[residual] = 0
    unseen = float(np.count_nonzero(front_known == 0) / front_known.size)
    res = float(np.count_nonzero(residual) / front_known.size)
    coverage = max(0.0, unseen - res)
    return frame, unseen, coverage, res, front_known, occupied


def boundary_discontinuity(frame, front_known, occupied):
    hidden = ((front_known == 0) & (occupied > 0)).astype(np.uint8) * 255
    if not np.any(hidden):
        return 0.0, 0.0
    rim = cv2.morphologyEx(hidden, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)) > 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    local = cv2.GaussianBlur(gray, (0, 0), 2.0)
    jump = np.abs(gray - local)
    vals = jump[rim]
    if vals.size == 0:
        return 0.0, 0.0
    return float(np.mean(vals)), float(np.quantile(vals, .95))


def main():
    ap = argparse.ArgumentParser()
    for k in ('source', 'depth', 'spine', 'output', 'report'):
        ap.add_argument('--' + k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--width', type=int, default=960)
    ap.add_argument('--fps', type=int, default=24)
    ap.add_argument('--segment-frames', type=int, default=24)
    ap.add_argument('--ppu', type=float, default=520.0)
    ap.add_argument('--samples', type=int, default=8)
    ap.add_argument('--bands', type=int, default=4)
    ap.add_argument('--behind', type=float, default=.08)
    a = ap.parse_args()

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(dep, poses, a.ppu, a.samples, a.behind)
    layers = build_banded_cache(src, support, zmap, max(2, a.bands))
    if a.support_map:
        a.support_map.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(a.support_map), support)

    h, w = src.shape[:2]
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*'mp4v'), a.fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError('video writer failed')

    unseen, coverage, residual = [], [], []
    bmean, b95 = [], []
    worst = {'fraction': -1.0, 'frame': -1, 'pose': None}
    fn = 0
    for i in range(len(poses) - 1):
        p0 = np.asarray(poses[i]['position'], np.float32)
        p1 = np.asarray(poses[i + 1]['position'], np.float32)
        for j in range(a.segment_frames):
            t = smoothstep(j / float(a.segment_frames))
            p = p0 * (1 - t) + p1 * t
            if np.linalg.norm(p) < 1e-6:
                writer.write(src); fn += 1; continue
            frame, u, c, r, fk, occ = render(src, dep, layers, p, a.ppu)
            bm, bp = boundary_discontinuity(frame, fk, occ)
            writer.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r); bmean.append(bm); b95.append(bp)
            if r > worst['fraction']:
                worst = {'fraction': r, 'frame': fn, 'pose': [float(x) for x in p]}
            fn += 1
    writer.write(src)
    writer.release()

    maxu = max(unseen, default=0.0)
    maxr = max(residual, default=0.0)
    cov = float(np.mean([c/u if u > 1e-9 else 1.0 for c, u in zip(coverage, unseen)])) if unseen else 1.0
    sf = float(np.count_nonzero(support) / support.size)
    rep = {
        'status': 'DEPTH_BANDED_WORLD_CACHE_READY_FOR_VISUAL_REVIEW',
        'mode': 'camera_conditioned_depth_banded_persistent_world_cache',
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'support_fraction': sf,
        'depth_band_count': len(layers),
        'behind_offset': a.behind,
        'max_foreground_unseen_fraction': maxu,
        'mean_hidden_layer_coverage_ratio': cov,
        'max_residual_uncovered_fraction': maxr,
        'mean_hidden_boundary_discontinuity': float(np.mean(bmean)) if bmean else 0.0,
        'max_hidden_boundary_discontinuity_q95': max(b95, default=0.0),
        'worst_residual': worst,
        'exact_final_source_relock': True,
        'coverage_gate': bool(maxu > .001 and cov >= .96 and maxr <= .003),
        'visual_gate': 'PENDING_HUMAN_REVIEW',
        'rule': 'coverage_is_not_valid_world; visual review remains authoritative'
    }
    a.report.write_text(json.dumps(rep, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
