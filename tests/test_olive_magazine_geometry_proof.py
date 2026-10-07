import importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location("p",R/"scripts/render_olive_magazine_proof.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_proof_uses_candidate_geometry_and_lineage():
 h=m.render();assert h.count('class="cover"')==12;assert 'style="left:' in h;assert "EVIDENCE-DRIVEN GEOMETRY" in h;assert "BASE GEOMETRY" in h or "asymmetrical hierarchy" in h
