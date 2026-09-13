#!/usr/bin/env python3
"""Universal durable execution wrapper for canonical Doré capabilities.

Every normal canonical capability call passes through this layer after ingress
normalization and identity/binding resolution. Transport success is never treated as
execution completion. Long-running work renews its lease; expired work is reclaimed
only when recovery is safe.
"""
from __future__ import annotations

import hashlib,json,threading
from typing import Any,Callable


def _digest(value:Any)->str:return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
def _task_id(envelope):return "cap-"+_digest({"request_id":envelope.get("request_id"),"conversation_id":envelope.get("conversation_id"),"session_id":envelope.get("session_id"),"consumer_id":envelope.get("consumer_id")})[:32]
def _message(envelope,task_id):return {"message_id":task_id,"kind":"capability.call","related_goal":envelope.get("conversation_id"),"request_id":envelope.get("request_id"),"conversation_id":envelope.get("conversation_id"),"session_id":envelope.get("session_id"),"consumer_id":envelope.get("consumer_id"),"capability_id":envelope.get("capability_id"),"payload":envelope.get("payload") or {}}
def _retry_safe(binding,descriptor):
 if "retry_safe" in binding:return bool(binding.get("retry_safe"))
 if descriptor.get("requires_verified_execution") is True:return False
 return binding.get("kind")!="production-action"

def _heartbeat_loop(stop,plane,task_id,owner,lease_seconds,interval):
 while not stop.wait(interval):
  renewed=plane.heartbeat(task_id,consumer=owner,lease_seconds=lease_seconds)
  if not renewed.get("ok"):return

def _verification(envelope,binding,result_sha):return {"ok":True,"strategy":"deterministic-handler-result-v1","capability_id":envelope.get("capability_id"),"result_sha256":result_sha,"binding_kind":binding.get("kind")}

