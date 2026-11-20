#!/usr/bin/env python3
"""Fail a Westside Pages build if an old favicon replaces approved W R1."""
from pathlib import Path
from hashlib import sha256
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
icon = root / 'static/favicon.svg'
template = root / 'layouts/_default/baseof.html'
expected_sha256 = '5d14b2dcd6947dbcd73bee1ba58346d4d8f039dae03cd23bf0dc8277b4a1ea3d'
issues = []

if not icon.is_file():
    issues.append('Missing canonical static/favicon.svg')
else:
    raw = icon.read_bytes()
    if sha256(raw).hexdigest() != expected_sha256:
        issues.append('Production W icon differs from approved R1 bytes. Obtain explicit design approval for a new release and update its lock.')
    try:
        svg = ET.fromstring(raw)
        if svg.attrib.get('data-ws-icon-release') != 'R1-20261120':
            issues.append('Approved R1 icon marker is missing')
        if not any(element.attrib.get('fill') == '#A2872A' for element in svg):
            issues.append('Canonical gold token missing')
        if not any(element.attrib.get('fill') == '#FAF9F5' for element in svg):
            issues.append('Canonical paper token missing')
    except ET.ParseError as exc:
        issues.append(f'Invalid SVG: {exc}')

if not template.is_file():
    issues.append('Hugo base template missing')
else:
    html = template.read_text(encoding='utf-8')
    if '"favicon.svg" | relURL' not in html or '?v=20261120-w-r1' not in html:
        issues.append('Hugo base template must reference the canonical versioned favicon.svg')

if issues:
    for issue in issues:
        print(f'::error::{issue}', file=sys.stderr)
    raise SystemExit(1)
print('Westside R1 icon authority verified: canonical SVG, OS tokens, Hugo entrypoint.')
