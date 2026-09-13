#!/usr/bin/env python3
"""Real-browser raster evidence for Doré Design sandbox candidates.

No synthetic fallback is allowed: a candidate raster is valid only when an
installed Chrome/Chromium-family browser renders the canonical candidate HTML
into a PNG. PNG dimensions are verified from the IHDR chunk using stdlib only.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

BROWSERS = (
    'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser',
)

MAC_BROWSER_PATHS = (
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
)


def _mac_browser_paths() -> tuple[str, ...]:
    home = Path.home()
    return MAC_BROWSER_PATHS + (
        str(home / 'Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
        str(home / 'Applications/Chromium.app/Contents/MacOS/Chromium'),
        str(home / 'Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'),
        str(home / 'Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'),
    )


def browser_binary() -> str:
    override = os.environ.get('DORE_DESIGN_BROWSER')
    if override:
        p = shutil.which(override) or (override if Path(override).exists() else None)
        if p:
            return str(p)
        raise RuntimeError('configured_design_browser_not_found:' + override)
    for name in BROWSERS:
        p = shutil.which(name)
        if p:
            return p
    for candidate in _mac_browser_paths():
        path = Path(candidate)
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
    raise RuntimeError('real_browser_required_for_raster_evidence')


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
        raise ValueError('invalid_png_raster')
    width, height = struct.unpack('>II', data[16:24])
    if width < 1 or height < 1:
        raise ValueError('invalid_png_dimensions')
    return width, height


def rasterize_html(html: str, *, output: Path, width: int, height: int) -> dict:
    if not isinstance(html, str) or '<html' not in html.lower():
        raise ValueError('candidate_html_required')
    width = max(64, min(int(width), 8192))
    height = max(64, min(int(height), 8192))
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    browser = browser_binary()
    with tempfile.TemporaryDirectory(prefix='dore-raster-') as td:
        src = Path(td) / 'candidate.html'
        src.write_text(html, encoding='utf-8')
        cmd = [
            browser,
            '--headless=new',
            '--disable-gpu',
            '--hide-scrollbars',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--force-device-scale-factor=1',
            f'--window-size={width},{height}',
            f'--screenshot={output.resolve()}',
            src.resolve().as_uri(),
        ]
        cp = subprocess.run(cmd, text=True, capture_output=True, timeout=90)
        if cp.returncode != 0 or not output.exists():
            raise RuntimeError('browser_raster_failed:' + (cp.stderr or cp.stdout or '')[-2000:])
    actual_w, actual_h = png_dimensions(output)
    raw = output.read_bytes()
    return {
        'schema': 'dore.design.raster-evidence.v1',
        'engine': Path(browser).name,
        'path': str(output),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'width': actual_w,
        'height': actual_h,
        'requested_width': width,
        'requested_height': height,
        'byte_size': len(raw),
        'real_browser_render': True,
    }


def rasterize_candidate(candidate: dict, *, root: Path, task_id: str) -> dict:
    geometry = candidate.get('geometry') or {}
    canvas = geometry.get('canvas') or {}
    width = int(round(float(canvas.get('w') or 1440)))
    height = int(round(float(canvas.get('h') or 900)))
    cid = str(candidate.get('candidate_id') or '').strip()
    if not cid:
        raise ValueError('candidate_id_required')
    target = Path(root) / 'rasters' / str(task_id) / (cid + '.png')
    evidence = rasterize_html(candidate.get('rendered_html') or '', output=target, width=width, height=height)
    if evidence['width'] != width or evidence['height'] != height:
        raise RuntimeError(f'raster_dimension_mismatch:{evidence["width"]}x{evidence["height"]}!={width}x{height}')
    return evidence
