#!/usr/bin/env python3
"""Doré Universal Source Enumerator v1.

Provider-neutral 1→N expansion ahead of the frozen Universal Source Contract.
It emits source pointers only; it is not identity, rights, editorial, or persistence authority.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlparse

SCHEMA = "dore.source-enumeration.v1"
EVIDENCE = {"link", "structured-data", "api", "feed", "sitemap", "manifest", "pagination"}


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        values = dict(attrs)
        self._href = values.get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join("".join(self._text).split())))
            self._href = None
            self._text = []


def _pointer(url: str, root: str, evidence: str, provider_id: str | None = None, label: str | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {"sourceUrl": url, "discoveredFrom": root, "evidence": evidence}
    if provider_id:
        item["providerId"] = provider_id
    if label:
        item["label"] = label
    return item


def _dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for item in items:
        key = (str(item.get("providerId") or ""), str(item.get("sourceUrl") or ""))
        if not key[1] or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def enumerate_collection(args: dict[str, Any]) -> dict[str, Any]:
    root = str(args.get("sourceUrl") or "").strip()
    if not root:
        return {"ok": False, "schema": SCHEMA, "status": "failed", "reason": "source-url-required"}

    items: list[dict[str, Any]] = []
    continuation: dict[str, Any] | None = None

    records = args.get("records")
    if isinstance(records, list):
        for record in records:
            if not isinstance(record, dict):
                continue
            url = record.get("sourceUrl") or record.get("url") or record.get("href")
            if not url:
                continue
            evidence = str(record.get("evidence") or "api")
            if evidence not in EVIDENCE:
                evidence = "api"
            items.append(_pointer(urljoin(root, str(url)), root, evidence, str(record.get("id") or record.get("providerId") or "") or None, str(record.get("label") or record.get("title") or "") or None))

    manifest = args.get("manifest")
    if isinstance(manifest, dict):
        members = manifest.get("items") or manifest.get("members") or manifest.get("entries") or []
        if isinstance(members, list):
            for member in members:
                if isinstance(member, str):
                    items.append(_pointer(urljoin(root, member), root, "manifest"))
                elif isinstance(member, dict):
                    url = member.get("id") or member.get("url") or member.get("href")
                    if url:
                        items.append(_pointer(urljoin(root, str(url)), root, "manifest", str(member.get("providerId") or "") or None, str(member.get("label") or member.get("title") or "") or None))

    html = args.get("html")
    if isinstance(html, str) and html:
        parser = _Links()
        parser.feed(html)
        root_host = urlparse(root).netloc
        for href, label in parser.links:
            url = urljoin(root, href)
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"}:
                continue
            # Enumeration may follow external resource links, but skips empty/self anchors.
            if url.split("#", 1)[0] == root.split("#", 1)[0]:
                continue
            items.append(_pointer(url, root, "link", label=label or None))

    next_url = args.get("next") or args.get("nextUrl")
    if next_url:
        continuation = {"sourceUrl": urljoin(root, str(next_url)), "evidence": "pagination"}

    items = _dedupe(items)
    limit = args.get("limit")
    if isinstance(limit, int) and limit > 0 and len(items) > limit:
        continuation = continuation or {"offset": limit, "evidence": "pagination"}
        items = items[:limit]

    return {
        "ok": True,
        "schema": SCHEMA,
        "status": "ready",
        "sourcePointer": root,
        "count": len(items),
        "items": items,
        "continuation": continuation,
        "authority": False,
        "rightsAuthority": False,
        "canonicalIdentityAuthority": False,
        "providerSpecificRouting": False,
        "persistence": "request-scoped-none",
        "storesSourceMedia": False,
    }


def execute(args: dict[str, Any]) -> dict[str, Any]:
    return enumerate_collection(args)


if __name__ == "__main__":
    import sys
    payload = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(execute(payload), ensure_ascii=False, indent=2))
