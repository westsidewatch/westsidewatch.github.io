# Jerusalem 3000 — Real DEM ingest

Phase 1 knife 2/7.

Canonical target: Copernicus DEM GLO-30 (`COPERNICUS_30`), Jerusalem AOI already fixed in `data/copernicus-dem-request.json`.

## Current access reality (2026-09-24)

CDSE now restricts COP-DEM-GLO-30 access to users registered for Copernicus Contributing Missions (CCM) data. General-public CCM users retain download rights for GLO-30, but the account must opt into CCM and accept the applicable ESA licence. Requests that omit `demInstance` default to GLO-90; Jerusalem 3000 must therefore keep `COPERNICUS_30` explicit.

Official access paths include Copernicus Browser, OData, S3-compatible storage, and Sentinel Hub Process API. Credentials/tokens are runtime secrets and must never enter this repository.

## Ingest

Once an authorized GLO-30 GeoTIFF covering the canonical AOI exists locally:

```bash
python3 scripts/ingest_jerusalem_dem.py /path/to/jerusalem-glo30.tif
```

The wrapper invokes `scripts/build_terrain_mesh.py`, which validates AOI coverage and generates:

`preview/jerusalem-3000/data/terrain/jerusalem-real.mesh.json`

No substitute GLO-90 payload may be silently labelled GLO-30. No synthetic terrain may be promoted to REAL TERRAIN.

## Attribution gate

Any distributed derivative must retain the applicable Copernicus WorldDEM-30 attribution required by the licence. Attribution metadata will be attached to the generated terrain authority before production publication.
