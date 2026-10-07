import importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location("r",R/"scripts/render_magazine_candidate_review.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_review_exposes_six_ranked_distinct_proposals():
 h=m.render("david-pawson");assert h.count('class="proposal"')==6
 for family in ["full-bleed","asymmetric-split","negative-space","portrait-inset","extreme-crop","typographic-no-portrait"]:assert family in h
 for rank in range(1,7):assert f"#{rank} ·" in h
 assert "EVIDENCE → GEOMETRY → SCORE → RANK" in h
