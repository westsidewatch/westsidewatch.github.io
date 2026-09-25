#!/usr/bin/env python3
"""Jerusalem 3000 canonical DEM ingest wrapper.

Input must be a locally obtained, licensed Copernicus DEM GeoTIFF covering the
canonical Jerusalem AOI. This script intentionally performs no authentication
and stores no credentials. It delegates validation and mesh generation to the
existing build_terrain_mesh.py pipeline.
"""
import subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv) not in (2,3):
    raise SystemExit('usage: ingest_jerusalem_dem.py INPUT.tif [OUTPUT.json]')
src=Path(sys.argv[1]).expanduser().resolve()
out=Path(sys.argv[2]).expanduser().resolve() if len(sys.argv)==3 else ROOT/'preview/jerusalem-3000/data/terrain/jerusalem-real.mesh.json'
if not src.is_file():
    raise SystemExit(f'DEM input not found: {src}')
out.parent.mkdir(parents=True,exist_ok=True)
subprocess.run([sys.executable,str(ROOT/'scripts/build_terrain_mesh.py'),str(src),str(out)],check=True)
print(f'J3K_REAL_TERRAIN=BUILT input={src.name} output={out}')
