(() => {
  const root = document.querySelector('[data-dawn-video-surface]');
  if (!root) return;

  const frame = root.querySelector('[data-video-frame]');
  const sourceLink = root.querySelector('[data-source-link]');
  const params = new URLSearchParams(window.location.search);
  const source = params.get('source') || '';

  const parseYouTube = (value) => {
    try {
      const url = new URL(value);
      const host = url.hostname.toLowerCase();
      let id = '';
      if ((host === 'youtube.com' || host === 'www.youtube.com' || host === 'm.youtube.com') && url.pathname === '/watch') {
        id = url.searchParams.get('v') || '';
      } else if (host === 'youtu.be') {
        id = url.pathname.replace(/^\/+/, '').split('/')[0] || '';
      }
      return /^[A-Za-z0-9_-]{11}$/.test(id) ? id : '';
    } catch (_) {
      return '';
    }
  };

  const id = parseYouTube(source);
  if (!id) {
    root.dataset.viewerState = 'error';
    return;
  }

  frame.src = `https://www.youtube-nocookie.com/embed/${id}`;
  sourceLink.href = source;
  root.dataset.viewerState = 'ready';
})();
