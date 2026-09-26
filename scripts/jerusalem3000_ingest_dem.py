#!/usr/bin/env python3
import json, math, os, urllib.request
from pathlib import Path
import rasterio
from rasterio.windows import from_bounds
from rasterio.enums import Resampling

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview/jerusalem-3000/data/terrain/copernicus-glo90-jerusalem.json'
AOI=dict(west=35.195,south=31.745,east=35.255,north=31.805)
ORIGIN=dict(lat=31.778,lon=35.235)
TILE='Copernicus_DSM_COG_30_N31_00_E035_00_DEM'
URL=f'https://copernicus-dem-90m.s3.eu-central-1.amazonaws.com/{TILE}/{TILE}.tif'
TMP='/tmp/j3k-copernicus-glo90.tif'
urllib.request.urlretrieve(URL,TMP)
with rasterio.open(TMP) as src:
    window=from_bounds(AOI['west'],AOI['south'],AOI['east'],AOI['north'],src.transform)
    # Preserve the native ~90 m information; 76x76 is sufficient for the 6.7 x 5.7 km AOI.
    width=76;height=76
    arr=src.read(1,window=window,out_shape=(height,width),resampling=Resampling.bilinear).astype('float64')
    nodata=src.nodata
    if nodata is not None and (arr==nodata).any(): raise SystemExit('DEM AOI contains nodata')
values=[round(float(v),2) for row in arr for v in row]
OUT.parent.mkdir(parents=True,exist_ok=True)
payload={
 'schema':'j3k-elevation-grid-v1','id':'jerusalem-copernicus-glo90-2021','source':'Copernicus DEM GLO-90 / AWS Open Data','sourceUrl':URL,'sourceRelease':'Copernicus DEM 2021','license':'COP-DEM-GLO-90-F Global 90m Full, Free & Open','attribution':'Copernicus DEM accessed via AWS Open Data; © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved','bounds':AOI,'origin':ORIGIN,'width':width,'height':height,'verticalDatum':'source Copernicus DEM orthometric heights','verticalDatumOffsetMetres':min(values),'minElevationMetres':min(values),'maxElevationMetres':max(values),'values':values
}
OUT.write_text(json.dumps(payload,separators=(',',':'))+'\n')
print(f'wrote {OUT}: {width}x{height}, elevation {min(values)}..{max(values)} m')
