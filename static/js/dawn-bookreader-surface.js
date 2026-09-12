const root = document.querySelector('[data-dawn-bookreader-surface]');
if (root) {
  const params = new URLSearchParams(location.search);
  const itemId = (params.get('id') || '').trim();
  const frame = root.querySelector('[data-bookreader-frame]');
  const source = root.querySelector('[data-bookreader-source]');
  const status = root.querySelector('[data-bookreader-status]');
  const valid = /^[A-Za-z0-9._-]+$/.test(itemId);

  if (!valid) {
    root.dataset.viewerState = 'invalid-source';
    status.textContent = '無效的 Internet Archive item id。';
  } else {
    const detailsUrl = `https://archive.org/details/${itemId}`;
    const embedUrl = `https://archive.org/embed/${itemId}`;
    root.dataset.externalSource = 'true';
    root.dataset.viewerState = 'loading';
    source.href = detailsUrl;
    frame.src = embedUrl;
    frame.addEventListener('load', () => {
      root.dataset.viewerState = 'ready';
      status.textContent = 'Internet Archive BookReader · external source';
    }, { once: true });
  }
}
