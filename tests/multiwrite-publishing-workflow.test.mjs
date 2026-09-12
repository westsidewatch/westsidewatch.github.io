import test from 'node:test';
import assert from 'node:assert/strict';
import {createPublishingWorkflow,workflowFromCompile} from '../static/multiwrite/publishing-workflow.mjs';

test('publishing workflow starts at whole-book understanding',()=>{
 const w=createPublishingWorkflow();
 assert.equal(w.schema,'dore.publishing-workflow.v1');
 assert.equal(w.current,'understanding');
 assert.equal(w.steps.length,8);
 assert.equal(w.steps.at(-1).id,'publish');
});

test('authorial decisions stop workflow before art direction',()=>{
 const w=workflowFromCompile({intelligenceReport:{structure:{chapterCount:14},semantic:{runtime:{semantic:true,degraded:false}}},editorialReport:{readiness:'review-required',counts:{issues:2,authorialDecisions:1}}});
 assert.equal(w.current,'author-decision');
 assert.equal(w.blocked,true);
 assert.equal(w.summary.chapters,14);
 assert.equal(w.steps.find(x=>x.id==='art-direction').status,'locked');
});

test('clean editorial result advances to Doré art direction',()=>{
 const w=workflowFromCompile({intelligenceReport:{structure:{chapterCount:3},semantic:{runtime:{semantic:true,degraded:false}}},editorialReport:{readiness:'ready',counts:{issues:0,authorialDecisions:0}}});
 assert.equal(w.current,'art-direction');
 assert.equal(w.blocked,false);
 assert.equal(w.steps.find(x=>x.id==='editorial').status,'complete');
 assert.equal(w.steps.find(x=>x.id==='art-direction').status,'active');
});
