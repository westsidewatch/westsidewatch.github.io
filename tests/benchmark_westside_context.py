"""Real-world baseline benchmark for the Westside Context projection."""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

from dore_core.context.compiler import build_index, search, search_context


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

CONTEXT_CASES = (
    ("ONE 查經前哨站", ("Main Site", "2. Journal", "WALK", "以馬忤斯 Emmaus")),
    ("黎明書局", ("Main Site", "4. 橄欖山 / Mount of Olives", "4.1 黎明書局 / Dawn Library")),
    ("多雷探索", ("Main Site", "9. 多雷探索 / Doré Exploration")),
)


def run(source: Path, limit: int) -> int:
    markdown = source.read_text(encoding="utf-8")
    db = sqlite3.connect(":memory:")
    source_sha = build_index(markdown, db, str(source))
    failures = []

    print(f"source: {source}")
    print(f"sha256: {source_sha}")
    print(f"queries: {len(QUERIES)}")

    for query, expected in QUERIES:
        results = search(db, query, limit=limit)
        titles = [node.title for node in results]
        ok = any(expected in title for title in titles)
        if not ok:
            failures.append(f"retrieval: {query} -> {expected}")
        print(f"[{'PASS' if ok else 'MISS'}] {query}")

    print(f"\nretrieval baseline: {len(QUERIES) - sum('retrieval:' in x for x in failures)}/{len(QUERIES)}")
    print("context packet cases:")

    for query, expected_chain in CONTEXT_CASES:
        packets = search_context(db, query, limit=limit)
        actual = ()
        for packet in packets:
            chain = tuple(node.title for node in packet.ancestors) + (packet.match.title,)
            if chain == expected_chain:
                actual = chain
                break
        ok = actual == expected_chain
        if not ok:
            failures.append(f"context: {query} -> {' > '.join(expected_chain)}")
        print(f"[{'PASS' if ok else 'MISS'}] {query}")
        if actual:
            print("       " + " > ".join(actual))

    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print(f"- {failure}")
    else:
        print("\nALL CONTEXT BASELINES PASS")
    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("docs/MASTER_SITE_ARCHITECTURE.md"))
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.limit < 1 or not args.source.is_file():
        print("invalid benchmark arguments/source", file=sys.stderr)
        return 2
    return run(args.source, args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
