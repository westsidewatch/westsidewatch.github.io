from pathlib import Path

from dore_core.context.economy import (
    ContextBudget,
    bounded_working_set,
    fingerprint,
    needs_invalidation,
)


def test_working_set_is_bounded(tmp_path: Path):
    paths = []
    for i in range(5):
        p = tmp_path / f"{i}.txt"
        p.write_text("x" * 10, encoding="utf-8")
        paths.append(p)
    decision = bounded_working_set("ui", "upgrade", paths, budget=ContextBudget(max_files=2, max_bytes=100))
    assert len(decision.evidence) == 2
    assert decision.insufficient is False


def test_empty_context_fails_closed():
    decision = bounded_working_set("ui", "upgrade", [])
    assert decision.insufficient is True


def test_fingerprint_invalidates_changed_evidence(tmp_path: Path):
    p = tmp_path / "ui.css"
    p.write_text("a", encoding="utf-8")
    cached = fingerprint(p)
    assert needs_invalidation(cached, p) is False
    p.write_text("b", encoding="utf-8")
    assert needs_invalidation(cached, p) is True
