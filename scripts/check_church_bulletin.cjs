#!/usr/bin/env node
const fs=require('node:fs');
const assert=require('node:assert/strict');
const d=JSON.parse(fs.readFileSync('data/church/bulletins/2026-10-11.json','utf8'));
assert.equal(d.schedule.length,7);
assert.deepEqual(d.schedule.map(x=>x.time),['10:30–11:00','11:00–11:30','11:30–12:20','12:20–12:40','12:40','12:45–13:00','13:00–13:30']);
for(const [i,s] of d.schedule.entries()){
 assert.ok(s.title,'missing stage '+i);
 assert.ok(s.actions.length,'missing actions '+i);
 for(const a of s.actions)assert.ok(a.text,'missing action text '+i);
}
assert.equal(d.sermon_title,'凡事謝恩');
assert.equal(d.next.date_label,'10月18日');
assert.equal(d.date,'2026-10-11');
assert.equal(d.church,'神召會活水堂西區教會');
assert.equal(d.address,'205 Wilmington Ave., North York, ON M3H 6B3');
assert.deepEqual(d.team.map(x=>x.role),['主任牧師','司會主席','敬拜主領','今日證道']);
assert.deepEqual(d.schedule.map(x=>x.actions.length),[1,2,1,2,2,2,1]);
assert.deepEqual(d.schedule.map(x=>x.title),['以等候宣告敬拜神','以揚聲讚美敬拜神','以聆聽信息敬拜神','以回應奉獻敬拜神','以領受祝福敬拜神','以關懷相交敬拜神','以合一禱告敬拜神']);
const frontMatter=fs.readFileSync('content/church/bulletin-2026-10-11.md','utf8');
assert.match(frontMatter,/layout: "bulletin"/);
assert.match(frontMatter,/date: 2026-10-11/);
const template=fs.readFileSync('layouts/church/bulletin.html','utf8');
assert.match(template,/site\.Data\.church\.bulletins/);
assert.match(template,/range \$data\.schedule/);
assert.match(template,/range \.actions/);
console.log('PASS church bulletin: dated data, seven stages, actions and reusable template');
