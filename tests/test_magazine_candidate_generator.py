import importlib.util
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"scripts"/"generate_magazine_candidates.py"
spec=importlib.util.spec_from_file_location("mg",P); mg=importlib.util.module_from_spec(spec); spec.loader.exec_module(mg)

def test_missing_portrait_fails_to_typographic_only():
 out=mg.generate("jiang-xiuqin","missing")
 assert out["candidateCount"]==1
 assert out["candidates"][0]["family"]=="typographic-no-portrait"
 assert out["candidates"][0]["assetPolicy"]["identitySynthesis"] is False

def test_verified_portrait_produces_distinct_deterministic_families():
 a=mg.generate("jiang-xiuqin","verified"); b=mg.generate("jiang-xiuqin","verified")
 assert a==b and a["candidateCount"]==6
 assert len({x["family"] for x in a["candidates"]})==6
 assert len({x["id"] for x in a["candidates"]})==6
