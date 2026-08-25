import {proofSubtitleSegments} from './subtitle-proofread.js';

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

function parseJsonArrayAfter(text,needle){
  const start=text.indexOf(needle);if(start<0)return null;
  let i=text.indexOf('[',start+needle.length);if(i<0)return null;
  const begin=i;let depth=0,inString=false,escaped=false;
  for(;i<text.length;i++){
    const c=text[i];
    if(inString){
      if(escaped){escaped=false;continue}
      if(c==='\\'){escaped=true;continue}
      if(c==='"')inString=false;
      continue;
    }
    if(c==='"'){inString=true;continue}
    if(c==='[')depth++;
    else if(c===']'){
      depth--;
      if(depth===0){try{return JSON.parse(text.slice(begin,i+1))}catch{return null}}
    }
  }
  return null;
}

function chooseCaptionTrack(tracks,targetLanguage){
  if(!Array.isArray(tracks)||!tracks.length)return null;
  const target=String(targetLanguage||'').toLowerCase();
  const prefs=[];
  if(target.startsWith('zh'))prefs.push('zh-Hant','zh-TW','zh-HK','zh-Hans','zh-CN','zh');
  if(target.startsWith('en'))prefs.push('en','en-US','en-GB');
  prefs.push('zh-Hant','zh-Hans','zh','en');
  for(const lang of prefs){const t=tracks.find(x=>String(x?.languageCode||'').toLowerCase()===lang.toLowerCase());if(t)return t}
  return tracks.find(x=>x?.kind!=='asr')||tracks[0];
}

function captionFetchUrl(baseUrl){
  try{
    const u=new URL(baseUrl);
    const h=u.hostname.toLowerCase();
    if(!(h==='youtube.com'||h.endsWith('.youtube.com')||h.endsWith('.googlevideo.com')))return null;
    u.searchParams.set('fmt','vtt');
    return u.toString();
  }catch{return null}
}

async function acquireYoutubeCaption(row){
  const canonical=new URL(row.canonical_url);
  if(canonical.hostname!=='youtube.com')return {ok:false,status:'executor-unsupported-host',reason:'automatic-caption-acquisition-currently-youtube-only'};
  const watch=await fetch(canonical.toString(),{headers:{'accept-language':'en-US,en;q=0.8','user-agent':'Mozilla/5.0 (compatible; WestsideWatch-Dore/1.0)'}});
  if(!watch.ok)return {ok:false,status:'caption-source-fetch-failed',reason:`youtube-watch-http-${watch.status}`};
  const html=await watch.text();
  const tracks=parseJsonArrayAfter(html,'"captionTracks":');
  if(!tracks?.length)return {ok:false,status:'needs-transcription-audio',reason:'no-caption-track-advertised'};
  const track=chooseCaptionTrack(tracks,row.target_language);
  const fetchUrl=captionFetchUrl(track?.baseUrl);
  if(!fetchUrl)return {ok:false,status:'caption-source-rejected',reason:'caption-track-url-outside-allowed-hosts'};
  const cap=await fetch(fetchUrl,{headers:{'accept-language':'en-US,en;q=0.8','user-agent':'Mozilla/5.0 (compatible; WestsideWatch-Dore/1.0)'}});
  if(!cap.ok)return {ok:false,status:'caption-source-fetch-failed',reason:`caption-http-${cap.status}`};
  const text=await cap.text();
  if(!text.trim())return {ok:false,status:'caption-source-empty',reason:'caption-response-empty'};
  if(text.length>750000)return {ok:false,status:'caption-source-too-large',reason:'caption-exceeds-d1-payload-boundary'};
  return {ok:true,status:'caption-acquired-awaiting-proofread',caption:{language_code:track.languageCode||null,name:track?.name?.simpleText||null,kind:track.kind||'manual',is_translatable:Boolean(track.isTranslatable),format:'vtt',text}};
}

function parseVttForProofread(vtt){
  const normalized=String(vtt||'').replace(/\r\n?/g,'\n');
  if(!normalized.trim().startsWith('WEBVTT'))throw new Error('acquired_caption_not_webvtt');
  const blocks=normalized.split(/\n{2,}/);
  const cues=[];
  for(let blockIndex=0;blockIndex<blocks.length;blockIndex++){
    const lines=blocks[blockIndex].split('\n');
    const timingIndex=lines.findIndex(line=>line.includes('-->'));
    if(timingIndex<0)continue;
    const textStart=timingIndex+1;
    if(textStart>=lines.length)continue;
    cues.push({id:cues.length,blockIndex,lines,textStart,text:lines.slice(textStart).join('\n')});
  }
  if(!cues.length)throw new Error('webvtt_has_no_cues');
  return {blocks,cues};
}

