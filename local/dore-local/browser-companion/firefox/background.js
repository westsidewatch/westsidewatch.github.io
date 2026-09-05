const ENDPOINT = 'http://127.0.0.1:4312';
const PROTOCOL = 'dore.a2a.v1';

async function call(path, options = undefined) {
  const r = await fetch(ENDPOINT + path, options);
  const body = await r.json();
  if (!r.ok || body.ok === false) throw new Error(body.error || `DORÉ HTTP ${r.status}`);
  return body;
}

browser.runtime.onMessage.addListener(async (msg, sender) => {
  if (!sender.tab || !sender.tab.url || !sender.tab.url.startsWith('https://chatgpt.com/')) {
    throw new Error('unauthorized_sender');
  }
  if (!msg || msg.protocol !== PROTOCOL) throw new Error('invalid_protocol');
  if (msg.type === 'health') return call('/health');
  if (msg.type === 'invoke') {
    if (typeof msg.capability !== 'string' || !msg.capability) throw new Error('invalid_capability');
    return call('/invoke', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        protocol: PROTOCOL,
        request_id: msg.request_id || crypto.randomUUID(),
        capability: msg.capability,
        params: msg.params && typeof msg.params === 'object' ? msg.params : {}
      })
    });
  }
  throw new Error('unsupported_message');
});
