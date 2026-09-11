#!/usr/bin/env python3
"""Continuous AW-011 production pipeline entrypoint.

Runs production preflight first. If a scaffold manifest is supplied, immediately
validates provider output against the generated build manifest. The runner stops at
the first invalid boundary and never fabricates missing production artifacts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_aw011 import InputError, build
from scaffold_gate import MaskError, ScaffoldError, validate


def run(production_manifest: Path, out_dir: Path, scaffold_manifest: Path | None = None) -> dict:
    preflight = build(production_manifest, out_dir)
    result = {
        "aw_id": "AW-011",
        "stage": "camera-corridor-pipeline-v1",
        "preflight": preflight,
        "scaffold": None,
    }

    if preflight["status"] != "READY_FOR_SCAFFOLD":
        result["status"] = preflight["status"]
        return result

    if scaffold_manifest is None:
        result["status"] = "AWAITING_SCAFFOLD"
        return result

    scaffold_report = validate(out_dir / "build-manifest.json", scaffold_manifest)
    result["scaffold"] = scaffold_report
    result["status"] = "SCAFFOLD_ACCEPTED"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("production_manifest", type=Path)
    parser.add_argument("--scaffold-manifest", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("build/aw-011"))
    args = parser.parse_args()

    try:
        report = run(args.production_manifest, args.out_dir, args.scaffold_manifest)
    except (InputError, ScaffoldError, MaskError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"aw_id": "AW-011", "status": "BLOCKED_PIPELINE", "error": str(exc)}))
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "pipeline-report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] in ("AWAITING_SCAFFOLD", "SCAFFOLD_ACCEPTED") else 3


if __name__ == "__main__":
    raise SystemExit(main())
