(()=>{
"use strict";
// Mark mixed editorial labels by script, without touching Scripture text or user input.
const selectors=".note-ref,.note-caption,.edition,.coord,.unit figcaption,.note-coordinate,.sticky-reference,.booklist button";
function format(root){for(const e of root.querySelectorAll(selectors)){for(const node of [...e.childNodes]){if(node.nodeType!==Node.TEXT_NODE||!node.data.trim()||!/[A-Za-z0-9]/.test(node.data))continue;const parts=node.data.match(/[A-Za-z0-9À-ÖØ-öø-ÿ]+(?:[ .,:;–—&'’/\-]+[A-Za-z0-9À-ÖØ-öø-ÿ]+)*|[^A-Za-z0-9À-ÖØ-öø-ÿ]+/g)||[];if(!parts.length)continue;const frag=document.createDocumentFragment();for(const part of parts){if(/[A-Za-z0-9]/.test(part)){const span=document.createElement("span");span.lang="en";span.textContent=part;frag.append(span)}else frag.append(document.createTextNode(part))}node.replaceWith(frag)}}}
const root=document.querySelector(".workspace");let scheduled=false;const run=()=>{scheduled=false;format(root)};new MutationObserver(()=>{if(!scheduled){scheduled=true;queueMicrotask(run)}}).observe(root,{childList:true,subtree:true});run();
})();