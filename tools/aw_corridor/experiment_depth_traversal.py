#!/usr/bin/env python3
"""AW-011 V4: discontinuity-aware depth-grid mesh traversal.

Canonical Doré RGB is texture authority. A regular depth grid becomes connected
triangles only where local depth is continuous. Travel poses project that mesh;
triangles are rasterized as opaque textured surfaces with a z-buffer. Pixels not
covered by geometry are the only unseen pixels eligible for temporary fill.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np


def smoothstep(t): return t*t*(3.0-2.0*t)

def load_pose_points(path):
    poses=json.loads(path.read_text(encoding="utf-8")).get("poses")
    if not isinstance(poses,list) or len(poses)<4: raise ValueError("Camera Spine needs canonical, travel, and return poses")
    return poses

def prepare(source_path,depth_path,width):
    src=cv2.imread(str(source_path),cv2.IMREAD_COLOR); dep=cv2.imread(str(depth_path),cv2.IMREAD_GRAYSCALE)
    if src is None or dep is None: raise ValueError("cannot read source/depth")
    if width>0 and src.shape[1]!=width:
        h=int(round(src.shape[0]*width/src.shape[1])); src=cv2.resize(src,(width,h),interpolation=cv2.INTER_AREA); dep=cv2.resize(dep,(width,h),interpolation=cv2.INTER_CUBIC)
    elif dep.shape[:2]!=src.shape[:2]: dep=cv2.resize(dep,(src.shape[1],src.shape[0]),interpolation=cv2.INTER_CUBIC)
    d=dep.astype(np.float32)/255.0; lo,hi=np.quantile(d,[.05,.95]); d=np.clip((d-lo)/max(1e-6,hi-lo),0,1).astype(np.float32)
    return src,d

def project_grid(depth,cam_x,cam_y,cam_z,ppu,step):
    h,w=depth.shape
    xs=np.arange(0,w,step,dtype=np.int32); ys=np.arange(0,h,step,dtype=np.int32)
    if xs[-1]!=w-1: xs=np.r_[xs,w-1]
    if ys[-1]!=h-1: ys=np.r_[ys,h-1]
    xx,yy=np.meshgrid(xs.astype(np.float32),ys.astype(np.float32)); z=depth[np.ix_(ys,xs)]
    gain=np.float32(1.0+max(-.35,min(.35,-cam_z*.9))); cx=np.float32((w-1)*.5); cy=np.float32((h-1)*.5)
    sx=np.float32(cam_x*ppu)*(.35+1.30*z); sy=np.float32(cam_y*ppu)*(.45+.90*z)
    px=cx+(xx-cx)*gain+sx; py=cy+(yy-cy)*gain+sy
    return xs,ys,xx,yy,z,px.astype(np.float32),py.astype(np.float32)

def raster_triangle(src,zbuf,out,known,src_xy,dst_xy,zv):
    h,w=zbuf.shape
    minx=max(0,int(np.floor(dst_xy[:,0].min()))); maxx=min(w-1,int(np.ceil(dst_xy[:,0].max())))
    miny=max(0,int(np.floor(dst_xy[:,1].min()))); maxy=min(h-1,int(np.ceil(dst_xy[:,1].max())))
    if minx>maxx or miny>maxy: return 0
    x0,y0=dst_xy[0]; x1,y1=dst_xy[1]; x2,y2=dst_xy[2]
    den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
    if abs(float(den))<1e-5: return 0
    gx,gy=np.meshgrid(np.arange(minx,maxx+1,dtype=np.float32)+.5,np.arange(miny,maxy+1,dtype=np.float32)+.5)
    a=((y1-y2)*(gx-x2)+(x2-x1)*(gy-y2))/den; b=((y2-y0)*(gx-x2)+(x0-x2)*(gy-y2))/den; c=1-a-b
    inside=(a>=-1e-4)&(b>=-1e-4)&(c>=-1e-4)
    if not np.any(inside): return 0
    zz=a*zv[0]+b*zv[1]+c*zv[2]
    zb=zbuf[miny:maxy+1,minx:maxx+1]; take=inside&(zz>=zb)
    if not np.any(take): return 0
    su=a*src_xy[0,0]+b*src_xy[1,0]+c*src_xy[2,0]; sv=a*src_xy[0,1]+b*src_xy[1,1]+c*src_xy[2,1]
    ui=np.clip(np.rint(su).astype(np.int32),0,w-1); vi=np.clip(np.rint(sv).astype(np.int32),0,h-1)
    patch=out[miny:maxy+1,minx:maxx+1]; kp=known[miny:maxy+1,minx:maxx+1]
    patch[take]=src[vi[take],ui[take]]; zb[take]=zz[take]; kp[take]=255
    return int(np.count_nonzero(take))

def render_mesh(source,depth,cam_x,cam_y,cam_z,ppu,step,edge_threshold):
    h,w=depth.shape; xs,ys,xx,yy,z,px,py=project_grid(depth,cam_x,cam_y,cam_z,ppu,step)
    out=np.zeros_like(source); known=np.zeros((h,w),np.uint8); zbuf=np.full((h,w),-np.inf,np.float32)
    faces=0; cut=0; writes=0
    rows,cols=z.shape
    for r in range(rows-1):
      for c in range(cols-1):
        ids=[(r,c),(r,c+1),(r+1,c+1),(r+1,c)]
        for tri in ((0,1,2),(0,2,3)):
          q=[ids[k] for k in tri]; zv=np.array([z[a,b] for a,b in q],np.float32)
          if float(zv.max()-zv.min())>edge_threshold: cut+=1; continue
          sxy=np.array([[xx[a,b],yy[a,b]] for a,b in q],np.float32); dxy=np.array([[px[a,b],py[a,b]] for a,b in q],np.float32)
          writes+=raster_triangle(source,zbuf,out,known,sxy,dxy,zv); faces+=1
    unseen=cv2.bitwise_not(known); uf=float(np.count_nonzero(unseen)/unseen.size)
    if np.any(unseen):
        fill=cv2.inpaint(out,unseen,2.0,cv2.INPAINT_TELEA); out[unseen>0]=fill[unseen>0]
    disp=px-xx
    q1,q2=np.quantile(z,[1/3,2/3]); bands=[z<=q1,(z>q1)&(z<=q2),z>q2]; bs=[float(np.mean(np.abs(disp[m]))) for m in bands]
    return out,{"camera":[float(cam_x),float(cam_y),float(cam_z)],"known_fraction":float(np.count_nonzero(known)/known.size),"unseen_fraction":uf,"mesh_faces":faces,"depth_discontinuity_faces_cut":cut,"raster_writes":writes,"depth_band_mean_abs_x_shift_px":bs,"depth_band_shift_span_px":float(max(bs)-min(bs)),"depth_band_shift_variance":float(np.var(bs)),"projected_x_displacement_std_px":float(np.std(px-xx)),"projected_y_displacement_std_px":float(np.std(py-yy))}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",type=Path,required=True); ap.add_argument("--depth",type=Path,required=True); ap.add_argument("--spine",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); ap.add_argument("--report",type=Path,required=True); ap.add_argument("--width",type=int,default=960); ap.add_argument("--fps",type=int,default=24); ap.add_argument("--segment-frames",type=int,default=24); ap.add_argument("--pixels-per-unit",type=float,default=520.0); ap.add_argument("--mesh-step",type=int,default=6); ap.add_argument("--depth-edge-threshold",type=float,default=.10); args=ap.parse_args()
    source,depth=prepare(args.source,args.depth,args.width); poses=load_pose_points(args.spine); h,w=source.shape[:2]; args.output.parent.mkdir(parents=True,exist_ok=True)
    writer=cv2.VideoWriter(str(args.output),cv2.VideoWriter_fourcc(*"mp4v"),args.fps,(w,h));
    if not writer.isOpened(): raise RuntimeError("video writer failed")
    metrics=[]; fc=0
    for si in range(len(poses)-1):
      pa=np.asarray(poses[si]["position"],np.float32); pb=np.asarray(poses[si+1]["position"],np.float32)
      for j in range(args.segment_frames):
        s=smoothstep(j/float(args.segment_frames)); p=pa*(1-s)+pb*s
        frame,m=render_mesh(source,depth,float(p[0]),float(p[1]),float(p[2]),args.pixels_per_unit,args.mesh_step,args.depth_edge_threshold); writer.write(frame); m.update(segment=si,frame=fc); metrics.append(m); fc+=1
    writer.write(source); writer.release(); fc+=1
    travel=[m for m in metrics if sum(abs(v) for v in m["camera"])>1e-6]
    span=max((m["depth_band_shift_span_px"] for m in travel),default=0); var=max((m["depth_band_shift_variance"] for m in travel),default=0); unseen=max((m["unseen_fraction"] for m in travel),default=0); std=max((m["projected_x_displacement_std_px"] for m in travel),default=0); cuts=max((m["depth_discontinuity_faces_cut"] for m in travel),default=0)
    passed=span>=3 and var>=1 and std>=2 and unseen>.001 and cuts>0
    report={"status":"GEOMETRIC_TRAVERSAL_ACCEPTED" if passed else "GEOMETRIC_TRAVERSAL_TOO_PLANAR","mode":"depth_aware_camera_corridor_v4_discontinuity_mesh","source_authority":"canonical_dore_011_rgb_texture","visibility_model":"depth_grid_triangle_mesh_zbuffer_depth_discontinuity_cut","depth_role":"geometry_evidence_only","unseen_fill_role":"true_uncovered_geometry_only","mesh_step_px":args.mesh_step,"depth_edge_threshold":args.depth_edge_threshold,"resolution":[w,h],"fps":args.fps,"frame_count":fc,"duration_seconds":fc/args.fps,"max_depth_band_shift_span_px":span,"max_depth_band_shift_variance":var,"max_map_x_displacement_std_px":std,"max_unseen_fraction":unseen,"max_depth_discontinuity_faces_cut":cuts,"exact_final_source_relock":True,"quantitative_gate":passed,"visual_gate":"PENDING_HUMAN_REVIEW","gate":passed,"samples":metrics[::max(1,len(metrics)//12)]}
    args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0 if passed else 2
if __name__=="__main__": raise SystemExit(main())
