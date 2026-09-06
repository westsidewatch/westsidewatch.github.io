# Multiwrite Cover acceptance

The slice is accepted only when production rollout reports PASS and the resident workspace contains `multiwrite-cover`.

Visible contract:
- Pages contains `多寫 · Cover`.
- `/editor?page=multiwrite-cover` renders the cover from structured workspace nodes.
- Cover elements are selectable and draggable; position persists via `set_node`.
- Cover is not a flattened bitmap.
- Frame and local image tools remain available for adding/replacing artwork.
