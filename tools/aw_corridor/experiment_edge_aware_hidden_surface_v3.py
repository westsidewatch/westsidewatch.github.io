#!/usr/bin/env python3
"""AW-011 topology falsification v3.

Camera-conditioned edge-topology test with persistent boundary foundation.
The occlusion-association radius is derived from the actual Camera Spine.
Large radii are evaluated with a distance transform rather than a giant
morphological kernel so the experiment remains computationally tractable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_edge_aware_hidden_surface_v2 import build_surface, boundary_discontinuity
from experiment_world_cache import raster_layer, build_hidden_layer


def camera_lateral_budget(poses, ppu: float) -> tuple[float, int]:
    if not poses:
        return 0.0, 31
    p0 = np.asarray(poses[0]['position'], np.float32)
    shift = 0.0
    for pose in poses:
        p = np.asarray(pose['position'], np.float32)
        d = p - p0
        shift = max(shift, float(np.hypot(d[0], d[1]) * ppu))
    return shift, max(31, int(np.ceil(shift + 12.0)))


def fast_occlusion_topology(dep: np.ndarray, support: np.ndarray, edge_q: float,
                            edge_floor: float, min_jump: float, zone_radius: int):
    gx = cv2.Sobel(dep, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(dep, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.magnitude(gx, gy)
    nz = grad[grad > 0]
    qthr = float(np.quantile(nz, edge_q)) if nz.size else 0.0
    threshold = max(edge_floor, qthr)

    k9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    local_min = cv2.erode(dep, k9)
    local_max = cv2.dilate(dep, k9)
    jump = local_max - local_min
    edge = ((grad >= threshold) & (jump >= min_jump)).astype(np.uint8) * 255

    # Exact Euclidean association to the nearest edge avoids O(r^2) dilation.
    # distanceTransform measures distance to zero pixels, hence edge pixels are 0.
    inv_edge = np.where(edge > 0, 0, 255).astype(np.uint8)
    dist = cv2.distanceTransform(inv_edge, cv2.DIST_L2, 5)
    zone = (dist <= float(zone_radius)).astype(np.uint8) * 255
    relevant = cv2.bitwise_and(zone, support)

    span = np.maximum(jump, 1e-6)
    rel = (dep - local_min) / span
    background = ((zone > 0) & (rel <= .35)).astype(np.uint8) * 255
    foreground = ((zone > 0) & (rel >= .65)).astype(np.uint8) * 255

    # Component identity belongs to the actual edge graph, not the dilated zone.
    # Expand each component through the zone by nearest-edge assignment only where
    # needed by support. For this falsification build_surface only needs labels at
    # relevant support locations, so nearest connected edge ID is sufficient.
    ncomp, edge_labels = cv2.connectedComponents((edge > 0).astype(np.uint8), 8)
    labels = np.zeros_like(edge_labels)
    if ncomp > 1 and np.any(relevant):
        # Propagate edge IDs cheaply by iterative nearest-neighbour label dilation;
        # only support pixels are consumed downstream. 3x3 dilation converges in
        # zone_radius iterations and is substantially cheaper than a 281x281 kernel.
        labels = edge_labels.astype(np.int32)
        frontier = labels.copy()
        target = (zone > 0) & (labels == 0)
        kernel = np.ones((3, 3), np.uint8)
        for _ in range(int(zone_radius)):
            if not np.any(target & (relevant > 0)):
                break
            new_labels = labels.copy()
            # Propagate one component at a time only across still-unlabelled zone.
            # Component count is small for AW-011; this preserves edge identity.
            for cid in range(1, ncomp):
                m = (labels == cid).astype(np.uint8)
                if not np.any(m):
                    continue
                grown = cv2.dilate(m, kernel) > 0
                take = grown & (zone > 0) & (new_labels == 0)
                new_labels[take] = cid
            if np.array_equal(new_labels, labels):
                break
            labels = new_labels
            target = (zone > 0) & (labels == 0)

    return {
        'edge': edge,
        'zone': zone,
        'relevant_support': relevant,
        'background': background,
        'foreground': foreground,
        'labels': labels,
        'component_count': int(max(0, ncomp - 1)),
        'local_min': local_min,
        'local_max': local_max,
        'jump': jump,
        'threshold': threshold,
    }


def raster_support(mask, depth, p, ppu, sever_threshold=None):
    probe = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    warped, known = raster_layer(probe, depth, p, ppu, 6, sever_threshold)
    return (known > 0) & (warped[:, :, 0] > 96)


def render(src, dep, topo_rgb, topo_depth, topo_mask,
           base_rgb, base_depth, foundation_mask,
           p, ppu=520.0, sever_threshold=.065):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    bimg, bknown = raster_layer(base_rgb, base_depth, p, ppu, 6, None)
    bvis = raster_support(foundation_mask, base_depth, p, ppu, None)
    btake = (bknown > 0) & bvis
    frame[btake] = bimg[btake]
    occupied[btake] = 255

    himg, hknown = raster_layer(topo_rgb, topo_depth, p, ppu, 6, sever_threshold)
    hvis = raster_support(topo_mask, topo_depth, p, ppu, sever_threshold)
    htake = (hknown > 0) & hvis
    frame[htake] = himg[htake]
    occupied[htake] = 255

    front, front_known = raster_layer(src, dep, p, ppu, 6, .10)
    ft = front_known > 0
    frame[ft] = front[ft]

    residual = (front_known == 0) & (occupied == 0)
    frame[residual] = 0
    unseen = float(np.count_nonzero(front_known == 0) / front_known.size)
    res = float(np.count_nonzero(residual) / front_known.size)
    return (frame, unseen, max(0.0, unseen - res), res, front_known, occupied,
            int(np.count_nonzero(htake)), int(np.count_nonzero(btake)))


def main():
    ap = argparse.ArgumentParser()
    for k in ('source', 'depth', 'spine', 'output', 'report'):
        ap.add_argument('--' + k, type=Path, required=True)
    ap.add_argument('--support-map', type=Path)
    ap.add_argument('--edge-map', type=Path)
    ap.add_argument('--background-map', type=Path)
    ap.add_argument('--foundation-map', type=Path)
    ap.add_argument('--width', type=int, default=960)
    ap.add_argument('--fps', type=int, default=24)
    ap.add_argument('--segment-frames', type=int, default=12)
    ap.add_argument('--ppu', type=float, default=520.0)
    ap.add_argument('--samples', type=int, default=8)
    ap.add_argument('--behind', type=float, default=.08)
    ap.add_argument('--edge-q', type=float, default=.90)
    ap.add_argument('--min-jump', type=float, default=.055)
    ap.add_argument('--sever-threshold', type=float, default=.065)
    a = ap.parse_args()

    src, dep = prepare(a.source, a.depth, a.width)
    poses = load_pose_points(a.spine)
    lateral_shift, zone_radius = camera_lateral_budget(poses, a.ppu)

    support, zmap, used, mapped, inv_err = collect_depth_conditioned_support(
        dep, poses, a.ppu, a.samples, a.behind)
    topo = fast_occlusion_topology(dep, support, a.edge_q, .025, a.min_jump, zone_radius)
    topo_rgb, topo_depth, topo_mask, unresolved, summaries = build_surface(
        src, dep, support, zmap, topo)

    base_rgb, base_depth, _ = build_hidden_layer(src, dep)
    foundation_mask = cv2.dilate(
        unresolved, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))

    for path, image in ((a.support_map, support), (a.edge_map, topo['edge']),
                        (a.background_map, topo['background']),
                        (a.foundation_map, foundation_mask)):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(path), image)

    h, w = src.shape[:2]
    a.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(a.output), cv2.VideoWriter_fourcc(*'mp4v'), a.fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError('video writer failed')

    unseen, coverage, residual, bmean, b95 = [], [], [], [], []
    topo_contrib = foundation_contrib = 0
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
            frame, u, c, r, fk, occ, tc, bc = render(
                src, dep, topo_rgb, topo_depth, topo_mask,
                base_rgb, base_depth, foundation_mask, p, a.ppu, a.sever_threshold)
            bm, bp = boundary_discontinuity(frame, fk, occ)
            writer.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r); bmean.append(bm); b95.append(bp)
            topo_contrib += tc; foundation_contrib += bc
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
    foundation_ratio = float(np.count_nonzero(unresolved) / support_pixels)
    rep = {
        'status': 'CAMERA_CONDITIONED_EDGE_TOPOLOGY_READY_FOR_VISUAL_REVIEW',
        'mode': 'camera_conditioned_edge_topology_plus_persistent_boundary_foundation',
        'hypothesis': 'large internal defects are primarily caused by lost foreground/background occlusion topology',
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'support_fraction': float(np.count_nonzero(support) / support.size),
        'max_camera_lateral_shift_pixels': lateral_shift,
        'camera_conditioned_zone_radius_pixels': zone_radius,
        'occlusion_component_count': topo['component_count'],
        'edge_gradient_threshold': topo['threshold'],
        'minimum_depth_jump': a.min_jump,
        'triangle_sever_threshold': a.sever_threshold,
        'support_attached_to_occlusion_topology_ratio': attached,
        'foundation_support_ratio': foundation_ratio,
        'max_foreground_unseen_fraction': maxu,
        'mean_hidden_layer_coverage_ratio': cov,
        'max_residual_uncovered_fraction': maxr,
        'mean_hidden_boundary_discontinuity': float(np.mean(bmean)) if bmean else 0.0,
        'max_hidden_boundary_discontinuity_q95': max(b95, default=0.0),
        'topology_rendered_pixels_total': topo_contrib,
        'foundation_rendered_pixels_total': foundation_contrib,
        'worst_residual': worst,
        'surface_summaries': summaries[:64],
        'persistent_surface_count': 2,
        'per_frame_synthesis': False,
        'exact_final_source_relock': True,
        'coverage_gate': bool(maxu > .001 and cov >= .96 and maxr <= .003),
        'visual_gate': 'PENDING_HUMAN_REVIEW',
        'decision_rule': 'judge camel/rider and lower-left surface continuity; if defects persist after demand is fully assigned, move to joint hidden color+depth completion'
    }
    a.report.write_text(json.dumps(rep, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