function proofreadVtt(vtt){
  const parsed=parseVttForProofread(vtt);
  const correctedById=new Map();
  let changed=0;
  for(let offset=0;offset<parsed.cues.length;offset+=500){
    const batch=parsed.cues.slice(offset,offset+500).map(c=>({id:c.id,text:c.text}));
    const processed=proofSubtitleSegments(batch);
    changed+=processed.summary.changed;
    for(const result of processed.results)correctedById.set(result.id,result.corrected);
  }
  for(const cue of parsed.cues){
    const corrected=correctedById.get(cue.id);
    if(typeof corrected!=='string')continue;
    parsed.blocks[cue.blockIndex]=[...cue.lines.slice(0,cue.textStart),...corrected.split('\n')].join('\n');
  }
  return {text:parsed.blocks.join('\n\n'),summary:{segments:parsed.cues.length,changed}};
}

function needsTranslation(sourceLanguage,targetLanguage,mode){
  const modeValue=String(mode||'').toLowerCase();
  if(!modeValue.includes('translate'))return false;
  const source=String(sourceLanguage||'').toLowerCase();
  const target=String(targetLanguage||'').toLowerCase();
  if(!target)return false;
  if(target.startsWith('zh-hant')||target==='zh-tw'||target==='zh-hk')return !(source.startsWith('zh-hant')||source==='zh-tw'||source==='zh-hk');
  if(target.startsWith('zh-hans')||target==='zh-cn')return !(source.startsWith('zh-hans')||source==='zh-cn');
  return !source.startsWith(target.split('-')[0]);
}

async function loadJob(db,id){
  return db.prepare(`SELECT id,resource_id,url,canonical_url,target_language,mode,status,created_at,updated_at,payload_json FROM dore_video_subtitle_jobs WHERE id=?1`).bind(id).first();
}

function readPayload(row){let payload={};try{payload=JSON.parse(row.payload_json||'{}')}catch{}return payload}

async function persistExecution(db,row,result){
  const now=new Date().toISOString();
  const payload=readPayload(row);
  payload.execution={...(payload.execution||{}),caption_acquisition:{attempted_at:now,ok:result.ok,status:result.status,reason:result.reason||null}};
  if(result.caption)payload.acquired_caption=result.caption;
  await db.prepare(`UPDATE dore_video_subtitle_jobs SET status=?1,updated_at=?2,payload_json=?3 WHERE id=?4`).bind(result.status,now,JSON.stringify(payload),row.id).run();
  return {...result,job_id:row.id,updated_at:now};
}

async function executeProofread(db,row){
  const payload=readPayload(row);
  const caption=payload?.acquired_caption;
  if(!caption?.text||caption?.format!=='vtt')return {ok:false,http:409,error:'acquired_vtt_required',status:row.status};
  const processed=proofreadVtt(caption.text);
  if(processed.text.length>750000)return {ok:false,http:413,error:'proofread_caption_too_large'};
  const translate=needsTranslation(caption.language_code,row.target_language,row.mode);
  const status=translate?'proofread-complete-needs-translation':'proofread-complete-result-ready';
  const now=new Date().toISOString();
  payload.proofread_caption={format:'vtt',language_code:caption.language_code||null,target_language:row.target_language,text:processed.text,summary:processed.summary,proofreader_schema:'dore.subtitle-proofread.v2',completed_at:now};
  payload.execution={...(payload.execution||{}),proofread:{completed_at:now,ok:true,status,segments:processed.summary.segments,changed:processed.summary.changed,translation_required:translate}};
  await db.prepare(`UPDATE dore_video_subtitle_jobs SET status=?1,updated_at=?2,payload_json=?3 WHERE id=?4`).bind(status,now,JSON.stringify(payload),row.id).run();
  return {ok:true,http:200,status,job_id:row.id,updated_at:now,summary:processed.summary,translation_required:translate};
}

