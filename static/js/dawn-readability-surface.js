(() => {
  const root = document.querySelector('[data-dawn-readability-surface]');
  if (!root) return;

  const params = new URLSearchParams(window.location.search);
  const payloadPath = params.get('payload') || '/dawn-library/readability/acceptance.json';
  if (!payloadPath.startsWith('/dawn-library/readability/')) {
    root.dataset.viewerState = 'error';
    return;
  }

  fetch(payloadPath, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw new Error(`payload HTTP ${response.status}`);
      return response.json();
    })
    .then((payload) => {
      if (!payload || payload.external !== true || payload.ownership !== 'external' || !payload.sourceUrl) {
        throw new Error('invalid readability payload');
      }
      root.querySelector('[data-readability-title]').textContent = payload.title || 'Readable article';
      root.querySelector('[data-readability-byline]').textContent = payload.byline || '';
      root.querySelector('[data-readability-excerpt]').textContent = payload.excerpt || '';
      root.querySelector('[data-readability-source]').href = payload.sourceUrl;
      root.dataset.viewerState = 'ready';
    })
    .catch(() => {
      root.dataset.viewerState = 'error';
    });
})();
