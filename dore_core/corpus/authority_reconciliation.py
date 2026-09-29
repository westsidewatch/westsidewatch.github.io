from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping, Sequence
import re
import unicodedata

from dore_core.corpus.admission_pipeline import WorkCandidate


class ReconcileState(str, Enum):
    EXACT_AUTHORITY = "exact-authority"
    PROBABLE_AUTHORITY = "probable-authority"
    REVIEW = "review"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class AuthorityWork:
    authority: str
    authority_id: str
    title: str
    creator: str | None = None
    alternate_titles: tuple[str, ...] = ()
    identifiers: Mapping[str, str] | None = None


@dataclass(frozen=True)
class Reconciliation:
    candidate_id: str
    state: ReconcileState
    authority: str | None
    authority_id: str | None
    confidence: float
    reasons: tuple[str, ...]


def _norm(value: str | None) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def _tokens(value: str | None) -> set[str]:
    return set(_norm(value).split())


def _jaccard(a: str | None, b: str | None) -> float:
    aa, bb = _tokens(a), _tokens(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def _candidate_ids(candidate: WorkCandidate) -> set[tuple[str, str]]:
    return {(k.casefold(), v.casefold()) for k, v in candidate.identifiers if v}


def _authority_ids(work: AuthorityWork) -> set[tuple[str, str]]:
    return {(k.casefold(), v.casefold()) for k, v in (work.identifiers or {}).items() if v}


def score(candidate: WorkCandidate, work: AuthorityWork) -> tuple[float, tuple[str, ...]]:
    if _candidate_ids(candidate) & _authority_ids(work):
        return 1.0, ("shared-external-identifier",)
    title_scores = [_jaccard(candidate.normalized_title, work.title)]
    title_scores.extend(_jaccard(candidate.normalized_title, t) for t in work.alternate_titles)
    title = max(title_scores)
    creator = _jaccard(candidate.normalized_creator, work.creator)
    value = min(1.0, 0.82 * title + 0.18 * creator)
    return value, ("title-author-authority-score",)


def reconcile_candidate(candidate: WorkCandidate, authorities: Sequence[AuthorityWork]) -> Reconciliation:
    if not authorities:
        return Reconciliation(candidate.candidate_id, ReconcileState.UNRESOLVED, None, None, 0.0,
                              ("no-authority-candidates",))
    ranked = sorted(((score(candidate, work), work) for work in authorities),
                    key=lambda item: item[0][0], reverse=True)
    (best_score, reasons), best = ranked[0]
    second = ranked[1][0][0] if len(ranked) > 1 else 0.0
    margin = best_score - second
    if best_score == 1.0:
        state = ReconcileState.EXACT_AUTHORITY
    elif best_score >= 0.90 and margin >= 0.08:
        state = ReconcileState.EXACT_AUTHORITY
    elif best_score >= 0.78 and margin >= 0.05:
        state = ReconcileState.PROBABLE_AUTHORITY
    elif best_score >= 0.68:
        state = ReconcileState.REVIEW
    else:
        state = ReconcileState.UNRESOLVED
    return Reconciliation(candidate.candidate_id, state, best.authority, best.authority_id,
                          round(best_score, 4), reasons + (f"margin:{margin:.4f}",))


def reconcile_batch(candidates: Iterable[WorkCandidate], authority_index: Mapping[str, Sequence[AuthorityWork]]) -> tuple[Reconciliation, ...]:
    """Authority index is keyed by cheap normalized blocking keys supplied by adapters.

    PRDL/Open Library adapters can populate several keys per authority Work. This stage
    stays source-agnostic so Dawn Library never depends on one external authority.
    """
    output = []
    for candidate in candidates:
        creator = _norm(candidate.normalized_creator)
        title = _norm(candidate.normalized_title)
        keys = (f"ct:{creator}::{title}", f"c:{creator}", f"t:{title}")
        pool: list[AuthorityWork] = []
        seen: set[tuple[str, str]] = set()
        for key in keys:
            for work in authority_index.get(key, ()):
                identity = (work.authority, work.authority_id)
                if identity not in seen:
                    seen.add(identity)
                    pool.append(work)
        output.append(reconcile_candidate(candidate, pool))
    return tuple(output)
