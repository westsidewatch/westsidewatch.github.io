// Editorial and integrity gates for the Church visitor pathway. No network/secrets.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=p=>readFileSync(p,'utf8');
const json=p=>JSON.parse(read(p));
const base='static/data/church/';
const sunday=json(base+'current-sunday.json'),gatherings=json(base+'gatherings.json'),ministries=json(base+'ministries.json');
const p2=read('static/p2/living-water.html'),tour=read('static/p2/church-tour.html'),scene=read('static/p2/church-tour.js'),
 ministry=read('static/js/p2-church-ministry.js'),app=read('static/js/church-sunday.js'),
 overview=read('static/church/visit/index.html'),visitor=read('static/js/church-visit.js'),
 forms=read('static/church/forms/index.html'),formApp=read('static/js/church-forms.js'),
 api=read('functions/api/church-intake.js'),editor=read('static/tools/church-schedule-editor.html');
assert.equal(sunday.schemaVersion,1);
assert.equal(sunday.status,'archive','Historical October 11 bulletin must not be presented as live');
assert.equal(sunday.date,'2026-10-11');
assert.equal(sunday.schedule.length,7);
assert.ok(sunday.schedule.every(r=>r.time&&r.title&&typeof r.detail==='string'));
assert.ok(gatherings.items.some(x=>x.id==='monday'&&x.day==='週一'&&x.time==='中午'&&!x.timeVerified));
assert.ok(gatherings.items.some(x=>x.id==='friday'&&x.time==='晚上'&&!x.timeVerified));
assert.ok(gatherings.items.some(x=>x.id==='wednesday'&&x.mode==='線上'));
assert.deepEqual(ministries.items.map(x=>x.id),['welcome','fellowship','worship','prayer','care','discipleship','witness']);
assert.ok(ministries.items.every(x=>x.href.startsWith('/')&&x.action));
assert.ok(p2.includes('/js/church-sunday.js')&&tour.includes('/js/church-sunday.js'));
assert.ok(ministry.includes('window.WestsideSunday?.mountTour(root)'));
assert.ok(app.includes("fetch(source,{cache:'no-store'})")&&app.includes("const source='/data/church/current-sunday.json'"));
assert.ok(app.includes("d.status!=='current'"),'Expired calendar dates must not be silently current');
assert.ok(scene.includes("southWallName.position.set(9.35,5.75,0.16)"));
assert.ok(scene.includes("神召會活水堂西區教會")&&scene.includes("P.A.O.C. Living Water Assembly West"));
assert.ok(scene.includes("crossAperture={x:15,y:3.65"),'Never overwrite cross geometry');
assert.ok(scene.includes("{ at:251, p:[18.2,6.8,17.7]"));
assert.ok(read('static/js/p2-living-water.js').includes('const buildStart=2.50,buildEnd=3.27'));
assert.ok(p2.includes('href="/p2/church-tour.html?entry=p2"'));
assert.ok(ministry.includes('data-story-link')&&ministry.includes('/data/church/ministries.json'));
assert.ok(overview.includes('id="sunday"')&&overview.includes('id="gatherings"')&&overview.includes('id="invitation"'));
assert.ok(overview.includes('church-visit__identity-lockup')&&overview.includes('church-visit__scripture-tile'));
assert.ok(overview.includes('神召會活水堂西區教會')&&overview.includes('P.A.O.C. Living Water Assembly West'));
assert.ok(forms.includes('id="church-gospel" hidden')&&forms.includes('church-form__gospel-steps'));
assert.ok(forms.includes('約翰福音')&&forms.includes('羅馬書'));
assert.ok(formApp.includes('gospel.hidden=false'));
assert.ok(overview.includes('href="/join/"'),'Original Gate remains accessible without its broken historical QR');
assert.ok(!overview.includes('一座可以走進去的教會，也是一個可以繼續參與的教會'));
for(const kind of ['join','decision','newcomer','prayer']){
 assert.ok(forms.includes('name="consent"'));
 assert.ok(overview.includes('data-church-qr="'+kind+'"'));
 assert.ok(overview.includes('/church/forms/?type='+kind));
 assert.ok(formApp.includes(kind+':{title:'));
}
const matrices=visitor.match(/const qrMatrix=(\{[^\n]+\});/);
assert.ok(matrices,'QR matrices must be stored as local static bitmaps');
const qr=JSON.parse(matrices[1]);
for(const [kind,encoded] of Object.entries(qr))assert.ok(Buffer.from(encoded,'base64').length>=211,kind+' QR is incomplete');
assert.ok(api.includes('TURNSTILE_SECRET_KEY')&&api.includes('RESEND_API_KEY'));
assert.ok(api.includes('const available=env')&&api.includes('if(!available(env))return reject(503'));
assert.ok(api.includes('if(!verify?.success)return reject(403'));
assert.ok(api.includes('if(!receipt.ok)return reject(502'));
assert.ok(editor.includes('下載本週 JSON')&&read('static/js/church-schedule-editor.js').includes('current-sunday.json'));
for(const page of [overview,forms,editor])assert.ok(page.includes('/css/westside-design-os.css')&&page.includes('data-ws-scope='));
assert.ok(read('layouts/church/portal.html').includes('href="/church/visit/"'));
console.log('Church visitor contract passed: shared Sunday, 7 ministries, south-wall name, 4 offline QR, fail-closed intake');
