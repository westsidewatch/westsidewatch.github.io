# Doré Multi-Loop Agency 1.0

Agent Core owns this policy; Resident Runtime only wakes it.

`Observe → Evaluate Progress → Prioritize → Route → Yield → Resume → Learn`

## Invariants

- Execution success is not goal success.
- Repeated activity is not progress.
- Progress requires positive goal delta, positive evidence delta, a repaired failed gate, or a newly observed peer reply.
- A peer request remains non-blocking. With no reply and no evidence delta it enters exponential cooldown instead of being re-queued on every wake.
- A measured local repair gap outranks broad research. For the first acceptance, `RESPONSIVE_PASS=false` routes to `LOCAL_RESPONSIVE_REPAIR` before reference expansion.
- Fixing responsive evidence does not complete the parent goal while qualified references or source families remain below their thresholds.

The persisted checkpoint is `~/.dore/agency/<goal_id>.json`. It contains the normalized goal/evidence/peer snapshot, material deltas, stall count, selected route, and peer cooldown.
