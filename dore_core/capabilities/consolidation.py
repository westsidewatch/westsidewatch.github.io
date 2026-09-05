from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from json import dumps
from typing import Iterable

from .executor import ExecutionResult
from .model import TaskState


def _hash(value: object) -> str:
    raw = dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)
    return sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ExecutionEvidence:
    capability_id: str
    ok: bool
    input_schemas: tuple[str, ...]
    output_schemas: tuple[str, ...]
    route_level: str | None
    provider_activations: int
    failure: str | None
    fingerprint: str


@dataclass(frozen=True)
class CapabilityCandidate:
    capability_id: str
    fingerprint: str
    successful_runs: int
    failed_runs: int
    status: str
    reason: str
    target_level: str


@dataclass
class ConsolidationLedger:
    """Offline evidence ledger for Doré capability maturation.

    This object never mutates the production registry or reflex router. It only
    emits candidates after repeated compatible evidence. Promotion remains a
    separate regression-gated action.
    """

    evidence: list[ExecutionEvidence] = field(default_factory=list)

    def record(self, result: ExecutionResult, state: TaskState) -> ExecutionEvidence:
        output_schemas = tuple(artifact.schema for artifact in result.output_artifacts)
        route_level = state.route_history[-1].level if state.route_history else None
        input_schemas = tuple(sorted({artifact.schema for artifact in state.artifacts.values()} - set(output_schemas)))
        shape = {
            "capability_id": result.capability_id,
            "ok": result.ok,
            "input_schemas": input_schemas,
            "output_schemas": output_schemas,
            "route_level": route_level,
        }
        item = ExecutionEvidence(
            capability_id=result.capability_id,
            ok=result.ok,
            input_schemas=input_schemas,
            output_schemas=output_schemas,
            route_level=route_level,
            provider_activations=int(state.telemetry.get("provider_activations", 0)),
            failure=result.error,
            fingerprint=_hash(shape),
        )
        self.evidence.append(item)
        return item

    def candidate(
        self,
        capability_id: str,
        *,
        min_successes: int = 3,
        target_level: str = "L1",
    ) -> CapabilityCandidate | None:
        rows = [item for item in self.evidence if item.capability_id == capability_id]
        if not rows:
            return None
        groups: dict[str, list[ExecutionEvidence]] = {}
        for row in rows:
            groups.setdefault(row.fingerprint, []).append(row)
        fingerprint, strongest = max(groups.items(), key=lambda pair: sum(1 for x in pair[1] if x.ok))
        successes = sum(1 for x in strongest if x.ok)
        failures = sum(1 for x in strongest if not x.ok)
        if failures:
            return CapabilityCandidate(
                capability_id, fingerprint, successes, failures, "BLOCKED",
                "matching execution shape contains failures; regression evidence required before promotion",
                target_level,
            )
        if successes < min_successes:
            return CapabilityCandidate(
                capability_id, fingerprint, successes, failures, "INSUFFICIENT_EVIDENCE",
                f"requires at least {min_successes} compatible successful runs",
                target_level,
            )
        return CapabilityCandidate(
            capability_id, fingerprint, successes, failures, "REGRESSION_REQUIRED",
            "repeated compatible success qualifies for candidate evaluation; production promotion is not automatic",
            target_level,
        )

    def candidates(self, *, min_successes: int = 3, target_level: str = "L1") -> tuple[CapabilityCandidate, ...]:
        ids = sorted({item.capability_id for item in self.evidence})
        return tuple(
            candidate
            for cid in ids
            if (candidate := self.candidate(cid, min_successes=min_successes, target_level=target_level)) is not None
        )
