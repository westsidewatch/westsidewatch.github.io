/* Restart the silent architecture-growth ornament when the Church page opens.
   Observe the established P2 phase; never change its scroll/door choreography. */
(() => {
  const stage = document.querySelector('.showcase');
  const frame = document.querySelector('.church-editorial__maquette');
  if (!stage || !frame) return;

  let wasChurch = stage.dataset.p2Phase === 'church';
  const startBuild = () => {
    if (frame.dataset.src) {
      // WebGL and model downloads begin only on entering the Church page.
      frame.src = frame.dataset.src;
      delete frame.dataset.src;
    } else {
      frame.contentWindow?.postMessage({ type: 'P2_CHURCH_BUILD_REPLAY' }, location.origin);
    }
  };
  const onPhaseChange = () => {
    const isChurch = stage.dataset.p2Phase === 'church';
    if (isChurch && !wasChurch) {
      startBuild();
    }
    wasChurch = isChurch;
  };

  if (wasChurch) startBuild();

  new MutationObserver(onPhaseChange).observe(stage, {
    attributes: true,
    attributeFilter: ['data-p2-phase'],
  });
})();
