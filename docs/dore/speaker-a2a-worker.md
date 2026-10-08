# Doré speaker cover — A2A local worker contract

## Status

The worker entrypoint and optional binding to the existing Companion Gateway are implemented. Installation on an authorized Mac is required; GitHub fixture tests alone do not prove a running model. The binding uses the established localhost service and does not create another Gateway.

## Execution on authorized Mac mini runner

1. Check out branch `dore/speaker-design-compiler-v0` in the existing repository.
2. Prepare a canonical job:

```sh
python3 scripts/prepare_dore_local_image_job.py --speaker david-pawson
```

3. Configure the locally installed image generator command, replacing placeholders with the prompt file and output file paths:

```sh
export DORE_LOCAL_IMAGE_BACKEND='your-local-generator --prompt-file {prompt_file} --output {output_file}'
python3 scripts/run_dore_speaker_a2a.py --job local/dore-speaker-jobs/david-pawson --dry-run
```

4. Existing A2A agent runner executes the same command **without** `--dry-run` after local backend capability and authorization are verified. It returns machine-readable `LOCAL_RENDER_COMPLETE` or an error. No user-facing manual Draw Things copy/paste.

## Worker safety

- Uses argv without shell execution.
- Enforces canonical job schema and non-portrait policy.
- Rejects path escapes and refuses to overwrite existing generated image.
- Times out after 30 minutes for generation and 2 minutes for compositing.
- Requires real nonempty background output before compositing.
- Does not publish or merge anything.
- Does not assume Draw Things exposes a CLI or API. A verified backend adapter is required.

## Acceptance

A2A gateway availability, authorized Mac execution, installed local image model, backend command compatibility, actual image generation and final visual review remain separate gates. This contract is not proof of any of them.

## Installed Gateway binding

`Companion /a2a` now supports `design.speaker-cover.render` for the `design`
consumer. The binding accepts only canonical `speaker` and boolean `dry_run`;
backend commands, URLs and arbitrary paths are not accepted over the transport.
The fixed adapter uses the existing `http://127.0.0.1:8790` local image service,
requires `model_backed: true`, rejects SVG fallback and downloads only PNG assets
from that service. Completed requests have durable receipts; exact retries replay
those receipts rather than rerunning the model. A process lock serializes work.

From a Mac-side shell, including Codex's local terminal tool:

```sh
python3 scripts/call_dore_speaker_gateway.py --speaker david-pawson --dry-run
python3 scripts/call_dore_speaker_gateway.py --speaker david-pawson --request-id speaker-proof-1
```

The existing Companion launch configuration uses `DORE_SPEAKER_WORKER_ROOT` for
the deployed minimal worker bundle and `DORE_SPEAKER_PYTHON` for a Python runtime
with Pillow. Put the bundle in the existing Application Support service directory:
macOS background processes may not read a Documents checkout. Preserve the
original launch configuration and Companion before updating them. No new daemon,
public port, paid API, or production publishing is involved.

Model readiness does not establish cover quality. Inspect the actual PNG and
model provenance before accepting any cover. The existing resident model's canvas
settings govern generation; the compositor outputs 720×960, which does not prove
that the model generated at that resolution or met the editorial constraints.
