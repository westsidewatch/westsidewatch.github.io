#!/usr/bin/env python3
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUTH=json.loads((ROOT/"preview/jerusalem-3000/data/terrain-authority.json").read_text())
LEDGER=json.loads((ROOT/"preview/jerusalem-3000/data/objects/herodian-30ce.json").read_text())
o=AUTH["coordinateSystem"]["origin"]; lat0=math.radians(o["lat"]); lon0=math.radians(o["lon"]); R=6378137.0
errors=[]
for obj in LEDGER["objects"]:
 s=obj.get("spatial") or {}; a=s.get("anchor"); enu=s.get("enuMetres")
 if not a:
  if s.get("registration")!="withheld": errors.append(f'{obj["id"]}: missing anchor must be withheld')
  continue
 east=(math.radians(a["lon"])-lon0)*math.cos(lat0)*R
 north=(math.radians(a["lat"])-lat0)*R
 if not enu: errors.append(f'{obj["id"]}: missing ENU'); continue
 if abs(enu["east"]-east)>.5 or abs(enu["north"]-north)>.5: errors.append(f'{obj["id"]}: ENU drift')
 if not (AUTH["areaOfInterest"]["west"]<=a["lon"]<=AUTH["areaOfInterest"]["east"] and AUTH["areaOfInterest"]["south"]<=a["lat"]<=AUTH["areaOfInterest"]["north"]): errors.append(f'{obj["id"]}: outside AOI')
 if enu.get("up") is not None: errors.append(f'{obj["id"]}: up must remain null before DEM ingest')
if errors:
 print("\n".join(errors)); raise SystemExit(1)
print(f'J3K_HERODIAN_REGISTRATION=PASS objects={len(LEDGER["objects"])}')
