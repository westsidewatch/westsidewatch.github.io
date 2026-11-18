# Jerusalem 3000 — Public real DEM ingest

Current runtime (2026-10-28): Copernicus GLO-30 Public,217x217 node-centred grid over the original AOI. The previously recorded CDSE account restriction does not block this publicly accessible AWS tile; no credential or Gateway is needed for this ingest.

Source: https://registry.opendata.aws/copernicus-dem/

Tile: https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/Copernicus_DSM_COG_10_N31_00_E035_00_DEM/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif

Offline reproduction (requires rasterio/numpy):

```sh
python3 scripts/jerusalem3000_ingest_dem30.py /path/to/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif
```

Output: copernicus-glo30-jerusalem.json. The source SHA256 is stored in that file; the output SHA256 is stored in data/terrain-manifest.json and versions the browser cache. Updating the output also requires updating that manifest hash.

The native one-arcsecond sample centres map to scene vertices, including the AOI bounds. Preserve the shared origin and fixed540.13m scene datum. GLO-90 remains a retired comparison asset, not an active fallback. Do not label GLO-90 as30m or synthetic relief as measured terrain.

This is a modern DSM including buildings and vegetation, not an ancient ground reconstruction. Maintain attribution: Copernicus DEM accessed via AWS Open Data; copyright DLR e.V.2010-2014 and Airbus Defence and Space GmbH2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. See the published Copernicus DEM licence linked by the official registry.
