"""Bound tool/browser/build output and reuse verified state when inputs are unchanged."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True)
class OutputDigest:
    head: str
    tail: str
    omitted_bytes: int
    original_bytes: int

@dataclass(frozen=True)
class VerifiedState:
    key: str
    input_fingerprint: str
    verification: str
    passed: bool

def compress_output(text: str, *, max_bytes: int = 12000) -> OutputDigest:
    raw = text.encode("utf-8")
    if len(raw) <= max_bytes:
        return OutputDigest(text, "", 0, len(raw))
    half = max_bytes // 2
    head = raw[:half].decode("utf-8", errors="ignore")
    tail = raw[-half:].decode("utf-8", errors="ignore")
    kept = len(head.encode("utf-8")) + len(tail.encode("utf-8"))
    return OutputDigest(head, tail, max(0, len(raw) - kept), len(raw))

def fingerprint_inputs(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda p: str(p)):
        digest.update(str(path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()

def can_reuse_verified(state: VerifiedState, paths: Iterable[Path]) -> bool:
    return state.passed and state.input_fingerprint == fingerprint_inputs(paths)

def browser_text_budget(text: str, *, max_bytes: int = 16000) -> OutputDigest:
    """Browser/accessibility text uses the same bounded evidence contract."""
    return compress_output(text, max_bytes=max_bytes)
