(()=>{
  const han=/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/g;
  const latin=/[A-Za-z]/g;
  const selector='h1,h2,h3,h4,p,li,a,span,strong,b,em,small,blockquote,cite,button,label';
  const classify=root=>{
    for(const el of root.querySelectorAll(selector)){
      if(el.closest('svg,script,style,template')||el.classList.contains('type-en')||el.classList.contains('type-zh')||el.classList.contains('type-mixed'))continue;
      const direct=[...el.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent).join(' ').trim();
      if(!direct)continue;
      const h=(direct.match(han)||[]).length,l=(direct.match(latin)||[]).length;
      if(h&&l)el.classList.add(h>=l*.45?'type-mixed':'type-en');
      else if(h)el.classList.add('type-zh');
      else if(l)el.classList.add('type-en');
    }
  };
  const start=()=>{
    classify(document);
    new MutationObserver(records=>{for(const record of records)for(const node of record.addedNodes)if(node.nodeType===Node.ELEMENT_NODE)classify(node)}).observe(document.body,{childList:true,subtree:true});
  };
  document.readyState==='loading'?document.addEventListener('DOMContentLoaded',start,{once:true}):start();
})();
