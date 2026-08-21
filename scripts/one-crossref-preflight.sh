#!/usr/bin/env bash
set -euo pipefail

APP="static/one/one-app.js"
INDEX="static/one/index.html"
AUDIT="static/one/one-cross-reference-scripture-global-audit.js"
HEBREWS="static/one/one-cross-reference-scripture-hebrews.js"
MAJOR="static/one/one-cross-reference-scripture-major-prophets.js"
WISDOM="static/one/one-cross-reference-scripture-wisdom.js"
CANONICAL="static/one/one-cross-reference-scripture.js"

for f in "$APP" "$INDEX" "$AUDIT" "$HEBREWS" "$MAJOR" "$WISDOM" "$CANONICAL"; do
  test -s "$f" || { echo "FAIL missing required file: $f"; exit 1; }
done

# Internal/backend status copy must never be rendered to readers.
for forbidden in \
  '本條目前只保留串珠關係與說明' \
  '不以說明文字冒充經文引用' \
  'Scripture pending' \
  '經文待補' \
  'connection-scripture-missing'; do
  if grep -Fq "$forbidden" "$APP" "$INDEX"; then
    echo "FAIL backend-only copy leaked into reader-facing renderer: $forbidden"
    exit 1
  fi
done

# Missing Scripture must render nothing, never a placeholder paragraph.
grep -Fq 'const quote=scripture?`<blockquote data-one-scripture="true">${scripture}</blockquote>`:'"'"''"'"';' "$APP" || {
  echo 'FAIL connectionMarkup no longer uses an empty fallback for missing Scripture'
  exit 1
}

# Required Scripture layers and read-only audit must be loaded before the app renderer.
python3 - <<'PY'
from pathlib import Path
s=Path('static/one/index.html').read_text(encoding='utf-8')
required=[
 'one-cross-reference-scripture.js',
 'one-cross-reference-scripture-wisdom.js',
 'one-cross-reference-scripture-major-prophets.js',
 'one-cross-reference-scripture-hebrews.js',
 'one-cross-reference-scripture-global-audit.js',
 'one-app.js',
]
pos=[]
for name in required:
    i=s.find(name)
    if i<0: raise SystemExit(f'FAIL loader missing from index: {name}')
    pos.append(i)
if pos != sorted(pos):
    raise SystemExit('FAIL Scripture/audit/app load order is wrong')
PY

# Audit is read-only and must explicitly detect the original corruption modes.
grep -Fq 'explanationCopied' "$AUDIT" || { echo 'FAIL audit no longer checks explanation-as-Scripture'; exit 1; }
grep -Fq 'relationshipCopied' "$AUDIT" || { echo 'FAIL audit no longer checks relationship-as-Scripture'; exit 1; }
grep -Fq 'conflicts' "$AUDIT" || { echo 'FAIL audit no longer checks conflicting Scripture'; exit 1; }
grep -Fq 'missingRows' "$AUDIT" || { echo 'FAIL audit no longer checks missing Scripture'; exit 1; }

# Scripture fillers may use explanations for notes, but may never assign field 3 to field 4 in explanation-only layers.
if grep -Eq 'row\[3\][[:space:]]*=[[:space:]]*row\[2\]' "$WISDOM" "$MAJOR" "$HEBREWS"; then
  echo 'FAIL explanation-only Scripture layer promotes commentary into Scripture'
  exit 1
fi

echo 'PASS ONE cross-reference preflight: no backend UI leakage; loader order and audit guards intact.'
