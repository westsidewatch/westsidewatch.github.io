import { resourceWork } from '../../js/resource-fabric-client.mjs';

/**
 * Bridge the lightweight collection surface back to the canonical Dawn Work.
 * Cover-preview objects stay presentation-only; Reader always receives the
 * Resource Fabric / canonical projection so reading resolution keeps one identity.
 */
export function installCoverReaderBridge({choose,scrollToReader=true}={}){
  if(typeof choose!=='function')throw new TypeError('installCoverReaderBridge requires choose(work)');
  let ticket=0;
  const onSelect=async event=>{
    const preview=event?.detail?.work;
    const workId=preview?.workId;
    if(!workId)return;
    const mine=++ticket;
    document.documentElement.dataset.dawnCoverSelection='resolving';
    try{
      const work=await resourceWork(workId);
      if(mine!==ticket)return;
      if(!work)throw new Error(`canonical Work not found: ${workId}`);
      await choose(work);
      if(mine!==ticket)return;
      document.documentElement.dataset.dawnCoverSelection='ready';
      document.documentElement.dataset.dawnSelectedWork=workId;
      if(scrollToReader)document.querySelector('#library-top .right')?.scrollIntoView({behavior:'smooth',block:'start'});
    }catch(error){
      if(mine!==ticket)return;
      document.documentElement.dataset.dawnCoverSelection='error';
      console.error('[Dawn Library] cover → reader bridge failed',error);
    }
  };
  window.addEventListener('dawn:cover-select',onSelect);
  return ()=>window.removeEventListener('dawn:cover-select',onSelect);
}
