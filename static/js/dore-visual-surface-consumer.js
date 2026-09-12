(() => {
  'use strict';

  const CONTRACT = Object.freeze({
    schema: 'dore.visual-surface-consumer.v1',
    source: 'dore.visual-surface-orchestrator.v1',
    graphOwns: 'identity+relationships',
    surfaceOwns: 'presentation+motion',
    products: 'shared',
  });

  const roleClass = role => role ? `dore-surface--role-${role}` : '';
  const motionClass = motion => motion ? `dore-surface--motion-${motion}` : '';

  function clearClasses(element) {
    [...element.classList].forEach(name => {
      if (name.startsWith('dore-surface--role-') || name.startsWith('dore-surface--motion-')) element.classList.remove(name);
    });
  }

  function apply(element, assignment = {}) {
    if (!element) return null;
    const role = String(assignment.role || element.dataset.editorialRole || '').trim();
    const motion = String(assignment.motion || element.dataset.editorialMotion || '').trim();
    const surface = String(assignment.surface || element.dataset.editorialSurface || '').trim();
    const preset = String(assignment.preset || element.dataset.surfacePreset || 'card-8x5').trim();
    const product = String(assignment.product || element.dataset.doreSurfaceProduct || '').trim();
    const weight = Number(assignment.weight || element.dataset.editorialWeight || 1) || 1;

    clearClasses(element);
    if (role) element.classList.add(roleClass(role));
    if (motion) element.classList.add(motionClass(motion));
    element.dataset.doreSurfaceConsumer = CONTRACT.schema;
    element.dataset.doreSurfaceSource = CONTRACT.source;
    if (product) element.dataset.doreSurfaceProduct = product;
    if (role) element.dataset.editorialRole = role;
    element.dataset.editorialWeight = String(weight);
    if (motion) element.dataset.editorialMotion = motion;
    if (surface) element.dataset.editorialSurface = surface;
    if (preset) element.dataset.surfacePreset = preset;
    element.style.setProperty('--dore-surface-weight', String(weight));
    return { product, role, weight, motion, surface, preset };
  }

  function consume(root = document) {
    root.querySelectorAll('[data-editorial-role]').forEach(element => apply(element));
  }

  function attachOne(root = document) {
    const now = root.querySelector('.now');
    const art = root.querySelector('#chapter-cover-art');
    if (!now || !art) return false;
    const sync = () => apply(now, {
      product: 'one',
      role: 'primary',
      weight: 2,
      motion: art.hidden ? 'near-still' : 'focus',
      surface: 'one-chapter-hero',
      preset: 'card-8x5',
    });
    sync();
    new MutationObserver(sync).observe(art, { attributes: true, attributeFilter: ['src', 'hidden'] });
    return true;
  }

  window.DoreVisualSurfaceConsumer = Object.freeze({ CONTRACT, apply, consume, attachOne });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => consume(), { once: true });
  else consume();
})();
