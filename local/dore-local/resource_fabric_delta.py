#!/usr/bin/env python3
"""Immutable Resource Fabric delta segments and selected compaction.

Updates never rewrite the base corpus. A changed Work becomes one content-addressed
segment routed only to its Work/search buckets. Compaction rewrites only selected
bucket overlays; source segments remain immutable and may be garbage-collected later.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FABRIC = ROOT / "static/dawn-library/resource-fabric"
TOKEN_RE = re.compile(r"[\w\u3400-\u9fff]+", re.UNICODE)


def fnv1a(text: str) -> int:
    h = 0x811C9DC5
    for b in str(text).encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def normalize(text: str) -> str:
    return " ".join(TOKEN_RE.findall((text or "").casefold()))


def prefix(token: str) -> str:
    return token[: min(4, len(token))]


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def load_manifest(root: Path = FABRIC) -> dict:
    data = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if data.get("schema") != "dore.resource-fabric.surface-manifest.v0":
        raise RuntimeError("resource_fabric_manifest_schema_mismatch")
    data.setdefault("delta", {"schema": "dore.resource-fabric.delta-routing.v0", "segments": [], "retiredSegments": [], "workRoutes": {}, "searchRoutes": {}})
    delta = data["delta"]
    delta.setdefault("segments", [])
    delta.setdefault("retiredSegments", [])
    delta.setdefault("workRoutes", {})
    delta.setdefault("searchRoutes", {})
    return data


def record_from_work(work: dict) -> list:
    wid = str(work.get("workId") or "")
    if not wid:
        raise ValueError("workId required")
    authors = work.get("authors") or []
    author = authors[0] if authors else ""
    cover = work.get("resourceCoverPointer") or work.get("coverPointer") or (work.get("cover") or {}).get("pointer")
    return [wid, work.get("title") or "Untitled", author, cover, work.get("readingPointer"), bool(work.get("authorityBacked")), authors, work.get("languages") or [], work.get("authorityIds") or {}, work.get("edition") or {}]


def search_rows(record: list) -> list[list]:
    text = normalize(f"{record[1]} {record[2]}")
    return [[prefix(token), record[0], record[1], record[2]] for token in sorted(set(text.split())) if token]


def segment_payload(record: list, *, op: str = "+Work") -> dict:
    rows = search_rows(record) if op == "+Work" else []
    return {"schema": "dore.resource-fabric.delta-segment.v0", "operations": [{"op": op, "workId": record[0], "record": record if op == "+Work" else None}], "searchRows": rows}


def segment_id(payload: dict) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def route_append(routes: dict, key: str, rel: str) -> None:
    rows = [p for p in routes.get(key, []) if p != rel]
    rows.append(rel)
    routes[key] = rows


def _read_segment(root: Path, rel: str) -> dict:
    return json.loads((root / rel).read_text(encoding="utf-8"))


def overlay_work(root: Path, manifest: dict, work_id: str) -> list | None:
    key = f"{fnv1a(work_id) % int(manifest['workShardCount']):02x}"
    routes = manifest["delta"]["workRoutes"].get(key, [])
    for rel in reversed(routes):
        seg = _read_segment(root, rel)
        for op in reversed(seg.get("operations") or []):
            if op.get("workId") != work_id:
                continue
            if op.get("op") == "-Work":
                return None
            if op.get("op") == "+Work":
                return op.get("record")
    base = json.loads((root / f"work-{key}.json").read_text(encoding="utf-8"))
    return next((row for row in base.get("rows") or [] if row and row[0] == work_id), None)


def append_record(record: list, root: Path = FABRIC) -> dict:
    manifest = load_manifest(root)
    existed = overlay_work(root, manifest, record[0]) is not None
    work_shards = int(manifest["workShardCount"])
    search_buckets = int(manifest["searchBucketCount"])
    payload = segment_payload(record)
    sid = segment_id(payload)
    rel = f"segments/{sid}.json"
    path = root / rel
    before = path.read_bytes() if path.exists() else None
    if not path.exists():
        dump(path, payload)
    if before is not None and path.read_bytes() != before:
        raise RuntimeError("immutable_segment_mutated")
    delta = manifest["delta"]
    if sid not in delta["segments"]:
        delta["segments"].append(sid)
    if not existed:
        manifest["workCount"] = int(manifest.get("workCount") or 0) + 1
    wkey = f"{fnv1a(record[0]) % work_shards:02x}"
    route_append(delta["workRoutes"], wkey, rel)
    for row in payload["searchRows"]:
        skey = f"{fnv1a(row[0]) % search_buckets:02x}"
        route_append(delta["searchRoutes"], skey, rel)
    manifest["deltaWorkCount"] = len({op.get("workId") for rel0 in delta["workRoutes"].values() for p in rel0 for op in (_read_segment(root, p).get("operations") or []) if op.get("op") == "+Work"})
    dump(root / "manifest.json", manifest)
    return {"segmentId": sid, "path": rel, "workBucket": wkey, "searchRows": len(payload["searchRows"]), "touchedBaseShards": 0, "newWork": not existed}


def append_work(work: dict, root: Path = FABRIC) -> dict:
    return append_record(record_from_work(work), root)


def compact_work_bucket(bucket: str, root: Path = FABRIC) -> dict:
    manifest = load_manifest(root)
    routes = list(manifest["delta"]["workRoutes"].get(bucket, []))
    if len(routes) < 2:
        return {"bucket": bucket, "compacted": False, "segments": len(routes)}
    latest: dict[str, dict] = {}
    search_rows_out: list[list] = []
    for rel in routes:
        seg = _read_segment(root, rel)
        for op in seg.get("operations") or []:
            latest[str(op.get("workId"))] = op
    operations = [latest[k] for k in sorted(latest)]
    for op in operations:
        if op.get("op") == "+Work" and op.get("record"):
            search_rows_out.extend(search_rows(op["record"]))
    payload = {"schema": "dore.resource-fabric.delta-segment.v0", "operations": operations, "searchRows": search_rows_out, "compactedFrom": routes}
    sid = segment_id(payload)
    rel = f"segments/{sid}.json"
    path = root / rel
    if not path.exists():
        dump(path, payload)
    delta = manifest["delta"]
    delta["workRoutes"][bucket] = [rel]
    for old in routes:
        if old != rel and old not in delta["retiredSegments"]:
            delta["retiredSegments"].append(old)
    if sid not in delta["segments"]:
        delta["segments"].append(sid)
    touched_search = set()
    for old in routes:
        for row in (_read_segment(root, old).get("searchRows") or []):
            touched_search.add(f"{fnv1a(row[0]) % int(manifest['searchBucketCount']):02x}")
    for skey in touched_search:
        current = [p for p in delta["searchRoutes"].get(skey, []) if p not in routes]
        if any(f"{fnv1a(r[0]) % int(manifest['searchBucketCount']):02x}" == skey for r in search_rows_out):
            current.append(rel)
        delta["searchRoutes"][skey] = current
    dump(root / "manifest.json", manifest)
    return {"bucket": bucket, "compacted": True, "fromSegments": len(routes), "toSegment": rel, "baseShardsRewritten": 0, "searchBucketsTouched": len(touched_search)}


def self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="dore-resource-delta-") as td:
        root = Path(td)
        dump(root / "work-00.json", {"schema": "dore.resource-fabric.work-shard.v0", "rows": []})
        dump(root / "search-00.json", {"schema": "dore.resource-fabric.search-bucket.v0", "rows": []})
        dump(root / "manifest.json", {"schema": "dore.resource-fabric.surface-manifest.v0", "workCount": 0, "workShardCount": 1, "searchBucketCount": 1, "identityAuthority": "Dawn", "canonicalMonolithRequired": False})
        base_hash = hashlib.sha256((root / "work-00.json").read_bytes()).hexdigest()
        ids = []
        for i in range(3):
            work = {"workId": f"dawn:delta:{i}", "title": f"Delta Work {i}", "authors": ["Doré"], "authorityBacked": False}
            result = append_work(work, root)
            ids.append(work["workId"])
            assert result["touchedBaseShards"] == 0 and result["newWork"] is True
        # Updating an existing Work must not inflate workCount.
        updated = {"workId": ids[0], "title": "Delta Work 0 revised", "authors": ["Doré"], "authorityBacked": False}
        update_result = append_work(updated, root)
        assert update_result["newWork"] is False
        manifest = load_manifest(root)
        assert manifest["workCount"] == 3
        before = {wid: overlay_work(root, manifest, wid) for wid in ids}
        routes = manifest["delta"]["workRoutes"]["00"]
        hashes = {rel: hashlib.sha256((root / rel).read_bytes()).hexdigest() for rel in routes}
        compact = compact_work_bucket("00", root)
        after_manifest = load_manifest(root)
        after = {wid: overlay_work(root, after_manifest, wid) for wid in ids}
        assert before == after
        assert base_hash == hashlib.sha256((root / "work-00.json").read_bytes()).hexdigest()
        assert all(hashes[rel] == hashlib.sha256((root / rel).read_bytes()).hexdigest() for rel in routes)
        assert compact["baseShardsRewritten"] == 0
    print("DORE_RESOURCE_FABRIC_DELTA_APPEND_O_DELTA=PASS")
    print("DORE_RESOURCE_FABRIC_DELTA_IDEMPOTENT_COUNT=PASS")
    print("DORE_RESOURCE_FABRIC_SEGMENT_IMMUTABILITY=PASS")
    print("DORE_RESOURCE_FABRIC_SELECTED_COMPACTION=PASS")
    print("DORE_RESOURCE_FABRIC_COMPACTION_EQUIVALENCE=PASS")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--work-json")
    p.add_argument("--compact-work-bucket")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test(); return 0
    if args.work_json:
        work = json.loads(Path(args.work_json).read_text(encoding="utf-8"))
        print(json.dumps(append_work(work), ensure_ascii=False)); return 0
    if args.compact_work_bucket:
        print(json.dumps(compact_work_bucket(args.compact_work_bucket), ensure_ascii=False)); return 0
    p.error("one operation required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
