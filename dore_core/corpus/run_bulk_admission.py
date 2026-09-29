from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from dore_core.corpus.admission_pipeline import (
    MatchState, build_exception_queue, cluster_dawn_candidates,
    process_batch, summarize,
)
from dore_core.corpus.adapters.eebo_tcp import iter_csv, iter_tei


def run(source: str, fmt: str, limit: int | None = None) -> dict:
    records = tuple(iter_csv(source, limit) if fmt == "csv" else iter_tei(source, limit))
    decisions = process_batch(records)
    candidates = cluster_dawn_candidates(records, decisions)
    exceptions = build_exception_queue(candidates)
    states = Counter(c.match_state.value for c in candidates)
    return {
        "source": "EEBO-TCP",
        "input": source,
        "format": fmt,
        "limit": limit,
        "sourceRecords": len(records),
        "routes": summarize(decisions),
        "workCandidates": len(candidates),
        "matchStates": dict(sorted(states.items())),
        "exceptionQueue": len(exceptions),
        "autoResolvable": sum(states[s.value] for s in (MatchState.EXACT, MatchState.NEW)),
        "policy": {
            "bibleText": "ONE/Bible-world",
            "commentary": "ONE/Bible-world",
            "ambiguousIdentity": "exception queue",
            "weakMatch": "keep separate",
            "translation": "after canonical admission via Doré Language Faculty",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Doré corpus-scale admission")
    parser.add_argument("source")
    parser.add_argument("--format", choices=("tei", "csv"), default="tei")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = run(args.source, args.format, args.limit)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
