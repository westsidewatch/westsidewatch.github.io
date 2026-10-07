from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_olive_live_surfaces_adopt_magazine_contract():
 carrier=(ROOT/"layouts/olive/surface-carrier.html").read_text(encoding="utf-8")
 js=(ROOT/"olive/olive.js").read_text(encoding="utf-8")
 assert "dore-magazine-card" in carrier
 assert "data.doreSurface='speaker-card'" in carrier
 assert "data.doreIdentitySynthesis='false'" in carrier
 assert "dataset.doreSurface='speaker-card'" in js
 assert "dataset.doreIdentitySynthesis='false'" in js
def test_olive_live_palette_has_no_gold_token():
 for p in ("layouts/olive/surface-carrier.html","olive/index.html","olive/olive.js"):
  text=(ROOT/p).read_text(encoding="utf-8")
  assert "#CEBD74" not in text

def test_all_live_carrier_cards_are_magazine_controlled():
 carrier=(ROOT/"layouts/olive/surface-carrier.html").read_text(encoding="utf-8")
 assert carrier.count('class="olive-speaker-card dore-magazine-card') >= 22
 assert '--dore-type-x' in carrier and '--dore-type-h' in carrier

def test_live_olive_exposes_all_six_magazine_families():
 carrier=(ROOT/"layouts/olive/surface-carrier.html").read_text(encoding="utf-8")
 js=(ROOT/"olive/olive.js").read_text(encoding="utf-8")
 families=("full-bleed","asymmetric-split","negative-space","portrait-inset","extreme-crop","typographic-no-portrait")
 for family in families:
  assert 'data-dore-family="'+family+'"' in carrier
  assert family in js
