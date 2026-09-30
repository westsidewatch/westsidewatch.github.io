from __future__ import annotations

import pytest

from dore_core.language.base import TextWitness
from dore_core.language.materialization import MaterializationUnavailable, materialize_text
from dore_core.language.source_mapping import map_public_domain_source


def _gutenberg_work() -> dict:
    return {
        "workId": "test:gutenberg:1342",
        "title": "Pride and Prejudice",
        "languages": ["en"],
        "authorityIds": {"projectGutenberg": "1342"},
    }


def test_gutenberg_remains_a_human_reader_pointer_not_an_automated_text_source() -> None:
    mapping = map_public_domain_source(_gutenberg_work())
    assert mapping is not None
    assert mapping.provider == "project-gutenberg"
    assert mapping.source_url == "https://www.gutenberg.org/ebooks/1342"
    assert mapping.policy.automated_access_permitted is False
    assert mapping.policy.full_text_storage_permitted is False
    assert mapping.policy.persistent_cache_permitted is False
    assert mapping.policy.may_retrieve_automatically() is False


def test_materializer_never_calls_remote_loader_for_gutenberg() -> None:
    mapping = map_public_domain_source(_gutenberg_work())
    assert mapping is not None
    witness = TextWitness(
        witness_id=mapping.witness_id,
        language="en",
        edition="project-gutenberg",
        source_id="1342",
        snapshot="remote-live",
        license_id="project-gutenberg-license",
        metadata={"workId": "test:gutenberg:1342"},
    )
    called = False

    def forbidden_remote_loader(*_args, **_kwargs):
        nonlocal called
        called = True
        return "should never be fetched"

    with pytest.raises(MaterializationUnavailable):
        materialize_text(
            witness=witness,
            policy=mapping.policy,
            remote_loader=forbidden_remote_loader,
        )

    assert called is False
