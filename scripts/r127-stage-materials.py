import json,shutil
from pathlib import Path
src=Path("artifacts/r124/r127-originals")
dst=Path("static/experiments/seven-realm-r124/materials/r127");dst.mkdir(parents=True,exist_ok=True)
rows=json.loads((src/"report.json").read_text())
for r in rows:
 if r["state"]=="native_original_acquired_pending_visual_and_rights_review":shutil.copyfile(src/(r["id"]+".svg"),dst/(r["id"]+".svg"))
(dst/"report.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n")
