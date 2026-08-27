const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});

// OpenAI/ChatGPT API access is intentionally disabled for Doré.
// This endpoint must never make a paid external model request.
export function onRequestGet(){
 return json({ok:false,schema:'dore.conversation-disabled.v1',configured:false,provider:null,error:'external_paid_ai_disabled'},503);
}

export async function onRequestPost(){
 return json({ok:false,schema:'dore.conversation-disabled.v1',error:'external_paid_ai_disabled'},503);
}
