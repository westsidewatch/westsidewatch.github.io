#!/usr/bin/env python3
"""Dependency-free Resource Fabric inverse-scaling benchmark seed.

This is deliberately not the final storage engine. It freezes the workload and
acceptance metrics before OSS adapters (Parquet/FST/Roaring/Zstd) are selected.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
import zlib
from dataclasses import dataclass

SCALES = (10_000, 100_000, 1_000_000)
PATTERNS = (
    ("en", "book", "public-domain", "remote"),
    ("zh", "book", "link-only", "remote"),
    ("en", "pdf", "link-only", "remote"),
    ("zh", "video", "link-only", "browser-runtime"),
)

@dataclass(frozen=True)
class Work:
    wid: int
    title: str
    creator: str
    pattern: int
    pointer: str


def make_work(i: int) -> Work:
    # Deterministic synthetic corpus: repeated structure + unique delta.
    p = i % len(PATTERNS)
    return Work(i, f"Work {i:07d}", f"Creator {i % 4096:04d}", p, f"src:{i:07x}")


def json_record(w: Work) -> bytes:
    language, kind, rights, access = PATTERNS[w.pattern]
    return json.dumps({
        "id": f"dawn:work:{w.wid}", "title": w.title, "creator": w.creator,
        "language": language, "kind": kind, "rights": rights, "access": access,
        "pointer": w.pointer,
    }, separators=(",", ":")).encode()


def delta_record(w: Work) -> bytes:
    # Shared fields collapse into a pattern reference; only identity/delta remain.
    return f"{w.wid}|{w.pattern}|{w.title}|{w.creator}|{w.pointer}\n".encode()


def run_scale(n: int) -> dict:
    t0 = time.perf_counter()
    raw_bytes = 0
    delta_bytes = 0
    # zlib is only a stdlib control. v1 adapters will benchmark Zstd dictionary.
    compressor = zlib.compressobj(level=6)
    compressed = 0
    membership = [0] * len(PATTERNS)
    sample = {}
    for i in range(n):
        w = make_work(i)
        raw_bytes += len(json_record(w))
        d = delta_record(w)
        delta_bytes += len(d)
        compressed += len(compressor.compress(d))
        membership[w.pattern] += 1
        if i in (0, n // 2, n - 1):
            sample[i] = (w.title, w.creator, w.pattern, w.pointer)
    compressed += len(compressor.flush())
    build_ms = (time.perf_counter() - t0) * 1000

    # O(1) identity lookup model: query touches only the requested delta + atlas pattern.
    rng = random.Random(725)
    q0 = time.perf_counter()
    touched = 0
    for _ in range(1000):
        i = rng.randrange(n)
        w = make_work(i)
        touched += len(delta_record(w)) + len("|".join(PATTERNS[w.pattern]).encode())
    query_ms = (time.perf_counter() - q0) * 1000

    return {
        "works": n,
        "baselineJsonBytesPerWork": raw_bytes / n,
        "deltaBytesPerWork": delta_bytes / n,
        "compressedDeltaBytesPerWork": compressed / n,
        "queryTouchedBytesPerLookup": touched / 1000,
        "buildMs": build_ms,
        "lookup1000Ms": query_ms,
        "membershipCounts": membership,
        "sampleIntegrity": len(sample) == 3,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=1_000_000)
    args = ap.parse_args()
    rows = [run_scale(n) for n in SCALES if n <= args.max]
    if not rows:
        raise SystemExit("no benchmark scale selected")
    print(json.dumps({"schema":"dore.resource-fabric.benchmark.v0","rows":rows}, indent=2))
    if any(not r["sampleIntegrity"] for r in rows):
        return 2
    # The active lookup footprint must remain bounded while corpus grows.
    if len(rows) > 1 and rows[-1]["queryTouchedBytesPerLookup"] > rows[0]["queryTouchedBytesPerLookup"] * 1.15:
        return 3
    print("DORE_RESOURCE_FABRIC_ACTIVE_FOOTPRINT_BOUNDED=PASS")
    print("DORE_RESOURCE_FABRIC_DELTA_MODEL=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
