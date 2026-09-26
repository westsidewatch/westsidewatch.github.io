#!/usr/bin/env python3
"""Minimal MCP JSON-RPC exposure for Doré gateway.

This layer only exposes existing gateway capabilities. Execution remains in
conversation_gateway -> A2A -> capability bus.
"""
from __future__ import annotations

import json
import sys
from typing import Any

import conversation_gateway


def result(request_id: Any, value: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": value}


def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def tools() -> list[dict[str, Any]]:
    return [
        {"name": "dore_discover", "description": "Discover Doré capabilities", "inputSchema": {"type": "object"}},
        {"name": "dore_describe", "description": "Describe Doré capability", "inputSchema": {"type": "object", "required": ["capability"]}},
        {"name": "dore_call", "description": "Call approved Doré capability", "inputSchema": {"type": "object", "required": ["capability", "args"]}},
    ]


def dispatch(message: dict[str, Any]) -> dict[str, Any]:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        return result(request_id, {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}})
    if method == "tools/list":
        return result(request_id, {"tools": tools()})
    if method == "tools/call":
        params = message.get("params", {})
        return result(request_id, conversation_gateway.dispatch({"operation": "call", **params}))
    return error(request_id, -32601, f"unknown method: {method}")


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            print(json.dumps(dispatch(json.loads(line)), ensure_ascii=False), flush=True)
        except Exception as exc:
            print(json.dumps(error(None, -32000, str(exc)), ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
