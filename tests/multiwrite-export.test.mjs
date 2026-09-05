import test from 'node:test';
import assert from 'node:assert/strict';
import { buildExportBackup, mergeExportSections, safeFilename } from '../static/multiwrite/export-core.mjs';

test('exports sections in source order without rewriting section text', () => {
  const sections = [
    { role: 'chapter', title: '第一章', text: '# 第一章\n原文 A。' },
    { role: 'appendix', title: '附錄', text: '附錄原文 B。' },
  ];
  assert.equal(mergeExportSections(sections), '# 第一章\n原文 A。\n\n附錄原文 B。');
});

test('JSON backup records draft state and complete text', () => {
  const book = { id: 'demo', title: '測試／書', subtitle: '副題', schema: 'multiwrite.book.v1' };
  const sections = [
    { role: 'chapter', title: '第一章', draft: true, text: '工作版本內容' },
    { role: 'appendix', title: '附錄', draft: false, text: '原稿內容' },
  ];
  const backup = buildExportBackup(book, sections, '2026-09-05T00:00:00.000Z');
  assert.equal(backup.schema, 'multiwrite.export.v1');
  assert.equal(backup.book.id, 'demo');
  assert.equal(backup.sections[0].draft, true);
  assert.equal(backup.sections[0].text, '工作版本內容');
  assert.equal(backup.sections[1].text, '原稿內容');
});

test('filename sanitizer removes filesystem-invalid characters', () => {
  assert.equal(safeFilename('神很遠／神很近: A/B?'), '神很遠／神很近- A-B-');
});
