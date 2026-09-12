from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class ReconciledIdentity:
    source: str
    item_type: str | None
    title: str
    creators: tuple[str, ...]
    date: str | None
    publisher: str | None
    isbn: str | None
    doi: str | None
    url: str | None
    library_catalog: str | None

    @property
    def authority_ids(self) -> dict[str, str]:
        ids: dict[str, str] = {}
        if self.isbn:
            ids['isbn'] = self.isbn
        if self.doi:
            ids['doi'] = self.doi
        return ids


class ZoteroTranslationAdapter:
    """Thin client for the official Zotero translation-server contract."""

    def __init__(self, base_url: str = 'http://127.0.0.1:1969', timeout: float = 30.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def search_identifier(self, identifier: str) -> list[ReconciledIdentity]:
        return self._translate('/search', identifier)

    def translate_web(self, url: str) -> list[ReconciledIdentity]:
        return self._translate('/web', url)

    def _translate(self, endpoint: str, value: str) -> list[ReconciledIdentity]:
        payload = str(value or '').strip()
        if not payload:
            return []
        req = Request(
            f'{self.base_url}{endpoint}',
            data=payload.encode('utf-8'),
            method='POST',
            headers={'Content-Type': 'text/plain; charset=utf-8', 'Accept': 'application/json'},
        )
        with urlopen(req, timeout=self.timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
        if not isinstance(data, list):
            return []
        return [self._identity(item) for item in data if isinstance(item, dict) and item.get('title')]

    @staticmethod
    def _identity(item: dict[str, Any]) -> ReconciledIdentity:
        creators: list[str] = []
        for creator in item.get('creators') or []:
            if not isinstance(creator, dict):
                continue
            literal = str(creator.get('name') or '').strip()
            if literal:
                creators.append(literal)
                continue
            first = str(creator.get('firstName') or '').strip()
            last = str(creator.get('lastName') or '').strip()
            full = ' '.join(part for part in (first, last) if part)
            if full:
                creators.append(full)
        return ReconciledIdentity(
            source='zotero-translation-server',
            item_type=item.get('itemType'),
            title=str(item.get('title') or '').strip(),
            creators=tuple(creators),
            date=(str(item.get('date')).strip() if item.get('date') else None),
            publisher=(str(item.get('publisher')).strip() if item.get('publisher') else None),
            isbn=(str(item.get('ISBN')).strip() if item.get('ISBN') else None),
            doi=(str(item.get('DOI')).strip() if item.get('DOI') else None),
            url=(str(item.get('url')).strip() if item.get('url') else None),
            library_catalog=(str(item.get('libraryCatalog')).strip() if item.get('libraryCatalog') else None),
        )
