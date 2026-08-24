const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});

export async function onRequestGet({env}){
  const d1Bound=Boolean(env.DORE_SENSORY);
  const r2Bound=Boolean(env.DORE_ASSETS);
  if(!d1Bound||!r2Bound){
    return json({
      ok:false,
      connection:'dore-cloudflare-assets',
      d1_bound:d1Bound,
      r2_bound:r2Bound,
      error:!d1Bound?'dore_sensory_unbound':'dore_assets_unbound'
    },503);
  }

  try{
    // Read-only R2 probe: no object is created and no production asset is mutated.
    const probe=await env.DORE_ASSETS.list({limit:1});
    return json({
      ok:true,
      connection:'dore-cloudflare-assets',
      d1_bound:true,
      r2_bound:true,
      r2_readable:true,
      sample_object_count:Array.isArray(probe?.objects)?probe.objects.length:0,
      truncated:Boolean(probe?.truncated),
      checked_at:new Date().toISOString()
    });
  }catch(error){
    return json({
      ok:false,
      connection:'dore-cloudflare-assets',
      d1_bound:true,
      r2_bound:true,
      r2_readable:false,
      error:'r2_probe_failed',
      detail:String(error?.message||error)
    },500);
  }
}
