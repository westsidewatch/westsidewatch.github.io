(() => {
  const PROTOCOL = 'dore.a2a.v1';
  const COMMANDS = Object.freeze({
    'health': 'dore.health',
    'stage2': 'design2.stage2.acceptance',
    'tests': 'design2.tests',
    'preview': 'design2.preview'
  });
  let lastCommand = '';
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
      el.title='DORÉ A2A local status';
      document.documentElement.appendChild(el);
    }
    return el;
  }
  function setBadge(text, ok = null) {
    const el=ensureBadge(); el.textContent=text;
    el.style.background=ok===true?'#dfe8c8':ok===false?'#f0c7c7':'#efe4bd';
    el.style.color='#29251e';
  }
  async function runUserCommand(name) {
    const capability=COMMANDS[name];
    if (!capability) { setBadge('DORÉ A2A · UNKNOWN',false); return; }
    setBadge(`DORÉ A2A · ${name.toUpperCase()}…`);
    try {
      const r=await invoke(capability,{});
      const ok=!!(r && r.ok && r.result && r.result.ok !== false);
      setBadge(ok?`DORÉ A2A · ${name.toUpperCase()} PASS`:`DORÉ A2A · ${name.toUpperCase()} FAIL`,ok);
      console.info('[DORÉ A2A user command]',name,r);
    } catch(e) {
      setBadge(`DORÉ A2A · ${name.toUpperCase()} ERROR`,false);
      console.error('[DORÉ A2A user command]',name,e);
    }
  }
  function composerText() {
    const el=document.querySelector('#prompt-textarea') || document.querySelector('textarea[data-testid="prompt-textarea"]');
    if (!el) return '';
    return String('value' in el ? el.value : el.innerText || el.textContent || '').trim();
  }
  function maybeRunCommand() {
    const text=composerText();
    const m=text.match(/^\/dore\s+(health|stage2|tests|preview)\s*$/i);
    if (!m || text===lastCommand) return;
    lastCommand=text;
    runUserCommand(m[1].toLowerCase());
    setTimeout(()=>{ if(lastCommand===text) lastCommand=''; },3000);
  }
  document.addEventListener('keydown',e=>{
    if (e.key==='Enter' && !e.shiftKey && !e.isComposing) maybeRunCommand();
  },true);
  document.addEventListener('click',e=>{
    const b=e.target && e.target.closest && e.target.closest('button[data-testid="send-button"],button[aria-label*="Send"],button[aria-label*="傳送"],button[aria-label*="发送"]');
    if (b) maybeRunCommand();
  },true);
  async function probe() {
    try { const h=await health(); setBadge(h.ok?'DORÉ A2A · LOCAL':'DORÉ A2A · WAIT'); }
    catch (_) { const el=ensureBadge();el.textContent='DORÉ A2A · OFFLINE';el.style.background='#eee';el.style.color='#666'; }
  }
  globalThis.DORE_A2A_COMPANION = Object.freeze({health,invoke,runUserCommand,commands:Object.keys(COMMANDS)});
  probe(); setInterval(probe,30000);
})();
