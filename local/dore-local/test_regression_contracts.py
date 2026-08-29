from pathlib import Path
core=Path(__file__).with_name('dore_local.py').read_text(encoding='utf-8')
ui=(Path(__file__).parents[2]/'static/dore/dore-search-runtime.js').read_text(encoding='utf-8')
assert "project_id IN (?, 'aug-history', 'dore-global')" in core
assert 'Language contract:' in core
assert 'Capability contract:' in core
assert 'System Boundary Assessment' in core
assert 'providerLabel' in ui
assert "version:'7.2.0'" in ui
print('DORE_REGRESSION_CONTRACT_PASS')
