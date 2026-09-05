(() => {
  const ENDPOINT = 'http://127.0.0.1:4312';
  const PROTOCOL = 'dore.a2a.v1';
  async function call(path, options) {
    const r = await fetch(ENDPOINT + path, options);
    const body = await r.json();
    if (!r.ok || body.ok === false) throw new Error(body.error || `DORÉ HTTP ${r.status}`);
    return body;
  }
  async function health() { return call('/health'); }
  async function invoke(capability, params = {}) {
    if (typeof capability !== 'string' || !capability) throw new Error('invalid_capability');
    return call('/invoke', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({protocol:PROTOCOL,request_id:crypto.randomUUID(),capability,params})});
  }
  // Isolated-world API: intentionally not a general page->extension RPC surface.
  // A small visible status marker is enough to prove the transport is alive.
  async function probe() {
    let el = document.getElementById('dore-a2a-status');
    if (!el) {
      el = document.createElement('div'); el.id='dore-a2a-status';
      Object.assign(el.style,{position:'fixed',right:'12px',bottom:'12px',zIndex:'2147483647',font:'11px system-ui',padding:'5px 8px',borderRadius:'8px',opacity:'.72',pointerEvents:'none'});
      document.documentElement.appendChild(el);
    }
    try { const h=await health(); el.textContent=h.ok?'DORÉ A2A · LOCAL':'DORÉ A2A · WAIT'; el.style.background='#efe4bd';el.style.color='#29251e'; }
    catch (_) { el.textContent='DORÉ A2A · OFFLINE';el.style.background='#eee';el.style.color='#666'; }
  }
  globalThis.DORE_A2A_COMPANION = Object.freeze({health,invoke});
  probe(); setInterval(probe,30000);
})();
