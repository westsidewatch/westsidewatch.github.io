import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/"scripts/retrieve_editorial_precedents.py"
s=importlib.util.spec_from_file_location("r",P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_retrieval_returns_traceable_real_evidence():
 for family in m.FAMILY_HINTS:
  rows=m.retrieve(family)
  assert rows, family
  assert all(x["id"] and x["source"] and x["authority"] for x in rows)
def test_retrieval_is_deterministic():
 assert m.retrieve("typographic-no-portrait")==m.retrieve("typographic-no-portrait")
