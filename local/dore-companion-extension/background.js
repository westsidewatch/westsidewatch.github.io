/* DORÉ Companion 1.4 production A2A bridge. */

let transportModulePromise = null;
let sequence = 0;
const sessionId = `session-${crypto.randomUUID()}`;

function transportModule() {
  if (!transportModulePromise) transportModulePromise = import(browser.runtime.getURL("native_transport.js"));
  return transportModulePromise;
}

function conversationId() {
  const match = locationFromSender || "chatgpt";
  return match;
}
let locationFromSender = "chatgpt";

function nextRequestId() {
  sequence += 1;
  return `req-${Date.now()}-${sequence}-${crypto.randomUUID()}`;
}

function client() {
  return { name: "dore-companion", version: "1.4.0", transport_preference: "firefox-native-messaging" };
}

function envelopeFromCommand(command, context = {}) {
  const raw = String(command || "").trim();
  const normalized = raw.toLowerCase();
  if (normalized === "/dore stage2" || normalized === "dore stage2") {
    return { command: raw, source: "chatgpt-companion-1.4", client: client() };
  }

  if (normalized === "/dore design" || normalized === "/dore design live") {
    return {
      protocol: "dore.a2a/1",
      action: "dispatch",
      request_id: nextRequestId(),
      conversation_id: String(context.conversation_id || "chatgpt-unknown"),
      session_id: sessionId,
      consumer_id: "design",
      capability_id: "design.compose",
      payload: {
        asset_candidate: {
          asset_id: "a2a:production-live-gate",
          provider: "dore-control-plane",
          kind: "typed-live-gate",
          rendered: false,
          claim_boundary: "production A2A control-plane live gate"
        }
      },
      source: "chatgpt-companion-1.4",
      client: client()
    };
  }

  return { protocol: "dore.a2a/1", command: raw, source: "chatgpt-companion-1.4", client: client() };
}

async function probeHealth() {
  try {
    const transport = await transportModule();
    const result = await transport.nativeHealth();
    return { online: Boolean(result && result.ok), transport: result && result.transport ? result.transport : "unknown", result };
  } catch (error) {
    return { online: false, transport: "unavailable", error: String(error && error.message ? error.message : error) };
  }
}

browser.runtime.onMessage.addListener((message, sender) => {
  if (!message || typeof message !== "object") return undefined;
  if (message.type === "dore.health") return probeHealth();
  if (message.type === "dore.command") {
    const command = String(message.command || "").trim();
    if (!command.toLowerCase().startsWith("/dore")) return Promise.resolve({ ok: false, ignored: true, reason: "not-a-dore-command" });
    const context = { conversation_id: String(message.conversation_id || (sender && sender.tab && sender.tab.url) || "chatgpt-unknown") };
    return transportModule()
      .then((transport) => transport.sendDorePayload(envelopeFromCommand(command, context)))
      .then((result) => ({ ok: result && result.status !== "failed", result, stage: "control-plane" }))
      .catch((error) => ({ ok: false, stage: "transport", error: String(error && error.message ? error.message : error) }));
  }
  return undefined;
});
