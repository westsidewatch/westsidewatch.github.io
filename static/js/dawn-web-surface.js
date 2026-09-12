(() => {
  const ROOT = document.querySelector('[data-dawn-biblical-world]');
  const DIALOG = document.querySelector('[data-dawn-web-surface-dialog]');
  if (!ROOT || !DIALOG) return;

  const LIST = ROOT.querySelector('[data-dawn-biblical-world-list]');
  const STATUS = ROOT.querySelector('[data-dawn-biblical-world-status]');
  const FRAME = DIALOG.querySelector('[data-dawn-web-surface-frame]');
  const TITLE = DIALOG.querySelector('[data-dawn-web-surface-title]');
  const SOURCE = DIALOG.querySelector('[data-dawn-web-surface-source]');
  const OPEN = DIALOG.querySelector('[data-dawn-web-surface-open]');
  const CLOSE = DIALOG.querySelector('[data-dawn-web-surface-close]');
  const CATALOG_URL = '/dawn-library/biblical-world/catalog.json';

  function approvedGutenbergPointer(item) {
    return (item.sources || []).find((source) => {
      try {
        const url = new URL(source.url);
        return source.provider === 'Project Gutenberg' &&
          url.protocol === 'https:' &&
          (url.hostname === 'www.gutenberg.org' || url.hostname === 'gutenberg.org') &&
          url.pathname.startsWith('/ebooks/');
      } catch (_) {
        return false;
      }
    });
  }

  function closeSurface() {
    FRAME.removeAttribute('src');
    FRAME.title = '';
    if (typeof DIALOG.close === 'function') DIALOG.close();
    else DIALOG.removeAttribute('open');
  }

  function openSurface(item, pointer) {
    const title = item.work?.title || item.id || 'External resource';
    TITLE.textContent = title;
    SOURCE.textContent = 'Project Gutenberg · external source';
    OPEN.href = pointer.url;
    FRAME.src = pointer.url;
    FRAME.title = `${title} — Project Gutenberg preview`;
    if (typeof DIALOG.showModal === 'function') DIALOG.showModal();
    else DIALOG.setAttribute('open', '');
  }

  function card(item, pointer) {
    const article = document.createElement('article');
    article.className = 'dawn-web-card';
    const title = item.work?.title || item.id || 'Untitled';
    const author = item.work?.author || '';
    const relations = (item.relations || []).slice(0, 3);

    const meta = document.createElement('p');
    meta.className = 'dawn-web-card__meta';
    meta.textContent = 'PROJECT GUTENBERG · EXTERNAL';

    const heading = document.createElement('h3');
    heading.textContent = title;
    const byline = document.createElement('p');
    byline.className = 'dawn-web-card__author';
    byline.textContent = author;

    const tags = document.createElement('p');
    tags.className = 'dawn-web-card__relations';
    tags.textContent = relations.join(' · ');

    const actions = document.createElement('div');
    actions.className = 'dawn-web-card__actions';
    const preview = document.createElement('button');
    preview.type = 'button';
    preview.className = 'dawn-web-card__preview';
    preview.textContent = '在黎明書局閱讀';
    preview.addEventListener('click', () => openSurface(item, pointer));

    const external = document.createElement('a');
    external.href = pointer.url;
    external.target = '_blank';
    external.rel = 'noopener noreferrer';
    external.textContent = '原網站 ↗';

    actions.append(preview, external);
    article.append(meta, heading, byline, tags, actions);
    return article;
  }

  async function load() {
    STATUS.textContent = '正在連接外部館藏…';
    try {
      const response = await fetch(CATALOG_URL, { credentials: 'same-origin' });
      if (!response.ok) throw new Error(`catalog ${response.status}`);
      const catalog = await response.json();
      const items = (catalog.items || [])
        .map((item) => [item, approvedGutenbergPointer(item)])
        .filter(([, pointer]) => pointer);

      LIST.replaceChildren(...items.map(([item, pointer]) => card(item, pointer)));
      STATUS.textContent = `${items.length} 項正式館藏可直接預覽；正文仍保留在 Project Gutenberg。`;
      ROOT.dataset.ready = 'true';
    } catch (error) {
      STATUS.textContent = '外部館藏暫時無法載入。';
      ROOT.dataset.ready = 'false';
      console.warn('[Dawn Web Surface]', error);
    }
  }

  CLOSE?.addEventListener('click', closeSurface);
  DIALOG.addEventListener('cancel', (event) => {
    event.preventDefault();
    closeSurface();
  });
  DIALOG.addEventListener('click', (event) => {
    if (event.target === DIALOG) closeSurface();
  });

  load();
})();
