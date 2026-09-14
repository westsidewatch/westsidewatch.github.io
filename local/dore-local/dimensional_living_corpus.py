from dataclasses import asdict, dataclass
from typing import Any, Dict, List

CORPUS_SCHEMA = "dore.dimensional-living-corpus.v0"

@dataclass(frozen=True)
class LivingWork:
    work_id: str
    volume: str
    title: str
    temporal_order: int
    role: str
    active: bool = True

WORKS = [
    LivingWork("westside:vol00", "Vol.00", "Watch, A City of Light", 0, "earlier-timeline parallel cultivation"),
    LivingWork("westside:vol01", "Vol.01", "The Shadow of the Cross", 1, "parallel capability-driving work"),
]

def default_corpus() -> Dict[str, Any]:
    return {
        "schema": CORPUS_SCHEMA,
        "growth_mode": "parallel-real-writing",
        "do_not_wait_for_completion": True,
        "works": [asdict(work) for work in WORKS],
        "baseline_pairs": [
            {"source": "westside:vol00", "compare_with": "westside:vol01"},
            {"source": "westside:vol01", "compare_with": "westside:vol00"},
        ],
    }

def corpus_context(work_id: str) -> Dict[str, Any]:
    corpus = default_corpus()
    current = next((work for work in corpus["works"] if work["work_id"] == work_id), None)
    if current is None:
        raise ValueError("unknown living-corpus work")
    peers: List[Dict[str, Any]] = [work for work in corpus["works"] if work["work_id"] != work_id and work["active"]]
    return {"living_corpus": corpus, "current_work": current, "parallel_peers": peers}
