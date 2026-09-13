#!/usr/bin/env python3
"""Immutable runtime generation identity for the Doré A2A control plane.

Repository state may move while a long-lived launchd process remains resident.
This module captures the generation that actually started the process and exposes
current checkout drift separately. A restart decision must never be inferred from
repository HEAD alone.
"""
from __future__ import annotations
import hashlib,json,os,subprocess
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve()
REGISTRY=ROOT/'dore-core'/'runtime'/'capability-registry.v1.json'
SCHEMA='dore.a2a-runtime-generation.v1'
STARTED_AT=datetime.now(timezone.utc).isoformat()

def _sha_bytes(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def file_sha(path:Path)->str|None:
 try:return _sha_bytes(path.read_bytes())
 except Exception:return None

def _git(*args)->str|None:
 try:
  p=subprocess.run(['git','-C',str(ROOT),*args],capture_output=True,text=True,timeout=3,check=False)
  value=p.stdout.strip()
  return value if p.returncode==0 and value else None
 except Exception:return None

def _active_commit()->str|None:
 return os.environ.get('DORE_CONTROL_PLANE_COMMIT') or os.environ.get('GITHUB_SHA') or _git('rev-parse','HEAD')

def _active_ref()->str|None:
 return os.environ.get('DORE_CONTROL_PLANE_REF') or os.environ.get('GITHUB_REF_NAME') or _git('rev-parse','--abbrev-ref','HEAD')

ACTIVE_COMMIT=_active_commit()
ACTIVE_REF=_active_ref()
ACTIVE_REGISTRY_SHA256=file_sha(REGISTRY)
GENERATION_ID=_sha_bytes(json.dumps({'commit':ACTIVE_COMMIT,'ref':ACTIVE_REF,'registry_sha256':ACTIVE_REGISTRY_SHA256},sort_keys=True,separators=(',',':')).encode())

def checkout_state():
 return {'commit':_git('rev-parse','HEAD'),'ref':_git('rev-parse','--abbrev-ref','HEAD'),'registry_sha256':file_sha(REGISTRY)}

def module_generation(path:Path):
 return {'source':str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),'source_sha256':file_sha(path),'loaded_at':datetime.now(timezone.utc).isoformat(),'runtime_generation':GENERATION_ID,'active_control_plane_commit':ACTIVE_COMMIT}

def identity(*,loaded_modules=None,degraded_modules=None):
 current=checkout_state()
 drift=bool((ACTIVE_COMMIT and current.get('commit') and ACTIVE_COMMIT!=current['commit']) or (ACTIVE_REGISTRY_SHA256 and current.get('registry_sha256') and ACTIVE_REGISTRY_SHA256!=current['registry_sha256']))
 return {'schema':SCHEMA,'runtime_generation':GENERATION_ID,'started_at':STARTED_AT,'active_control_plane_commit':ACTIVE_COMMIT,'active_control_plane_ref':ACTIVE_REF,'active_registry_sha256':ACTIVE_REGISTRY_SHA256,'checkout':current,'restart_required':drift,'loaded_modules':dict(loaded_modules or {}),'degraded_modules':dict(degraded_modules or {})}
