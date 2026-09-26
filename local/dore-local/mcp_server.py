#!/usr/bin/env python3
"""Thin MCP exposure layer for Doré conversation gateway.

This module owns no capability execution. All requests are delegated to
conversation_gateway.dispatch(), preserving the existing A2A boundary.
"""
from __future__ import annotations

import json
import sys
from typing import Any

import conversation_gateway


def handle(request: dict[str, Any]) -> dict[str, Any]:
    return conversation_gateway.dispatch(request)


def tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": "dore_discover",
            "description": "Discover available Doré capabilities.",
            "inputSchema": {"type": "object"},
        },
        {
            "name": "dore_describe",
            "description": "Describe a Doré capability contract.",
            "inputSchema": {"type": "object", "required": ["capability"]},
        },
        {
            "name": "dore_call",
            "description": "Call an approved Doré capability through the existing gateway.",
            "inputSchema": {"type": "object", "required": ["capability", "args"]},
        },
    ]


def main() -> int:
    for line in sys.stdin:
        request = json.loads(line)
        response = handle(request)
        print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
