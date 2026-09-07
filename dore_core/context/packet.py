"""Stable, dependency-free serialization boundary for Westside Context packets."""
from __future__ import annotations

from .compiler import ContextNode, ContextPacket


def node_dict(node: ContextNode) -> dict[str, object]:
    return {
        "node_id": node.node_id,
        "title": node.title,
        "level": node.level,
        "parent_id": node.parent_id,
        "content": node.content,
        "source_path": node.source_path,
        "source_sha256": node.source_sha256,
        "ordinal": node.ordinal,
    }


def packet_dict(packet: ContextPacket) -> dict[str, object]:
    """Return an explicit, provenance-preserving packet for a Doré adapter boundary."""
    return {
        "match": node_dict(packet.match),
        "ancestors": [node_dict(node) for node in packet.ancestors],
        "path": [node.node_id for node in packet.ancestors] + [packet.match.node_id],
    }
