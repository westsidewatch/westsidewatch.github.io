#!/usr/bin/env python3
"""Select the minimum useful AW-011 anchor evidence for a fixed Camera Corridor.

The planner is provider-neutral. It operates on discrete evidence cells rather than
image formats so One2Scene/GenWarp/NoPoSplat adapters can all feed the same core.
A cell may be one pixel, a mask tile, or another stable spatial sample identifier.

Input schema:
{
  "max_residual_unseen_fraction": 0.01,
  "poses": [
    {"id": "P001", "weight": 1.0, "unseen": ["x0", "x1"]}
  ],
  "candidates": [
    {
      "id": "A001",
      "covers": {"P001": ["x0"]},
      "redundancy_penalty": 0.0,
      "weak_overlap_penalty": 0.0
    }
  ]
}

Output is a deterministic selection trace plus residual evidence debt.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Set, Tuple


@dataclass(frozen=True)
class Pose:
    id: str
    weight: float
    initial_unseen: frozenset[str]


@dataclass(frozen=True)
class Candidate:
    id: str
    covers: Mapping[str, frozenset[str]]
    redundancy_penalty: float = 0.0
    weak_overlap_penalty: float = 0.0

    @property
    def fixed_penalty(self) -> float:
        return self.redundancy_penalty + self.weak_overlap_penalty


def _as_cells(values: Iterable[object]) -> frozenset[str]:
    return frozenset(str(value) for value in values)


def parse_problem(data: Mapping[str, object]) -> Tuple[List[Pose], List[Candidate], float]:
    threshold = float(data.get("max_residual_unseen_fraction", 0.01))
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("max_residual_unseen_fraction must be between 0 and 1")

    raw_poses = data.get("poses")
    raw_candidates = data.get("candidates")
    if not isinstance(raw_poses, list) or not raw_poses:
        raise ValueError("poses must be a non-empty list")
    if not isinstance(raw_candidates, list):
        raise ValueError("candidates must be a list")

    poses: List[Pose] = []
    seen_pose_ids: Set[str] = set()
    for raw in raw_poses:
        if not isinstance(raw, dict):
            raise ValueError("each pose must be an object")
        pose_id = str(raw["id"])
        if pose_id in seen_pose_ids:
            raise ValueError(f"duplicate pose id: {pose_id}")
        seen_pose_ids.add(pose_id)
        weight = float(raw.get("weight", 1.0))
        if weight < 0:
            raise ValueError(f"pose weight must be non-negative: {pose_id}")
        unseen = raw.get("unseen", [])
        if not isinstance(unseen, list):
            raise ValueError(f"pose unseen must be a list: {pose_id}")
        poses.append(Pose(pose_id, weight, _as_cells(unseen)))

    candidates: List[Candidate] = []
    seen_candidate_ids: Set[str] = set()
    for raw in raw_candidates:
        if not isinstance(raw, dict):
            raise ValueError("each candidate must be an object")
        candidate_id = str(raw["id"])
        if candidate_id in seen_candidate_ids:
            raise ValueError(f"duplicate candidate id: {candidate_id}")
        seen_candidate_ids.add(candidate_id)
        raw_covers = raw.get("covers", {})
        if not isinstance(raw_covers, dict):
            raise ValueError(f"candidate covers must be an object: {candidate_id}")

        covers: Dict[str, frozenset[str]] = {}
        for pose_id, cells in raw_covers.items():
            if str(pose_id) not in seen_pose_ids:
                raise ValueError(f"candidate {candidate_id} references unknown pose {pose_id}")
            if not isinstance(cells, list):
                raise ValueError(f"coverage cells must be a list: {candidate_id}/{pose_id}")
            covers[str(pose_id)] = _as_cells(cells)

        candidates.append(
            Candidate(
                id=candidate_id,
                covers=covers,
                redundancy_penalty=float(raw.get("redundancy_penalty", 0.0)),
                weak_overlap_penalty=float(raw.get("weak_overlap_penalty", 0.0)),
            )
        )

    return poses, candidates, threshold


def residual_fraction(pose: Pose, residual: Set[str]) -> float:
    if not pose.initial_unseen:
        return 0.0
    return len(residual) / len(pose.initial_unseen)


def corridor_passes(
    poses: Iterable[Pose], residuals: Mapping[str, Set[str]], threshold: float
) -> bool:
    return all(residual_fraction(pose, residuals[pose.id]) <= threshold for pose in poses)


def marginal_gain(
    candidate: Candidate,
    poses: Iterable[Pose],
    residuals: Mapping[str, Set[str]],
) -> Tuple[float, Dict[str, int]]:
    per_pose: Dict[str, int] = {}
    weighted_coverage = 0.0
    for pose in poses:
        newly_resolved = residuals[pose.id].intersection(candidate.covers.get(pose.id, frozenset()))
        count = len(newly_resolved)
        per_pose[pose.id] = count
        weighted_coverage += pose.weight * count
    return weighted_coverage - candidate.fixed_penalty, per_pose


def plan(
    poses: List[Pose], candidates: List[Candidate], threshold: float
) -> MutableMapping[str, object]:
    residuals: Dict[str, Set[str]] = {pose.id: set(pose.initial_unseen) for pose in poses}
    remaining = {candidate.id: candidate for candidate in candidates}
    selected: List[MutableMapping[str, object]] = []

    while remaining and not corridor_passes(poses, residuals, threshold):
        ranked = []
        for candidate in remaining.values():
            gain, per_pose = marginal_gain(candidate, poses, residuals)
            ranked.append((gain, candidate.id, candidate, per_pose))

        # Highest marginal gain wins. Candidate id is the deterministic tie-breaker.
        ranked.sort(key=lambda item: (-item[0], item[1]))
        gain, _, winner, per_pose = ranked[0]

        # An anchor that cannot reduce evidence debt is forbidden.
        if gain <= 0:
            break

        before = {pose.id: len(residuals[pose.id]) for pose in poses}
        for pose in poses:
            residuals[pose.id].difference_update(winner.covers.get(pose.id, frozenset()))
        after = {pose.id: len(residuals[pose.id]) for pose in poses}

        selected.append(
            {
                "anchor_id": winner.id,
                "marginal_gain": gain,
                "newly_resolved_cells": per_pose,
                "residual_before": before,
                "residual_after": after,
            }
        )
        del remaining[winner.id]

    pose_report = {}
    for pose in poses:
        pose_report[pose.id] = {
            "initial_unseen_cells": len(pose.initial_unseen),
            "residual_unseen_cells": len(residuals[pose.id]),
            "residual_unseen_fraction": residual_fraction(pose, residuals[pose.id]),
            "passes": residual_fraction(pose, residuals[pose.id]) <= threshold,
        }

    return {
        "planner": "aw-011-greedy-marginal-evidence-v1",
        "threshold": threshold,
        "selected_anchor_ids": [step["anchor_id"] for step in selected],
        "selection_trace": selected,
        "poses": pose_report,
        "corridor_passes": corridor_passes(poses, residuals, threshold),
        "unresolved_pose_ids": [pose.id for pose in poses if residual_fraction(pose, residuals[pose.id]) > threshold],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", type=Path, help="JSON evidence problem")
    parser.add_argument("--out", type=Path, help="write report JSON instead of stdout")
    args = parser.parse_args()

    data = json.loads(args.problem.read_text(encoding="utf-8"))
    poses, candidates, threshold = parse_problem(data)
    report = plan(poses, candidates, threshold)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0 if report["corridor_passes"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
