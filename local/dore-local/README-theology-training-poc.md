# Theology Alignment Micro-POC

The local training POC is intentionally isolated from Doré canonical stores.

The live Theology Rails are already on the guarded Doré Local dialogue path. Training remains a separate adapter experiment and does not replace the deterministic authority/admission boundary.

Prepare the isolated MLX-VLM toolchain:

```bash
python3 local/dore-local/theology-training-prepare.py
python3 local/dore-local/theology-training-readiness.py
```

The quarantine directory must be external to Doré canonical/runtime stores and contain:

```text
train-32.jsonl
valid.jsonl
test.jsonl
```

Configure that owner-controlled path without placing it under `~/.dore` or `~/Library/Application Support/Dore`:

```bash
export DORE_THEOLOGY_QUARANTINE=/path/outside/dore/quarantine
```

Dry-run the exact 32-example MLX-VLM orchestration:

```bash
python3 local/dore-local/theology-training-poc.py \
  --quarantine "$DORE_THEOLOGY_QUARANTINE" \
  --size 32
```

The fixed A2A capability `theology.training.micro32` invokes `theology-training-micro32.py`, which always runs exactly 32 examples with `--execute`. It does not accept an arbitrary shell command, model, dataset path, or learning-curve size from the caller. The training process runs cache-only and keeps the LoRA adapter separate from the base/runtime model.

Later Minimum Sufficient Learning stages use `train-64.jsonl`, `train-128.jsonl`, and `train-256.jsonl`, but they are not exposed by the micro32 capability. Advance only after the 32-example real-Mac run has measured runtime, adapter size, and behavioral effect.
