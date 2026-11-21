# PARADISO · GitHub cinema (rebuild v1)

An independent `/paradiso/` static application. Host in `static/paradiso/` under the existing Hugo GitHub Pages pipeline. It does not import any existing Westside Watch CSS, JS, data, or components and does not modify the `/cinema/` section.

## Live functionality

- Search + genre navigation: original label `基督福音劇集` preserved
- Native WebM / MP4 and hls.js HLS playback inside a single modal
- Episodes, resume time, retry/fallback, favorites, local browser-only collection
- Curated, genuine complete movies from source-identified Wikimedia Commons; runtime playback remains unverified until observed from external network
- No embedded third-party ad players, scripts or casino sites; `hls.js` is loaded only when needed from jsDelivr

## Files

- index.html — standalone public frontend
- styles.css — responsive cinema styling
- app.js — player and library state
- catalog.json — authoritative catalog; every entry must link to a genuine complete licensed/authorized source

## Admission gate

A source must be a real complete film or the complete intended episode with a confirmed rights basis, not a demo clip, trailer or test asset. The listing of a media file and a working player are not proof of entire-file decode or absence of inserted visual ads. Before promoting any new commercial title to production, validate permission, complete episodes, playback and advertising.

## Local checks

`node --check app.js`; `python -m json.tool catalog.json`; browser smoke test.

## Deployment

The existing Hugo configuration already mounts `static/` into the Pages output. `/static/paradiso/index.html` becomes `/paradiso/index.html` without adding any navigation to the church website. The host for `/paradiso/` will be the GitHub Pages URL for this repository; deployment verification must confirm the HTTP response in the actual hosted environment.