export async function onRequestPost({request,env}){
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}

  if(body?.action==='execute-caption-acquisition'){
    const jobId=Number(body?.job_id);
    if(!jobId)return json({ok:false,error:'job_id_required'},400);
    if(!env?.DORE_SENSORY)return json({ok:false,error:'dore_sensory_unavailable'},503);
    try{
      await ensureSchema(env.DORE_SENSORY);
      const row=await loadJob(env.DORE_SENSORY,jobId);
      if(!row)return json({ok:false,error:'job_not_found'},404);
      if(['completed','cancelled'].includes(row.status))return json({ok:false,error:'job_not_executable',status:row.status},409);
      if(!row.canonical_url)return json({ok:false,error:'canonical_url_missing'},409);
      let result;
      try{result=await acquireYoutubeCaption(row)}catch(e){result={ok:false,status:'caption-acquisition-retryable-failure',reason:String(e?.message||e)}}
      const persisted=await persistExecution(env.DORE_SENSORY,row,result);
      const http=result.ok?200:(result.status==='needs-transcription-audio'||result.status==='executor-unsupported-host'?202:502);
      return json({ok:result.ok,schema:'dore.video-subtitle.v5',execution:persisted,boundary:'Caption acquisition uses only caption tracks advertised by the supported video source. No subtitle text is invented. Audio transcription remains a separate executor stage.'},http);
    }catch(e){console.error('caption acquisition executor',e);return json({ok:false,error:'caption_acquisition_executor_failed'},500)}
  }

  if(body?.action==='execute-proofread'){
    const jobId=Number(body?.job_id);
    if(!jobId)return json({ok:false,error:'job_id_required'},400);
    if(!env?.DORE_SENSORY)return json({ok:false,error:'dore_sensory_unavailable'},503);
    try{
      await ensureSchema(env.DORE_SENSORY);
      const row=await loadJob(env.DORE_SENSORY,jobId);
      if(!row)return json({ok:false,error:'job_not_found'},404);
      if(!['caption-acquired-awaiting-proofread','proofread-complete-needs-translation','proofread-complete-result-ready'].includes(row.status))return json({ok:false,error:'job_not_ready_for_proofread',status:row.status},409);
      let result;
      try{result=await executeProofread(env.DORE_SENSORY,row)}catch(e){return json({ok:false,error:'proofread_execution_failed',detail:String(e?.message||e)},422)}
      if(!result.ok)return json(result,result.http||500);
      return json({ok:true,schema:'dore.video-subtitle.v5',execution:result,boundary:'Proofreading reuses Doré conservative biblical-term rules. Translation remains a distinct stage and is never fabricated.'},result.http);
    }catch(e){console.error('subtitle proofread executor',e);return json({ok:false,error:'subtitle_proofread_executor_failed'},500)}
  }

  const rawUrl=String(body?.url||'').trim();
  const canonicalUrl=canonicalize(rawUrl);
  if(!canonicalUrl||!supported(canonicalUrl))return json({ok:false,error:'supported_video_url_required'},400);
  const resourceId=String(body?.resource_id||'').trim()||null;
  const targetLanguage=String(body?.target_language||'zh-Hant').trim();
  const mode=String(body?.mode||'proofread-and-translate').trim();
  const createdAt=new Date().toISOString();
  const job={schema:'dore.video-subtitle.v5',url:rawUrl,canonical_url:canonicalUrl,resource_id:resourceId,target_language:targetLanguage,mode,created_at:createdAt,intent:'video_to_corrected_accessible_subtitle',pipeline:['identify-video','canonicalize-deduplicate','resolve-library-resource','obtain-caption-or-audio','transcribe-if-needed','dore-proofread','translate-if-needed','scripture-align','human-review','library-feedback','learning-feedback']};
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
    const row=await loadJob(env.DORE_SENSORY,id);
    if(!row)return json({ok:false,error:'job_not_found'},404);
    return json({ok:true,schema:'dore.video-subtitle.v5',job:row});
  }catch(e){console.error('video subtitle job lookup',e);return json({ok:false,error:'job_lookup_failed'},500)}}
  return json({ok:true,schema:'dore.video-subtitle.v5',status:'caption-and-proofread-executors-connected',pipeline:'video URL → canonicalize/deduplicate → Liming resource → advertised caption acquisition → audio transcription if needed → Doré proofread → translation if needed → Scripture alignment → human review → library + learning feedback',executors:['youtube-advertised-caption-acquisition','dore-vtt-proofread']});
}
