/* One Look selector: shared interaction contract, realm-owned presentation. */
(()=>{'use strict';
 const roots=document.querySelectorAll('[data-ws-one-look-selector]');
 for(const root of roots){
  const cards=()=>[...root.querySelectorAll('[data-ws-one-look-card]:not([data-ws-one-look-clone])')];
  const choose=(card)=>{
   if(!card||card.hasAttribute('inert'))return;
   for(const item of cards())item.setAttribute('aria-pressed',String(item===card));
   root.dispatchEvent(new CustomEvent('ws-one-look:select',{bubbles:true,detail:{id:card.dataset.wsOneLookCard}}));
  };
  root.addEventListener('click',event=>{const card=event.target.closest('[data-ws-one-look-card]');if(card&&root.contains(card))choose(card)});
  root.addEventListener('keydown',event=>{
   if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
   const all=cards();if(!all.length)return;
   const active=event.target.closest('[data-ws-one-look-card]');if(!active||!root.contains(active))return;
   event.preventDefault();const index=all.indexOf(active);
   const next=event.key==='Home'?0:event.key==='End'?all.length-1:(index+(event.key==='ArrowRight'?1:-1)+all.length)%all.length;
   all[next].focus();choose(all[next]);
  });
  const pause=()=>root.classList.add('ws-one-look-paused');
  const resume=()=>root.classList.remove('ws-one-look-paused');
  root.addEventListener('mouseenter',pause);root.addEventListener('mouseleave',resume);
  root.addEventListener('focusin',pause);root.addEventListener('focusout',event=>{if(!root.contains(event.relatedTarget))resume()});
 }
})();
