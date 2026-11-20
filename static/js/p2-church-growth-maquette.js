/* P2 Church programme: the existing 3D architectural model is an image-like
   silent ornament. Prime as the Red Sea doors open; replay upon Church arrival.
   Never interfere with the P2 scroll owner or the door choreography. */
(() => {
  const stage = document.querySelector('.showcase');
  const frame = document.querySelector('.church-editorial__maquette');
  if (!stage || !frame) return;

  let wasChurch = false;
  let loaded = Boolean(frame.getAttribute('src'));

  const prime = () => {
    if (!loaded && frame.dataset.src) {
      // Fetch before the door is completely open, so the Sunday page is not blank.
      const url = frame.dataset.src;
      loaded = true;
      frame.src = url;
      delete frame.dataset.src;
    }
  };

  const replay = () => {
    if (frame.contentWindow && !frame.dataset.src) {
      frame.contentWindow.postMessage({type:'P2_CHURCH_BUILD_REPLAY'}, location.origin);
    }
  };

  frame.addEventListener('load', () => {
    if (stage.dataset.p2Phase === 'church') replay();
  });

  const sync = () => {
    const phase = stage.dataset.p2Phase;
    if (phase === 'red-sea' || phase === 'church') prime();
    const isChurch = phase === 'church';
    if (isChurch && !wasChurch) replay();
    wasChurch = isChurch;
  };

  new MutationObserver(sync).observe(stage, {
    attributes:true,
    attributeFilter:['data-p2-phase']
  });
  sync();
})();
