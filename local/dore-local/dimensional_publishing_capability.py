"""Westside Dimensional Writing & Publishing capability.

Provider-agnostic Core substrate shared by Journal, Dawn, ONE, Doré Folio and book publishing.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any, Callable, Dict, List, Optional

from dimensional_living_corpus import corpus_context
from dimensional_writing_judge import judge_batch
from dimensional_writing_loop import DimensionalWritingLoop

CAPABILITY_ID = "publishing.dimensional-writing"
SCHEMA_VERSION = "1.0"

@dataclass
class EditorialPlan:
    capability: str
    schema_version: str
    title: str
    thesis: str
    manuscript: str
    deep_dive: List[Dict[str, Any]] = field(default_factory=list)
    emergence: List[Dict[str, Any]] = field(default_factory=list)
    sensory: List[Dict[str, Any]] = field(default_factory=list)
    visual: List[Dict[str, Any]] = field(default_factory=list)
    return_lines: List[Dict[str, Any]] = field(default_factory=list)
    surfaces: List[str] = field(default_factory=list)
    publication: Dict[str, Any] = field(default_factory=dict)
    growth: Dict[str, Any] = field(default_factory=dict)
    corpus: Dict[str, Any] = field(default_factory=dict)
    degraded: bool = False

class DimensionalPublishingCapability:
    """Compile a manuscript into a reusable dimensional editorial plan.

    Inference is injected: this module has no provider/browser dependency. The author's
    manuscript and thesis remain authority; generated material may deepen but not silently
    replace them.
    """
    def __init__(
        self,
        infer: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        research: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ):
        self.infer = infer
        self.research = research

    def compile(self, *, title: str, manuscript: str, thesis: str = "", context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = dict(context or {})
        work_id = context.get("work_id")
        corpus: Dict[str, Any] = {}
        if work_id in {"westside:vol00", "westside:vol01"}:
            corpus = corpus_context(work_id)
            context = {**context, **corpus}

        request = {
            "title": title, "thesis": thesis, "manuscript": manuscript, "context": context,
            "movement": ["discover", "excavate", "expand", "make-perceptible", "wander", "plant-return-lines", "converge"],
            "rule": "Every expansion must earn its return; research, media and interaction build reading rather than decorate it.",
            "dimensions": ["original-language", "history", "geography", "reception", "scholarship", "visual-evidence", "audio", "maps", "primary-sources", "counter-reading"],
            "emergence_types": ["person", "work", "concept", "place", "manuscript", "artwork", "related-feature", "source"],
        }
        generated: Dict[str, Any] = {}
        degraded = False
        if self.infer:
            try:
                generated = self.infer(request) or {}
            except Exception:
                degraded = True
        else:
            degraded = True

        growth = DimensionalWritingLoop(
            infer=self.infer,
            research=self.research,
            judge=judge_batch,
        ).run(title=title, manuscript=manuscript, thesis=thesis, context=context)
        degraded = degraded or bool(growth.get("degraded"))

        return asdict(EditorialPlan(
            capability=CAPABILITY_ID, schema_version=SCHEMA_VERSION,
            title=title, thesis=thesis, manuscript=manuscript,
            deep_dive=list(generated.get("deep_dive", [])),
            emergence=list(generated.get("emergence", [])),
            sensory=list(generated.get("sensory", [])),
            visual=list(generated.get("visual", [])),
            return_lines=list(generated.get("return_lines", [])),
            surfaces=["journal", "dawn", "one", "dore-folio", "book"],
            publication={
                "journal_feature": True, "book_ready_pipeline": True,
                "research_collection": True, "image_prompt_discovery": True,
                "contextual_emergence": True, "audio_optional": True, "map_optional": True,
                "growth_mode": "parallel-real-writing" if corpus else "single-work",
            },
            growth=growth,
            corpus=corpus,
            degraded=degraded,
        ))
