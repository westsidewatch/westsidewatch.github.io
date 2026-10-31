import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {dirname,resolve} from 'node:path';
const args=process.argv.slice(2),options={};
for(let i=0;i<args.length;i+=2){assert.ok(['--report','--render-commit','--out'].includes(args[i])&&args[i+1]);options[args[i]]=args[i+1];}
for(const key of ['--report','--render-commit','--out'])assert.ok(options[key],`Missing ${key}`);
assert.match(options['--render-commit'],/^[a-f0-9]{7,40}$/);
const [raw,programmeRaw]=await Promise.all([readFile(options['--report'],'utf8'),readFile(new URL('../preview/jerusalem-3000/data/landmark-building-programme.v1.json',import.meta.url),'utf8')]);
const report=JSON.parse(raw),programme=JSON.parse(programmeRaw),entities=new Map(programme.entities.map(e=>[e.id,e]));
assert.equal(report.rows.length,18);assert.equal(programme.phases.length,18);
const phases=report.rows.map((row,i)=>{
 const planned=programme.phases[i],actual=row.landmarks;assert.equal(row.foundation.phaseId,planned.phase);assert.equal(actual.phase,planned.phase);
 assert.equal(actual.visibleModelAnchors.length,row.foundation.renderer.visibleLandmarkIds.length);assert.equal(actual.historicalGeometryAccepted,false);
 const visible=new Set(actual.visibleModelAnchors.map(a=>a.id));assert.equal(visible.size,actual.visibleModelAnchors.length);
 const monuments=new Set(actual.visibleModelAnchors.filter(a=>a.kind==='monument').map(a=>a.id));assert.ok(actual.visibleModelAnchors.every(a=>['monument','gate'].includes(a.kind)));assert.deepEqual([...visible].sort(),[...row.foundation.renderer.visibleLandmarkIds].sort());
 const groups=planned.buildingGroups.map(group=>({id:group.id,label:group.label,members:group.members.map(member=>{
  const entity=entities.get(member.landmarkId);assert.ok(entity);
  const ids=entity.existingRuntimeIds||[],matches=ids.filter(id=>visible.has(id));
  return {id:entity.id,label:entity.label,kind:entity.kind,intendedState:member.intendedState,visibleLandmarkIds:matches,visibleMonumentIds:matches.filter(id=>monuments.has(id)),status:matches.length?'existing-illustration-not-accepted-reconstruction':'not-matched-in-visible-landmark-layer',historicalGeometryAccepted:false};
 })}));
 return {phase:planned.phase,label:planned.label,groups,visibleLandmarkIds:[...visible],visibleMonumentIds:[...monuments],matchedCandidates:groups.flatMap(g=>g.members).filter(m=>m.visibleLandmarkIds.length).map(m=>m.id),unmatchedCandidates:groups.flatMap(g=>g.members).filter(m=>!m.visibleLandmarkIds.length).map(m=>m.id),foundationAccepted:false};
});
const hash=s=>createHash('sha256').update(s).digest('hex');
const audit={schema:'j3k.landmark-execution-audit.v2',renderBaselineCommit:options['--render-commit'],reportSha256:hash(raw),programmeSha256:hash(programmeRaw),scope:'planned-groups-compared-with-actually-visible-monuments-and-designated-gates-not-full-water-road-or-place-coverage',historicalGeometryAccepted:false,phases};
const lines=['# 全18期標誌性建築量體對照','','以實際可見公共核心與指定城門量體對照候選清單；對應既有示意不等於復原完成。未在此層對應不表示水工、城牆、場所或道路不存在。不能用住宅數量補足地標缺口。','',`渲染基準：${audit.renderBaselineCommit}；輸入與清單雜湊見JSON。`,'','| 時期 | 已顯示地標量體（含指定城門） | 候選群中有示意對應 | 尚未在此層對應 |','| --- | ---: | ---: | ---: |'];
for(const p of phases)lines.push(`| ${p.label} | ${p.visibleLandmarkIds.length} | ${p.matchedCandidates.length} | ${p.unmatchedCandidates.length} |`);
for(const p of phases){lines.push('',`## ${p.label}`,'');for(const group of p.groups)lines.push(`- ${group.label}：${group.members.map(m=>`${m.label}（${m.visibleLandmarkIds.length?'已有示意量體，待核定':'未在地標量體層對應'}）`).join('；')}。`);}
lines.push('','全18期均保留歷史幾何未驗收；不同時期不要求有相同數量的建築。最早聚落沒有可核定具名地標時，不為湊數新增王宮或神廟。','');
const out=resolve(options['--out']);await mkdir(dirname(out),{recursive:true});await writeFile(out+'.json',JSON.stringify(audit,null,2)+'\n');await writeFile(out+'.md',lines.join('\n'));
console.log(JSON.stringify({phases:phases.length,visibleLandmarks:phases.map(p=>({phase:p.phase,count:p.visibleLandmarkIds.length})),historicalGeometryAccepted:false}));
