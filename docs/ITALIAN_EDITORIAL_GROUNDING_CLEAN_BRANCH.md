# Italian Editorial Grounding — clean integration

This branch starts from the current `main` head and is the clean integration surface for the historical-image grounded Italian Editorial Atlas work.

Authority order:

1. exact historical magazine image;
2. grounded eight-dimensional visual observation of that exact image;
3. Italian publication / era / lineage as context only;
4. deterministic prompt compilation from grounded observations;
5. generated images as evaluation evidence only.

Hard boundaries:

- manually authored visual fingerprint prose is not runtime prompt authority;
- shared grammar-token lookup must not substitute another evidence image for the image selected by the user;
- concrete architecture, materials, grids, colors, motifs, objects, overlays or secondary imagery may not be invented from lineage priors;
- insufficient visual evidence remains insufficient;
- Doré-local grounded vision is preferred; grounded ChatGPT vision is explicit teacher/fallback only and is not canonical Doré learning;
- final generation regression cannot PASS without real generated artifacts compared against the exact historical evidence authority.

Changes are transplanted selectively against current `main`; old diverged branch history must not be force-merged.
