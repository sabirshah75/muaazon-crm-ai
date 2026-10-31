#!/usr/bin/env python3
"""Interact with the local CRM sign-in screen without submitting personal data."""
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome",headless=True,args=["--disable-gpu","--no-first-run","--disable-extensions"])
    context = browser.new_context(viewport={"width":1280,"height":820},reduced_motion="reduce")
    page = context.new_page()
    errors=[]
    page.on("pageerror",lambda e: errors.append(str(e)[:180]))
    response = page.goto("http://localhost:3000/welcome",wait_until="domcontentloaded",timeout=30000)
    page.get_by_text("Continue with Email").first.click(timeout=20000)
    page.wait_for_timeout(1500)
    output = {
      "http": response.status if response else None,
      "url": page.url, "title": page.title(),
      "text": page.locator("body").inner_text(timeout=10000)[:900],
      "inputs": page.locator("input").evaluate_all("(nodes)=>nodes.map(n=>({type:n.type,placeholder:n.placeholder,ariaLabel:n.getAttribute('aria-label')}))"),
      "buttons": page.locator("button").all_inner_texts()[:16],
      "pageErrors":errors
    }
    print(json.dumps(output,ensure_ascii=False))
    browser.close()
