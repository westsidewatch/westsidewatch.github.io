import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mod(path,name):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_missing_portrait_production_is_complete_and_safe():
 g=mod("scripts/generate_magazine_candidates.py","g");s=mod("scripts/score_magazine_candidates.py","s");p=mod("scripts/compose_magazine_production.py","p")
 scored=s.rank(g.generate("david-pawson","missing"));profile=g.load(g.PROFILE);out=p.produce(scored,profile)
 assert out["preflight"]["pass"] is True
 assert set(out["variants"])=={"web-hero","speaker-card","mobile","preview-image"}
 assert out["composition"]["identitySynthesis"] is False
 assert "dore-cover" in out["composition"]["html"]
def test_preflight_rejects_black_gold():
 p=mod("scripts/compose_magazine_production.py","p")
 c={"candidate":"x","html":"x","css":"color:#CEBD74;background:#000","identitySynthesis":False}
 assert p.preflight(c,{k:{} for k in p.SURFACES})["pass"] is False
