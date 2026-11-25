#!/usr/bin/env python3
"""Reproducible public GLO-30 ingest; same AOI/origin/fixed scene datum.
Usage: python scripts/jerusalem3000_ingest_dem30.py /path/to/source.tif
Requires rasterio and numpy for offline ingestion only. Runtime uses local JSON.
"""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin
ROOT=Path(__file__).resolve().parents[1]
URL='https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/Copernicus_DSM_COG_10_N31_00_E035_00_DEM/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif'

def ingest(source, output):
    aoi=dict(west=35.195,south=31.745,east=35.255,north=31.805)
    # 1 arc-second latitude / longitude nodes: no upsampling of source information.
    width=height=217
    dx=(aoi['east']-aoi['west'])/(width-1);dy=(aoi['north']-aoi['south'])/(height-1)
    # Pixel CENTRES, not edges, coincide with scene mesh vertices at AOI bounds.
    transform=from_origin(aoi['west']-dx/2,aoi['north']+dy/2,dx,dy)
    arr=np.full((height,width),np.nan,dtype='float32')
    with rasterio.open(source) as src:
        if str(src.crs)!='EPSG:4326' or src.width!=3600 or src.height!=3600:
            raise ValueError('Expected full published one-arcsecond GLO-30 tile')
        if src.bounds.left>aoi['west'] or src.bounds.right<aoi['east'] or src.bounds.top<aoi['north'] or src.bounds.bottom>aoi['south']:
            raise ValueError('Source does not cover canonical AOI')
        reproject(source=rasterio.band(src,1),destination=arr,src_transform=src.transform,src_crs=src.crs,dst_transform=transform,dst_crs='EPSG:4326',resampling=Resampling.bilinear,dst_nodata=np.nan)
    if not np.isfinite(arr).all():raise ValueError('Missing source elevations')
    values=[round(float(v),2) for v in arr.ravel()]
    data=dict(schema='j3k-elevation-grid-v1',id='jerusalem-copernicus-glo30-2021',source='Copernicus DEM GLO-30 Public / AWS Open Data',sourceUrl=URL,sourceRelease='Copernicus DEM 2021',sourceSha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),license='Copernicus DEM GLO-30 Public, free under Copernicus DEM licence',attribution='Copernicus DEM accessed via AWS Open Data; (c) DLR e.V. 2010-2014 and (c) Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved',bounds=aoi,origin=dict(lat=31.778,lon=35.235),width=width,height=height,nominalResolutionMetres=30,sampleConvention='node-centres-at-bounds-not-cell-edges',verticalDatum='source Copernicus DEM orthometric heights',verticalDatumOffsetMetres=540.13,sceneDatumPolicy='fixed legacy datum retained; not AOI minimum',minElevationMetres=min(values),maxElevationMetres=max(values),values=values)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print(json.dumps({ 'output':str(output),'grid':[width,height],'range':[min(values),max(values)],'sourceSha256':data['sourceSha256'],'bytes':output.stat().st_size}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--out',type=Path,default=ROOT/'preview/jerusalem-3000/data/terrain/copernicus-glo30-jerusalem.json');a=p.parse_args();ingest(a.source,a.out)
