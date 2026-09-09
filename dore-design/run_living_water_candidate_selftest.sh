#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 living_water_candidate_selftest.py
python3 -m py_compile living_water_candidate.py app_visual_v2.py
