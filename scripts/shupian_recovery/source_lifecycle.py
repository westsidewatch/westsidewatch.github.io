"""PARADISO: stable source identity and failure diagnostics.

Safe public evidence only: do not emit raw stream URLs, query credentials,
cookies, authorization headers, or redirect destinations.
"""
from __future__ import annotations

import hashlib
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit, unquote

_HTTP = re.compile(r"https?://[^\s'\"<>]+", re.I)


def url_fingerprint(url):
    """Full address identity: changed query/token produces a different digest."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]


def path_fingerprint(url):
    """Stable origin/path identity: compare rotating query strings separately."""
    p = urlsplit(url)
    stable = urlunsplit((p.scheme.lower(), (p.hostname or "").lower(), p.path, "", ""))
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()[:24]


def episode_key(provider, title, episode):
    """Exact provider work+episode key for tracking; not a URL identity."""
    norm = lambda x: re.sub(r"\s+", "", str(x)).casefold()
    return "|".join((str(provider), norm(title), norm(episode)))


def equivalent_episode(title, episode, other_title, other_episode):
    """Conservative alternate-source matching; never assume a different season."""
    norm = lambda x: re.sub(r"\s+", "", str(x)).casefold()
    return norm(title) == norm(other_title) and norm(episode) == norm(other_episode)


def sanitized_error(error):
    """Do not expose link tokens/query parameters in the public JSON report."""
    return _HTTP.sub("[redacted-url]", str(error))[:180]


def failure_class(error):
    """Differentiate gone/not found from restricted, transient, and parser errors."""
    if isinstance(error, HTTPError):
        if error.code == 404:
            return "http_404_missing_or_masked"
        if error.code in (401, 403):
            return "http_access_restricted"
        if error.code == 429:
            return "http_rate_limited"
        if error.code in (500, 502, 503, 504):
            return "http_temporary_server_error"
        return "http_other_error"
    if isinstance(error, (TimeoutError, URLError)):
        return "network_error"
    if isinstance(error, (UnicodeError, ValueError)):
        return "parse_or_validation_error"
    return "other_error"


def source_evidence(candidate, prior=None):
    """Persist fingerprint, not URL. Compare only to a matching episode/provider."""
    url = candidate["url"]
    now = url_fingerprint(url)
    path = path_fingerprint(url)
    prev = prior or {}
    prev_hash = prev.get("source_fingerprint")
    prev_path = prev.get("source_path_fingerprint")
    comparison = ("no_comparable_baseline" if not prev_hash
                  else "same_exact_url" if prev_hash == now
                  else "same_path_changed_url" if prev_path == path
                  else "different_url")
    return {"source_fingerprint": now,
            "source_path_fingerprint": path,
            "url_comparison": comparison,
            "previous_manifest": prev.get("manifest", "unknown"),
            "previous_observed_at_utc": prev.get("observed_at_utc")}
