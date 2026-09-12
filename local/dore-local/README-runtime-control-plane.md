# Doré Runtime Control Plane — Mac relay recovery note

The GitHub issue relay is the authoritative remote handoff for local Design production rollout. A non-main Design rollout must include both `ref` and the exact 40-character `expected_sha`; the local capability creates a detached rollout worktree and fails closed if the fetched ref does not match that SHA.

Current acceptance path:

1. GitHub issue body uses protocol `dore.a2a/1` and capability `design.production.rollout`.
2. The self-hosted macOS relay forwards the request to the local Unix control plane.
3. `production_actions.design_production_rollout` fetches the named ref, verifies `expected_sha`, installs from the detached worktree, then verifies Design 2.0 production health.
4. The issue receives a `DORÉ_LOCAL_RESULT` receipt containing the installed head and resident health evidence.

A GitHub commit or PR head is not considered live until the local result receipt reports the same `head`/`expected_sha` and Design 2.0 health passes.
