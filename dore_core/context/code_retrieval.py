"""Dependency-free local code retrieval for Doré Context Economy.

Lexical/symbol retrieval is intentionally the v0 default: zero API cost, deterministic,
and small enough to sit in front of Codex. External semantic engines can be adapters
later; they must not become a new authority layer.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_\-]*|[\u3400-\u9fff]{2,}")
TEXT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".md", ".json", ".yml", ".yaml"}

@dataclass(frozen=True)
class CodeHit:
    path: str
    score: float
    symbols: tuple[str, ...]
    excerpt: str
    bytes_returned: int

def _terms(value: str) -> set[str]:
    return {term.lower() for term in WORD_RE.findall(value)}

def python_symbols(text: str) -> tuple[str, ...]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return ()
    names = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(node.name)
    return tuple(dict.fromkeys(names))

def _symbols(path: Path, text: str) -> tuple[str, ...]:
    if path.suffix == ".py":
        return python_symbols(text)
    # Cheap cross-language symbol hints; no external parser dependency in v0.
    candidates = re.findall(r"(?:function|class|const|let|var)\s+([A-Za-z_$][\w$]*)", text)
    return tuple(dict.fromkeys(candidates))

def candidate_files(root: Path, *, include: Iterable[str] = ()) -> list[Path]:
    explicit = [root / item for item in include]
    if explicit:
        return [p for p in explicit if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES]
    # No implicit whole-repository walk: callers must resolve a surface first.
    return []

def retrieve_code(query: str, files: Iterable[Path], *, limit: int = 6, excerpt_chars: int = 1800) -> list[CodeHit]:
    q = _terms(query)
    hits: list[CodeHit] = []
    for path in files:
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        symbols = _symbols(path, text)
        path_terms = _terms(str(path))
        symbol_terms = _terms(" ".join(symbols))
        text_terms = _terms(text[:120_000])
        score = 6 * len(q & symbol_terms) + 3 * len(q & path_terms) + len(q & text_terms)
        if score <= 0:
            continue
        excerpt = _best_excerpt(text, q, excerpt_chars)
        hits.append(CodeHit(str(path), float(score), symbols, excerpt, len(excerpt.encode("utf-8"))))
    hits.sort(key=lambda hit: (-hit.score, hit.bytes_returned, hit.path))
    return hits[: max(0, limit)]

def _best_excerpt(text: str, terms: set[str], width: int) -> str:
    lowered = text.lower()
    positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
    start = max(0, (min(positions) if positions else 0) - width // 4)
    return text[start:start + width]
