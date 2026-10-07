#!/usr/bin/env python3
"""Acceptance checks for Doré Video Master and its loopback bridge wiring."""
from pathlib import Path
import ast, json

ROOT=Path(__file__).resolve().parents[2]
MASTER=ROOT/"dore-core/tools/video_master.py"
BRIDGE=ROOT/"local/dore-local/video_bridge.py"
CONTRACT=ROOT/"dore-core/contracts/video-master-v0.json"

def main():
    ast.parse(MASTER.read_text(encoding="utf-8"))
    ast.parse(BRIDGE.read_text(encoding="utf-8"))
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["capability"]=="video-master"
    m=MASTER.read_text(encoding="utf-8")
    b=BRIDGE.read_text(encoding="utf-8")
    for token in ("quality_gate","blackdetect","freezedetect","avg_frame_rate","restore"):
        assert token in m, token
    for token in ("master-probe","restore","auto_master","mastering","mastered","master_failed"):
        assert token in b, token
    print("Doré Video Master acceptance: PASS")

if __name__=="__main__": main()
