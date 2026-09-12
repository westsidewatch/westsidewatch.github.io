const SCHEMA='dore.publishing-workflow.v1';
const STEPS=[
 ['understanding','理解全書'],
 ['editorial','編輯檢查'],
 ['author-decision','作者決定'],
 ['art-direction','美術總監'],
 ['cover','正式封面'],
 ['build','出版構建'],
 ['validation','出版驗收'],
 ['publish','黎明書局']
];

function statusFor(step,index,currentIndex,blocked){
 if(blocked&&index>currentIndex)return 'locked';
 if(index<currentIndex)return 'complete';
 if(index===currentIndex)return blocked?'blocked':'active';
 return 'pending';
}

export function createPublishingWorkflow(){
 return {schema:SCHEMA,state:'idle',current:'understanding',blocked:false,steps:STEPS.map(([id,label])=>({id,label,status:'pending'})),updatedAt:new Date().toISOString()};
}

export function workflowFromCompile({intelligenceReport,editorialReport}={}){
 const authorial=Number(editorialReport?.counts?.authorialDecisions||0);
 const issues=Number(editorialReport?.counts?.issues||0);
 const blocked=editorialReport?.readiness==='blocked'||authorial>0;
 const current=editorialReport?.readiness==='blocked'?'editorial':authorial>0?'author-decision':'art-direction';
 const currentIndex=Math.max(0,STEPS.findIndex(([id])=>id===current));
 return {
  schema:SCHEMA,
  state:blocked?'waiting':'ready',
  current,
  blocked,
  summary:{chapters:Number(intelligenceReport?.structure?.chapterCount||0),issues,authorialDecisions:authorial,semantic:intelligenceReport?.semantic?.runtime?.semantic===true,degraded:intelligenceReport?.semantic?.runtime?.degraded!==false},
  steps:STEPS.map(([id,label],index)=>({id,label,status:statusFor(id,index,currentIndex,blocked)})),
  updatedAt:new Date().toISOString()
 };
}

export {SCHEMA as PUBLISHING_WORKFLOW_SCHEMA,STEPS as PUBLISHING_WORKFLOW_STEPS};
