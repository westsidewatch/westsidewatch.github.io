#!/usr/bin/env python3
"""Deterministic, collision-checked two-ink geometry for Olive Mountain covers.

Layout families and scores remain owned by Doré Magazine Engine. This module
only assigns a series-distinct background silhouette, never a person's likeness.
"""
import json
from pathlib import Path

PAPER = "#FAF9F5"
OLIVE = "#738A5A"
GOLD = "#CEBD74"

# Normalized 0..100 coordinates. Each entry differs in silhouette AND placement.
# Abstract forms only; biography-specific representational motifs require verification.
SHAPES = [
    ("corner-notch", "M0 9 H36 V24 H23 V38 H0Z", "upper-left", "stepped"),
    ("lower-band", "M0 77 H67 V92 H43 V100 H0Z", "lower-left", "horizontal"),
    ("open-chevron", "M0 28 L29 10 L47 24 L18 43 L0 43Z", "upper-left", "chevron"),
    ("side-terrace", "M73 35 H100 V72 H88 V59 H73Z", "middle-right", "stepped"),
    ("offset-islands", "M3 58 H25 V67 H3Z M31 72 H59 V81 H31Z", "lower-left", "islands"),
    ("top-shelf", "M43 0 H100 V13 H70 V24 H43Z", "upper-right", "horizontal"),
    ("bottom-corner", "M66 100 V73 H84 V86 H100 V100Z", "lower-right", "stepped"),
    ("fork", "M0 54 H38 V62 H19 V87 H9 V62 H0Z", "middle-left", "fork"),
    ("open-frame", "M57 4 H95 V13 H68 V42 H57Z", "upper-right", "frame"),
    ("staggered-bars", "M5 73 H37 V80 H5Z M14 84 H48 V91 H14Z", "lower-left", "horizontal"),
    ("cut-corner", "M72 0 H100 V34 H88 L72 17Z", "upper-right", "diagonal"),
    ("short-crossbar", "M45 56 H100 V63 H76 V76 H65 V63 H45Z", "middle-right", "fork"),
]

def assign(slugs):
    if len(slugs) > len(SHAPES):
        raise ValueError("Not enough unique geometry identities")
    if len(set(slugs)) != len(slugs):
        raise ValueError("Duplicate speaker")
    records = []
    for slug, (identity, path, region, vocabulary) in zip(slugs, SHAPES):
        records.append({
            "speaker": slug,
            "identity": identity,
            "goldPath": path,
            "region": region,
            "vocabulary": vocabulary,
            "oliveAccent": "one sparse secondary field only",
            "palette": {"paper": PAPER, "portrait": OLIVE, "geometry": GOLD},
            "biographicalMotif": "requires-verified-person-specific-evidence",
        })
    validate(records)
    return records

def validate(records):
    keys = ("identity", "goldPath")
    for key in keys:
        if len({r[key] for r in records}) != len(records):
            raise ValueError("Duplicate " + key)
    if any(r["palette"] != {"paper": PAPER, "portrait": OLIVE, "geometry": GOLD} for r in records):
        raise ValueError("Incorrect color separation")
    if len({(r["region"], r["vocabulary"]) for r in records}) < min(8, len(records)):
        raise ValueError("Insufficient geometric variety")
    return True

def enrich(selection):
    records = selection["records"]
    geometries = assign([r["speaker"] for r in records])
    return {
        **selection,
        "schema": "dore.olive-series-diversity.v2",
        "geometryPolicy": "unique silhouette + region + vocabulary; 2-ink; no portrait synthesis",
        "records": [{**r, "goldGeometry": g} for r, g in zip(records, geometries)],
    }
