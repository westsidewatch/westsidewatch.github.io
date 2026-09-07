"""Real-world baseline benchmark for the Westside Context projection.

This benchmark intentionally measures the smallest current implementation first:
canonical Markdown -> SQLite/FTS5 -> ranked context nodes.
It does not modify the canonical architecture and does not require network/API access.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

from dore_core.context.compiler import build_index, search


QUERIES = (
    ("主站結構", "Main Site"),
    ("Journal 的出版核心", "Journal"),
    ("以馬忤斯 Emmaus", "以馬忤斯 Emmaus"),
    ("ONE 查經前哨站", "ONE"),
    ("多寫 寫作研究工作台", "多寫"),
    ("黎明書局", "4.1 黎明書局 / Dawn Library"),
    ("三晨星 光譜 策展集", "The three-layer editorial model"),
    ("知識脈絡", "Knowledge context / 知識脈絡"),
    ("Church Prayer Meeting", "5. Church"),
    ("多雷搜索不是 AI Chat", "7. 全站功能：多雷搜索"),
    ("Storybook 設計訓練環境", "8. Storybook / Design Training Environment"),
    ("多雷探索", "9. 多雷探索 / Doré Exploration"),
)


def run(source: Path, limit: int) -> int:
    markdown = source.read_text(encoding="utf-8")
    db = sqlite3.connect(":memory:")
    source_sha = build_index(markdown, db, str(source))

    passed = 0
    print(f"source: {source}")
    print(f"sha256: {source_sha}")
    print(f"queries: {len(QUERIES)}")
    print()

    for query, expected in QUERIES:
        results = search(db, query, limit=limit)
        titles = [node.title for node in results]
        ok = any(expected in title for title in titles)
        passed += int(ok)
        mark = "PASS" if ok else "MISS"
        print(f"[{mark}] {query}")
        print("       " + " | ".join(titles[:limit]))

    print()
    print(f"baseline: {passed}/{len(QUERIES)} queries retrieved the expected context node")
    return 0 if passed == len(QUERIES) else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("docs/MASTER_SITE_ARCHITECTURE.md"),
        help="canonical Westside architecture Markdown file",
    )
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.limit < 1:
        print("--limit must be >= 1", file=sys.stderr)
        return 2
    if not args.source.is_file():
        print(f"source not found: {args.source}", file=sys.stderr)
        return 2
    return run(args.source, args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
