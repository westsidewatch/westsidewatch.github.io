# Design 2.0 — Direct Manipulation Slice

Status: implemented for `multiwrite-home`.

This slice makes the canvas itself editable rather than treating the iframe as preview-only.

Implemented:
- direct click selection on all workspace nodes
- visible selection box
- four corner resize handles
- pointer drag to reposition
- pointer resize to change width/height
- arrow-key nudging; Shift+arrow = 10 px
- every completed manipulation writes back through the existing `set_node` workspace operation
- same structured workspace remains source of truth
- no new third-party runtime dependency

This deliberately absorbs the interaction model learned from mature editor primitives such as Moveable without making Doré depend on a heavyweight embedded editor. The current implementation is a Doré-native primitive and can later gain snapping, guides, multi-selection, rotation and constraints.
