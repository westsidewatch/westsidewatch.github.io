from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITOR = (ROOT / 'static/multiwrite/book-editor.mjs').read_text()
BRIDGE = (ROOT / 'static/multiwrite/book-compile-bridge.mjs').read_text()


def test_editorial_report_has_three_action_classes():
    assert 'AUTO_FIX' in EDITOR
    assert 'SUGGESTED_COMPLETION' in EDITOR
    assert 'AUTHORIAL_DECISION_REQUIRED' in EDITOR
    assert "dore.editorial-report.v1" in EDITOR


def test_substantive_or_doctrinal_rewrite_is_never_silent():
    assert "doctrinalOrSubstantiveRewriteAllowed: false" in EDITOR
    assert "humanAuthorityDecisive: true" in EDITOR
    assert "silentActionsAllowed: ['AUTO_FIX']" in EDITOR


def test_generated_completion_stays_proposed():
    assert "generatedCompletionMustRemainProposed: true" in EDITOR
    assert '不自動生成進正文' in EDITOR
    assert '不得覆寫作者立場' in EDITOR


def test_book_compile_runs_editorial_analysis_before_artifact_export():
    compile_block = BRIDGE.split('export async function compileCurrentBook()', 1)[1]
    assert 'analyzeBookForPublication(bookModel)' in compile_block
    assert 'buildBookBuild({' in compile_block
    assert compile_block.index('analyzeBookForPublication(bookModel)') < compile_block.index('buildBookBuild({')
    assert 'return await original.call(button, event)' in BRIDGE


def test_hard_editorial_block_stops_export():
    assert "editorialReport.readiness === 'blocked'" in BRIDGE
    blocked = BRIDGE.split("editorialReport.readiness === 'blocked'", 1)[1]
    assert 'return undefined' in blocked


def test_authorial_review_is_visible_but_not_silently_resolved():
    assert "editorialReport.readiness === 'review-required'" in BRIDGE
    assert 'authorialDecisions' in EDITOR
    assert '需作者決定' in BRIDGE


def test_mechanical_fix_boundary_exists_without_prose_mutation():
    assert 'applyMechanicalEditorialFixes' in EDITOR
    assert 'does not mutate prose' in EDITOR
    assert 'applied: []' in EDITOR
