from typing import Any, Dict, List

JUDGE_ID = "publishing.dimensional-writing.judge"
JUDGE_VERSION = "0.1"

REQUIRED_CHECKS = (
    "thesis_preserved",
    "author_voice_preserved",
    "dimension_earns_return",
    "evidence_supports_claim",
    "media_participates_in_argument",
    "reader_burden_not_increased",
)


def judge_proposal(proposal: Dict[str, Any]) -> Dict[str, Any]:
    checks = proposal.get("checks") or {}
    failures: List[str] = [name for name in REQUIRED_CHECKS if checks.get(name) is not True]
    return {
        "judge": JUDGE_ID,
        "judge_version": JUDGE_VERSION,
        "proposal_id": proposal.get("id"),
        "admit": not failures,
        "failures": failures,
        "requires_author_approval": True,
    }


def judge_batch(payload: Dict[str, Any]) -> Dict[str, Any]:
    accepted, rejected = [], []
    for proposal in payload.get("proposals", []):
        result = judge_proposal(proposal)
        item = {**proposal, "judgment": result}
        (accepted if result["admit"] else rejected).append(item)
    return {"accepted": accepted, "rejected": rejected, "unresolved": []}
