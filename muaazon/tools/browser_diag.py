import json
import sys
from playwright.sync_api import sync_playwright

url = "http://localhost:3000/welcome"
with sync_playwright() as pw:
    browser = pw.chromium.launch(channel="chrome", headless=True,
      args=["--disable-extensions", "--disable-gpu", "--no-first-run"])
    context = browser.new_context(viewport={"width":1200,"height":800})
    page = context.new_page()
    failed=[]
    console=[]
    page.on("requestfailed", lambda req: failed.append({"url":req.url[:150], "failure":req.failure}))
    page.on("pageerror", lambda err: console.append(str(err)[:220]))
    page.on("console", lambda msg: console.append(f"{msg.type}:{msg.text[:180]}") if msg.type=="error" else None)
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=22000)
        page.wait_for_timeout(6000)
        print(json.dumps({
          "url":page.url,"response":response.status if response else None,
          "title":page.title(),
          "bodyLength":len(page.locator("body").inner_text(timeout=5000)),
          "rootLength":len(page.locator("#root").inner_html(timeout=5000)),
          "failed_requests":failed[:12],"console_errors":console[:12],
        }, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"exception":str(exc)[:500],"failed_requests":failed[:12],"console_errors":console[:12]}))
        sys.exit(1)
    finally:
        browser.close()
