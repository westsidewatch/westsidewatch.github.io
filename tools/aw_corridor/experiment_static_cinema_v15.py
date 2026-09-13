#!/usr/bin/env python3
"""AW-011 V15: force the real second blade through a stricter engraving gate.

V14 proved the dual-blade plumbing but its gate was too permissive. V15 keeps
exactly the same camera, geometry, first blade and second blade, and changes only
the admission gate so flat/weakly structured wound fills are rejected.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import cv2
import numpy as np
import experiment_static_cinema_v14 as base


def _orientation_hist(gray: np.ndarray, mask: np.ndarray, bins: int = 12):
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy)
    ang = (cv2.phase(gx, gy, angleInDegrees=True) % 180.0)
    sel = mask & (mag > 6.0)
    if not np.any(sel):
        return np.zeros(bins, np.float32)
    h, _ = np.histogram(ang[sel], bins=bins, range=(0.0, 180.0), weights=mag[sel])
    h = h.astype(np.float32)
    s = float(h.sum())
    return h / s if s > 0 else h


def strict_engraving_metrics(img: np.ndarray, wound: np.ndarray, ring_px: int = 5):
    m = wound.astype(np.uint8)
    if not np.any(m):
        return {
            'wound_pixels':0,'edge_density_wound':0.0,'edge_density_ring':0.0,
            'variance_wound':0.0,'variance_ring':0.0,'edge_density_ratio':1.0,
            'variance_ratio':1.0,'orientation_similarity':1.0,
            'line_crossing_score':1.0,'fidelity_pass':True,
            'gate':'v15_strict_engraving_continuity'
        }
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(ring_px*2+1,ring_px*2+1))
    wound_b=m>0
    ring=(cv2.dilate(m,kernel)>0)&(~wound_b)
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(g,45,110)>0
    ew=float(edges[wound_b].mean()) if np.any(wound_b) else 0.0
    er=float(edges[ring].mean()) if np.any(ring) else 0.0
    vw=float(np.var(g[wound_b].astype(np.float32))) if np.any(wound_b) else 0.0
    vr=float(np.var(g[ring].astype(np.float32))) if np.any(ring) else 0.0
    edge_ratio=ew/max(er,1e-6); var_ratio=vw/max(vr,1e-6)

    hw=_orientation_hist(g,wound_b); hr=_orientation_hist(g,ring)
    orientation_similarity=float(np.minimum(hw,hr).sum())

    # A line-crossing proxy: edges inside the wound should touch a dilated edge
    # field on both sides often enough to look like continuation, not a gray cap.
    wound_edges=edges & wound_b
    ring_edges=edges & ring
    near_ring=cv2.dilate(ring_edges.astype(np.uint8),np.ones((5,5),np.uint8))>0
    crossing=float((wound_edges & near_ring).sum()/max(int(wound_edges.sum()),1))

    # V14 frame 08 was ~0.583 edge ratio / ~0.620 variance ratio and looked bad.
    # V15 intentionally rejects that class. Orientation and crossing prevent a
    # noisy fill from passing merely by having enough contrast.
    passed=bool(
        edge_ratio>=0.78 and
        var_ratio>=0.72 and
        orientation_similarity>=0.58 and
        crossing>=0.55
    )
    return {
        'wound_pixels':int(np.count_nonzero(wound_b)),
        'edge_density_wound':ew,'edge_density_ring':er,
        'variance_wound':vw,'variance_ring':vr,
        'edge_density_ratio':edge_ratio,'variance_ratio':var_ratio,
        'orientation_similarity':orientation_similarity,
        'line_crossing_score':crossing,
        'fidelity_pass':passed,
        'gate':'v15_strict_engraving_continuity'
    }


def _report_path(argv):
    for i,a in enumerate(argv):
        if a=='--report' and i+1<len(argv): return Path(argv[i+1])
        if a.startswith('--report='): return Path(a.split('=',1)[1])
    return None


def main():
    base.engraving_metrics = strict_engraving_metrics
    report = _report_path(sys.argv[1:])
    rc = base.main()
    if report and report.exists():
        data=json.loads(report.read_text(encoding='utf-8'))
        data['status']='STATIC_CINEMA_V15_SECOND_BLADE_DEPLOYED_READY_FOR_VISUAL_REVIEW'
        data['mode']='v13_geometry_blade_plus_v15_strict_fidelity_gate_plus_real_engraving_blade'
        data['fidelity_gate']='v15_strict_engraving_continuity'
        data['fidelity_thresholds']={
            'edge_density_ratio_min':0.78,
            'variance_ratio_min':0.72,
            'orientation_similarity_min':0.58,
            'line_crossing_score_min':0.55
        }
        data['capability_policy']='blade1 geometry closure -> strict engraving continuity gate -> blade2 mandatory on flat/discontinuous fills; no generative fallback'
        report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(data,indent=2))
    return rc

if __name__=='__main__':
    raise SystemExit(main())
