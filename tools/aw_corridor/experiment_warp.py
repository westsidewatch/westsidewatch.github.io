#!/usr/bin/env python3
"""Generate a first real AW-011 planar reprojection mask pass.

This is deliberately a light experiment provider, not the final scaffold model. It
uses the actual source dimensions and Camera Spine translation to compute which
pixels remain source-visible after a planar camera shift and which pixels become
unseen/disoccluded. The output is consumed by mask_evidence.py unchanged.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
import zlib
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"


def jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise ValueError(f"not a JPEG: {path}")
    i = 2
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in (0xD8, 0xD9):
            continue
        if i + 2 > len(data):
            break
        seg_len = int.from_bytes(data[i:i+2], "big")
        if seg_len < 2 or i + seg_len > len(data):
            raise ValueError("invalid JPEG segment")
        if marker in {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}:
            if seg_len < 7:
                raise ValueError("invalid JPEG SOF")
            h = int.from_bytes(data[i+3:i+5], "big")
            w = int.from_bytes(data[i+5:i+7], "big")
            return w, h
        i += seg_len
    raise ValueError("JPEG dimensions not found")


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def write_gray_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    if len(pixels) != width * height:
        raise ValueError("pixel length mismatch")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = b"".join(b"\x00" + pixels[y*width:(y+1)*width] for y in range(height))
    payload = (
        PNG_SIG
        + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
        + png_chunk(b"IDAT", zlib.compress(raw, 9))
        + png_chunk(b"IEND", b"")
    )
    path.write_bytes(payload)


def build_masks(source: Path, spine: Path, out_root: Path, manifest_out: Path, pixels_per_world_unit: float) -> dict:
    width, height = jpeg_size(source)
    camera = json.loads(spine.read_text(encoding="utf-8"))
    poses = camera.get("poses")
    if not isinstance(poses, list) or len(poses) < 3:
        raise ValueError("camera spine requires departure/travel/return")
    canonical = poses[0]
    cpos = canonical.get("position")
    if not isinstance(cpos, list) or len(cpos) != 3:
        raise ValueError("canonical position missing")

    manifest = {"max_residual_unseen_fraction": 0.01, "poses": [], "candidates": []}
    reports = []
    for pose in poses[1:-1]:
        pose_id = str(pose.get("id", ""))
        pos = pose.get("position")
        if not pose_id or not isinstance(pos, list) or len(pos) != 3:
            raise ValueError("travel pose missing id/position")

        dx = int(round((float(pos[0]) - float(cpos[0])) * pixels_per_world_unit))
        dy = int(round((float(pos[1]) - float(cpos[1])) * pixels_per_world_unit))
        dx = max(-(width - 1), min(width - 1, dx))
        dy = max(-(height - 1), min(height - 1, dy))

        unseen = bytearray(width * height)
        known = bytearray(width * height)
        unseen_count = 0
        for y in range(height):
            sy = y - dy
            row = y * width
            for x in range(width):
                sx = x - dx
                idx = row + x
                is_known = 0 <= sx < width and 0 <= sy < height
                if is_known:
                    known[idx] = 255
                else:
                    unseen[idx] = 255
                    unseen_count += 1

        pose_dir = out_root / "poses" / pose_id
        unseen_path = pose_dir / "unseen-mask.png"
        known_path = pose_dir / "known-mask.png"
        write_gray_png(unseen_path, width, height, bytes(unseen))
        write_gray_png(known_path, width, height, bytes(known))
        rel_unseen = unseen_path.relative_to(manifest_out.parent).as_posix()
        manifest["poses"].append({"id": pose_id, "weight": 1.0, "unseen_mask": rel_unseen})
        reports.append({
            "id": pose_id,
            "dx_pixels": dx,
            "dy_pixels": dy,
            "unseen_pixels": unseen_count,
            "unseen_fraction": unseen_count / (width * height),
        })

    manifest_out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"source_size": [width, height], "poses": reports, "mask_manifest": str(manifest_out)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--spine", type=Path, required=True)
    ap.add_argument("--out-root", type=Path, required=True)
    ap.add_argument("--manifest-out", type=Path, required=True)
    ap.add_argument("--pixels-per-world-unit", type=float, default=420.0)
    args = ap.parse_args()
    report = build_masks(args.source, args.spine, args.out_root, args.manifest_out, args.pixels_per_world_unit)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
