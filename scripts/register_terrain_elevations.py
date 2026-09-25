#!/usr/bin/env python3
"""Register Jerusalem 3000 object elevations against the canonical terrain mesh.

Usage:
  python3 scripts/register_terrain_elevations.py terrain-mesh.json objects.json output.json

The script never invents elevation. It samples the nearest valid terrain vertex
in the same local ENU frame and records sampling provenance on each object.
"""
import copy, json, math, sys


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def nearest_height(vertices, east, north):
    best = None
    for v in vertices:
        if v is None:
            continue
        de = v[0] - east
        dn = v[2] - north
        d2 = de * de + dn * dn
        if best is None or d2 < best[0]:
            best = (d2, v[1])
    if best is None:
        raise ValueError("terrain mesh has no valid vertices")
    return best[1], math.sqrt(best[0])


def main(mesh_path, ledger_path, output_path):
    mesh = load(mesh_path)
    ledger = load(ledger_path)
    out = copy.deepcopy(ledger)
    if mesh.get("schema") != "j3k-terrain-mesh-v1":
        raise SystemExit("unsupported terrain schema")
    for obj in out.get("objects", []):
        spatial = obj.get("spatial") or {}
        enu = spatial.get("enuMetres")
        if not enu:
            continue
        height, distance = nearest_height(mesh["vertices"], enu["east"], enu["north"])
        enu["up"] = round(height, 3)
        spatial["elevationRegistration"] = {
            "method": "nearest-canonical-terrain-vertex",
            "meshSchema": mesh["schema"],
            "sampleDistanceMetres": round(distance, 3),
            "authority": "canonical-terrain-mesh"
        }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"registered terrain elevations -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: register_terrain_elevations.py terrain-mesh.json objects.json output.json")
    main(*sys.argv[1:])
