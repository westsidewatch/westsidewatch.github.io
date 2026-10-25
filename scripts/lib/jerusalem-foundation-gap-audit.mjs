import assert from 'node:assert/strict';
const SPATIAL=['districts','routes','waterDefense','sacredCivic'];
const DOMAINS=[...SPATIAL,'occupation','lifecycle'];
const count=n=>{assert.ok(Number.isInteger(n)&&n>=0,'counts must be nonnegative integers');return n;};
export function buildFoundationGapAudit({plan,timeline,report,provenance}){
 assert.deepEqual(plan.domains,DOMAINS);const ids=timeline.phases.map(p=>p.id);
 assert.equal(ids.length,18);assert.equal(new Set(ids).size,18);assert.deepEqual(plan.phases.map(p=>p.id),ids);
 assert.equal(plan.transitions.length,17);assert.equal(report.phaseReports?.length,18);
 assert.match(provenance?.renderBaselineCommit||'',/^[a-f0-9]{7,40}$/);for(const key of ['reportSha256','planSha256'])assert.match(provenance[key]||'',/^[a-f0-9]{64}$/);
 const phases=report.phaseReports.map((sample,i)=>{
  const f=sample.foundation,s=sample.spatialSkeleton,definition=plan.phases[i];
  assert.equal(f.phaseId,ids[i]);assert.equal(sample.time.phase,ids[i]);assert.equal(s.phaseId,ids[i]);
  assert.equal(f.active,true);assert.equal(s.evidenceMode,'all');assert.equal(Math.floor(s.position),i);assert.equal(s.position,sample.value);assert.equal(f.position,s.position);
  assert.equal(f.terrain.sampling,'rendered-dem-triangles');assert.equal(s.terrain,'modern-dem-rendered-triangles');assert.equal(f.foundationAccepted,false);assert.equal(f.registrationAccounting.visibleScopeAccounted,true);
  assert.deepEqual(s.window,plan.spatialSkeletonView.windowMetres,'capture window must match reviewed plan');
  assert.equal(new Set(s.features.map(f=>f.id)).size,s.features.length,'map IDs must be unique across domains');assert.ok(s.features.every(f=>typeof f.id==='string'&&f.id&&SPATIAL.includes(f.domain)));
  const domains={};for(const key of SPATIAL){
   const inventory=f.domains[key],spatial=s.domains[key];assert.ok(inventory&&spatial);const registered=count(inventory.registeredObjects),active=count(spatial.activeObjects),mapped=count(spatial.spatialObjects);
   assert.ok(mapped<=active&&active<=registered);assert.equal(spatial.gapIds.length,active-mapped);assert.equal(new Set(spatial.gapIds).size,spatial.gapIds.length);
   assert.ok(count(inventory.visibleBoundObjects)<=registered);
   const features=s.features.filter(feature=>feature.domain===key);assert.equal(features.length,mapped);assert.equal(new Set(features.map(feature=>feature.id)).size,mapped);
   domains[key]={reviewStatus:definition.domains[key],registered,activeMappedScope:active,mapped,activeWithoutGeometryIds:[...spatial.gapIds].sort(),visibleBound:count(inventory.visibleBoundObjects),finding:!registered?'no-registered-domain':active>mapped?'active-geometry-gap':mapped?'mapped-partial-scope':'registered-no-active-map-representation'};
  }
  const life=f.domains.lifecycle;
  domains.occupation={reviewStatus:definition.domains.occupation,registered:count(f.domains.occupation.registeredObjects),visibleBound:count(f.domains.occupation.visibleBoundObjects),layoutEnvelope:s.layoutEnvelope?structuredClone(s.layoutEnvelope):null,finding:'registered-model-envelope-not-historical-occupation-boundary'};
  domains.lifecycle={reviewStatus:definition.domains.lifecycle,registeredWithEvents:count(life.registeredObjects),declaredContextScopes:count(life.explicitEventScopes),unclassified:count(life.unclassifiedWithoutDeclaredEvents),states:structuredClone(life.states),finding:'existing-event-accounting-not-historical-lineage-acceptance'};
  assert.equal(domains.lifecycle.unclassified,0);assert.equal(f.renderer.outOfPhaseBindingIds.length,0);
  return {id:ids[i],label:timeline.phases[i].label,owner:f.owner,domains,visibleComponents:count(f.renderer.visibleComponents),unboundComponents:count(f.renderer.unboundComponents),annotationComponents:count(f.renderer.displayAnnotationComponents),provisionalInheritedComponents:count(f.renderer.provisionalInheritedComponents),scope:definition.gap,historicalFoundationAccepted:false};
 });
 const transitions=plan.transitions.map((t,i)=>{
  assert.equal(t.from,ids[i]);assert.equal(t.to,ids[i+1]);
  const before=new Set(report.phaseReports[i].spatialSkeleton.features.map(f=>f.id)),after=new Set(report.phaseReports[i+1].spatialSkeleton.features.map(f=>f.id));
  return {from:t.from,to:t.to,reviewStatus:t.status,sharedMappedIds:[...before].filter(id=>after.has(id)).sort(),sourceOnlyMappedIds:[...before].filter(id=>!after.has(id)).sort(),targetOnlyMappedIds:[...after].filter(id=>!before.has(id)).sort(),interpretation:'map-ID-presence-only-not-retain-build-demolish-or-reuse-events',historicalTransitionAccepted:false,requiredReview:['dated-source-scope','persistent-new-ruin-withdraw-unknown-object-fates','geometry-validity-and-ground','exact-forward-backward-projection'],evidence:structuredClone(t.acceptanceEvidence)};
 });
 const flags={withoutRegisteredDistricts:phases.filter(p=>p.domains.districts.registered===0).map(p=>p.id),withActiveGeometryGaps:phases.filter(p=>SPATIAL.some(d=>p.domains[d].activeWithoutGeometryIds.length)).map(p=>p.id),withoutMappedWaterDefense:phases.filter(p=>p.domains.waterDefense.mapped===0).map(p=>p.id),withoutMappedSacredCivic:phases.filter(p=>p.domains.sacredCivic.mapped===0).map(p=>p.id)};
 const review=plan.sourceSpatialBindingReview;
 if(review){assert.equal(review.status,'reviewed-with-deferred-geometry');assert.ok(review.evidence);const mapped=new Set(report.phaseReports.flatMap(r=>r.spatialSkeleton.features.map(f=>f.id))),deferred=new Set(review.deferredGeometryIds);assert.ok(review.registeredSourceZoneIds.every(id=>mapped.has(id)),'reviewed source zones must appear in capture');assert.ok(phases.every(p=>SPATIAL.every(d=>p.domains[d].activeWithoutGeometryIds.every(id=>deferred.has(id)))),'new geometry gaps require an updated decision');}
 return {schema:'j3k.foundation-gap-audit.v1',scope:'engineering-spatial-inventory-not-historical-completeness',provenance:structuredClone(provenance),capturePolicy:'sequential-all-evidence-active-snapshots; registered counts include unresolved records and may depend on prior generation; not city size',window:{...plan.spatialSkeletonView.windowMetres},phases,transitions,flags,
 priorities:[
  {id:'existing-spatial-bindings',order:1,dependsOn:[],phases:flags.withActiveGeometryGaps,deliverable:'先核對已登記分區、道路、水防及核心的幾何與分類；明確暫緩定位的對象保持缺口，避免重建已有模型。',gate:'每項具備適用來源的可用幾何，或明確暫緩決定；驗證場景／地圖身分與篩選恢復。'},
  {id:'early-period-districts',order:2,dependsOn:['existing-spatial-bindings'],phases:ids.slice(0,4),deliverable:'統一最早聚落至大衛—所羅門四期的分區、路徑與佔用範圍，各期保留獨立年代與地形關係。',gate:'零登記不等於歷史不存在；範圍、年代和未知邊界均需明示。'},
  {id:'hellenistic-independent-foundation',order:3,dependsOn:['early-period-districts'],phases:['hellenistic-hasmonean'],deliverable:'以獨立來源約束分區、入口及公共核心，替換希臘化時期的參考城衍生骨架。',gate:'不能把縮放希律城或複製圍牆作為本期依據。'},
  {id:'later-water-civic-foundations',order:4,dependsOn:['existing-spatial-bindings'],phases:ids.slice(10,16),deliverable:'成組規劃Aelia至鄂圖曼六期的防禦、水系與公共核心，再進入建築深化。',gate:'預留空區不算完成核心；城牆年代及座標依據必須明確。'},
  {id:'modern-coverage',order:5,dependsOn:['later-water-civic-foundations'],phases:ids.slice(16),deliverable:'成對補足城外擴張／現代的東部及遠端地區與交通脈絡，明示各層年代範圍。',gate:'西側局部窗口不算完整城市，也不代表政治邊界。'},
  {id:'adjacent-transition-acceptance',order:6,dependsOn:['early-period-districts','hellenistic-independent-foundation','later-water-civic-foundations','modern-coverage'],phases:ids,deliverable:'逐段審核17段接續的保留、新建、毀壞、退出與未知去向，驗證反向還原。',gate:'共同ID、外觀相似、原型保留百分比或切換測試均不能證明歷史存續。'}
 ],nextPackage:review?'early-period-districts':'existing-spatial-bindings',sourceSpatialBindingReview:review?structuredClone(review):null,detailWork:'paused-until-foundation-review-accepted',historicalFoundationAccepted:false};
}
const NAMES={'existing-spatial-bindings':'既有對象定位與分類','early-period-districts':'早期四期分區基礎','hellenistic-independent-foundation':'希臘化獨立骨架','later-water-civic-foundations':'後期六期水防與公共核心','modern-coverage':'現代覆蓋範圍','adjacent-transition-acceptance':'17段接續驗收'};
export function renderFoundationGapMarkdown(audit){
 const lines=['# Jerusalem 3000：18期／17段空間缺口矩陣','',`渲染基準：\`${audit.provenance.renderBaselineCommit}\`。此表是工程盤點；整體歷史基礎尚未驗收，建築細雕暫停。`,'','數字 `登記／地圖` 表示帳本登記數／當前有效且可定位的骨架圖對象。帳本可能含前期留下的未明去向記錄，並受逐期生成順序影響，不能當作城市規模。地圖為零不代表建築不存在；公共核心欄只盤點目前 monument 分類，不能涵蓋所有建築語義。','',`共同地圖窗口：X[${audit.window.minX},${audit.window.maxX}]、Z[${audit.window.minZ},${audit.window.maxZ}] 公尺；使用現代DEM，非古地表。`,'','## 18期空間矩陣','','| 時期 | 分區 | 路徑 | 水防 | 公共核心 | 佔用可見綁定 | 未明事件 | 主動對象缺少幾何 |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |'];
 for(const p of audit.phases)lines.push(`| ${p.label} | ${SPATIAL.map(d=>`${p.domains[d].registered}／${p.domains[d].mapped}`).join(' | ')} | ${p.domains.occupation.visibleBound} | ${p.domains.lifecycle.states.unresolved||0} | ${SPATIAL.reduce((n,d)=>n+p.domains[d].activeWithoutGeometryIds.length,0)} |`);
 lines.push('','佔用可見綁定是已登記 block／parcel／building 的模型數，不是歷史住宅數。事件未明是現有事件投影狀態，不等同於未綁定或資料錯誤。完整對象ID、分類與幾何缺口見 JSON。每期六域的審核狀態保留自計劃，數量不自動提升驗收。','', '## 優先順序與交付門檻','');
 for(const p of audit.priorities)lines.push(`${p.order}. **${NAMES[p.id]}**（${p.id}）— ${p.deliverable} 驗收門檻：${p.gate}`);
 lines.push('',audit.sourceSpatialBindingReview?'既有區位核對已完成，來源要求暫緩的對象仍保留缺口。下一包：**early-period-districts**，早期四期分區／路徑／佔用基礎。':'下一包：先處理 **existing-spatial-bindings**，核對既有核心與水防的定位／分類；有來源才補定位，明確 withheld 的對象繼續保留缺口。','', '## 17段相鄰接續','','下面只比較四類骨架圖對象ID的出現。共同ID不等於已證明存續，僅前期／僅後期不等於拆除／新建；不含全部佔用或不可定位對象。所有接續歷史驗收仍為 false。','','| 接續 | 共同地圖ID | 僅前期 | 僅後期 | 審核狀態 |','| --- | ---: | ---: | ---: | --- |');
 for(const t of audit.transitions)lines.push(`| ${t.from} → ${t.to} | ${t.sharedMappedIds.length} | ${t.sourceOnlyMappedIds.length} | ${t.targetOnlyMappedIds.length} | ${t.reviewStatus} |`);
 lines.push('','17段都需檢查有年代的來源、具體對象去向、地形／幾何適用期和正反向投影；既有17條舊繼承規則與局部反向測試不能代替這項驗收。','', '## 各期範圍與缺口','');
 for(const p of audit.phases)lines.push(`- **${p.label}**：${p.scope}`);
 lines.push('','## 重製','','先執行全18期瀏覽器檢查，再以報告生成矩陣：','','```sh','node scripts/audit_jerusalem_3000_foundation_gaps.mjs --report work/j3k-validation/phase-report.json --render-commit <captured-render-commit> --out work/j3k-validation/foundation-gap-audit','```','','輸入報告與計劃的 SHA-256 記錄於 JSON；這是固定基準快照，不是假定永遠最新的即時狀態。CI 會從當次瀏覽器報告產出新矩陣，不額外載入網站資料或生成場景。','');
 return lines.join('\n');
}
