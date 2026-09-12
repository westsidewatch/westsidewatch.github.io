import {compileCurrentBook} from './book-compile-bridge.mjs';
import {createPublishingWorkflow,workflowFromCompile} from './publishing-workflow.mjs';

let root=null;
function esc(v=''){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]))}
function stepMarkup(step){return `<li class="publish-step is-${step.status}" data-step="${esc(step.id)}"><span class="publish-step-mark"></span><span>${esc(step.label)}</span><small>${step.status==='complete'?'完成':step.status==='active'?'進行中':step.status==='blocked'?'需處理':step.status==='locked'?'等待前置':'待開始'}</small></li>`}
function panelMarkup(workflow=createPublishingWorkflow()){
 const s=workflow.summary||{};
 const detail=workflow.state==='idle'?'從整書理解開始，建立真正的出版工作流。':`已理解 ${s.chapters||0} 章 · 編輯問題 ${s.issues||0} · 作者決定 ${s.authorialDecisions||0}`;
 return `<div class="publishing-workflow-backdrop" id="publishingWorkflow"><section class="publishing-workflow" role="dialog" aria-modal="true" aria-labelledby="publishingWorkflowTitle"><header><div><span class="publishing-kicker">DORÉ PUBLISHING WORKFLOW</span><h2 id="publishingWorkflowTitle">成書</h2><p>${esc(detail)}</p></div><button class="publishing-close" type="button" aria-label="關閉">×</button></header><ol class="publishing-steps">${workflow.steps.map(stepMarkup).join('')}</ol><div class="publishing-status">${workflow.blocked?'成書停在需要處理的關卡；不會越過作者決定自動出版。':'BookModel 是唯一出版狀態；DOCX / PDF 等將作為完成後的衍生輸出。'}</div><footer><button class="book-action" data-publishing-close type="button">稍後繼續</button><button class="book-action primary" data-publishing-start type="button">${workflow.state==='idle'?'開始成書':'重新檢查'}</button></footer></section></div>`;
}
function render(workflow){if(!root)return;const next=document.createElement('div');next.innerHTML=panelMarkup(workflow);const replacement=next.firstElementChild;root.replaceWith(replacement);root=replacement;bind()}
function close(){root?.remove();root=null}
function bind(){root.querySelector('.publishing-close').onclick=close;root.querySelector('[data-publishing-close]').onclick=close;root.addEventListener('click',e=>{if(e.target===root)close()});root.querySelector('[data-publishing-start]').onclick=async()=>{const button=root.querySelector('[data-publishing-start]');button.disabled=true;button.textContent='理解整部作品…';try{const compiled=await compileCurrentBook();render(workflowFromCompile(compiled))}catch(error){root.querySelector('.publishing-status').textContent=`成書檢查失敗：${error.message}`;button.disabled=false;button.textContent='重試'}}}
export function openPublishingWorkflow(){if(root)return;document.querySelector('#bookMenu')?.classList.remove('open');document.querySelector('#makeBook')?.setAttribute('aria-expanded','false');const holder=document.createElement('div');holder.innerHTML=panelMarkup();root=holder.firstElementChild;document.body.appendChild(root);bind()}
// The legacy 成書 menu remains the live user-facing entry point until the
// publishing workflow owns the complete path through artifact output. Do not
// intercept #makeBook here: export.js must retain DOCX/PDF/MD/TXT/JSON output.
window.addEventListener('multiwrite:open-publishing-workflow',openPublishingWorkflow);
