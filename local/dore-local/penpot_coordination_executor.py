#!/usr/bin/env python3
"""Execute coordination Penpot inspections through live MCP tools, not acknowledgements."""
from __future__ import annotations
import time
from penpot_agent import list_tools,call_tool,_text_from_result,_semantic_ok

DENY=('create','delete','remove','update','set','write','move','resize','rename','change','apply','insert','add','clone','duplicate','replace','edit','modify')
ALLOW=('get','list','read','inspect','find','query','search','current','page','file','selection','export','render','screenshot','view')

def readonly_tools(tools):
    out=[]
    for t in tools:
        hay=((t.get('name') or '')+' '+(t.get('description') or '')).lower()
        if any(x in hay for x in DENY): continue
        if any(x in hay for x in ALLOW): out.append(t)
    return out

def execute_readonly(task:str):
    """Run a deterministic live read-only Penpot inspection.

    The old implementation depended on private Ollama helper functions removed
    from penpot_agent.py. Coordination only needs live evidence here, so use
    official MCP discovery/read tools directly instead of an LLM tool loop.
    """
    started=time.time(); trace=[]
    try: all_tools=list_tools()
    except Exception as e:
        return {'ok':False,'executed':False,'error':'penpot_list_tools:'+type(e).__name__+':'+str(e),'duration_seconds':round(time.time()-started,3),'trace':[]}
    names=[t.get('name') for t in all_tools]
    if 'execute_code' not in names:
        return {'ok':False,'executed':False,'error':'penpot_execute_code_missing','available_tool_names':names,'duration_seconds':round(time.time()-started,3),'trace':[]}
    # Tool discovery and high_level_overview are served without a Penpot document
    # connection.  A read-only execute_code call is the actual end-to-end gate:
    # client -> HTTP MCP -> WebSocket bridge -> live Penpot plugin -> document.
    args={'code':'return JSON.stringify({fileId:penpot.currentFile?.id||null,fileName:penpot.currentFile?.name||null,pageId:penpot.currentPage?.id||null,pageName:penpot.currentPage?.name||null,rootChildren:(penpot.currentPage?.root?.children||[]).length});'}
    try:
        result=call_tool('execute_code',args); evidence=_text_from_result(result); ok=_semantic_ok(result)
        trace.append({'tool':'execute_code','ok':ok,'arguments':{'code':'<read-only-document-probe>'},'result_excerpt':evidence[:6000]})
    except Exception as e:
        return {'ok':False,'executed':False,'error':'penpot_document_probe:'+type(e).__name__+':'+str(e),'task':task,'duration_seconds':round(time.time()-started,3),'trace':trace}
    if not ok:
        return {'ok':False,'executed':True,'error':'penpot_plugin_disconnected','answer':'Penpot MCP is reachable, but no live Penpot document plugin is connected.','task':task,'trace':trace,'duration_seconds':round(time.time()-started,3)}
    return {'ok':True,'executed':True,'answer':'Live Penpot document evidence collected.','task':task,'trace':trace,'duration_seconds':round(time.time()-started,3)}
