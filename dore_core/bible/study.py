from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .reference import BibleReference


ALLOWED_BLOCK_KINDS = {
    "heading",
    "bible-reference",
    "note",
    "evidence",
    "quotation",
    "question",
    "application",
    "cue",
    "media",
}

ALLOWED_ACTIONS = {"keep", "flow", "present"}


@dataclass
class StudyFlowItem:
    block_id: str
    order: int
    duration_seconds: Optional[int] = None
    present: bool = False

    def __post_init__(self) -> None:
        if not self.block_id:
            raise ValueError("flow_block_id_required")
        if self.order < 0:
            raise ValueError("flow_order_must_be_non_negative")
        if self.duration_seconds is not None and self.duration_seconds < 0:
            raise ValueError("flow_duration_must_be_non_negative")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_id": self.block_id,
            "order": self.order,
            "duration_seconds": self.duration_seconds,
            "present": self.present,
        }


@dataclass
class StudyBlock:
    id: str
    kind: str
    text: str = ""
    bible_reference: Optional[BibleReference] = None
    source_ref: Optional[str] = None
    evidence_status: Optional[str] = None
    actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("study_block_id_required")
        if self.kind not in ALLOWED_BLOCK_KINDS:
            raise ValueError("unsupported_study_block_kind")
        unknown = [action for action in self.actions if action not in ALLOWED_ACTIONS]
        if unknown:
            raise ValueError("unsupported_study_block_action")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "text": self.text,
            "bible_reference": (
                self.bible_reference.to_dict() if self.bible_reference else None
            ),
            "source_ref": self.source_ref,
            "evidence_status": self.evidence_status,
            "actions": list(self.actions),
            "metadata": dict(self.metadata),
        }


@dataclass
class StudyDocument:
    id: str
    title: str
    mode: str = "prepare"
    bible_context: Optional[BibleReference] = None
    blocks: List[StudyBlock] = field(default_factory=list)
    flow: List[StudyFlowItem] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("study_document_id_required")
        if self.mode not in {"prepare", "live", "present"}:
            raise ValueError("unsupported_study_document_mode")

    @property
    def planned_duration_seconds(self) -> int:
        return sum(item.duration_seconds or 0 for item in self.flow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": "dore.study-document.v1",
            "id": self.id,
            "title": self.title,
            "mode": self.mode,
            "bible_context": self.bible_context.to_dict() if self.bible_context else None,
            "blocks": [block.to_dict() for block in self.blocks],
            "flow": [item.to_dict() for item in sorted(self.flow, key=lambda x: x.order)],
            "planned_duration_seconds": self.planned_duration_seconds,
            "metadata": dict(self.metadata),
        }
