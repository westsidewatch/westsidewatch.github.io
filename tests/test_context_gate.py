from pathlib import Path
import pytest
from dore_core.context.gate import ui_context, ui_expand, tool_context

def test_gate_returns_bounded_ranked_context(tmp_path: Path):
    p = tmp_path / "cinema.py"
    p.write_text("def chronology_transition():\n    return 'motion'\n", encoding="utf-8")
    result = ui_context("cinema", "chronology transition", [p])
    assert len(result.admission.evidence) == 1
    assert result.code
    assert "chronology_transition" in result.code[0].symbols

def test_expansion_requires_reason(tmp_path: Path):
    with pytest.raises(ValueError):
        ui_expand("ui", "task", [], reason="")

def test_tool_context_is_bounded():
    digest = tool_context("x" * 50000, max_bytes=1000)
    assert digest.omitted_bytes > 0
