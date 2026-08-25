const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','access-control-allow-origin':'*'}});
const supported=url=>{try{const u=new URL(url);return /^https?:$/.test(u.protocol)&&/(youtube\.com|youtu\.be|vimeo\.com|facebook\.com|fb\.watch|instagram\.com|westsidewatch\.ca)$/i.test(u.hostname.replace(/^www\./,''))}catch{return false}};
export async function onRequestPost({request,env}){
 let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
 const url=String(body?.url||'').trim();if(!supported(url))return json({ok:false,error:'supported_video_url_required'},400);
 const resourceId=String(body?.resource_id||'').trim()||null;
 const targetLanguage=String(body?.target_language||'zh-Hant').trim();
 const mode=String(body?.mode||'proofread-and-translate').trim();
 const job={schema:'dore.video-subtitle.v2',url,resource_id:resourceId,target_language:targetLanguage,mode,created_at:new Date().toISOString(),intent:'video_to_corrected_accessible_subtitle',pipeline:['identify-video','resolve-library-resource','obtain-caption-or-audio','transcribe-if-needed','dore-proofread','translate-if-needed','scripture-align','human-review','library-feedback','learning-feedback']};
 let recorded=false,jobId=null;
 if(env?.DORE_SENSORY){try{
   await env.DORE_SENSORY.prepare(`CREATE TABLE IF NOT EXISTS dore_video_subtitle_jobs (id INTEGER PRIMARY KEY AUTOINCREMENT,resource_id TEXT,url TEXT NOT NULL,target_language TEXT NOT NULL DEFAULT 'zh-Hant',mode TEXT NOT NULL DEFAULT 'proofread-and-translate',status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,payload_json TEXT NOT NULL)`).run();
   const info=await env.DORE_SENSORY.prepare('PRAGMA table_info(dore_video_subtitle_jobs)').all();
   const cols=new Set((info?.results||[]).map(r=>r.name));
   if(!cols.has('resource_id'))await env.DORE_SENSORY.prepare('ALTER TABLE dore_video_subtitle_jobs ADD COLUMN resource_id TEXT').run();
   if(!cols.has('target_language'))await env.DORE_SENSORY.prepare("ALTER TABLE dore_video_subtitle_jobs ADD COLUMN target_language TEXT NOT NULL DEFAULT 'zh-Hant'").run();
   if(!cols.has('mode'))await env.DORE_SENSORY.prepare("ALTER TABLE dore_video_subtitle_jobs ADD COLUMN mode TEXT NOT NULL DEFAULT 'proofread-and-translate'").run();
   if(!cols.has('updated_at'))await env.DORE_SENSORY.prepare('ALTER TABLE dore_video_subtitle_jobs ADD COLUMN updated_at TEXT').run();
   const r=await env.DORE_SENSORY.prepare(`INSERT INTO dore_video_subtitle_jobs(resource_id,url,target_language,mode,status,created_at,updated_at,payload_json) VALUES(?1,?2,?3,?4,'awaiting-transcription-executor',?5,?5,?6)`).bind(resourceId,url,targetLanguage,mode,job.created_at,JSON.stringify(job)).run();
   jobId=r?.meta?.last_row_id||null;recorded=true;
   if(resourceId){
     try{await env.DORE_SENSORY.prepare(`UPDATE liming_resources SET chinese_access=CASE WHEN ?1 LIKE 'zh%' THEN 'dore-subtitle-queued' ELSE chinese_access END,updated_at=?2 WHERE resource_id=?3`).bind(targetLanguage,job.created_at,resourceId).run()}catch(e){console.warn('library subtitle feedback skipped',e)}
   }
 }catch(e){console.error('video subtitle job registry',e)}}
 return json({ok:true,status:'awaiting-transcription-executor',recorded,job_id:jobId,job,message:'影片已進入 Doré 字幕工作隊列；若它來自黎明書局，工作會綁定同一 resource_id，完成後回寫中文可及性與學習反饋。',boundary:'目前仍不會在沒有取得字幕或音訊的情況下虛構字幕。'},202);
}
export async function onRequestGet(){return json({ok:true,schema:'dore.video-subtitle.v2',status:'library-linked-intent-router-ready',pipeline:'Liming resource/video URL → caption/audio → transcription → Doré proofread → translation → Scripture alignment → human review → library + learning feedback',executor:'not-yet-connected'})}
