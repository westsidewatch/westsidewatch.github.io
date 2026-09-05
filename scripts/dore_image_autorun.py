#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path

from dore_core.capabilities.image_pipeline import generate_resident_image, result_payload
from dore_core.capabilities.image_renderer import ComfyUIRenderer
from dore_core.capabilities.image_runtime_config import load_resident_image_config
from dore_core.capabilities.image_workflow import template_from_payload
from dore_core.capabilities.providers import ProviderDescriptor

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "dore-image" / "resident.json"
DEFAULT_JOB = ROOT / "dore-image" / "jobs" / "next.json"


def _object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def run(config_path: Path = DEFAULT_CONFIG, job_path: Path = DEFAULT_JOB) -> dict:
    if not config_path.exists():
        return {"status": "NOT_READY", "reason": "resident-config-missing", "expected": str(config_path.relative_to(ROOT))}
    if not job_path.exists():
        return {"status": "IDLE", "reason": "no-image-job"}
    config = load_resident_image_config(config_path)
    job = _object(job_path)
    template_path = (ROOT / config.template).resolve()
    if ROOT not in template_path.parents:
        raise ValueError("template escapes repository root")
    template = template_from_payload(_object(template_path))
    renderer = ComfyUIRenderer(ProviderDescriptor("local-image-renderer", "http-json", config.endpoint, "local_free"))
    health = renderer.health()
    if not health.ok:
        return {"status": "NOT_READY", "reason": "resident-renderer-unreachable", "provider": health.id}
    result = generate_resident_image(
        renderer=renderer, template=template, brief=dict(job.get("brief") or {}),
        subject=str(job.get("subject") or "Doré editorial image"), model=config.model,
        seed=int(job.get("seed", 1)), output_dir=(ROOT / config.output_dir),
        correction_direction=str(job.get("correction") or ""),
    )
    done = job_path.with_name("last-completed.json")
    done.parent.mkdir(parents=True, exist_ok=True)
    done.write_text(json.dumps({"job": job, "result": result_payload(result)}, ensure_ascii=False, indent=2), encoding="utf-8")
    job_path.unlink()
    return {"status": "PASS", **result_payload(result)}


def main() -> int:
    payload = run(Path(os.environ.get("DORE_IMAGE_CONFIG", DEFAULT_CONFIG)), Path(os.environ.get("DORE_IMAGE_JOB", DEFAULT_JOB)))
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] in {"PASS", "IDLE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
