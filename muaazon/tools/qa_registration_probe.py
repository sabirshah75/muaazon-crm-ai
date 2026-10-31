#!/usr/bin/env python3
"""Synthetic-only local CRM registration probe; does not use customer data."""
import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
 b=p.chromium.launch(channel='chrome',headless=True,args=['--disable-gpu','--disable-extensions'])
 x=b.new_page()
 events=[]
 x.on('pageerror',lambda e: events.append(str(e)[:140]))
 x.goto('http://localhost:3000/welcome',wait_until='domcontentloaded',timeout=30000)
 x.get_by_text('Continue with Email').first.click(timeout=22000)
 x.get_by_placeholder('Email').fill('muaazon-qa@example.test')
 x.get_by_role('button',name='Continue').click(timeout=22000)
 x.wait_for_timeout(4000)
 print(json.dumps({
  'url':x.url,'text':x.locator('body').inner_text()[:600],
  'inputs':x.locator('input').evaluate_all("(nodes)=>nodes.map(n=>({type:n.type,placeholder:n.placeholder}))"),
  'buttons':x.locator('button').all_inner_texts()[:12],
  'page_errors':events,
 },ensure_ascii=False))
 b.close()
