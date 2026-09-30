"""Policy-bound Project Gutenberg plain-text loader.

Retrieval is intentionally injectable for tests and constrained to Gutenberg
hosts/ebook identities. The loader returns text only; persistence decisions stay
inside language.materialization.
"""
from __future__ import annotations

import re
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from dore_core.language.access import WitnessAccessPolicy
from dore_core.language.base import TextWitness

_GUTENBERG_ID = re.compile(r"(?:gutenberg:|ebooks/)(\d+)", re.I)
_ALLOWED_HOSTS = {"gutenberg.org", "www.gutenberg.org"}


def _ebook_id(witness: TextWitness, policy: WitnessAccessPolicy) -> str:
    for value in (witness.source_id, witness.witness_id, policy.source_url):
        match = _GUTENBERG_ID.search(str(value or ""))
        if match:
            return match.group(1)
    raise ValueError("Project Gutenberg ebook id missing from witness/policy")


def _assert_gutenberg_policy(policy: WitnessAccessPolicy) -> None:
    if not policy.may_retrieve_automatically():
        raise PermissionError("policy forbids automated retrieval")
    parsed = urlparse(str(policy.source_url or ""))
    if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
        raise PermissionError("remote loader only accepts HTTPS Project Gutenberg sources")


def gutenberg_plain_text_urls(ebook_id: str) -> tuple[str, ...]:
    """Known Gutenberg UTF-8 plain-text routes, ordered by preference."""
    return (
        f"https://www.gutenberg.org/ebooks/{ebook_id}.txt.utf-8",
        f"https://www.gutenberg.org/files/{ebook_id}/{ebook_id}-0.txt",
        f"https://www.gutenberg.org/files/{ebook_id}/{ebook_id}.txt",
    )


def load_gutenberg_text(
    witness: TextWitness,
    policy: WitnessAccessPolicy,
    *,
    timeout: float = 20.0,
    fetch: Callable[[str, float], str | None] | None = None,
) -> str | None:
    """Fetch the first available Gutenberg UTF-8 text representation."""
    _assert_gutenberg_policy(policy)
    ebook_id = _ebook_id(witness, policy)

    def default_fetch(url: str, timeout_value: float) -> str | None:
        request = Request(url, headers={"User-Agent": "DawnLibrary/1.0 (+https://westsidewatch.github.io/)"})
        try:
            with urlopen(request, timeout=timeout_value) as response:
                content_type = str(response.headers.get("Content-Type") or "").casefold()
                if "text/plain" not in content_type and "application/octet-stream" not in content_type:
                    return None
                data = response.read()
        except (HTTPError, URLError, TimeoutError):
            return None
        text = data.decode("utf-8-sig", errors="replace").strip()
        return text if len(text) >= 256 else None

    loader = fetch or default_fetch
    for url in gutenberg_plain_text_urls(ebook_id):
        text = loader(url, timeout)
        if text:
            return text
    return None
