#!/usr/bin/env python3
"""AW-011 V7: residual-driven multilayer persistent LDI.

Extends V6 by constructing additional hidden depth/color layers only where the
camera corridor still exposes missing world. Doré RGB remains immutable on the
front layer; hidden evidence is generated once in canonical space and reused.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np
from experiment_depth_traversal import prepare, load_pose_points, smoothstep
from experiment_world_cache import build_hidden_layer, raster_layer


def build_layers(src, dep, count=4):
    rgb1, d1, mask = build_hidden_layer(src, dep)
    layers = [(rgb1, d1)]
    # Additional layers recede progressively.  Completion is canonical and
    # deterministic: no frame is independently synthesized.
    base_rgb = rgb1
    base_depth = d1
    for i in range(1, count):
        radius = 7.0 + 4.0 * i
        grow = cv2.dilate(mask, np.ones((9 + 4*i, 9 + 4*i), np.uint8), iterations=1)
        rgb = cv2.inpaint(base_rgb, grow, radius, cv2.INPAINT_TELEA)
        depth = np.clip(cv2.GaussianBlur(base_depth, (0, 0), 5.0 + 2*i) - (0.10 + 0.05*i), 0.0, 1.0).astype(np.float32)
        layers.append((rgb, depth))
        base_rgb, base_depth = rgb, depth
    return layers, mask


def render(src, dep, layers, p, ppu=520.0, step=6, fg_thr=0.10):
    h, w = dep.shape
    frame = np.zeros_like(src)
    occupied = np.zeros((h, w), np.uint8)
    per_layer = []
    # Farthest to nearest hidden layer.
    for rgb, depth in reversed(layers):
        img, known = raster_layer(rgb, depth, p, ppu, step, None)
        add = (known > 0) & (occupied == 0)
        frame[add] = img[add]
        occupied[known > 0] = 255
        per_layer.append(int(np.count_nonzero(add)))
    front, front_known = raster_layer(src, dep, p, ppu, step, fg_thr)
    frame[front_known > 0] = front[front_known > 0]
    residual = (front_known == 0) & (occupied == 0)
    # Diagnostic fallback only; not counted as world coverage.
    if np.any(residual):
        stable = cv2.inpaint(frame, residual.astype(np.uint8)*255, 3.0, cv2.INPAINT_TELEA)
        frame[residual] = stable[residual]
    u = float(np.count_nonzero(front_known == 0) / front_known.size)
    r = float(np.count_nonzero(residual) / front_known.size)
    c = max(0.0, u-r)
    return frame, u, c, r, per_layer


def main():
    ap=argparse.ArgumentParser()
    for n in ("source","depth","spine","output","report"):
        ap.add_argument("--"+n,type=Path,required=True)
    ap.add_argument("--width",type=int,default=960); ap.add_argument("--fps",type=int,default=24)
    ap.add_argument("--segment-frames",type=int,default=24); ap.add_argument("--layers",type=int,default=4)
    a=ap.parse_args()
    src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    layers,mask=build_layers(src,dep,max(1,a.layers)); h,w=src.shape[:2]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    wr=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*"mp4v"),a.fps,(w,h))
    if not wr.isOpened(): raise RuntimeError("video writer failed")
    unseen=[]; coverage=[]; residual=[]; layer_pixels=np.zeros(len(layers),np.int64)
    worst={"fraction":-1.0,"frame":-1,"pose":None}; frame_no=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]["position"],np.float32); p1=np.asarray(poses[i+1]["position"],np.float32)
        for j in range(a.segment_frames):
            s=smoothstep(j/float(a.segment_frames)); p=p0*(1-s)+p1*s
            frame,u,c,r,lp=render(src,dep,layers,p); wr.write(frame)
            unseen.append(u); coverage.append(c); residual.append(r)
            layer_pixels += np.asarray(list(reversed(lp)),np.int64)
            if r>worst["fraction"]: worst={"fraction":r,"frame":frame_no,"pose":[float(x) for x in p]}
            frame_no+=1
    wr.write(src); wr.release()
    max_u=max(unseen,default=0.0); max_r=max(residual,default=0.0)
    ratios=[c/u if u>1e-9 else 1.0 for c,u in zip(coverage,unseen)]; mean_ratio=float(np.mean(ratios))
    passed=max_u>0.001 and mean_ratio>=0.90 and max_r<=0.005
    report={"status":"MULTILAYER_LDI_ACCEPTED" if passed else "MULTILAYER_LDI_INSUFFICIENT",
      "mode":"moge2_residual_driven_multilayer_ldi_v7","layer_count":len(layers),
      "hidden_layers_generated_once":True,"per_frame_synthesis":False,
      "max_foreground_unseen_fraction":max_u,"mean_hidden_layer_coverage_ratio":mean_ratio,
      "max_residual_uncovered_fraction":max_r,"worst_residual":worst,
      "hidden_source_mask_fraction":float(np.count_nonzero(mask)/mask.size),
      "layer_contributed_pixels_total":[int(x) for x in layer_pixels],
      "exact_final_source_relock":True,"quantitative_gate":passed,"visual_gate":"PENDING_HUMAN_REVIEW"}
    a.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2))
    return 0 if passed else 2
if __name__=="__main__": raise SystemExit(main())
