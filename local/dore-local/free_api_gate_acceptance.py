#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory

from free_api_gate import FreeApiPolicyError, reserve, validate

POLICY = {
    "provider": "fixture",
    "billing": "free-only",
    "credentials": "none",
    "paid_fallback": False,
    "daily_request_limit": 2,
    "per_call_result_limit": 10,
}

validate(POLICY)
for bad in (
    {**POLICY, "billing": "metered"},
    {**POLICY, "paid_fallback": True},
    {**POLICY, "credentials": "required-paid"},
):
    try:
        validate(bad)
        raise AssertionError("unsafe policy was accepted")
    except FreeApiPolicyError:
        pass

with TemporaryDirectory() as directory:
    ledger = str(Path(directory) / "usage.json")
    assert reserve(POLICY, ledger)["used"] == 1
    assert reserve(POLICY, ledger)["used"] == 2
    try:
        reserve(POLICY, ledger)
        raise AssertionError("daily limit was not enforced")
    except FreeApiPolicyError as error:
        assert str(error) == "free_daily_limit_exhausted"

print("DORE_FREE_API_GATE_ACCEPTANCE=PASS")
