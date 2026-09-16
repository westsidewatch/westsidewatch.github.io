#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

from two_days_capability_bridge import resolve, DEFAULT_PROFILES, REGISTRY
from dimensional_publishing_capability import DimensionalPublishingCapability, CAPABILITY_ID


def main() -> None:
    registry = json.loads(Path(REGISTRY).read_text(encoding="utf-8"))
    ids = {item["id"] for item in registry["capabilities"]}
    assert CAPABILITY_ID in ids
    assert CAPABILITY_ID in DEFAULT_PROFILES["writing"]
    assert CAPABILITY_ID not in DEFAULT_PROFILES["design"]
    assert CAPABILITY_ID not in DEFAULT_PROFILES["bible-study"]
    assert CAPABILITY_ID not in DEFAULT_PROFILES["publishing"]

    today = {
        "schema_id": "two-days.today.v0",
        "active_head": "the-gate/article-3",
        "work_heads": {
            "the-gate/article-3": {
                "accepted_head": {"version_id": "v17", "sha256": "accepted"},
                "working_head": {"version_id": "v18", "sha256": "working"},
            }
        },
        "resume_head": {"artifact_id": "the-gate/article-3", "instruction": "continue article 3", "unfinished_edge": "from accepted scene"},
        "source_refs": [{"kind": "artifact-ledger", "id": "the-gate:v17"}],
    }
    context = resolve(profile="writing", today=today)
    refs = [item["id"] for item in context["capability_refs"]]
    assert CAPABILITY_ID in refs
    assert context["task"]["active_artifact"] == today["active_head"]
    assert context["task"]["accepted_head"]["version_id"] == "v17"
    assert context["task"]["working_head"]["version_id"] == "v18"
    assert context["task"]["resume_head"] == today["resume_head"]

    manuscript = "城门已经关上，城里的灯仍然亮着。"
    thesis = "作者的原稿与立意保持最高 authority。"
    seen = {}
    def infer(request):
        seen.update(request)
        return {"deep_dive": [{"kind": "history", "note": "expand evidence only"}]}

    plan = DimensionalPublishingCapability(infer=infer).compile(
        title="The Gate · Article 3",
        manuscript=manuscript,
        thesis=thesis,
        context=context,
    )
    assert plan["capability"] == CAPABILITY_ID
    assert plan["manuscript"] == manuscript
    assert plan["thesis"] == thesis
    assert plan["deep_dive"][0]["note"] == "expand evidence only"
    assert seen["context"]["task"]["active_artifact"] == "the-gate/article-3"
    assert context["authority"]["state"] == "TODAY"
    assert context["authority"]["artifact_text"] == "artifact-ledger"
    assert context["authority"]["may_rewrite_author_thesis"] is False
    print("TWO_DAYS_WRITING_CAPABILITY_CONNECTION_PASS")


if __name__ == "__main__":
    main()
