#!/usr/bin/env python3
"""Acceptance harness for the first Doré Reflex engineering spike."""
from __future__ import annotations

from pathlib import Path
import tempfile

from reflex_contracts import SourceDescriptor
from reflex_projections import project
from reflex_router import ReflexRouter


SAMPLE = b"""# Job and His Friends\n\nEliphaz speaks from received wisdom.\nBildad judges from visible outcome.\nZophar speaks with assumed certainty.\n"""


def main() -> None:
    router = ReflexRouter()
    source = SourceDescriptor(
        mime="text/markdown",
        name="job-friends.md",
        canonical_id="work:test-job-friends",
        source_pointer="fixture://job-friends.md",
    )

    with tempfile.TemporaryDirectory() as tmp:
        before = sorted(Path(tmp).rglob("*"))
        session = router.open(source, SAMPLE)
        assert session.adapter == "text"

        search = project(session, "text.search")
        publishing = project(session, "publishing.structure")
        design = project(session, "design.structure")

        assert len(search["chunks"]) == 4
        assert search["chunks"][0]["provenance"]["canonicalId"] == source.canonical_id
        assert publishing["sections"][1]["title"] == "Job and His Friends"
        assert design["signals"]["headingCount"] == 1
        assert design["authority"]["layoutDecision"] is False

        session.close()
        assert session.closed is True
        assert session.events == []
        after = sorted(Path(tmp).rglob("*"))
        assert before == after, "Reflex v0 must not persist a second substrate"

    binary = router.open(SourceDescriptor(mime="application/octet-stream", name="unknown.bin"), b"\x00\x01")
    assert binary.adapter == "degraded"
    assert any(event.kind == "unsupported" for event in binary.iter_events())
    binary.close()

    print("PASS: Dor\u00e9 Reflex v0 ephemeral one-source/multi-projection acceptance")


if __name__ == "__main__":
    main()
