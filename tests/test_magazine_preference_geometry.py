import importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location("g",R/"scripts/generate_magazine_candidates.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_preference_mutation_changes_geometry():
 g={"image":[50,10,40,70],"type":[7,12,40,60]};x,ops=m.pref_mutate(g,{"negative_space":1,"portrait_scale":-1,"type_scale":-1,"name_alignment":"left"});assert x!=g;assert len(ops)==4
def test_candidates_expose_preference_authority():
 rows=m.generate("david-pawson","verified")["candidates"];assert all("preferenceAuthority" in x for x in rows)
