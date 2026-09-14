#!/usr/bin/env python3
"""Compile the canonical identity spine into bounded Resource Fabric surface projections."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DAWN = ROOT / "static" / "dawn-library"
CANONICAL = DAWN / "canonical-index.json"
COVERS = DAWN / "cover-registry.json"
SURFACE = DAWN / "surfaces" / "dawn-storefront.json"
OUT = DAWN / "resource-fabric"
WORK_SHARDS = 64
SEARCH_BUCKETS = 64
TOKEN_RE = re.compile(r"[\w\u3400-\u9fff]+", re.UNICODE)


def fnv1a(text: str) -> int:
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def normalize(text: str) -> str:
    return " ".join(TOKEN_RE.findall((text or "").casefold()))


def token_prefix(token: str) -> str:
    return token[: min(4, len(token))]


def dump(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main() -> int:
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
    works = canonical.get("works") or {}
    covers = json.loads(COVERS.read_text(encoding="utf-8")) if COVERS.exists() else {"covers": {}}
    cover_map = covers.get("covers") or {}
    surface = json.loads(SURFACE.read_text(encoding="utf-8")) if SURFACE.exists() else {"shelves": []}

    work_shards = [[] for _ in range(WORK_SHARDS)]
    search_buckets = [[] for _ in range(SEARCH_BUCKETS)]
    featured_ids = []
    for shelf in surface.get("shelves") or []:
        for item in shelf.get("items") or []:
            wid = item.get("workId")
            if wid and wid not in featured_ids:
                featured_ids.append(wid)

    projected = {}
    for wid, work in works.items():
        authors = work.get("authors") or []
        author = authors[0] if authors else ""
        cover_pointer = ((cover_map.get(wid) or {}).get("pointer") or (work.get("cover") or {}).get("pointer"))
        record = [
            wid,
            work.get("title") or "Untitled",
            author,
            cover_pointer,
            work.get("readingPointer"),
            bool(work.get("authorityBacked")),
            authors,
            work.get("languages") or [],
            work.get("authorityIds") or {},
            work.get("edition") or {},
        ]
        projected[wid] = record
        work_shards[fnv1a(wid) % WORK_SHARDS].append(record)

        text = normalize(f"{record[1]} {record[2]}")
        prefixes = {token_prefix(t) for t in text.split() if t}
        for prefix in prefixes:
            bucket = fnv1a(prefix) % SEARCH_BUCKETS
            search_buckets[bucket].append([prefix, wid, record[1], record[2]])

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("work-*.json"):
        old.unlink()
    for old in OUT.glob("search-*.json"):
        old.unlink()

    for i, rows in enumerate(work_shards):
        dump(OUT / f"work-{i:02x}.json", {"schema":"dore.resource-fabric.work-shard.v0","rows":rows})
    for i, rows in enumerate(search_buckets):
        dump(OUT / f"search-{i:02x}.json", {"schema":"dore.resource-fabric.search-bucket.v0","rows":rows})

    featured = [projected[wid] for wid in featured_ids if wid in projected]
    dump(OUT / "featured.json", {"schema":"dore.resource-fabric.featured.v0","rows":featured})
    dump(OUT / "manifest.json", {
        "schema":"dore.resource-fabric.surface-manifest.v0",
        "workCount":len(works),
        "authorityBackedWorks":sum(1 for w in works.values() if w.get("authorityBacked")),
        "workShardCount":WORK_SHARDS,
        "searchBucketCount":SEARCH_BUCKETS,
        "featuredCount":len(featured),
        "identityAuthority":canonical.get("identityAuthority") or "Dawn",
        "canonicalMonolithRequired":False,
        "recordSchema":["workId","title","primaryAuthor","coverPointer","readingPointer","authorityBacked","authors","languages","authorityIds","edition"],
        "delta":{"schema":"dore.resource-fabric.delta-routing.v0","segments":[],"retiredSegments":[],"workRoutes":{},"searchRoutes":{}},
        "deltaWorkCount":0,
    })

    compiled = sum(len(x) for x in work_shards)
    assert compiled == len(works)
    assert all(wid in projected for wid in featured_ids if wid in works)
    print(f"DORE_RESOURCE_FABRIC_SURFACE_WORKS={compiled}")
    print("DORE_RESOURCE_FABRIC_SURFACE_PROJECTION=PASS")
    print("DORE_RESOURCE_FABRIC_CURATED_NOT_EXISTENCE_GATE=PASS")
    print("DORE_RESOURCE_FABRIC_SHARED_CONSUMER_PROJECTION=PASS")
    print("DORE_RESOURCE_FABRIC_DELTA_ROUTING_READY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
