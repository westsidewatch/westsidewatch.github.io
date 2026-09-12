#!/usr/bin/env python3
"""AW-011: edge-aware persistent hidden-surface experiment.

Question under test
-------------------
The previous depth-banded cache knew *where* hidden world was demanded and kept
an estimated depth, but it still collapsed that support into generic layers.
This experiment isolates one hypothesis: the large white/gray holes and stretched
surfaces are primarily caused by lost occlusion topology.

Everything upstream stays fixed: Camera Spine, MoGe depth, trajectory sampling,
world-demand discovery, and inverse projection. Only the hidden-world
representation changes.

For each depth discontinuity we:
  1. identify a local occlusion zone;
  2. classify foreground/background sides from the local depth jump;
  3. keep hidden support on the background side of that topology;
  4. sever triangle connectivity across strong depth jumps;
  5. complete colour with foreground context masked out;
  6. persist the resulting support for the whole camera path.

This is deliberately *not* a diffusion/generative completion test. If topology
alone does not remove the characteristic failure, the next experiment should
move to joint hidden colour+depth completion rather than another representation
swap.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_world_cache import raster_layer


def occlusion_topology(dep: np.ndarray, support: np.ndarray, edge_q: float = .90,
                       edge_floor: float = .025, min_jump: float = .055,
                       zone_radius: int = 31):
    """Return strong depth edges and foreground/background side hypotheses."""
    gx = cv2.Sobel(dep, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(dep, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.magnitude(gx, gy)
    nz = grad[grad > 0]
    qthr = float(np.quantile(nz, edge_q)) if nz.size else 0.0
    threshold = max(edge_floor, qthr)

    # Local min/max provide a representation-agnostic estimate of which side
    # of an edge is farther/nearer. In the AW-011 depth convention, larger
    # values are nearer and win the front z-buffer.
    k9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    local_min = cv2.erode(dep, k9)
    local_max = cv2.dilate(dep, k9)
    jump = local_max - local_min
    edge = ((grad >= threshold) & (jump >= min_jump)).astype(np.uint8) * 255

    # Connect each demanded hidden patch to the nearest meaningful occlusion
    # structure, but do not turn the whole image into an edge zone.
    zrad = max(5, int(zone_radius))
    zk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * zrad + 1, 2 * zrad + 1))
    zone = cv2.dilate(edge, zk)
    relevant = cv2.bitwise_and(zone, support)

    # Side classification is intentionally conservative. Pixels close to the
    # lower part of the local depth span are background evidence; pixels close
    # to the upper part are foreground evidence. Ambiguous middle pixels remain
    # unlabeled rather than being forced into either side.
    span = np.maximum(jump, 1e-6)
    rel = (dep - local_min) / span
    background = ((zone > 0) & (rel <= .35)).astype(np.uint8) * 255
    foreground = ((zone > 0) & (rel >= .65)).astype(np.uint8) * 255

    # Build component IDs over connected occlusion zones. A component is the
    # persistent edge_id carried by hidden support in this experiment.
    ncomp, labels = cv2.connectedComponents((zone > 0).astype(np.uint8), 8)
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


def build_edge_aware_cache(src: np.ndarray, dep: np.ndarray, support: np.ndarray,
                           zmap: np.ndarray, topo: dict, behind_margin: float = .025,
                           context_radius: int = 19):
    """Build persistent hidden surfaces keyed by occlusion component/edge_id."""
    labels = topo['labels']
    relevant = topo['relevant_support'] > 0
    background = topo['background'] > 0
    foreground = topo['foreground'] > 0
    local_min = topo['local_min']
    layers = []
    unresolved = (support > 0) & (~relevant)

    ids = np.unique(labels[relevant])
    ids = ids[ids > 0]
    for edge_id in ids.tolist():
        zone = labels == edge_id
        demanded = relevant & zone
        if np.count_nonzero(demanded) < 24:
            unresolved |= demanded
            continue

        # Keep the demanded hidden surface behind the background side of this
        # particular occlusion relation.  This is the key change from generic
        # depth bands: depth is conditioned on edge topology, not a global bin.
        hidden_z = zmap.copy()
        target_back = np.clip(local_min - behind_margin, 0.0, 1.0)
        have_z = hidden_z > 0
        hidden_z[demanded & have_z] = np.minimum(hidden_z[demanded & have_z], target_back[demanded & have_z])
        hidden_z[demanded & (~have_z)] = target_back[demanded & (~have_z)]

        # Expand only enough for triangle support and texture continuation.
        support_mask = demanded.astype(np.uint8) * 255
        support_mask = cv2.dilate(support_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        support_bool = support_mask > 0

        # Exclude the foreground side from colour evidence. Inpainting across a
        # mask containing the nearby foreground forces continuation from the
        # remaining/background context instead of smearing the occluder into
        # the newly exposed surface.
        near = cv2.dilate(support_mask, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (2 * context_radius + 1, 2 * context_radius + 1))) > 0
        completion = support_bool | (foreground & zone & near)
        completion_mask = completion.astype(np.uint8) * 255
        rgb = cv2.inpaint(src, completion_mask, 7.0, cv2.INPAINT_TELEA)

        # Use the original depth field as the carrier outside the hidden patch;
        # replace only the demanded support. This prevents zero-depth canvas
        # regions from participating in triangle construction.
        depth = dep.copy()
        dmiss = support_bool & (hidden_z <= 0)
        if np.any(dmiss):
            tmp = hidden_z.copy()
            tmp = cv2.inpaint(tmp, dmiss.astype(np.uint8) * 255, 3.0, cv2.INPAINT_TELEA)
            hidden_z[dmiss] = tmp[dmiss]
        depth[support_bool] = np.where(hidden_z[support_bool] > 0,
                                       hidden_z[support_bool],
                                       target_back[support_bool])
        depth = np.clip(depth, 0, 1).astype(np.float32)

        bg_evidence = int(np.count_nonzero(background & zone & near))
        layers.append({
            'edge_id': int(edge_id),
            'rgb': rgb,
            'depth': depth,
            'mask': support_mask,
            'support_pixels': int(np.count_nonzero(support_bool)),
            'background_evidence_pixels': bg_evidence,
            'median_hidden_depth': float(np.median(depth[support_bool])) if np.any(support_bool) else 0.0,
        })

    return layers, unresolved.astype(np.uint8) * 255


def raster_support(mask, depth, p, ppu, step=6, edge_threshold=.065):
    rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    warped, known = raster_layer(rgb, depth, p, ppu, step, edge_threshold)
    return (known > 0) & (warped[:, :, 0] > 96)


def render(src, dep, layers, p, ppu=520.0, sever_threshold=.065):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)

    # Render deeper hidden surfaces first. Their edge_id/topology is persistent
    # over the whole camera path; there is no per-frame synthesis.
    order = sorted(range(len(layers)), key=lambda i: layers[i]['median_hidden_depth'])
    for i in order:
        layer = layers[i]
        img, known = raster_layer(layer['rgb'], layer['depth'], p, ppu, 6, sever_threshold)
        visible = raster_support(layer['mask'], layer['depth'], p, ppu, 6, sever_threshold)
        take = (known > 0) & visible
        frame[take] = img[take]
        occupied[take] = 255

    front, front_known = raster_layer(src, dep, p, ppu, 6, .10)
    front_take = front_known > 0
    frame[front_take] = front[front_take]

    residual = (front_known == 0) & (occupied == 0)
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
    ap.add_argument('--segment-frames', type=int, default=24)
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
    layers, unresolved = build_edge_aware_cache(src, dep, support, zmap, topo)

    for path, image in ((a.support_map, support), (a.edge_map, topo['edge']),
                        (a.background_map, topo['background']),
                        (a.unresolved_map, unresolved)):
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
            frame, u, c, r, fk, occ = render(src, dep, layers, p, a.ppu, a.sever_threshold)
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
    relf = float(np.count_nonzero(topo['relevant_support']) / max(1, np.count_nonzero(support)))
    unresolved_fraction = float(np.count_nonzero(unresolved) / max(1, np.count_nonzero(support)))
    rep = {
        'status': 'EDGE_AWARE_HIDDEN_SURFACE_READY_FOR_VISUAL_REVIEW',
        'mode': 'camera_conditioned_occlusion_topology_persistent_hidden_surface',
        'hypothesis': 'large visual defects are caused primarily by lost foreground/background occlusion topology',
        'trajectory_samples_used': used,
        'mapped_support_samples': mapped,
        'mean_inverse_projection_error_pixels': inv_err,
        'support_fraction': sf,
        'occlusion_component_count': topo['component_count'],
        'persistent_hidden_surface_count': len(layers),
        'edge_gradient_threshold': topo['threshold'],
        'minimum_depth_jump': a.min_jump,
        'zone_radius_pixels': a.zone_radius,
        'triangle_sever_threshold': a.sever_threshold,
        'support_attached_to_occlusion_topology_ratio': relf,
        'unresolved_support_ratio': unresolved_fraction,
        'max_foreground_unseen_fraction': maxu,
        'mean_hidden_layer_coverage_ratio': cov,
        'max_residual_uncovered_fraction': maxr,
        'mean_hidden_boundary_discontinuity': float(np.mean(bmean)) if bmean else 0.0,
        'max_hidden_boundary_discontinuity_q95': max(b95, default=0.0),
        'worst_residual': worst,
        'surface_summaries': [{
            'edge_id': x['edge_id'],
            'support_pixels': x['support_pixels'],
            'background_evidence_pixels': x['background_evidence_pixels'],
            'median_hidden_depth': x['median_hidden_depth'],
        } for x in layers[:64]],
        'exact_final_source_relock': True,
        'coverage_gate': bool(maxu > .001 and cov >= .96 and maxr <= .003),
        'visual_gate': 'PENDING_HUMAN_REVIEW',
        'decision_rule': 'if characteristic holes/stretching persist, reject topology-only representation and move to joint hidden color+depth completion'
    }
    a.report.write_text(json.dumps(rep, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