def execute(envelope:dict[str,Any],descriptor:dict[str,Any],binding:dict[str,Any],provider_call:Callable[[],dict[str,Any]],*,plane:Any)->dict[str,Any]:
 task_id=_task_id(envelope);message=_message(envelope,task_id);task=plane.register(message)
 if task.get("status")=="PASS":
  s=plane.status(task_id);return {"ok":True,"task_id":task_id,"execution_status":"PASS","completion_evidence":bool(s.get("completion_evidence")),"replayed":True,"result":task.get("result"),"artifact":task.get("artifact"),"verification":task.get("verification")}

 owner=f"universal:{envelope.get('consumer_id') or 'dore'}";lease_seconds=max(30,int(descriptor.get("lease_seconds") or binding.get("lease_seconds") or getattr(plane,"DEFAULT_LEASE_SECONDS",300)))
 rec=plane.recoverability(task_id) if hasattr(plane,"recoverability") else {"state":"READY","task":task}
 resume_from=rec.get("resume_from")
 # A crashed worker may have crossed an external side-effect boundary. Never replay
 # such RUNNING work generically; preserve UNKNOWN until its explicit recovery contract exists.
 if rec.get("state")=="RECLAIMABLE" and resume_from in {"RUNNING","CLAIMED"} and not _retry_safe(binding,descriptor):
  return {"ok":False,"task_id":task_id,"execution_status":"UNKNOWN","completion_evidence":False,"recovery_state":"RECLAIMABLE","error":{"code":"unsafe_replay_blocked","message":"expired side-effecting execution requires capability-specific recovery"}}

 claimed=plane.claim(task_id,consumer=owner,lease_seconds=lease_seconds)
 if not claimed.get("ok"):
  current=claimed.get("task") or task;return {"ok":False,"task_id":task_id,"execution_status":current.get("status"),"completion_evidence":False,"recovery_state":plane.status(task_id).get("recovery_state") if hasattr(plane,"status") else None,"error":{"code":claimed.get("code") or "claim_failed"}}
 reclaimed=bool(claimed.get("reclaimed"));resume_from=claimed.get("resume_from") if reclaimed else None
 current=claimed.get("task") or {}

 # Crash after durable artifact/verification does not rerun provider work.
 if reclaimed and resume_from in {"ARTIFACT_PRODUCED","VERIFIED"}:
  artifact=current.get("artifact")
  if resume_from=="ARTIFACT_PRODUCED" and artifact:
   verified=plane.verify(task_id,_verification(envelope,binding,artifact.get("result_sha256") or artifact.get("sha256")),consumer=owner)
   if not verified.get("ok"):return {"ok":False,"task_id":task_id,"execution_status":"FAIL","completion_evidence":False,"reclaimed":True,"error":{"code":"recovered_verification_failed"}}
  completed=plane.complete(task_id,result=current.get("result") or (artifact or {}).get("result"),consumer=owner);s=plane.status(task_id)
  return {"ok":bool(completed.get("ok") and s.get("completion_evidence")),"task_id":task_id,"execution_status":(s.get("task") or {}).get("status"),"completion_evidence":bool(s.get("completion_evidence")),"reclaimed":True,"provider_reexecuted":False,"result":(s.get("task") or {}).get("result"),"artifact":(s.get("task") or {}).get("artifact"),"verification":(s.get("task") or {}).get("verification")}

 running=plane.transition(task_id,"RUNNING",consumer=owner)
 if not running.get("ok"):return {"ok":False,"task_id":task_id,"execution_status":"UNKNOWN","completion_evidence":False,"error":{"code":running.get("code") or "running_transition_failed"}}
 if descriptor.get("requires_verified_execution") is True and not descriptor.get("verification_contract"):
  failed=plane.transition(task_id,"FAIL",consumer=owner,result={"ok":False,"error":{"code":"verification_contract_required"}})
  return {"ok":False,"task_id":task_id,"execution_status":"FAIL","completion_evidence":False,"error":{"code":"verification_contract_required","message":"side-effect capability requires an explicit verification contract before execution"},"task":failed.get("task")}

 interval=float(binding.get("heartbeat_interval_seconds") or descriptor.get("heartbeat_interval_seconds") or max(1.0,min(30.0,lease_seconds/3.0)));stop=threading.Event();thread=threading.Thread(target=_heartbeat_loop,args=(stop,plane,task_id,owner,lease_seconds,interval),daemon=True,name="dore-a2a-heartbeat");thread.start()
 try:
  result=provider_call()
 except Exception as exc:
  stop.set();thread.join(timeout=max(0.1,interval*2));plane.transition(task_id,"FAIL",consumer=owner,result={"ok":False,"error":{"code":"provider_exception","message":str(exc)}})
  return {"ok":False,"task_id":task_id,"execution_status":"FAIL","completion_evidence":False,"error":{"code":"provider_exception","message":str(exc)}}
 finally:
  stop.set()
 try:thread.join(timeout=max(0.1,interval*2))
 except RuntimeError:pass

 semantic_ok=bool(isinstance(result,dict) and result.get("ok") is True and str(result.get("status") or "completed").lower() not in {"failed","error"})
 if not semantic_ok:
  plane.transition(task_id,"FAIL",consumer=owner,result=result if isinstance(result,dict) else {"value":result});return {"ok":False,"task_id":task_id,"execution_status":"FAIL","completion_evidence":False,"result":result}
 artifact={"schema":"dore.a2a-capability-result-artifact.v1","capability_id":envelope.get("capability_id"),"request_id":envelope.get("request_id"),"result_sha256":_digest(result),"result":result}
 recorded=plane.record_artifact(task_id,artifact,consumer=owner)
 if not recorded.get("ok"):return {"ok":False,"task_id":task_id,"execution_status":"UNKNOWN","completion_evidence":False,"recovery_state":plane.status(task_id).get("recovery_state") if hasattr(plane,"status") else None,"error":{"code":recorded.get("code") or "artifact_record_failed"},"result":result}
 verified=plane.verify(task_id,_verification(envelope,binding,artifact["result_sha256"]),consumer=owner)
 if not verified.get("ok"):return {"ok":False,"task_id":task_id,"execution_status":"FAIL","completion_evidence":False,"result":result,"verification":verified.get("task",{}).get("verification")}
 completed=plane.complete(task_id,result=result,consumer=owner);s=plane.status(task_id)
 return {"ok":bool(completed.get("ok") and s.get("completion_evidence")),"task_id":task_id,"execution_status":(s.get("task") or {}).get("status"),"completion_evidence":bool(s.get("completion_evidence")),"replayed":False,"reclaimed":reclaimed,"result":result,"artifact":(s.get("task") or {}).get("artifact"),"verification":(s.get("task") or {}).get("verification")}
