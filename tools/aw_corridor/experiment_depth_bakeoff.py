#!/usr/bin/env python3
"""V5 geometry-provider bake-off for AW-011."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

def normalize_depth(a):
    a=np.asarray(a,dtype=np.float32); finite=np.isfinite(a)
    if not np.any(finite): raise ValueError('provider returned no finite depth')
    lo,hi=np.quantile(a[finite],[.02,.98]); n=np.clip((a-lo)/max(float(hi-lo),1e-6),0,1)
    return (n*255).astype(np.uint8)

def diagnostics(depth8):
    d=depth8.astype(np.float32)/255.; gx=cv2.Sobel(d,cv2.CV_32F,1,0,ksize=3); gy=cv2.Sobel(d,cv2.CV_32F,0,1,ksize=3); g=np.sqrt(gx*gx+gy*gy)
    q05,q50,q95=[float(x) for x in np.quantile(d,[.05,.5,.95])]
    return {'q05':q05,'q50':q50,'q95':q95,'q95_q05_spread':q95-q05,'standard_deviation':float(d.std()),'edge_gradient_mean':float(g.mean()),'edge_gradient_q95':float(np.quantile(g,.95))}

def depth_anything(source,model):
    from transformers import pipeline
    r=pipeline(task='depth-estimation',model=model,device=-1)(source); x=r.get('predicted_depth',r.get('depth'))
    if isinstance(x,Image.Image): x=np.asarray(x)
    elif hasattr(x,'detach'): x=x.detach().cpu().numpy().squeeze()
    return np.asarray(x)

def depth_pro(source_path):
    import torch, depth_pro
    model,transform=depth_pro.create_model_and_transforms(); model.eval()
    image,_,f_px=depth_pro.load_rgb(str(source_path)); image=transform(image)
    with torch.no_grad(): prediction=model.infer(image,f_px=f_px)
    d=prediction['depth'].detach().cpu().numpy().squeeze().astype(np.float32)
    return 1./np.maximum(d,1e-6)

def moge(source_path):
    import torch
    from moge.model.v2 import MoGeModel
    # Small v2 model is deliberate for CPU CI. Same MoGe-2 geometry family,
    # much lighter than ViT-L; visual winner can later be rerun with ViT-L.
    model=MoGeModel.from_pretrained('Ruicheng/moge-2-vits-normal').to(torch.device('cpu')).eval()
    image=cv2.cvtColor(cv2.imread(str(source_path)),cv2.COLOR_BGR2RGB)
    # Bound CPU cost without changing output aspect ratio; renderer upsamples depth.
    h,w=image.shape[:2]; scale=min(1.0,768.0/max(h,w))
    if scale<1: image=cv2.resize(image,(round(w*scale),round(h*scale)),interpolation=cv2.INTER_AREA)
    image=torch.from_numpy(image.copy()).permute(2,0,1).float()/255.
    with torch.no_grad(): out=model.infer(image,resolution_level=2,use_fp16=False)
    d=out['depth'].detach().cpu().numpy().squeeze().astype(np.float32)
    return 1./np.maximum(d,1e-6)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--provider',choices=['depth-anything','depth-pro','moge'],required=True); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--report',type=Path,required=True); ap.add_argument('--model',default='depth-anything/Depth-Anything-V2-Small-hf'); args=ap.parse_args()
    source=Image.open(args.source).convert('RGB')
    raw=depth_anything(source,args.model) if args.provider=='depth-anything' else depth_pro(args.source) if args.provider=='depth-pro' else moge(args.source)
    raw=cv2.resize(np.asarray(raw,dtype=np.float32),source.size,interpolation=cv2.INTER_CUBIC); depth8=normalize_depth(raw); args.output.parent.mkdir(parents=True,exist_ok=True); cv2.imwrite(str(args.output),depth8)
    report={'status':'DEPTH_PROVIDER_ACCEPTED','provider':args.provider,'source_size':list(source.size),'depth_size':list(source.size),'authority_rule':'source_rgb_unchanged_depth_is_geometry_evidence_only',**diagnostics(depth8)}; args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
