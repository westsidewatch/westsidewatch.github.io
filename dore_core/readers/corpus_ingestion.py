"""Doré full-corpus ingestion engine v0.1.

Consumes already-fetched pinned corpus files through the original-language
adapters. Network retrieval is intentionally outside this module so snapshots
remain explicit and auditable.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable
from .original_language import TokenRecord, iter_oshb_words, parse_morphgnt_line, validate_token

@dataclass
class IngestionReport:
    source_records: int = 0
    emitted_tokens: int = 0
    warnings: int = 0
    failures: int = 0
    excluded_records: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def ingest_morphgnt(lines: Iterable[str]) -> tuple[list[TokenRecord], IngestionReport]:
    tokens: list[TokenRecord] = []
    report = IngestionReport()
    verse_orders: dict[str, int] = {}
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        report.source_records += 1
        ref = line.split(maxsplit=1)[0]
        verse_orders[ref] = verse_orders.get(ref, 0) + 1
        try:
            token = parse_morphgnt_line(line, verse_orders[ref])
            errors = validate_token(token)
            if errors:
                report.failures += 1
                continue
            tokens.append(token)
            report.emitted_tokens += 1
            if token.validation_status == "warn":
                report.warnings += 1
        except (ValueError, IndexError):
            report.failures += 1
    return tokens, report


def ingest_oshb(xml_text: str, book_code: str) -> tuple[list[TokenRecord], IngestionReport]:
    tokens: list[TokenRecord] = []
    report = IngestionReport()
    for token in iter_oshb_words(xml_text, book_code):
        report.source_records += 1
        errors = validate_token(token)
        if errors:
            report.failures += 1
            continue
        tokens.append(token)
        report.emitted_tokens += 1
        if token.validation_status == "warn":
            report.warnings += 1
    return tokens, report


def assert_lossless(report: IngestionReport) -> None:
    """Enforce CR003 for records that the adapter recognizes as source tokens."""
    if report.failures or report.excluded_records:
        raise AssertionError(f"ingestion not lossless: {report.to_dict()}")
    if report.source_records != report.emitted_tokens:
        raise AssertionError(f"token count mismatch: {report.to_dict()}")
