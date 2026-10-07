import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mg=mod("mgp",Path("scripts/generate_magazine_candidates.py"));ms=mod("msp",Path("scripts/score_magazine_candidates.py"))
def test_candidates_carry_traceable_precedents_into_scoring():
 c=mg.generate("david-pawson","verified")["candidates"]
 assert all(x["precedents"]["evidenceIds"] for x in c)
 out=ms.rank({"candidates":c})
 assert all("referenceQuality" in x["score"]["editorial"] and "lineageFidelity" in x["score"]["editorial"] for x in out["candidates"])
def test_removing_precedents_reduces_reward():
 c=mg.generate("david-pawson","verified")["candidates"][0]
 with_refs=ms.score(c)["score"]["reward"]
 c["precedents"]={"evidenceIds":[],"matchedTokens":[],"items":[]}
 assert ms.score(c)["score"]["reward"] < with_refs
