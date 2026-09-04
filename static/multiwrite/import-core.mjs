const CHINESE_NUM = '[一二三四五六七八九十百千零〇兩两\d]+';

export const ROLE_OPTIONS = [
  ['book_title', '書名'],
  ['front_matter', '前置內容'],
  ['chapter', '章'],
  ['section', '節'],
  ['appendix', '附錄'],
  ['body', '正文']
];

export function makeId(prefix = 'node') {
  const random = Math.random().toString(36).slice(2, 9);
  return `${prefix}-${Date.now().toString(36)}-${random}`;
}

export function normalizeText(input = '') {
  return String(input).replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n');
}

export function detectHeading(line, index = 0) {
  const raw = line.trim();
  if (!raw) return null;

  const md = raw.match(/^(#{1,6})\s+(.+)$/);
  if (md) {
    const level = md[1].length;
    const title = md[2].trim();
    return { level, title, role: inferRole(title, level, index) };
  }

  const chapterRe = new RegExp(`^第${CHINESE_NUM}章(?:補遺)?[\s　:：—-]*(.*)$`);
  const chapter = raw.match(chapterRe);
  if (chapter) return { level: 1, title: raw, role: 'chapter' };

  if (/^(附錄|附录|Appendix)\b/i.test(raw)) return { level: 1, title: raw, role: 'appendix' };
  if (/^(序言|前言|引言|後記|后记|Preface|Foreword|Introduction|Afterword)\b/i.test(raw)) {
    return { level: 1, title: raw, role: 'front_matter' };
  }
  return null;
}

export function inferRole(title, level = 1, index = 0) {
  const t = title.trim();
  if (/^(附錄|附录|Appendix)\b/i.test(t)) return 'appendix';
  if (new RegExp(`^第${CHINESE_NUM}章`).test(t) || /^Chapter\s+\w+/i.test(t)) return 'chapter';
  if (/^(序言|前言|引言|後記|后记|Preface|Foreword|Introduction|Afterword)\b/i.test(t)) return 'front_matter';
  if (index === 0 && level === 1) return 'book_title';
  if (level === 1) return 'chapter';
  if (level === 2) return 'section';
  return 'body';
}

export function parseStructuredText(input, sourceFile = '貼上文字') {
  const text = normalizeText(input);
  const lines = text.split('\n');
  const nodes = [];
  let current = null;
  let buffer = [];

  const flush = () => {
    if (!current && !buffer.length) return;
    if (!current) {
      const content = buffer.join('\n');
      if (content.trim()) {
        nodes.push({
          id: makeId('body'),
          role: 'body',
          title: '正文',
          content,
          sourceFile,
          order: nodes.length,
          headingLevel: null
        });
      }
    } else {
      current.content = buffer.join('\n').replace(/^\n+/, '');
      current.order = nodes.length;
      nodes.push(current);
    }
    current = null;
    buffer = [];
  };

  lines.forEach((line) => {
    const heading = detectHeading(line, nodes.length);
    if (heading) {
      flush();
      current = {
        id: makeId('part'),
        role: heading.role,
        title: heading.title,
        content: '',
        sourceFile,
        order: 0,
        headingLevel: heading.level,
        originalHeading: line
      };
    } else {
      buffer.push(line);
    }
  });
  flush();

  if (!nodes.length && text.trim()) {
    nodes.push({ id: makeId('body'), role: 'body', title: sourceFile, content: text, sourceFile, order: 0, headingLevel: null });
  }
  return nodes;
}

export function mergeImports(imports) {
  return imports.flatMap(({ sourceFile, text }) => parseStructuredText(text, sourceFile))
    .map((node, order) => ({ ...node, order }));
}

export function buildBook({ title, subtitle = '', nodes, sources = [] }) {
  return {
    schema: 'multiwrite.book.v1',
    id: makeId('book'),
    title: title || nodes.find((n) => n.role === 'book_title')?.title || '未命名書稿',
    subtitle,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    import: {
      mode: 'manual',
      aiTransformed: false,
      sourceCount: sources.length,
      sources
    },
    nodes: nodes.map((node, order) => ({ ...node, order }))
  };
}

export function validateBook(book) {
  const errors = [];
  if (!book?.title?.trim()) errors.push('缺少書名');
  if (!Array.isArray(book?.nodes) || !book.nodes.length) errors.push('沒有可匯入內容');
  if (Array.isArray(book?.nodes)) {
    const orders = book.nodes.map((n) => n.order);
    const stable = orders.every((n, i) => n === i);
    if (!stable) errors.push('章節順序不連續');
  }
  return { valid: errors.length === 0, errors };
}
