# Doré Real Signal Loop 1.0

An official, free, no-key Atom feed enters Newsroom as a provenance-bearing source observation. The connector does not infer publication authority.

`official feed → source observation → canonical event identity → revision ledger → Editorial Gravity → Newsroom/Dawn → review-only draft → resume`

## Contracts

- Transport uses HTTPS and the fail-closed free API gate; no paid fallback or required credential.
- A stable external source ID becomes a canonical `signal_id`; the content hash protects revision integrity.
- Exact replay is deduplicated. Corrections and retractions append a new revision to the same signal.
- An operation is atomically recorded `PREPARED` before work and `COMMITTED` after its result; uncommitted work remains recoverable.
- A draft is never publication: `publishable=false`, `requires_human_editor=true`, and the operation records `published=false`.
- The displaced Loop must resume after each completed Newsroom episode.

## Evidence

- `python3 -m unittest discover -s local/dore-local -p 'test_real_signal_loop.py'`
- `python3 local/dore-local/real_signal_live_acceptance.py`
