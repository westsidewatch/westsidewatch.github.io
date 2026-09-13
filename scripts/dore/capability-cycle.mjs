#!/usr/bin/env node
import fs from 'node:fs';
import { orchestrateDawnSurfaces } from './dawn-surface-orchestrator.mjs';

const selection={id:'capability-cycle',candidates:[
{visualWorkId:'engraving',score:.44,type:'engraving',surfacePresetIds:['card-8x5'],surfacePresets:[{id:'card-8x5',focalRegionId:'engraving-focus'}]},
{visualWorkId:'manuscript',score:.42,type:'manuscript-illumination',surfacePresetIds:['card-8x5'],surfacePresets:[{id:'card-8x5',focalRegionId:'manuscript-focus'}]},
{visualWorkId:'photo',score:.40,type:'photograph',surfacePresetIds:['card-8x5'],surfacePresets:[{id:'card-8x5',focalRegionId:null}]},
{visualWorkId:'painting',score:.39,type:'painting',surfacePresetIds:['card-8x5'],surfacePresets:[{id:'card-8x5',focalRegionId:'painting-focus'}]}
]};
const tasks=[
{id:'scripture',context:{pageIndex:2,pageCount:5,contentRole:'scripture-study',textDensity:.76,previousVisualWorkIds:['engraving'],previousVisualTypes:['engraving'],needsNegativeSpace:true},expected:'manuscript'},
{id:'witness',context:{pageIndex:3,pageCount:5,contentRole:'witness-story',textDensity:.3,previousVisualWorkIds:['engraving','manuscript'],previousVisualTypes:['engraving','manuscript-illumination']},expected:'photo'},
{id:'closing',context:{pageIndex:5,pageCount:5,contentRole:'prayer-closing',textDensity:.58,previousVisualWorkIds:['engraving','manuscript','photo'],previousVisualTypes:['engraving','manuscript-illumination','photograph'],needsNegativeSpace:true},expected:'painting'}
];
const baseline=orchestrateDawnSurfaces(selection).surfaces[0].visualWorkIds[0];
const results=tasks.map(t=>{const out=orchestrateDawnSurfaces(selection,t.context);const pick=out.surfaces[0].visualWorkIds[0];return{id:t.id,pick,expected:t.expected,pass:pick===t.expected,decision:out.surfaces[0].contextDecision};});
const passed=results.filter(x=>x.pass).length;
const judgmentDelta=passed/tasks.length;
const transfers=[
{from:'architecture-threshold',to:'page-entry',principle:'threshold'},
{from:'furniture-modularity',to:'responsive-components',principle:'modularity'},
{from:'film-sequence',to:'storybook-sequence',principle:'visual-progression'},
{from:'editorial-hierarchy',to:'church-surface-hierarchy',principle:'hierarchy'}
];
const gaps=[];
if(judgmentDelta<1) gaps.push('surface-judgment');
gaps.push('live-multi-surface-design-action','unseen-resource-transfer');
const report={schema:'dore.capability-cycle.v1',baseline:{hero:baseline,contextAware:false},nourished:{tasks:results,contextAware:true},capabilityDelta:{designJudgment:judgmentDelta,decisionChangeRate:results.filter(x=>x.pick!==baseline).length/tasks.length,crossDomainTransfer:transfers.length},transfers,curriculumGap:gaps,nextRound:{mode:'gap-directed',targets:gaps},claims:{humanVisualQuality:'unmeasured',pixelFidelity:'unmeasured',productionRelease:false}};
fs.writeFileSync('dore-capability-cycle-report.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
if(passed!==tasks.length) process.exitCode=2;
