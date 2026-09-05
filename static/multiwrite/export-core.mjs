export function safeFilename(value = 'book') {
  const cleaned = String(value)
    .replace(/[\\/:*?"<>|]/g, '-')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/[. ]+$/g, '');
  return cleaned || 'book';
}

export function mergeExportSections(sections = []) {
  return sections.map((section) => String(section.text ?? '')).join('\n\n');
}

export function buildExportBackup(book, sections, exportedAt = new Date().toISOString()) {
  return {
    schema: 'multiwrite.export.v1',
    exportedAt,
    book: {
      id: book?.id || '',
      title: book?.title || '',
      subtitle: book?.subtitle || '',
      englishSubtitle: book?.englishSubtitle || '',
      sourceSchema: book?.schema || '',
    },
    sections: sections.map((section, index) => ({
      index,
      role: section.role || 'body',
      title: section.title || '',
      draft: Boolean(section.draft),
      text: String(section.text ?? ''),
    })),
  };
}
