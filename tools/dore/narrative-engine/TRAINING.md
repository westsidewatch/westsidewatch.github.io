# Narrative Engine training execution

No paid API or third-party service is required. The runner uses only the Python standard library.

## Commands

```sh
python3 tools/dore/narrative-engine/narrative.py test
python3 tools/dore/narrative-engine/training_runner.py test
python3 tools/dore/narrative-engine/training_runner.py exercises
python3 tools/dore/narrative-engine/training_runner.py assess path/to/submission.json
```

## Submission schema

```json
{
  "scene_id": "failed-assault",
  "draft": "A sourced, scene-driven draft...",
  "evidence": [
    {"category": "documented", "claim": "Insufficient ladders", "source": "Gesta Francorum"},
    {"category": "contextual", "claim": "A physical inference supported by terrain"}
  ],
  "reviewed": true
}
```

The runner refuses unsupported claims, documented claims with no named source, missing human review and unknown scenes. It flags quotations for manual checking. It cannot verify source accuracy, assess prose quality, or train model weights; those require separate work. Never treat REVIEW_READY as historical certification.

## Next integration

Implement a model-independent revision adapter that produces structured drafts and explicit evidence ledgers; compare them against the original Golden Gate text. Do not edit the canonical manuscript until reviewed and approved.
