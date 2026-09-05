"""Workspace bridge for DORÉ DESIGN 2.0 commands and revision navigation."""
import json,re
from pathlib import Path
import design2_commands
OPS={'node.patch','node.patch_many','node.text','node.nudge','node.align','node.distribute'}
def is_command(payload):return isinstance(payload,dict) and payload.get('op') in OPS
def execute(base,payload,expected_revision=None):
 current=base.workspace();revision=int(current.get('revision',0))
 if expected_revision is not None and int(expected_revision)!=revision:raise ValueError(f'stale_revision:{expected_revision}:{revision}')
 return base.save(design2_commands.apply(current,payload))
def _history_dir(base):return Path(getattr(base,'HIST',getattr(base,'HISTORY','')))
def _snapshot_rows(base):
 rows=[]
 for p in _history_dir(base).glob('*.json'):
  m=re.search(r'\.r(\d+)\.json$',p.name)
  try:
   data=json.loads(p.read_text(encoding='utf-8'));rev=int(data.get('revision',m.group(1) if m else -1));rows.append((rev,p,data))
  except Exception:continue
 return sorted(rows,key=lambda x:x[0])
def available_revisions(base):
 out=[r for r,_,_ in _snapshot_rows(base)];out.append(int(base.workspace().get('revision',0)));return sorted(set(out))
def navigate(base,direction,expected_revision):
 current=base.workspace();rev=int(current.get('revision',0))
 if int(expected_revision)!=rev:raise ValueError(f'stale_revision:{expected_revision}:{rev}')
 state=getattr(base,'_design2_history_state',None)
 if not state or state.get('head')!=rev:
  state={'head':rev,'undo':[(r,d) for r,_,d in _snapshot_rows(base) if r<rev],'redo':[]}
 if direction=='undo':
  if not state['undo']:raise ValueError('history_boundary')
  _,target=state['undo'].pop();state['redo'].append(json.loads(json.dumps(current)))
 elif direction=='redo':
  if not state['redo']:raise ValueError('history_boundary')
  target=state['redo'].pop();state['undo'].append((rev,json.loads(json.dumps(current))))
 else:raise ValueError('invalid_history_direction')
 target['revision']=rev
 restored=base.save(target);state['head']=int(restored['revision']);base._design2_history_state=state;return restored
def install(base):
 original_mutate=base.mutate
 def mutate(workspace,payload):
  if not is_command(payload):return original_mutate(workspace,payload)
  result=execute(base,payload,workspace.get('revision'))
  state=getattr(base,'_design2_history_state',None)
  if state:state['redo']=[];state['head']=int(result.get('revision',0))
  return result
 base.mutate=mutate;return original_mutate
