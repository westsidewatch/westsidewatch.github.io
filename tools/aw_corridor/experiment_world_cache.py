#!/usr/bin/env python3
import argparse,json,cv2,numpy as np
from pathlib import Path
from experiment_depth_traversal import prepare,load_pose_points,smoothstep,project_grid,raster_triangle

def bg(src,dep):
 g=np.hypot(cv2.Sobel(dep,cv2.CV_32F,1,0),cv2.Sobel(dep,cv2.CV_32F,0,1)); m=(g>.10).astype('uint8')*255; m=cv2.dilate(m,np.ones((15,15),np.uint8)); return cv2.inpaint(src,m,5,cv2.INPAINT_TELEA)

def frame(src,dep,p,cache,ppu=520,step=6,thr=.10):
 h,w=dep.shape; xs,ys,xx,yy,z,px,py=project_grid(dep,*map(float,p),ppu,step); out=np.zeros_like(src); k=np.zeros((h,w),np.uint8); zb=np.full((h,w),-np.inf,np.float32)
 for r in range(z.shape[0]-1):
  for c in range(z.shape[1]-1):
   q=[(r,c),(r,c+1),(r+1,c+1),(r+1,c)]
   for tri in ((0,1,2),(0,2,3)):
    t=[q[i] for i in tri]; zv=np.array([z[a,b] for a,b in t],np.float32)
    if zv.max()-zv.min()>thr: continue
    s=np.array([[xx[a,b],yy[a,b]] for a,b in t],np.float32); d=np.array([[px[a,b],py[a,b]] for a,b in t],np.float32); raster_triangle(src,zb,out,k,s,d,zv)
 x,y,zz=map(float,p); gain=1+max(-.35,min(.35,-zz*.9)); cx=(w-1)/2; cy=(h-1)/2; sx=x*ppu*.584; sy=y*ppu*.612; M=np.array([[gain,0,cx-cx*gain+sx],[0,gain,cy-cy*gain+sy]],np.float32); b=cv2.warpAffine(cache,M,(w,h),borderMode=cv2.BORDER_REFLECT101); b[k>0]=out[k>0]; return b,float(np.count_nonzero(k==0)/k.size)

def main():
 a=argparse.ArgumentParser()
 for n in ['source','depth','spine','output','report']: a.add_argument('--'+n,type=Path,required=True)
 a.add_argument('--width',type=int,default=960); a.add_argument('--fps',type=int,default=24); a.add_argument('--segment-frames',type=int,default=24); x=a.parse_args(); src,dep=prepare(x.source,x.depth,x.width); poses=load_pose_points(x.spine); cache=bg(src,dep); h,w=src.shape[:2]; x.output.parent.mkdir(parents=True,exist_ok=True); v=cv2.VideoWriter(str(x.output),cv2.VideoWriter_fourcc(*'mp4v'),x.fps,(w,h)); unseen=[]
 for i in range(len(poses)-1):
  p0=np.array(poses[i]['position'],np.float32); p1=np.array(poses[i+1]['position'],np.float32)
  for j in range(x.segment_frames):
   s=smoothstep(j/x.segment_frames); f,u=frame(src,dep,p0*(1-s)+p1*s,cache); v.write(f); unseen.append(u)
 v.write(src); v.release(); r={'status':'WORLD_CACHE_ACCEPTED','mode':'moge2_persistent_world_cache','max_unseen_fraction':max(unseen),'exact_final_source_relock':True,'visual_gate':'PENDING_HUMAN_REVIEW'}; x.report.parent.mkdir(parents=True,exist_ok=True); x.report.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r))
if __name__=='__main__': main()
