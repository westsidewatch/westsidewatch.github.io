from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from dore_core.corpus.admission_pipeline import (
    MatchState, build_exception_queue, cluster_dawn_candidates,
    process_batch, summarize,
)
from dore_core.corpus.authority_reconciliation import ReconcileState, reconcile_batch
from dore_core.corpus.adapters.authority_index import (
    build_index, iter_openlibrary_works, iter_prdl_csv, merge_indexes,
)
from dore_core.corpus.adapters.eebo_tcp import iter_csv, iter_tei


def run(source: str, fmt: str, limit: int | None = None,
        openlibrary: str | None = None, prdl: str | None = None,
        authority_limit: int | None = None) -> dict:
    records = tuple(iter_csv(source, limit) if fmt == "csv" else iter_tei(source, limit))
    decisions = process_batch(records)
    candidates = cluster_dawn_candidates(records, decisions)
    local_exceptions = build_exception_queue(candidates)
    states = Counter(c.match_state.value for c in candidates)

    indexes = []
    authority_sources = []
    if openlibrary:
        indexes.append(build_index(iter_openlibrary_works(openlibrary, authority_limit)))
        authority_sources.append("OpenLibrary")
    if prdl:
        indexes.append(build_index(iter_prdl_csv(prdl, authority_limit)))
        authority_sources.append("PRDL")

    reconciliations = ()
    authority_states: Counter[str] = Counter()
    if indexes:
        authority_index = merge_indexes(*indexes)
        reconciliations = reconcile_batch(candidates, authority_index)
        authority_states.update(r.state.value for r in reconciliations)

    authority_exceptions = sum(
        authority_states[s.value] for s in (ReconcileState.PROBABLE_AUTHORITY, ReconcileState.REVIEW)
    )
    existing_merges = authority_states[ReconcileState.EXACT_AUTHORITY.value]
    unresolved_new = authority_states[ReconcileState.UNRESOLVED.value] if indexes else states[MatchState.NEW.value]

    return {
        "source": "EEBO-TCP",
        "input": source,
        "format": fmt,
        "limit": limit,
        "sourceRecords": len(records),
        "routes": summarize(decisions),
        "workCandidates": len(candidates),
        "matchStates": dict(sorted(states.items())),
        "localExceptionQueue": len(local_exceptions),
        "authority": {
            "sources": authority_sources,
            "states": dict(sorted(authority_states.items())),
            "existingWorkMerges": existing_merges,
            "unresolvedNewWorks": unresolved_new,
            "exceptionQueue": authority_exceptions,
        },
        "policy": {
            "bibleText": "ONE/Bible-world",
            "commentary": "ONE/Bible-world",
            "authorityExact": "merge beneath existing canonical/authority Work candidate",
            "authorityProbableOrReview": "exception queue",
            "authorityUnresolved": "retain as new Work candidate; do not fabricate match",
            "weakMatch": "keep separate",
            "translation": "after canonical admission via Doré Language Faculty",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Doré corpus-scale admission")
    parser.add_argument("source")
    parser.add_argument("--format", choices=("tei", "csv"), default="tei")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--openlibrary", help="Open Library works dump (.txt/.gz)")
    parser.add_argument("--prdl", help="Normalized PRDL bibliography CSV")
    parser.add_argument("--authority-limit", type=int)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = run(args.source, args.format, args.limit, args.openlibrary, args.prdl, args.authority_limit)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
