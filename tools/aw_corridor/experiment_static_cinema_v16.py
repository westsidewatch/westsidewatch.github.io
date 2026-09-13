#!/usr/bin/env python3
"""Compatibility launcher for AW-011 strict three-blade V17.

The existing topology-probe workflow watches this path. Keep this launcher only
as a trigger/entry bridge until the workflow path list is updated safely.
"""
from experiment_static_cinema_v17 import main

if __name__ == '__main__':
    raise SystemExit(main())
