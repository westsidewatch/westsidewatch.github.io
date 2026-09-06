#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ops=(ROOT/'design2_layer_ops.py').read_text()
ui=(ROOT/'design2_arrange_ui.py').read_text()
bridge=(ROOT/'design2_canvas_state.py').read_text()
for token in ('align_nodes','center_nodes','distribute_nodes','stack_nodes','group_nodes','ungroup_nodes','reorder_node'):
    assert token in ops,token
for token in ('Center canvas','Distribute','Gap','Bring front','Forward','Backward','Send back','Group','Ungroup'):
    assert token in ui,token
assert 'payload={...m' in bridge
print('PASS design2 complete arrange contract')
