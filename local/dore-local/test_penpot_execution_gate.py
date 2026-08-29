#!/usr/bin/env python3
"""Static contract checks for Penpot execution and visual export gates."""
from pathlib import Path
p=Path(__file__).with_name('penpot_agent.py').read_text(encoding='utf-8')
assert "mutation_succeeded=False" in p
assert "penpot_no_mutation_executed" in p
assert "penpot_no_visual_evidence" in p
assert "penpot_visual_not_passed" in p
assert "verified':True" in p
assert "filePath-fallback" in p
assert "base64.b64encode" in p
assert "image_count" in p
assert "export_shape" in p
print('DORE_PENPOT_EXECUTION_GATE_PASS')
