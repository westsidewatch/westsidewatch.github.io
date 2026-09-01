#!/usr/bin/env python3
"""Regression checks: tool discovery alone must never pass Penpot readiness."""
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import penpot_agent as agent
import penpot_coordination_executor as coordination

agent._node=lambda op,payload=None:{'ok':True,'url':'http://127.0.0.1:4401/mcp','server':{'name':'penpot-mcp-server'},'tool_count':1,'tools':['execute_code']}
agent.call_tool=lambda name,args:{'ok':True,'result':{'content':[{'type':'text','text':'Tool execution failed: Error: No Penpot plugin instances are currently connected.'}]}}
disconnected=agent.status()
assert disconnected['transport_ok'] is True
assert disconnected['plugin_connected'] is False
assert disconnected['ok'] is False
assert disconnected['error']=='penpot_plugin_disconnected'

coordination.list_tools=lambda:[{'name':'execute_code','description':'Execute Penpot Plugin API code'}]
coordination.call_tool=agent.call_tool
work=coordination.execute_readonly('probe')
assert work['executed'] is True
assert work['ok'] is False
assert work['error']=='penpot_plugin_disconnected'

agent.call_tool=lambda name,args:{'ok':True,'result':{'content':[{'type':'text','text':'{"result":"{\\"fileId\\":\\"f1\\",\\"pageId\\":\\"p1\\"}","log":""}'}]}}
connected=agent.status()
assert connected['ok'] is True
assert connected['plugin_connected'] is True
assert connected['document']['fileId']=='f1'
print('DORE_PENPOT_CONNECTION_GATE_PASS')
