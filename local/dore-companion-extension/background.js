/* DORÉ Companion 1.3 background bridge. */

let transportModulePromise = null;

function transportModule() {
  if (!transportModulePromise) {
    transportModulePromise = import(browser.runtime.getURL("native_transport.js"));
  }
  return transportModulePromise;
}

function envelopeFromCommand(command) {
  const normalized = String(command || "").trim().toLowerCase();

  // Stage 2 is the frozen live diagnostic contract.  Keep it deliberately
  // outside the typed dispatch envelope so already-installed Native Hosts can
  // reach their legacy compatibility path instead of failing typed transport
  // validation on request/session fields that this diagnostic does not need.
  if (normalized === "/dore stage2" || normalized === "dore stage2") {
    return {
      command,
      source: "chatgpt-companion-1.3",
      client: {
        name: "dore-companion",
        version: "1.3.0",
        transport_preference: "firefox-native-messaging"
      }
    };
  }

  return {
    protocol: "dore.a2a/1",
    command,
    source: "chatgpt-companion-1.3",
    client: {
      name: "dore-companion",
      version: "1.3.0",
      transport_preference: "firefox-native-messaging"
    }
  };
}

async function probeHealth() {
  try {
    const transport = await transportModule();
    const result = await transport.nativeHealth();
    return {
      online: Boolean(result && result.ok),
      transport: result && result.transport ? result.transport : "unknown",
      result
    };
  } catch (error) {
    return {
      online: false,
      transport: "unavailable",
      error: String(error && error.message ? error.message : error)
    };
  }
}

browser.runtime.onMessage.addListener((message) => {
  if (!message || typeof message !== "object") return undefined;

  if (message.type === "dore.health") {
    return probeHealth();
  }

  if (message.type === "dore.command") {
    const command = String(message.command || "").trim();
    if (!command.toLowerCase().startsWith("/dore")) {
      return Promise.resolve({ ok: false, ignored: true, reason: "not-a-dore-command" });
    }

    return transportModule()
      .then((transport) => transport.sendDorePayload(envelopeFromCommand(command)))
      .then((result) => ({ ok: true, result }))
      .catch((error) => ({
        ok: false,
        error: String(error && error.message ? error.message : error)
      }));
  }

  return undefined;
});
