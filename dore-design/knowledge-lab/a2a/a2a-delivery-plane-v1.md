# A2A Delivery Plane 1.0

Inbound peer mail is independent of the product checkout:

`origin/main coordination path → git object read → isolated durable mailbox → identity/hash validation → dedupe/quarantine → delivery ACK → Doré consumer → separate execution receipt`

## Contract

- Fetch updates only the remote-tracking ref; it never updates, merges, rebases or cleans the product checkout.
- Messages are read with `git ls-tree` and `git show` from an exact source commit.
- `message_id + canonical content SHA-256` is the idempotency identity.
- Same ID/same hash is `REPLAY_DEDUPLICATED`; same ID/different hash is quarantined.
- Delivery ACK is emitted only after atomic durable-mailbox replacement.
- Delivery ACK carries `execution_status=NOT_STARTED`; execution remains owned by the worker.
- Consumer claim atomically advances only execution state to `RECEIVED`; its canonical reply explicitly disclaims task completion.
- The repo inbox remains a compatibility fallback, but the durable inbox wins on duplicate identity.

## Real fixture

`a2a_delivery_plane_acceptance.py` reads peer-review commit `174d0f5a3761f1205bdc390edfc1a95599dc7317` without changing HEAD or dirty files, delivers it once, then proves replay deduplication.
