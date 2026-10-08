# Doré speaker cover — A2A local worker contract

## Status

The **worker entrypoint** is implemented. The live A2A gateway and Mac mini are **not connected or executed by this PR**. A2A transport binding must use the project's existing authorized gateway and runner; do not invent endpoints, tokens, or launch agents.

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
