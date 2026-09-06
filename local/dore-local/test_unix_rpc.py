#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("unix_rpc_server", ROOT / "unix_rpc_server.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)


def main() -> int:
    health = MOD.dispatch({"jsonrpc": "2.0", "id": "h1", "method": "dore.health", "params": {}})
    result = health["result"]
    assert result["ok"] is True
    assert result["transport"] == "unix-domain-socket"
    assert result["lifecycle"] == "launchd-socket-activation"
    assert result["browser_required"] is False
    assert result["paid_runtime"] is False
    assert "image.generate" in result["production_capabilities"]

    listed = MOD.dispatch({"jsonrpc": "2.0", "id": "l1", "method": "capability.list", "params": {}})
    assert listed["result"]["ok"] is True
    assert listed["result"]["owner"] == "dore-core"
    image = next(x for x in listed["result"]["capabilities"] if x["id"] == "image.generate")
    assert image["callable"] is True
    assert image["provider"] == "dore-image-local"

    resolved = MOD.dispatch({"jsonrpc": "2.0", "id": "r1", "method": "capability.resolve", "params": {"capability": "image.generate"}})
    assert resolved["result"]["ok"] is True
    assert resolved["result"]["descriptor"]["owner"] == "dore-core"
    assert resolved["result"]["descriptor"]["callable"] is True
    assert resolved["result"]["descriptor"]["provider"] == "dore-image-local"

    legacy = MOD.dispatch({
        "jsonrpc": "2.0",
        "id": "c1",
        "method": "dore.payload",
        "params": {"capability": "design2.stage2.acceptance"},
    })
    assert legacy["result"]["ok"] is True
    assert legacy["result"]["status"] == "PASS"

    bad = MOD.dispatch({"jsonrpc": "2.0", "id": "x1", "method": "no.such.method", "params": {}})
    assert bad["error"]["code"] == -32601
    print("DORE_A2A_UNIX_CORE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
