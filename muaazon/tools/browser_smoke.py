#!/usr/bin/env python3
"""Local-only Twenty/Muaazon browser smoke testing; no credentials or data mutation."""
import json
import os
import pathlib
import sys
from playwright.sync_api import sync_playwright

URL = "http://localhost:3000/welcome"
OUT = pathlib.Path(os.environ.get("MUA_QA_DIR", "qa-evidence"))
OUT.mkdir(parents=True, exist_ok=True)
report = {"base_url": URL, "scenarios": [], "js_errors": []}

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True, args=[
        "--disable-gpu", "--no-first-run", "--disable-extensions",
    ])
    for label, width, height, mobile in [
        ("desktop", 1365, 768, False),
        ("mobile", 390, 844, True),
    ]:
        context = browser.new_context(
            viewport={"width": width, "height": height},
            is_mobile=mobile, has_touch=mobile, device_scale_factor=1,
            reduced_motion="reduce",
        )
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        try:
            response = page.goto(URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(6000)
            title = page.title()
            body = page.locator("body").inner_text(timeout=12000)[:1000]
            file_path = OUT / f"muaazon-{label}.png"
            page.screenshot(path=str(file_path), full_page=False, timeout=16000)
            scenario = {
                "viewport": label, "http": response.status if response else None,
                "url": page.url, "title": title,
                "has_root": page.locator("#root").count() > 0,
                "body_text_length": len(body),
                "horizontal_overflow": page.evaluate(
                    "document.documentElement.scrollWidth > window.innerWidth"
                ),
                "visible_text_excerpt": body[:300],
                "screenshot": str(file_path),
                "javascript_errors": errors[:5],
            }
        except Exception as e:
            scenario = {"viewport": label, "error": str(e)}
        report["scenarios"].append(scenario)
        context.close()
    browser.close()

(OUT / "browser-smoke.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8")
for scenario in report["scenarios"]:
    print(json.dumps(scenario, ensure_ascii=False))
if any(s.get("http") != 200 or not s.get("has_root") or s.get("body_text_length", 0) < 20 or s.get("javascript_errors") for s in report["scenarios"]):
    sys.exit(1)
print("BROWSER_SMOKE_PASS")
