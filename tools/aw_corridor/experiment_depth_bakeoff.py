#!/usr/bin/env python3
"""V5 geometry-provider bake-off for AW-011.

Runs independent monocular geometry providers against the same Doré authority
image and emits normalized 8-bit depth maps plus edge diagnostics. The V4
renderer remains unchanged so visual differences come from geometry evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def normalize_depth(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float32)
    finite = np.isfinite(a)
    if not np.any(finite):
        raise ValueError("provider returned no finite depth")
    lo, hi = np.quantile(a[finite], [0.02, 0.98])
    n = np.clip((a - lo) / max(float(hi - lo), 1e-6), 0.0, 1.0)
    return (n * 255.0).astype(np.uint8)


def diagnostics(depth8: np.ndarray) -> dict:
    d = depth8.astype(np.float32) / 255.0
    gx = cv2.Sobel(d, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(d, cv2.CV_32F, 0, 1, ksize=3)
    g = np.sqrt(gx * gx + gy * gy)
    q05, q50, q95 = [float(x) for x in np.quantile(d, [0.05, 0.50, 0.95])]
    return {
        "q05": q05, "q50": q50, "q95": q95,
        "q95_q05_spread": q95 - q05,
        "standard_deviation": float(d.std()),
        "edge_gradient_mean": float(g.mean()),
        "edge_gradient_q95": float(np.quantile(g, 0.95)),
    }


def depth_anything(source: Image.Image, model: str) -> np.ndarray:
    from transformers import pipeline
    est = pipeline(task="depth-estimation", model=model, device=-1)
    r = est(source)
    x = r.get("predicted_depth", r.get("depth"))
    if isinstance(x, Image.Image):
        x = np.asarray(x)
    elif hasattr(x, "detach"):
        x = x.detach().cpu().numpy().squeeze()
    return np.asarray(x)


def depth_pro(source_path: Path) -> np.ndarray:
    import torch
    import depth_pro
    model, transform = depth_pro.create_model_and_transforms()
    model.eval()
    image, _, f_px = depth_pro.load_rgb(str(source_path))
    image = transform(image)
    with torch.no_grad():
        prediction = model.infer(image, f_px=f_px)
    # Metric depth: invert so larger normalized value remains nearer, matching V4.
    d = prediction["depth"].detach().cpu().numpy().squeeze().astype(np.float32)
    return 1.0 / np.maximum(d, 1e-6)


def moge(source_path: Path) -> np.ndarray:
    import torch
    from moge.model.v2 import MoGeModel
    model = MoGeModel.from_pretrained("Ruicheng/moge-2-vitl-normal").eval()
    image = cv2.cvtColor(cv2.imread(str(source_path)), cv2.COLOR_BGR2RGB)
    image = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
    with torch.no_grad():
        out = model.infer(image)
    d = out["depth"].detach().cpu().numpy().squeeze().astype(np.float32)
    return 1.0 / np.maximum(d, 1e-6)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--provider", choices=["depth-anything", "depth-pro", "moge"], required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--model", default="depth-anything/Depth-Anything-V2-Small-hf")
    args = ap.parse_args()
    source = Image.open(args.source).convert("RGB")
    if args.provider == "depth-anything":
        raw = depth_anything(source, args.model)
    elif args.provider == "depth-pro":
        raw = depth_pro(args.source)
    else:
        raw = moge(args.source)
    raw = cv2.resize(np.asarray(raw, dtype=np.float32), source.size, interpolation=cv2.INTER_CUBIC)
    depth8 = normalize_depth(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.output), depth8)
    report = {"status":"DEPTH_PROVIDER_ACCEPTED", "provider":args.provider,
              "source_size":list(source.size), "depth_size":list(source.size),
              "authority_rule":"source_rgb_unchanged_depth_is_geometry_evidence_only",
              **diagnostics(depth8)}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
