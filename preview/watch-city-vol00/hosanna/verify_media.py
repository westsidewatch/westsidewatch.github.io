#!/usr/bin/env python3
"""Fail publication when Hosanna's publishable sequence points at missing local media."""
from pathlib import Path
import json, sys

HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/"sequence.json").read_text(encoding="utf-8"))
missing=[]
checked=0
for moment in manifest.get("moments",[]):
    if moment.get("rightsState")!="publishable" or not moment.get("asset"):
        continue
    asset=str(moment["asset"])
    if not asset.startswith("/preview/watch-city-vol00/hosanna/"):
        continue
    rel=asset.split("/preview/watch-city-vol00/hosanna/",1)[1].split("?",1)[0]
    checked+=1
    if not (HERE/rel).is_file():
        missing.append({"id":moment.get("id"),"asset":asset})
master=manifest.get("master",{})
asset=master.get("image")
if asset and str(asset).startswith("/preview/watch-city-vol00/hosanna/"):
    rel=str(asset).split("/preview/watch-city-vol00/hosanna/",1)[1].split("?",1)[0]
    checked+=1
    if not (HERE/rel).is_file():
        missing.append({"id":"master","asset":asset})
if missing:
    print(json.dumps({"ok":False,"checked":checked,"missing":missing},ensure_ascii=False,indent=2))
    sys.exit(1)
print(json.dumps({"ok":True,"checked":checked,"missing":[]},ensure_ascii=False))
