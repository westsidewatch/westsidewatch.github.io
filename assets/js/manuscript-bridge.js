/* Westside Watch Manuscript Bridge
 * Shared, dependency-free reader/edit coordination layer.
 * Keeps long Markdown addressable by heading/range without coupling consumers
 * to a CMS or to a specific reader UI.
 */
(function (global) {
  'use strict';

  const VERSION = '1.1.0';

  function normalize(text) { return String(text || '').replace(/\r\n?/g, '\n'); }
  function slug(text) {
    return String(text || '').replace(/[*_`~[\]()]/g, '').trim().toLowerCase()
      .replace(/\s+/g, '-').replace(/[^\p{L}\p{N}\-]+/gu, '').replace(/-+/g, '-');
  }
  function hash(text) {
    let h = 2166136261;
    const s = normalize(text);
    for (let i=0;i<s.length;i++) { h ^= s.charCodeAt(i); h = Math.imul(h,16777619); }
    return (h>>>0).toString(16).padStart(8,'0');
  }
  function headings(text) {
    const lines=normalize(text).split('\n'),out=[];
    lines.forEach((line,index)=>{const m=line.match(/^(#{1,6})\s+(.+?)\s*$/);if(!m)return;out.push({level:m[1].length,title:m[2].replace(/[*_`]/g,'').trim(),raw:line,line:index+1,index,id:slug(m[2])});});
    return out;
  }
  function section(text,selector) {
    const source=normalize(text),lines=source.split('\n'),hs=headings(source),wanted=typeof selector==='string'?{title:selector}:(selector||{});
    const matches=hs.filter(h=>(wanted.id&&h.id===wanted.id)||(wanted.title&&h.title===wanted.title)||(wanted.line&&h.line===Number(wanted.line)));
    if(!matches.length)return null;
    const occurrence=Math.max(1,Number(wanted.occurrence)||1),start=matches[occurrence-1]; if(!start)return null;
    const next=hs.find(h=>h.index>start.index&&h.level<=start.level),endIndex=next?next.index:lines.length;
    const body=lines.slice(start.index,endIndex).join('\n').replace(/\n+$/,'')+'\n';
    return {heading:start,startLine:start.line,endLine:endIndex,text:body,hash:hash(body)};
  }
  function range(text,startSelector,endSelector) {
    const source=normalize(text),lines=source.split('\n'),start=section(source,startSelector); if(!start)return null;
    let endLine=start.endLine;
    if(endSelector){const end=section(source,endSelector);if(!end||end.startLine<=start.startLine)throw new Error('Invalid manuscript end selector');endLine=end.startLine-1;}
    const body=lines.slice(start.startLine-1,endLine).join('\n').replace(/\n+$/,'')+'\n';
    return {heading:start.heading,startLine:start.startLine,endLine,text:body,hash:hash(body)};
  }
  function replaceRange(text,target,replacement,expectedHash) {
    const source=normalize(text),part=target&&target.end?range(source,target.start,target.end):section(source,target&&target.start?target.start:target);
    if(!part)throw new Error('Manuscript range not found');
    if(expectedHash&&part.hash!==expectedHash)throw new Error(`Manuscript range changed (${part.hash} != ${expectedHash})`);
    const lines=source.split('\n'),before=lines.slice(0,part.startLine-1),after=lines.slice(part.endLine),insert=normalize(replacement).replace(/^\n+|\n+$/g,'').split('\n');
    return {text:[...before,...insert,...after].join('\n').replace(/\n{3,}/g,'\n\n'),previous:part,insertedHash:hash(insert.join('\n')+'\n')};
  }
  function replaceSection(text,selector,replacement,expectedHash){return replaceRange(text,{start:selector},replacement,expectedHash).text;}
  function patchPlan(text,target,replacement){const source=normalize(text),part=target&&target.end?range(source,target.start,target.end):section(source,target&&target.start?target.start:target);if(!part)throw new Error('Manuscript range not found');return {target,expectedHash:part.hash,startLine:part.startLine,endLine:part.endLine,before:part.text,replacement:normalize(replacement).replace(/^\n+|\n+$/g,'')+'\n'};}
  function applyPlan(text,plan){return replaceRange(text,plan.target,plan.replacement,plan.expectedHash);}
  function sourceWithRevision(url,revision){const u=new URL(url,global.location&&global.location.href||undefined);u.searchParams.set('_rev',revision||Date.now().toString(36));return u.toString();}
  async function read(url,options){const opts=options||{},target=opts.fresh===false?url:sourceWithRevision(url,opts.revision),response=await fetch(target,{cache:opts.fresh===false?'default':'no-store'});if(!response.ok)throw new Error(`Manuscript read failed (${response.status})`);const text=normalize(await response.text());return{text,headings:headings(text),hash:hash(text),url};}
  function rememberPosition(key){if(!global.sessionStorage)return;global.sessionStorage.setItem(`manuscript:${key}:position`,JSON.stringify({y:global.scrollY||0,at:Date.now()}));}
  function restorePosition(key){if(!global.sessionStorage)return false;const raw=global.sessionStorage.getItem(`manuscript:${key}:position`);if(!raw)return false;try{const saved=JSON.parse(raw);requestAnimationFrame(()=>global.scrollTo(0,Number(saved.y)||0));return true}catch(_){return false}}
  function nearestHeading(root){if(!root)return null;const hs=[...root.querySelectorAll('h1,h2,h3,h4,h5,h6')];let current=null;for(const h of hs){if(h.getBoundingClientRect().top<=Math.max(120,global.innerHeight*.28))current=h;else break}return current?{title:current.textContent.trim(),id:current.id||slug(current.textContent)}:null;}
  function rememberAnchor(key,root){const anchor=nearestHeading(root);if(!anchor||!global.sessionStorage)return rememberPosition(key);global.sessionStorage.setItem(`manuscript:${key}:anchor`,JSON.stringify(anchor));rememberPosition(key);}
  function restoreAnchor(key,root){if(!global.sessionStorage||!root)return restorePosition(key);const raw=global.sessionStorage.getItem(`manuscript:${key}:anchor`);if(!raw)return restorePosition(key);try{const saved=JSON.parse(raw),target=[...root.querySelectorAll('h1,h2,h3,h4,h5,h6')].find(h=>(h.id&&h.id===saved.id)||h.textContent.trim()===saved.title);if(!target)return restorePosition(key);requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));return true}catch(_){return restorePosition(key)}}
  global.ManuscriptBridge=Object.freeze({version:VERSION,normalize,slug,hash,headings,section,range,replaceSection,replaceRange,patchPlan,applyPlan,sourceWithRevision,read,rememberPosition,restorePosition,rememberAnchor,restoreAnchor});
})(window);
