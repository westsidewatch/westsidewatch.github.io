const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','access-control-allow-origin':'*'}});

function canonicalize(raw){
  try{
    const u=new URL(String(raw||'').trim());
    if(!/^https?:$/.test(u.protocol))return null;
    u.hash='';
    u.hostname=u.hostname.toLowerCase().replace(/^www\./,'');
    if(u.hostname==='youtu.be'){
      const id=u.pathname.split('/').filter(Boolean)[0];
      if(!id)return null;
      return `https://youtube.com/watch?v=${encodeURIComponent(id)}`;
    }
    if(u.hostname==='youtube.com'){
      const id=u.searchParams.get('v');
      if(id)return `https://youtube.com/watch?v=${encodeURIComponent(id)}`;
    }
    for(const key of [...u.searchParams.keys()]){
      if(/^utm_/i.test(key)||['fbclid','gclid','si','feature'].includes(key))u.searchParams.delete(key);
    }
    u.pathname=u.pathname.replace(/\/+$/,'')||'/';
    const qs=[...u.searchParams.entries()].sort(([a],[b])=>a.localeCompare(b));
    u.search='';
    for(const [k,v] of qs)u.searchParams.append(k,v);
    return u.toString();
  }catch{return null}
}

const supported=url=>{try{const u=new URL(url);return /(youtube\.com|vimeo\.com|facebook\.com|fb\.watch|instagram\.com|westsidewatch\.ca)$/i.test(u.hostname)}catch{return false}};

async function ensureSchema(db){
  await db.prepare(`CREATE TABLE IF NOT EXISTS dore_video_subtitle_jobs (id INTEGER PRIMARY KEY AUTOINCREMENT,resource_id TEXT,url TEXT NOT NULL,canonical_url TEXT,target_language TEXT NOT NULL DEFAULT 'zh-Hant',mode TEXT NOT NULL DEFAULT 'proofread-and-translate',status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,payload_json TEXT NOT NULL)`).run();
  const info=await db.prepare('PRAGMA table_info(dore_video_subtitle_jobs)').all();
  const cols=new Set((info?.results||[]).map(r=>r.name));
  const additions=[
    ['resource_id','TEXT'],['canonical_url','TEXT'],['target_language',"TEXT NOT NULL DEFAULT 'zh-Hant'"],['mode',"TEXT NOT NULL DEFAULT 'proofread-and-translate'"],['updated_at','TEXT']
  ];
  for(const [name,type] of additions)if(!cols.has(name))await db.prepare(`ALTER TABLE dore_video_subtitle_jobs ADD COLUMN ${name} ${type}`).run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_video_subtitle_jobs_canonical ON dore_video_subtitle_jobs(canonical_url,target_language,mode,status)').run();
}

export async function onRequestPost({request,env}){
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  const rawUrl=String(body?.url||'').trim();
  const canonicalUrl=canonicalize(rawUrl);
  if(!canonicalUrl||!supported(canonicalUrl))return json({ok:false,error:'supported_video_url_required'},400);
  const resourceId=String(body?.resource_id||'').trim()||null;
  const targetLanguage=String(body?.target_language||'zh-Hant').trim();
  const mode=String(body?.mode||'proofread-and-translate').trim();
  const createdAt=new Date().toISOString();
  const job={schema:'dore.video-subtitle.v3',url:rawUrl,canonical_url:canonicalUrl,resource_id:resourceId,target_language:targetLanguage,mode,created_at:createdAt,intent:'video_to_corrected_accessible_subtitle',pipeline:['identify-video','canonicalize-deduplicate','resolve-library-resource','obtain-caption-or-audio','transcribe-if-needed','dore-proofread','translate-if-needed','scripture-align','human-review','library-feedback','learning-feedback']};
  let recorded=false,jobId=null,deduplicated=false;
  if(env?.DORE_SENSORY){try{
    await ensureSchema(env.DORE_SENSORY);
    const existing=await env.DORE_SENSORY.prepare(`SELECT id,status,resource_id,created_at,updated_at FROM dore_video_subtitle_jobs WHERE canonical_url=?1 AND target_language=?2 AND mode=?3 AND status NOT IN ('failed','cancelled','completed') ORDER BY id DESC LIMIT 1`).bind(canonicalUrl,targetLanguage,mode).first();
    if(existing){
      deduplicated=true;jobId=existing.id;
      return json({ok:true,status:existing.status,recorded:false,deduplicated:true,job_id:jobId,canonical_url:canonicalUrl,existing_job:existing,message:'已找到同一影片、語言與工作模式的進行中字幕任務；Doré 會續用既有 job，而不是重複建立。'},200);
    }
    const r=await env.DORE_SENSORY.prepare(`INSERT INTO dore_video_subtitle_jobs(resource_id,url,canonical_url,target_language,mode,status,created_at,updated_at,payload_json) VALUES(?1,?2,?3,?4,?5,'awaiting-transcription-executor',?6,?6,?7)`).bind(resourceId,rawUrl,canonicalUrl,targetLanguage,mode,createdAt,JSON.stringify(job)).run();
    jobId=r?.meta?.last_row_id||null;recorded=true;
    if(resourceId){
      try{await env.DORE_SENSORY.prepare(`UPDATE liming_resources SET chinese_access=CASE WHEN ?1 LIKE 'zh%' THEN 'dore-subtitle-queued' ELSE chinese_access END,updated_at=?2 WHERE resource_id=?3`).bind(targetLanguage,createdAt,resourceId).run()}catch(e){console.warn('library subtitle feedback skipped',e)}
    }
  }catch(e){console.error('video subtitle job registry',e)}
  return json({ok:true,status:'awaiting-transcription-executor',recorded,deduplicated,job_id:jobId,canonical_url:canonicalUrl,job,message:'影片已進入 Doré 字幕工作隊列；若它來自黎明書局，工作會綁定同一 resource_id，完成後回寫中文可及性與學習反饋。',boundary:'目前仍不會在沒有取得字幕或音訊的情況下虛構字幕。'},202);
}

export async function onRequestGet({request,env}){
  const u=new URL(request.url);const id=Number(u.searchParams.get('job_id'));
  if(id&&env?.DORE_SENSORY){try{
    await ensureSchema(env.DORE_SENSORY);
    const row=await env.DORE_SENSORY.prepare(`SELECT id,resource_id,url,canonical_url,target_language,mode,status,created_at,updated_at,payload_json FROM dore_video_subtitle_jobs WHERE id=?1`).bind(id).first();
    if(!row)return json({ok:false,error:'job_not_found'},404);
    return json({ok:true,schema:'dore.video-subtitle.v3',job:row});
  }catch(e){console.error('video subtitle job lookup',e);return json({ok:false,error:'job_lookup_failed'},500)}}
  return json({ok:true,schema:'dore.video-subtitle.v3',status:'library-linked-intent-router-ready',pipeline:'video URL → canonicalize/deduplicate → Liming resource → caption/audio → transcription → Doré proofread → translation → Scripture alignment → human review → library + learning feedback',executor:'not-yet-connected'});
}
