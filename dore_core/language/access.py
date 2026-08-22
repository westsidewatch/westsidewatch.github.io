"""Lawful witness access architecture for Doré.

Knowing a textual witness does not imply permission to persist its full text.
Access policy is first-class and must be checked before ingestion, caching,
or automated retrieval.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class WitnessAccessMode(str, Enum):
    LOCAL_CORPUS = "local_corpus"
    LICENSED_API = "licensed_api"
    EXTERNAL_READER = "external_reader"
    HUMAN_ONLY = "human_only"

@dataclass(frozen=True)
class WitnessAccessPolicy:
    witness_id: str
    mode: WitnessAccessMode
    source_name: str
    source_url: str | None = None
    license_id: str | None = None
    terms_url: str | None = None
    automated_access_permitted: bool = False
    full_text_storage_permitted: bool = False
    persistent_cache_permitted: bool = False
    quotation_notes: str | None = None
    notes: str | None = None

    def may_ingest_full_text(self) -> bool:
        return self.mode == WitnessAccessMode.LOCAL_CORPUS and self.full_text_storage_permitted

    def may_retrieve_automatically(self) -> bool:
        return self.mode in {WitnessAccessMode.LICENSED_API, WitnessAccessMode.EXTERNAL_READER} and self.automated_access_permitted

    def may_persist_retrieved_text(self) -> bool:
        return self.persistent_cache_permitted


def require_ingestion_permission(policy: WitnessAccessPolicy) -> None:
    if not policy.may_ingest_full_text():
        raise PermissionError(
            f"witness {policy.witness_id} is not authorized for full-text local ingestion; "
            f"access_mode={policy.mode.value}"
        )
