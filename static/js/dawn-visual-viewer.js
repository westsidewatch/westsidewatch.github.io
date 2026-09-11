(() => {
  const roots = document.querySelectorAll('[data-dawn-deep-zoom]');
  if (!roots.length || typeof window.OpenSeadragon !== 'function') return;

  roots.forEach((root) => {
    const imageUrl = root.dataset.imageUrl;
    const iiifService = root.dataset.iiifService;
    const manifestUrl = root.dataset.iiifManifest;
    const regionNodes = Array.from(root.querySelectorAll('[data-visual-region]'));
    const regionMap = new Map();

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

    const focusRegion = (regionId) => {
      const region = regionMap.get(regionId);
      if (!region) return;
      viewer.viewport.fitBounds(region.bounds, true);
      root.dataset.activeRegion = regionId;
      document.querySelectorAll(`[data-region-target="${CSS.escape(regionId)}"]`).forEach((button) => {
        button.setAttribute('aria-pressed', 'true');
      });
      document.querySelectorAll('[data-region-target]').forEach((button) => {
        if (button.dataset.regionTarget !== regionId) button.setAttribute('aria-pressed', 'false');
      });
    };

    viewer.addHandler('open', () => {
      root.dataset.viewerState = 'ready';

      regionNodes.forEach((node) => {
        const x = Number(node.dataset.regionX);
        const y = Number(node.dataset.regionY);
        const width = Number(node.dataset.regionW);
        const height = Number(node.dataset.regionH);
        if (![x, y, width, height].every(Number.isFinite) || width <= 0 || height <= 0) return;

        const regionId = node.dataset.regionId || '';
        const bounds = viewer.viewport.imageToViewportRectangle(x, y, width, height);
        const overlay = document.createElement('button');
        overlay.type = 'button';
        overlay.className = 'dawn-visual-region-overlay';
        overlay.dataset.regionId = regionId;
        overlay.dataset.provenance = node.dataset.regionProvenance || '';
        overlay.setAttribute('aria-label', node.dataset.regionLabel || 'Visual region');
        overlay.title = node.dataset.regionLabel || '';

        regionMap.set(regionId, { bounds, overlay });
        viewer.addOverlay({ element: overlay, location: bounds });
        overlay.addEventListener('click', () => focusRegion(regionId));
      });

      document.querySelectorAll('[data-region-target]').forEach((button) => {
        button.setAttribute('aria-pressed', 'false');
        button.addEventListener('click', () => focusRegion(button.dataset.regionTarget));
      });
    });

    viewer.addHandler('home', () => {
      delete root.dataset.activeRegion;
      document.querySelectorAll('[data-region-target]').forEach((button) => button.setAttribute('aria-pressed', 'false'));
    });

    viewer.addHandler('open-failed', () => {
      root.dataset.viewerState = 'failed';
      if (imageUrl && mode === 'iiif-image') root.dataset.viewerFallback = 'single-image-available';
    });

    if (manifestUrl) root.dataset.iiifManifestAvailable = 'true';
  });
})();
