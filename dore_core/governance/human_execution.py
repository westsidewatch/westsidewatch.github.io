"""Human execution fuse for DORÉ.

A human may perform one unavoidable bootstrap action. A second requested manual
Terminal/shell action in the same task is treated as an automation failure and
must be replaced by an automated path or a single packaged bootstrap.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class HumanExecutionDecision(str, Enum):
    ALLOW_BOOTSTRAP = "allow_bootstrap"
    FUSE = "fuse"


@dataclass(frozen=True)
class HumanExecutionAssessment:
    decision: HumanExecutionDecision
    reason: str
    required_action: str


def assess_manual_terminal_request(*, prior_manual_terminal_actions: int) -> HumanExecutionAssessment:
    """Decide whether another manual Terminal action may be delegated to a human.

    The first action is permitted only as bootstrap. Any subsequent action
    triggers the fuse and requires DORÉ to build/use automation instead.
    """
    if prior_manual_terminal_actions <= 0:
        return HumanExecutionAssessment(
            HumanExecutionDecision.ALLOW_BOOTSTRAP,
            "one unavoidable bootstrap action may be delegated to the human",
            "package the action as one atomic bootstrap and continue automatically afterwards",
        )
    return HumanExecutionAssessment(
        HumanExecutionDecision.FUSE,
        "a second manual Terminal action would turn the human into the execution transport",
        "stop delegating commands; use an existing local executor, self-repair, installer/updater, browser/native bridge, or build a one-shot bootstrap",
    )


def terminal_loop_fused(*, prior_manual_terminal_actions: int) -> bool:
    return assess_manual_terminal_request(
        prior_manual_terminal_actions=prior_manual_terminal_actions
    ).decision is HumanExecutionDecision.FUSE
