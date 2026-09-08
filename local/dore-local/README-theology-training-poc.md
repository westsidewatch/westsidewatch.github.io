# Theology Alignment Micro-POC

The local training POC is intentionally isolated from Doré canonical stores.

Readiness only:

```bash
python3 local/dore-local/theology-training-readiness.py
```

Dry-run orchestration against an external quarantine directory:

```bash
python3 local/dore-local/theology-training-poc.py \
  --quarantine /path/outside/dore/quarantine \
  --size 32
```

Actual training is blocked by process order until Theology Rails are integrated and accepted on the live AI-dialogue path. When that gate is closed, add `--execute`.

The quarantine directory must contain:

```text
train-32.jsonl
valid.jsonl
test.jsonl
```

Later learning-curve stages use `train-64.jsonl`, `train-128.jsonl`, and `train-256.jsonl`.

Do not place this directory under `~/.dore` or `~/Library/Application Support/Dore`.
