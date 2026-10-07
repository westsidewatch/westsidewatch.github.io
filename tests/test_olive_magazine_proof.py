import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts/render_olive_magazine_proof.py"
s=importlib.util.spec_from_file_location("proof",P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_proof_is_generated_from_all_canonical_speakers():
 h=m.render()
 assert h.count('class="cover"')==12
 for x in ["大衛鮑森","江秀琴","倪柝聲","唐崇榮","黃淑華"]: assert x in h
 assert "NO PORTRAIT" in h
