const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','access-control-allow-origin':'*'}});
const auth=(request,env)=>{const h=request.headers.get('authorization')||'';return Boolean(env.DORE_HEARTBEAT_TOKEN)&&h===`Bearer ${env.DORE_HEARTBEAT_TOKEN}`};
const list=v=>Array.isArray(v)?v:[];
const text=v=>String(v??'').trim();
const validUrl=v=>{try{const u=new URL(v);return /^https?:$/.test(u.protocol)}catch{return false}};
async function schema(db){
  await db.prepare(`CREATE TABLE IF NOT EXISTS liming_resources(
    resource_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    title_en TEXT,
    creator TEXT,
    series TEXT,
    resource_type TEXT NOT NULL,
    language TEXT,
    source_url TEXT NOT NULL UNIQUE,
    source_class TEXT NOT NULL DEFAULT 'unverified',
    rights_status TEXT NOT NULL DEFAULT 'unknown',
    morning_stars INTEGER NOT NULL DEFAULT 0,
    chinese_access TEXT NOT NULL DEFAULT 'unknown',
    status TEXT NOT NULL DEFAULT 'candidate',
    scripture_refs_json TEXT NOT NULL DEFAULT '[]',
    topics_json TEXT NOT NULL DEFAULT '[]',
    products_json TEXT NOT NULL DEFAULT '[]',
    provenance_json TEXT NOT NULL DEFAULT '{}',
    discovered_by TEXT NOT NULL DEFAULT 'dore',
    discovered_at TEXT NOT NULL,
    verified_at TEXT,
    updated_at TEXT NOT NULL
  )`).run();
  await db.prepare(`CREATE TABLE IF NOT EXISTS liming_resource_edges(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    edge_key TEXT NOT NULL,
    edge_value TEXT,
    provenance_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    UNIQUE(resource_id,edge_type,edge_key,edge_value)
  )`).run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_liming_creator ON liming_resources(creator)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_liming_series ON liming_resources(series)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_liming_status ON liming_resources(status)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_liming_stars ON liming_resources(morning_stars)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_liming_edges ON liming_resource_edges(edge_type,edge_key)').run();
}
function makeId(url){let h=2166136261;for(const c of url){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return 'LM-'+(h>>>0).toString(36).toUpperCase()}
export async function onRequestGet({request,env}){
  if(!env.DORE_SENSORY)return json({ok:false,error:'library_db_unbound'},503);
  await schema(env.DORE_SENSORY);
  const u=new URL(request.url),q=text(u.searchParams.get('q')),creator=text(u.searchParams.get('creator')),series=text(u.searchParams.get('series')),book=text(u.searchParams.get('book')),chapter=text(u.searchParams.get('chapter')),stars=Number(u.searchParams.get('morning_stars')||0),status=text(u.searchParams.get('status')||'published');
  const where=[],args=[];let n=1;
  if(q){where.push(`(title LIKE ?${n} OR title_en LIKE ?${n} OR creator LIKE ?${n} OR series LIKE ?${n})`);args.push('%'+q+'%');n++}
  if(creator){where.push(`creator=?${n}`);args.push(creator);n++}
  if(series){where.push(`series=?${n}`);args.push(series);n++}
  if(stars){where.push(`morning_stars>=?${n}`);args.push(stars);n++}
  if(status&&status!=='all'){where.push(`status=?${n}`);args.push(status);n++}
  if(book){where.push(`resource_id IN (SELECT resource_id FROM liming_resource_edges WHERE edge_type='scripture-book' AND edge_key=?${n})`);args.push(book);n++}
  if(chapter){where.push(`resource_id IN (SELECT resource_id FROM liming_resource_edges WHERE edge_type='scripture-chapter' AND edge_key=?${n})`);args.push(chapter);n++}
  const sql=`SELECT * FROM liming_resources ${where.length?'WHERE '+where.join(' AND '):''} ORDER BY morning_stars DESC, updated_at DESC LIMIT 100`;
  const r=await env.DORE_SENSORY.prepare(sql).bind(...args).all();
  return json({ok:true,schema:'liming.library.resources.v1',results:r.results||[]});
}
export async function onRequestPost({request,env}){
  if(!auth(request,env))return json({ok:false,error:'unauthorized'},401);
  if(!env.DORE_SENSORY)return json({ok:false,error:'library_db_unbound'},503);
  await schema(env.DORE_SENSORY);
  let b;try{b=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  const source_url=text(b.source_url),title=text(b.title),resource_type=text(b.resource_type||'web-resource');
  if(!title||!validUrl(source_url))return json({ok:false,error:'title_and_http_source_url_required'},400);
  const now=new Date().toISOString(),id=text(b.resource_id)||makeId(source_url),stars=Math.max(0,Math.min(3,Number(b.morning_stars)||0));
  const sourceClass=new Set(['official','authorized','institutional','library','third-party','unverified']).has(text(b.source_class))?text(b.source_class):'unverified';
  const rights=new Set(['official-share','public-domain','licensed','link-only','restricted','unknown']).has(text(b.rights_status))?text(b.rights_status):'unknown';
  const status=new Set(['candidate','reviewed','published','retired']).has(text(b.status))?text(b.status):'candidate';
  await env.DORE_SENSORY.prepare(`INSERT INTO liming_resources(resource_id,title,title_en,creator,series,resource_type,language,source_url,source_class,rights_status,morning_stars,chinese_access,status,scripture_refs_json,topics_json,products_json,provenance_json,discovered_by,discovered_at,verified_at,updated_at)
  VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14,?15,?16,?17,?18,?19,?20,?21)
  ON CONFLICT(source_url) DO UPDATE SET title=excluded.title,title_en=excluded.title_en,creator=excluded.creator,series=excluded.series,resource_type=excluded.resource_type,language=excluded.language,source_class=excluded.source_class,rights_status=excluded.rights_status,morning_stars=excluded.morning_stars,chinese_access=excluded.chinese_access,status=excluded.status,scripture_refs_json=excluded.scripture_refs_json,topics_json=excluded.topics_json,products_json=excluded.products_json,provenance_json=excluded.provenance_json,verified_at=excluded.verified_at,updated_at=excluded.updated_at`)
    .bind(id,title,text(b.title_en)||null,text(b.creator)||null,text(b.series)||null,resource_type,text(b.language)||null,source_url,sourceClass,rights,stars,text(b.chinese_access)||'unknown',status,JSON.stringify(list(b.scripture_refs)),JSON.stringify(list(b.topics)),JSON.stringify(list(b.products)),JSON.stringify(b.provenance||{}),text(b.discovered_by)||'dore',text(b.discovered_at)||now,text(b.verified_at)||null,now).run();
  const edges=[];
  for(const ref of list(b.scripture_refs)){
    if(ref?.book)edges.push(['scripture-book',String(ref.book),null]);
    if(ref?.book&&ref?.chapter)edges.push(['scripture-chapter',`${ref.book}:${ref.chapter}`,String(ref.verses||'')]);
  }
  if(text(b.creator))edges.push(['teacher',text(b.creator),null]);
  if(text(b.series))edges.push(['series',text(b.series),null]);
  for(const product of list(b.products))edges.push(['product',String(product),null]);
  for(const [type,key,value] of edges){await env.DORE_SENSORY.prepare(`INSERT OR IGNORE INTO liming_resource_edges(resource_id,edge_type,edge_key,edge_value,provenance_json,created_at) VALUES(?1,?2,?3,?4,?5,?6)`).bind(id,type,key,value,JSON.stringify(b.provenance||{}),now).run()}
  const row=await env.DORE_SENSORY.prepare('SELECT * FROM liming_resources WHERE source_url=?1').bind(source_url).first();
  return json({ok:true,schema:'liming.library.resources.v1',resource:row},201);
}
export async function onRequestPatch({request,env}){
  if(!auth(request,env))return json({ok:false,error:'unauthorized'},401);
  if(!env.DORE_SENSORY)return json({ok:false,error:'library_db_unbound'},503);
  await schema(env.DORE_SENSORY);
  let b;try{b=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  const id=text(b.resource_id),status=text(b.status);if(!id||!new Set(['candidate','reviewed','published','retired']).has(status))return json({ok:false,error:'resource_id_and_valid_status_required'},400);
  const now=new Date().toISOString(),verified=status==='reviewed'||status==='published'?now:null;
  await env.DORE_SENSORY.prepare('UPDATE liming_resources SET status=?1,verified_at=COALESCE(?2,verified_at),updated_at=?3 WHERE resource_id=?4').bind(status,verified,now,id).run();
  return json({ok:true,resource_id:id,status,updated_at:now});
}
