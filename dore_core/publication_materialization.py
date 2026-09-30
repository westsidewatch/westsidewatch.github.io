"""Bind lawful materialized text to the normalized Dawn publication layer."""
from __future__ import annotations

from dataclasses import dataclass

from .language.materialization import MaterializedText
from .publication import DawnPublication, PublicationLink


@dataclass(frozen=True)
class PublicationResource:
    href: str
    media_type: str
    body: str
    persisted: bool
    source_url: str | None


def bind_materialized_text(
    publication: DawnPublication,
    materialized: MaterializedText,
) -> tuple[DawnPublication, PublicationResource]:
    """Turn a materialized witness into the publication's readable resource.

    The text body stays outside the manifest.  The manifest points to a stable
    Dawn resource URI, matching the Streamer/Fetcher separation used by mature
    web-reader architectures.
    """
    expected = str(publication.source.get("witnessId") or "")
    actual = materialized.witness.witness_id
    if expected and expected != actual:
        raise ValueError("materialized witness does not match publication source")
    if not materialized.text.strip():
        raise ValueError("materialized publication text is empty")

    href = f"dawn://publication/{publication.identifier}/source"
    language = publication.languages[0] if publication.languages else None
    link = PublicationLink(
        href=href,
        type="text/plain",
        title=publication.title,
        language=language,
    )
    bound = DawnPublication(
        identifier=publication.identifier,
        title=publication.title,
        authors=publication.authors,
        languages=publication.languages,
        reading_order=(link,),
        resources=publication.resources,
        toc=publication.toc,
        source={**publication.source, "materialized": True, "persisted": materialized.persisted},
    )
    resource = PublicationResource(
        href=href,
        media_type="text/plain",
        body=materialized.text,
        persisted=materialized.persisted,
        source_url=materialized.source_url,
    )
    return bound, resource
