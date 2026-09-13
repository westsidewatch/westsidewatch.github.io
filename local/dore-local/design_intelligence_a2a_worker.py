#!/usr/bin/env python3
from importlib import import_module

worker = import_module('design_intelligence_a2a_worker_v8')
legacy = worker.legacy

if __name__ == '__main__':
    raise SystemExit(worker.main())
