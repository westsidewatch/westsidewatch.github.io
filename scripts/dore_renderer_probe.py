from __future__ import annotations

import json
import os
import platform
import subprocess

from dore_core.capabilities.providers import ProviderDescriptor, probe_json_http_provider


def _memory_bytes() -> int | None:
    if platform.system() == "Darwin":
        try:
            return int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip())
        except Exception:
            return None
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        return int(pages * page_size)
    except Exception:
        return None


def main() -> int:
    endpoint = os.environ.get("DORE_IMAGE_ENDPOINT", "http://127.0.0.1:8188")
    descriptor = ProviderDescriptor(
        id="local-image-renderer",
        transport="http-json",
        endpoint=endpoint,
        cost_class="local_free",
    )
    health = probe_json_http_provider(descriptor)
    report = {
        "status": "PASS" if health.ok else "NOT_READY",
        "provider": descriptor.id,
        "cost_class": descriptor.cost_class,
        "endpoint": descriptor.endpoint,
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "memory_bytes": _memory_bytes(),
            "python": platform.python_version(),
        },
        "health": {
            "ok": health.ok,
            "detail": health.detail,
            "metadata": health.metadata,
        },
        "interpretation": (
            "resident local renderer reachable; model/workflow/license still require explicit verification"
            if health.ok
            else "no resident renderer verified at configured endpoint; do not claim image generation capability yet"
        ),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0 if health.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
