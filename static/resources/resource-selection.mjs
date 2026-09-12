import {policy,reviews} from './selection-data.mjs';
const norm=v=>String(v??'').normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();
const decode=v=>{try{return decodeURIComponent(String(v??''))}catch{return String(v??'')}};
const urlnorm=v=>decode(v).replaceAll('_',' ').replace(/\/$/,'');
function identity(item){return {title:item.work?.title||item.title||item.name||'',urls:[...(Array.isArray(item.sources)?item.sources:[]).map(s=>s?.url),item.source?.url,item.sourceUrl,item.url].filter(Boolean).map(urlnorm)}}
export function resourceExcluded(item={}){
 const text=norm(decode(JSON.stringify(Object.fromEntries(['id','title','name','name_en','description','work','sourceUrl','url','topics','subject','categories','source','sources'].map(k=>[k,item[k]])))));
 const topics=Array.isArray(item.topics)?item.topics:[item.topics];
 return item.controversial===true||['rejected','controversial','excluded'].includes(item.contentReview)||policy.withdrawnIds.some(v=>text.includes(v))||topics.some(t=>policy.excludedTopics.includes(t))||policy.excludedPatterns.some(p=>new RegExp(p,'i').test(text));
}
export function bookDecision(item={}){
 if(resourceExcluded(item))return {status:'excluded',reason:'content-boundary'};
 if(item.completeWork===false)return {status:'excluded',reason:'not-a-complete-book'};
 const {title,urls}=identity(item),kind=item.resourceType||item.work?.type||item.kind;
 if(policy.nonBookKinds.includes(kind)||policy.nonBookPatterns.some(p=>new RegExp(p,'i').test(norm(title))))return {status:'excluded',reason:'not-a-book'};
 const r=reviews.find(r=>r.titles.some(t=>norm(t)===norm(title))&&r.sourceUrls.some(u=>urls.includes(urlnorm(u))));
 if(!r)return {status:'hold',reason:'book-identity-and-content-review-required'};
 if(!(r.status==='approved'&&r.contentReview==='approved'&&r.completeWork===true&&policy.acceptedBookKinds.includes(r.kind)&&r.creatorOrTranslation&&r.editionEvidence&&r.scope))return {status:'hold',reason:'incomplete-review'};
 return {status:'approved',reason:'reviewed-complete-book',policyVersion:policy.version,kind:r.kind};
}
export const bookAllowed=item=>bookDecision(item).status==='approved';

export function selectedReferenceAllowed(book={}){return book.library?.intake!=='dawn-reference'||bookAllowed({work:book.identity?.work||{title:book.title},sources:book.sources||[],controversial:book.controversial,contentReview:book.contentReview})}
