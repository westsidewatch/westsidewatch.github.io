#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def dump(path, obj):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')


def dump_jsonl(path, rows):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spine', required=True)
    ap.add_argument('--render-report', required=True)
    ap.add_argument('--camera-state', required=True)
    ap.add_argument('--routing-advisory', required=True)
    a = ap.parse_args()

    spine = read(a.spine)
    report = read(a.render_report)
    poses = spine.get('poses', [])
    rows = []
    for i in range(max(0, len(poses) - 1)):
        p0 = poses[i]; p1 = poses[i + 1]
        a0 = [float(x) for x in p0.get('position', [0,0,0])]
        a1 = [float(x) for x in p1.get('position', [0,0,0])]
        dx, dy, dz = a1[0]-a0[0], a1[1]-a0[1], a1[2]-a0[2]
        rows.append({
            'segment_index': i,
            'from_pose': p0.get('id'),
            'to_pose': p1.get('id'),
            'delta_xyz': [dx, dy, dz],
            'lateral_motion': math.hypot(dx, dy),
            'z_motion': abs(dz),
            'fov_delta_degrees': float(p1.get('fov_degrees',0)) - float(p0.get('fov_degrees',0)),
            'observer_mode': 'shadow'
        })
    dump_jsonl(a.camera_state, rows)
    residual = float(report.get('max_final_viewfinder_residual_fraction', 0.0))
    advisory = {
        'mode': 'advisory_only',
        'authoritative': False,
        'may_change_renderer': False,
        'may_change_camera_spine': False,
        'may_change_output_pixels': False,
        'camera_segments': len(rows),
        'observed_status': report.get('status'),
        'observed_raster_step': report.get('raster_step'),
        'observed_max_residual_fraction': residual,
        'observed_structural_disocclusion_pixels': report.get('worst_frame_structural_disocclusion_pixels'),
        'observed_micro_raster_candidate_pixels': report.get('worst_frame_micro_raster_candidate_pixels'),
        'recommendation': 'collect evidence only; routing remains disabled'
    }
    dump(a.routing_advisory, advisory)
    print(json.dumps(advisory, indent=2))

if __name__ == '__main__':
    main()
