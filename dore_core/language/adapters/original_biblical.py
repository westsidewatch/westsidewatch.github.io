"""Reference adapters that migrate Doré's validated biblical readers into the universal language core."""
from __future__ import annotations
from typing import Iterable
from dore_core.language.base import AdapterCapabilities, LanguageUnit, TextWitness
from dore_core.readers.original_language import iter_oshb_words, parse_morphgnt_line


def _unit_from_token(token) -> LanguageUnit:
    return LanguageUnit(
        witness_id=token.witness_id,
        canonical_ref_id=token.canonical_ref_id,
        order=token.order,
        surface=token.surface,
        normalized=token.normalized,
        language=token.language,
        analyses=tuple((a.type, a.value) for a in token.analyses),
        provenance=(
            f"textual_source:{token.textual_source_id}",
            f"snapshot:{token.corpus_snapshot}",
            f"native_ref:{token.source_native_ref}",
            f"token:{token.token_id}",
        ),
    )


class OSHBAdapter:
    adapter_id = "adapter.biblical.oshb"
    language = "he-arc"
    capabilities = AdapterCapabilities(
        segmentation=True,
        normalization=False,
        lemma=True,
        morphology=True,
        syntax=False,
        transliteration=False,
        speech=False,
        canonical_alignment=True,
    )

    def ingest(self, source: tuple[str, str], witness: TextWitness) -> Iterable[LanguageUnit]:
        xml_text, book_code = source
        for token in iter_oshb_words(xml_text, book_code):
            # OSHB contains Hebrew, Aramaic and one deliberately unresolved boundary verse.
            yield _unit_from_token(token)

    def normalize(self, text: str) -> str:
        return text


class MorphGNTAdapter:
    adapter_id = "adapter.biblical.morphgnt"
    language = "grc"
    capabilities = AdapterCapabilities(
        segmentation=True,
        normalization=True,
        lemma=True,
        morphology=True,
        syntax=False,
        transliteration=False,
        speech=False,
        canonical_alignment=True,
    )

    def ingest(self, source: str, witness: TextWitness) -> Iterable[LanguageUnit]:
        verse_orders: dict[str, int] = {}
        for raw in source.splitlines():
            line = raw.strip()
            if not line:
                continue
            ref = line.split(maxsplit=1)[0]
            verse_orders[ref] = verse_orders.get(ref, 0) + 1
            yield _unit_from_token(parse_morphgnt_line(line, verse_orders[ref]))

    def normalize(self, text: str) -> str:
        return text
