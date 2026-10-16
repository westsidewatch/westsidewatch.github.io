#!/usr/bin/env python3
import importlib.util,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("engraving",root/"scripts/dore_engraving.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
for subject in ("architecture","sphere","landscape","drapery"):
 for style in ("parallel","cross","wood"):
  a=m.render(subject,style);b=m.render(subject,style)
  assert a==b and "<svg" in a and a.count("<path")>10
  assert "#CEBD74" not in a and "#174B35" in a
try:m.render("unknown")
except ValueError:pass
else:raise AssertionError("invalid subject not rejected")
print("PASS 12 deterministic engraving render combinations")
