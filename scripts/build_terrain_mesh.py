#!/usr/bin/env python3
"""Jerusalem 3000 terrain ingest.

Reads a provenance-checked Copernicus DEM GeoTIFF cropped to the canonical AOI
and emits a compact browser mesh payload in local ENU metres.

Usage:
  python3 scripts/build_terrain_mesh.py input.tif output.json
"""
import json, math, sys
try:
    import rasterio
except ImportError:
    raise SystemExit("rasterio is required: python3 -m pip install rasterio")

ORIGIN_LAT=31.7780
ORIGIN_LON=35.2350
AOI=(35.195,31.745,35.255,31.805)
R=6378137.0

def enu(lon,lat,h):
    x=math.radians(lon-ORIGIN_LON)*R*math.cos(math.radians(ORIGIN_LAT))
    z=math.radians(lat-ORIGIN_LAT)*R
    return [round(x,3),round(float(h),3),round(z,3)]

def main(src_path,out_path):
    with rasterio.open(src_path) as ds:
        b=ds.bounds
        if b.left>AOI[0] or b.bottom>AOI[1] or b.right<AOI[2] or b.top<AOI[3]:
            raise SystemExit(f"DEM does not cover canonical AOI: {b}")
        window=rasterio.windows.from_bounds(*AOI,transform=ds.transform)
        arr=ds.read(1,window=window,masked=True)
        transform=ds.window_transform(window)
        # Keep canonical mesh light enough for GitHub Pages. Sampling is reversible:
        # authority remains the source raster; this is only a display mesh.
        stride=max(1,math.ceil(max(arr.shape)/160))
        rows=list(range(0,arr.shape[0],stride)); cols=list(range(0,arr.shape[1],stride))
        vertices=[]; valid=[]
        for r in rows:
            for c in cols:
                v=arr[r,c]
                if getattr(v,"mask",False):
                    vertices.append(None); valid.append(False); continue
                lon,lat=rasterio.transform.xy(transform,r,c,offset="center")
                vertices.append(enu(lon,lat,float(v))); valid.append(True)
        w=len(cols); h=len(rows); indices=[]
        for r in range(h-1):
            for c in range(w-1):
                a=r*w+c;b=a+1;d=(r+1)*w+c;e=d+1
                if valid[a] and valid[d] and valid[b]: indices += [a,d,b]
                if valid[b] and valid[d] and valid[e]: indices += [b,d,e]
        payload={"schema":"j3k-terrain-mesh-v1","source":{"path":src_path,"crs":str(ds.crs),"nodata":ds.nodata},
          "origin":{"lat":ORIGIN_LAT,"lon":ORIGIN_LON},"aoi":{"west":AOI[0],"south":AOI[1],"east":AOI[2],"north":AOI[3]},
          "grid":{"width":w,"height":h,"stride":stride},"vertices":vertices,"indices":indices}
    with open(out_path,"w",encoding="utf-8") as f: json.dump(payload,f,separators=(",",":"))
    print(f"wrote {out_path}: {len(vertices)} vertices / {len(indices)//3} triangles")

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: build_terrain_mesh.py input.tif output.json")
    main(sys.argv[1],sys.argv[2])
