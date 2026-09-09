#!/usr/bin/env python3
"""Fixed training-action wrapper for the bounded shadow64 candidate acceptance."""
from __future__ import annotations

import runpy
from pathlib import Path

TARGET = Path(__file__).resolve().with_name("theology-shadow64-candidate.py")

if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
