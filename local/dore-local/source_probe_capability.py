#!/usr/bin/env python3
"""Doré Universal Source Probe v0.

Standard-first media discovery for arbitrary URLs. The probe is intentionally
provider-neutral and ephemeral: it discovers source capabilities, provenance,
and confidence but does not persist media or become source authority.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

SCHEMA = "dore.source-probe.v0"
BANNED_HOST_SUFFIXES = ("wikisource.org",)


class ProbeHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.videos: list[dict[str, str]] = []
        self.sources: list[dict[str, str]] = []
        self.tracks: list[dict[str, str]] = []
        self.iframes: list[dict[str, str]] = []
        self._jsonld = False
        self._jsonld_buffer: list[str] = []
        self.jsonld: list[Any] = []

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {str(k).lower(): str(v or "") for k, v in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = self._attrs(attrs)
        tag = tag.lower()
        if tag == "meta":
            self.meta.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "video":
            self.videos.append(a)
        elif tag == "source":
            self.sources.append(a)
        elif tag == "track":
            self.tracks.append(a)
        elif tag == "iframe":
            self.iframes.append(a)
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._jsonld = True
            self._jsonld_buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._jsonld:
            raw = "".join(self._jsonld_buffer).strip()
            if raw:
                try:
                    self.jsonld.append(json.loads(raw))
                except json.JSONDecodeError:
                    pass
            self._jsonld = False
            self._jsonld_buffer = []

    def handle_data(self, data: str) -> None:
        if self._jsonld:
            self._jsonld_buffer.append(data)


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().rstrip(".")


def _source_allowed(url: str) -> bool:
    host = _host(url)
    return bool(host) and not any(host == suffix or host.endswith("." + suffix) for suffix in BANNED_HOST_SUFFIXES)


def _abs(base: str, value: str | None) -> str | None:
    value = str(value or "").strip()
    return urljoin(base, value) if value else None


def _walk_json(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_json(child)


def _values(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v) for v in value if isinstance(v, (str, int, float))]
    if isinstance(value, dict):
        for key in ("url", "contentUrl", "embedUrl"):
            if value.get(key):
                return [str(value[key])]
    return []


def _add(bucket: list[dict[str, Any]], value: str | None, source: str, confidence: float, **extra: Any) -> None:
    if not value:
        return
    item = {"url": value, "source": source, "confidence": confidence}
    item.update({k: v for k, v in extra.items() if v not in (None, "")})
    if not any(x.get("url") == value for x in bucket):
        bucket.append(item)


def _meta_map(parser: ProbeHTMLParser) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in parser.meta:
        key = (item.get("property") or item.get("name") or "").lower()
        content = item.get("content") or ""
        if key and content and key not in out:
            out[key] = content
    return out


def _fetch(url: str, timeout: int) -> tuple[str, str, str]:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/140 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.7",
        "Referer": f"https://{_host(url)}/",
    })
    with urlopen(req, timeout=timeout) as response:
        body = response.read(3_000_000).decode(response.headers.get_content_charset() or "utf-8", errors="replace")
        return response.geturl(), str(response.headers.get("Content-Type") or ""), body


def _runtime_boundary(url: str, code: int | None, message: str) -> dict[str, Any]:
    return {
        "ok": True,
        "status": "partial",
        "schema": SCHEMA,
        "profile": "media",
        "sourcePointer": url,
        "resolvedSourcePointer": url,
        "sourceAuthority": True,
        "probeAuthority": False,
        "reflexPersistent": False,
        "providerHint": _host(url),
        "identity": {"title": None, "creator": None, "duration": None},
        "capabilities": {"poster": [], "embed": [], "media": [], "manifest": [], "caption": [], "oembed": []},
        "needs": ["runtime-browser-probe", "generic-media-extractor", "caption-or-asr-resolution"],
        "provenance": {
            "networkUsed": True,
            "fetchBoundary": {"httpStatus": code, "message": message},
            "layers": ["source-policy", "standard-metadata", "static-media", "generic-extractor-fallback", "runtime-browser-fallback", "provider-adapter-last"],
            "confidence": 0.25,
        },
        "rights": {"rehost": False, "decision": "not-inferred-by-probe"},
    }


def execute(args: dict[str, Any]) -> dict[str, Any]:
    url = str(args.get("url") or args.get("sourcePointer") or "").strip()
    if not url:
        return {"ok": False, "status": "failed", "error": {"code": "invalid_args", "message": "url or sourcePointer is required"}}
    if not _source_allowed(url):
        return {"ok": False, "status": "blocked", "schema": SCHEMA, "sourcePointer": url, "sourcePolicy": {"allowed": False, "reason": "source-policy-deny"}}

    html = args.get("html")
    final_url = url
    content_type = str(args.get("contentType") or "")
    network_used = False
    if html is None:
        if not bool(args.get("allowNetwork", False)):
            return {"ok": False, "status": "not_ready", "schema": SCHEMA, "sourcePointer": url, "error": {"code": "html_or_network_required", "message": "provide html or allowNetwork=true"}}
        try:
            final_url, content_type, html = _fetch(url, int(args.get("timeoutSeconds") or 20))
            network_used = True
        except HTTPError as exc:
            if int(exc.code) in (401, 403, 405, 406, 429):
                return _runtime_boundary(url, int(exc.code), str(exc))
            return {"ok": False, "status": "failed", "schema": SCHEMA, "sourcePointer": url, "error": {"code": "source_fetch_failed", "message": str(exc)}}
        except Exception as exc:
            return _runtime_boundary(url, None, str(exc))

    parser = ProbeHTMLParser()
    parser.feed(str(html or ""))
    meta = _meta_map(parser)
    poster: list[dict[str, Any]] = []
    embed: list[dict[str, Any]] = []
    media: list[dict[str, Any]] = []
    captions: list[dict[str, Any]] = []
    oembed: list[dict[str, Any]] = []

    for key, confidence in (("og:image", 0.93), ("twitter:image", 0.86), ("twitter:image:src", 0.86)):
        _add(poster, _abs(final_url, meta.get(key)), key, confidence)
    for video in parser.videos:
        _add(poster, _abs(final_url, video.get("poster")), "html-video-poster", 0.95)
        _add(media, _abs(final_url, video.get("src")), "html-video-src", 0.95, mime=video.get("type"))
    for source in parser.sources:
        _add(media, _abs(final_url, source.get("src")), "html-source", 0.94, mime=source.get("type"))
    for track in parser.tracks:
        kind = (track.get("kind") or "").lower()
        if kind in ("subtitles", "captions"):
            _add(captions, _abs(final_url, track.get("src")), "html-track", 0.98, language=track.get("srclang"), label=track.get("label"), kind=kind)
    for frame in parser.iframes:
        _add(embed, _abs(final_url, frame.get("src")), "html-iframe", 0.78)
    for link in parser.links:
        rel = (link.get("rel") or "").lower()
        typ = (link.get("type") or "").lower()
        if "alternate" in rel and "oembed" in typ:
            _add(oembed, _abs(final_url, link.get("href")), "oembed-discovery", 0.99, mime=typ)

    title = meta.get("og:title") or meta.get("twitter:title") or ""
    creator = ""
    duration = None
    for root in parser.jsonld:
        for node in _walk_json(root):
            node_type = node.get("@type")
            types = node_type if isinstance(node_type, list) else [node_type]
            if "VideoObject" not in types:
                continue
            title = str(node.get("name") or title or "")
            author = node.get("author") or node.get("creator")
            if isinstance(author, dict):
                creator = str(author.get("name") or creator or "")
            elif isinstance(author, str):
                creator = author
            duration = node.get("duration") or duration
            for value in _values(node.get("thumbnailUrl")):
                _add(poster, _abs(final_url, value), "jsonld-videoobject-thumbnail", 0.99)
            for value in _values(node.get("embedUrl")):
                _add(embed, _abs(final_url, value), "jsonld-videoobject-embed", 0.99)
            for value in _values(node.get("contentUrl")):
                _add(media, _abs(final_url, value), "jsonld-videoobject-content", 0.99)
            for key in ("caption", "transcript"):
                for value in _values(node.get(key)):
                    if value.startswith("http://") or value.startswith("https://") or value.startswith("/"):
                        _add(captions, _abs(final_url, value), f"jsonld-videoobject-{key}", 0.90, kind=key)

    manifests = []
    for item in media:
        lower = item["url"].lower().split("?", 1)[0]
        if lower.endswith(".m3u8"):
            manifests.append({**item, "manifest": "hls"})
        elif lower.endswith(".mpd"):
            manifests.append({**item, "manifest": "dash"})

    needs: list[str] = []
    if not poster:
        needs.append("runtime-browser-probe")
    if not embed and not media:
        needs.append("generic-media-extractor")
    if not captions:
        needs.append("caption-or-asr-resolution")

    score = max([x["confidence"] for group in (poster, embed, media, captions, oembed) for x in group] or [0.25])
    return {
        "ok": True,
        "status": "completed",
        "schema": SCHEMA,
        "profile": "media",
        "sourcePointer": url,
        "resolvedSourcePointer": final_url,
        "sourceAuthority": True,
        "probeAuthority": False,
        "reflexPersistent": False,
        "providerHint": _host(final_url),
        "identity": {"title": title or None, "creator": creator or None, "duration": duration},
        "capabilities": {"poster": poster, "embed": embed, "media": media, "manifest": manifests, "caption": captions, "oembed": oembed},
        "needs": needs,
        "provenance": {
            "networkUsed": network_used,
            "contentType": content_type,
            "layers": ["source-policy", "standard-metadata", "static-media", "generic-extractor-fallback", "runtime-browser-fallback", "provider-adapter-last"],
            "confidence": round(float(score), 3),
        },
        "rights": {"rehost": False, "decision": "not-inferred-by-probe"},
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--network", action="store_true")
    ns = p.parse_args()
    print(json.dumps(execute({"url": ns.url, "allowNetwork": ns.network}), ensure_ascii=False, indent=2))
