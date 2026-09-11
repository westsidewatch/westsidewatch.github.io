#!/usr/bin/env python3
"""Compile the provider-neutral AW011 corridor into camera matrices and adapter jobs.

No model inference happens here. Camera Spine remains authority; providers consume the
compiled package. The output is intentionally small and replaceable.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def c2w_from_pose(eye, yaw_deg, pitch_deg):
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    ry = [[cy, 0.0, sy], [0.0, 1.0, 0.0], [-sy, 0.0, cy]]
    rx = [[1.0, 0.0, 0.0], [0.0, cp, -sp], [0.0, sp, cp]]
    r = matmul(ry, rx)
    return [
        [r[0][0], r[0][1], r[0][2], eye[0]],
        [r[1][0], r[1][1], r[1][2], eye[1]],
        [r[2][0], r[2][1], r[2][2], eye[2]],
        [0.0, 0.0, 0.0, 1.0],
    ]


def transpose(m):
    return [list(x) for x in zip(*m)]


def rigid_inverse(m):
    r = [row[:3] for row in m[:3]]
    rt = transpose(r)
    t = [m[0][3], m[1][3], m[2][3]]
    it = [-sum(rt[i][k] * t[k] for k in range(3)) for i in range(3)]
    return [
        [rt[0][0], rt[0][1], rt[0][2], it[0]],
        [rt[1][0], rt[1][1], rt[1][2], it[1]],
        [rt[2][0], rt[2][1], rt[2][2], it[2]],
        [0.0, 0.0, 0.0, 1.0],
    ]


def compile_package(spec):
    anchors = []
    by_id = {}
    for a in spec["anchors"]:
        c2w = c2w_from_pose(a["eye"], a["yaw_deg"], a["pitch_deg"])
        item = {**a, "c2w": c2w, "w2c": rigid_inverse(c2w), "intrinsics": spec["intrinsics"]}
        anchors.append(item)
        by_id[a["id"]] = item

    a0 = by_id["A0"]
    jobs = []
    for aid in ("A1", "A2"):
        tar = by_id[aid]
        jobs.append({
            "id": f"GENWARP-{aid}",
            "source_anchor": "A0",
            "target_anchor": aid,
            "source_c2w": a0["c2w"],
            "target_c2w": tar["c2w"],
            "expected_outputs": ["synthesized", "warped", "mask_raw", "correspondence"],
            "postprocess": [
                "derive normalized visible/unseen masks from actual warp coverage",
                "preserve warped known pixels as B_REPROJECTED",
                "label only true holes as D_INFERRED_UNSEEN",
                "never overwrite A0 canonical pixels"
            ]
        })

    return {
        "schema": "dore-film-anchor-package/v0.1",
        "source_corridor": spec["id"],
        "authority_anchor": spec["authority_anchor"],
        "camera_convention": spec["camera_convention"],
        "anchors": anchors,
        "camera_path": spec["camera_path"],
        "anchor_generation_jobs": jobs,
        "scaffold_input": {
            "ordered_views": ["A0", "A1", "A2"],
            "image_shape": spec["scaffold_contract"]["context_image"],
            "intrinsics_shape": spec["scaffold_contract"]["context_intrinsics"],
            "extrinsics_shape": spec["scaffold_contract"]["context_extrinsics"],
            "camera_matrix": "c2w",
        },
        "hard_rule": "Camera asks first; canonical/warped evidence wins; generation owns absence only."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    package = compile_package(spec)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(package, indent=2), encoding="utf-8")
    print(f"compiled {len(package['anchors'])} anchors and {len(package['anchor_generation_jobs'])} generation jobs -> {args.output}")


if __name__ == "__main__":
    main()
