from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Sequence


class Route(str, Enum):
    DAWN = "dawn-library"
    BIBLE_WORLD = "one-bible-world"
    HOLD = "hold-review"
    HIDDEN = "retain-raw-hide-public"


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
        [record.title, record.creator or "", *record.subjects, *record.text_types]
    ).casefold()


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    return " ".join(value.split()).strip() or None


def _work_key(creator: str | None, title: str) -> str:
    left = (creator or "anonymous").casefold()
    right = title.casefold()
    return "::".join((" ".join(left.split()), " ".join(right.split())))


def classify(record: SourceRecord) -> AdmissionDecision:
    text = _haystack(record)
    creator = _normalize(record.creator)
    title = _normalize(record.title) or record.source_id
    reasons: list[str] = []
    passed: list[str] = ["metadata-present"]
    pending: list[str] = []

    # Bible editions/texts never enter Dawn automatic translation.
    if any(marker in text for marker in BIBLE_TEXT_MARKERS):
        reasons.append("scripture-text-or-bible-edition")
        return AdmissionDecision(record.source, record.source_id, Route.BIBLE_WORLD,
                                 creator, title, None, tuple(reasons), tuple(passed), tuple(pending))

    # Scripture commentary/exposition is routed to ONE/Bible-world for boundary review.
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
    """Cheap deterministic first pass over hundreds/thousands of source records.

    It deliberately does not canonicalize. It shrinks the corpus and emits only
    ambiguous/high-value candidates for the expensive identity/dedup gates.
    """
    return tuple(classify(record) for record in records)


def summarize(decisions: Sequence[AdmissionDecision]) -> dict[str, int]:
    summary = {route.value: 0 for route in Route}
    for decision in decisions:
        summary[decision.route.value] += 1
    summary["total"] = len(decisions)
    return summary
