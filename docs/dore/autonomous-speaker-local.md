# Autonomous Mac mini speaker proof

Run from the Mac mini's existing repository checkout. This reuses the **already running** `dore.a2a/1` Gateway on `127.0.0.1:4312`, capability `design.speaker-cover.render`, consumer `design`.

```sh
python3 scripts/run_dore_speaker_local.py --speaker david-pawson
```

The command creates a unique request ID, sends one **real** A2A render request (`dry_run=false`), and stores the request and gateway JSON result in `local/dore-speaker-runs/<request-id>/`. No ChatGPT connection, paid API, new gateway or manual prompt pasting is required.

For a deliberate replay use `--request-id <same-id>` with unchanged arguments. To validate without rendering use `--dry-run` and a new request ID. The script rejects changing the request body for an existing request ID.

**Important:** This script must execute **on the Mac mini**. Merging GitHub code does not remotely run it, and it does not prove the local image backend exists. It does not publish or automatically approve an image. Review the actual cover against approved olive-and-white typography, identity constraints and editorial quality before any production use.
