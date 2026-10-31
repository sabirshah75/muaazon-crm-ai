#!/usr/bin/env python3
"""Axe-core automated WCAG A/AA scan of local CRM welcome page."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
axe_path = os.environ["MUA_AXE_JS"]
output = Path(os.environ["MUA_QA_DIR"]);output.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(channel="chrome",headless=True,args=["--no-first-run","--disable-gpu","--disable-extensions"])
    for label,size,mobile in [
        ("desktop",{"width":1365,"height":768},False),
        ("mobile",{"width":390,"height":844},True),
    ]:
        context=browser.new_context(viewport=size,is_mobile=mobile,has_touch=mobile,reduced_motion="reduce")
        page=context.new_page()
        page.goto("http://localhost:3000/welcome",wait_until="domcontentloaded",timeout=30000)
        page.get_by_text("Continue with Email").first.wait_for(timeout=22000)
        page.add_script_tag(path=axe_path)
        raw=page.evaluate("""async () => {
          return await axe.run(document, {
            runOnly:{type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']},
            resultTypes:['violations','incomplete','passes']});
        }""")
        summary={
            "viewport":label,
            "violations":[{"id":v["id"],"impact":v["impact"],
                "description":v["description"],
                "nodes":[{"target":n["target"],"failureSummary":n.get("failureSummary","")[:280]}
                    for n in v["nodes"][:5]]} for v in raw["violations"]],
            "passes":len(raw["passes"]),
            "incomplete":len(raw["incomplete"]),
        }
        results.append(summary)
        context.close()
    browser.close()
(output/"accessibility-axe.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
for item in results:
    print(json.dumps(item,ensure_ascii=False)[:6000])
if any(r["violations"] for r in results):
    print("AXE_WCAG_FAIL")
else:
    print("AXE_WCAG_AUTOMATED_PASS")
