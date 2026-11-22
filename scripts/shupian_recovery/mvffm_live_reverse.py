#!/usr/bin/env python3
"""PARADISO browser reverse-engineering trace for user-supplied video sites.

Passive by default: observe script registrations, iframe creation, popups,
requests and playback metadata. Does NOT bypass access controls, click ads,
download video or block media. Playback click is opt-in via --click-selector.
Requires: pip install playwright; python -m playwright install chromium.
"""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlsplit
import ipaddress

from media_ad_origin import classify

START_URL = "https://www.mvffm.net/drama/420952/"
INJECT = r"""
(() => {
  const marker = "__paradisoReverseEvents";
  if (Object.hasOwn(window, marker)) return;
  const events = [];
  Object.defineProperty(window, marker, {value: events, configurable: false});
  const save = (kind, data) => {
    if (events.length < 1000) {
      events.push({kind, ms: Date.now(), ...data});
    }
  };
  const originalAdd = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function(kind, listener, options) {
    if (["mousedown", "click", "pointerdown"].includes(kind)) {
      const body = typeof listener === "function"
        ? Function.prototype.toString.call(listener) : "";
      const suspicious = /shown_at|window\.open|createElement\(.iframe|location\.|popunder/i.test(body);
      save("listener", {event: kind, target: this === window ? "window"
        : this === document ? "document" : this?.nodeName || "unknown",
        capture: options === true || options?.capture === true,
        mentionsShownAt: body.includes("shown_at"), suspicious});
    }
    return Reflect.apply(originalAdd, this, [kind, listener, options]);
  };
  const originalOpen = window.open;
  window.open = function(...args) {
    let host = "";
    try { host = new URL(String(args[0] || ""), location.href).hostname; } catch {}
    save("window-open", {hostname: host, target: String(args[1] || "")});
    return Reflect.apply(originalOpen, this, args);
  };
  const originalCreate = Document.prototype.createElement;
  Document.prototype.createElement = function(tag, ...args) {
    if (String(tag).toLowerCase() === "iframe") {
      save("iframe-created", {owner: location.hostname});
    }
    return Reflect.apply(originalCreate, this, [tag, ...args]);
  };
  const originalSet = Storage.prototype.setItem;
  Storage.prototype.setItem = function(key, value) {
    if (key === "shown_at") save("ad-timer-set", {key: "shown_at"});
    return Reflect.apply(originalSet, this, [key, value]);
  };
  const originalGet = Storage.prototype.getItem;
  Storage.prototype.getItem = function(key) {
    if (key === "shown_at") save("ad-timer-read", {key: "shown_at"});
    return Reflect.apply(originalGet, this, [key]);
  };
  save("instrumented", {host: location.hostname});
})();
"""

def safe_url_parts(url):
    """Record host/path only, never URL credentials, query tokens or fragments."""
    p = urlsplit(str(url or ""))
    return {"host": p.hostname or "", "path": p.path[:180]}

def validate_target(target):
    p = urlsplit(target)
    if p.scheme != "https" or not p.hostname or p.username or p.password:
        raise ValueError("Only public HTTPS targets are permitted")
    if p.hostname in {"localhost", "localhost.localdomain"} or p.hostname.endswith((".local", ".internal")):
        raise ValueError("Local target rejected")
    try:
        addr = ipaddress.ip_address(p.hostname)
        if not addr.is_global: raise ValueError("Non-public target rejected")
    except ValueError as exc:
        if "rejected" in str(exc): raise
    return target

def summarize_trace(report):
    events = report.get("browser_events", [])
    kinds = {}
    for event in events:
        key = event.get("kind", "unknown")
        kinds[key] = kinds.get(key, 0) + 1
    cross = [x for x in report.get("navigations", [])
             if x.get("host") and x["host"] != report.get("target_host")]
    media = [x for x in report.get("requests", [])
             if x.get("media_candidate")]
    return {"event_counts": kinds,
            "cross_origin_navigations": len(cross),
            "media_request_count": len(media),
            "status": ("PAGE_AD_BEHAVIOR_OBSERVED"
                       if kinds.get("window-open", 0) or cross
                       else "NO_POPUP_OBSERVED_IN_THIS_RUN"),
            "limitation": "No observed popup does not certify no advertising; video frames uninspected"}

