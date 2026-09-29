"""Lawful text materialization boundary shared by Doré products.

Materialization is intentionally separate from discovery and bibliographic
authority. A known book is not automatically a readable full-text witness.
Dawn Library and future consumers must pass an explicit WitnessAccessPolicy.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .access import WitnessAccessPolicy
from .base import TextWitness


@dataclass(frozen=True)
class MaterializedText:
    witness: TextWitness
    text: str
    source_url: str | None
    persisted: bool


class MaterializationUnavailable(RuntimeError):
    pass


def materialize_text(
    *,
    witness: TextWitness,
    policy: WitnessAccessPolicy,
    local_loader: Callable[[TextWitness], str | None] | None = None,
    remote_loader: Callable[[TextWitness, WitnessAccessPolicy], str | None] | None = None,
) -> MaterializedText:
    """Resolve text only through a policy-authorized route.

    LOCAL_CORPUS may be read through ``local_loader`` when full-text ingestion is
    authorized. Remote retrieval is attempted only when the access policy says
    automated access is permitted. Retrieved text is marked persistent only when
    the policy explicitly permits persistent caching.
    """
    if policy.witness_id != witness.witness_id:
        raise ValueError("witness access policy does not match text witness")

    if policy.may_ingest_full_text() and local_loader is not None:
        text = local_loader(witness)
        if text:
            return MaterializedText(
                witness=witness,
                text=text,
                source_url=policy.source_url,
                persisted=True,
            )

    if policy.may_retrieve_automatically() and remote_loader is not None:
        text = remote_loader(witness, policy)
        if text:
            return MaterializedText(
                witness=witness,
                text=text,
                source_url=policy.source_url,
                persisted=policy.may_persist_retrieved_text(),
            )

    raise MaterializationUnavailable(
        f"no lawful materialization route for witness {witness.witness_id}; "
        f"access_mode={policy.mode.value}"
    )
