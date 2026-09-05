/* DORÉ Companion 1.0 ChatGPT content script. */

const BADGE_ID = "dore-a2a-companion-status";
let lastCommand = "";
let lastCommandAt = 0;
let healthTimer = null;

function ensureBadge() {
  let badge = document.getElementById(BADGE_ID);
  if (badge) return badge;

  badge = document.createElement("div");
  badge.id = BADGE_ID;
  badge.textContent = "DORÉ A2A · CHECKING";
  badge.setAttribute("role", "status");
  badge.style.cssText = [
    "position:fixed",
    "right:14px",
    "bottom:14px",
    "z-index:2147483647",
    "padding:6px 9px",
    "border-radius:999px",
    "font:600 11px/1.2 -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif",
    "letter-spacing:.04em",
    "background:rgba(20,20,20,.88)",
    "color:#d7bd72",
    "border:1px solid rgba(215,189,114,.55)",
    "box-shadow:0 2px 12px rgba(0,0,0,.18)",
    "pointer-events:none"
  ].join(";");
  document.documentElement.appendChild(badge);
  return badge;
}

function setBadge(state, detail) {
  const badge = ensureBadge();
  const normalized = String(state || "OFFLINE").toUpperCase();
  badge.textContent = `DORÉ A2A · ${normalized}`;
  if (detail) badge.title = detail;
  if (normalized === "ONLINE" || normalized === "PASS") {
    badge.style.opacity = "1";
  } else if (normalized === "WORKING") {
    badge.style.opacity = ".9";
  } else {
    badge.style.opacity = ".72";
  }
}

async function refreshHealth() {
  try {
    const reply = await browser.runtime.sendMessage({ type: "dore.health" });
    if (reply && reply.online) {
      setBadge("ONLINE", `transport: ${reply.transport || "native"}`);
    } else {
      setBadge("OFFLINE", reply && reply.error ? reply.error : "DORÉ native host unavailable");
    }
  } catch (error) {
    setBadge("OFFLINE", String(error && error.message ? error.message : error));
  }
}

function valueFromEditable(target) {
  if (!target) return "";
  if (target instanceof HTMLTextAreaElement || target instanceof HTMLInputElement) {
    return target.value || "";
  }
  const editable = target.closest && target.closest('[contenteditable="true"]');
  if (editable) return editable.innerText || editable.textContent || "";
  return "";
}

function findComposerValue() {
  const textarea = document.querySelector('textarea');
  if (textarea && textarea.value) return textarea.value;
  const editables = Array.from(document.querySelectorAll('[contenteditable="true"]'));
  for (const node of editables) {
    const text = (node.innerText || node.textContent || "").trim();
    if (text) return text;
  }
  return "";
}

async function dispatchCommand(raw) {
  const command = String(raw || "").trim();
  if (!command.toLowerCase().startsWith("/dore")) return;

  const now = Date.now();
  if (command === lastCommand && now - lastCommandAt < 2000) return;
  lastCommand = command;
  lastCommandAt = now;
  setBadge("WORKING", command);

  try {
    const reply = await browser.runtime.sendMessage({ type: "dore.command", command });
    if (reply && reply.ok && reply.result) {
      const result = reply.result;
      const status = String(result.status || (result.ok ? "PASS" : "ONLINE")).toUpperCase();
      setBadge(status === "COMPLETED" ? "PASS" : status, JSON.stringify(result));
      window.dispatchEvent(new CustomEvent("dore:a2a-result", { detail: result }));
    } else {
      setBadge("OFFLINE", reply && reply.error ? reply.error : "DORÉ command failed");
    }
  } catch (error) {
    setBadge("OFFLINE", String(error && error.message ? error.message : error));
  }
}

// Capture Enter before ChatGPT clears the composer, but never block ChatGPT itself.
document.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" || event.shiftKey || event.isComposing) return;
  const command = valueFromEditable(event.target);
  if (command.trim().toLowerCase().startsWith("/dore")) {
    queueMicrotask(() => dispatchCommand(command));
  }
}, true);

// Also cover mouse/touch send actions.
document.addEventListener("click", (event) => {
  const button = event.target && event.target.closest ? event.target.closest("button") : null;
  if (!button) return;
  const label = `${button.getAttribute("aria-label") || ""} ${button.getAttribute("data-testid") || ""}`.toLowerCase();
  if (!label.includes("send") && !label.includes("submit")) return;
  const command = findComposerValue();
  if (command.trim().toLowerCase().startsWith("/dore")) {
    queueMicrotask(() => dispatchCommand(command));
  }
}, true);

ensureBadge();
refreshHealth();
healthTimer = window.setInterval(refreshHealth, 10000);
window.addEventListener("beforeunload", () => {
  if (healthTimer) window.clearInterval(healthTimer);
}, { once: true });
