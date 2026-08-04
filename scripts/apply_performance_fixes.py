#!/usr/bin/env python3
from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Custom Web Architecture">
  <rect width="64" height="64" rx="14" fill="#242424"/>
  <path d="M15 18h34v7H22v14h27v7H15z" fill="#f47a3c"/>
  <path d="M27 29h22v7H34v10h-7z" fill="#fff"/>
</svg>
'''

LOGO_B64 = "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..." 

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
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (assets / "cwa-horizontal-black.png").write_bytes(base64.b64decode(LOGO_B64))
    patch_headshot(ROOT / "index.html", "Casey Keown, founder of Custom Web Architecture")
    patch_headshot(ROOT / "about.html", "Casey Keown")
    update_headers()
    print("Applied favicon, logo, responsive headshot, and cache-header optimizations.")


if __name__ == "__main__":
    main()
