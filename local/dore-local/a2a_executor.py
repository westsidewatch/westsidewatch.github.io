#!/usr/bin/env python3
"""Universal durable execution wrapper for canonical Doré capabilities.

Every normal canonical capability call passes through this layer after ingress
normalization and identity/binding resolution. Transport success is never treated as
execution completion. Long-running work renews its lease; expired work is reclaimed
only when recovery is safe. All execution failures are classified by the canonical
A2A failure vocabulary before a consumer decides whether work may retry, remains
unknown, is quarantined, requires research, or is terminal.
"""
from __future__ import annotations

import hashlib,json,threading
from typing import Any,Callable
import a2a_failure_policy as failure_policy


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

def _failure(task_id,failure,descriptor,binding,*,attempt=1,max_attempts=3,context=None):
 return failure_policy.decision(task_id,failure,descriptor=descriptor,binding=binding,attempt=attempt,max_attempts=max_attempts,context=context or {})

def _failure_response(task_id,decision,*,result=None,error=None):
 state=decision.get("state") or "TERMINAL_FAIL"
 execution_status={"RETRYABLE":"UNKNOWN","UNKNOWN":"UNKNOWN","QUARANTINED":"REJECTED","RESEARCH_REQUIRED":"DEFERRED","TERMINAL_FAIL":"FAIL"}.get(state,"FAIL")
 payload={"ok":False,"task_id":task_id,"execution_status":execution_status,"completion_evidence":False,"failure_state":state,"failure":decision}
 if result is not None:payload["result"]=result
 if error is not None:payload["error"]=error
 return payload

