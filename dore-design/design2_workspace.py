"""Workspace bridge for DORÉ DESIGN 2.0 commands."""
import design2_commands
OPS={'node.patch','node.patch_many','node.nudge','node.align','node.distribute'}
def is_command(payload):return isinstance(payload,dict) and payload.get('op') in OPS
def execute(base,payload,expected_revision=None):
    current=base.workspace();revision=int(current.get('revision',0))
    if expected_revision is not None and int(expected_revision)!=revision:raise ValueError(f'stale_revision:{expected_revision}:{revision}')
    return base.save(design2_commands.apply(current,payload))
def install(base):
    original_mutate=base.mutate
    def mutate(workspace,payload):
        if not is_command(payload):return original_mutate(workspace,payload)
        return execute(base,payload,workspace.get('revision'))
    base.mutate=mutate;return original_mutate
