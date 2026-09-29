"""Source mapping for lawful book-text materialization.

Maps bibliographic authority records to known full-text providers without
making Open Library bibliographic identity itself a full-text source.
"""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

from .access import WitnessAccessMode, WitnessAccessPolicy


@dataclass(frozen=True)
class SourceMapping:
    provider: str
    witness_id: str
    source_url: str
    policy: WitnessAccessPolicy


def _clean(value: object) -> str:
    return str(value or "").strip()


def map_public_domain_source(work: dict) -> SourceMapping | None:
    """Return a materializable source only when an explicit provider id exists.

    Supported mappings deliberately require provider-specific identifiers.
    ISBN/Open Library IDs remain bibliographic authority and never silently
    become permission to fetch full text.
    """
    work_id = _clean(work.get("workId"))
    ids = work.get("authorityIds") or {}
    edition = work.get("edition") or {}

    gutenberg_id = _clean(
        ids.get("projectGutenberg")
        or ids.get("gutenberg")
        or edition.get("projectGutenberg")
        or edition.get("gutenberg")
    )
    if gutenberg_id.isdigit():
        source_url = f"https://www.gutenberg.org/ebooks/{quote(gutenberg_id)}"
        witness_id = f"dawn:gutenberg:{gutenberg_id}"
        return SourceMapping(
            provider="project-gutenberg",
            witness_id=witness_id,
            source_url=source_url,
            policy=WitnessAccessPolicy(
                witness_id=witness_id,
                mode=WitnessAccessMode.EXTERNAL_READER,
                source_name="Project Gutenberg",
                source_url=source_url,
                license_id="project-gutenberg-license",
                terms_url="https://www.gutenberg.org/policy/license.html",
                automated_access_permitted=True,
                full_text_storage_permitted=False,
                persistent_cache_permitted=False,
                notes="Public-domain source mapping; persistence remains disabled by default.",
            ),
        )

    standard_ebooks = _clean(
        ids.get("standardEbooks")
        or ids.get("standard_ebooks")
        or edition.get("standardEbooks")
        or edition.get("standard_ebooks")
    )
    if standard_ebooks:
        slug = standard_ebooks.removeprefix("https://standardebooks.org/ebooks/").strip("/")
        if slug and ".." not in slug:
            source_url = f"https://standardebooks.org/ebooks/{quote(slug, safe='/')}"
            witness_id = f"dawn:standard-ebooks:{slug.replace('/', ':')}"
            return SourceMapping(
                provider="standard-ebooks",
                witness_id=witness_id,
                source_url=source_url,
                policy=WitnessAccessPolicy(
                    witness_id=witness_id,
                    mode=WitnessAccessMode.EXTERNAL_READER,
                    source_name="Standard Ebooks",
                    source_url=source_url,
                    license_id="standard-ebooks-public-domain",
                    terms_url="https://standardebooks.org/contribute/faq",
                    automated_access_permitted=True,
                    full_text_storage_permitted=False,
                    persistent_cache_permitted=False,
                    notes="Provider-specific public-domain mapping; persistence disabled by default.",
                ),
            )

    return None
