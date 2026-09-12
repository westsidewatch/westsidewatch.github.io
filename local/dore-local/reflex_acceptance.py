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


def _xlsx_fixture() -> bytes:
    """Build a real one-sheet XLSX entirely in memory for heterogeneous acceptance."""
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="Friends" sheetId="1" r:id="rId1"/></sheets>
</workbook>""",
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "xl/worksheets/sheet1.xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>Friend</t></is></c>
      <c r="B1" t="inlineStr"><is><t>Lens</t></is></c>
    </row>
    <row r="2">
      <c r="A2" t="inlineStr"><is><t>Eliphaz</t></is></c>
      <c r="B2" t="inlineStr"><is><t>received wisdom</t></is></c>
    </row>
    <row r="3">
      <c r="A3" t="inlineStr"><is><t>Bildad</t></is></c>
      <c r="B3" t="inlineStr"><is><t>visible outcome</t></is></c>
    </row>
    <row r="4">
      <c r="A4" t="inlineStr"><is><t>Zophar</t></is></c>
      <c r="B4" t="inlineStr"><is><t>assumed certainty</t></is></c>
    </row>
  </sheetData>
</worksheet>""",
        )
    return buffer.getvalue()


def _assert_three_projections(router: ReflexRouter, source: SourceDescriptor, payload: bytes, adapter: str) -> str:
    session = router.open(source, payload)
    assert session.adapter == adapter
    search = project(session, "text.search")
    publishing = project(session, "publishing.structure")
    design = project(session, "design.structure")
    assert search["chunks"], "search projection must contain source content"
    assert search["chunks"][0]["provenance"]["canonicalId"] == source.canonical_id
    assert publishing["source"]["canonicalId"] == source.canonical_id
    assert design["authority"]["layoutDecision"] is False
    joined = "\n".join(chunk["text"] for chunk in search["chunks"])
    session.close()
    assert session.closed is True
    assert session.events == []
    return joined


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
        docx_joined = _assert_three_projections(router, docx_source, _docx_fixture(), "markitdown")
        assert "Job and His Friends" in docx_joined
        assert "Bildad judges from visible outcome." in docx_joined

        xlsx_source = SourceDescriptor(
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            name="job-friends.xlsx",
            canonical_id="work:test-job-friends-xlsx",
            source_pointer="fixture://job-friends.xlsx",
        )
        xlsx_joined = _assert_three_projections(router, xlsx_source, _xlsx_fixture(), "markitdown")
        assert "Eliphaz" in xlsx_joined and "received wisdom" in xlsx_joined
        assert "Bildad" in xlsx_joined and "visible outcome" in xlsx_joined
        assert "Zophar" in xlsx_joined and "assumed certainty" in xlsx_joined

        after = sorted(Path(tmp).rglob("*"))
        assert before == after, "Reflex v0 must not persist a second substrate"

    binary = router.open(SourceDescriptor(mime="application/octet-stream", name="unknown.bin"), b"\x00\x01")
    assert binary.adapter == "degraded"
    assert any(event.kind == "unsupported" for event in binary.iter_events())
    binary.close()

    print("PASS: Doré Reflex v0 Markdown + DOCX + XLSX one-source/multi-projection acceptance")


if __name__ == "__main__":
    main()
