#!/usr/bin/env python3
"""AW-011 V12: trajectory-reserved 16:9 corridor renderer.

The ideal camera projection is the default. True depth projection is admitted
only where it deviates materially from that ideal projection. Hidden completion
remains persistent/canonical and is used only where foreground support opens.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np

from experiment_depth_traversal import prepare, load_pose_points, smoothstep, project_grid, raster_triangle
from experiment_depth_banded_world_cache import collect_depth_conditioned_support
from experiment_edge_aware_hidden_surface_v4 import camera_lateral_budget, nearest_edge_topology
from experiment_static_cinema_v10 import evaluate_ratio
from experiment_static_cinema_v11 import classify_components
from hidden_surface_provider import learned_three_stage_complete


def corridor_projection(depth, p, ppu, step, threshold):
    xs,ys,xx,yy,z,tx,ty = project_grid(depth,*map(float,p),ppu,step)
    h,w=depth.shape; cx=np.float32((w-1)*.5); cy=np.float32((h-1)*.5)
    cam_x,cam_y,cam_z=map(float,p)
    gain=np.float32(1.0+max(-.35,min(.35,-cam_z*.9)))
    zref=np.float32(np.median(z))
    ix=cx+(xx-cx)*gain+np.float32(cam_x*ppu)*(.35+1.30*zref)
    iy=cy+(yy-cy)*gain+np.float32(cam_y*ppu)*(.45+.90*zref)
    dev=np.hypot(tx-ix,ty-iy)
    active=dev>=float(threshold)
    px=np.where(active,tx,ix).astype(np.float32); py=np.where(active,ty,iy).astype(np.float32)
    return xs,ys,xx,yy,z,px,py,dev,active


def raster_layer_corridor(texture, depth, p, ppu, step, threshold, edge_threshold=None):
    h,w=depth.shape
    xs,ys,xx,yy,z,px,py,dev,active = corridor_projection(depth,p,ppu,step,threshold)
    out=np.zeros_like(texture); known=np.zeros((h,w),np.uint8); zbuf=np.full((h,w),-np.inf,np.float32)
    rows,cols=z.shape
    for r in range(rows-1):
        for c in range(cols-1):
            ids=[(r,c),(r,c+1),(r+1,c+1),(r+1,c)]
            for tri in ((0,1,2),(0,2,3)):
                q=[ids[k] for k in tri]; zv=np.array([z[a,b] for a,b in q],np.float32)
                if edge_threshold is not None and float(zv.max()-zv.min())>edge_threshold: continue
                sxy=np.array([[xx[a,b],yy[a,b]] for a,b in q],np.float32)
                dxy=np.array([[px[a,b],py[a,b]] for a,b in q],np.float32)
                raster_triangle(texture,zbuf,out,known,sxy,dxy,zv)
    return out,known,float(np.count_nonzero(active)/active.size),float(dev.max(initial=0.0))


def render(src,dep,irgb,idep,imask,p,ppu,step,threshold):
    h,w=dep.shape
    frame=np.zeros_like(src); occupied=np.zeros((h,w),np.uint8)
    iimg,iknown,iact,imax=raster_layer_corridor(irgb,idep,p,ppu,step,threshold,None)
    probe=cv2.cvtColor(imask,cv2.COLOR_GRAY2BGR)
    mimg,mknown,_,_=raster_layer_corridor(probe,idep,p,ppu,step,threshold,None)
    ivis=(mknown>0)&(mimg[:,:,0]>96); itake=(iknown>0)&ivis
    frame[itake]=iimg[itake]; occupied[itake]=255
    front,fknown,fact,fmax=raster_layer_corridor(src,dep,p,ppu,step,threshold,.10)
    frame[fknown>0]=front[fknown>0]
    residual=(fknown==0)&(occupied==0)
    return frame,residual,fact,max(fmax,imax),int(np.count_nonzero(itake))


def main():
    ap=argparse.ArgumentParser()
    for k in ('source','depth','spine','output','report'): ap.add_argument('--'+k,type=Path,required=True)
    ap.add_argument('--networks',type=Path,required=True); ap.add_argument('--edge-checkpoint',type=Path,required=True); ap.add_argument('--depth-checkpoint',type=Path,required=True); ap.add_argument('--color-checkpoint',type=Path,required=True)
    ap.add_argument('--device',default='cpu'); ap.add_argument('--width',type=int,default=480); ap.add_argument('--output-width',type=int,default=640); ap.add_argument('--fps',type=int,default=12); ap.add_argument('--segment-frames',type=int,default=4); ap.add_argument('--ppu',type=float,default=520.0); ap.add_argument('--samples',type=int,default=4); ap.add_argument('--behind',type=float,default=.08); ap.add_argument('--edge-q',type=float,default=.90); ap.add_argument('--min-jump',type=float,default=.055); ap.add_argument('--target-residual',type=float,default=.001); ap.add_argument('--min-view-scale',type=float,default=.45); ap.add_argument('--raster-step',type=int,default=3); ap.add_argument('--deviation-threshold',type=float,default=1.25)
    a=ap.parse_args()
    src,dep=prepare(a.source,a.depth,a.width); poses=load_pose_points(a.spine)
    shift,radius=camera_lateral_budget(poses,a.ppu)
    support,zmap,used,mapped,inv_err=collect_depth_conditioned_support(dep,poses,a.ppu,a.samples,a.behind)
    topo=nearest_edge_topology(dep,support,a.edge_q,.025,a.min_jump,radius)
    internal=learned_three_stage_complete(src,dep,support,zmap,topo,a.networks,a.edge_checkpoint,a.depth_checkpoint,a.color_checkpoint,a.device)
    frames=[]; masks=[]; active=[]; maxdev=[]; sampled=[]; hidden_pixels=0
    for i in range(len(poses)-1):
        p0=np.asarray(poses[i]['position'],np.float32); p1=np.asarray(poses[i+1]['position'],np.float32)
        for j in range(a.segment_frames):
            t=smoothstep(j/float(a.segment_frames)); p=p0*(1-t)+p1*t
            if np.linalg.norm(p)<1e-6: frame=src.copy(); residual=np.zeros(dep.shape,np.bool_); af=0.0; md=0.0; hp=0
            else: frame,residual,af,md,hp=render(src,dep,internal.rgb,internal.depth,internal.mask,p,a.ppu,a.raster_step,a.deviation_threshold)
            frames.append(frame); masks.append(residual); active.append(af); maxdev.append(md); sampled.append([float(x) for x in p]); hidden_pixels+=hp
    h,w=dep.shape; chosen=evaluate_ratio(masks,h,w,16/9,a.target_residual,a.min_view_scale); x0,y0,cw,ch=chosen['rect']
    crops=[m[y0:y0+ch,x0:x0+cw] for m in masks]; residuals=[float(np.count_nonzero(m)/m.size) for m in crops]
    wi=int(np.argmax(residuals)) if residuals else -1; wm=crops[wi] if wi>=0 else np.zeros((ch,cw),np.bool_); comps=classify_components(wm)
    out_w=a.output_width-(a.output_width%2); out_h=int(round(out_w*9/16)); out_h-=out_h%2
    a.output.parent.mkdir(parents=True,exist_ok=True); wr=cv2.VideoWriter(str(a.output),cv2.VideoWriter_fourcc(*'mp4v'),a.fps,(out_w,out_h))
    if not wr.isOpened(): raise RuntimeError('video writer failed')
    for fr in frames: wr.write(cv2.resize(fr[y0:y0+ch,x0:x0+cw],(out_w,out_h),interpolation=cv2.INTER_CUBIC))
    wr.write(cv2.resize(src[y0:y0+ch,x0:x0+cw],(out_w,out_h),interpolation=cv2.INTER_CUBIC)); wr.release()
    structural=sum(c['area'] for c in comps if c['kind']=='structural_disocclusion'); micro=sum(c['area'] for c in comps if c['kind']=='micro_raster_candidate')
    rep={'status':'STATIC_CINEMA_V12_TRAJECTORY_RESERVED_READY_FOR_VISUAL_REVIEW','mode':'nested_16_9_ideal_projection_plus_local_depth_deviation','authoritative_renderer_change':True,'canonical_world':'original_dore_artwork','external_world_generation':False,'deviation_threshold_px':a.deviation_threshold,'mean_active_3d_vertex_fraction':float(np.mean(active)) if active else 0.0,'max_active_3d_vertex_fraction':max(active,default=0.0),'max_true_3d_deviation_px':max(maxdev,default=0.0),'max_final_viewfinder_residual_fraction':max(residuals,default=0.0),'mean_final_viewfinder_residual_fraction':float(np.mean(residuals)) if residuals else 0.0,'worst_frame_index':wi,'worst_frame_pose':sampled[wi] if wi>=0 else None,'worst_frame_structural_disocclusion_pixels':structural,'worst_frame_micro_raster_candidate_pixels':micro,'persistent_hidden_pixels_rendered_total':hidden_pixels,'source_relock':True,'per_frame_synthesis':False,'principle':'2D same-ratio camera projection is default; true 3D is admitted only where depth deviation crosses threshold; completion remains persistent and local'}
    a.report.parent.mkdir(parents=True,exist_ok=True); a.report.write_text(json.dumps(rep,indent=2)+'\n',encoding='utf-8'); print(json.dumps(rep,indent=2))
if __name__=='__main__': raise SystemExit(main())
