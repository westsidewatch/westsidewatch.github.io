from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dore_core.capabilities.image_pipeline import generate_resident_image, result_payload
from dore_core.capabilities.image_renderer import ComfyUIRenderer
from dore_core.capabilities.image_workflow import template_from_payload
from dore_core.capabilities.providers import ProviderDescriptor


def _json_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Doré native resident image generation")
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("dore-image/generated"))
    parser.add_argument("--correction", default="")
    args = parser.parse_args()

    endpoint = os.environ.get("DORE_IMAGE_ENDPOINT", "http://127.0.0.1:8188")
    descriptor = ProviderDescriptor("local-image-renderer", "http-json", endpoint, "local_free")
    renderer = ComfyUIRenderer(descriptor)
    template = template_from_payload(_json_object(args.template))
    result = generate_resident_image(
        renderer=renderer,
        template=template,
        brief=_json_object(args.brief),
        subject=args.subject,
        model=args.model,
        seed=args.seed,
        output_dir=args.output_dir,
        correction_direction=args.correction,
    )
    print(json.dumps({"status": "PASS", **result_payload(result)}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
