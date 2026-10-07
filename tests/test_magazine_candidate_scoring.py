import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mod(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
mg=mod("mg",Path("scripts/generate_magazine_candidates.py"))
ms=mod("ms",Path("scripts/score_magazine_candidates.py"))

def test_candidates_are_ranked_and_repeatable():
 a=ms.rank(mg.generate("jiang-xiuqin","verified"));b=ms.rank(mg.generate("jiang-xiuqin","verified"))
 assert a==b and a["winner"]
 assert [x["rank"] for x in a["candidates"]]==list(range(1,7))
 assert all(x["scoreState"]=="scored" for x in a["candidates"])

def test_missing_portrait_fallback_passes_hard_gate():
 out=ms.rank(mg.generate("jiang-xiuqin","missing"))
 assert out["candidates"][0]["family"]=="typographic-no-portrait"
 assert out["candidates"][0]["score"]["hardPass"]

def test_missing_portrait_with_image_fails_closed():
 c=mg.generate("jiang-xiuqin","verified")["candidates"][0]
 c["assetPolicy"]["portrait"]="missing"
 assert ms.score(c)["score"]["hardPass"] is False
