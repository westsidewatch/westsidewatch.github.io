from pathlib import Path
from dore_core.context.metrics import ContextRunMetrics, aggregate, reduction_percent, write_metrics

def test_metrics_are_serializable(tmp_path: Path):
    metric = ContextRunMetrics("ui-001", "baseline", files_read=10, bytes_read=1000)
    target = tmp_path / "run.json"
    write_metrics(target, metric)
    assert '"task_id": "ui-001"' in target.read_text(encoding="utf-8")

def test_aggregate_and_reduction():
    rows = [
        ContextRunMetrics("a", "baseline", files_read=10, context_bytes=1000),
        ContextRunMetrics("b", "baseline", files_read=20, context_bytes=3000),
    ]
    totals = aggregate(rows)
    assert totals["files_read"] == 15
    assert totals["context_bytes"] == 2000
    assert reduction_percent(2000, 800) == 60.0
    assert reduction_percent(0, 0) is None
