#!/usr/bin/env python3
"""Local-only Doré image studio. No paid API, no external upload."""
import base64,json,secrets,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
HOST="127.0.0.1";PORT=4313;MODEL="http://127.0.0.1:8790"
TOKEN=secrets.token_urlsafe(24);LOCK=threading.Lock()
PAGE=r'''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Doré Image Studio</title>
<style>*{box-sizing:border-box}body{margin:0;background:#f5f1e8;color:#252525;font:16px system-ui}main{max-width:1180px;margin:auto;padding:5vw}header{border-bottom:1px solid #c6bfae;margin-bottom:30px}h1{font:normal clamp(48px,7vw,90px) Georgia;margin:8px 0}small{letter-spacing:.2em;color:#174b35}.layout{display:grid;grid-template-columns:minmax(280px,420px) 1fr;gap:40px}label{display:block;margin:20px 0 8px;font-size:13px}textarea,select{width:100%;border:1px solid #c6bfae;background:transparent;padding:14px;font:inherit}textarea{min-height:180px}.drop{border:1px dashed #718275;padding:28px;text-align:center;cursor:pointer}.drop.drag{background:#e1e9df}.preview{background:#e8e3d8;min-height:460px;display:grid;place-items:center}.preview img{max-width:100%;max-height:75vh}button{width:100%;background:#174b35;color:white;border:0;padding:17px;margin-top:22px;cursor:pointer;font:inherit}button:disabled{opacity:.5}#status{font-size:13px;white-space:pre-wrap}a{color:#174b35}@media(max-width:750px){.layout{grid-template-columns:1fr}.preview{min-height:320px}}</style>
<main><header><small>DORÉ / LOCAL IMAGE ENGINE</small><h1>Image Studio</h1><p>本地生成 · 貼上照片 · 拖放照片 · 選取照片</p></header><div class="layout"><form id="form"><label>生成模式</label><select id="mode"><option value="image_to_image">參考照片</option><option value="text_to_image">文字生成</option></select><label>畫面描述</label><textarea id="prompt" required placeholder="人物版畫、精細刻線、深橄欖綠、雜誌式構圖……"></textarea><label>參考照片</label><div class="drop" id="drop" tabindex="0" role="button">點擊選擇、拖放，或按 ⌘V / Ctrl+V 貼上圖片<input id="file" type="file" accept="image/png,image/jpeg,image/webp" hidden></div><p id="chosen"></p><button id="go">開始生成</button><p id="status" role="status">等待輸入</p></form><section><div class="preview"><span id="empty">IMAGE PREVIEW</span><img id="result" alt="生成預覽" hidden></div><p><a id="download" download="dore-image.png" hidden>儲存 PNG</a></p></section></div></main>
<script>
const token=__TOKEN__,file=document.querySelector('#file'),drop=document.querySelector('#drop'),chosen=document.querySelector('#chosen'),form=document.querySelector('#form'),mode=document.querySelector('#mode'),status=document.querySelector('#status'),go=document.querySelector('#go'),img=document.querySelector('#result'),download=document.querySelector('#download');let selected=null;
function setPhoto(f){if(!f)return;if(!['image/png','image/jpeg','image/webp'].includes(f.type)||f.size>12*1024*1024){status.textContent='圖片須為 PNG/JPEG/WebP，且小於 12MB';return}selected=f;chosen.textContent=f.name||'已貼上圖片';mode.value='image_to_image';const r=new FileReader();r.onload=()=>{img.src=r.result;img.hidden=false;document.querySelector('#empty').hidden=true};r.readAsDataURL(f)}
drop.onclick=()=>file.click();drop.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();file.click()}};file.onchange=()=>setPhoto(file.files[0]);
drop.ondragover=e=>{e.preventDefault();drop.classList.add('drag')};drop.ondragleave=()=>drop.classList.remove('drag');drop.ondrop=e=>{e.preventDefault();drop.classList.remove('drag');setPhoto(e.dataTransfer.files[0])};
document.addEventListener('paste',e=>{if(e.target.tagName==='TEXTAREA'||e.target.tagName==='INPUT')return;for(const item of e.clipboardData?.items||[]){if(item.type.startsWith('image/')){e.preventDefault();setPhoto(item.getAsFile());break}}});
form.onsubmit=async e=>{e.preventDefault();go.disabled=true;status.textContent='正在生成…';download.hidden=true;try{if(mode.value==='image_to_image'&&!selected)throw Error('請先選擇或貼上照片');const payload={mode:mode.value,message:'Generate image: '+document.querySelector('#prompt').value};if(mode.value==='image_to_image'){const encoded=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result.split(',')[1]);r.onerror=reject;r.readAsDataURL(selected)});payload.reference_image={mime_type:selected.type,data_base64:encoded}}const res=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json','X-Dore-Token':token},body:JSON.stringify(payload)});const data=await res.json();if(!res.ok)throw Error(data.error);img.src='data:image/png;base64,'+data.image_base64;img.hidden=false;download.href=img.src;download.hidden=false;status.textContent='生成完成（未發布）'}catch(err){status.textContent='生成失敗：'+err.message}finally{go.disabled=false}};
</script></html>'''
class Handler(BaseHTTPRequestHandler):
 def send(self,code,data,kind="application/json"):
  raw=data.encode() if isinstance(data,str) else data
  self.send_response(code);self.send_header("Content-Type",kind);self.send_header("Cache-Control","no-store");self.send_header("X-Content-Type-Options","nosniff");self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
 def reply(self,code,data):self.send(code,json.dumps(data,ensure_ascii=False))
 def do_GET(self):
  if self.path in ("/","/**"):return self.send(200,PAGE.replace("__TOKEN__",json.dumps(TOKEN)),"text/html; charset=utf-8")
  if self.path=="/favicon.ico":return self.send(204,b"","image/x-icon")
  if self.path=="/health":return self.reply(200,{"ok":True,"service":"dore-image-studio"})
  self.reply(404,{"error":"Not found"})
 def do_POST(self):
  if self.path!="/api/generate":return self.reply(404,{"error":"Not found"})
  if self.headers.get("X-Dore-Token")!=TOKEN:return self.reply(403,{"error":"Invalid session"})
  if self.headers.get("Origin") not in (None,f"http://{HOST}:{PORT}"):return self.reply(403,{"error":"Invalid origin"})
  try:length=int(self.headers.get("Content-Length","0"))
  except ValueError:return self.reply(400,{"error":"Invalid length"})
  if length<1 or length>17*1024*1024:return self.reply(413,{"error":"Request too large"})
  if not LOCK.acquire(False):return self.reply(409,{"error":"Model busy"})
  try:
   payload=json.loads(self.rfile.read(length))
   if payload.get("mode") not in ("text_to_image","image_to_image") or not isinstance(payload.get("message"),str) or not 1<=len(payload["message"])<=12000:raise ValueError("Invalid prompt")
   with urlopen(MODEL+"/health",timeout=15) as r:health=json.load(r)
   if health.get("model_backed") is not True:raise ValueError("Local model unavailable")
   if payload["mode"]=="image_to_image":
    if health.get("capabilities",{}).get("reference_image") is not True:raise ValueError("Local model has no reference-image capability")
    photo=payload.get("reference_image",{})
    if photo.get("mime_type") not in ("image/png","image/jpeg","image/webp"):raise ValueError("Invalid photo type")
    raw=base64.b64decode(photo.get("data_base64",""),validate=True)
    if not raw or len(raw)>12*1024*1024:raise ValueError("Invalid photo size")
    signatures={"image/png":raw.startswith(b"\x89PNG\r\n\x1a\n"),"image/jpeg":raw.startswith(b"\xff\xd8\xff"),"image/webp":raw.startswith(b"RIFF") and raw[8:12]==b"WEBP"}
    if not signatures[photo["mime_type"]]:raise ValueError("Invalid photo bytes")
   else:
    payload.pop("reference_image",None)
    payload.pop("mode",None)
   req=Request(MODEL+"/generate",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json","X-Dore-Origin":"dore-search"})
   with urlopen(req,timeout=1500) as r:result=json.load(r)
   if result.get("ok") is not True or result.get("model_backed") is not True:raise ValueError("Model did not generate an image")
   if payload["mode"]=="image_to_image" and result.get("reference_conditioned") is not True:raise ValueError("Model did not confirm photo conditioning")
   asset=urlparse(result.get("asset_url",""))
   if asset.scheme!="http" or asset.hostname!="127.0.0.1" or asset.port!=8790 or asset.path!="/asset":raise ValueError("Invalid asset URL")
   with urlopen(asset.geturl(),timeout=40) as r:png=r.read(32*1024*1024+1)
   if len(png)>32*1024*1024 or not png.startswith(b"\x89PNG\r\n\x1a\n"):raise ValueError("Invalid PNG")
   self.reply(200,{"ok":True,"image_base64":base64.b64encode(png).decode(),"published":False})
  except HTTPError as exc:
   detail=exc.read(8192).decode("utf-8","replace")
   try:
    parsed=json.loads(detail)
    detail=parsed.get("error") or parsed.get("message") or detail
   except ValueError:pass
   self.reply(422,{"error":f"Local model HTTP {exc.code}: {str(detail)[:1200]}"})
  except Exception as exc:self.reply(422,{"error":str(exc)})
  finally:LOCK.release()
if __name__=="__main__":
 print(f"Doré Image Studio: http://{HOST}:{PORT}/",flush=True)
 ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
