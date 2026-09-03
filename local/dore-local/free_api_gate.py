#!/usr/bin/env python3
"""Fail-closed policy gate for Doré network providers."""
from __future__ import annotations

import datetime
import json
import os
from pathlib import Path


class FreeApiPolicyError(RuntimeError):
    pass


def validate(policy: dict) -> None:
    required = {
        "provider",
        "billing",
        "credentials",
        "paid_fallback",
        "daily_request_limit",
        "per_call_result_limit",
    }
    missing = sorted(required - policy.keys())
    if missing:
        raise FreeApiPolicyError("missing_policy_fields:" + ",".join(missing))
    if policy["billing"] != "free-only":
        raise FreeApiPolicyError("provider_not_free_only")
    if policy["paid_fallback"] is not False:
        raise FreeApiPolicyError("paid_fallback_forbidden")
    if policy["credentials"] not in {"none", "optional-free"}:
        raise FreeApiPolicyError("paid_or_required_credentials_forbidden")
    if not 1 <= int(policy["daily_request_limit"]):
        raise FreeApiPolicyError("invalid_daily_request_limit")
    if not 1 <= int(policy["per_call_result_limit"]) <= 50:
        raise FreeApiPolicyError("invalid_per_call_result_limit")


def reserve(policy: dict, usage_file: str | None = None) -> dict:
    """Validate policy and reserve one request from today's local allowance."""
    validate(policy)
    path = Path(
        usage_file
        or os.environ.get("DORE_API_USAGE_FILE", "/private/tmp/dore-api-usage.json")
    )
    today = datetime.date.today().isoformat()
    ledger = {"date": today, "providers": {}}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if loaded.get("date") == today:
                ledger = loaded
        except (OSError, ValueError):
            raise FreeApiPolicyError("usage_ledger_unreadable")
    providers = ledger.setdefault("providers", {})
    used = int(providers.get(policy["provider"], 0))
    limit = int(policy["daily_request_limit"])
    if used >= limit:
        raise FreeApiPolicyError("free_daily_limit_exhausted")
    providers[policy["provider"]] = used + 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"provider": policy["provider"], "used": used + 1, "limit": limit}
