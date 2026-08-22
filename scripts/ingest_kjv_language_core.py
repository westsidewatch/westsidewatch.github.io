#!/usr/bin/env python3
"""Ingest the pinned TheologyCommons KJV 1769 JSON witness.

The first CI run is deliberately diagnostics-capable: if the upstream JSON
shape differs from supported layouts, the report records its structure rather
than silently treating partial data as PASS.
"""
from __future__ import annotations
import json, os, re, traceback
from pathlib import Path
from typing import Any, Iterable
from dore_core.language.base import TextWitness, LanguageUnit, validate_units
from dore_core.language.adapters.verse_list_json import BOOK_ALIASES, TOKEN_RE

REPORT = Path("reports/DORÉ-KJV-INGESTION.json")
SNAPSHOT = "014f6966aad1dc8888b088cd11ea8216a46fa738"
SOURCE = "TheologyCommons/Bible.TEI.KJV"


def shape(value: Any, depth: int = 0) -> Any:
    if depth >= 4:
        return type(value).__name__
    if isinstance(value, dict):
        keys = list(value)[:12]
        return {"type": "dict", "keys": keys, "sample": {k: shape(value[k], depth + 1) for k in keys[:3]}}
    if isinstance(value, list):
        return {"type": "list", "length": len(value), "sample": shape(value[0], depth + 1) if value else None}
    return {"type": type(value).__name__, "sample": str(value)[:160]}


def canon_book(value: Any) -> str | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    upper = raw.upper()
    if re.fullmatch(r"(?:[1-3][A-Z]{2}|[A-Z]{3})", upper):
        return upper
    return BOOK_ALIASES.get(raw.lower())


def row_units(rows: Iterable[dict[str, Any]], witness: TextWitness):
    for row in rows:
        if not isinstance(row, dict):
            continue
        book = canon_book(row.get("book") or row.get("bookName") or row.get("book_name") or row.get("b"))
        text = row.get("text") or row.get("verseText") or row.get("content")
        try:
            chapter = int(row.get("chapter") or row.get("chapterNumber") or row.get("c"))
            verse = int(row.get("verse") or row.get("verseNumber") or row.get("v"))
        except (TypeError, ValueError):
            continue
        if not book or not isinstance(text, str):
            continue
        ref = f"bible.ref.{book}.{chapter}.{verse}"
        for order, surface in enumerate(TOKEN_RE.findall(text), 1):
            yield LanguageUnit(witness.witness_id, ref, order, surface, " ".join(surface.split()), witness.language,
                               (), (f"textual_source:{witness.source_id}", f"snapshot:{witness.snapshot}"))


def nested_units(data: Any, witness: TextWitness):
    # Supported common forms: {books:[...]}, books keyed by name, or flat verse rows.
    if isinstance(data, list):
        yield from row_units(data, witness)
        return
    if not isinstance(data, dict):
        return
    for key in ("verses", "data", "rows"):
        if isinstance(data.get(key), list):
            yield from row_units(data[key], witness)
            return
    books = data.get("books") or data.get("Books")
    if isinstance(books, list):
        for b in books:
            if not isinstance(b, dict): continue
            book = canon_book(b.get("book") or b.get("name") or b.get("bookName") or b.get("id"))
            chapters = b.get("chapters") or b.get("Chapters")
            if not book or not isinstance(chapters, list): continue
            for ch in chapters:
                if not isinstance(ch, dict): continue
                try: chapter = int(ch.get("chapter") or ch.get("number") or ch.get("id"))
                except (TypeError, ValueError): continue
                verses = ch.get("verses") or ch.get("Verses")
                if not isinstance(verses, list): continue
                for v in verses:
                    if not isinstance(v, dict): continue
                    try: verse = int(v.get("verse") or v.get("number") or v.get("id"))
                    except (TypeError, ValueError): continue
                    text = v.get("text") or v.get("content") or v.get("verseText")
                    if not isinstance(text, str): continue
                    ref=f"bible.ref.{book}.{chapter}.{verse}"
                    for order,surface in enumerate(TOKEN_RE.findall(text),1):
                        yield LanguageUnit(witness.witness_id,ref,order,surface," ".join(surface.split()),witness.language,(),
                            (f"textual_source:{witness.source_id}",f"snapshot:{witness.snapshot}"))
        return


def main() -> None:
    report = {"witness":"KJV-1769","source":SOURCE,"snapshot":SNAPSHOT,"license":"Public Domain"}
    try:
        path=Path(os.environ.get("DORE_KJV_JSON", ".cache/kjv/KJV.json"))
        data=json.loads(path.read_text(encoding="utf-8-sig"))
        witness=TextWitness("bible.kjv.1769","en","King James Version 1769",SOURCE,SNAPSHOT,"Public Domain")
        units=list(nested_units(data,witness))
        errors=validate_units(units,witness)
        refs={u.canonical_ref_id for u in units if u.canonical_ref_id}
        books={r.split(".")[2] for r in refs}
        report.update(source_shape=shape(data),units=len(units),verses=len(refs),books=len(books),book_ids=sorted(books),validation_errors=errors[:100])
        report["status"]="PASS" if len(books)==66 and len(refs)>=30000 and not errors else "FAIL"
        if report["status"] != "PASS" and not units:
            report["diagnostic"]="No supported verse structure recognized; inspect source_shape and extend parser."
    except Exception as exc:
        report.update(status="INFRA_FAIL",error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc())
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if report["status"] != "PASS": raise SystemExit(1)

if __name__ == "__main__": main()
