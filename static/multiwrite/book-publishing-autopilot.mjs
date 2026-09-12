// DORÉ 成書 autopilot: automated stages stay headless; only human decisions surface.
const SCHEMA='dore.book-publishing-autopilot.v1';

function needsHuman(editorialReport={}){
  const decisions=Number(editorialReport?.counts?.authorialDecisions||0);
  return editorialReport?.readiness==='blocked'||decisions>0;
}

function deriveArtDirection(bookModel={}){
  const intent=bookModel.intent||{};
  const existing=bookModel.design?.artDirection;
  if(existing)return existing;
  return {
    id:`auto-${bookModel.id||bookModel.workId||'book'}`,
    mode:'automatic',
    visualTone:intent.visualTone||'quiet-editorial',
    illustrationDensity:intent.illustrationDensity||'low',
    readingMode:intent.readingMode||'continuous',
    source:'book-intent'
  };
}

export function runPublishingAutopilot({bookModel,bookBuild,intelligenceReport,editorialReport}={}){
  if(!bookModel||!bookBuild)throw new Error('BookModel and BookBuild are required.');
  const human=needsHuman(editorialReport);
  const artDirection=deriveArtDirection(bookModel);
  bookModel.design={...(bookModel.design||{}),artDirection};
  bookBuild.artDirectionId=artDirection.id||'';
  const handoff=human?{
    required:true,
    kind:'authorial-decision',
    count:Number(editorialReport?.counts?.authorialDecisions||editorialReport?.counts?.issues||1),
    message:'有內容需要作者決定後才能繼續成書。'
  }:null;
  const result={
    schema:SCHEMA,
    state:human?'waiting-for-human':'automatic',
    humanHandoff:handoff,
    bookModel,
    bookBuild,
    intelligenceReport,
    editorialReport,
    completedHeadlessStages:['understanding','editorial','visual-direction','build-preparation'],
    next:human?'authorial-decision':'artifact-build'
  };
  window.__dorePublishingAutopilot=result;
  window.dispatchEvent(new CustomEvent(human?'multiwrite:publishing-human-handoff':'multiwrite:publishing-autopilot-ready',{detail:result}));
  return result;
}

export {SCHEMA as BOOK_PUBLISHING_AUTOPILOT_SCHEMA};