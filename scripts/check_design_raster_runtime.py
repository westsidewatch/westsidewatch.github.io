#!/usr/bin/env python3
"""Real Firefox/browser smoke test using the four training snapshots, without inference."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'dore-design'))
import weapon_proficiency as training
import design2_renderer
import design_intelligence_raster as raster
root = Path(sys.argv[1])
results = []
for cid in training.IDS:
    html = design2_renderer.render_snapshot(training.snapshot(cid), edit=False)
    results.append(raster.rasterize_html(html, output=root / (cid + '.png'), width=1440, height=900))
assert len({r['sha256'] for r in results}) == 4
(root / 'manifest.json').write_text(json.dumps(results, indent=2))
print('REAL_BROWSER_RASTER_SMOKE=PASS')
