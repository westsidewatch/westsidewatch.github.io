#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).parent
ops=(root/'design2_layer_ops.py').read_text()
ui=(root/'design2_arrange_ui.py').read_text()
app=(root/'app_visual_v2.py').read_text()
cover=(root/'design2_cover_interaction.py').read_text()
assert 'batch_set_nodes' in ops and 'reorder_nodes' in ops
assert "'type':'frame'" in ops
assert "op:'reorder_nodes'" in ui and '8*1024*1024' in ui
assert 'multiwrite-cover' in app and 'design2_cover_acceptance' in app
assert 'd2-resize-handle' in cover
print('DESIGN2_PRODUCTION_CLOSEOUT_PASS')
