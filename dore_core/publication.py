"""Small Readium-shaped publication contract shared by Dawn consumers.

The Reader consumes this normalized publication model rather than provider
HTML, EPUB internals, or Gutenberg-specific URLs. Source adapters own those
provider details and emit a Publication.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class PublicationLink:
    href: str
    type: str = "text/html"
    title: str | None = None
    rel: tuple[str, ...] = ()
    language: str | None = None

    def to_dict(self) -> dict[str, Any]:
        row: dict[str, Any] = {"href": self.href, "type": self.type}
        if self.title:
            row["title"] = self.title
        if self.rel:
            row["rel"] = list(self.rel)
        if self.language:
            row["language"] = self.language
        return row


@dataclass(frozen=True)
class DawnPublication:
    identifier: str
    title: str
    authors: tuple[str, ...] = ()
    languages: tuple[str, ...] = ()
    reading_order: tuple[PublicationLink, ...] = ()
    resources: tuple[PublicationLink, ...] = ()
    toc: tuple[PublicationLink, ...] = ()
    source: dict[str, Any] = field(default_factory=dict)

    def to_manifest(self) -> dict[str, Any]:
        """Return a Web Publication Manifest-shaped JSON object."""
        metadata: dict[str, Any] = {"identifier": self.identifier, "title": self.title}
        if self.authors:
            metadata["author"] = [{"name": name} for name in self.authors]
        if self.languages:
            metadata["language"] = list(self.languages)
        return {
            "@context": ["https://readium.org/webpub-manifest/context.jsonld"],
            "metadata": metadata,
            "readingOrder": [link.to_dict() for link in self.reading_order],
            "resources": [link.to_dict() for link in self.resources],
            "toc": [link.to_dict() for link in self.toc],
            "dore:source": dict(self.source),
        }


def publication_from_text(
    *,
    identifier: str,
    title: str,
    text_href: str,
    authors: tuple[str, ...] = (),
    languages: tuple[str, ...] = (),
    source: dict[str, Any] | None = None,
) -> DawnPublication:
    """Normalize a single materialized text witness into Reader input."""
    language = languages[0] if languages else None
    return DawnPublication(
        identifier=identifier,
        title=title,
        authors=authors,
        languages=languages,
        reading_order=(PublicationLink(href=text_href, type="text/plain", title=title, language=language),),
        source=dict(source or {}),
    )
