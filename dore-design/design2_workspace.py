"""Workspace bridge for DORÉ DESIGN 2.0 commands and revision navigation."""
import json
from pathlib import Path
import design2_commands
OPS={'node.patch','node.patch_many','node.text','node.nudge','node.align','node.distribute'}
def is_command(payload):return isinstance(payload,dict) and payload.get('op') in OPS
def execute(base,payload,expected_revision=None):
    current=base.workspace();revision=int(current.get('revision',0))
    if expected_revision is not None and int(expected_revision)!=revision:raise ValueError(f'stale_revision:{expected_revision}:{revision}')
    return base.save(design2_commands.apply(current,payload))
def _history_dir(base):return Path(base.HISTORY)
def available_revisions(base):
    out=[]
    for p in _history_dir(base).glob('*.json'):
        try:out.append(int(p.stem))
        except ValueError:pass
    out.append(int(base.workspace().get('revision',0)))
    return sorted(set(out))
def navigate(base,direction,expected_revision):
    current=base.workspace();rev=int(current.get('revision',0))
    if int(expected_revision)!=rev:raise ValueError(f'stale_revision:{expected_revision}:{rev}')
    revisions=available_revisions(base)
    if direction=='undo':candidates=[r for r in revisions if r<rev];target=max(candidates) if candidates else None
    elif direction=='redo':candidates=[r for r in revisions if r>rev];target=min(candidates) if candidates else None
    else:raise ValueError('invalid_history_direction')
    if target is None:raise ValueError('history_boundary')
    source=_history_dir(base)/f'{target}.json'
    if not source.exists():raise ValueError('history_revision_missing')
    snapshot=json.loads(source.read_text())
    # save() creates a new monotonic revision and snapshots the current state;
    # history is therefore non-destructive even when restoring an old state.
    snapshot['revision']=rev
    return base.save(snapshot)
def install(base):
    original_mutate=base.mutate
    def mutate(workspace,payload):
        if not is_command(payload):return original_mutate(workspace,payload)
        return execute(base,payload,workspace.get('revision'))
    base.mutate=mutate;return original_mutate
