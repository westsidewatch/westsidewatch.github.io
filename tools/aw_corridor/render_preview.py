#!/usr/bin/env python3
"""Render a continuous low-resolution AW-011 camera-corridor preview.

The preview is intentionally experimental. Known pixels always come from a planar
reprojection of the real Doré source; only border regions exposed by camera motion
are filled, using OpenCV Telea as D_INFERRED_UNSEEN. The final frame is the source
view again, while the full-resolution production gate remains responsible for the
byte-exact P000 relock.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def frame_for_pose(
    source: np.ndarray,
    dx: int,
    dy: int,
    inpaint_radius: float,
) -> tuple[np.ndarray, int]:
    height, width = source.shape[:2]
    matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    known = cv2.warpAffine(
        source,
        matrix,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )

    known_mask = np.zeros((height, width), dtype=np.uint8)
    cv2.warpAffine(
        np.full((height, width), 255, dtype=np.uint8),
        matrix,
        (width, height),
        dst=known_mask,
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    unseen = cv2.bitwise_not(known_mask)
    unseen_pixels = int(np.count_nonzero(unseen))

    if unseen_pixels:
        output = cv2.inpaint(known, unseen, inpaint_radius, cv2.INPAINT_TELEA)
        output[known_mask > 0] = known[known_mask > 0]
    else:
        output = known
    return output, unseen_pixels


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--spine", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--fps", type=float, default=24.0)
    ap.add_argument("--segment-frames", type=int, nargs="+", default=[24, 24, 36])
    ap.add_argument("--pixels-per-world-unit", type=float, default=420.0)
    ap.add_argument("--inpaint-radius", type=float, default=5.0)
    args = ap.parse_args()

    source_full = cv2.imread(str(args.source), cv2.IMREAD_COLOR)
    if source_full is None:
        raise ValueError(f"cannot read source: {args.source}")
    h0, w0 = source_full.shape[:2]
    if args.width <= 0 or args.width > w0:
        raise ValueError("preview width must be > 0 and <= source width")
    scale = args.width / w0
    height = int(round(h0 * scale))
    source = cv2.resize(source_full, (args.width, height), interpolation=cv2.INTER_AREA)

    spine = json.loads(args.spine.read_text(encoding="utf-8"))
    poses = spine.get("poses")
    if not isinstance(poses, list) or len(poses) < 3:
        raise ValueError("camera spine requires at least three poses")
    if len(args.segment_frames) != len(poses) - 1:
        raise ValueError("segment frame counts must equal pose transitions")
    if any(n < 2 for n in args.segment_frames):
        raise ValueError("each segment needs at least two frames")

    canonical = poses[0]
    cpos = canonical.get("position")
    if not isinstance(cpos, list) or len(cpos) != 3:
        raise ValueError("canonical pose position missing")
    if poses[-1].get("id") != canonical.get("id"):
        raise ValueError("camera spine must return to canonical pose")

    preview_ppwu = args.pixels_per_world_unit * scale
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)

    fourcc_candidates = ["mp4v", "avc1"]
    writer = None
    chosen_codec = None
    for codec in fourcc_candidates:
        candidate = cv2.VideoWriter(
            str(args.output),
            cv2.VideoWriter_fourcc(*codec),
            args.fps,
            (args.width, height),
        )
        if candidate.isOpened():
            writer = candidate
            chosen_codec = codec
            break
        candidate.release()
    if writer is None:
        raise RuntimeError("no MP4 codec available through OpenCV VideoWriter")

    total_frames = 0
    max_unseen_pixels = 0
    max_abs_dx = 0
    max_abs_dy = 0
    segment_reports = []

    try:
        for segment_index, (start, end, count) in enumerate(
            zip(poses[:-1], poses[1:], args.segment_frames)
        ):
            spos = start.get("position")
            epos = end.get("position")
            if not isinstance(spos, list) or not isinstance(epos, list) or len(spos) != 3 or len(epos) != 3:
                raise ValueError("every pose must contain position [x,y,z]")

            seg_max_unseen = 0
            # Avoid duplicate knot frames after the first segment.
            first_i = 0 if segment_index == 0 else 1
            for i in range(first_i, count):
                raw_t = i / (count - 1)
                t = smoothstep(raw_t)
                x = lerp(float(spos[0]), float(epos[0]), t)
                y = lerp(float(spos[1]), float(epos[1]), t)
                dx = int(round((x - float(cpos[0])) * preview_ppwu))
                dy = int(round((y - float(cpos[1])) * preview_ppwu))
                max_abs_dx = max(max_abs_dx, abs(dx))
                max_abs_dy = max(max_abs_dy, abs(dy))

                frame, unseen_pixels = frame_for_pose(source, dx, dy, args.inpaint_radius)
                # The last frame is deliberately the resized source view again.
                if segment_index == len(poses) - 2 and i == count - 1:
                    frame = source.copy()
                    unseen_pixels = 0
                writer.write(frame)
                total_frames += 1
                max_unseen_pixels = max(max_unseen_pixels, unseen_pixels)
                seg_max_unseen = max(seg_max_unseen, unseen_pixels)

            segment_reports.append({
                "from": start.get("id"),
                "to": end.get("id"),
                "requested_frames": count,
                "written_frames": count if segment_index == 0 else count - 1,
                "max_unseen_pixels": seg_max_unseen,
            })
    finally:
        writer.release()

    if not args.output.is_file() or args.output.stat().st_size <= 0:
        raise RuntimeError("preview video was not created")

    report = {
        "aw_id": "AW-011",
        "stage": "continuous-preview-v1",
        "status": "PREVIEW_RENDERED",
        "output": str(args.output),
        "bytes": args.output.stat().st_size,
        "codec": chosen_codec,
        "fps": args.fps,
        "frame_count": total_frames,
        "duration_seconds": total_frames / args.fps,
        "resolution": [args.width, height],
        "source_resolution": [w0, h0],
        "scale": scale,
        "max_abs_dx_pixels": max_abs_dx,
        "max_abs_dy_pixels": max_abs_dy,
        "max_unseen_pixels": max_unseen_pixels,
        "provenance": {
            "known": "B_REPROJECTED_FROM_DORE_011",
            "unseen": "D_INFERRED_UNSEEN_OPEN_CV_TELEA_EXPERIMENT",
        },
        "final_frame": "P000_SOURCE_VIEW_RELOCK",
        "segments": segment_reports,
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
