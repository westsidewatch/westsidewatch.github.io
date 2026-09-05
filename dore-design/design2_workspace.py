"""Workspace bridge for DORÉ DESIGN 2.0 commands.

Keeps the existing atomic workspace persistence/history while making the 2.0
validated command layer the only mutation path used by the new editor shell.
"""
import design2_commands

OPS={'node.patch','node.patch_many','node.nudge'}


def is_command(payload):
    return isinstance(payload,dict) and payload.get('op') in OPS


def execute(base,payload,expected_revision=None):
    current=base.workspace()
    revision=int(current.get('revision',0))
    if expected_revision is not None and int(expected_revision)!=revision:
        raise ValueError(f'stale_revision:{expected_revision}:{revision}')
    changed=design2_commands.apply(current,payload)
    # base.save owns validation, history snapshot, atomic disk replacement and
    # monotonic revision assignment. The command core itself stays pure.
    return base.save(changed)


def install(base):
    """Install compatibility bridge without changing legacy command behavior."""
    original_mutate=base.mutate
    def mutate(workspace,payload):
        if not is_command(payload):
            return original_mutate(workspace,payload)
        # Legacy callers pass a workspace object; protect against writing over a
        # newer resident revision by binding the command to that revision.
        return execute(base,payload,workspace.get('revision'))
    base.mutate=mutate
    return original_mutate
