(() => {
  const roots = document.querySelectorAll('[data-dawn-deep-zoom]');
  if (!roots.length || typeof window.OpenSeadragon !== 'function') return;

  roots.forEach((root) => {
    const imageUrl = root.dataset.imageUrl;
    const iiifService = root.dataset.iiifService;
    const manifestUrl = root.dataset.iiifManifest;
    const regionNodes = Array.from(root.querySelectorAll('[data-visual-region]'));

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

      regionNodes.forEach((node) => {
        const x = Number(node.dataset.regionX);
        const y = Number(node.dataset.regionY);
        const width = Number(node.dataset.regionW);
        const height = Number(node.dataset.regionH);
        if (![x, y, width, height].every(Number.isFinite) || width <= 0 || height <= 0) return;

        const overlay = document.createElement('button');
        overlay.type = 'button';
        overlay.className = 'dawn-visual-region-overlay';
        overlay.dataset.regionId = node.dataset.regionId || '';
        overlay.dataset.provenance = node.dataset.regionProvenance || '';
        overlay.setAttribute('aria-label', node.dataset.regionLabel || 'Visual region');
        overlay.title = node.dataset.regionLabel || '';

        viewer.addOverlay({
          element: overlay,
          location: viewer.viewport.imageToViewportRectangle(x, y, width, height)
        });

        overlay.addEventListener('click', () => {
          viewer.viewport.fitBounds(
            viewer.viewport.imageToViewportRectangle(x, y, width, height),
            true
          );
        });
      });
    });

    viewer.addHandler('open-failed', () => {
      root.dataset.viewerState = 'failed';
      if (imageUrl && mode === 'iiif-image') {
        root.dataset.viewerFallback = 'single-image-available';
      }
    });

    if (manifestUrl) root.dataset.iiifManifestAvailable = 'true';
  });
})();
