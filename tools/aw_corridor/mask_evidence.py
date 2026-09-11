#!/usr/bin/env python3
"""Build AW corridor planner evidence directly from strict binary PNG masks.

No imaging dependency is required. The PNG decoder intentionally supports only the
mask formats accepted by the production contract: 8-bit, non-interlaced grayscale,
RGB, grayscale+alpha, or RGBA PNG. Mask color samples must be binary 0/255.
Alpha is ignored; RGB channels must agree. This keeps mask semantics explicit.
"""
from __future__ import annotations

import argparse
import json
import struct
import zlib
from pathlib import Path
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class MaskError(ValueError):
    pass


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_binary_png(path: Path) -> tuple[int, int, list[bool]]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise MaskError(f"not a PNG mask: {path}")

    pos = len(PNG_SIGNATURE)
    width = height = bit_depth = color_type = interlace = None
    compressed = bytearray()
    saw_iend = False

    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        ctype = data[pos + 4 : pos + 8]
        payload = data[pos + 8 : pos + 8 + length]
        if pos + 12 + length > len(data):
            raise MaskError(f"truncated PNG chunk: {path}")
        pos += 12 + length

        if ctype == b"IHDR":
            if length != 13:
                raise MaskError("invalid IHDR")
            width, height, bit_depth, color_type, comp, filt, interlace = struct.unpack(
                ">IIBBBBB", payload
            )
            if comp != 0 or filt != 0:
                raise MaskError("unsupported PNG compression/filter method")
        elif ctype == b"IDAT":
            compressed.extend(payload)
        elif ctype == b"IEND":
            saw_iend = True
            break

    if None in (width, height, bit_depth, color_type, interlace) or not saw_iend:
        raise MaskError(f"incomplete PNG: {path}")
    if width <= 0 or height <= 0:
        raise MaskError("mask dimensions must be positive")
    if bit_depth != 8 or color_type not in (0, 2, 4, 6) or interlace != 0:
        raise MaskError(
            "mask PNG must be 8-bit non-interlaced grayscale/RGB/GA/RGBA"
        )

    channels = {0: 1, 2: 3, 4: 2, 6: 4}[color_type]
    raw = zlib.decompress(bytes(compressed))
    stride = width * channels
    expected = height * (stride + 1)
    if len(raw) != expected:
        raise MaskError(f"unexpected decompressed PNG size: {path}")

    rows: list[bytearray] = []
    offset = 0
    prev = bytearray(stride)
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        scan = bytearray(raw[offset : offset + stride])
        offset += stride
        recon = bytearray(stride)
        for i, value in enumerate(scan):
            left = recon[i - channels] if i >= channels else 0
            above = prev[i]
            upper_left = prev[i - channels] if i >= channels else 0
            if filter_type == 0:
                decoded = value
            elif filter_type == 1:
                decoded = (value + left) & 255
            elif filter_type == 2:
                decoded = (value + above) & 255
            elif filter_type == 3:
                decoded = (value + ((left + above) // 2)) & 255
            elif filter_type == 4:
                decoded = (value + _paeth(left, above, upper_left)) & 255
            else:
                raise MaskError(f"unsupported PNG filter {filter_type}: {path}")
            recon[i] = decoded
        rows.append(recon)
        prev = recon

    mask: list[bool] = []
    for row in rows:
        for x in range(width):
            pixel = row[x * channels : (x + 1) * channels]
            samples = [pixel[0]] if color_type in (0, 4) else list(pixel[:3])
            if len(set(samples)) != 1:
                raise MaskError(f"mask RGB channels disagree at pixel {x}: {path}")
            if samples[0] not in (0, 255):
                raise MaskError(
                    f"mask sample must be 0 or 255, got {samples[0]}: {path}"
                )
            mask.append(samples[0] == 255)

    return width, height, mask


def mask_cells(pose_id: str, width: int, mask: list[bool]) -> list[str]:
    return [
        f"{pose_id}:{index // width}:{index % width}"
        for index, enabled in enumerate(mask)
        if enabled
    ]


def _resolve(root: Path, value: Any, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise MaskError(f"{field} must be a non-empty path")
    path = Path(value)
    return path if path.is_absolute() else (root / path).resolve()


def build_problem(manifest_path: Path) -> dict[str, Any]:
    root = manifest_path.parent.resolve()
    obj = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise MaskError("mask manifest root must be an object")

    poses_raw = obj.get("poses")
    candidates_raw = obj.get("candidates", [])
    if not isinstance(poses_raw, list) or not poses_raw:
        raise MaskError("poses must be a non-empty list")
    if not isinstance(candidates_raw, list):
        raise MaskError("candidates must be a list")

    pose_dims: dict[str, tuple[int, int]] = {}
    pose_unseen: dict[str, set[str]] = {}
    poses = []

    for raw in poses_raw:
        if not isinstance(raw, dict):
            raise MaskError("each pose must be an object")
        pose_id = str(raw.get("id", "")).strip()
        if not pose_id or pose_id in pose_dims:
            raise MaskError(f"invalid or duplicate pose id: {pose_id}")
        path = _resolve(
            root, raw.get("unseen_mask"), f"poses[{pose_id}].unseen_mask"
        )
        width, height, mask = read_binary_png(path)
        cells = set(mask_cells(pose_id, width, mask))
        pose_dims[pose_id] = (width, height)
        pose_unseen[pose_id] = cells
        poses.append(
            {
                "id": pose_id,
                "weight": float(raw.get("weight", 1.0)),
                "unseen": sorted(cells),
            }
        )

    candidates = []
    seen_candidates: set[str] = set()
    for raw in candidates_raw:
        if not isinstance(raw, dict):
            raise MaskError("each candidate must be an object")
        candidate_id = str(raw.get("id", "")).strip()
        if not candidate_id or candidate_id in seen_candidates:
            raise MaskError(f"invalid or duplicate candidate id: {candidate_id}")
        seen_candidates.add(candidate_id)

        coverage_raw = raw.get("coverage_masks", {})
        if not isinstance(coverage_raw, dict):
            raise MaskError(f"coverage_masks must be an object: {candidate_id}")

        covers: dict[str, list[str]] = {}
        for pose_id, value in coverage_raw.items():
            pose_id = str(pose_id)
            if pose_id not in pose_dims:
                raise MaskError(
                    f"candidate {candidate_id} references unknown pose {pose_id}"
                )
            path = _resolve(
                root,
                value,
                f"candidates[{candidate_id}].coverage_masks[{pose_id}]",
            )
            width, height, mask = read_binary_png(path)
            if (width, height) != pose_dims[pose_id]:
                raise MaskError(
                    f"mask dimensions differ for {candidate_id}/{pose_id}: "
                    f"{(width, height)} != {pose_dims[pose_id]}"
                )
            coverage = set(mask_cells(pose_id, width, mask)) & pose_unseen[pose_id]
            covers[pose_id] = sorted(coverage)

        candidates.append(
            {
                "id": candidate_id,
                "covers": covers,
                "redundancy_penalty": float(raw.get("redundancy_penalty", 0.0)),
                "weak_overlap_penalty": float(raw.get("weak_overlap_penalty", 0.0)),
            }
        )

    return {
        "max_residual_unseen_fraction": float(
            obj.get("max_residual_unseen_fraction", 0.01)
        ),
        "poses": poses,
        "candidates": candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    try:
        problem = build_problem(args.manifest)
    except (OSError, json.JSONDecodeError, MaskError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED_MASK_INPUT", "error": str(exc)}))
        return 2

    rendered = json.dumps(problem, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
