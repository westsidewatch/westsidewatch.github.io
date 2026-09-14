// DORÉ 成書 autopilot: automated stages stay headless; only human decisions surface.
import { buildPublicationArtifacts } from './book-artifact-build.mjs';
import { requestCoreCover } from './book-cover-client.mjs';
import { admitSourceUses } from './source-capability-admission.mjs';
const SCHEMA='dore.book-publishing-autopilot.v2';
function needsHuman(editorialReport={}){const decisions=Number(editorialReport?.counts?.authorialDecisions||0);return editorialReport?.readiness==='blocked'||decisions>0}
function deriveArtDirection(bookModel={}){const intent=bookModel.intent||{},existing=bookModel.design?.artDirection;if(existing)return existing;return{id:`auto-${bookModel.id||bookModel.workId||'book'}`,mode:'automatic',visualTone:intent.visualTone||'quiet-editorial',illustrationDensity:intent.illustrationDensity||'low',readingMode:intent.readingMode||'continuous',source:'book-intent'}}
export async function runPublishingAutopilot({bookModel,bookBuild,intelligenceReport,editorialReport,sourceUses=[]}={}){
 if(!bookModel||!bookBuild)throw new Error('BookModel and BookBuild are required.');
 const sourceAdmission=admitSourceUses(sourceUses);
 bookModel.internalProvenance={...(bookModel.internalProvenance||{}),sourceCapabilityAdmission:{schema:sourceAdmission.schema,status:sourceAdmission.status,counts:sourceAdmission.counts,rows:sourceAdmission.rows}};
 const sourceBlocked=sourceAdmission.status==='blocked',sourceDeferred=sourceAdmission.status==='deferred';
 const human=needsHuman(editorialReport),artDirection=deriveArtDirection(bookModel);
 bookModel.design={...(bookModel.design||{}),artDirection};bookBuild.artDirectionId=artDirection.id||'';
 const handoff=human?{required:true,kind:'authorial-decision',count:Number(editorialReport?.counts?.authorialDecisions||editorialReport?.counts?.issues||1),message:'有內容需要作者決定後才能繼續成書。'}:null;
 let coverResult=null,artifacts=null,acceptance=null;
 if(!human&&!sourceBlocked&&!sourceDeferred){coverResult=await requestCoreCover(bookModel);if(coverResult?.artifact)bookModel.design={...(bookModel.design||{}),cover:coverResult.artifact};artifacts=buildPublicationArtifacts({bookModel,bookBuild,requireCover:true});acceptance={status:artifacts.qa.status,artifactSet:artifacts.schema,checks:{...artifacts.qa.checks,coverGenerated:Boolean(coverResult?.artifact)},coverRuntime:coverResult?.source||'none'};bookModel.validation={...bookModel.validation,status:acceptance.status,gates:[...(bookModel.validation?.gates||[]),{id:'source-capability-admission',status:'pass'},{id:'publication-artifacts',status:acceptance.status}]};bookBuild.qaResult={...bookBuild.qaResult,status:acceptance.status,publicationAcceptance:acceptance};if(acceptance.status==='pass')bookBuild.publishedAt=new Date().toISOString()}
 else if(sourceBlocked||sourceDeferred){bookModel.validation={...bookModel.validation,status:'blocked',gates:[...(bookModel.validation?.gates||[]),{id:'source-capability-admission',status:sourceBlocked?'blocked':'deferred'}]};bookBuild.qaResult={...bookBuild.qaResult,status:'blocked',sourceCapabilityAdmission:sourceAdmission}}
 const state=human?'waiting-for-human':sourceDeferred?'waiting-for-source-capability':sourceBlocked?'blocked':acceptance?.status==='pass'?'built':'blocked';
 const completed=human?['understanding','editorial','visual-direction','build-preparation']:sourceBlocked||sourceDeferred?['understanding','editorial','visual-direction','source-capability-admission']:['understanding','editorial','visual-direction','source-capability-admission','formal-cover','artifact-build','publication-acceptance'];
 const next=human?'authorial-decision':sourceDeferred?'source-runtime-resolution':sourceBlocked?'source-admission-repair':acceptance?.status==='pass'?'materialize-artifacts':'artifact-repair';
 const result={schema:SCHEMA,state,humanHandoff:handoff,sourceCapabilityAdmission:sourceAdmission,bookModel,bookBuild,intelligenceReport,editorialReport,coverResult,artifacts,publicationAcceptance:acceptance,completedHeadlessStages:completed,next};
 window.__dorePublishingAutopilot=result;window.dispatchEvent(new CustomEvent(human?'multiwrite:publishing-human-handoff':acceptance?.status==='pass'?'multiwrite:publication-accepted':'multiwrite:publishing-autopilot-blocked',{detail:result}));return result}
export {SCHEMA as BOOK_PUBLISHING_AUTOPILOT_SCHEMA};
