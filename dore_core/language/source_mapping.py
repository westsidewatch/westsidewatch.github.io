"""Source mapping for lawful book-text materialization.

Maps bibliographic authority records to known full-text providers without
making bibliographic identity itself permission to fetch full text.
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
    """Map explicit provider identities to access-policy-bound reader sources."""
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
                terms_url="https://www.gutenberg.org/policy/terms_of_use.html",
                automated_access_permitted=False,
                full_text_storage_permitted=False,
                persistent_cache_permitted=False,
                notes=(
                    "Human-reader source only. Project Gutenberg states that its website is for human users; "
                    "Doré keeps the canonical landing-page pointer but does not automate website text retrieval."
                ),
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
