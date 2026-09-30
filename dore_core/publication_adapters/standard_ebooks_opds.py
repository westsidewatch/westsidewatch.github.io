"""Resolve Standard Ebooks EPUB acquisition through its OPDS catalog.

The catalog, not a guessed download filename, is authoritative for the EPUB
acquisition URL. This follows the normal OPDS reader flow: discover entry ->
select application/epub+zip acquisition link -> fetch publication.
"""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

OPDS_ROOT = "https://standardebooks.org/feeds/opds"
ATOM = "{http://www.w3.org/2005/Atom}"
OPDS_ACQUISITION = "http://opds-spec.org/acquisition"


@dataclass(frozen=True)
class StandardEbooksAcquisition:
    identifier: str
    title: str
    epub_url: str
    media_type: str = "application/epub+zip"


def _read(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Dore-Dawn-Library/1.0 (+https://westsidewatch.github.io/)"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def _entry_identifier(entry: ET.Element) -> str:
    node = entry.find(f"{ATOM}id")
    return (node.text or "").strip() if node is not None else ""


def _entry_title(entry: ET.Element) -> str:
    node = entry.find(f"{ATOM}title")
    return (node.text or "").strip() if node is not None else ""


def _epub_link(entry: ET.Element, base_url: str) -> str | None:
    candidates: list[tuple[int, str]] = []
    for link in entry.findall(f"{ATOM}link"):
        if link.get("rel") != OPDS_ACQUISITION or link.get("type") != "application/epub+zip":
            continue
        href = link.get("href")
        if not href:
            continue
        label = " ".join(filter(None, (link.get("title"), link.get("properties")))).casefold()
        # Prefer the broadly compatible build when a catalog exposes variants.
        score = 0 if "compatible" in label else 1
        candidates.append((score, urljoin(base_url, href)))
    return sorted(candidates)[0][1] if candidates else None


def find_standard_ebooks_epub(identifier: str, *, feed_url: str = OPDS_ROOT) -> StandardEbooksAcquisition:
    """Find a Standard Ebooks acquisition link without guessing file paths.

    ``identifier`` is the Standard Ebooks slug stored in Dawn authorityIds,
    e.g. ``jane-austen/pride-and-prejudice``. OPDS pagination/navigation is
    followed until a matching entry is found.
    """
    target = identifier.removeprefix("https://standardebooks.org/ebooks/").strip("/")
    if not target or ".." in target:
        raise ValueError("invalid Standard Ebooks identifier")

    wanted_url = f"https://standardebooks.org/ebooks/{target}"
    queue = [feed_url]
    seen: set[str] = set()
    while queue:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        root = ET.fromstring(_read(url))
        for entry in root.findall(f"{ATOM}entry"):
            entry_id = _entry_identifier(entry)
            alternate = next((urljoin(url, l.get("href")) for l in entry.findall(f"{ATOM}link") if l.get("rel") == "alternate" and l.get("href")), "")
            if wanted_url not in {entry_id.rstrip("/"), alternate.rstrip("/")}:
                continue
            epub = _epub_link(entry, url)
            if not epub:
                raise LookupError(f"Standard Ebooks entry has no EPUB acquisition: {target}")
            return StandardEbooksAcquisition(target, _entry_title(entry), epub)
        # Follow only explicit OPDS pagination; never crawl arbitrary links.
        for link in root.findall(f"{ATOM}link"):
            if link.get("rel") in {"next"} and link.get("href"):
                queue.append(urljoin(url, link.get("href")))
    raise LookupError(f"Standard Ebooks OPDS entry not found: {target}")


def load_standard_ebooks_epub(acquisition: StandardEbooksAcquisition) -> bytes:
    if not acquisition.epub_url.startswith("https://standardebooks.org/"):
        raise ValueError("refusing non-Standard-Ebooks acquisition host")
    payload = _read(acquisition.epub_url)
    if len(payload) < 1024 or not payload.startswith(b"PK"):
        raise ValueError("Standard Ebooks acquisition did not return a valid EPUB container")
    return payload
