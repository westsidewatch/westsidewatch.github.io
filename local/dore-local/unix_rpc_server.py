#!/usr/bin/env python3
"""DORÉ local A2A control plane over a launchd-activated Unix domain socket."""
from __future__ import annotations

import asyncio
import ctypes
import json
import os
import socket
from pathlib import Path

import native_host

PROTOCOL = "dore.a2a/1"
SERVICE = "dore-a2a-unix"
SOCKET_KEY = b"DoreA2A"
MAX_LINE_BYTES = 1024 * 1024


def _launchd_socket() -> socket.socket:
    """Claim the socket prepared by launchd via launch_activate_socket(3)."""
    libc = ctypes.CDLL(None)
    activate = libc.launch_activate_socket
    activate.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.POINTER(ctypes.c_size_t)]
    activate.restype = ctypes.c_int
    fds = ctypes.POINTER(ctypes.c_int)()
    count = ctypes.c_size_t(0)
    rc = activate(SOCKET_KEY, ctypes.byref(fds), ctypes.byref(count))
    if rc != 0 or count.value != 1:
        raise RuntimeError(f"launch_activate_socket failed rc={rc} count={count.value}")
    fd = int(fds[0])
    libc.free(fds)
    sock = socket.socket(fileno=fd)
    sock.setblocking(False)
    return sock


def _peer_uid(fd: int) -> int | None:
    """Read the peer euid from a connected BSD socket on macOS."""
    libc = ctypes.CDLL(None)
    fn = getattr(libc, "getpeereid", None)
    if fn is None:
        return None
    euid = ctypes.c_uint(0)
    egid = ctypes.c_uint(0)
    fn.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint)]
    fn.restype = ctypes.c_int
    if fn(fd, ctypes.byref(euid), ctypes.byref(egid)) != 0:
        return None
    return int(euid.value)


def _peer_allowed(writer: asyncio.StreamWriter) -> bool:
    sock = writer.get_extra_info("socket")
    if sock is None:
        return False
    uid = _peer_uid(sock.fileno())
    if uid is None:
        # CI and non-macOS contract tests do not have getpeereid(3); the actual
        # production target is macOS where failure to resolve the peer is deny.
        return os.uname().sysname != "Darwin"
    return uid == os.getuid()


def _jsonrpc_error(request_id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def dispatch(request: dict) -> dict:
    request_id = request.get("id")
    if request.get("jsonrpc") != "2.0":
        return _jsonrpc_error(request_id, -32600, "invalid request")
    method = request.get("method")
    params = request.get("params") or {}
    if not isinstance(params, dict):
        return _jsonrpc_error(request_id, -32602, "params must be an object")

    if method in {"dore.health", "health"}:
        result = {
            "ok": True,
            "service": SERVICE,
            "protocol": PROTOCOL,
            "transport": "unix-domain-socket",
            "lifecycle": "launchd-socket-activation",
            "socket": "~/.dore/run/dore.sock",
            "browser_required": False,
            "paid_runtime": False,
            "production_capabilities": sorted(native_host.PRODUCTION.CAPABILITIES),
        }
    elif method in {"dore.call", "capability.call"}:
        capability = str(params.get("capability") or "")
        if not capability:
            return _jsonrpc_error(request_id, -32602, "capability is required")
        payload = {
            "capability": capability,
            "args": params.get("args") or {},
            "conversation_id": params.get("conversation_id"),
            "session_id": params.get("session_id"),
            "request_id": params.get("request_id"),
        }
        result = native_host.route_payload(payload)
    elif method == "dore.payload":
        result = native_host.route_payload(params)
    else:
        return _jsonrpc_error(request_id, -32601, f"method not found: {method}")
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


async def _handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        if not _peer_allowed(writer):
            writer.write((json.dumps(_jsonrpc_error(None, -32001, "peer uid rejected")) + "\n").encode())
            await writer.drain()
            return
        while True:
            raw = await reader.readline()
            if not raw:
                return
            if len(raw) > MAX_LINE_BYTES:
                response = _jsonrpc_error(None, -32000, "request too large")
            else:
                try:
                    request = json.loads(raw.decode("utf-8"))
                    response = dispatch(request) if isinstance(request, dict) else _jsonrpc_error(None, -32600, "invalid request")
                except Exception as exc:
                    response = _jsonrpc_error(None, -32603, str(exc))
            writer.write((json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8"))
            await writer.drain()
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass


async def main() -> None:
    sock = _launchd_socket()
    server = await asyncio.start_unix_server(_handle, sock=sock)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
