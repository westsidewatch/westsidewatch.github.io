from pathlib import Path
from dore_core.context.tool_economy import (
    VerifiedState, browser_text_budget, can_reuse_verified, compress_output, fingerprint_inputs
)

def test_large_output_keeps_head_tail_and_reports_omission():
    text = "HEAD\n" + ("x" * 30000) + "\nTAIL"
    result = compress_output(text, max_bytes=1000)
    assert result.original_bytes > 1000
    assert result.omitted_bytes > 0
    assert "HEAD" in result.head
    assert "TAIL" in result.tail

def test_verified_state_reuse_requires_unchanged_inputs(tmp_path: Path):
    p = tmp_path / "ui.css"
    p.write_text("a", encoding="utf-8")
    state = VerifiedState("ui", fingerprint_inputs([p]), "build+visual", True)
    assert can_reuse_verified(state, [p])
    p.write_text("b", encoding="utf-8")
    assert not can_reuse_verified(state, [p])

def test_failed_verification_is_never_reused(tmp_path: Path):
    p = tmp_path / "ui.css"
    p.write_text("a", encoding="utf-8")
    state = VerifiedState("ui", fingerprint_inputs([p]), "build", False)
    assert not can_reuse_verified(state, [p])

def test_browser_context_is_bounded():
    result = browser_text_budget("z" * 50000, max_bytes=2000)
    assert result.omitted_bytes > 0
