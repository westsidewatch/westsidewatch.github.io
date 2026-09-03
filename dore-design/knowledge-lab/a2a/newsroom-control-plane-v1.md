# Doré Newsroom → Multi-Loop Control Plane 1.0

Newsroom is an event-driven Living Loop, not a permanently spinning daemon.

`verified WorldSignal → Editorial Gravity → wake/pre-empt → reuse Dawn assets → targeted enrichment only for gaps → prayer + report drafts → human editorial review → resume prior work`

## Boundaries

- A signal without publisher-and-URL provenance is rejected before routing.
- Popularity is not an Editorial Gravity input and cannot cause pre-emption.
- Newsroom reuses provenance-preserving KnowledgeAssets before enrichment.
- Dawn enrichment is delta-only and is woken only when named topic gaps remain.
- Outputs are drafts with `publishable=false` and `requires_human_editor=true`.
- A2A remains a capability-recovery path, not a peer business Loop.
- Completing a Newsroom episode resumes the checkpointed lower-priority workflow.

## Executable evidence

- `python3 local/dore-local/test_newsroom_control_plane.py`
- `python3 local/dore-local/newsroom_control_plane_acceptance.py`
