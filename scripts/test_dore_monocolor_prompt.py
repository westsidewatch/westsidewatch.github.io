#!/usr/bin/env python3
"""Contract tests for Doré mono-color prompt compiler."""
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("mono",ROOT/"scripts/compile_dore_monocolor_prompt.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def test():
    doc=mod.compile_prompt("Ancient stone gate","敬畏耶和華是智慧的開端")
    p=doc["generationPrompt"];r=doc["recipe"]
    assert "敬畏耶和華是智慧的開端" in p
    assert "#174B35" in p and "#FFFFFF" in p
    assert "#CEBD74" not in p
    assert "crosshatching" in p
    assert r["publishAllowed"] is False and r["state"]=="PROMPT_READY_NOT_RENDERED"
    assert "No invented identity portraits" in r["constraints"]
    try:mod.compile_prompt("x","",section="unknown")
    except ValueError:pass
    else:raise AssertionError("unapproved section accepted")
    try:mod.compile_prompt("x","",ratio="17:1")
    except ValueError:pass
    else:raise AssertionError("unapproved ratio accepted")
    print("PASS: mono-color prompt contract")
if __name__=="__main__":test()
