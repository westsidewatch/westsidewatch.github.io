"""Measurement primitives for Doré Context Economy A/B benchmarks."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True)
class ContextRunMetrics:
    task_id: str
    mode: str
    files_read: int = 0
    bytes_read: int = 0
    search_calls: int = 0
    tool_calls: int = 0
    context_bytes: int = 0
    repeated_reads: int = 0
    verification_passed: bool = False
    visual_acceptance: bool | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

def write_metrics(path: Path, metrics: ContextRunMetrics) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def aggregate(runs: Iterable[ContextRunMetrics]) -> dict[str, float]:
    rows = list(runs)
    if not rows:
        return {}
    numeric = ("files_read", "bytes_read", "search_calls", "tool_calls", "context_bytes", "repeated_reads")
    return {key: sum(getattr(row, key) for row in rows) / len(rows) for key in numeric}

def reduction_percent(baseline: float, gated: float) -> float | None:
    if baseline <= 0:
        return None
    return round((baseline - gated) / baseline * 100.0, 2)
