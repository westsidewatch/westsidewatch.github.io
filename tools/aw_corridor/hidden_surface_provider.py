#!/usr/bin/env python3
"""Hidden-world completion providers for AW-011.

The learned adapter intentionally imports only the three inference networks from
3D Photo Inpainting's ``networks.py`` and three state-dict checkpoints. It does
not depend on the legacy mesh/viewer/MiDaS pipeline or its Python 3.7 runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class HiddenSurfaceResult:
    rgb: np.ndarray
    depth: np.ndarray
    mask: np.ndarray
    edge: np.ndarray
    provider: str


def hidden_completion_mask(support: np.ndarray, topo: dict) -> np.ndarray:
    mask = cv2.dilate(
        support,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)),
        iterations=1,
    )
    foreground = topo['foreground'] > 0
    near = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))) > 0
    return ((mask > 0) | (foreground & near)).astype(np.uint8)


def classical_complete(src, dep, support, zmap, topo, behind_margin=.025):
    """V5-compatible deterministic fallback, kept as an explicit provider."""
    demanded = support > 0
    if not np.any(demanded):
        return HiddenSurfaceResult(src.copy(), dep.copy(), support.copy(), topo['edge'].copy(), 'classical')

    mask = cv2.dilate(support, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)), iterations=1)
    m = mask > 0
    local_min = topo['local_min']
    target_back = np.clip(local_min - behind_margin, 0.0, 1.0).astype(np.float32)
    hidden = np.zeros_like(dep, np.float32)
    have = (zmap > 0) & m
    hidden[have] = np.minimum(zmap[have], target_back[have])
    hidden[m & (~have)] = target_back[m & (~have)]
    smooth = cv2.bilateralFilter(hidden.copy(), 9, 0.06, 9.0)
    hidden[m] = np.minimum(smooth[m], target_back[m])
    hidden = np.clip(hidden, 0.0, 1.0)

    completion = hidden_completion_mask(support, topo)
    rgb = cv2.inpaint(src, completion * 255, 7.0, cv2.INPAINT_TELEA)
    hdep = dep.copy().astype(np.float32)
    hdep[m] = hidden[m]
    return HiddenSurfaceResult(rgb, hdep, mask, topo['edge'].copy(), 'classical')


def _load_networks(path: Path):
    spec = importlib.util.spec_from_file_location('dore_3dphoto_networks', path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'cannot import network definitions from {path}')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tensor(torch, array, device, channels=False):
    t = torch.from_numpy(np.ascontiguousarray(array)).float().to(device)
    if channels:
        return t.permute(2, 0, 1).unsqueeze(0)
    return t.unsqueeze(0).unsqueeze(0)


def _load_three_stage_models(torch, networks_path, edge_checkpoint, depth_checkpoint, color_checkpoint, device):
    mod = _load_networks(networks_path)
    edge_model = mod.Inpaint_Edge_Net(init_weights=True)
    depth_model = mod.Inpaint_Depth_Net()
    color_model = mod.Inpaint_Color_Net()
    map_location = torch.device(device)
    edge_model.load_state_dict(torch.load(edge_checkpoint, map_location=map_location, weights_only=True))
    depth_model.load_state_dict(torch.load(depth_checkpoint, map_location=map_location, weights_only=True), strict=True)
    color_model.load_state_dict(torch.load(color_checkpoint, map_location=map_location, weights_only=True))
    edge_model.to(device).eval(); depth_model.to(device).eval(); color_model.to(device).eval()
    return edge_model, depth_model, color_model


def _three_stage_infer(torch, edge_model, depth_model, color_model, rgb, depth, hole, known_edge, device, edge_threshold=.002):
    context = 1.0 - hole
    input_rgb = rgb * context[..., None]
    safe_depth = np.clip(depth.astype(np.float32), 1e-6, 1.0)
    log_safe = np.log(safe_depth)
    mean_log = float(np.mean(log_safe[context > .5])) if np.any(context > .5) else 0.0
    zero_mean_depth = (log_safe - mean_log) * context
    disp = (1.0 / safe_depth) * context
    dmax = float(disp.max())
    if dmax > 0: disp /= dmax

    t_mask = _tensor(torch, hole, device)
    t_context = _tensor(torch, context, device)
    t_rgb = _tensor(torch, input_rgb, device, channels=True)
    t_disp = _tensor(torch, disp, device)
    t_edge = _tensor(torch, known_edge * context, device)
    t_zero = _tensor(torch, zero_mean_depth, device)
    with torch.inference_mode():
        edge_raw = edge_model.forward_3P(t_mask, t_context, t_rgb, t_disp, t_edge, unit_length=128, cuda=device)
        learned_edge = (edge_raw > edge_threshold).float() * t_mask + t_edge
        depth_raw = depth_model.forward_3P(t_mask, t_context, t_zero, learned_edge, unit_length=128, cuda=device)
        color_raw = color_model.forward_3P(t_mask, t_context, t_rgb, learned_edge, unit_length=128, cuda=device)

    predicted_depth = np.exp(depth_raw.squeeze().cpu().numpy() + mean_log).astype(np.float32)
    predicted_rgb = np.clip(color_raw.squeeze(0).permute(1, 2, 0).cpu().numpy(), 0.0, 1.0)
    edge_np = (learned_edge.squeeze().cpu().numpy() > .5).astype(np.uint8) * 255
    return predicted_rgb, predicted_depth, edge_np


def learned_three_stage_complete(
    src,
    dep,
    support,
    zmap,
    topo,
    networks_path: Path,
    edge_checkpoint: Path,
    depth_checkpoint: Path,
    color_checkpoint: Path,
    device='cpu',
    behind_margin=.025,
    edge_threshold=.002,
):
    """EdgeModel -> DepthModel -> ColorModel completion in canonical world space.

    Visible Doré pixels are never admitted from model output. Network depth is
    also constrained behind the owning visible surface before rasterization.
    """
    import torch

    base = classical_complete(src, dep, support, zmap, topo, behind_margin)
    mask = base.mask > 0
    if not np.any(mask):
        return HiddenSurfaceResult(base.rgb, base.depth, base.mask, base.edge, 'three-stage-empty')

    edge_model, depth_model, color_model = _load_three_stage_models(
        torch, networks_path, edge_checkpoint, depth_checkpoint, color_checkpoint, device
    )
    rgb = src.astype(np.float32) / 255.0
    known_edge = topo['edge'].astype(np.float32) / 255.0
    predicted_rgb, predicted_depth, edge_np = _three_stage_infer(
        torch, edge_model, depth_model, color_model, rgb, dep, mask.astype(np.float32), known_edge, device, edge_threshold
    )

    # Geometry remains authoritative: learned content may fill a hidden surface,
    # but cannot move it in front of the local occluder/background constraint.
    target_back = np.clip(topo['local_min'] - behind_margin, 0.0, 1.0).astype(np.float32)
    out_depth = dep.copy().astype(np.float32)
    candidate_depth = np.minimum(np.clip(predicted_depth, 0.0, 1.0), target_back)
    finite = np.isfinite(candidate_depth) & (candidate_depth > 0)
    accepted = mask & finite
    out_depth[accepted] = candidate_depth[accepted]
    out_depth[mask & (~finite)] = base.depth[mask & (~finite)]

    out_rgb = src.copy()
    learned_u8 = np.uint8(np.round(predicted_rgb * 255.0))
    out_rgb[mask] = learned_u8[mask]
    # Source-authority invariant: only canonical hidden support may change.
    out_rgb[~mask] = src[~mask]
    out_depth[~mask] = dep[~mask]
    return HiddenSurfaceResult(out_rgb, out_depth, base.mask, edge_np, '3d-photo-edge-depth-color')


def learned_three_stage_extend_canvas(
    src,
    dep,
    pad,
    networks_path: Path,
    edge_checkpoint: Path,
    depth_checkpoint: Path,
    color_checkpoint: Path,
    device='cpu',
    behind_margin=.025,
    edge_threshold=.002,
    seam_pixels=8,
):
    """Create one persistent learned world outside the original image rectangle.

    The center rectangle is immutable source authority. Only the padded border is
    unknown/model-owned. This is world completion, not per-frame synthesis.
    """
    import torch

    h, w = dep.shape
    ph, pw = h + 2 * pad, w + 2 * pad
    hole = np.ones((ph, pw), np.float32)
    hole[pad:pad+h, pad:pad+w] = 0.0

    # The model sees the real artwork only in the canonical center. RGB outside
    # starts empty; replicated depth is geometry context, never accepted as art.
    rgb = np.zeros((ph, pw, 3), np.float32)
    rgb[pad:pad+h, pad:pad+w] = src.astype(np.float32) / 255.0
    depth_ref = cv2.copyMakeBorder(dep.astype(np.float32), pad, pad, pad, pad, cv2.BORDER_REPLICATE)

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    source_edge = cv2.Canny(gray, 60, 140).astype(np.float32) / 255.0
    known_edge = np.zeros((ph, pw), np.float32)
    known_edge[pad:pad+h, pad:pad+w] = source_edge

    edge_model, depth_model, color_model = _load_three_stage_models(
        torch, networks_path, edge_checkpoint, depth_checkpoint, color_checkpoint, device
    )
    predicted_rgb, predicted_depth, edge_np = _three_stage_infer(
        torch, edge_model, depth_model, color_model, rgb, depth_ref, hole, known_edge, device, edge_threshold
    )

    model_u8 = np.uint8(np.round(predicted_rgb * 255.0))
    out_rgb = model_u8.copy()
    out_rgb[pad:pad+h, pad:pad+w] = src

    # Keep the learned border behind the nearest canonical boundary geometry.
    target_back = np.clip(depth_ref - behind_margin, 0.0, 1.0)
    candidate_depth = np.minimum(np.clip(predicted_depth, 0.0, 1.0), target_back)
    finite = np.isfinite(candidate_depth) & (candidate_depth > 0)
    out_depth = target_back.copy()
    border = hole > .5
    out_depth[border & finite] = candidate_depth[border & finite]
    out_depth[pad:pad+h, pad:pad+w] = dep

    # Narrow seam admission: the model remains primary. A small alpha ramp at
    # the four source boundaries suppresses a hard chromatic cut without turning
    # the border back into a reflected/stretched world.
    seam_pixels = max(0, int(seam_pixels))
    if seam_pixels:
        nearest = cv2.copyMakeBorder(src, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
        yy, xx = np.indices((ph, pw))
        dx = np.maximum(np.maximum(pad - xx, xx - (pad + w - 1)), 0)
        dy = np.maximum(np.maximum(pad - yy, yy - (pad + h - 1)), 0)
        dist = np.maximum(dx, dy).astype(np.float32)
        band = border & (dist <= seam_pixels)
        alpha = np.clip(dist / float(seam_pixels), 0.0, 1.0)[..., None]
        blended = np.uint8(np.round(nearest.astype(np.float32) * (1.0 - alpha) + out_rgb.astype(np.float32) * alpha))
        out_rgb[band] = blended[band]

    mask = (border.astype(np.uint8) * 255)
    return HiddenSurfaceResult(out_rgb, out_depth.astype(np.float32), mask, edge_np, '3d-photo-learned-extended-world')
