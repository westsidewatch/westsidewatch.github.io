#!/usr/bin/env python3
"""Offline Chromium proof that legacy mvffm ad signals are observable at runtime.

Simulated site runs under a network-stubbed origin: no real pages, gambling
domains or media are fetched. This test checks functionality, not live site.
"""
from __future__ import annotations
import asyncio
from urllib.parse import urlsplit

from playwright.async_api import async_playwright
from mvffm_live_reverse import INJECT, summarize_trace

MOCK_HTML = """<!doctype html>
<html><head><title>MVFFM synthetic trace</title></head>
<body><button id="play">Play</button><video id="film" controls></video>
<script>
window.addEventListener("mousedown", function() {
 const shown_at = localStorage.getItem("shown_at");
 if (!shown_at) localStorage.setItem("shown_at", Date.now().toString());
 window.open("https://popup.example/ads?token=sensitive", "_blank");
 const ad = document.createElement("iframe");
 ad.src = "about:blank"; document.body.appendChild(ad);
}, true);
document.getElementById("play").addEventListener("click", () => {
 document.getElementById("film").setAttribute("data-play-attempt", "yes");
});
</script></body></html>"""

async def smoke():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(service_workers="block")
        await context.add_init_script(INJECT)
        async def route(request):
            if urlsplit(request.request.url).hostname == "www.mvffm.net":
                await request.fulfill(status=200, content_type="text/html", body=MOCK_HTML)
            else:
                await request.abort()
        await context.route("**/*", route)
        page = await context.new_page()
        await page.goto("https://www.mvffm.net/drama/420952/", wait_until="domcontentloaded")
        await page.locator("#play").dispatch_event("mousedown")
        await page.locator("#play").click()
        events = await page.evaluate("window.__paradisoReverseEvents || []")
        types = [e.get("kind") for e in events]
        assert "listener" in types, types
        assert "ad-timer-read" in types, types
        assert "ad-timer-set" in types, types
        assert "window-open" in types, types
        assert "iframe-created" in types, types
        assert await page.locator("#film").get_attribute("data-play-attempt") == "yes"
        summary = summarize_trace({"browser_events":events})
        assert summary["status"] == "PAGE_AD_BEHAVIOR_OBSERVED", summary
        await browser.close()
        print("PASS: browser event reverse instrumentation observes ad chain without suppressing play control")

if __name__ == "__main__":
    asyncio.run(smoke())
