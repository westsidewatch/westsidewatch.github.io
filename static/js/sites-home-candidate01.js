(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-candidate-window]').forEach((screen) => {
    const cards = [...screen.querySelectorAll('.candidate-window-card')];
    const preview = screen.querySelector('.candidate-window-preview');
    if (!preview || !cards.length) return;
    const setPreview = (card) => {
      const image = card.querySelector('img');
      preview.style.setProperty('--candidate-image', `url("${image.currentSrc || image.src}")`);
      preview.querySelector('[data-preview-kind]').textContent = card.dataset.kind || '';
      preview.querySelector('[data-preview-title]').textContent = card.dataset.title || '';
      preview.querySelector('[data-preview-subtitle]').textContent = card.dataset.subtitle || '';
      screen.classList.add('is-window-active');
      cards.forEach((item) => item.toggleAttribute('data-active', item === card));
    };
    const clearPreview = () => {
      screen.classList.remove('is-window-active');
      cards.forEach((item) => item.removeAttribute('data-active'));
    };
    cards.forEach((card) => {
      card.addEventListener('mouseenter', () => setPreview(card));
      card.addEventListener('focus', () => setPreview(card));
      card.addEventListener('mouseleave', () => { if (!reduce) clearPreview(); });
      card.addEventListener('blur', clearPreview);
    });
    screen.addEventListener('mouseleave', clearPreview);
  });
})();
