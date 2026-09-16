#!/usr/bin/env python3
"""Real-browser raster evidence for Doré Design sandbox candidates.

No synthetic fallback is allowed: a candidate raster is valid only when an
installed supported browser renders the canonical candidate HTML into a PNG.
PNG dimensions are verified from the IHDR chunk using stdlib only.
"""
from __future__ import annotations

import hashlib
import os
import json
import signal
import time
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

BROWSERS = (
    'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'firefox',
)

MAC_BROWSER_PATHS = (
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Firefox.app/Contents/MacOS/firefox',
)


def _mac_browser_paths() -> tuple[str, ...]:
    home = Path.home()
    return MAC_BROWSER_PATHS + (
        str(home / 'Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
        str(home / 'Applications/Chromium.app/Contents/MacOS/Chromium'),
        str(home / 'Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'),
        str(home / 'Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'),
        str(home / 'Applications/Firefox.app/Contents/MacOS/firefox'),
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


def _browser_command(browser: str, *, output: Path, width: int, height: int, uri: str, profile: Path) -> list[str]:
    name = Path(browser).name.lower()
    if 'firefox' in name:
        return [
            browser,
            '--headless',
            '--no-remote',
            '--profile', str(profile.resolve()),
            '--window-size', f'{width},{height}',
            '--screenshot', str(output.resolve()),
            uri,
        ]
    return [
        browser,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--force-device-scale-factor=1',
        f'--user-data-dir={profile.resolve()}',
        f'--window-size={width},{height}',
        f'--screenshot={output.resolve()}',
        uri,
    ]


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
        raise ValueError('invalid_png_raster')
    width, height = struct.unpack('>II', data[16:24])
    if width < 1 or height < 1:
        raise ValueError('invalid_png_dimensions')
    return width, height


def _stop_browser(proc):
    """Reap only this isolated browser session, including inherited children."""
    if os.name == 'posix':
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif proc.poll() is None:
        proc.kill()
    proc.wait()


def _render_attempt(browser, root, output, width, height, attempt):
    profile = root / f'profile-{attempt}'
    profile.mkdir()
    if 'firefox' in Path(browser).name.lower():
        # Fresh profiles must not perform first-run UI or background updates.
        prefs = {'browser.shell.checkDefaultBrowser': False,
                 'browser.startup.homepage_override.mstone': 'ignore',
                 'browser.aboutwelcome.enabled': False,
                 'datareporting.policy.dataSubmissionEnabled': False,
                 'toolkit.telemetry.reportingpolicy.firstRun': False,
                 'app.update.auto': False,
                 'layout.css.devPixelsPerPx': '1.0'}
        (profile / 'user.js').write_text(''.join(
            f'user_pref({json.dumps(k)}, {json.dumps(v)});\n' for k, v in prefs.items()))
    cmd = _browser_command(browser, output=output, width=width, height=height,
                           uri=(root / 'candidate.html').resolve().as_uri(), profile=profile)
    started = time.monotonic()
    # File-backed logs avoid waiting forever for EOF from browser descendants.
    log = root / f'browser-{attempt}.log'
    with log.open('wb') as stream:
        proc = subprocess.Popen(cmd, stdout=stream, stderr=stream,
                                start_new_session=(os.name == 'posix'))
        try:
            code = proc.wait(timeout=45)
            if code != 0:
                raise RuntimeError(f'browser_exit:{code}')
            if png_dimensions(output) != (width, height):
                raise RuntimeError('raster_dimension_mismatch')
        except (subprocess.TimeoutExpired, RuntimeError, OSError, ValueError) as exc:
            raise RuntimeError(f'{type(exc).__name__}:{exc}') from exc
        finally:
            _stop_browser(proc)
    return round(time.monotonic() - started, 3)


def rasterize_html(html: str, *, output: Path, width: int, height: int) -> dict:
    if not isinstance(html, str) or '<html' not in html.lower():
        raise ValueError('candidate_html_required')
    width = max(64, min(int(width), 8192))
    height = max(64, min(int(height), 8192))
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    browser = browser_binary()
    with tempfile.TemporaryDirectory(prefix='dore-raster-') as td:
        root = Path(td)
        src = root / 'candidate.html'
        src.write_text(html, encoding='utf-8')
        failures = []
        # Never admit a stale output or a partial screenshot from a failed process.
        for attempt in (1, 2):
            pending = root / f'candidate-{attempt}.png'
            try:
                elapsed = _render_attempt(browser, root, pending, width, height, attempt)
                output.write_bytes(pending.read_bytes())
                break
            except RuntimeError as exc:
                log = root / f'browser-{attempt}.log'
                failures.append({'attempt': attempt, 'error': str(exc),
                                 'log': log.read_text(errors='replace')[-4000:] if log.exists() else ''})
        else:
            diagnostic = output.with_suffix('.raster-failure.json')
            diagnostic.write_text(json.dumps({'browser': browser, 'attempts': failures}, indent=2))
            raise RuntimeError('browser_raster_failed:' + str(diagnostic) + ':' + json.dumps(failures))
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
