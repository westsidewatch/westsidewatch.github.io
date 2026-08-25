const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','access-control-allow-origin':'*'}});

function readPayload(row){
  try{return JSON.parse(row?.payload_json||'{}')}catch{return {}}
}

function explicitDownloadPermission(payload){
  const rights=payload?.rights||payload?.provenance?.rights||{};
  if(rights?.subtitle_download===true||rights?.subtitle_download==='allowed')return {allowed:true,basis:rights?.basis||rights?.license||'explicit-recorded-permission'};
  if(rights?.public_derivative===true)return {allowed:true,basis:rights?.basis||rights?.license||'explicit-public-derivative-permission'};
  return {allowed:false,basis:rights?.status||rights?.license||'permission-not-recorded'};
}

function publicState(row,payload,permission){
  const status=String(row?.status||'');
  const result=payload?.translated_caption||payload?.proofread_caption||null;
  const ready=status==='proofread-complete-result-ready'||status==='translated-result-ready'||status==='completed';
  const translationRequired=status==='proofread-complete-needs-translation';
  const transcriptionRequired=status==='needs-transcription-audio';
  const failed=/failure|failed|rejected|too-large|empty/.test(status);
  const downloadable=Boolean(ready&&result?.text&&result?.format==='vtt'&&permission.allowed);
  let reader_state='processing';
  if(downloadable)reader_state='result-downloadable';
  else if(ready&&result?.text)reader_state='result-ready-rights-restricted';
  else if(translationRequired)reader_state='translation-required';
  else if(transcriptionRequired)reader_state='transcription-required';
  else if(failed)reader_state='processing-error';
  return {
    job_id:row.id,
    status,
    reader_state,
    canonical_url:row.canonical_url,
    resource_id:row.resource_id||null,
    source_language:result?.language_code||payload?.acquired_caption?.language_code||null,
    target_language:row.target_language,
    format:result?.format||null,
    summary:result?.summary||null,
    rights:{download_allowed:permission.allowed,basis:permission.basis},
    download:downloadable?{available:true,url:`/api/dore/video-subtitle-result?job_id=${encodeURIComponent(row.id)}&download=1`,format:'vtt'}:{available:false},
    next_step:translationRequired?'translation-executor':transcriptionRequired?'audio-transcription-executor':ready&&!permission.allowed?'rights-review':failed?'executor-diagnosis':ready?'reader-delivery':'continue-processing'
  };
}

async function loadJob(db,id){
  return db.prepare(`SELECT id,resource_id,url,canonical_url,target_language,mode,status,created_at,updated_at,payload_json FROM dore_video_subtitle_jobs WHERE id=?1`).bind(id).first();
}

export async function onRequestGet({request,env}){
  const u=new URL(request.url);
  const id=Number(u.searchParams.get('job_id'));
  if(!id)return json({ok:false,error:'job_id_required'},400);
  if(!env?.DORE_SENSORY)return json({ok:false,error:'dore_sensory_unavailable'},503);
  let row;
  try{row=await loadJob(env.DORE_SENSORY,id)}catch(e){console.error('subtitle result lookup',e);return json({ok:false,error:'result_lookup_failed'},500)}
  if(!row)return json({ok:false,error:'job_not_found'},404);
  const payload=readPayload(row);
  const permission=explicitDownloadPermission(payload);
  const state=publicState(row,payload,permission);

  if(u.searchParams.get('download')==='1'){
    if(!state.download.available)return json({ok:false,error:'subtitle_download_not_authorized',reader_state:state.reader_state,rights:state.rights},403);
    const result=payload?.translated_caption||payload?.proofread_caption;
    const filename=`dore-subtitle-${row.id}.vtt`;
    return new Response(result.text,{status:200,headers:{'content-type':'text/vtt; charset=utf-8','content-disposition':`attachment; filename="${filename}"`,'cache-control':'private, no-store','x-content-type-options':'nosniff'}});
  }

  return json({ok:true,schema:'dore.video-subtitle-result.v1',result:state,boundary:'Raw acquired/proofread subtitle text is not exposed by this public result endpoint unless an explicit recorded rights permission allows downloadable derivative subtitle delivery.'});
}
