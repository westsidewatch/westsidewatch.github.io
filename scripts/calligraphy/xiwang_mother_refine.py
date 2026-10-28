#!/usr/bin/env python3
"""Experimental Xi Wang plaque-wordmark optical revision, based on user-approved mother.
No image generation or third-party calligraphy imitation. Original bitmap remains immutable.

Usage:
  python scripts/calligraphy/xiwang_mother_refine.py mother.png --output output-dir
Requires: pillow, numpy, opencv-python
Candidate only: does NOT replace the protected Westside Watch / P2 SVG.
"""
import argparse
from pathlib import Path
import cv2
import numpy as np
from PIL import Image


def revise(source: Path, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    color = np.asarray(Image.open(source).convert("RGB"), dtype=np.float32)
    h, w = color.shape[:2]
    y, x = np.mgrid[:h, :w].astype(np.float32)
    # Measurements are locked to the approved 1024x1536 mother.
    if (w, h) != (1024, 1536):
        raise ValueError("This localized optical revision requires the exact 1024x1536 mother image")

    # Widen the central counters in 西 only, while leaving the main upper beam in place.
    xi_spread = 0.065 * np.exp(-(((y - 490) / 180)**4 + ((x - 525) / 350)**4))
    mapx = (x - (x - 525) * xi_spread).astype(np.float32)
    # Lift 望's middle optical weight, preserving the heavy final baseline.
    shift = 10.0 * np.exp(-(((x - 525) / 265)**2 + ((y - 1025) / 190)**2) * 1.35)
    mapy = (y + shift).astype(np.float32)
    color = cv2.remap(color, mapx, mapy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    value = .2126 * color[:, :, 0] + .7152 * color[:, :, 1] + .0722 * color[:, :, 2]
    ink = np.clip((253.7 - value) / 249.7, 0, 1).astype(np.float32)

    def ellipse(cx, cy, rx, ry):
        return np.exp(-(((x - cx) / rx)**2 + ((y - cy) / ry)**2) * 2.4).astype(np.float32)

    fine_erosion = cv2.erode(ink, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    local_clearance = np.clip(.50 * ellipse(520, 474, 244, 196)
                              + .46 * ellipse(500, 1030, 230, 240), 0, .50)
    ink = ink * (1 - local_clearance) + fine_erosion * local_clearance

    # Modest wet pigment density and <=1px edge hydration; preserve authentic flywhite.
    small_dilate = cv2.dilate(ink, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    ink = np.clip(ink + .20 * np.maximum(0, small_dilate - ink) * ink**.13, 0, 1)
    ink = np.clip(ink + .070 * ink * (1 - ink), 0, 1)
    for cx, cy, rx, ry, amp in ((565, 205, 230, 100, .027), (695, 558, 200, 125, .020),
                                (685, 860, 155, 125, .023), (750, 1365, 190, 90, .023)):
        ink = np.clip(ink + amp * ellipse(cx, cy, rx, ry) * ink * (1 - ink), 0, 1)

    lum = np.mean(color, axis=2)
    residual = lum - cv2.GaussianBlur(lum, (0, 0), 1.3)
    gray = np.clip(255 - ink * 251.5 + .20 * residual * ink, 0, 255).astype(np.uint8)
    Image.fromarray(np.stack([gray] * 3, axis=2), "RGB").save(
        folder / "xiwang-mother-v02-ink-wet-structure.png", optimize=True)
    rgba = np.empty((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = [10, 10, 10]
    rgba[:, :, 3] = (np.clip(ink, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(
        folder / "xiwang-mother-v02-transparent.png", optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mother", type=Path)
    parser.add_argument("--output", type=Path, default=Path("/tmp/xiwang-mother-v02"))
    args = parser.parse_args()
    revise(args.mother, args.output)
