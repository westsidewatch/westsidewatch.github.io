#!/usr/bin/env python3
"""Acceptance harness for the Doré Reflex v0 engineering spike."""
from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

from reflex_capability import CAPABILITY_ID, RESULT_SCHEMA, execute as execute_reflex
from reflex_contracts import REFLEX_EVENT_KINDS, ReflexSession, SourceDescriptor
from reflex_projections import project
from reflex_router import ReflexRouter


SAMPLE = b"""# Job and His Friends\n\nEliphaz speaks from received wisdom.\nBildad judges from visible outcome.\nZophar speaks with assumed certainty.\n"""


def _docx_fixture() -> bytes:
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


def _exercise(router: ReflexRouter, source: SourceDescriptor, payload: bytes, adapter: str) -> dict:
    session = router.open(source, payload)
    assert session.adapter == adapter
    kinds = [event.kind for event in session.iter_events()]
    assert set(kinds) <= REFLEX_EVENT_KINDS

    search = project(session, "text.search")
    publishing = project(session, "publishing.structure")
    design = project(session, "design.structure")
    assert search["chunks"], "search projection must contain source content"
    assert search["chunks"][0]["provenance"]["canonicalId"] == source.canonical_id
    assert publishing["source"]["canonicalId"] == source.canonical_id
    assert design["authority"]["layoutDecision"] is False
    assert design["authority"]["brandDecision"] is False
    joined = "\n".join(chunk["text"] for chunk in search["chunks"])

    result = {
        "joined": joined,
        "kinds": kinds,
        "search": search,
        "publishing": publishing,
        "design": design,
    }
    session.close()
    assert session.closed is True
    assert session.events == []
    return result


def _runtime_request(source: SourceDescriptor, payload: bytes, intent: str) -> dict:
    return {
        "intent": intent,
        "source": {
            "mime": source.mime,
            "name": source.name,
            "canonicalId": source.canonical_id,
            "sourcePointer": source.source_pointer,
        },
        "payloadBase64": base64.b64encode(payload).decode("ascii"),
    }


def _runtime_three(source: SourceDescriptor, payload: bytes, adapter: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for intent in ("text.search", "publishing.structure", "design.structure"):
        result = execute_reflex(_runtime_request(source, payload, intent))
        assert result["ok"] is True
        assert result["status"] == "completed"
        assert result["capability"] == CAPABILITY_ID
        assert result["schema"] == RESULT_SCHEMA
        assert result["adapter"] == adapter
        assert result["source"]["canonicalId"] == source.canonical_id
        assert result["source"]["sourcePointer"] == source.source_pointer
        assert "events" not in result and "session" not in result
        assert result["projection"]["schema"].startswith("dore.reflex.")
        out[intent] = result
    assert len({item["projection"]["schema"] for item in out.values()}) == 3
    return out


class TrackingRouter(ReflexRouter):
    def __init__(self) -> None:
        super().__init__()
        self.last_session: ReflexSession | None = None

    def open(self, source: SourceDescriptor, payload: bytes) -> ReflexSession:
        self.last_session = super().open(source, payload)
        return self.last_session


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

        markdown = _exercise(router, source, SAMPLE, "text")
        assert "heading" in markdown["kinds"]
        assert "Job and His Friends" in markdown["joined"]
        assert markdown["design"]["signals"]["headingCount"] == 1
        markdown_runtime = _runtime_three(source, SAMPLE, "text")
        assert "Job and His Friends" in "\n".join(
            chunk["text"] for chunk in markdown_runtime["text.search"]["projection"]["chunks"]
        )

        docx_source = SourceDescriptor(
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            name="job-friends.docx",
            canonical_id="work:test-job-friends-docx",
            source_pointer="fixture://job-friends.docx",
        )
        docx_payload = _docx_fixture()
        docx = _exercise(router, docx_source, docx_payload, "markitdown")
        assert "Job and His Friends" in docx["joined"]
        assert "Bildad judges from visible outcome." in docx["joined"]
        docx_runtime = _runtime_three(docx_source, docx_payload, "markitdown")
        assert docx_runtime["publishing.structure"]["projection"]["source"]["canonicalId"] == docx_source.canonical_id

        xlsx_source = SourceDescriptor(
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            name="job-friends.xlsx",
            canonical_id="work:test-job-friends-xlsx",
            source_pointer="fixture://job-friends.xlsx",
        )
        xlsx_payload = _xlsx_fixture()
        xlsx = _exercise(router, xlsx_source, xlsx_payload, "markitdown")
        assert "table.start" in xlsx["kinds"]
        assert xlsx["kinds"].count("table.row") == 4
        assert "table.end" in xlsx["kinds"]
        table_chunks = [chunk for chunk in xlsx["search"]["chunks"] if chunk["kind"] == "table.row"]
        assert table_chunks[0]["cells"] == ["Friend", "Lens"]
        assert table_chunks[0]["header"] is True
        assert table_chunks[2]["cells"] == ["Bildad", "visible outcome"]
        assert xlsx["design"]["signals"]["hasStructuredTable"] is True
        assert xlsx["design"]["signals"]["tableRowCount"] == 4
        table_blocks = [
            block
            for section in xlsx["publishing"]["sections"]
            for block in section["blocks"]
            if block["type"] == "table"
        ]
        assert len(table_blocks) == 1
        assert table_blocks[0]["rows"][3]["cells"] == ["Zophar", "assumed certainty"]
        xlsx_runtime = _runtime_three(xlsx_source, xlsx_payload, "markitdown")
        assert xlsx_runtime["design.structure"]["projection"]["signals"]["hasStructuredTable"] is True

        tracking = TrackingRouter()

        def fail_projection(_session: ReflexSession, _intent: str) -> dict:
            raise RuntimeError("forced projection failure")

        try:
            execute_reflex(
                _runtime_request(source, SAMPLE, "text.search"),
                router=tracking,
                projector=fail_projection,
            )
            raise AssertionError("forced projection failure must escape")
        except RuntimeError as exc:
            assert str(exc) == "forced projection failure"
        assert tracking.last_session is not None
        assert tracking.last_session.closed is True
        assert tracking.last_session.events == []

        bad_intent = execute_reflex(_runtime_request(source, SAMPLE, "not.a.real.intent"))
        assert bad_intent["ok"] is False
        assert bad_intent["error"]["code"] == "unsupported_intent"
        bad_payload = _runtime_request(source, SAMPLE, "text.search")
        bad_payload["payloadBase64"] = "%%%not-base64%%%"
        invalid_payload = execute_reflex(bad_payload)
        assert invalid_payload["ok"] is False
        assert invalid_payload["error"]["code"] == "invalid_args"

        after = sorted(Path(tmp).rglob("*"))
        assert before == after, "Reflex v0 must not persist a second substrate"

    binary = router.open(SourceDescriptor(mime="application/octet-stream", name="unknown.bin"), b"\x00\x01")
    assert binary.adapter == "degraded"
    assert any(event.kind == "unsupported" for event in binary.iter_events())
    binary.close()

    print("PASS: Doré Reflex v0 live runtime capability across Markdown + DOCX + XLSX")


if __name__ == "__main__":
    main()
