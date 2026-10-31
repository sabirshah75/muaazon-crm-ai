#!/usr/bin/env python3
"""Reproducible, minimal Muaazon metadata overlay on Twenty compiled assets.

No JS bundles, licenses or original branding assets are deleted.
Output must be mounted read-only; original release artifacts stay in base/.
"""
import argparse
import json
import pathlib
import re
import sys

def replace_once(content: str, old: str, new: str) -> str:
    if content.count(old) != 1:
        raise ValueError(f"Expected one occurrence of: {old[:80]!r}, found {content.count(old)}")
    return content.replace(old, new, 1)

def apply_branding(base_dir: pathlib.Path, output_dir: pathlib.Path):
    index = (base_dir / "index.html").read_text(encoding="utf-8")
    # The release is built HTML; source index.html references /src/index.tsx.
    if not re.search(r"/assets/index-[^\"\s]+\.js", index):
        raise ValueError("Expected compiled Twenty frontend. Refusing to patch development HTML")
    updates = [
        ("<title>Twenty</title>", "<title>Muaazon CRM AI</title>"),
        ('<meta name="theme-color" content="#000000" />',
         '<meta name="theme-color" content="#152848" />'),
        ('<meta name="description" content="A modern open-source CRM" />',
         '<meta name="description" content="Muaazon CRM AI — internal CRM, powered by Twenty." />'),
        ('<meta property="og:title" content="Twenty" />',
         '<meta property="og:title" content="Muaazon CRM AI" />'),
        ('<meta name="twitter:title" content="Twenty" />',
         '<meta name="twitter:title" content="Muaazon CRM AI" />'),
    ]
    for before, after in updates:
        index = replace_once(index, before, after)
    # Temporary accessibility compatibility bridge until the React source is built.
    # Scoped to the upstream auth page; no network access or credential handling.
    accessibility = """<style id="muaazon-auth-a11y">
      a[href="https://twenty.com/privacy-policy"],
      a[href="https://twenty.com/terms"] {
        color: #595959 !important;
      }
    </style>
    <script id="muaazon-logo-a11y">
    (() => {
      const label = () => {
        const anchor = document.querySelector('a[href="/welcome"]');
        if (anchor && !anchor.textContent.trim() &&
            !anchor.getAttribute('aria-label')) {
          anchor.setAttribute('aria-label', 'Return to CRM welcome');
          return true;
        }
        return Boolean(anchor && anchor.getAttribute('aria-label'));
      };
      const observer = new MutationObserver(() => {
        if (label()) observer.disconnect();
      });
      if (document.documentElement) {
        observer.observe(document.documentElement, {childList: true, subtree: true});
      }
      if (document.readyState === 'loading')
        document.addEventListener('DOMContentLoaded', label, {once: true});
      else label();
      setTimeout(() => observer.disconnect(), 15000);
    })();
    </script>
    """
    index = replace_once(index, "</head>", accessibility + "</head>")
    manifest = json.loads((base_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest.update({
        "name": "Muaazon CRM AI",
        "short_name": "Muaazon CRM",
        "theme_color": "#152848",
    })
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(index, encoding="utf-8")
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return output_dir

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    apply_branding(args.base, args.output)
    print("BRANDING_OVERLAY_PASS")

if __name__ == "__main__":
    main()
