from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional

CAPABILITY_ID = "publishing.dimensional-writing"
LOOP_VERSION = "0.1"

STAGES = (
    "understand",
    "find-center",
    "detect-gaps",
    "choose-dimensions",
    "excavate",
    "make-perceptible",
    "propose",
    "judge",
    "return",
    "reread",
)


@dataclass
class LoopResult:
    capability: str
    loop_version: str
    title: str
    thesis: str
    manuscript: str
    stages: List[Dict[str, Any]] = field(default_factory=list)
    proposals: List[Dict[str, Any]] = field(default_factory=list)
    accepted_candidates: List[Dict[str, Any]] = field(default_factory=list)
    rejected_candidates: List[Dict[str, Any]] = field(default_factory=list)
    unresolved: List[Dict[str, Any]] = field(default_factory=list)
    degraded: bool = False


class DimensionalWritingLoop:
    def __init__(
        self,
        infer: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        research: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        judge: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ):
        self.infer = infer
        self.research = research
        self.judge = judge

    def run(
        self,
        *,
        title: str,
        manuscript: str,
        thesis: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        context = context or {}
        state: Dict[str, Any] = {
            "title": title,
            "thesis": thesis,
            "manuscript": manuscript,
            "context": context,
            "author_authority": True,
            "may_rewrite_thesis": False,
        }
        stages: List[Dict[str, Any]] = []
        degraded = False
        generated: Dict[str, Any] = {}

        if self.infer:
            try:
                generated = self.infer(
                    {
                        **state,
                        "stages": list(STAGES),
                        "instruction": (
                            "Develop the manuscript dimensionally. Select only dimensions that deepen the thesis; "
                            "every excursion must name its return line. Preserve author thesis and textual authority."
                        ),
                    }
                ) or {}
            except Exception as exc:
                degraded = True
                stages.append({"stage": "infer", "status": "degraded", "error": type(exc).__name__})
        else:
            degraded = True
            stages.append({"stage": "infer", "status": "unavailable"})

        research_result: Dict[str, Any] = {}
        research_requests = list(generated.get("research_requests", []))
        if research_requests and self.research:
            try:
                research_result = self.research({**state, "requests": research_requests}) or {}
            except Exception as exc:
                degraded = True
                stages.append({"stage": "excavate", "status": "degraded", "error": type(exc).__name__})

        proposals = list(generated.get("proposals", []))
        judgment: Dict[str, Any] = {}
        if self.judge and proposals:
            try:
                judgment = self.judge({**state, "proposals": proposals, "research": research_result}) or {}
            except Exception as exc:
                degraded = True
                stages.append({"stage": "judge", "status": "degraded", "error": type(exc).__name__})

        accepted = list(judgment.get("accepted", []))
        rejected = list(judgment.get("rejected", []))
        unresolved = list(judgment.get("unresolved", proposals if not judgment else []))
        stages.extend(list(generated.get("stage_evidence", [])))

        return asdict(
            LoopResult(
                capability=CAPABILITY_ID,
                loop_version=LOOP_VERSION,
                title=title,
                thesis=thesis,
                manuscript=manuscript,
                stages=stages,
                proposals=proposals,
                accepted_candidates=accepted,
                rejected_candidates=rejected,
                unresolved=unresolved,
                degraded=degraded,
            )
        )
