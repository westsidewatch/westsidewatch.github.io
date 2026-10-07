#!/usr/bin/env python3
"""Fail closed when the published Olive composition runtime is stale."""
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/"scripts/build_olive_magazine_runtime.py"
RUNTIME=ROOT/"static/dore-design/runtime/olive-speaker-compositions.v1.json"
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
 expected=module(BUILD,"olive_runtime_builder").build()
 actual=json.loads(RUNTIME.read_text(encoding="utf-8"))
 if actual!=expected:
  print("STALE: Olive magazine runtime does not match current Doré scoring authority")
  return 1
 print("PASS: Olive magazine runtime matches current Doré scoring authority")
 return 0
if __name__=="__main__":raise SystemExit(main())
