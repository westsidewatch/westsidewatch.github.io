from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Sequence
import re
import unicodedata


class Route(str, Enum):
    DAWN = "dawn-library"
    BIBLE_WORLD = "one-bible-world"
    HOLD = "hold-review"
    HIDDEN = "retain-raw-hide-public"


class MatchState(str, Enum):
    EXACT = "exact"
    PROBABLE = "probable"
    REVIEW = "review"
    NEW = "new-work"


@dataclass(frozen=True)
class SourceRecord:
    source: str
    source_id: str
    title: str
    creator: str | None = None
    date: str | None = None
    language: str | None = None
    phase: str | None = None
    rights: str | None = None
    subjects: tuple[str, ...] = ()
    text_types: tuple[str, ...] = ()
    readable: bool = False
    identifiers: Mapping[str, str] = field(default_factory=dict)
    alternate_titles: tuple[str, ...] = ()
    publisher: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AdmissionDecision:
    source: str
    source_id: str
    route: Route
    normalized_creator: str | None
    normalized_title: str
    work_key: str | None
    reasons: tuple[str, ...]
    gates_passed: tuple[str, ...]
    gates_pending: tuple[str, ...]


@dataclass(frozen=True)
class WorkCandidate:
    candidate_id: str
    normalized_creator: str | None
    normalized_title: str
    source_records: tuple[SourceRecord, ...]
    identifiers: tuple[tuple[str, str], ...]
    match_state: MatchState
    confidence: float
    reasons: tuple[str, ...]


BIBLE_TEXT_MARKERS = (
    "bible", "holy bible", "new testament", "old testament", "psalter",
)
COMMENTARY_MARKERS = (
    "commentary", "exposition", "annotations upon", "notes upon", "paraphrase upon",
    "homilies on matthew", "upon the epistle", "upon the gospel",
)
CHRISTIAN_READING_MARKERS = (
    "christ", "christian", "church", "divinity", "theology", "god", "faith",
    "prayer", "piety", "sermon", "ministry", "pastor", "saint", "religion",
    "spiritual", "holy living", "holy dying", "providence", "grace",
)


def _haystack(record: SourceRecord) -> str:
    return " ".join(
        [record.title, record.creator or "", *record.alternate_titles,
         *record.subjects, *record.text_types]
    ).casefold()


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or None


def _identity_text(value: str | None) -> str:
    value = _normalize(value) or ""
    value = value.casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return " ".join(value.split())


def _work_key(creator: str | None, title: str) -> str:
    return f"{_identity_text(creator) or 'anonymous'}::{_identity_text(title)}"


def classify(record: SourceRecord) -> AdmissionDecision:
    text = _haystack(record)
    creator = _normalize(record.creator)
    title = _normalize(record.title) or record.source_id
    reasons: list[str] = []
    passed: list[str] = ["metadata-present"]
    pending: list[str] = []

    if any(marker in text for marker in BIBLE_TEXT_MARKERS):
        reasons.append("scripture-text-or-bible-edition")
        return AdmissionDecision(record.source, record.source_id, Route.BIBLE_WORLD,
                                 creator, title, None, tuple(reasons), tuple(passed), tuple(pending))

    if any(marker in text for marker in COMMENTARY_MARKERS):
        reasons.append("scripture-commentary-or-exposition")
        return AdmissionDecision(record.source, record.source_id, Route.BIBLE_WORLD,
                                 creator, title, _work_key(creator, title), tuple(reasons), tuple(passed), tuple(pending))

    rights = (record.rights or "").casefold()
    if record.phase and "phase 2" in record.phase.casefold() and not any(
        token in rights for token in ("cc0", "public domain", "pddl")
    ):
        reasons.append("phase2-rights-not-explicitly-open")
        pending.append("rights")
        return AdmissionDecision(record.source, record.source_id, Route.HOLD,
                                 creator, title, _work_key(creator, title), tuple(reasons), tuple(passed), tuple(pending))

    if not record.readable:
        reasons.append("no-readable-witness-yet")
        pending.append("readable-witness")

    if not any(marker in text for marker in CHRISTIAN_READING_MARKERS):
        reasons.append("not-yet-classified-as-christian-reading")
        return AdmissionDecision(record.source, record.source_id, Route.HIDDEN,
                                 creator, title, _work_key(creator, title), tuple(reasons), tuple(passed), tuple(pending))

    reasons.append("christian-reading-candidate")
    pending.extend(("work-identity", "cross-source-dedup", "rights-provenance"))
    if record.readable:
        passed.append("readable-witness")
    return AdmissionDecision(record.source, record.source_id, Route.DAWN,
                             creator, title, _work_key(creator, title), tuple(reasons), tuple(passed), tuple(dict.fromkeys(pending)))


