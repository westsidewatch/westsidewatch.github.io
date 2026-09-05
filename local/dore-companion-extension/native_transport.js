/* DORÉ Companion transport.
 * Production path: Firefox Native Messaging -> ca.dore.companion.
 * Compatibility path: localhost:4312 only when the native host is unavailable.
 *
 * This module owns transport only. Existing ChatGPT-page capture logic should
 * pass the already-formed Companion payload to sendDorePayload().
 */

const DORE_NATIVE_HOST = "ca.dore.companion";
const DORE_FALLBACK_URL = "http://127.0.0.1:4312/a2a";

let nativePort = null;
let nativeUnavailable = false;
const pending = new Map();
let sequence = 0;

function nextTransportId() {
  sequence += 1;
  return `dore-native-${Date.now()}-${sequence}`;
}

function ensureNativePort() {
  if (nativePort) return nativePort;
  if (nativeUnavailable) return null;

  try {
    nativePort = browser.runtime.connectNative(DORE_NATIVE_HOST);
  } catch (error) {
    nativeUnavailable = true;
    console.warn("[DORÉ] Native Messaging unavailable; 4312 fallback enabled", error);
    return null;
  }

  nativePort.onMessage.addListener((message) => {
    const id = message && message.__dore_transport_id;
    if (id && pending.has(id)) {
      const entry = pending.get(id);
      pending.delete(id);
      const clean = { ...message };
      delete clean.__dore_transport_id;
      entry.resolve(clean);
      return;
    }

    // Native host responses may preserve the A2A request_id rather than the
    // private carrier id. Resolve the oldest request; the port is serialized by
    // this module, so this remains deterministic for current Companion usage.
    const first = pending.entries().next();
    if (!first.done) {
      const [key, entry] = first.value;
      pending.delete(key);
      entry.resolve(message);
    }
  });

  nativePort.onDisconnect.addListener(() => {
    const error = browser.runtime.lastError;
    nativePort = null;
    nativeUnavailable = true;
    for (const [, entry] of pending) {
      entry.reject(error || new Error("DORÉ native host disconnected"));
    }
    pending.clear();
    console.warn("[DORÉ] Native host disconnected; 4312 fallback enabled", error || "");
  });

  return nativePort;
}

async function sendViaNative(payload) {
  const port = ensureNativePort();
  if (!port) throw new Error("native host unavailable");

  const transportId = nextTransportId();
  return new Promise((resolve, reject) => {
    pending.set(transportId, { resolve, reject });
    try {
      port.postMessage({ ...payload, __dore_transport_id: transportId });
    } catch (error) {
      pending.delete(transportId);
      reject(error);
    }
  });
}

async function sendVia4312(payload) {
  const response = await fetch(DORE_FALLBACK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    body: JSON.stringify(payload),
  });
  const body = await response.json();
  if (!response.ok) {
    throw new Error(body && body.error ? String(body.error) : `DORÉ 4312 HTTP ${response.status}`);
  }
  return body;
}

export async function sendDorePayload(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    throw new TypeError("DORÉ Companion payload must be an object");
  }

  try {
    return await sendViaNative(payload);
  } catch (nativeError) {
    console.warn("[DORÉ] Falling back to localhost:4312", nativeError);
    return sendVia4312(payload);
  }
}

export async function nativeHealth() {
  return sendDorePayload({ action: "native.health" });
}

export function resetNativeTransportForRetry() {
  nativeUnavailable = false;
  if (nativePort) {
    try { nativePort.disconnect(); } catch (_) {}
  }
  nativePort = null;
}
