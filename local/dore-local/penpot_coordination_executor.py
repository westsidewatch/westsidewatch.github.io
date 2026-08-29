#!/usr/bin/env python3
"""Execute coordination Penpot inspections through live MCP tools, not acknowledgements."""
from __future__ import annotations
import json,time
from penpot_agent import list_tools,call_tool,_ollama,_as_ollama_tools,_text_from_result,_clean_answer,MAX_STEPS,VOICE_RULE

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
    started=time.time()
    try: all_tools=list_tools()
    except Exception as e:
        return {'ok':False,'executed':False,'error':'penpot_list_tools:'+type(e).__name__+':'+str(e),'duration_seconds':round(time.time()-started,3),'trace':[]}
    tools=readonly_tools(all_tools); names=[t.get('name') for t in tools]
    if not tools:
        return {'ok':False,'executed':False,'error':'no_readonly_penpot_tools','available_tool_names':[t.get('name') for t in all_tools],'duration_seconds':round(time.time()-started,3),'trace':[]}
    system=f'''You are Doré executing a REAL READ-ONLY Penpot inspection through live MCP tools.\n{VOICE_RULE}\nYou MUST call Penpot tools before answering. Never return a plan, acknowledgement, intention, or promise as the work result. No mutation tools are exposed. Report only evidence actually returned in this run, including exact names, IDs and metadata when available. If timestamps/history are unavailable, state that exact limitation.\nRead-only tools: {', '.join(names)}'''
    messages=[{'role':'system','content':system},{'role':'user','content':task}]; trace=[]
    for step in range(MAX_STEPS):
        try: msg=_ollama(messages,_as_ollama_tools(tools))
        except Exception as e:
            return {'ok':False,'executed':bool(trace),'error':'penpot_agent_model:'+type(e).__name__+':'+str(e),'trace':trace,'duration_seconds':round(time.time()-started,3)}
        calls=msg.get('tool_calls') or []; assistant={'role':'assistant','content':msg.get('content') or ''}
        if calls: assistant['tool_calls']=calls
        messages.append(assistant)
        if not calls:
            if not trace:
                messages.append({'role':'user','content':'No Penpot tool has been executed. Execute a read-only tool now. Do not answer with a plan.'}); continue
            return {'ok':True,'executed':True,'answer':_clean_answer(msg.get('content') or ''),'trace':trace,'steps':step+1,'duration_seconds':round(time.time()-started,3)}
        for call in calls:
            fn=call.get('function') or {}; name=fn.get('name'); args=fn.get('arguments') or {}
            result=call_tool(name,args) if name in names else {'ok':False,'error':'readonly_tool_blocked:'+str(name)}
            text=_text_from_result(result)
            trace.append({'tool':name,'ok':bool(result.get('ok')),'arguments':args,'result_excerpt':text[:6000]})
            messages.append({'role':'tool','tool_name':name,'content':text})
    return {'ok':False,'executed':bool(trace),'error':'penpot_readonly_step_limit','trace':trace,'steps':MAX_STEPS,'duration_seconds':round(time.time()-started,3)}
