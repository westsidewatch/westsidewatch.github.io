#!/usr/bin/env python3
"""Stable entrypoint for the current Doré Design A2A worker."""
from design_intelligence_a2a_worker_v6 import legacy

if __name__ == '__main__':
    raise SystemExit(legacy.main())