def process_batch(records: Iterable[SourceRecord]) -> tuple[AdmissionDecision, ...]:
    return tuple(classify(record) for record in records)


def summarize(decisions: Sequence[AdmissionDecision]) -> dict[str, int]:
    summary = {route.value: 0 for route in Route}
    for decision in decisions:
        summary[decision.route.value] += 1
    summary["total"] = len(decisions)
    return summary


def _shared_identifier(a: SourceRecord, b: SourceRecord) -> bool:
    a_ids = {(k.casefold(), v.casefold()) for k, v in a.identifiers.items() if v}
    b_ids = {(k.casefold(), v.casefold()) for k, v in b.identifiers.items() if v}
    return bool(a_ids & b_ids)


def _token_similarity(a: str, b: str) -> float:
    aa, bb = set(_identity_text(a).split()), set(_identity_text(b).split())
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def _record_similarity(a: SourceRecord, b: SourceRecord) -> float:
    if _shared_identifier(a, b):
        return 1.0
    title = max(
        [_token_similarity(a.title, b.title)] +
        [_token_similarity(x, b.title) for x in a.alternate_titles] +
        [_token_similarity(a.title, x) for x in b.alternate_titles]
    )
    creator = _token_similarity(a.creator or "", b.creator or "")
    date_bonus = 0.05 if a.date and b.date and a.date == b.date else 0.0
    publisher_bonus = 0.05 if a.publisher and b.publisher and _identity_text(a.publisher) == _identity_text(b.publisher) else 0.0
    return min(1.0, 0.72 * title + 0.18 * creator + date_bonus + publisher_bonus)


def cluster_dawn_candidates(records: Sequence[SourceRecord], decisions: Sequence[AdmissionDecision] | None = None) -> tuple[WorkCandidate, ...]:
    """Cheap batch entity-resolution stage before external authority reconciliation.

    Exact identifiers and normalized Work keys collapse automatically. Fuzzy matches
    become probable/review candidates; uncertain records remain separate. A later
    adapter may replace/augment this scorer with dedupe/OpenRefine-style learned
    reconciliation without changing the product contract.
    """
    decisions = decisions or process_batch(records)
    dawn_ids = {(d.source, d.source_id) for d in decisions if d.route is Route.DAWN}
    pool = [r for r in records if (r.source, r.source_id) in dawn_ids]
    clusters: list[list[SourceRecord]] = []

    for record in pool:
        best_index: int | None = None
        best_score = 0.0
        for index, cluster in enumerate(clusters):
            score = max(_record_similarity(record, existing) for existing in cluster)
            if score > best_score:
                best_index, best_score = index, score
        if best_index is not None and best_score >= 0.78:
            clusters[best_index].append(record)
        else:
            clusters.append([record])

    result: list[WorkCandidate] = []
    for index, cluster in enumerate(clusters, start=1):
        anchor = cluster[0]
        pair_scores = [
            _record_similarity(anchor, item) for item in cluster[1:]
        ]
        confidence = min(pair_scores) if pair_scores else 1.0
        has_shared_ids = any(_shared_identifier(anchor, item) for item in cluster[1:])
        if len(cluster) == 1:
            state = MatchState.NEW
            reasons = ("single-record-work-candidate", "authority-reconciliation-pending")
        elif has_shared_ids or confidence >= 0.93:
            state = MatchState.EXACT
            reasons = ("high-confidence-record-collapse",)
        elif confidence >= 0.84:
            state = MatchState.PROBABLE
            reasons = ("probable-same-work", "authority-reconciliation-required")
        else:
            state = MatchState.REVIEW
            reasons = ("ambiguous-work-cluster", "manual-or-authority-review-required")
        identifiers = sorted({(k, v) for r in cluster for k, v in r.identifiers.items() if v})
        result.append(WorkCandidate(
            candidate_id=f"work-candidate-{index:06d}",
            normalized_creator=_normalize(anchor.creator),
            normalized_title=_normalize(anchor.title) or anchor.source_id,
            source_records=tuple(cluster),
            identifiers=tuple(identifiers),
            match_state=state,
            confidence=round(confidence, 4),
            reasons=reasons,
        ))
    return tuple(result)


def build_exception_queue(candidates: Sequence[WorkCandidate]) -> tuple[WorkCandidate, ...]:
    """Only ambiguous/probable identities need expensive reconciliation/review."""
    return tuple(c for c in candidates if c.match_state in (MatchState.PROBABLE, MatchState.REVIEW))
