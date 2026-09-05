#!/usr/bin/env python3
"""Zero-dependency DORÉ Unix-socket JSON-RPC client."""
from __future__ import annotations

import argparse
import json
import socket
import uuid
from pathlib import Path

DEFAULT_SOCKET = Path.home() / ".dore" / "run" / "dore.sock"
MAX_RESPONSE_BYTES = 1024 * 1024


def call(method: str, params: dict | None = None, socket_path: Path = DEFAULT_SOCKET, timeout: float = 15.0) -> dict:
    request = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": method, "params": params or {}}
    raw = (json.dumps(request, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(timeout)
        client.connect(str(socket_path))
        client.sendall(raw)
        chunks = bytearray()
        while b"\n" not in chunks:
            part = client.recv(65536)
            if not part:
                break
            chunks.extend(part)
            if len(chunks) > MAX_RESPONSE_BYTES:
                raise RuntimeError("response too large")
    if not chunks:
        raise RuntimeError("empty response")
    return json.loads(bytes(chunks).split(b"\n", 1)[0].decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", default=str(DEFAULT_SOCKET))
    parser.add_argument("--method", default="dore.health")
    parser.add_argument("--capability")
    parser.add_argument("--args", default="{}")
    ns = parser.parse_args()
    params = json.loads(ns.args)
    method = ns.method
    if ns.capability:
        method = "dore.call"
        params = {"capability": ns.capability, "args": params}
    response = call(method, params, Path(ns.socket).expanduser())
    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0 if "result" in response else 1


if __name__ == "__main__":
    raise SystemExit(main())
