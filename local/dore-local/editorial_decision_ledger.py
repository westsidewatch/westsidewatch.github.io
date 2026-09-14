from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import hashlib
import json

LEDGER_SCHEMA = "dore.editorial-decision.v0"
ALLOWED_DECISIONS = {"accept", "reject", "revise", "defer"}


@dataclass
class EditorialDecision:
    work_id: str
    original: str
    proposal: str
    decision: str
    reason: str
    capability: str = "publishing.dimensional-writing"
    thesis_relation: str = ""
    source_basis: List[Dict[str, Any]] = field(default_factory=list)
    author_revision: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def record(self) -> Dict[str, Any]:
        if self.decision not in ALLOWED_DECISIONS:
            raise ValueError("invalid editorial decision")
        payload = asdict(self)
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return {
            "schema": LEDGER_SCHEMA,
            "decision_id": "ed-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:20],
            **payload,
        }
