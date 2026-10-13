import importlib.util
from pathlib import Path

R = Path(__file__).resolve().parents[1]
s = importlib.util.spec_from_file_location("g", R / "scripts/generate_magazine_candidates.py")
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)


def test_evidence_drives_geometry():
    a = m.generate("david-pawson", "verified")
    b = m.generate("david-pawson", "verified")
    assert a == b
    assert all(x["precedents"]["evidenceIds"] for x in a["candidates"])
    assert any(x["geometryAuthority"]["operations"] for x in a["candidates"])
