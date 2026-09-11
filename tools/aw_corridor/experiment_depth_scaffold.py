#!/usr/bin/env python3
"""Build the first non-planar AW-011 world scaffold from monocular depth.

This is an experimental scaffold provider, not a final film renderer. It translates
one Doré authority image into a camera-consumable depth field, then measures
whether the representation contains enough depth separation to proceed to
geometric traversal work. Known source RGB remains untouched.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image
from transformers import pipeline


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--model", default="depth-anything/Depth-Anything-V2-Small-hf")
    args = ap.parse_args()

    source = Image.open(args.source).convert("RGB")
    estimator = pipeline(task="depth-estimation", model=args.model, device=-1)
    result = estimator(source)
    depth = result["depth"]
    if not isinstance(depth, Image.Image):
        depth = Image.fromarray(np.asarray(depth))
    depth = depth.resize(source.size, Image.Resampling.BICUBIC).convert("L")
    arr = np.asarray(depth, dtype=np.float32) / 255.0

    # Quantiles are deliberately reported: a useful corridor scaffold must not
    # collapse to a single plane. This gate measures representation, not beauty.
    q05, q25, q50, q75, q95 = [float(x) for x in np.quantile(arr, [0.05, 0.25, 0.50, 0.75, 0.95])]
    spread = q95 - q05
    std = float(arr.std())
    nonplanar = spread >= 0.10 and std >= 0.03

    args.output.parent.mkdir(parents=True, exist_ok=True)
    depth.save(args.output)
    report = {
        "status": "DEPTH_SCAFFOLD_ACCEPTED" if nonplanar else "DEPTH_SCAFFOLD_TOO_FLAT",
        "provider": "depth-anything-v2-small",
        "model": args.model,
        "source_size": list(source.size),
        "depth_size": list(depth.size),
        "quantiles": {"q05": q05, "q25": q25, "q50": q50, "q75": q75, "q95": q95},
        "q95_q05_spread": spread,
        "standard_deviation": std,
        "nonplanar_gate": nonplanar,
        "authority_rule": "source_rgb_unchanged_depth_is_geometry_evidence_only"
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if nonplanar else 2


if __name__ == "__main__":
    raise SystemExit(main())
