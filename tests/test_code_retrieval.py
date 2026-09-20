from pathlib import Path
from dore_core.context.code_retrieval import candidate_files, retrieve_code

def test_retrieval_prefers_symbol_match(tmp_path: Path):
    strong = tmp_path / "motion.py"
    weak = tmp_path / "notes.md"
    strong.write_text("def timeline_transition():\n    return 'motion'\n", encoding="utf-8")
    weak.write_text("timeline notes about motion", encoding="utf-8")
    hits = retrieve_code("timeline transition", [weak, strong], limit=2)
    assert hits[0].path.endswith("motion.py")
    assert "timeline_transition" in hits[0].symbols

def test_retrieval_returns_bounded_excerpt(tmp_path: Path):
    p = tmp_path / "large.js"
    p.write_text("const targetMotion = 1;\n" + ("x" * 10000), encoding="utf-8")
    hit = retrieve_code("target motion", [p], limit=1, excerpt_chars=500)[0]
    assert len(hit.excerpt) <= 500

def test_no_implicit_repository_walk(tmp_path: Path):
    (tmp_path / "secret.py").write_text("def hidden(): pass", encoding="utf-8")
    assert candidate_files(tmp_path) == []
