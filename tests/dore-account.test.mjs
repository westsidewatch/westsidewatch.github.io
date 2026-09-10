import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {test} from 'node:test';
const source=readFileSync(new URL('../static/dore/account/auth.js',import.meta.url),'utf8');
async function setup({session=null,otpError=null,settingsError=false,hash='',search=''}={}) {
  const calls=[];const timers=[];let listener;
  const node=()=>({hidden:false,disabled:false,textContent:'',value:' person@example.com ',listeners:{},addEventListener(e,f){this.listeners[e]=f},setAttribute(){},checkValidity(){return this.value.includes('@')},reportValidity(){this.invalid=true}});
  const ids=Object.fromEntries(['status','email-form','email','session-panel','session-email','logout','continue'].map(id=>[id,node()]));
  const submit=node();ids['email-form'].querySelector=()=>submit;
  const providers=['google','apple','microsoft','github'].map(provider=>Object.assign(node(),{dataset:{provider}}));
  const groups={'.providers':node(),'.divider':node()};const link=node();
  const auth={getSession:async()=>({data:{session},error:null}),onAuthStateChange:f=>{listener=f},signInWithOtp:async args=>{calls.push(args);return {error:otpError}},signOut:async()=>({error:null})};
  const history=[];
  vm.runInNewContext(source,{window:{DORE_AUTH_CONFIG:{url:'https://auth.example',publishableKey:'public'},supabase:{createClient:()=>({auth})},location:{origin:'https://site.example',hash,search,pathname:'/dore/account/'},history:{replaceState(...args){history.push(args)}}},document:{getElementById:id=>ids[id],querySelectorAll:s=>s==='.account-link'?[link]:providers,querySelector:s=>groups[s],title:'Account'},fetch:async()=>({ok:!settingsError,json:async()=>({external:{email:true,google:false},disable_signup:false})}),AbortSignal,URLSearchParams,Date,setInterval:f=>{timers.push(f);return 1},clearInterval(){}});
  await new Promise(resolve=>setImmediate(resolve));
  return {ids,submit,providers,calls,listener,link,history};
}
test('only configured providers appear; duplicate sends and cooldown are blocked',async()=>{
 const x=await setup();assert.ok(x.providers.every(p=>p.hidden));assert.equal(x.submit.disabled,false);
 const event={preventDefault(){}};
 await Promise.all([x.ids['email-form'].listeners.submit(event),x.ids['email-form'].listeners.submit(event)]);
 assert.equal(x.calls.length,1);assert.equal(x.calls[0].email,'person@example.com');assert.equal(x.calls[0].options.shouldCreateUser,true);assert.equal(x.submit.disabled,true);
 await x.ids['email-form'].listeners.submit(event);assert.equal(x.calls.length,1);
});
test('failed sends recover and permit retry',async()=>{const x=await setup({otpError:{status:429,message:'rate limit'}});await x.ids['email-form'].listeners.submit({preventDefault(){}});assert.equal(x.submit.disabled,false);assert.match(x.ids.status.textContent,/過於頻繁/)});
test('session updates account entry and logout restores form',async()=>{const x=await setup({session:{user:{email:'a@example.com'}}});assert.equal(x.ids['email-form'].hidden,true);assert.equal(x.link.textContent,'我的帳號');assert.equal(x.ids.continue.href,'/multiwrite/#library');await x.ids.logout.listeners.click();assert.equal(x.ids['email-form'].hidden,false);assert.equal(x.link.textContent,'註冊／登入')});
test('unavailable settings fail closed',async()=>{const x=await setup({settingsError:true});assert.equal(x.submit.disabled,true);assert.match(x.ids.status.textContent,/載入失敗/)});
test('query callback errors are visible and removed from address',async()=>{const x=await setup({search:'?error=access_denied&error_description=Denied'});assert.match(x.ids.status.textContent,/登入未完成/);assert.equal(x.history[0][2],'/dore/account/')});
test('invalid email never sends',async()=>{const x=await setup();x.ids.email.value='invalid';await x.ids['email-form'].listeners.submit({preventDefault(){}});assert.equal(x.calls.length,0);assert.equal(x.ids.email.invalid,true)});
