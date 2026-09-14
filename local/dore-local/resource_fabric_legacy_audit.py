#!/usr/bin/env python3
"""Fail CI when a runtime bypasses the shared Resource Fabric Work substrate."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "dore-core/resource-fabric/legacy-runtime-retirement.v0.json"

# These are authority/reconciliation inputs. They may be read by build/compile/audit code,
# never by product/browser/runtime consumers.
FORBIDDEN_RUNTIME_TOKENS = (
    "canonical-index.json",
    "identity-cache.json",
)

STATIC_RUNTIME_SUFFIXES = {".js", ".mjs", ".html"}
PY_RUNTIME_ROOTS = (
    ROOT / "dore-design",
    ROOT / "local/dore-local",
)

# Build, compiler, migration, benchmark, and this audit are deliberately outside runtime.
PY_BUILD_ONLY_NAMES = {
    "resource_fabric_surface_compile.py",
    "resource_fabric_legacy_audit.py",
    "resource_fabric_inverse_scaling.py",
}
PY_BUILD_ONLY_PATTERNS = (
    re.compile(r"(?:^|_)compile(?:r)?\.py$"),
    re.compile(r"(?:^|_)build(?:er)?\.py$"),
    re.compile(r"(?:^|_)migrat(?:e|ion).*\.py$"),
    re.compile(r"(?:^|_)benchmark.*\.py$"),
)


def is_build_only_python(path: Path) -> bool:
    name = path.name
    if name in PY_BUILD_ONLY_NAMES:
        return True
    return any(pattern.search(name) for pattern in PY_BUILD_ONLY_PATTERNS)


def runtime_files() -> list[Path]:
    out: list[Path] = []
    static = ROOT / "static"
    if static.exists():
        for path in static.rglob("*"):
            if path.is_file() and path.suffix.lower() in STATIC_RUNTIME_SUFFIXES:
                out.append(path)
    for base in PY_RUNTIME_ROOTS:
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if path.is_file() and not is_build_only_python(path):
                out.append(path)
    return sorted(set(out))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema"] == "dore.resource-fabric.legacy-runtime-retirement.v0"
    assert contract["status"] == "enforced"
    assert contract["singleWorkSubstrate"] == "resource-fabric"
    assert contract["boundaries"]["runtimeCanonicalMonolithAllowed"] is False
    assert contract["boundaries"]["consumerCatalogCopiesAllowed"] is False

    offenders: list[dict[str, object]] = []
    scanned = runtime_files()
    for path in scanned:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        hits = [token for token in FORBIDDEN_RUNTIME_TOKENS if token in text]
        if hits:
            offenders.append({"path": rel(path), "tokens": hits})

    specialized = {entry["path"]: entry for entry in contract["specializedIndexes"]}
    scripture = specialized.get("static/dore/search-index.json")
    assert scripture and scripture["purpose"] == "scripture-text-search-only"
    assert scripture["mayBecomeWorkSubstrate"] is False
    entity = specialized.get("static/dore/entity-index.json")
    assert entity and entity["mayBecomeWorkSubstrate"] is False

    browser_client = ROOT / "static/js/resource-fabric-client.mjs"
    python_reader = ROOT / "local/dore-local/resource_fabric_reader.py"
    assert browser_client.exists(), "shared browser Resource Fabric client missing"
    assert python_reader.exists(), "shared Python Resource Fabric reader missing"
    browser_text = browser_client.read_text(encoding="utf-8")
    reader_text = python_reader.read_text(encoding="utf-8")
    assert "canonicalMonolithRequired" in browser_text
    assert "resource-fabric" in browser_text
    assert "resource-fabric" in reader_text

    if offenders:
        print("DORE_RESOURCE_FABRIC_LEGACY_RUNTIME_INDEXES=FAIL")
        for offender in offenders:
            print("legacy-runtime-offender=" + json.dumps(offender, ensure_ascii=False, sort_keys=True))
        raise SystemExit(1)

    print(f"DORE_RESOURCE_FABRIC_LEGACY_RUNTIME_SCANNED={len(scanned)}")
    print("DORE_RESOURCE_FABRIC_LEGACY_RUNTIME_INDEXES=PASS")
    print("DORE_RESOURCE_FABRIC_SINGLE_WORK_SUBSTRATE=PASS")
    print("DORE_RESOURCE_FABRIC_SCRIPTURE_INDEX_SEPARATION=PASS")


if __name__ == "__main__":
    main()
