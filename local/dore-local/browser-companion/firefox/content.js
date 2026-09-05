(() => {
  const PROTOCOL = 'dore.a2a.v1';
  function send(msg) { return browser.runtime.sendMessage({protocol:PROTOCOL,...msg}); }
  async function health() { return send({type:'health'}); }
  async function invoke(capability, params = {}) {
    if (typeof capability !== 'string' || !capability) throw new Error('invalid_capability');
    return send({type:'invoke',request_id:crypto.randomUUID(),capability,params});
  }
  function ensureBadge() {
    let el=document.getElementById('dore-a2a-status');
    if (!el) {
      el=document.createElement('button'); el.id='dore-a2a-status'; el.type='button';
      Object.assign(el.style,{position:'fixed',right:'12px',bottom:'12px',zIndex:'2147483647',font:'11px system-ui',padding:'5px 8px',border:'0',borderRadius:'8px',opacity:'.82',cursor:'pointer'});
      el.title='Click to run DORÉ A2A capability gate';
      el.addEventListener('click', async () => {
        el.disabled=true;el.textContent='DORÉ A2A · TESTING';
        try {
          const r=await invoke('design2.stage2.acceptance',{});
          const ok=!!(r && r.ok && r.result && r.result.ok);
          el.textContent=ok?'DORÉ A2A · GATE PASS':'DORÉ A2A · GATE FAIL';
          el.style.background=ok?'#dfe8c8':'#f0c7c7';el.style.color='#29251e';
          console.info('[DORÉ A2A gate]',r);
        } catch (e) {
          el.textContent='DORÉ A2A · GATE ERROR';el.style.background='#f0c7c7';el.style.color='#29251e';console.error('[DORÉ A2A gate]',e);
        } finally {el.disabled=false;}
      });
      document.documentElement.appendChild(el);
    }
    return el;
  }
  async function probe() {
    const el=ensureBadge();
    try { const h=await health(); el.textContent=h.ok?'DORÉ A2A · LOCAL':'DORÉ A2A · WAIT'; el.style.background='#efe4bd';el.style.color='#29251e'; }
    catch (_) { el.textContent='DORÉ A2A · OFFLINE';el.style.background='#eee';el.style.color='#666'; }
  }
  globalThis.DORE_A2A_COMPANION = Object.freeze({health,invoke});
  probe(); setInterval(probe,30000);
})();