def execute(envelope:dict[str,Any],descriptor:dict[str,Any],binding:dict[str,Any],provider_call:Callable[[],dict[str,Any]],*,plane:Any)->dict[str,Any]:
 task_id=_task_id(envelope);message=_message(envelope,task_id);task=plane.register(message)
 if task.get("status")=="PASS":
  s=plane.status(task_id);return {"ok":True,"task_id":task_id,"execution_status":"PASS","completion_evidence":bool(s.get("completion_evidence")),"replayed":True,"result":task.get("result"),"artifact":task.get("artifact"),"verification":task.get("verification")}

 owner=f"universal:{envelope.get('consumer_id') or 'dore'}";lease_seconds=max(30,int(descriptor.get("lease_seconds") or binding.get("lease_seconds") or getattr(plane,"DEFAULT_LEASE_SECONDS",300)))
 rec=plane.recoverability(task_id) if hasattr(plane,"recoverability") else {"state":"READY","task":task};resume_from=rec.get("resume_from")
 if rec.get("state")=="RECLAIMABLE" and resume_from in {"RUNNING","CLAIMED"} and not _retry_safe(binding,descriptor):
  decision=_failure(task_id,{"code":"worker_lost"},descriptor,binding,context={"resume_from":resume_from,"reclaimable":True,"unsafe_replay":True})
  return _failure_response(task_id,decision,error={"code":"unsafe_replay_blocked","message":"expired side-effecting execution requires capability-specific recovery"})

 claimed=plane.claim(task_id,consumer=owner,lease_seconds=lease_seconds)
 if not claimed.get("ok"):
  current=claimed.get("task") or task;decision=_failure(task_id,{"code":claimed.get("code") or "claim_failed"},descriptor,binding,context={"stage":"claim"})
  response=_failure_response(task_id,decision,error={"code":claimed.get("code") or "claim_failed"});response["execution_status"]=current.get("status") or response["execution_status"];response["recovery_state"]=plane.status(task_id).get("recovery_state") if hasattr(plane,"status") else None;return response
 claimed_recovery=bool(claimed.get("reclaimed"));resume_from=claimed.get("resume_from") if claimed_recovery else None;current=claimed.get("task") or {}

 if claimed_recovery and resume_from in {"ARTIFACT_PRODUCED","VERIFIED"}:
  artifact=current.get("artifact")
  if resume_from=="ARTIFACT_PRODUCED" and artifact:
   verified=plane.verify(task_id,_verification(envelope,binding,artifact.get("result_sha256") or artifact.get("sha256")),consumer=owner)
   if not verified.get("ok"):
    decision=_failure(task_id,{"code":"verification_failed"},descriptor,binding,context={"stage":"recovered_verify"});return _failure_response(task_id,decision,error={"code":"recovered_verification_failed"})
  completed=plane.complete(task_id,result=current.get("result") or (artifact or {}).get("result"),consumer=owner);s=plane.status(task_id)
  return {"ok":bool(completed.get("ok") and s.get("completion_evidence")),"task_id":task_id,"execution_status":(s.get("task") or {}).get("status"),"completion_evidence":bool(s.get("completion_evidence")),"reclaimed":True,"provider_reexecuted":False,"result":(s.get("task") or {}).get("result"),"artifact":(s.get("task") or {}).get("artifact"),"verification":(s.get("task") or {}).get("verification")}

 running=plane.transition(task_id,"RUNNING",consumer=owner)
 if not running.get("ok"):
  decision=_failure(task_id,{"code":running.get("code") or "worker_lost"},descriptor,binding,context={"stage":"running_transition"});return _failure_response(task_id,decision,error={"code":running.get("code") or "running_transition_failed"})
 if descriptor.get("requires_verified_execution") is True and not descriptor.get("verification_contract"):
  failed=plane.transition(task_id,"FAIL",consumer=owner,result={"ok":False,"error":{"code":"verification_contract_required"}});decision=_failure(task_id,{"code":"policy_violation"},descriptor,binding,context={"stage":"verification_contract"})
  response=_failure_response(task_id,decision,error={"code":"verification_contract_required","message":"side-effect capability requires an explicit verification contract before execution"});response["task"]=failed.get("task");return response

 interval=float(binding.get("heartbeat_interval_seconds") or descriptor.get("heartbeat_interval_seconds") or max(1.0,min(30.0,lease_seconds/3.0)));stop=threading.Event();thread=threading.Thread(target=_heartbeat_loop,args=(stop,plane,task_id,owner,lease_seconds,interval),daemon=True,name="dore-a2a-heartbeat");thread.start()
 try:result=provider_call()
 except Exception as exc:
  stop.set();thread.join(timeout=max(0.1,interval*2));decision=_failure(task_id,exc,descriptor,binding,context={"stage":"provider"})
  if decision.get("state") in {"TERMINAL_FAIL","QUARANTINED"}:plane.transition(task_id,"FAIL",consumer=owner,result={"ok":False,"error":{"code":"provider_exception","message":str(exc)},"failure_state":decision.get("state")})
  return _failure_response(task_id,decision,error={"code":"provider_exception","message":str(exc)})
 finally:stop.set()
 try:thread.join(timeout=max(0.1,interval*2))
 except RuntimeError:pass

 semantic_ok=bool(isinstance(result,dict) and result.get("ok") is True and str(result.get("status") or "completed").lower() not in {"failed","error"})
 if not semantic_ok:
  failure=result if isinstance(result,dict) else {"code":"provider_result_invalid","value":result};decision=_failure(task_id,failure,descriptor,binding,context={"stage":"semantic_result"})
  if decision.get("state") in {"TERMINAL_FAIL","QUARANTINED"}:plane.transition(task_id,"FAIL",consumer=owner,result=failure)
  return _failure_response(task_id,decision,result=result)
 artifact={"schema":"dore.a2a-capability-result-artifact.v1","capability_id":envelope.get("capability_id"),"request_id":envelope.get("request_id"),"result_sha256":_digest(result),"result":result}
 recorded=plane.record_artifact(task_id,artifact,consumer=owner)
 if not recorded.get("ok"):
  decision=_failure(task_id,{"code":recorded.get("code") or "worker_lost"},descriptor,binding,context={"stage":"artifact_record"});response=_failure_response(task_id,decision,result=result,error={"code":recorded.get("code") or "artifact_record_failed"});response["recovery_state"]=plane.status(task_id).get("recovery_state") if hasattr(plane,"status") else None;return response
 verified=plane.verify(task_id,_verification(envelope,binding,artifact["result_sha256"]),consumer=owner)
 if not verified.get("ok"):
  decision=_failure(task_id,{"code":"verification_failed"},descriptor,binding,context={"stage":"verify"});return _failure_response(task_id,decision,result=result,error={"code":"execution_verification_failed"})
 completed=plane.complete(task_id,result=result,consumer=owner);s=plane.status(task_id)
 return {"ok":bool(completed.get("ok") and s.get("completion_evidence")),"task_id":task_id,"execution_status":(s.get("task") or {}).get("status"),"completion_evidence":bool(s.get("completion_evidence")),"replayed":False,"reclaimed":claimed_recovery,"result":result,"artifact":(s.get("task") or {}).get("artifact"),"verification":(s.get("task") or {}).get("verification")}
