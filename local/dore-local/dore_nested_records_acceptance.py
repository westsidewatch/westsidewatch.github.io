#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

for rel in (
    'docs/dore/design/README.md',
    'docs/dore/film/README.md',
    'docs/dore/lessons/README.md',
):
    assert (ROOT / rel).exists(), f'missing nested index: {rel}'

film_root = ROOT / 'docs/dore/film'
film_files = {p.relative_to(ROOT).as_posix() for p in film_root.rglob('*') if p.is_file()}
expected_film = {
    'docs/dore/film/README.md',
    'docs/dore/film/DORÉ-FILM-PRODUCTION-HANDBOOK.md',
    'docs/dore/film/DORÉ-ANCHORED-WORLD-ENGINEERING-TRANSLATION.md',
    'docs/dore/film/DORÉ-ANCHORED-WORLD-ROUTE-01.md',
    'docs/dore/film/aw011-anchor-corridor-v1.json',
    'docs/dore/film/tools/aw011-anchor-package.py',
    'docs/dore/film/tools/camera-canvas-placement.js',
    'docs/dore/film/tools/camera-spine-parity-check.py',
    'docs/dore/film/tools/camera-spine-timeline.js',
    'docs/dore/film/tools/canvas-placement-validate.py',
    'docs/dore/film/tools/import-camera-spine.py',
    'docs/dore/film/CAMERA-SPINE-EXPERIMENT-01-ACCEPTANCE.md',
    'docs/dore/film/CANVAS-PLACEMENT-EXPERIMENT-01-ACCEPTANCE.md',
    'docs/dore/film/EXPERIMENTAL-FILM-01.md',
    'docs/dore/film/camera-spine-experiment-01.html',
    'docs/dore/film/camera-spine-experiment-01.json',
    'docs/dore/film/canvas-placement-experiment-01.json',
}
assert film_files == expected_film, f'film record drift: {sorted(film_files ^ expected_film)}'

film_index = (film_root / 'README.md').read_text()
assert 'director-level visual review' in film_index
assert 'never, by itself, proof' in film_index
assert 'ACTIVE PRODUCTION HANDBOOK' in (film_root / 'DORÉ-FILM-PRODUCTION-HANDBOOK.md').read_text()
assert 'VISUAL DIRECTOR REVIEW REQUIRED' in (film_root / 'CAMERA-SPINE-EXPERIMENT-01-ACCEPTANCE.md').read_text()

lesson_root = ROOT / 'docs/dore/lessons'
lesson_files = {p.relative_to(ROOT).as_posix() for p in lesson_root.rglob('*') if p.is_file()}
expected_lessons = {
    'docs/dore/lessons/README.md',
    'docs/dore/lessons/ONE-LESSON-001-GOSPEL-HARMONY-AUDIT.md',
}
assert lesson_files == expected_lessons, f'lesson record drift: {sorted(lesson_files ^ expected_lessons)}'
assert 'do not become product architecture' in (lesson_root / 'README.md').read_text()

design_root = ROOT / 'docs/dore/design'
design_visible = {p.relative_to(ROOT).as_posix() for p in design_root.glob('*') if p.is_file() and not p.name.startswith('.')}
expected_design_visible = {
    'docs/dore/design/README.md',
    'docs/dore/design/candidate01-4w-transparent-label-hotfix.md',
}
assert design_visible == expected_design_visible, f'design visible record drift: {sorted(design_visible ^ expected_design_visible)}'

print(f'DORE_NESTED_RECORDS=PASS film={len(film_files)} lessons={len(lesson_files)} design_visible={len(design_visible)}')
