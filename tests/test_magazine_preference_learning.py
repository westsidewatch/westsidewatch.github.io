import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,R/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
rp=mod("rp",Path("scripts/record_magazine_preference.py"));sc=mod("sc",Path("scripts/score_magazine_candidates.py"))
def test_preference_record_is_normalized_and_deduplicated():
 d={"records":[]};rp.record(d,"david-pawson","negative-space",["full-bleed"],{"negative_space":1});rp.record(d,"david-pawson","negative-space",["full-bleed"],{"negative_space":1});assert len(d["records"])==1
def test_preference_dimension_is_part_of_editorial_score():
 c={"family":"negative-space","geometry":{"image":[56,14,36,72],"type":[7,12,39,54]},"assetPolicy":{"portrait":"verified"},"content":{"speaker":"david-pawson"},"precedents":{"items":[],"matchedTokens":[]}}
 assert "humanPreference" in sc.score(c)["score"]["editorial"]
