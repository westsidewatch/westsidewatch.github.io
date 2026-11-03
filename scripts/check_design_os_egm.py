#!/usr/bin/env python3
"""Check source integration ONLY; never fake an actual isolated agent review."""
from __future__ import annotations

import configparser
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ".tools/elephant-goldfish-model"
URL = "https://github.com/google/elephant-goldfish-model.git"
DOC = "docs/design/WESTSIDE-EGM-INTEGRATION.md"


def die(message: str) -> None:
    print("EGM / Design OS integration FAIL:", message, file=sys.stderr)
    raise SystemExit(1)


def text(path: str) -> str:
    file = ROOT / path
    if not file.is_file():
        die(f"missing {path}")
    return file.read_text(encoding="utf-8")


def main() -> None:
    parser = configparser.ConfigParser()
    parser.read_string(text(".gitmodules"))
    section = f'submodule "{SOURCE}"'
    if section not in parser:
        die("EGM submodule metadata not registered")
    if parser[section].get("path") != SOURCE or parser[section].get("url") != URL:
        die("unexpected EGM upstream path or URL")
    try:
        tree = subprocess.run(
            ["git", "ls-tree", "HEAD", "--", SOURCE],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as e:
        die(f"cannot inspect pinned gitlink: {e}")
    if not re.fullmatch(r"160000 commit [0-9a-f]{40}\t" + re.escape(SOURCE), tree):
        die("EGM source must be a pinned Git submodule commit, not a floating ref")
    agent = text("AGENTS.md")
    protocol = text(DOC)
    os_document = text("docs/design/WESTSIDE-DESIGN-OS.md")
    manual = text("docs/design/WESTSIDE-EDITORIAL-MANUAL.md")
    setup = text("scripts/egm-setup.sh")
    if "EGM artifact directory: .dev/egm" not in agent:
        die("agent artifact direction is missing")
    if DOC not in agent or DOC.split("/")[-1] not in os_document:
        die("EGM is not discoverable from the canonical Design OS entrypoints")
    if "fresh isolated" not in protocol.lower() or "Goldfish" not in manual:
        die("independent reviewer requirements are not registered")
    for part in ("--prepare", "--check", "--install-codex",
                 "codex plugin marketplace add google/elephant-goldfish-model",
                 "codex plugin add egm@egm"):
        if part not in setup:
            die("official Codex setup contract missing " + part)
    print("Westside Design OS / upstream EGM source integration: PASS")
    print("NOTE: This is source wiring only, NOT a live Goldfish review.")


if __name__ == "__main__":
    main()
