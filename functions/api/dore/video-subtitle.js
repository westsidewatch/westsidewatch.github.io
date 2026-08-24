const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','access-control-allow-origin':'*'}});
const supported=url=>{try{const u=new URL(url);return /^https?:$/.test(u.protocol)&&/(youtube\.com|youtu\.be|vimeo\.com|facebook\.com|fb\.watch|instagram\.com|westsidewatch\.ca)$/i.test(u.hostname.replace(/^www\./,''))}catch{return false}};
export async function onRequestPost({request,env}){
 let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
 const url=String(body?.url||'').trim();if(!supported(url))return json({ok:false,error:'supported_video_url_required'},400);
 const job={schema:'dore.video-subtitle.v1',url,created_at:new Date().toISOString(),intent:'video_to_corrected_subtitle',pipeline:['identify-video','obtain-caption-or-audio','transcribe-if-needed','dore-proofread','human-review','learning-feedback']};
 // Doré is taught the intent now, but Cloudflare Pages has no local Whisper/ffmpeg
 // executor. Persist the job when D1 is available; never fabricate subtitles.
 let recorded=false;
 if(env?.DORE_SENSORY){try{await env.DORE_SENSORY.prepare(`CREATE TABLE IF NOT EXISTS dore_video_subtitle_jobs (id INTEGER PRIMARY KEY AUTOINCREMENT,url TEXT NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL,payload_json TEXT NOT NULL)`).run();await env.DORE_SENSORY.prepare(`INSERT INTO dore_video_subtitle_jobs(url,status,created_at,payload_json) VALUES(?1,'awaiting-transcription-executor',?2,?3)`).bind(url,job.created_at,JSON.stringify(job)).run();recorded=true}catch(e){console.error('video subtitle job registry',e)}}
 return json({ok:true,status:'awaiting-transcription-executor',recorded,job,message:'我已認出影片字幕任務並建立工作記錄。下一步需要接入可取得字幕／音訊並執行 Whisper 的 worker，之後才會交給 Doré 校對。',boundary:'目前沒有在 Cloudflare 假裝執行本機 Whisper；在真正取得字幕以前，不會生成虛構字幕。'},202);
}
export async function onRequestGet(){return json({ok:true,schema:'dore.video-subtitle.v1',status:'intent-router-ready',pipeline:'video URL → caption/audio → transcription → Doré proofread → human feedback',executor:'not-yet-connected'})}
