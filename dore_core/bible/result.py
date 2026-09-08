from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from .context_policy import SearchContextPolicy, apply_search_context_policy
from .reference import BibleReference


_ALLOWED_EVIDENCE_STATUS = {
    "canonical",
    "supported",
    "possible",
    "disputed",
    "unsupported",
}


def augment_context_result(
    result: Dict[str, Any],
    *,
    source_kind: Optional[str] = None,
    bible_reference: Optional[BibleReference] = None,
    evidence_status: Optional[str] = None,
    actions: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """Add Bible Intelligence metadata without breaking legacy result fields."""

    if not isinstance(result, dict):
        raise ValueError("context_result_must_be_object")
    if evidence_status is not None and evidence_status not in _ALLOWED_EVIDENCE_STATUS:
        raise ValueError("unsupported_evidence_status")

    out = dict(result)
    if source_kind is not None:
        out["source_kind"] = str(source_kind).strip().lower()
    elif "source_kind" not in out:
        out["source_kind"] = str(out.get("kind") or "document").strip().lower()

    if bible_reference is not None:
        out["canonical_reference"] = bible_reference.to_dict()
    else:
        out.setdefault("canonical_reference", None)

    if evidence_status is not None:
        out["evidence_status"] = evidence_status
    else:
        out.setdefault("evidence_status", None)

    if actions is not None:
        out["actions"] = list(actions)
    else:
        out.setdefault("actions", ["keep", "flow", "present"])

    return out


def apply_bible_context_result_policy(
    results: Iterable[Dict[str, Any]], policy: SearchContextPolicy
) -> List[Dict[str, Any]]:
    augmented = [augment_context_result(result) for result in results if isinstance(result, dict)]
    return apply_search_context_policy(augmented, policy)
