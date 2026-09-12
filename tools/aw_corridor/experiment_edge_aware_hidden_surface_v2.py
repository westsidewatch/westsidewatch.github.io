#!/usr/bin/env python3
"""AW-011 fast falsification: one persistent edge-aware hidden surface.

This keeps the exact upstream geometry/world-demand path fixed and tests only
whether explicit occlusion topology improves the hidden world.  Unlike the first
edge-aware prototype, all edge components are composited into one persistent
surface so rendering cost does not scale with component count.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_edge_aware_hidden_surface import occlusion_topology
from experiment_world_cache import raster_layer


def build_surface(src, dep, support, zmap, topo, behind_margin=.025, context_radius=19):
    relevant = topo['relevant_support'] > 0
    foreground = topo['foreground'] > 0
    local_min = topo['local_min']

    # Only support attached to a real depth discontinuity enters this test.
    demanded = relevant.copy()
    mask = demanded.astype(np.uint8) * 255
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    m = mask > 0

    target_back = np.clip(local_min - behind_margin, 0.0, 1.0)
    hz = zmap.copy()
    have = hz > 0
    hz[m & have] = np.minimum(hz[m & have], target_back[m & have])
    hz[m & (~have)] = target_back[m & (~have)]

    # Mask foreground-side context out of the completion problem.  Telea remains
    # a diagnostic colour completer here; the hypothesis under test is topology,
    # not learned appearance synthesis.
    near = cv2.dilate(mask, cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (2 * context_radius + 1, 2 * context_radius + 1))) > 0
    completion = m | (foreground & near & (topo['zone'] > 0))
    rgb = cv2.inpaint(src, completion.astype(np.uint8) * 255, 7.0, cv2.INPAINT_TELEA)

    depth = dep.copy()
    depth[m] = np.where(hz[m] > 0, hz[m], target_back[m])
    depth = np.clip(depth, 0, 1).astype(np.float32)
    unresolved = ((support > 0) & (~relevant)).astype(np.uint8) * 255

    labels = topo['labels']
    ids = np.unique(labels[demanded])
    ids = ids[ids > 0]
    summaries = []
    for edge_id in ids.tolist():
        z = demanded & (labels == edge_id)
        if not np.any(z):
            continue
        summaries.append({
            'edge_id': int(edge_id),
            'support_pixels': int(np.count_nonzero(z)),
            'median_hidden_depth': float(np.median(depth[z])),
        })
    return rgb, depth, mask, unresolved, summaries


def raster_support(mask, depth, p, ppu, sever_threshold):
    probe = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    warped, known = raster_layer(probe, depth, p, ppu, 6, sever_threshold)
    return (known > 0) & (warped[:, :, 0] > 96)


def render(src, dep, rgb, hidden_depth, mask, p, ppu=520.0, sever_threshold=.065):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    himg, hknown = raster_layer(rgb, hidden_depth, p, ppu, 6, sever_threshold)
    hvisible = raster_support(mask, hidden_depth, p, ppu, sever_threshold)
    take = (hknown > 0) & hvisible
    frame[take] = himg[take]
    occupied[take] = 255

    front, front_known = raster_layer(src, dep, p, ppu, 6, .10)
    ft = front_known > 0
    frame[ft] = front[ft]

    residual = (front_known == 0) & (occupied == 0)
    frame[residual] = 0
    unseen = float(np.count_nonzero(front_known == 0) / front_known.size)
    res = float(np.count_nonzero(residual) / front_known.size)
    return frame, unseen, max(0.0, unseen - res), res, front_known, occupied


def boundary_discontinuity(frame, front_known, occupied):
    hidden = ((front_known == 0) & (occupied > 0)).astype(np.uint8) * 255
    if not np.any(hidden):
        return 0.0, 0.0
    rim = cv2.morphologyEx(hidden, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8)) > 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    local = cv2.GaussianBlur(gray, (0, 0), 2.0)
    vals = np.abs(gray - local)[rim]
    if vals.size == 0:
        return 0.0, 0.0
    return float(np.mean(vals)), float(np.quantile(vals, .95))


def main():
    ap = argparse.ArgumentParser()
    for k in ('source', 'depth', 'spine', 'output', 'report'):
        ap.add_argument('--' + k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--edge-map', type=Path)
    ap.add_argument('--background-map', type=Path)
    ap.add_argument('--unresolved-map', type=Path)
    ap.add_argument('--width', type=int, default=960)
    ap.add_argument('--fps', type=int, default=24)
    ap.add_argument('--segment-frames', type=int, default=12)
    ap.add_argument('--ppu', type=float, default=520.0)
    ap.add_argument('--samples', type=int, default=8)
    ap.add_argument('--behind', type=float, default=.08)
    ap.add_argument('--edge-q', type=float, default=.90)
    ap.add_argument('--min-jump', type=float, default=.055)
    ap.add_argument('--zone-radius', type=int, default=31)
    ap.add_argument('--sever-threshold', type=float, default=.065)
    a = ap.parse_args()

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(
        dep, poses, a.ppu, a.samples, a.behind)
    topo = occlusion_topology(dep, support, a.edge_q, .025, a.min_jump, a.zone_radius)
    rgb, hdep, hmask, unresolved, summaries = build_surface(src, dep, support, zmap, topo)

    for path, image in ((a.support_map, support), (a.edge_map, topo['edge']),
                        (a.background_map, topo['background']), (a.unresolved_map, unresolved)):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(path), image)

    h, w = src.shape[:2]
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*'mp4v'), a.fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError('video writer failed')

    unseen, coverage, residual, bmean, b95 = [], [], [], [], []
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
            frame, u, c, r, fk, occ = render(src, dep, rgb, hdep, hmask, p, a.ppu, a.sever_threshold)
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
    support_pixels = max(1, np.count_nonzero(support))
    attached = float(np.count_nonzero(topo['relevant_support']) / support_pixels)
    unresolved_ratio = float(np.count_nonzero(unresolved) / support_pixels)
    rep = {
        'status': 'EDGE_TOPOLOGY_FALSIFICATION_READY_FOR_VISUAL_REVIEW',
        'mode': 'single_persistent_occlusion_topology_hidden_surface',
        'hypothesis': 'large defects are primarily caused by lost foreground/background occlusion topology',
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'support_fraction': float(np.count_nonzero(support) / support.size),
        'occlusion_component_count': topo['component_count'],
        'edge_gradient_threshold': topo['threshold'],
        'minimum_depth_jump': a.min_jump,
        'zone_radius_pixels': a.zone_radius,
        'triangle_sever_threshold': a.sever_threshold,
        'support_attached_to_occlusion_topology_ratio': attached,
        'unresolved_support_ratio': unresolved_ratio,
        'max_foreground_unseen_fraction': maxu,
        'mean_hidden_layer_coverage_ratio': cov,
        'max_residual_uncovered_fraction': maxr,
        'mean_hidden_boundary_discontinuity': float(np.mean(bmean)) if bmean else 0.0,
        'max_hidden_boundary_discontinuity_q95': max(b95, default=0.0),
        'worst_residual': worst,
        'surface_summaries': summaries[:64],
        'persistent_surface_count': 1,
        'per_frame_synthesis': False,
        'exact_final_source_relock': True,
        'coverage_gate': bool(maxu > .001 and cov >= .96 and maxr <= .003),
        'visual_gate': 'PENDING_HUMAN_REVIEW',
        'decision_rule': 'if characteristic holes/stretching persist, topology-only is falsified; next test joint hidden color+depth completion'
    }
    a.report.write_text(json.dumps(rep, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
