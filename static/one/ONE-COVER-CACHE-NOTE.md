# ONE Cover Deployment Cache Note

When canonical cover CSS, the gilt-frame SVG, or a fixed Studio illustration changes, the production asset query version in `index.html` should be advanced in the same release. Until that version bump is made, browser or CDN cache may temporarily display the previous frame or Studio registry despite the repository containing the new master.

For the 2026-08-18 cover-master change, a hard reload is required if the old square/star cover persists before the next index asset-version bump.
