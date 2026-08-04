#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Custom Web Architecture">
  <rect width="64" height="64" rx="14" fill="#242424"/>
  <path d="M15 18h34v7H22v14h27v7H15z" fill="#f47a3c"/>
  <path d="M27 29h22v7H34v10h-7z" fill="#fff"/>
</svg>
'''

LOGO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 100" role="img" aria-label="Custom Web Architecture">
  <g fill="#242424">
    <path d="M8 12h72v14H24v48h56v14H8z"/>
    <path d="M38 38h42v14H52v36H38z"/>
    <text x="105" y="64" font-family="Arial, Helvetica, sans-serif" font-size="40" font-weight="700" letter-spacing="-1">Custom Web Architecture</text>
  </g>
</svg>
'''

PICTURE = '''<picture>
            <source type="image/webp" srcset="/assets/headshot-640.webp 640w, /assets/headshot-960.webp 960w" sizes="(max-width: 768px) 80vw, 32vw">
            <img src="/assets/headshot-640.jpg" srcset="/assets/headshot-640.jpg 640w, /assets/headshot-960.jpg 960w" sizes="(max-width: 768px) 80vw, 32vw" alt="{alt}" width="640" height="962" loading="eager" fetchpriority="high" decoding="async">
          </picture>'''


def patch_headshot(path: Path, alt: str) -> None:
    text = path.read_text(encoding="utf-8")
    pattern = r'<img\s+src="/assets/headshot\.jpg"\s+alt="[^"]*"\s+loading="lazy">'
    updated, count = re.subn(pattern, PICTURE.format(alt=alt), text, count=1)
    if count != 1 and "/assets/headshot-640.webp" not in text:
        raise RuntimeError(f"Could not find hero headshot in {path}")
    path.write_text(updated if count else text, encoding="utf-8")


def replace_logo_references() -> None:
    targets = list(ROOT.glob("*.html")) + list((ROOT / "blog").rglob("*.html"))
    targets += [ROOT / "scripts" / "build_blog.py", ROOT / "scripts" / "build_blog_index.py"]
    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("/assets/cwa-horizontal-black.png", "/assets/cwa-horizontal-black.svg")
        path.write_text(text, encoding="utf-8")


def update_headers() -> None:
    path = ROOT / "_headers"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    block = '''

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/css/*
  Cache-Control: public, max-age=31536000, immutable

/scripts/*
  Cache-Control: public, max-age=31536000, immutable
'''
    if "/assets/*" not in text:
        text = text.rstrip() + block
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (ASSETS / "cwa-horizontal-black.svg").write_text(LOGO, encoding="utf-8")
    patch_headshot(ROOT / "index.html", "Casey Keown, founder of Custom Web Architecture")
    patch_headshot(ROOT / "about.html", "Casey Keown")
    replace_logo_references()
    update_headers()
    print("Applied lightweight favicon and logo, responsive hero images, and long-lived asset caching.")


if __name__ == "__main__":
    main()
