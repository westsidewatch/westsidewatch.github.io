# Local model adapter

The Golden Gate pilot now supports an explicit local subprocess protocol, without selecting a paid service or guessing the Doré runtime.

The executable reads one JSON task from stdin and writes one JSON candidate submission to stdout. It must return `scene_id`, `draft`, `evidence` and `reviewed`. A model should set `reviewed: false`; only an actual human reviewer may approve it. Evidence citations are not independently verified by the adapter.

```sh
python3 tools/dore/narrative-engine/local_adapter.py test
python3 tools/dore/narrative-engine/local_adapter.py run \
  --source docs/projects/watch-city-vol00/manuscript/JERUSALEM-BUILD.md \
  --scene failed-assault \
  --output /tmp/golden-gate-review.json \
  --model-command /absolute/path/to/local-dore-model-command
```

The command must already exist. This repository change does not install or start a model. Output stays outside the canonical manuscript, and unreviewed drafts remain blocked. The self-test uses a mock Python process and verifies the subprocess contract; it is **not** proof that a real model is connected. Never supply an untrusted executable as the model command.
