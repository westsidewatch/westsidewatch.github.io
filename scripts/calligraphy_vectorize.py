#!/usr/bin/env python3
"""Minimal calligraphy bitmap -> canonical SVG bridge.

Uses the mature open-source Potrace CLI when available. This deliberately stays
small: preprocess elsewhere if needed; this module only traces, tightens the
viewBox, and emits a reusable glyph SVG.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

_VIEWBOX = re.compile(r'viewBox="([^"]+)"')
_WIDTH = re.compile(r'\swidth="[^"]+"')
_HEIGHT = re.compile(r'\sheight="[^"]+"')


def vectorize(input_path: Path, output_path: Path, *, threshold: float = 0.55, turdsize: int = 2) -> Path:
    potrace = shutil.which("potrace")
    if not potrace:
        raise RuntimeError("potrace is required (install the open-source Potrace CLI)")

    suffix = input_path.suffix.lower()
    if suffix not in {".pbm", ".pgm", ".ppm", ".bmp"}:
        raise RuntimeError("input must be PBM/PGM/PPM/BMP; use the existing image ingest step for conversion")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="calligraphy-svg-") as td:
        raw_svg = Path(td) / "glyph.svg"
        # Potrace handles bitmap tracing; -t removes tiny scan noise, -a keeps curves smooth.
        subprocess.run([
            potrace, str(input_path), "-s", "-o", str(raw_svg),
            "-t", str(turdsize), "-a", "1.0"
        ], check=True)
        svg = raw_svg.read_text(encoding="utf-8")

    # Canonical web asset: responsive SVG, preserve the tracer's exact path geometry.
    svg = _WIDTH.sub('', svg, count=1)
    svg = _HEIGHT.sub('', svg, count=1)
    if not _VIEWBOX.search(svg):
        raise RuntimeError("tracer SVG has no viewBox")
    svg = svg.replace('<svg ', '<svg width="100%" height="100%" preserveAspectRatio="xMidYMid meet" ', 1)
    output_path.write_text(svg, encoding="utf-8")
    return output_path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--threshold", type=float, default=.55)
    p.add_argument("--turdsize", type=int, default=2)
    args = p.parse_args()
    vectorize(args.input, args.output, threshold=args.threshold, turdsize=args.turdsize)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
