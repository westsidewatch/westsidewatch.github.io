#!/usr/bin/env python3
"""Recovered PARADISO HLS verification core.

Source: user-owned paradiso_engine_v1.zip (2026-11-20).
This is a source-inspection gate for authorized media, not a stream
redistributor, DRM bypass, or automatic public catalog admission.
The original provider discovery layer remains in the archived ZIP;
it is intentionally not enabled by the public website.
"""
from __future__ import annotations

import ipaddress
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urljoin, urlparse

CASINO = re.compile(
    r'(?i)(?:賭場|赌场|博彩|彩票|娱乐城|真人荷官|老虎机|下注|充[值幣币]|'
    r'casino|betting|sportsbook|slot\s*machine|gambling|jackpot|poker\s*bonus)'
)
ADS = re.compile(
    r'(?i)EXT-X-(?:CUE-(?:OUT|IN)|DATERANGE|SCTE35|ASSET|OATCLS-SCTE35)|'
    r'(?:^|/)ads?(?:/|[-_.])|(?:promo|commercial|pre[-_]?roll)[-_/]'
)


class VerificationError(ValueError):
    pass


def validate_public_url(url: str) -> str:
    p = urlparse(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password:
        raise VerificationError('Only public HTTPS URLs are accepted')
    try:
        ip = ipaddress.ip_address(p.hostname)
    except ValueError:
        ip = None
    if ip is not None and not ip.is_global:
        raise VerificationError('Private, reserved, or local IP address not allowed')
    if p.hostname.lower() in ('localhost', 'localhost.localdomain') or p.hostname.endswith(('.local', '.internal')):
        raise VerificationError('Local network host not allowed')
    return url


def parse_hls(playlist: str, base_url: str):
    """Parse a single HLS manifest; reject incomplete VOD and expose ad cues."""
    validate_public_url(base_url)
    lines = [line.strip() for line in playlist.splitlines() if line.strip()]
    if not lines or lines[0] != '#EXTM3U':
        raise VerificationError('Not an HLS manifest')
    marker_lines = [line for line in lines if ADS.search(line)]
    children, segments, durations = [], [], []
    master = False
    for i, line in enumerate(lines):
        if line.startswith('#EXT-X-STREAM-INF:'):
            master = True
            for candidate in lines[i+1:i+2]:
                if not candidate.startswith('#'):
                    children.append(urljoin(base_url, candidate))
        if line.startswith('#EXTINF:'):
            try:
                durations.append(float(line.split(':', 1)[1].split(',')[0]))
            except Exception as exc:
                raise VerificationError('Broken EXTINF duration') from exc
        if line[0] != '#':
            if master:
                continue
            if line.lower().split('?')[0].endswith('.m3u8'):
                children.append(urljoin(base_url, line))
            else:
                segments.append(urljoin(base_url, line))
    keys = [line for line in lines if line.startswith('#EXT-X-KEY:')]
    if not master and lines[-1] != '#EXT-X-ENDLIST':
        raise VerificationError('Incomplete VOD playlist (missing ENDLIST)')
    if not master and len(segments) != len(durations):
        raise VerificationError('Segment count and duration count differ')
    for value in children + segments:
        validate_public_url(value)
    return {
        'master': master, 'children': children, 'segments': segments,
        'duration_sec': round(sum(durations), 2), 'ad_markers': marker_lines,
        'encryption': keys, 'complete': master or lines[-1] == '#EXT-X-ENDLIST',
    }


def permit_import(record):
    """Only authorized, fully reviewed media can enter the real cinema."""
    return bool(
        record.get('copyright_or_usage_review') == 'PASS'
        and record.get('whole_work_verified') is True
        and record.get('every_episode_verified') is True
        and record.get('full_ad_review') == 'PASS'
        and record.get('in_site_playback') == 'PASS'
        and record.get('all_segments_verified') is True
        and record.get('ad_markers_count', 0) == 0
        and not record.get('known_baked_in_ads')
        and record.get('approval') == 'APPROVED'
    )


def merge_catalog(current, verified):
    result = json.loads(json.dumps(current))
    if 'items' not in result or not isinstance(result['items'], list):
        raise VerificationError('Catalog requires items array')
    existing = {str(item.get('id')) for item in result['items']}
    added = []
    for item in verified:
        if not permit_import(item) or str(item.get('id')) in existing:
            continue
        safe = {k: v for k, v in item.items() if k not in ('admin_notes', 'approval')}
        result['items'].append(safe)
        added.append(item.get('id'))
        existing.add(str(item.get('id')))
    return result, added


def scan_video_frames(video: str, output_dir: str, interval_sec: int = 30, duration_sec=None):
    """Inspect authorized local video frames; no result certifies ad-free."""
    if not Path(video).is_file():
        raise VerificationError('Local authorized video file required')
    if interval_sec < 1:
        raise VerificationError('Frame interval must be positive')
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    if duration_sec is None:
        r = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=nk=1:nw=1', video],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode:
            raise VerificationError('ffprobe unable to determine duration')
        duration_sec = float(r.stdout.strip())
    seconds = sorted(set([0, max(0, int(duration_sec-1))]
                         + list(range(0, int(duration_sec), interval_sec))))
    scans = []
    for t in seconds:
        frame = target / f'frame-{t:07d}.jpg'
        cmd = ['ffmpeg', '-y', '-hide_banner', '-nostdin', '-loglevel', 'error',
               '-ss', str(t), '-i', video, '-frames:v', '1',
               '-vf', 'scale=960:-2', str(frame)]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=90)
            if r.returncode or not frame.is_file() or frame.stat().st_size < 500:
                scans.append({'at_sec': t, 'decoded': False, 'ad_keyword_hits': []})
                continue
            p = subprocess.run(['tesseract', str(frame), 'stdout', '--psm', '11'],
                               capture_output=True, text=True, timeout=30)
            matches = sorted(set(m.group(0) for m in CASINO.finditer(p.stdout or '')))
            scans.append({'at_sec': t, 'decoded': True, 'ad_keyword_hits': matches})
        except (subprocess.TimeoutExpired, OSError):
            scans.append({'at_sec': t, 'decoded': False, 'ad_keyword_hits': []})
    status = ('REJECT_AD_SUSPECTED' if any(x['ad_keyword_hits'] for x in scans)
              else 'REJECT_DECODE' if not all(x['decoded'] for x in scans)
              else 'NEEDS_VISUAL_REVIEW')
    return {'video': video, 'duration_sec': duration_sec, 'frames': scans,
            'status': status, 'certified_ad_free': False}


def rank_providers(stats):
    return sorted([
        {'provider': p['provider'], 'sampled': p['sampled'],
         'probe_pass': p['probe_pass'],
         'estimated_probe_success': round((p['probe_pass'] + 1) / (p['sampled'] + 2), 4)}
        for p in stats
    ], key=lambda p: p['estimated_probe_success'], reverse=True)
