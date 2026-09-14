#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[2]
workflow=(root/'.github/workflows/dore-a2a-github-relay.yml').read_text(encoding='utf-8')
entry=(root/'local/dore-local/github_a2a_entry.py').read_text(encoding='utf-8')
checks={
 'issues':'issues:' in workflow,
 'workflow_dispatch':'workflow_dispatch:' in workflow,
 'repository_dispatch':'repository_dispatch:' in workflow,
 'single_execution_step':workflow.count('python3 local/dore-local/github_a2a_entry.py')==1,
 'no_in_rpc_refresh':'install-unix-a2a-macos.sh' not in workflow and 'Refresh DORÉ Unix control plane' not in workflow,
 'resident_core':'Execute through resident Universal A2A Core' in workflow,
 'public_dore_call':"call('dore.call'" in entry,
 'github_transport':"'transport':'github'" in entry,
 'issue_result_channel':'DORE_REPLY_ISSUE_NUMBER' in workflow and 'post_issue_comment' in entry,
}
assert all(checks.values()),checks
print('A2A_THREE_ENTRANCES_ONE_CORE_PASS',checks)
