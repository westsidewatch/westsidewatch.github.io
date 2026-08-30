#!/usr/bin/env python3
"""Execute coordination Penpot inspections through live MCP tools, not acknowledgements."""
from __future__ import annotations
import time
from penpot_agent import list_tools,call_tool,_text_from_result

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
    tools=readonly_tools(all_tools); names=[t.get('name') for t in tools]
    preferred=[]
    if 'high_level_overview' in names: preferred.append(('high_level_overview',{}))
    if 'execute_code' in names:
        # execute_code is intentionally excluded by readonly_tools because it can mutate.
        pass
    if not preferred:
        return {'ok':False,'executed':False,'error':'no_safe_readonly_penpot_tools','available_tool_names':[t.get('name') for t in all_tools],'duration_seconds':round(time.time()-started,3),'trace':[]}
    for name,args in preferred:
        try:
            result=call_tool(name,args); text=_text_from_result(result)
            trace.append({'tool':name,'ok':bool(result.get('ok')),'arguments':args,'result_excerpt':text[:6000]})
        except Exception as e:
            trace.append({'tool':name,'ok':False,'arguments':args,'exception':type(e).__name__+': '+str(e)})
    ok=any(x.get('ok') for x in trace)
    return {'ok':ok,'executed':bool(trace),'answer':'Live Penpot read-only evidence collected.' if ok else 'Penpot read-only inspection failed.','task':task,'trace':trace,'duration_seconds':round(time.time()-started,3)}
