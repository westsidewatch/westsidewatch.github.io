import test from 'node:test';
import assert from 'node:assert/strict';
import { buildBook, mergeImports, parseStructuredText, validateBook } from '../static/multiwrite/import-core.mjs';

test('detects book, chapters, sections and appendix without rewriting content', () => {
  const source = `# 測試書\n\n前置文字\n\n# 第一章　開始\n\n第一章正文。\n\n## 第一節\n\n節正文。\n\n# 附錄一　資料\n\n附錄原文。`;
  const nodes = parseStructuredText(source, 'sample.md');
  assert.deepEqual(nodes.map((n) => n.role), ['book_title', 'chapter', 'section', 'appendix']);
  assert.equal(nodes[1].content.trim(), '第一章正文。');
  assert.equal(nodes[2].content.trim(), '節正文。');
  assert.equal(nodes[3].content.trim(), '附錄原文。');
});

test('preserves source order across multiple files', () => {
  const nodes = mergeImports([
    { sourceFile: 'a.md', text: '# 第一章\nA' },
    { sourceFile: 'b.md', text: '# 第二章\nB' }
  ]);
  assert.deepEqual(nodes.map((n) => n.order), [0, 1]);
  assert.deepEqual(nodes.map((n) => n.sourceFile), ['a.md', 'b.md']);
});

test('manual role correction remains valid book data', () => {
  const nodes = parseStructuredText('# 一段標題\n內容', 'draft.md');
  nodes[0].role = 'appendix';
  const book = buildBook({ title: '手動修正', nodes, sources: [{ name: 'draft.md' }] });
  assert.equal(book.import.aiTransformed, false);
  assert.equal(book.nodes[0].role, 'appendix');
  assert.equal(validateBook(book).valid, true);
});
