from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch(channel="chrome",headless=True,args=["--disable-extensions","--disable-gpu"])
 x=b.new_page()
 x.goto("http://localhost:3000/welcome",wait_until="domcontentloaded",timeout=30000)
 x.get_by_text("Continue with Email").first.wait_for(timeout=20000)
 for selector in ['.uexihlt','a[target="_blank"][rel="noopener noreferrer"]','a[href$="terms"]']:
  print('SELECTOR',selector)
  for node in x.locator(selector).all()[:3]:
   print(node.evaluate('e=>({outer:e.outerHTML.slice(0,1200),parent:e.parentElement.outerHTML.slice(0,2000),color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor})'))
 b.close()
