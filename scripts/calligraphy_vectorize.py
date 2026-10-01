#!/usr/bin/env python3
"""Fast calligraphy image -> canonical SVG.

Accepts a local bitmap or a direct remote image URL. Remote HTML/source pages are
rejected: the caller must provide the actual image asset. ImageMagick converts
common web images to PBM; Potrace traces the glyph to SVG paths.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

_VIEWBOX = re.compile(r'viewBox="([^"]+)"')
_WIDTH = re.compile(r'\swidth="[^"]+"')
_HEIGHT = re.compile(r'\sheight="[^"]+"')


def _tool(*names: str) -> str | None:
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def _download_image(url: str, target: Path) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": "WestsideWatch-Calligraphy/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        content_type = (response.headers.get("Content-Type") or "").lower()
        if "text/html" in content_type:
            raise RuntimeError("source URL is HTML, not a direct glyph image")
        target.write_bytes(response.read())
    return target


def _to_pbm(source: Path, target: Path, threshold: float) -> Path:
    if source.suffix.lower() == ".pbm":
        shutil.copyfile(source, target)
        return target
    magick = _tool("magick", "convert")
    if not magick:
        raise RuntimeError("ImageMagick is required for PNG/JPEG/WebP input")
    threshold_pct = max(0, min(100, round(threshold * 100)))
    cmd = [magick, str(source), "-alpha", "off", "-colorspace", "Gray", "-threshold", f"{threshold_pct}%", str(target)]
    subprocess.run(cmd, check=True)
    return target


def vectorize(input_value: str, output_path: Path, *, threshold: float = 0.55, turdsize: int = 2) -> Path:
    potrace = _tool("potrace")
    if not potrace:
        raise RuntimeError("potrace is required")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="calligraphy-svg-") as td:
        td = Path(td)
        if input_value.startswith(("http://", "https://")):
            suffix = Path(urlparse(input_value).path).suffix or ".img"
            source = _download_image(input_value, td / f"source{suffix}")
        else:
            source = Path(input_value).expanduser().resolve()
            if not source.is_file():
                raise RuntimeError(f"input not found: {source}")

        pbm = _to_pbm(source, td / "glyph.pbm", threshold)
        raw_svg = td / "glyph.svg"
        subprocess.run([potrace, str(pbm), "-s", "-o", str(raw_svg), "-t", str(turdsize), "-a", "1.0"], check=True)
        svg = raw_svg.read_text(encoding="utf-8")

    svg = _WIDTH.sub('', svg, count=1)
    svg = _HEIGHT.sub('', svg, count=1)
    if not _VIEWBOX.search(svg):
        raise RuntimeError("tracer SVG has no viewBox")
    svg = svg.replace('<svg ', '<svg width="100%" height="100%" preserveAspectRatio="xMidYMid meet" ', 1)
    output_path.write_text(svg, encoding="utf-8")
    return output_path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input", help="local image path or direct http(s) image URL")
    p.add_argument("output", type=Path)
    p.add_argument("--threshold", type=float, default=.55)
    p.add_argument("--turdsize", type=int, default=2)
    args = p.parse_args()
    vectorize(args.input, args.output, threshold=args.threshold, turdsize=args.turdsize)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
