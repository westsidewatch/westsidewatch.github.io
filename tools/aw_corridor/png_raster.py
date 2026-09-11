#!/usr/bin/env python3
"""Minimal 8-bit non-interlaced PNG raster codec for AW-011 production gates."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class RasterError(ValueError):
    pass


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png(path: Path) -> tuple[int, int, int, bytes]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise RasterError(f"not a PNG: {path}")
    pos = len(PNG_SIGNATURE)
    width = height = bit_depth = color_type = interlace = None
    compressed = bytearray()
    saw_iend = False
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos+4])[0]
        ctype = data[pos+4:pos+8]
        payload = data[pos+8:pos+8+length]
        if pos + 12 + length > len(data):
            raise RasterError(f"truncated PNG chunk: {path}")
        pos += 12 + length
        if ctype == b"IHDR":
            if length != 13:
                raise RasterError("invalid IHDR")
            width, height, bit_depth, color_type, comp, filt, interlace = struct.unpack(">IIBBBBB", payload)
            if comp != 0 or filt != 0:
                raise RasterError("unsupported PNG compression/filter method")
        elif ctype == b"IDAT":
            compressed.extend(payload)
        elif ctype == b"IEND":
            saw_iend = True
            break
    if None in (width, height, bit_depth, color_type, interlace) or not saw_iend:
        raise RasterError(f"incomplete PNG: {path}")
    if bit_depth != 8 or color_type not in (0, 2, 4, 6) or interlace != 0:
        raise RasterError("PNG must be 8-bit non-interlaced grayscale/RGB/GA/RGBA")
    channels = {0:1, 2:3, 4:2, 6:4}[color_type]
    raw = zlib.decompress(bytes(compressed))
    stride = width * channels
    if len(raw) != height * (stride + 1):
        raise RasterError(f"unexpected decompressed PNG size: {path}")
    out = bytearray(width * height * channels)
    offset = 0
    dst = 0
    prev = bytearray(stride)
    for _ in range(height):
        filter_type = raw[offset]
        offset += 1
        scan = raw[offset:offset+stride]
        offset += stride
        recon = bytearray(stride)
        for i, value in enumerate(scan):
            left = recon[i-channels] if i >= channels else 0
            above = prev[i]
            upper_left = prev[i-channels] if i >= channels else 0
            if filter_type == 0:
                decoded = value
            elif filter_type == 1:
                decoded = (value + left) & 255
            elif filter_type == 2:
                decoded = (value + above) & 255
            elif filter_type == 3:
                decoded = (value + ((left + above)//2)) & 255
            elif filter_type == 4:
                decoded = (value + _paeth(left, above, upper_left)) & 255
            else:
                raise RasterError(f"unsupported PNG filter {filter_type}: {path}")
            recon[i] = decoded
        out[dst:dst+stride] = recon
        dst += stride
        prev = recon
    return width, height, channels, bytes(out)


def _chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)


def write_png(path: Path, width: int, height: int, channels: int, pixels: bytes) -> None:
    if width <= 0 or height <= 0 or channels not in (1, 2, 3, 4):
        raise RasterError("invalid raster geometry")
    if len(pixels) != width * height * channels:
        raise RasterError("pixel byte length does not match raster geometry")
    color_type = {1:0, 2:4, 3:2, 4:6}[channels]
    raw = bytearray()
    stride = width * channels
    for y in range(height):
        raw.append(0)
        raw.extend(pixels[y*stride:(y+1)*stride])
    data = bytearray(PNG_SIGNATURE)
    data.extend(_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)))
    data.extend(_chunk(b"IDAT", zlib.compress(bytes(raw))))
    data.extend(_chunk(b"IEND", b""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(data))
