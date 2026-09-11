(() => {
  const roots = document.querySelectorAll('[data-dawn-deep-zoom]');
  if (!roots.length || typeof window.OpenSeadragon !== 'function') return;

  roots.forEach((root) => {
    const imageUrl = root.dataset.imageUrl;
    const iiifService = root.dataset.iiifService;
    const manifestUrl = root.dataset.iiifManifest;

    let tileSources;
    let mode;

    if (iiifService) {
      tileSources = iiifService.replace(/\/$/, '') + '/info.json';
      mode = 'iiif-image';
    } else if (imageUrl) {
      tileSources = { type: 'image', url: imageUrl };
      mode = 'single-image-fallback';
    } else {
      root.dataset.viewerState = 'unavailable';
      return;
    }

    const viewer = window.OpenSeadragon({
      element: root,
      tileSources,
      prefixUrl: 'https://cdn.jsdelivr.net/npm/openseadragon@6.1.0/build/openseadragon/images/',
      showNavigator: true,
      navigatorAutoFade: true,
      showRotationControl: false,
      showHomeControl: true,
      showFullPageControl: true,
      visibilityRatio: 1,
      constrainDuringPan: true,
      gestureSettingsMouse: { clickToZoom: true },
      gestureSettingsTouch: { pinchToZoom: true }
    });

    root.dataset.viewerMode = mode;
    root.dataset.viewerState = 'loading';

    viewer.addHandler('open', () => {
      root.dataset.viewerState = 'ready';
    });

    viewer.addHandler('open-failed', () => {
      root.dataset.viewerState = 'failed';
    });

    if (manifestUrl) {
      root.dataset.iiifManifestAvailable = 'true';
    }
  });
})();
