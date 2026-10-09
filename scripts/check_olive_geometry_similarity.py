#!/usr/bin/env python3
"""Visual silhouette similarity gate using dependency-free SVG path sampling.

Supports the absolute M/L/H/V/Z subset used by the approved abstract gold paths.
Fails closed for unsupported SVG commands. Compare at multiple coarse resolutions
to catch near-duplicates that use different path strings.
"""
import re
from olive_gold_geometry import SHAPES

TOKENS = re.compile(r"[MLHVZmlhvz]|-?(?:\d+(?:\.\d*)?|\.\d+)")
SUPPORTED = set("MLHVZ")

def polygons(path):
    tokens = TOKENS.findall(path)
    residue = TOKENS.sub("", path)
    if residue.strip().replace(",", ""):
        raise ValueError("Unsupported path syntax")
    parts, poly, cursor, start = [], [], (0., 0.), None
    i = 0
    command = None
    while i < len(tokens):
        token = tokens[i]
        if token.isalpha():
            if token not in SUPPORTED:
                raise ValueError("Unsupported SVG command: " + token)
            command = token
            i += 1
            if command == "Z":
                if poly:
                    parts.append(poly)
                    poly = []
                if start is not None:
                    cursor = start
                command = None
            continue
        if command not in ("M", "L", "H", "V"):
            raise ValueError("Missing path command")
        needed = 2 if command in ("M", "L") else 1
        if i + needed > len(tokens) or any(t.isalpha() for t in tokens[i:i+needed]):
            raise ValueError("Incomplete coordinate")
        nums = [float(v) for v in tokens[i:i+needed]]
        i += needed
        if command in ("M", "L"):
            cursor = (nums[0], nums[1])
        elif command == "H":
            cursor = (nums[0], cursor[1])
        else:
            cursor = (cursor[0], nums[0])
        if command == "M":
            if poly:
                parts.append(poly)
            poly = [cursor]
            start = cursor
            command = "L"
        else:
            poly.append(cursor)
    if poly:
        parts.append(poly)
    if not parts or any(len(p) < 3 for p in parts):
        raise ValueError("Degenerate SVG geometry")
    return parts

def contains(poly, x, y):
    inside = False
    for a, b in zip(poly, poly[1:] + poly[:1]):
        if (a[1] > y) != (b[1] > y):
            crossing = (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]
            if x < crossing:
                inside = not inside
    return inside

def mask(path, size=24):
    shapes = polygons(path)
    return frozenset((i,j) for j in range(size) for i in range(size)
        if any(contains(poly, (i+.5)*100/size, (j+.5)*100/size) for poly in shapes))

def similarity(a,b,size=24):
    x,y=mask(a,size),mask(b,size)
    return len(x & y)/len(x | y) if x or y else 1.

def audit(shapes=SHAPES, threshold=.72):
    pairs=[]
    for i in range(len(shapes)):
        for j in range(i+1,len(shapes)):
            a,b=shapes[i],shapes[j]
            score=max(similarity(a[1],b[1],size) for size in (16,24,32))
            pairs.append({"a":a[0],"b":b[0],"iou":round(score,4)})
    failures=[p for p in pairs if p["iou"]>=threshold]
    return {"threshold":threshold,"maxSimilarity":max((p["iou"] for p in pairs),default=0),
            "failures":failures,"pairs":sorted(pairs,key=lambda p:p["iou"],reverse=True)}

if __name__ == "__main__":
    import json
    report=audit()
    print(json.dumps(report,indent=2))
    if report["failures"]:
        raise SystemExit("BLOCKED: visually similar gold geometry")
