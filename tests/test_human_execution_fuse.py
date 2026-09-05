from dore_core.governance.human_execution import (
    HumanExecutionDecision,
    assess_manual_terminal_request,
    terminal_loop_fused,
)


def test_first_manual_terminal_action_is_bootstrap_only():
    result = assess_manual_terminal_request(prior_manual_terminal_actions=0)
    assert result.decision is HumanExecutionDecision.ALLOW_BOOTSTRAP
    assert "bootstrap" in result.required_action
    assert terminal_loop_fused(prior_manual_terminal_actions=0) is False


def test_second_manual_terminal_action_triggers_fuse():
    result = assess_manual_terminal_request(prior_manual_terminal_actions=1)
    assert result.decision is HumanExecutionDecision.FUSE
    assert "stop delegating commands" in result.required_action
    assert terminal_loop_fused(prior_manual_terminal_actions=1) is True


def test_fuse_stays_active_after_multiple_manual_actions():
    assert terminal_loop_fused(prior_manual_terminal_actions=5) is True