async def inspect(url, *, timeout_ms=18000, observe_ms=3000, click_selector=None):
    from playwright.async_api import async_playwright
    validate_target(url)
    result = {"schema": 1, "target": safe_url_parts(url),
              "target_host": urlsplit(url).hostname,
              "at_utc": datetime.now(timezone.utc).isoformat(),
              "browser_events": [], "requests": [], "navigations": [],
              "frames": [], "errors": [], "video_dom": [], "page_html_signals": None,
              "media_verification": "NOT_PERFORMED"}
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=False,
                                            service_workers="block")
        await context.add_init_script(INJECT)
        pages = []
        def handle_page(page):
            pages.append(page)
            page.on("request", lambda request: result["requests"].append({
                **safe_url_parts(request.url),
                "type": request.resource_type,
                "media_candidate": any(x in urlsplit(request.url).path.lower()
                                       for x in (".m3u8", ".mpd", ".mp4", ".ts", ".m4s"))
            }) if len(result["requests"]) < 2500 else None)
            page.on("framenavigated", lambda frame: result["navigations"].append(
                safe_url_parts(frame.url)) if len(result["navigations"]) < 2500 else None)
            page.on("pageerror", lambda error: result["errors"].append(
                "pageerror: " + str(error)[:160]) if len(result["errors"]) < 100 else None)
        context.on("page", handle_page)
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        except Exception as exc:
            result["errors"].append("navigation: " + str(exc)[:250])
        if click_selector:
            try:
                await page.locator(click_selector).first.click(timeout=5000)
            except Exception as exc:
                result["errors"].append("optional-click: " + str(exc)[:250])
        await page.wait_for_timeout(observe_ms)
        try:
            from media_ad_origin import inspect_html
            result["page_html_signals"] = inspect_html(await page.content())
            result["video_dom"] = await page.locator("video").evaluate_all(
                "(els) => els.map(e => ({hasSrc: !!e.currentSrc || !!e.src, paused: e.paused}))")
        except Exception as exc:
            result["errors"].append("dom: " + str(exc)[:160])
        for p in pages:
            for frame in p.frames:
                try:
                    events = await frame.evaluate("window.__paradisoReverseEvents || []")
                    result["browser_events"].extend(
                        dict(e, frame_host=urlsplit(frame.url).hostname)
                        for e in events if isinstance(e, dict))
                except Exception:
                    pass
                if len(result["frames"]) < 300:
                    result["frames"].append(safe_url_parts(frame.url))
        await browser.close()
    result["summary"] = summarize_trace(result)
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default=START_URL)
    p.add_argument("--output", default="shupian-mvffm-live-reverse.json")
    p.add_argument("--timeout-ms", type=int, default=18000)
    p.add_argument("--observe-ms", type=int, default=3000)
    p.add_argument("--click-selector", help="Optional explicit selector to test a play click")
    a = p.parse_args()
    if not 0 <= a.observe_ms <= 60000 or not 1000 <= a.timeout_ms <= 60000:
        p.error("Timeout outside supported limits")
    r = asyncio.run(inspect(a.url, timeout_ms=a.timeout_ms,
                            observe_ms=a.observe_ms,
                            click_selector=a.click_selector))
    Path(a.output).write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    print(json.dumps({"summary": r["summary"], "errors": len(r["errors"]),
                      "output": a.output}, ensure_ascii=False))
    return 0 if not any(x.startswith("navigation:") for x in r["errors"]) else 2

if __name__ == "__main__":
    raise SystemExit(main())
