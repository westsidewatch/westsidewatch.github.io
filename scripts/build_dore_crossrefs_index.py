#!/usr/bin/env python3
"""Build Doré's browser cross-reference shards from the NEUU/OpenBible+TSK corpus.

The upstream dataset is CC BY 4.0 and stored with Git LFS. This builder downloads the
single consolidated LFS object, normalizes references to Doré OSIS codes, guarantees
bidirectionality, and emits 66 lazy-loadable book shards plus a provenance manifest.
No Bible translation text is copied into the generated index.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

UPSTREAM_REPO = "https://github.com/neuu-org/bible-crossrefs-dataset.git"
UPSTREAM_PATH = "data/01_processed/combined_crossrefs.json"
OUT_DIR = Path("static/dore/crossrefs")
MANIFEST = OUT_DIR / "manifest.json"
SOURCE_ID = "neuu-bible-crossrefs"
LICENSE = "CC BY 4.0"

BOOK_ALIASES = {
    "GEN":"GEN","EXO":"EXO","LEV":"LEV","NUM":"NUM","DEU":"DEU","JOS":"JOS","JOSH":"JOS","JDG":"JDG","JUDG":"JDG","RUT":"RUT","RUTH":"RUT",
    "1SA":"1SA","1SAM":"1SA","2SA":"2SA","2SAM":"2SA","1KI":"1KI","1KGS":"1KI","2KI":"2KI","2KGS":"2KI","1CH":"1CH","1CHR":"1CH","2CH":"2CH","2CHR":"2CH",
    "EZR":"EZR","NEH":"NEH","EST":"EST","ESTH":"EST","JOB":"JOB","PSA":"PSA","PS":"PSA","PSALM":"PSA","PRO":"PRO","PRV":"PRO","ECC":"ECC","QOH":"ECC","SNG":"SNG","SONG":"SNG","SOS":"SNG",
    "ISA":"ISA","JER":"JER","LAM":"LAM","EZK":"EZK","EZE":"EZK","DAN":"DAN","HOS":"HOS","JOL":"JOL","JOE":"JOL","JOEL":"JOL","AMO":"AMO","OBA":"OBA","OBAD":"OBA","JON":"JON","JONAH":"JON","MIC":"MIC","NAM":"NAM","NAH":"NAM","HAB":"HAB","ZEP":"ZEP","HAG":"HAG","ZEC":"ZEC","MAL":"MAL",
    "MAT":"MAT","MATT":"MAT","MRK":"MRK","MARK":"MRK","LUK":"LUK","LUKE":"LUK","JHN":"JHN","JOH":"JHN","JOHN":"JHN","ACT":"ACT","ROM":"ROM","1CO":"1CO","1COR":"1CO","2CO":"2CO","2COR":"2CO","GAL":"GAL","EPH":"EPH","PHP":"PHP","PHIL":"PHP","COL":"COL","1TH":"1TH","1THES":"1TH","2TH":"2TH","2THES":"2TH","1TI":"1TI","1TIM":"1TI","2TI":"2TI","2TIM":"2TI","TIT":"TIT","PHM":"PHM","HEB":"HEB","JAS":"JAS","JAM":"JAS","1PE":"1PE","1PET":"1PE","2PE":"2PE","2PET":"2PE","1JN":"1JN","1JOHN":"1JN","2JN":"2JN","2JOHN":"2JN","3JN":"3JN","3JOHN":"3JN","JUD":"JUD","JUDE":"JUD","REV":"REV",
}
BOOKS = [
    "GEN","EXO","LEV","NUM","DEU","JOS","JDG","RUT","1SA","2SA","1KI","2KI","1CH","2CH","EZR","NEH","EST","JOB","PSA","PRO","ECC","SNG","ISA","JER","LAM","EZK","DAN","HOS","JOL","AMO","OBA","JON","MIC","NAM","HAB","ZEP","HAG","ZEC","MAL","MAT","MRK","LUK","JHN","ACT","ROM","1CO","2CO","GAL","EPH","PHP","COL","1TH","2TH","1TI","2TI","TIT","PHM","HEB","JAS","1PE","2PE","1JN","2JN","3JN","JUD","REV"
]


def run(*args: str, cwd: Path | None = None) -> str:
    p = subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=True)
    return p.stdout.strip()


def canonical(ref: str) -> str | None:
    raw = str(ref or "").strip().replace(" ", ".")
    raw = raw.replace("bible.ref.", "")
    parts = [p for p in raw.split(".") if p]
    if len(parts) < 3:
        return None
    book = BOOK_ALIASES.get(parts[0].upper().replace("_", ""))
    if not book:
        return None
    try:
        chapter, verse = int(parts[1]), int(parts[2])
    except ValueError:
        return None
    if chapter < 1 or verse < 1:
        return None
    return f"{book}.{chapter}.{verse}"


def source_mask(meta: Any) -> int:
    mask = 0
    if isinstance(meta, dict):
        sources = meta.get("sources", meta.get("source_details", {}))
        if isinstance(sources, dict):
            names = [str(k).lower() for k, v in sources.items() if v]
        elif isinstance(sources, list):
            names = [str(x.get("source", "")).lower() if isinstance(x, dict) else str(x).lower() for x in sources]
        else:
            names = [str(sources).lower()]
        if any("openbible" in n for n in names): mask |= 1
        if any(("tsk" in n or "souliberty" in n) for n in names): mask |= 2
    return mask or 2


def unpack_target(item: Any) -> tuple[str | None, int, int]:
    if isinstance(item, str):
        return canonical(item), 0, 2
    if not isinstance(item, dict):
        return None, 0, 0
    target = item.get("to") or item.get("target_verse") or item.get("to_verse") or item.get("target") or item.get("ref") or item.get("verse")
    votes = int(item.get("votes") or item.get("vote_count") or 0)
    return canonical(str(target or "")), votes, source_mask(item)


def iter_edges(data: Any) -> Iterable[tuple[str, str, int, int]]:
    if not isinstance(data, dict):
        raise ValueError("NEUU combined_crossrefs.json must be an object keyed by source verse")
    for raw_source, raw_refs in data.items():
        source = canonical(raw_source)
        if not source:
            continue
        if isinstance(raw_refs, dict):
            refs = []
            for target, meta in raw_refs.items():
                if isinstance(meta, dict):
                    refs.append({"to": target, **meta})
                else:
                    refs.append({"to": target})
        elif isinstance(raw_refs, list):
            refs = raw_refs
        else:
            continue
        for item in refs:
            target, votes, mask = unpack_target(item)
            if target and target != source:
                yield source, target, votes, mask


def materialize_upstream(explicit: Path | None) -> tuple[Path, str, tempfile.TemporaryDirectory[str] | None]:
    if explicit:
        return explicit, "local", None
    td: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory(prefix="dore-crossrefs-")
    repo = Path(td.name) / "dataset"
    env = os.environ.copy(); env["GIT_LFS_SKIP_SMUDGE"] = "1"
    subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", UPSTREAM_REPO, str(repo)], check=True, env=env)
    try:
        run("git", "lfs", "version", cwd=repo)
    except Exception as exc:
        td.cleanup(); raise RuntimeError("git-lfs is required to ingest the NEUU corpus") from exc
    run("git", "lfs", "pull", f"--include={UPSTREAM_PATH}", "--exclude=", cwd=repo)
    src = repo / UPSTREAM_PATH
    head = run("git", "rev-parse", "HEAD", cwd=repo)
    if not src.exists() or src.stat().st_size < 1_000_000:
        td.cleanup(); raise RuntimeError("NEUU LFS corpus was not materialized")
    return src, head, td


def build(source_path: Path, upstream_commit: str) -> dict[str, Any]:
    with source_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    pairs: dict[tuple[str, str], list[int]] = {}
    raw_edges = 0
    for a, b, votes, mask in iter_edges(data):
        raw_edges += 1
        for x, y in ((a, b), (b, a)):
            key = (x, y)
            old = pairs.setdefault(key, [0, 0])
            old[0] = max(old[0], votes)
            old[1] |= mask

    by_book: dict[str, dict[str, list[list[Any]]]] = {b: defaultdict(list) for b in BOOKS}
    source_counts = {"openbible": 0, "tsk": 0, "both": 0}
    vertices: set[str] = set()
    for (source, target), (votes, mask) in pairs.items():
        book, ch, vs = source.split(".")
        if book not in by_book:
            continue
        vertices.add(source); vertices.add(target)
        key = f"{ch}.{vs}"
        by_book[book][key].append([target, votes, mask])
        if mask == 3: source_counts["both"] += 1
        elif mask & 1: source_counts["openbible"] += 1
        elif mask & 2: source_counts["tsk"] += 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUT_DIR.glob("*.json"):
        stale.unlink()
    shard_stats = {}
    for book in BOOKS:
        refs = by_book[book]
        for rows in refs.values():
            rows.sort(key=lambda x: (-x[1], -((x[2] == 3) * 1), x[0]))
        payload = {
            "schema": "dore.crossrefs.book.v1",
            "book": book,
            "source_dataset": SOURCE_ID,
            "license": LICENSE,
            "refs": dict(sorted(refs.items(), key=lambda kv: tuple(map(int, kv[0].split(".")))))
        }
        path = OUT_DIR / f"{book}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        shard_stats[book] = {"verses": len(refs), "bytes": path.stat().st_size}

    manifest = {
        "schema": "dore.crossrefs.manifest.v1",
        "source_dataset": SOURCE_ID,
        "source_name": "NEUU Bible Cross-Reference Dataset (OpenBible.info + TSK/SoulLiberty)",
        "license": LICENSE,
        "attribution": "NEUU Bible Cross-Reference Dataset; OpenBible.info cross references; Treasury of Scripture Knowledge/SoulLiberty",
        "upstream_repository": UPSTREAM_REPO,
        "upstream_path": UPSTREAM_PATH,
        "upstream_commit": upstream_commit,
        "contains_bible_text": False,
        "bidirectional": True,
        "stats": {
            "raw_edges": raw_edges,
            "directed_edges": len(pairs),
            "unique_verses": len(vertices),
            "books": sum(1 for b in BOOKS if by_book[b]),
            "source_counts": source_counts
        },
        "shards": shard_stats
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, help="Existing materialized combined_crossrefs.json")
    args = ap.parse_args()
    src, commit, td = materialize_upstream(args.source)
    try:
        manifest = build(src, commit)
    finally:
        if td is not None: td.cleanup()
    s = manifest["stats"]
    if s["directed_edges"] < 1_000_000 or s["unique_verses"] < 30_000:
        raise SystemExit(f"Cross-reference corpus unexpectedly small: {s}")
    print(json.dumps({"status":"PASS", **s, "manifest":str(MANIFEST)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
