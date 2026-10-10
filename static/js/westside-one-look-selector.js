/* One Look selector: shared interaction contract, realm-owned presentation. */
(()=>{'use strict';
 const roots=document.querySelectorAll('[data-ws-one-look-selector]');
 for(const root of roots){
  const cards=()=>[...root.querySelectorAll('[data-ws-one-look-card]:not([data-ws-one-look-clone])')];
  const choose=(card)=>{
   if(!card||card.hasAttribute('inert')||card.hasAttribute('data-ws-one-look-clone'))return;
   for(const item of cards()){const selected=item===card;item.setAttribute('aria-pressed',String(selected));item.toggleAttribute('data-ws-one-look-selected',selected);}
   const panels=[...document.querySelectorAll('[data-ws-one-look-panel]')].filter(panel=>panel.closest('[data-ws-one-look-selector]')===root || panel.dataset.wsOneLookOwner===root.id);
   for(const panel of panels){const selected=panel.dataset.wsOneLookPanel===card.dataset.wsOneLookCard;panel.hidden=!selected;panel.toggleAttribute('data-ws-one-look-active',selected);}
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
  const initial=cards().find(card=>card.getAttribute('aria-pressed')==='true')||cards()[0];if(initial)choose(initial);
  const pause=()=>root.classList.add('ws-one-look-paused');
  const resume=()=>root.classList.remove('ws-one-look-paused');
  root.addEventListener('mouseenter',pause);root.addEventListener('mouseleave',resume);
  root.addEventListener('focusin',pause);root.addEventListener('focusout',event=>{if(!root.contains(event.relatedTarget))resume()});
 }
})();
