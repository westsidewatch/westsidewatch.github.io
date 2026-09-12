#!/usr/bin/env python3
"""Acceptance harness for the first Doré Reflex engineering spike."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

from reflex_contracts import SourceDescriptor
from reflex_projections import project
from reflex_router import ReflexRouter


SAMPLE = b"""# Job and His Friends\n\nEliphaz speaks from received wisdom.\nBildad judges from visible outcome.\nZophar speaks with assumed certainty.\n"""


def _docx_fixture() -> bytes:
    """Build a real minimal DOCX entirely in memory for adapter acceptance."""
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>Job and His Friends</w:t></w:r></w:p>
    <w:p><w:r><w:t>Eliphaz speaks from received wisdom.</w:t></w:r></w:p>
    <w:p><w:r><w:t>Bildad judges from visible outcome.</w:t></w:r></w:p>
    <w:p><w:r><w:t>Zophar speaks with assumed certainty.</w:t></w:r></w:p>
    <w:sectPr/>
  </w:body>
</w:document>""",
        )
    return buffer.getvalue()


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

        docx_source = SourceDescriptor(
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            name="job-friends.docx",
            canonical_id="work:test-job-friends-docx",
            source_pointer="fixture://job-friends.docx",
        )
        docx = router.open(docx_source, _docx_fixture())
        assert docx.adapter == "markitdown"

        docx_search = project(docx, "text.search")
        docx_publishing = project(docx, "publishing.structure")
        docx_design = project(docx, "design.structure")
        joined = "\n".join(chunk["text"] for chunk in docx_search["chunks"])
        assert "Job and His Friends" in joined
        assert "Bildad judges from visible outcome." in joined
        assert docx_search["chunks"][0]["provenance"]["canonicalId"] == docx_source.canonical_id
        assert docx_publishing["source"]["canonicalId"] == docx_source.canonical_id
        assert docx_design["authority"]["layoutDecision"] is False
        docx.close()
        assert docx.events == []

        after = sorted(Path(tmp).rglob("*"))
        assert before == after, "Reflex v0 must not persist a second substrate"

    binary = router.open(SourceDescriptor(mime="application/octet-stream", name="unknown.bin"), b"\x00\x01")
    assert binary.adapter == "degraded"
    assert any(event.kind == "unsupported" for event in binary.iter_events())
    binary.close()

    print("PASS: Dor\u00e9 Reflex v0 Markdown + in-memory DOCX multi-projection acceptance")


if __name__ == "__main__":
    main()
