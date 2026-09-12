"""Narrow browser-to-Core transport for product-facing local capabilities.

This module deliberately does not expose Capability Bus as a generic browser RPC.
Only explicitly reviewed product capabilities may cross this boundary.
"""

import capability_bus
import production_actions

BROWSER_CAPABILITY_ALLOWLIST = frozenset({
    "publishing.book-intelligence",
})


def call_browser_capability(payload):
    if not isinstance(payload, dict):
        return {"ok": False, "error": "invalid_payload"}, 400

    capability = str(payload.get("capability") or "").strip()
    if capability not in BROWSER_CAPABILITY_ALLOWLIST:
        return {"ok": False, "error": "capability_not_allowed"}, 403

    args = payload.get("args")
    if not isinstance(args, dict):
        return {"ok": False, "error": "invalid_args"}, 400

    try:
        result = capability_bus.call(
            capability,
            args,
            production_actions,
            caller_product="multiwrite",
        )
    except Exception:
        return {"ok": False, "error": "capability_call_failed"}, 500

    if not isinstance(result, dict):
        return {"ok": False, "error": "invalid_capability_response"}, 502

    # Keep the Core response shape intact for reviewed capabilities while
    # preventing caller-controlled routing identity from entering Core.
    status = 200 if result.get("ok") else 502
    return result, status
