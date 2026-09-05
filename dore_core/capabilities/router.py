from __future__ import annotations

import re
from collections import Counter

from .model import RouteDecision, TaskState
from .registry import CapabilityRegistry

_WORD_RE = re.compile(r"[\w.-]+", re.UNICODE)


def _tokens(text: str) -> Counter[str]:
    return Counter(m.group(0).casefold() for m in _WORD_RE.finditer(text))


class SparseCapabilityRouter:
    """Free-first L0/L1 router.

    L0 exact trigger matching runs first. L1 uses a deterministic lexical score
    over compact manifests. No model, embedding service or provider is required.
    A future semantic adapter may be plugged in only for unresolved cases.
    """

    def __init__(self, registry: CapabilityRegistry, *, max_active: int = 3) -> None:
        if max_active < 1:
            raise ValueError("max_active must be >= 1")
        self.registry = registry
        self.max_active = max_active

    def route(self, text: str, *, state: TaskState | None = None) -> RouteDecision:
        query = text.casefold().strip()
        exact: list[str] = []
        for manifest in self.registry.all():
            if any(trigger.casefold() in query for trigger in manifest.triggers):
                exact.append(manifest.id)

        if exact:
            chosen = tuple(exact[: self.max_active])
            decision = RouteDecision(
                intent=query,
                capability_ids=chosen,
                level="L0",
                confidence=1.0,
                reason="deterministic trigger match",
            )
            return self._record(decision, state)

        q = _tokens(query)
        ranked: list[tuple[float, str]] = []
        for manifest in self.registry.all():
            d = _tokens(manifest.searchable_text)
            overlap = sum(min(q[t], d[t]) for t in q)
            if overlap:
                score = overlap / max(1, sum(q.values()))
                ranked.append((score, manifest.id))
        ranked.sort(key=lambda x: (-x[0], x[1]))

        if ranked:
            best = ranked[0][0]
            chosen = tuple(cid for score, cid in ranked if score >= max(0.25, best * 0.6))[: self.max_active]
            decision = RouteDecision(
                intent=query,
                capability_ids=chosen,
                level="L1",
                confidence=min(0.95, best),
                reason="local lexical capability search",
            )
        else:
            decision = RouteDecision(
                intent=query,
                capability_ids=(),
                level="L2_REQUIRED",
                confidence=0.0,
                reason="no cheap route resolved intent",
            )
        return self._record(decision, state)

    @staticmethod
    def _record(decision: RouteDecision, state: TaskState | None) -> RouteDecision:
        if state is not None:
            state.record_route(decision)
            for capability_id in decision.capability_ids:
                state.activate(capability_id)
        return decision
