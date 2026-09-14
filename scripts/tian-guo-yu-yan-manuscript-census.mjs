#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const projectId = 'book.tian-guo-yu-yan';
const manuscriptPath = process.argv[2] || 'data/publishing/manuscripts/tian-guo-yu-yan.md';
const outputPath = process.argv[3] || 'data/publishing/tian-guo-yu-yan.manuscript-census.v1.json';

if (!fs.existsSync(manuscriptPath)) {
  console.error(`Canonical manuscript is not materialized: ${manuscriptPath}`);
  process.exit(2);
}

const raw = fs.readFileSync(manuscriptPath, 'utf8');
if (!raw.trim()) {
  console.error('Canonical manuscript is empty. Refusing census.');
  process.exit(3);
}

const normalizeNewlines = (text) => text.replace(/\r\n?/g, '\n');
const normalized = normalizeNewlines(raw);
const hasLeadingBom = normalized.startsWith('\uFEFF');

const sha256 = crypto.createHash('sha256').update(raw, 'utf8').digest('hex');
const hanMatches = normalized.match(/[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]/gu) || [];
const nonWhitespaceMatches = normalized.match(/\S/gu) || [];

// Census prose without changing or rewriting the source. UTF-8 BOM and common
// Markdown controls are ignored only in the analytical view; canonical bytes stay untouched.
const proseForCount = normalized
  .replace(/^\uFEFF/, '')
  .replace(/^---\s*$/gm, '')
  .replace(/^#{1,6}\s+/gm, '')
  .replace(/^>\s?/gm, '')
  .replace(/\*\*|__|\*|_/g, '')
  .replace(/`{1,3}/g, '')
  .replace(/\\$/gm, '');
const proseNonWhitespaceMatches = proseForCount.match(/\S/gu) || [];

const lines = normalized.split('\n');
const headings = [];
let charOffset = 0;
for (let i = 0; i < lines.length; i += 1) {
  const line = lines[i];
  const lineForHeadingMatch = i === 0 ? line.replace(/^\uFEFF/, '') : line;
  const match = lineForHeadingMatch.match(/^(#{1,6})\s+(.+?)\s*$/);
  if (match) {
    headings.push({
      level: match[1].length,
      text: match[2],
      line: i + 1,
      charOffset
    });
  }
  charOffset += line.length + (i < lines.length - 1 ? 1 : 0);
}

const topLevelSections = headings
  .filter((heading) => heading.level === 1)
  .map((heading, index, arr) => ({
    id: `section-${String(index + 1).padStart(2, '0')}`,
    title: heading.text,
    startLine: heading.line,
    startCharOffset: heading.charOffset,
    endCharOffsetExclusive: arr[index + 1]?.charOffset ?? normalized.length
  }));

for (const section of topLevelSections) {
  const text = normalized.slice(section.startCharOffset, section.endCharOffsetExclusive);
  section.hanCharacters = (text.match(/[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]/gu) || []).length;
  section.nonWhitespaceCharacters = (text.match(/\S/gu) || []).length;
}

const result = {
  schema: 'dore.manuscript-census.v1',
  projectId,
  source: {
    path: manuscriptPath,
    byteLength: Buffer.byteLength(raw, 'utf8'),
    sha256,
    newlineNormalizationAppliedForAnalysisOnly: raw !== normalized,
    leadingBomIgnoredForAnalysisOnly: hasLeadingBom,
    sourceBytesModified: false
  },
  exact: {
    hanCharacters: hanMatches.length,
    nonWhitespaceCharacters: nonWhitespaceMatches.length,
    proseNonWhitespaceCharactersExcludingCommonMarkdownControls: proseNonWhitespaceMatches.length,
    lines: lines.length,
    markdownHeadings: headings.length,
    topLevelSections: topLevelSections.length
  },
  headings,
  topLevelSectionCensus: topLevelSections,
  authority: {
    censusMayRewriteSource: false,
    authorThesisAuthority: true,
    observedHeadingsAreNotFrozenToc: true
  }
};

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(result.exact));
