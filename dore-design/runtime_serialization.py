#!/usr/bin/env python3
"""Serialize Doré Design workspace mutations inside the threaded resident.

The resident uses ThreadingHTTPServer. Historically /api/workspace POST handled
`mutate(workspace(), payload)`, which allowed two threads to read the same
revision and race their saves through the same temp path. Install this guard at
runtime so every mutation reloads the latest workspace while holding one
re-entrant process lock. Reads remain side-effect free and may run concurrently.
"""
from __future__ import annotations
import threading

_LOCK = threading.RLock()
_INSTALLED = False


def install(base):
    global _INSTALLED
    if _INSTALLED:
        return {'ok': True, 'installed': False, 'reason': 'already-installed'}

    original_workspace = base.workspace
    original_save = base.save
    original_mutate = base.mutate
    original_undo = base.undo

    def serialized_save(w, snapshot_before=True):
        with _LOCK:
            return original_save(w, snapshot_before=snapshot_before)

    def serialized_undo():
        with _LOCK:
            return original_undo()

    def serialized_mutate(_stale_workspace, payload):
        # Ignore the request thread's preloaded object. Reload only after the
        # writer lock is acquired so two concurrent POSTs cannot share a base
        # revision or overwrite each other.
        with _LOCK:
            current = original_workspace()
            return original_mutate(current, payload)

    base.save = serialized_save
    base.undo = serialized_undo
    base.mutate = serialized_mutate
    base.runtime_write_lock = _LOCK
    base.runtime_serialization = {
        'schema': 'dore.design.runtime-serialization.v1',
        'single_writer': True,
        'reload_after_lock': True,
        'threading_model': 'ThreadingHTTPServer',
    }
    _INSTALLED = True
    return {'ok': True, 'installed': True, **base.runtime_serialization}
