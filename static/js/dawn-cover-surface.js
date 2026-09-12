const root = document.querySelector('[data-dawn-cover-surface]');
if (root) {
  const params = new URLSearchParams(location.search);
  const source = params.get('src') || '';
  const image = root.querySelector('[data-cover-image]');
  const link = root.querySelector('[data-cover-source]');
  const status = root.querySelector('[data-cover-status]');

  let sourceUrl;
  try {
    sourceUrl = new URL(source);
    if (sourceUrl.protocol !== 'https:') throw new Error('https required');
  } catch (_) {
    root.dataset.viewerState = 'invalid-source';
    status.textContent = '無效的封面來源。';
    throw new Error('Dawn Cover Surface requires an HTTPS ?src= URL');
  }

  root.dataset.externalSource = 'true';
  root.dataset.viewerState = 'loading';
  link.href = sourceUrl.href;
  image.src = sourceUrl.href;

  image.addEventListener('load', () => {
    root.dataset.viewerState = 'ready';
    status.textContent = 'External cover · pointer only';
  }, { once: true });

  image.addEventListener('error', () => {
    root.dataset.viewerState = 'failed';
    status.textContent = '封面暫時不可用。';
  }, { once: true });
}
