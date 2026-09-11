#!/usr/bin/env python3
"""Compose generated AW-011 pixels only into scaffold-declared unseen regions."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from mask_evidence import MaskError, read_binary_png
from png_raster import RasterError, read_png, write_png


class FrameGateError(ValueError):
    pass


def compose(known_path: Path, generated_path: Path, unseen_mask_path: Path, out_path: Path) -> dict:
    kw, kh, kc, known = read_png(known_path)
    gw, gh, gc, generated = read_png(generated_path)
    mw, mh, unseen = read_binary_png(unseen_mask_path)
    if (kw, kh) != (gw, gh) or (kw, kh) != (mw, mh):
        raise FrameGateError(
            f"dimension mismatch: known={(kw,kh)}, generated={(gw,gh)}, mask={(mw,mh)}"
        )
    if kc != gc:
        raise FrameGateError(f"channel mismatch: known={kc}, generated={gc}")

    output = bytearray(known)
    unseen_pixels = 0
    for pixel_index, enabled in enumerate(unseen):
        if not enabled:
            continue
        unseen_pixels += 1
        start = pixel_index * kc
        output[start:start+kc] = generated[start:start+kc]

    known_delta = 0
    for pixel_index, enabled in enumerate(unseen):
        if enabled:
            continue
        start = pixel_index * kc
        known_delta += sum(
            1 for i in range(kc) if output[start+i] != known[start+i]
        )
    if known_delta != 0:
        raise FrameGateError(f"known-pixel conservation failed: {known_delta} channel deltas")

    write_png(out_path, kw, kh, kc, bytes(output))
    return {
        "status": "FRAME_ACCEPTED",
        "width": kw,
        "height": kh,
        "channels": kc,
        "known_pixel_count": kw * kh - unseen_pixels,
        "unseen_pixel_count": unseen_pixels,
        "known_channel_delta_count": known_delta,
        "output": str(out_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("known", type=Path)
    parser.add_argument("generated", type=Path)
    parser.add_argument("unseen_mask", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        report = compose(args.known, args.generated, args.unseen_mask, args.output)
    except (OSError, MaskError, RasterError, FrameGateError, ValueError) as exc:
        print(json.dumps({"status":"BLOCKED_FRAME","error":str(exc)}))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
