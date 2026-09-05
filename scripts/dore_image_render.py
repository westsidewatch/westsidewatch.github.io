from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dore_core.capabilities.image_renderer import ComfyUIRenderer, RenderRequest
from dore_core.capabilities.providers import ProviderDescriptor


def main() -> int:
    parser = argparse.ArgumentParser(description="Doré resident image render entrypoint")
    parser.add_argument("workflow", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--workflow-id")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    workflow = json.loads(args.workflow.read_text(encoding="utf-8"))
    endpoint = os.environ.get("DORE_IMAGE_ENDPOINT", "http://127.0.0.1:8188")
    renderer = ComfyUIRenderer(ProviderDescriptor("local-image-renderer", "http-json", endpoint, "local_free"))
    artifact = renderer.render(RenderRequest(workflow, args.seed, args.model, args.workflow_id))
    print(json.dumps({"status": "PASS", "images": artifact.images, "provenance": artifact.provenance}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
